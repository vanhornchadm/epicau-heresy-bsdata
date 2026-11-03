"""Build the Quartz site's Markdown from data/, the README and git history.

Usage: python3 build_content.py [content_dir]
Publishes the data/ files the BattleScribe data is built from: each army, Legion, formation, upgrade, unit, Titan
weapon and rule gets a page with its settings shown, its [[links]] pointed at the right army's pages, and its design
notes from the README. Adds the roster rules, design notes, sources, backlog and changelog pages. Writes into
content_dir (default: site/content), which it empties first.
"""
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import generate as G  # noqa: E402  (the data as the generator reads it, and its rule matching)
from markdown_data import Doc, docs  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'content')
DATA = os.path.join(ROOT, 'data')
REPO_URL = 'https://github.com/vanhornchadm/epicau-heresy-bsdata'
INDEX_URL = f'{REPO_URL}/releases/latest/download/epicau-heresy-bsdata.latest.bsi'
KIND_FOLDERS = {'units': 'unit', 'weapons': 'weapon', 'formations': 'formation', 'upgrades': 'upgrade'}
FOLDER_TITLES = {'units': 'Units', 'weapons': 'Titan weapons', 'formations': 'Formations', 'upgrades': 'Upgrades'}
# Prefixes dropped when matching README labels to entries ("Legion Tarantula Battery" -> "Tarantula Battery")
PREFIXES = ('Legion ', 'Solar Auxilia ', 'Imperial Navy ', 'Auxilia ')
MUNITORUM = 'Departmento Munitorum'
# Sources of the EpicAU rules every list shares, shown on rule pages with no sources of their own
EPICAU_RULE_SOURCES = [('EpicAU wiki (archived)', 'the Special Rules page and reference sheets'),
                       ('Net Epic Armageddon rulebook', 'core rules')]


# --- the data ------------------------------------------------------------------------------------

class Page:
    def __init__(self, kind, doc, army=None, choice=None):
        self.kind, self.doc, self.army, self.choice = kind, doc, army, choice
        rel = os.path.relpath(doc.path, DATA)[:-len('.md')]
        self.path = rel if kind == 'rule' else f'armies/{rel}'
        self.name = doc.title

    def link(self, text=None):
        return f'[[{self.path}|{text or self.name}]]'

    @property
    def fan(self):
        return bool(self.doc.get('fan-made'))


PAGES = []
ARMY_DATA = {a['name']: a for a in G.ARMIES}
UNIT_PAGES = {}  # (sheet, unit name) -> Page
WEAPON_PAGES = {}  # weapon name -> Page
RULE_PAGES = {}  # rule name -> Page
ENTRY_PAGES = defaultdict(dict)  # (army, choice or None) -> {(kind, name): Page}


def collect():
    for d in docs(os.path.join(DATA, 'rules')):
        RULE_PAGES[d.title] = Page('rule', d)
        PAGES.append(RULE_PAGES[d.title])
    for folder in sorted(os.listdir(DATA)):
        path = os.path.join(DATA, folder)
        if folder == 'rules' or not os.path.isdir(path):
            continue
        army = folder if os.path.exists(os.path.join(path, 'index.md')) else None
        if army:
            PAGES.append(Page('army', Doc(os.path.join(path, 'index.md')), army))
        for sub, kind in KIND_FOLDERS.items():
            for d in docs(os.path.join(path, sub)):
                p = Page(kind, d, army or folder)
                PAGES.append(p)
                if kind == 'unit':
                    UNIT_PAGES[(d.get('sheet', folder), d.title)] = p
                elif kind == 'weapon':
                    WEAPON_PAGES[d.title] = p
                else:
                    ENTRY_PAGES[(army, None)][(kind, d.title)] = p
        choice_folder = army and ARMY_DATA[army].get('legions') and Doc(os.path.join(path, 'index.md')).get('choice-folder')
        for choice in (L['name'] for L in ARMY_DATA[army].get('legions', [])) if choice_folder else ():
            sub = os.path.join(path, choice_folder, choice)
            PAGES.append(Page('choice', Doc(os.path.join(sub, 'index.md')), army, choice))
            for kind_folder in ('formations', 'upgrades'):
                for d in docs(os.path.join(sub, kind_folder)):
                    p = Page(KIND_FOLDERS[kind_folder], d, army, choice)
                    PAGES.append(p)
                    ENTRY_PAGES[(army, choice)][(p.kind, d.title)] = p


