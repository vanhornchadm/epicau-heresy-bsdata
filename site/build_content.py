"""Build the Quartz site's Markdown from the BattleScribe data, README and git history.

Usage: python3 build_content.py [content_dir]
Reads the .gst/.cat files in the repo root (the published data, not the specs), so every page
shows what BattleScribe shows. Writes armies/, rules/, the roster rules, design notes, backlog
and changelog pages into content_dir (default: site/content), which it empties first.
"""
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

from sources import SOURCES, ENTRY_SOURCES, EPICAU_RULE_SOURCES

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'content')
REPO_URL = 'https://github.com/vanhornchadm/epicau-heresy-bsdata'
GST_FILE = 'Epic Armageddon - EpicAU Horus Heresy.gst'

UNIT_TYPES = {'Unit', 'War Engine'}
UNIT_CHARS = ['Type', 'Speed', 'Armour', 'CC', 'FF']
WAR_ENGINE_CHARS = ['Damage Capacity', 'Void Shields', 'Critical Hit']
# Units added from Departmento Munitorum to fill wiki gaps: not fan-made, but not on the wiki either
MUNITORUM = {'Sabre Strike Tank', 'Solar Auxilia Tank Hunter Squadron'}
# Groups that hold a formation's upgrades rather than its units
UPGRADE_GROUPS = {'Upgrades', 'Free upgrades'}
# Prefixes dropped when matching README labels to entries ("Legion Tarantula Battery" -> "Tarantula Battery")
PREFIXES = ('Legion ', 'Solar Auxilia ', 'Imperial Navy ', 'Auxilia ')


# --- loading ---------------------------------------------------------------------------------------

def load(path):
    root = ET.parse(path).getroot()
    for el in root.iter():
        el.tag = el.tag.split('}')[-1]
    return root


GST = load(os.path.join(ROOT, GST_FILE))
CATS = {}  # army name -> catalogue root
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.cat'):
        CATS[f[len('EpicAU - '):-len('.cat')]] = load(os.path.join(ROOT, f))

PROFILES, RULES, ENTRIES, GROUPS = {}, {}, {}, {}
for root in [GST, *CATS.values()]:
    for el in root.iter('profile'):
        PROFILES[el.get('id')] = el
    for el in root.iter('rule'):
        RULES[el.get('id')] = el
    for el in root.iter('selectionEntry'):
        ENTRIES[el.get('id')] = el
    for el in root.iter('selectionEntryGroup'):
        GROUPS[el.get('id')] = el


def fan(name):
    return name.endswith('*') or '*)' in name


def plain(name):
    """The name without its fan-made asterisk."""
    return name.replace('*', '')


def filename(name):
    return re.sub(r'[\\/:#?"<>|]', '-', plain(name)).strip()


def pts(el):
    c = el.find("costs/cost[@typeId='points']")
    return float(c.get('value')) if c is not None else 0.0


def fmt_pts(v):
    return f'{int(v)}' if v == int(v) else f'{v:g}'


def limits(el):
    """(min, max) from the entry's own parent-scope selection constraints; None where unset."""
    lo = hi = None
    for c in el.findall('constraints/constraint'):
        if c.get('field') != 'selections' or c.get('scope') != 'parent':
            continue
        v = int(float(c.get('value')))
        if c.get('type') == 'min':
            lo = v
        elif c.get('type') == 'max':
            hi = v
    return lo, hi


def count_text(lo, hi):
    if (lo is None and hi is None) or hi == 0:  # max 0 is raised by a modifier, e.g. the fan-made toggle
        return ''
    if lo == hi:
        return f'{lo}'
    if hi is None or hi < 0:
        return f'{lo or 0}+'
    return f'{lo or 0}-{hi}'


def chars(profile):
    return {c.get('name'): (c.text or '').strip() for c in profile.findall('characteristics/characteristic')}


def resolve(el):
    """An entryLink's target, or the element itself."""
    if el.tag == 'entryLink':
        return (ENTRIES if el.get('type') == 'selectionEntry' else GROUPS).get(el.get('targetId'))
    return el


def own_profiles(el):
    out = [p for p in el.findall('profiles/profile')]
    out += [PROFILES[i.get('targetId')] for i in el.findall('infoLinks/infoLink')
            if i.get('type') == 'profile' and i.get('targetId') in PROFILES]
    return out


def own_rules(el):
    out = [r for r in el.findall('rules/rule')]
    out += [RULES[i.get('targetId')] for i in el.findall('infoLinks/infoLink')
            if i.get('type') == 'rule' and i.get('targetId') in RULES]
    return out


def children(el):
    """Child entries and groups in document order, with entryLinks resolved."""
    for tag in ('selectionEntries/selectionEntry', 'selectionEntryGroups/selectionEntryGroup',
                'entryLinks/entryLink'):
        for c in el.findall(tag):
            t = resolve(c)
            if t is not None:
                yield c, t