def sheets(army):
    return ARMY_DATA[army]['sheets'] if army in ARMY_DATA else [army]


def find_unit(army, name):
    return next((UNIT_PAGES[(s, name)] for s in sheets(army) if (s, name) in UNIT_PAGES), None)


def find_entry(page, kind, name):
    """A formation's upgrade: its own Legion's version first, then the army's."""
    return ENTRY_PAGES[(page.army, page.choice)].get((kind, name)) or ENTRY_PAGES[(page.army, None)].get((kind, name))


LINK_RE = re.compile(r'\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]')


def resolve_links(page, text):
    """Point [[Name]] links at the page they mean in this army; names with no page stay as text."""
    def sub(m):
        name, label = m.group(1).strip(), m.group(2)
        target = find_unit(page.army, name) or WEAPON_PAGES.get(name)
        return target.link(label or name) if target else (label or name)
    return LINK_RE.sub(sub, text)


# --- README design notes --------------------------------------------------------------------------

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
    return m.group(1).replace('*', '') if m else ''


DECISIONS = bullets(section(README, 'Data decisions and gaps'))
# Trailing words dropped for a loose match ("Dire Wolf Heavy Scout Titan" -> "Dire Wolf")
GENERIC = {'Titan', 'Heavy', 'Scout', 'Battle', 'Battle-Automata', 'Vehicle', 'Demolition', 'Weapons', 'Platform',
           'Squadron', 'Battery', 'Detachment', 'Maniple', 'Cohort', 'Host', 'Patrol', 'Talon', 'Fighter'}


def keys(name, loose=False):
    ks = {name}
    for p in PREFIXES:
        if name.startswith(p):
            ks.add(name[len(p):])
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


def design_notes(page):
    notes = notes_for(page.name) or (notes_for(page.name, True) if page.kind in ('unit', 'weapon') else '')
    if not notes:
        return ''
    return '## Design notes\n\nFrom the [[design-notes|data decisions]]:\n\n' + notes + '\n\n'


# --- sources --------------------------------------------------------------------------------------

def read_sources():
    """data/sources.md: '## Name', then an optional '<url>' line and a description, per source."""
    d = Doc(os.path.join(DATA, 'sources.md'))
    out = {}
    for name in d.sections:
        text = d.text(name)
        m = re.match(r'<(\S+)>\s*', text)
        out[name] = (m.group(1) if m else None, text[m.end():] if m else text)
    return d, out


SOURCES_DOC, SOURCES = read_sources()
SOURCE_USES = defaultdict(list)  # source name -> [(page link, what)]
UNSOURCED = []


def sources_section(page):
    """The page's Sources section with each source linked, recording each use for the Sources page."""
    items = page.doc.items('Sources')
    if not items:
        if page.kind == 'rule' and page.name in G.RULES:
            items = [(f'{n}: {what}', 0, []) for n, what in EPICAU_RULE_SOURCES]
        elif page.fan:
            UNSOURCED.append(page.doc.where())
            return ''
        else:
            return ''
    lines = []
    for text, line, _ in items:
        name, _, what = text.partition(': ')
        if name not in SOURCES:
            raise page.doc.error(f'source {name!r} is not in data/sources.md', line)
        SOURCE_USES[name].append((page.link(), what))
        url = SOURCES[name][0]
        lines.append(f'- [{name}]({url}): {what}' if url else f'- {name}: {what}')
    return '## Sources\n\n' + '\n'.join(lines) + '\n\nSee [[sources|all sources]].\n\n'