def unit_profile(el):
    return next((p for p in own_profiles(el) if p.get('typeName') in UNIT_TYPES), None)


def is_weapon_option(el):
    """A pick that only adds Weapon profiles (a weapon choice or Titan weapon)."""
    profs = own_profiles(el)
    return (el.get('type') == 'upgrade' and profs and all(p.get('typeName') == 'Weapon' for p in profs)
            and not list(children(el)))


# --- collecting what's new ------------------------------------------------------------------------

class Model:
    """A unit with a Unit or War Engine profile, merged over every place it appears."""

    def __init__(self, army, el):
        self.army, self.el, self.name = army, el, el.get('name')
        self.profile = unit_profile(el)
        self.places = {}  # (kind, name) -> cost text

    @property
    def new(self):
        return fan(self.name) or plain(self.name) in MUNITORUM


class Entry:
    """A formation, upgrade or Titan weapon page."""

    def __init__(self, army, kind, el, parent=None):
        self.army, self.kind, self.el, self.name = army, kind, el, el.get('name')
        self.parents = set([parent] if parent else [])


MODELS = {}  # (army, name) -> Model
FORMATIONS = {}  # (army, name) -> Entry; fan-made, Munitorum, or holding a new unit
UPGRADES = {}  # (army, name) -> Entry; fan-made upgrades
WEAPONS = {}  # (army, name) -> Entry; fan-made Titan weapons
RULE_USERS = defaultdict(set)  # rule name -> {(army, model or entry name, new?)}


def walk(army, top, el, in_upgrades=False, upgrade=None):
    """Record every model, upgrade and weapon under a formation, and the rules they use."""
    for link, t in children(el):
        name = t.get('name')
        if t.tag == 'selectionEntryGroup':
            walk(army, top, t, in_upgrades or name in UPGRADE_GROUPS, upgrade)
            continue
        if is_weapon_option(t):
            if fan(name):
                WEAPONS.setdefault((army, name), Entry(army, 'weapon', t)).parents.add(top.get('name'))
            continue
        if in_upgrades and t.get('type') == 'upgrade' and not unit_profile(t):
            if fan(name):
                UPGRADES.setdefault((army, name), Entry(army, 'upgrade', t)).parents.add(top.get('name'))
            walk(army, top, t, in_upgrades, upgrade or name)
            continue
        if unit_profile(t) is not None:
            m = MODELS.setdefault((army, name), Model(army, t))
            if upgrade:
                m.places[('upgrade', upgrade)] = None
            else:
                m.places[('formation', top.get('name'))] = None
        walk(army, top, t, in_upgrades, upgrade)


TOP = {}  # (army, name) -> formation element, first copy (Legion formations repeat per Legion)
for army, root in CATS.items():
    for el in root.findall('selectionEntries/selectionEntry') + root.findall('sharedSelectionEntries/selectionEntry'):
        if el.get('type') != 'unit':
            continue
        TOP.setdefault((army, el.get('name')), el)
        walk(army, el, el)

# Rules used by every unit, so a rule only fan-made units use counts as new
for m in MODELS.values():
    for r in own_rules(m.el) + [r for _, t in children(m.el) for r in own_rules(t)]:
        RULE_USERS[r.get('name')].add((m.army, m.name, m.new))
for e in list(UPGRADES.values()) + list(WEAPONS.values()):
    for r in own_rules(e.el):
        RULE_USERS[r.get('name')].add((e.army, e.name, True))
NEW_MODELS = {k: m for k, m in MODELS.items() if m.new}
for m in NEW_MODELS.values():  # EpicAU formations that gained a new unit get a page too

    for kind, name in m.places:
        if kind == 'formation':
            FORMATIONS.setdefault((m.army, name), Entry(m.army, 'formation', TOP[(m.army, name)]))
for (army, name), el in TOP.items():
    if fan(name) or plain(name) in MUNITORUM:
        FORMATIONS.setdefault((army, name), Entry(army, 'formation', el))


MODEL_NAMES = {name for _, name in MODELS}


def unit_specific(rule_name, owner=None):
    """Rules shown on their owner's page: named after their unit or upgrade, such as 'Critical Hit (Ascalon*)',
    or a weapon's overflow notes."""
    m = re.search(r'\((.+)\)$', rule_name)
    return (rule_name == owner or rule_name.endswith(' notes')  # '<weapon> notes': a weapon cell too long for the table
            or bool(m and (m.group(1) in MODEL_NAMES or m.group(1) == owner)))


def is_new_rule(name):
    users = RULE_USERS.get(name, ())
    return bool(users) and all(new for _, _, new in users)


# --- README sections -----------------------------------------------------------------------------

README = open(os.path.join(ROOT, 'README.md')).read()


def section(text, heading):
    m = re.search(rf'^## {re.escape(heading)}\n(.*?)(?=^## |\Z)', text, re.S | re.M)
    return m.group(1).strip() if m else ''


def bullets(text):
    """Top-level '- ' bullets with their indented children, as (first line, full text, [child bullets])."""
    out, cur = [], None
    for line in text.split('\n'):
        if line.startswith('- '):
            cur = [line]
            out.append(cur)
        elif cur is not None and (line.startswith('  ') or not line.strip()):
            cur.append(line)
        else:
            cur = None
    result = []
    for b in out:
        body = '\n'.join(b).rstrip()
        kids = []
        for line in b[1:]:
            if re.match(r'^  - ', line):
                kids.append([line])
            elif kids and line.startswith('    '):
                kids[-1].append(line)
        result.append((b[0], body, ['\n'.join(k) for k in kids]))
    return result


def label(line):
    m = re.match(r'^\s*- \*\*(.+?)\*\*', line)
    return plain(m.group(1)) if m else ''


DECISIONS = bullets(section(README, 'Data decisions and gaps'))


# Trailing words dropped for a loose match ("Dire Wolf Heavy Scout Titan" -> "Dire Wolf")
GENERIC = {'Titan', 'Heavy', 'Scout', 'Battle', 'Battle-Automata', 'Vehicle', 'Demolition', 'Weapons', 'Platform',
           'Squadron', 'Battery', 'Detachment', 'Maniple', 'Cohort', 'Host', 'Patrol', 'Talon', 'Fighter'}


def keys(name, loose=False):
    n = plain(name)
    ks = {n}
    for p in PREFIXES:
        if n.startswith(p):
            ks.add(n[len(p):])
    if loose:
        for k in list(ks):
            words = k.split()
            while len(words) > 1 and words[-1] in GENERIC:
                words.pop()
                ks.add(' '.join(words))
    return ks


def notes_for(name, loose=False):
    """README design notes about an entry: the sub-bullet that names it, else the bullet that does.

    A name only matches a whole name in the label: "Warmaster" doesn't match "Warmaster Iconoclast".
    """
    ks = keys(name, loose)
    hit = lambda lab: any(re.search(rf'(?<![A-Za-z]){re.escape(k)}(?![a-z])(?! [A-Z][a-z])', lab) for k in ks)
    out = []
    for first, body, kids in DECISIONS:
        sub = [k for k in kids if hit(label(k))]
        if sub:
            out.append(first + '\n' + '\n'.join(sub))
        elif hit(label(first)):
            out.append(body)
    return '\n'.join(out)


# --- page writing --------------------------------------------------------------------------------

def army_dir(army):
    return f'armies/{army}'


def link(path, text):
    return f'[[{path}|{text}]]'


def model_link(army, name):
    if (army, name) in NEW_MODELS:
        return link(f'{army_dir(army)}/units/{filename(name)}', plain(name))
    return plain(name)


def formation_link(army, name):
    if (army, name) in FORMATIONS:
        return link(f'{army_dir(army)}/formations/{filename(name)}', plain(name))
    return plain(name)


def upgrade_link(army, name):
    if (army, name) in UPGRADES:
        return link(f'{army_dir(army)}/upgrades/{filename(name)}', plain(name))
    return plain(name)


def rule_link(name):
    return link(f'rules/{filename(name)}', plain(name))


def weapon_link(army, name):
    if (army, name) in WEAPONS:
        return link(f'{army_dir(army)}/weapons/{filename(name)}', plain(name))
    return plain(name)


def esc(cell):
    return cell.replace('|', '\\|').replace('\n', '<br>')