def munitorum(page):
    return not page.fan and any(t.startswith(MUNITORUM + ':') for t, _, _ in page.doc.items('Sources'))


# --- page writing --------------------------------------------------------------------------------

def yaml_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def frontmatter(title, tags, description=None):
    lines = ['---', f'title: {yaml_str(title)}']
    if description:
        lines.append(f'description: {yaml_str(description)}')
    lines.append('tags:')
    lines += [f'  - {t}' for t in tags]
    lines.append('---')
    return '\n'.join(lines) + '\n\n'


def tag(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def table(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)]
    out += ['| ' + ' | '.join(str(c).replace('|', '\\|') for c in r) + ' |' for r in rows]
    return '\n'.join(out)


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(text.rstrip() + '\n')


def md_page(title, tags, description, body):
    return frontmatter(title, tags, description) + body.strip() + '\n'


def origin(page):
    if page.fan:
        return ('> [!note] Fan-made\n> Not part of EpicAU. It is shown in BattleScribe only once a roster takes '
                '**Allow fan-made units**, and its name carries an asterisk (*).\n\n')
    if munitorum(page):
        return ('> [!info] From Departmento Munitorum\n> Missing from the archived EpicAU wiki, so this comes from '
                '[Departmento Munitorum](https://munitorum.com).\n\n')
    return ''


def origin_tags(page):
    return ['fan-made'] if page.fan else ['munitorum'] if munitorum(page) else []


def facts(rows):
    """'**Label:** value' lines for the values that are set."""
    return '  \n'.join(f'**{k}:** {v}' for k, v in rows if v not in (None, '', [])) + '\n\n'


def army_link(army):
    return f'[[armies/{army}/index|{army}]]'


def choice_link(page):
    return f'[[armies/{page.army}/{choice_folder(page.army)}/{page.choice}/index|{page.choice}]]'


def choice_folder(army):
    return Doc(os.path.join(DATA, army, 'index.md')).get('choice-folder')


def rule_link(name):
    return RULE_PAGES[name].link(G.ACRONYMS.get(name, name)) if name in RULE_PAGES else name


def upgrade_links(page, names):
    def one(name):
        p = find_entry(page, 'upgrade', name)
        return p.link() if p else name
    return ', '.join(' or '.join(one(n.strip()) for n in group.split(' OR ')) for group in names)


def cost_text(cost):
    return f'{G.fmt(cost).removesuffix(".0")} pts' if cost else None


def limit_text(doc):
    return f'0-{doc.get("limit")}' if doc.get('limit') else None


def body(page):
    """The file's own text below its title, with links resolved and the Sources section rebuilt."""
    lines = open(page.doc.path, encoding='utf-8').read().split('\n')
    if lines[0] == '---':
        lines = lines[lines.index('---', 1) + 1:]
    text, skip = [], False
    for line in lines:
        if line.startswith('# '):
            continue
        if line.startswith('## '):
            skip = line[3:].strip() in ('Sources', 'Design notes')
        if not skip:
            text.append(line)
    return resolve_links(page, '\n'.join(text).strip()) + '\n\n'


def unit_page(page):
    unit = next(u for u in G.UNITS[page.doc.get('sheet', os.path.basename(os.path.dirname(os.path.dirname(page.doc.path))))]
                if u['name'] == page.name)
    rules = G.rules_in(unit['notes'] + ' ' + ' '.join(w['firepower'] for w in unit['weapons']))
    text = frontmatter(page.name, ['unit', tag(page.army), tag(unit['type'] or 'unit'), *origin_tags(page)],
                       f'{page.name}: {page.army} unit profile and weapons.')
    text += origin(page)
    sheet = page.doc.get('sheet')
    text += facts([('Army', army_link(page.army) if page.army in ARMY_DATA else page.army),
                   ('Reference sheet', sheet), ('Rules', ', '.join(rule_link(r) for r in rules))])
    return text + body(page) + sources_section(page) + design_notes(page)


def formation_page(page):
    d = page.doc
    slot = G.SLOT_CAT[d.get('slot')]
    text = frontmatter(page.name, ['formation', tag(page.army), tag(slot), *origin_tags(page)],
                       f'{page.name}: {slot} for {page.army}' + (f' ({page.choice})' if page.choice else '') + '.')
    text += origin(page)
    text += facts([('Army', army_link(page.army)),
                   (choice_label(page.army), choice_link(page) if page.choice else None),
                   ('Only with', ', '.join(d.get('only-with', []))), ('Slot', slot),
                   ('Cost', cost_text(d.get('cost')) or 'per unit, as below'), ('Limit', limit_text(d)),
                   ('Upgrades', upgrade_links(page, d.get('upgrades', []))),
                   ('Free upgrades', upgrade_links(page, d.get('extra-upgrades', []))),
                   ('Rules', ', '.join(rule_link(r) for r in d.get('rules', [])))])
    return text + body(page) + sources_section(page) + design_notes(page)


def upgrade_page(page):
    d = page.doc
    taken_by = sorted({p.name for p in PAGES if p.kind == 'formation' and p.army == page.army
                       and (p.choice in (None, page.choice) or not page.choice)
                       and page.name in [n.strip() for g in p.doc.get('upgrades', []) + p.doc.get('extra-upgrades', [])
                                         for n in g.split(' OR ')]})
    text = frontmatter(page.name, ['upgrade', tag(page.army), *origin_tags(page)],
                       f'{page.name}: {page.army} formation upgrade.')
    text += origin(page)
    text += facts([('Army', army_link(page.army)), (choice_label(page.army), choice_link(page) if page.choice else None),
                   ('Cost', cost_text(d.get('cost')) or 'per unit, as below'), ('Limit', limit_text(d)),
                   ('Rules', ', '.join(rule_link(r) for r in d.get('rules', []))),
                   ('Taken by', f'{len(taken_by)} formation{"s" if len(taken_by) != 1 else ""}')])
    return text + body(page) + sources_section(page) + design_notes(page)


def weapon_page(page):
    w = G.TITAN_WEAPONS[page.name]
    text = frontmatter(page.name, ['weapon', tag(page.army), *origin_tags(page)], f'{page.name}: Titan weapon.')
    text += origin(page)
    text += facts([('Army', army_link(page.army)),
                   ('Rules', ', '.join(rule_link(r) for r in G.rules_in(w['firepower'] + ' ' + w['notes'])))])
    return text + body(page) + sources_section(page) + design_notes(page)


def rule_page(page):
    d = page.doc
    text = frontmatter(page.name, ['rule'], f'{page.name}: special rule.')
    text += facts([('Shown as', d.get('acronym'))])
    return text + body(page) + sources_section(page)


def choice_label(army):
    return ARMY_DATA[army].get('choice', {}).get('label', 'Choice')


def formations_table(pages):
    rows = []
    for p in sorted(pages, key=lambda p: (list(G.SLOT_CAT).index(p.doc.get('slot')), p.name)):
        rows.append([p.link(p.name + ('*' if p.fan else '')), G.SLOT_CAT[p.doc.get('slot')],
                     cost_text(p.doc.get('cost')) or 'per unit'])
    return table(['Formation', 'Slot', 'Cost'], rows) + '\n\n'


def revision(army):
    path = os.path.join(ROOT, f'EpicAU - {army}.cat')
    m = os.path.exists(path) and re.search(r'<catalogue\b[^>]*?\brevision="(\d+)"', open(path).read())
    return m.group(1) if m else '?'