def table(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)]
    out += ['| ' + ' | '.join(esc(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out)


def yaml_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def frontmatter(title, tags, description=None, aliases=()):
    lines = ['---', f'title: {yaml_str(title)}']
    if description:
        lines.append(f'description: {yaml_str(description)}')
    if aliases:
        lines.append('aliases:')
        lines += [f'  - {yaml_str(a)}' for a in aliases]
    lines.append('tags:')
    lines += [f'  - {t}' for t in tags]
    lines.append('---')
    return '\n'.join(lines) + '\n\n'


def tag(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def origin_tags(name):
    return ['fan-made'] if fan(name) else (['munitorum'] if plain(name) in MUNITORUM else [])


def origin_line(name):
    if fan(name):
        return ('> [!note] Fan-made\n> Not part of EpicAU. It is shown in BattleScribe only once a roster takes '
                '**Allow fan-made units**, and its name carries an asterisk (*).\n\n')
    if plain(name) in MUNITORUM:
        return ('> [!info] From Departmento Munitorum\n> Missing from the archived EpicAU wiki, so this comes from '
                '[Departmento Munitorum](https://munitorum.com).\n\n')
    return ''


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(text.rstrip() + '\n')


def weapon_rows(profs, choice=''):
    return [[p.get('name'), chars(p).get('Range', ''), chars(p).get('Firepower', ''), chars(p).get('Notes', ''),
             *([choice] if choice is not None else [])] for p in profs if p.get('typeName') == 'Weapon']


def weapons_section(army, el):
    """Fixed weapons, then each weapon pick's options, as one table."""
    rows = weapon_rows(own_profiles(el), 'Fixed')
    picks = []
    for _, g in children(el):
        if g.tag != 'selectionEntryGroup':
            continue
        opts = [t for _, t in children(g) if is_weapon_option(t)]
        if not opts:
            continue
        lo, hi = limits(g)
        default = g.get('defaultSelectionEntryId')
        names = []
        for o in opts:
            c = pts(o)
            names.append(weapon_link(army, o.get('name')) + (f' (+{fmt_pts(c)} pts)' if c else '') +
                         (' (default)' if o.get('id') == default else ''))
            rows += weapon_rows(own_profiles(o), g.get('name'))
        picks.append(f'- **{g.get("name")}**' + (f' ({count_text(lo, hi)})' if hi and hi > 1 else '') +
                     ': ' + ', '.join(names))
    out = ''
    if rows:
        seen, uniq = set(), []
        for r in rows:
            if tuple(r) not in seen:
                seen.add(tuple(r))
                uniq.append(r)
        out += '## Weapons\n\n' + table(['Weapon', 'Range', 'Firepower', 'Notes', 'Mount'], uniq) + '\n\n'
    if picks:
        out += '### Weapon choices\n\nPicked on each unit in the builder:\n\n' + '\n'.join(picks) + '\n\n'
    return out


def rules_section(el, owner):
    rules = own_rules(el)
    for _, t in children(el):
        if t.tag == 'selectionEntryGroup':
            for _, o in children(t):
                rules += own_rules(o)
    seen, specific, shared = set(), [], []
    for r in rules:
        n = r.get('name')
        if n in seen:
            continue
        seen.add(n)
        desc = (r.findtext('description') or '').strip()
        if unit_specific(n, owner):
            specific.append(f'- **{plain(n)}:** {desc}')
        else:
            shared.append(f'- {rule_link(n)}' + (' *(new)*' if is_new_rule(n) else ''))
    out = ''
    if specific or shared:
        out += '## Special rules\n\n' + '\n'.join(specific + shared) + '\n\n'
    return out


def first_notes(*tries):
    """The notes of the first (names, loose) try that finds any."""
    for names, loose in tries:
        notes = list(dict.fromkeys(n for n in (notes_for(x, loose) for x in names) if n))
        if notes:
            return '\n'.join(notes)
    return ''


def design_notes(notes):
    if not notes:
        return ''
    return '## Design notes\n\nFrom the [[design-notes|data decisions]]:\n\n' + notes + '\n\n'


def new_units_in(army, el):
    return [t.get('name') for t in el.iter('selectionEntry') if (army, t.get('name')) in NEW_MODELS]


def entry_notes(e):
    """A formation's or upgrade's own notes, else those of the new units it holds."""
    units = list(dict.fromkeys(new_units_in(e.army, e.el)))
    return first_notes(([e.name], False), ([e.name], True), (units, False), (sorted(e.parents), False))


SOURCE_USES = defaultdict(list)  # source key -> [(link, what)], for the Sources page
UNSOURCED = []


def sources_of(*names):
    """The sources of the first name that has any, as {source key: what came from it}."""
    for group in names:
        merged = {}
        for n in ([group] if isinstance(group, str) else group):
            for key, what in ENTRY_SOURCES.get(plain(n), ()):
                if what not in merged.setdefault(key, []):
                    merged[key].append(what)
        if merged:
            return {k: '; '.join(v) for k, v in merged.items()}
    return {}


def sources_section(srcs, page_link, name):
    """The page's Sources section, recording each use for the Sources page."""
    if not srcs:
        UNSOURCED.append(name)
        return ''
    lines = []
    for key, what in srcs.items():
        title, url, _ = SOURCES[key]
        SOURCE_USES[key].append((page_link, what))
        lines.append(f'- ' + (f'[{title}]({url})' if url else title) + f': {what}')
    return '## Sources\n\n' + '\n'.join(lines) + '\n\nSee [[sources|all sources]].\n\n'


def model_page(m):
    p = chars(m.profile)
    war_engine = m.profile.get('typeName') == 'War Engine'
    cols = UNIT_CHARS + ([c for c in WAR_ENGINE_CHARS if c != 'Critical Hit'] if war_engine else [])
    text = frontmatter(plain(m.name), ['unit', tag(m.army), tag(p.get('Type', '') or 'unit'), *origin_tags(m.name)],
                       f'{plain(m.name)}: {m.army} unit profile, weapons and rules.')
    text += origin_line(m.name)
    text += f'**Army:** [[{army_dir(m.army)}/index|{m.army}]]\n\n'
    text += '## Profile\n\n' + table(cols, [[p.get(c, '') for c in cols]]) + '\n\n'
    if war_engine and p.get('Critical Hit') and p.get('Critical Hit') != 'See rules':
        text += f'**Critical Hit:** {p["Critical Hit"]}\n\n'
    text += weapons_section(m.army, m.el)
    text += rules_section(m.el, m.name)
    places = []
    for (kind, name) in sorted(m.places):
        if kind == 'formation':
            places.append(f'- {formation_link(m.army, name)}')
        else:
            places.append(f'- {upgrade_link(m.army, name)} (upgrade)')
    if places:
        text += '## Taken in\n\n' + '\n'.join(places) + '\n\n'
    holders = [(FORMATIONS if k == 'formation' else UPGRADES).get((m.army, n)) for k, n in sorted(m.places)]
    text += sources_section(sources_of(m.name, [h.name for h in holders if h]), model_link(m.army, m.name), m.name)
    text += design_notes(first_notes(([m.name], False), ([h.name for h in holders if h], False), ([m.name], True)))
    return text


def slot(el):
    c = el.find("categoryLinks/categoryLink[@primary='true']")
    return c.get('name') if c is not None else ''


def composition(army, el, depth=0):
    """Nested list of a formation's units and choices; upgrade groups listed separately."""
    lines, ups = [], []
    pad = '  ' * depth
    seen = set()
    for _, t in children(el):
        name = t.get('name')
        if t.tag == 'selectionEntryGroup':
            if name in UPGRADE_GROUPS:
                for _, u in children(t):
                    if u.get('name') not in ups:
                        ups.append(u.get('name'))
                continue
            sub, sub_ups = composition(army, t, depth + 1)
            ups += [u for u in sub_ups if u not in ups]
            if sub:
                lo, hi = limits(t)
                n = count_text(lo, hi)
                lines.append(f'{pad}- **{plain(name)}**' + (f' ({n})' if n else '') + ':')
                lines += sub
            continue
        if name in seen or is_weapon_option(t):
            continue
        seen.add(name)
        lo, hi = limits(t)
        n = count_text(lo, hi)
        c = pts(t)
        cost = f', +{fmt_pts(c)} pts each' if c and unit_profile(t) is not None else (f', +{fmt_pts(c)} pts' if c else '')
        if unit_profile(t) is not None:
            lines.append(f'{pad}- ' + (f'{n} × ' if n else '') + model_link(army, name) + cost)
        else:
            sub, sub_ups = composition(army, t, depth + 1)
            ups += [u for u in sub_ups if u not in ups]
            lines.append(f'{pad}- {plain(name)}' + (f' ({n})' if n else '') + cost + (':' if sub else ''))
            lines += sub
    return lines, ups


def formation_page(e):
    el = e.el
    text = frontmatter(plain(e.name), ['formation', tag(e.army), tag(slot(el)), *origin_tags(e.name)],
                       f'{plain(e.name)}: {slot(el)} for {e.army}.')
    text += origin_line(e.name)
    if not fan(e.name) and plain(e.name) not in MUNITORUM:
        text += ('> [!tip] New options\n> An EpicAU formation with fan-made units added as choices. Only the new '
                 'units link to their own pages.\n\n')
    text += f'**Army:** [[{army_dir(e.army)}/index|{e.army}]]  \n**Slot:** {slot(el)}  \n'
    text += (f'**Cost:** {fmt_pts(pts(el))} pts' if pts(el) else '**Cost:** per unit, as below') + '\n\n'
    comp, ups = composition(e.army, el)
    text += '## Composition\n\n' + '\n'.join(comp) + '\n\n'
    if ups:
        text += '## Upgrades\n\n' + ', '.join(upgrade_link(e.army, u) for u in ups) + '\n\n'
    new_units = list(dict.fromkeys(new_units_in(e.army, el)))
    text += sources_section(sources_of(e.name, new_units), formation_link(e.army, e.name), e.name)
    text += design_notes(entry_notes(e))
    return text


def upgrade_page(e):
    el = e.el
    c = pts(el)
    title = plain(e.name) + (' (upgrade)' if e.name in MODEL_NAMES else '')
    text = frontmatter(title, ['upgrade', tag(e.army), *origin_tags(e.name)],
                       f'{plain(e.name)}: {e.army} formation upgrade.')
    text += origin_line(e.name)
    text += f'**Army:** [[{army_dir(e.army)}/index|{e.army}]]  \n'
    text += (f'**Cost:** {fmt_pts(c)} pts' if c else '**Cost:** per unit, as below') + '\n\n'
    comp, _ = composition(e.army, el)
    if comp:
        text += '## Adds\n\n' + '\n'.join(comp) + '\n\n'
    text += rules_section(el, e.name)
    parents = sorted(e.parents)
    text += f'## Taken by\n\n{len(parents)} formation{"s" if len(parents) != 1 else ""}:\n\n'
    text += '\n'.join(f'- {formation_link(e.army, p)}' for p in parents) + '\n\n'
    text += sources_section(sources_of(e.name), upgrade_link(e.army, e.name), e.name)
    text += design_notes(entry_notes(e))
    return text


def weapon_page(e):
    el = e.el
    text = frontmatter(plain(e.name), ['weapon', tag(e.army), *origin_tags(e.name)],
                       f'{plain(e.name)}: {e.army} Titan weapon.')
    text += origin_line(e.name)
    text += f'**Army:** [[{army_dir(e.army)}/index|{e.army}]]  \n**Cost:** +{fmt_pts(pts(el))} pts\n\n'
    text += '## Profile\n\n' + table(['Weapon', 'Range', 'Firepower', 'Notes'],
                                     weapon_rows(own_profiles(el), None)) + '\n\n'
    text += rules_section(el, e.name)
    text += '## Mounted on\n\n' + '\n'.join(f'- {formation_link(e.army, p)}' for p in sorted(e.parents)) + '\n\n'
    text += sources_section(sources_of(e.name, sorted(e.parents)), weapon_link(e.army, e.name), e.name)
    text += design_notes(first_notes(([e.name], False), (sorted(e.parents), True)))
    return text


def rule_page(name, rule):
    users = sorted(RULE_USERS[name])
    new = is_new_rule(name)
    text = frontmatter(plain(name), ['rule', *(['new-rule'] if new else [])],
                       f'{plain(name)}: special rule.')
    if new:
        text += '> [!note] New rule\n> Only fan-made units use this rule.\n\n'
    text += (rule.findtext('description') or '').strip() + '\n\n'
    new_users = [(a, n) for a, n, nw in users if nw]
    old = sorted({a for a, n, nw in users if not nw})
    if new_users:
        text += '## New units with this rule\n\n' + '\n'.join(
            f'- {model_link(a, n) if (a, n) in NEW_MODELS else upgrade_link(a, n)} ({a})' for a, n in new_users) + '\n\n'
    if old:
        n_old = sum(1 for _, _, nw in users if not nw)
        text += f'Also used by {n_old} EpicAU unit{"s" if n_old != 1 else ""} in {", ".join(old)}.\n\n'
    srcs = sources_of(name) if new else dict(EPICAU_RULE_SOURCES)
    text += sources_section(srcs, rule_link(name), name)
    return text


def sources_page():
    text = frontmatter('Sources', ['sources'], 'Where the new units and rules come from.')
    text += ('Where each unit, upgrade, weapon and rule added beyond the EpicAU wiki comes from. Each page also '
             'lists its own sources, and the [[design-notes|design notes]] explain each conversion. Rule text is '
             'summarised in our own words, not copied.\n\n')
    for key, (title, url, about) in SOURCES.items():
        uses = SOURCE_USES.get(key, [])
        if not uses:
            continue
        text += f'## {title}\n\n{about}' + (f' <{url}>' if url else '') + '\n\n'
        pages = [(l, w) for l, w in uses if not l.startswith('[[rules/')]
        rules = [(l, w) for l, w in uses if l.startswith('[[rules/')]
        if pages:
            text += '\n'.join(f'- {l}: {w}' for l, w in pages) + '\n\n'
        if rules:
            text += f'Rules: {", ".join(l for l, _ in rules)}\n\n'
    return text


FOLDERS = {'formations': 'Formations', 'units': 'Units', 'upgrades': 'Upgrades', 'weapons': 'Titan weapons'}


def changed_armies():
    return [a for a in CATS if any(k[0] == a for k in [*FORMATIONS, *UPGRADES, *NEW_MODELS, *WEAPONS])]


def army_page(army):
    root = CATS[army]
    fms = sorted((e for (a, _), e in FORMATIONS.items() if a == army), key=lambda e: e.name)
    new_f = [e for e in fms if fan(e.name) or plain(e.name) in MUNITORUM]
    changed = [e for e in fms if e not in new_f]
    ups = sorted((e for (a, _), e in UPGRADES.items() if a == army), key=lambda e: e.name)
    wps = sorted((e for (a, _), e in WEAPONS.items() if a == army), key=lambda e: e.name)
    ms = sorted((m for (a, _), m in NEW_MODELS.items() if a == army), key=lambda m: m.name)
    text = frontmatter(army, ['army', tag(army)], f'New {army} formations, units and upgrades.')
    text += f'Catalogue `EpicAU - {army}.cat`, revision {root.get("revision")}.\n\n'
    if new_f:
        text += '## New formations\n\n' + table(['Formation', 'Slot', 'Cost'], [
            [link(f'{army_dir(army)}/formations/{filename(e.name)}', plain(e.name)),
             slot(e.el), f'{fmt_pts(pts(e.el))} pts' if pts(e.el) else 'per unit'] for e in new_f]) + '\n\n'
    if changed:
        text += ('## EpicAU formations with new choices\n\n' +
                 '\n'.join(f'- {formation_link(army, e.name)}' for e in changed) + '\n\n')
    if ups:
        text += '## New upgrades\n\n' + '\n'.join(
            f'- {upgrade_link(army, e.name)} ({fmt_pts(pts(e.el))} pts)' for e in ups) + '\n\n'
    if wps:
        text += '## New Titan weapons\n\n' + '\n'.join(
            f'- {weapon_link(army, e.name)} (+{fmt_pts(pts(e.el))} pts)' for e in wps) + '\n\n'
    if ms:
        text += '## New units\n\n' + table(['Unit'] + UNIT_CHARS, [
            [link(f'{army_dir(army)}/units/{filename(m.name)}', plain(m.name))] +
            [chars(m.profile).get(c, '') for c in UNIT_CHARS] for m in ms]) + '\n'
    return text


def rules_index():
    used = sorted(n for n in RULE_USERS if any(nw for _, _, nw in RULE_USERS[n]))
    used = [n for n in used if not any(unit_specific(n, u) for _, u, _ in RULE_USERS[n])]
    new = [n for n in used if is_new_rule(n)]
    old = [n for n in used if not is_new_rule(n)]
    text = frontmatter('Special rules', ['rules'], 'Special rules used by the new units.')
    text += ('Rules the new units use. Rules named after one unit, such as its critical hit, are on that unit\'s '
             'page. Rule text is summarised, not quoted; see the NetEA rulebook and EpicAU wiki for full wording. '
             'For roster construction rules, see [[roster-rules|Roster rules]].\n\n')
    text += '## New rules\n\nUsed only by fan-made units:\n\n' + '\n'.join(f'- {rule_link(n)}' for n in new) + '\n\n'
    text += ('## EpicAU rules used by new units\n\n' + '\n'.join(f'- {rule_link(n)}' for n in old) + '\n')
    return text, new + old


# --- changelog ------------------------------------------------------------------------------------

DATA_FILES = {GST_FILE: 'Game system', **{f'EpicAU - {a}.cat': a for a in CATS}}


def git(*args):
    return subprocess.run(['git', '-C', ROOT, *args], capture_output=True, text=True, check=True).stdout


def changelog():
    sep, end = '\x1f', '\x1e'
    log = git('log', '--date=short', f'--format={end}%H{sep}%h{sep}%ad{sep}%s{sep}%b{sep}', '--name-only')
    commits = []
    for rec in log.split(end)[1:]:
        full, short, date, subject, body, files = rec.split(sep)
        body = '\n'.join(l for l in body.strip().split('\n') if not re.match(r'^[A-Za-z-]+-By: ', l)).strip()
        files = [f for f in files.strip().split('\n') if f]
        commits.append((full, short, date, subject, body, files))
    text = frontmatter('Changelog', ['changelog'], 'Every change made to the BattleScribe data, newest first.')
    text += ('Every commit to the BattleScribe data, newest first, generated from the git history. '
             f'Each commit links to its diff on [GitHub]({REPO_URL}).\n\n')
    text += '## Current revisions\n\n' + table(['File', 'Revision'], [
        [DATA_FILES[f], (GST if f == GST_FILE else CATS[DATA_FILES[f]]).get('revision')] for f in DATA_FILES]) + '\n\n'
    last = None
    for full, short, date, subject, body, files in commits:
        if date != last:
            text += f'## {date}\n\n'
            last = date
        text += f'### {subject}\n\n'
        if body:
            text += re.sub(r'(?<!\n)\n(?!\n|- |\* |\d+\. )', ' ', body) + '\n\n'
        touched = sorted({DATA_FILES[f] for f in files if f in DATA_FILES})
        meta = f'[`{short}`]({REPO_URL}/commit/{full})'
        if touched:
            meta += ' · ' + ', '.join(touched)
        text += meta + '\n\n'
    return text


# --- static pages ---------------------------------------------------------------------------------

def md_page(title, tags, description, body):
    return frontmatter(title, tags, description) + body.strip() + '\n'


def index_page(rule_count):
    n_f = sum(1 for e in FORMATIONS.values() if fan(e.name) or plain(e.name) in MUNITORUM)
    armies = changed_armies()
    intro = README.split('\n## ')[0].split('\n', 1)[1].strip()
    text = frontmatter('EpicAU Horus Heresy BSData', ['home'],
                       'New units, rules and changes in the EpicAU Horus Heresy BattleScribe data.')
    text += intro + '\n\n'
    text += ('This site lists what the data adds beyond the EpicAU wiki: fan-made units converted from Legions '
             'Imperialis and other Epic lists, units filled in from Departmento Munitorum, the rules they use, '
             'the roster rules the data enforces, and a changelog of the work.\n\n')
    text += (f'**{n_f}** new formations, **{len(UPGRADES)}** new upgrades, **{len(WEAPONS)}** new Titan weapons and '
             f'**{len(NEW_MODELS)}** new units, using **{rule_count}** special rules.\n\n')
    text += '## Armies\n\n' + '\n'.join(f'- [[{army_dir(a)}/index|{a}]]' for a in armies) + '\n\n'
    text += ('## Reference\n\n'
             '- [[rules/index|Special rules]]: the rules the new units use\n'
             '- [[roster-rules|Roster rules]]: how rosters are built and what BattleScribe enforces\n'
             '- [[design-notes|Design notes]]: where each unit comes from and how it was converted\n'
             '- [[backlog|Backlog]]: fan-made candidates still to consider\n'
             '- [[sources|Sources]]: where each new unit and rule comes from\n'
             '- [[changelog|Changelog]]: every change to the data\n\n')
    text += ('## Using the data\n\nCopy the `.gst` and `.cat` files from the '
             f'[repository]({REPO_URL}) into a BattleScribe data folder. Fan-made units stay hidden until a roster '
             'takes **Allow fan-made units** from its Configuration entry, and are marked with an asterisk (*).\n')
    return text


def body(path):
    """A Markdown file without its title line, or '' if it isn't there."""
    full = os.path.join(ROOT, path)
    return open(full).read().split('\n', 1)[1].strip() if os.path.exists(full) else ''


def backlog():
    """The fan-made candidates in TODO.md, then the Legions Imperialis coverage in MISSING_UNITS.md."""
    text = body('TODO.md')
    missing = body('MISSING_UNITS.md')
    if missing:
        text += '\n\n## Legions Imperialis coverage\n\n' + missing.replace('\n## ', '\n### ')
    return md_page('Backlog', ['backlog'], 'Fan-made candidates still to consider, and Legions Imperialis coverage.',
                   text)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for m in NEW_MODELS.values():
        write(f'{army_dir(m.army)}/units/{filename(m.name)}.md', model_page(m))
    for e in FORMATIONS.values():
        write(f'{army_dir(e.army)}/formations/{filename(e.name)}.md', formation_page(e))
    for e in UPGRADES.values():
        write(f'{army_dir(e.army)}/upgrades/{filename(e.name)}.md', upgrade_page(e))
    for e in WEAPONS.values():
        write(f'{army_dir(e.army)}/weapons/{filename(e.name)}.md', weapon_page(e))
    armies = changed_armies()
    for a in armies:
        write(f'{army_dir(a)}/index.md', army_page(a))
        for folder, title in FOLDERS.items():
            if os.path.isdir(os.path.join(OUT, army_dir(a), folder)):
                write(f'{army_dir(a)}/{folder}/index.md', md_page(title, [tag(a)], f'New {a} {folder}.', ''))
    unchanged = [a for a in CATS if a not in armies]
    write('armies/index.md', md_page('Armies', ['army'], 'The army lists and what each adds.',
                                     '\n'.join(f'- [[{army_dir(a)}/index|{a}]]' for a in armies) +
                                     f'\n\n{" and ".join(unchanged)} have nothing added beyond the EpicAU wiki.'))
    text, rule_names = rules_index()
    write('rules/index.md', text)
    by_name = {}
    for r in RULES.values():
        by_name.setdefault(r.get('name'), r)
    for n in rule_names:
        write(f'rules/{filename(n)}.md', rule_page(n, by_name[n]))
    write('roster-rules.md', md_page('Roster rules', ['rules'], 'How rosters are built, and which rules BattleScribe enforces.',
                                     section(README, 'Building a roster') + '\n\n## Validation status\n\n' +
                                     section(README, 'Validation status')))
    write('design-notes.md', md_page('Design notes', ['notes'], 'Where each unit comes from and how it was converted.',
                                     section(README, 'Data decisions and gaps')))
    write('sources.md', sources_page())
    write('backlog.md', backlog())
    write('changelog.md', changelog())
    write('index.md', index_page(len(rule_names)))
    if UNSOURCED:
        print(f'NO SOURCE in site/sources.py for: {", ".join(sorted(set(UNSOURCED)))}')
    print(f'Wrote {len(FORMATIONS)} formations, {len(UPGRADES)} upgrades, {len(WEAPONS)} weapons, '
          f'{len(NEW_MODELS)} units and {len(rule_names)} rules to {OUT}')


if __name__ == '__main__':
    main()