def army_page(page):
    a, d = ARMY_DATA[page.army], page.doc
    text = frontmatter(page.army, ['army', tag(page.army)], f'The {page.army} army list.')
    caps = {a['upgrade_cap'], a['support_cap'], a['low_cap']}
    text += facts([('Catalogue', f'`EpicAU - {page.army}.cat`, revision {revision(page.army)}'),
                   ('Strategy rating', a['strategy']), ('Initiative', a['initiative']),
                   ('Support detachments per line', a['supports_per_line']),
                   ('Upgrades per formation', 'no limit' if caps == {None} else ' / '.join(map(str, sorted(caps - {None})))),
                   ('Allies and Lords of War', f'up to {d.get("allies-fraction")} of the points'
                    if d.get('allies-fraction') else None),
                   ('Cohesive allies', ', '.join(a['cohesive'])), ('Disruptive allies', ', '.join(a['disruptive'])),
                   ('Rules', ', '.join(rule_link(r) for r in a['rules']))])
    text += body(page)
    if a.get('legions'):
        text += f'## {choice_label(page.army)}\n\n' + '\n'.join(
            f'- [[armies/{page.army}/{choice_folder(page.army)}/{L["name"]}/index|{L["name"]}]]'
            + (f' ({L["allegiance"]})' if L['allegiance'] else '') for L in a['legions']) + '\n\n'
    own = [p for p in PAGES if p.army == page.army and p.choice is None]
    text += '## Formations\n\n' + formations_table([p for p in own if p.kind == 'formation'])
    ups = sorted((p for p in own if p.kind == 'upgrade'), key=lambda p: p.name)
    if ups:
        text += '## Upgrades\n\n' + '\n'.join(f'- {p.link()}' + ('*' if p.fan else '') + (
            f' ({cost_text(p.doc.get("cost"))})' if p.doc.get('cost') else '') for p in ups) + '\n\n'
    text += (f'## Units\n\nThe [[armies/{page.army}/units/index|units]] on the '
             f'{", ".join(a["sheets"])} reference sheet{"s" if len(a["sheets"]) > 1 else ""}.\n')
    return text


def choice_page(page):
    L = next(L for L in ARMY_DATA[page.army]['legions'] if L['name'] == page.choice)
    d = page.doc
    text = frontmatter(page.choice, [tag(choice_label(page.army)), tag(page.army)],
                       f'{page.choice}: {choice_label(page.army)} of the {page.army} list.')
    text += facts([('Army', army_link(page.army)), ('Allegiance', L['allegiance']),
                   ('Cohesive allies', ', '.join(L['cohesive']) or 'none'),
                   ('Disruptive allies', ', '.join(L['disruptive']) or 'none'),
                   ('Removes', ', '.join(d.get('remove', [])))])
    text += body(page)
    own = [p for p in PAGES if p.army == page.army and p.choice == page.choice]
    if [p for p in own if p.kind == 'formation']:
        text += '## Formations\n\nAdded, or replacing the core formation of the same name:\n\n' + \
            formations_table([p for p in own if p.kind == 'formation'])
    also = [p for p in PAGES if p.army == page.army and p.choice is None and p.kind == 'formation'
            and page.choice in p.doc.get('only-with', [])]
    if also:
        text += '## Formations\n\n' + formations_table(also)
    ups = [p for p in own if p.kind == 'upgrade']
    if ups:
        text += '## Upgrades\n\n' + '\n'.join(f'- {p.link()}' for p in ups) + '\n\n'
    return text


def sources_page():
    text = frontmatter('Sources', ['sources'], 'Where the units and rules come from.')
    text += (SOURCES_DOC.text() + ' Rule text is summarised in our own '
             'words, not copied; the [[design-notes|design notes]] explain each conversion.\n\n')
    for name, (url, about) in SOURCES.items():
        uses = SOURCE_USES.get(name, [])
        text += f'## {name}\n\n{about}' + (f' <{url}>' if url else '') + '\n\n'
        pages = [(l, w) for l, w in uses if not l.startswith('[[rules/')]
        rules = [l for l, _ in uses if l.startswith('[[rules/')]
        if pages:
            text += '\n'.join(f'- {l}: {w}' for l, w in pages) + '\n\n'
        if rules:
            text += f'Rules: {", ".join(rules)}\n\n'
    return text


# --- changelog ------------------------------------------------------------------------------------

DATA_FILES = {G.GST_FILE: 'Game system', **{f'EpicAU - {a}.cat': a for a in ARMY_DATA}}


def git(*args):
    return subprocess.run(['git', '-C', ROOT, *args], capture_output=True, text=True, check=True).stdout


def file_revision(f):
    m = re.search(r'<(?:gameSystem|catalogue)\b[^>]*?\brevision="(\d+)"', open(os.path.join(ROOT, f)).read())
    return m.group(1) if m else '?'


def changelog():
    sep, end = '\x1f', '\x1e'
    log = git('log', '--date=short', f'--format={end}%H{sep}%h{sep}%ad{sep}%s{sep}%b{sep}', '--name-only')
    commits = []
    for rec in log.split(end)[1:]:
        full, short, date, subject, body_, files = rec.split(sep)
        body_ = '\n'.join(l for l in body_.strip().split('\n') if not re.match(r'^[A-Za-z-]+-By: ', l)).strip()
        files = [f for f in files.strip().split('\n') if f]
        commits.append((full, short, date, subject, body_, files))
    text = frontmatter('Changelog', ['changelog'], 'Every change made to the BattleScribe data, newest first.')
    text += ('Every commit to the data, newest first, generated from the git history. '
             f'Each commit links to its diff on [GitHub]({REPO_URL}).\n\n')
    text += '## Current revisions\n\n' + table(['File', 'Revision'], [
        [label_, file_revision(f)] for f, label_ in DATA_FILES.items() if os.path.exists(os.path.join(ROOT, f))]) + '\n\n'
    last = None
    for full, short, date, subject, body_, files in commits:
        if date != last:
            text += f'## {date}\n\n'
            last = date
        text += f'### {subject}\n\n'
        if body_:
            text += re.sub(r'(?<!\n)\n(?!\n|- |\* |\d+\. )', ' ', body_) + '\n\n'
        touched = sorted({DATA_FILES[f] for f in files if f in DATA_FILES})
        meta = f'[`{short}`]({REPO_URL}/commit/{full})'
        if touched:
            meta += ' · ' + ', '.join(touched)
        text += meta + '\n\n'
    return text


# --- static pages ---------------------------------------------------------------------------------

def index_page():
    count = lambda kind: sum(1 for p in PAGES if p.kind == kind)
    fan = lambda kind: sum(1 for p in PAGES if p.kind == kind and p.fan)
    intro = README.split('\n## ')[0].split('\n', 1)[1].strip()
    text = frontmatter('EpicAU Horus Heresy BSData', ['home'],
                       'The EpicAU Horus Heresy army lists, units and rules behind the BattleScribe data.')
    text += intro + '\n\n'
    text += ('This site publishes the Markdown files the BattleScribe data is built from: every army list, '
             'formation, upgrade, unit and special rule, with the fan-made ones marked, plus the roster rules, '
             'design notes and a changelog.\n\n')
    text += (f'**{count("formation")}** formations ({fan("formation")} fan-made), **{count("upgrade")}** upgrades, '
             f'**{count("unit")}** units ({fan("unit")} fan-made), **{count("weapon")}** Titan weapons and '
             f'**{count("rule")}** special rules.\n\n')
    text += '## Armies\n\n' + '\n'.join(f'- {army_link(a)}' for a in sorted(ARMY_DATA)) + '\n\n'
    text += ('## Reference\n\n'
             '- [[rules/index|Special rules]]\n'
             '- [[roster-rules|Roster rules]]: how rosters are built and what BattleScribe enforces\n'
             '- [[design-notes|Design notes]]: where each unit comes from and how it was converted\n'
             '- [[writing-data|Writing data]]: how to add or change a unit, formation or rule\n'
             '- [[backlog|Backlog]]: fan-made candidates still to consider\n'
             '- [[sources|Sources]]: where each new unit and rule comes from\n'
             '- [[changelog|Changelog]]: every change to the data\n\n')
    text += ('## Using the data\n\n'
             f'In BattleScribe or New Recruit, add the data index <{INDEX_URL}>. It always points at the latest '
             f'release, so updates arrive on their own. You can also copy the `.gst` and `.cat` files from the '
             f'[repository]({REPO_URL}). Fan-made units stay hidden until a roster takes **Allow fan-made units** '
             'from its Configuration entry, and are marked with an asterisk (*).\n')
    return text


def file_body(path):
    """A Markdown file without its title line, or '' if it isn't there."""
    full = os.path.join(ROOT, path)
    return open(full).read().split('\n', 1)[1].strip() if os.path.exists(full) else ''


def backlog():
    """The fan-made candidates in docs/TODO.md, then the Legions Imperialis coverage in docs/MISSING_UNITS.md."""
    text = file_body('docs/TODO.md')
    missing = file_body('docs/MISSING_UNITS.md')
    if missing:
        text += '\n\n## Legions Imperialis coverage\n\n' + missing.replace('\n## ', '\n### ')
    return md_page('Backlog', ['backlog'], 'Fan-made candidates still to consider, and Legions Imperialis coverage.',
                   text)


WRITERS = {'unit': unit_page, 'formation': formation_page, 'upgrade': upgrade_page, 'weapon': weapon_page,
           'rule': rule_page, 'army': army_page, 'choice': choice_page}


def main():
    collect()
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for page in PAGES:
        write(page.path + '.md', WRITERS[page.kind](page))
    folders = {os.path.dirname(p.path) for p in PAGES if p.kind in KIND_FOLDERS.values()}
    for folder in folders:
        base = os.path.basename(folder)
        army = folder.split('/')[1]
        write(f'{folder}/index.md', md_page(FOLDER_TITLES[base], [tag(army)], f'{army} {base}.', ''))
    for army in ARMY_DATA:
        if ARMY_DATA[army].get('legions'):
            cf = choice_folder(army)
            write(f'armies/{army}/{cf}/index.md', md_page(cf.capitalize(), [tag(army)], f'{army} {cf}.', ''))
    write('armies/index.md', md_page('Armies', ['army'], 'The army lists.',
                                     '\n'.join(f'- {army_link(a)}' for a in sorted(ARMY_DATA))))
    write('rules/index.md', md_page('Special rules', ['rules'], 'The special rules the army lists use.',
                                    'Rule text is summarised, not quoted; see the NetEA rulebook and EpicAU wiki for '
                                    'full wording. For roster construction rules, see [[roster-rules|Roster rules]].'
                                    '\n\n' + '\n'.join(f'- {p.link()}' for _, p in sorted(RULE_PAGES.items()))))
    write('roster-rules.md', md_page('Roster rules', ['rules'], 'How rosters are built, and which rules BattleScribe enforces.',
                                     section(README, 'Building a roster') + '\n\n## Validation status\n\n' +
                                     section(README, 'Validation status')))
    write('design-notes.md', md_page('Design notes', ['notes'], 'Where each unit comes from and how it was converted.',
                                     section(README, 'Data decisions and gaps')))
    write('writing-data.md', md_page('Writing data', ['docs'], 'How to add or change a unit, formation or rule.',
                                     file_body('data/README.md')))
    write('sources.md', sources_page())
    write('backlog.md', backlog())
    write('changelog.md', changelog())
    write('index.md', index_page())
    if UNSOURCED:
        print(f'NO SOURCE (add a "## Sources" section) in: {", ".join(sorted(set(UNSOURCED)))}')
    counts = defaultdict(int)
    for p in PAGES:
        counts[p.kind] += 1
    print(f'Wrote {", ".join(f"{n} {k} pages" for k, n in sorted(counts.items()))} to {OUT}')


if __name__ == '__main__':
    main()
