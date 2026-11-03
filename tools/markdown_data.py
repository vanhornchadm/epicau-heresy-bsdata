"""Read the army lists, units, weapons and rules from the Markdown files in data/.

Each entry is one file: YAML-style front matter for its settings, a '# Name' heading, a description paragraph, and
'## ' sections. Front matter is a small YAML subset: 'key: value' scalars and 'key:' followed by '  - item' lists.

    data/rules/<rule>.md                         a special rule (description; acronym, pattern, matches)
    data/<Army>/index.md                         an army list's settings, notes, and the order of its Legions
    data/<Army>/units/<unit>.md                  a reference-sheet unit: stat line, weapons, notes, weapon options
    data/<Army>/weapons/<weapon>.md              a Titan weapon
    data/<Army>/formations/<formation>.md        a formation: slot, cost, upgrades, limit and composition
    data/<Army>/upgrades/<upgrade>.md            an upgrade: cost, limit and what it adds
    data/<Army>/<folder>/<choice>/index.md       one option of the list's choice (a Legion): allegiance, allies
    data/<Army>/<folder>/<choice>/formations/    formations only that option takes (they may share a core name)
    data/<Army>/<folder>/<choice>/upgrades/      upgrades only that option takes, or its versions of core ones

Composition and upgrade lists use one bullet per part; data/README.md describes the format. Sections the generator doesn't read
(Sources, Design notes, anything else) are for people and the site.

load() returns the same structures the generator was first written against: reference sheets of unit records,
Titan weapons, rules, weapon options and army list specs.
"""
import json
import os
import re
from collections import OrderedDict

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
SLOTS = ('line', 'support', 'low', 'horde', 'greater', 'followers', 'special')
# Labels a part gets when the file gives none
DEFAULT_LABEL = {'or': 'Units', 'mix': 'Units', 'fill': 'Transports', 'swap': 'Upgrades'}



class DataError(ValueError):
    pass


# ------------------------------------------------------------------ files
def parse_scalar(text):
    text = text.strip()
    if text[:1] == "'" and text[-1:] == "'" and len(text) > 1:
        return text[1:-1].replace("''", "'")
    if text[:1] == '"' and text[-1:] == '"' and len(text) > 1:
        return json.loads(text)
    if re.fullmatch(r'-?\d+', text):
        return int(text)
    if re.fullmatch(r'-?\d+\.\d+', text):
        return float(text)
    if text in ('true', 'false'):
        return text == 'true'
    if text in ('null', '~', ''):
        return None
    return text


def parse_front_matter(text, where):
    data, key = OrderedDict(), None
    for n, line in enumerate(text.splitlines(), 2):
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        item = re.match(r'\s+- (.*)$', line) or re.match(r'- (.*)$', line)
        if item and key is not None:
            data[key].append(parse_scalar(item.group(1)))
            continue
        m = re.match(r'([A-Za-z][\w-]*):(?:\s+(.*))?$', line)
        if not m:
            raise DataError(f'{where}:{n}: unreadable front matter line {line!r}')
        key, value = m.group(1), m.group(2)
        if value is None or not value.strip():
            data[key] = []
        else:
            data[key], key = parse_scalar(value), None
    return data


class Doc:
    """One Markdown file: front matter, '# title', the description below it and its '## ' sections."""

    def __init__(self, path):
        self.path = path
        text = open(path, encoding='utf-8').read()
        self.meta = OrderedDict()
        if text.startswith('---\n'):
            end = text.index('\n---', 4)
            self.meta = parse_front_matter(text[4:end], self.where())
            text = text[end + 4:].lstrip('\n')
        self.title, self.intro, self.sections = None, [], OrderedDict()
        current = self.intro
        for line in text.splitlines():
            if line.startswith('# ') and self.title is None:
                self.title = line[2:].strip()
            elif line.startswith('## '):
                current = self.sections.setdefault(line[3:].strip(), [])
            else:
                current.append(line)
        if not self.title:
            raise DataError(f'{self.where()}: no "# Name" heading')

    def where(self):
        return os.path.relpath(self.path, os.path.dirname(ROOT))

    def get(self, key, default=None):
        return self.meta.get(key, default)

    def text(self, section=None):
        """A section (or the description) as text: lines of a paragraph joined, paragraphs split by a blank line."""
        lines = self.intro if section is None else self.sections.get(section, [])
        paras, cur = [], []
        for line in lines + ['']:
            if line.strip():
                cur.append(line.strip())
            elif cur:
                paras.append(' '.join(cur))
                cur = []
        return '\n\n'.join(paras)

    def items(self, section):
        """A section's bullet list as a tree of (text, line number, children)."""
        root, stack = [], [(-1, None)]
        start = self.line_of(section)
        for n, line in enumerate(self.sections.get(section, []), start + 1):
            if not line.strip():
                continue
            m = re.match(r'( *)- (.*)$', line)
            if not m:
                raise DataError(f'{self.where()}:{n}: expected a "- " list item in "{section}", got {line!r}')
            depth = len(m.group(1))
            while stack[-1][0] >= depth:
                stack.pop()
            node = (m.group(2).strip(), n, [])
            (stack[-1][1][2] if stack[-1][1] else root).append(node)
            stack.append((depth, node))
        return root

    def table(self, section):
        """A section's first Markdown table as a list of {header: cell} rows."""
        rows = [split_row(line) for line in self.sections.get(section, []) if line.strip().startswith('|')]
        if len(rows) < 2 or not all(re.fullmatch(r':?-{3,}:?', c) for c in rows[1]):
            return []
        return [dict(zip(rows[0], r)) for r in rows[2:]]

    def line_of(self, section):
        for n, line in enumerate(open(self.path, encoding='utf-8'), 1):
            if line.rstrip('\n') == f'## {section}':
                return n
        return 0

    def error(self, message, line=None):
        return DataError(f'{self.where()}{":" + str(line) if line else ""}: {message}')


def split_row(line):
    cells = re.split(r'(?<!\\)\|', line.strip())[1:-1]
    return [c.strip().replace('\\|', '|') for c in cells]


def docs(folder):
    if not os.path.isdir(folder):
        return []
    return [Doc(os.path.join(folder, f)) for f in sorted(os.listdir(folder)) if f.endswith('.md')]


def number(text):
    return float(text) if '.' in text else int(text)


# ------------------------------------------------------------------ composition
COUNT = r'\d+(?:-\d+|\+)?'
NUM = r'-?\d+(?:\.\d+)?'
UNIT_RE = re.compile(rf'^(?:({COUNT}) +)?\[\[([^\]|]+)(?:\|([^\]]+))?\]\](?:, \+?({NUM}) pts each)?( \(fan-made\))?$')
LABEL_RE = re.compile(r'^\*\*(.+?)\*\*: (.*)$')
OPT_RE = re.compile(rf'^\*\*(.+?)\*\*(?:, \+?({NUM}) pts)?(?::(?: (.*))?)?$')
SWAP_RE = re.compile(rf'^(.+?) *(?:->|→) *\[\[([^\]|]+)\]\](?:, \+?({NUM}) pts each)?$')


def count(text):
    if text.endswith('+'):
        return int(text[:-1]), None
    lo, _, hi = text.partition('-')
    return int(lo), int(hi or lo)


def unit_part(doc, text, line, default=None):
    m = UNIT_RE.match(text)
    if not m:
        raise doc.error(f'not a unit line: {text!r} (expected e.g. "4 [[Unit]], +25 pts each")', line)
    if m.group(1) is None and default is None:
        raise doc.error(f'{text!r} needs a count', line)
    lo, hi = count(m.group(1)) if m.group(1) else default
    return {'kind': 'unit', 'unit': m.group(2).strip(), 'min': lo, 'max': hi,
            'each': number(m.group(4)) if m.group(4) else 0, 'label': m.group(3), 'new': bool(m.group(5))}


def children(doc, node, inline):
    """A group's members: the text after its colon, or the items nested below it."""
    text, line, kids = node
    if inline and kids:
        raise doc.error('give a group\'s members after the colon or below it, not both', line)
    return [(inline, line, [])] if inline else kids


def part(doc, node):
    text, line, kids = node
    label = None
    if (m := LABEL_RE.match(text)):
        label, text = m.group(1), m.group(2)
    low = text[:1].lower() + text[1:]
    if (g := re.match(r'^one of:(?: (.*))?$', low)):
        inline = text[g.start(1):] if g.group(1) else None
        opts = [option(doc, k) for k in children(doc, node, inline)]
        return {'kind': 'or', 'opts': opts, 'label': label or DEFAULT_LABEL['or']}
    if (g := re.match(rf'^({COUNT}) in any mix of:$', low)):
        lo, hi = count(g.group(1))
        units = [unit_part(doc, k[0], k[1], default=(0, hi)) for k in kids]
        return {'kind': 'mix', 'min': lo, 'max': hi, 'units': units, 'label': label or DEFAULT_LABEL['mix']}
    if (g := re.match(rf'^transports carrying ({NUM}) (.+?) each:(?: (.*))?$', low)):
        inline = text[g.start(3):] if g.group(3) else None
        units = [unit_part(doc, k[0], k[1], default=(0, None)) for k in children(doc, node, inline)]
        return {'kind': 'fill', 'per': number(g.group(1)), 'space': text[g.start(2):g.end(2)], 'units': units,
                'label': label or DEFAULT_LABEL['fill']}
    if (g := re.match(rf'^upgrade ({COUNT}):(?: (.*))?$', low)):
        lo, hi = count(g.group(1))
        inline = text[g.start(2):] if g.group(2) else None
        swaps = [swap(doc, k) for k in children(doc, node, inline)]
        return {'kind': 'swap', 'min': lo, 'max': hi, 'swaps': swaps, 'label': label or DEFAULT_LABEL['swap']}
    if label:
        raise doc.error(f'a label goes on a group ("**{label}**: one of:"), not on {text!r}', line)
    if kids:
        raise doc.error(f'{text!r} has nested items but is not a group', line)
    return unit_part(doc, text, line)


def option(doc, node):
    text, line, kids = node
    m = OPT_RE.match(text)
    if not m:
        raise doc.error(f'not an option: {text!r} (expected "**Option**: <part>" or "**Option**, +50 pts:")', line)
    parts = [part(doc, k) for k in children(doc, node, m.group(3))]
    return {'label': m.group(1), 'parts': parts, 'cost': number(m.group(2)) if m.group(2) else 0}


def swap(doc, node):
    text, line, kids = node
    m = SWAP_RE.match(text)
    if not m:
        raise doc.error(f'not a swap: {text!r} (expected "[[Unit]] -> [[Upgraded Unit]], +20 pts each")', line)
    frm = re.findall(r'\[\[([^\]|]+)\]\]', m.group(1))
    if not frm:
        raise doc.error(f'no unit to swap from in {text!r}', line)
    return (frm[0] if len(frm) == 1 else tuple(frm), m.group(2), number(m.group(3)) if m.group(3) else 0)


def parts(doc, section):
    return [part(doc, node) for node in doc.items(section)]


# ------------------------------------------------------------------ limits
LIMIT_RE = re.compile(r'^(\d+) per (?:army|(\d+) pts( or part thereof)?)$')


def limit(doc):
    text = doc.get('limit')
    if text is None:
        return None, None, False
    m = LIMIT_RE.match(str(text))
    if not m:
        raise doc.error(f'limit {text!r} should read "1 per army", "1 per 2000 pts" or "1 per 500 pts or part thereof"')
    return int(m.group(1)), int(m.group(2)) if m.group(2) else None, bool(m.group(3))


def names(doc, key):
    value = doc.get(key, [])
    return [value] if isinstance(value, str) else list(value)


def check_keys(doc, allowed):
    unknown = [k for k in doc.meta if k not in allowed]
    if unknown:
        raise doc.error(f'unknown front matter {unknown}; allowed: {sorted(allowed)}')


SITE_KEYS = {'tags', 'aliases', 'description'}  # Quartz settings, ignored here


# ------------------------------------------------------------------ entries
def formation(doc, choice_key=None):
    check_keys(doc, {'slot', 'cost', 'upgrades', 'extra-upgrades', 'limit', 'rules', 'fan-made', 'only-with'} | SITE_KEYS)
    slot = doc.get('slot')
    if slot not in SLOTS:
        raise doc.error(f'slot {slot!r} should be one of {SLOTS}')
    maxn, per, round_up = limit(doc)
    f = {'name': doc.title, 'slot': slot, 'cost': doc.get('cost', 0), 'units': parts(doc, 'Composition'),
         'up': ', '.join(names(doc, 'upgrades')), 'maxn': maxn, 'per': per, 'round_up': round_up,
         'rules': names(doc, 'rules'), 'note': doc.text() or None, 'extra_up': names(doc, 'extra-upgrades'),
         'new': bool(doc.get('fan-made'))}
    if doc.get('only-with'):
        f['show_for'] = names(doc, 'only-with')
    return f


def upgrade(doc):
    check_keys(doc, {'cost', 'limit', 'rules', 'fan-made'} | SITE_KEYS)
    maxn, per, round_up = limit(doc)
    return {'name': doc.title, 'cost': doc.get('cost', 0), 'parts': parts(doc, 'Adds'), 'rules': names(doc, 'rules'),
            'desc': doc.text() or None, 'maxn': maxn, 'per': per, 'round_up': round_up,
            'new': bool(doc.get('fan-made'))}


OPTION_ATTR = re.compile(rf'^(?:\+?({NUM}) pts|(FF|Armour|CC) (\S+)|needs (.+?): (.+))$')


def weapon_options(doc):
    """[group] from the unit's 'Weapon options' section:

        - **Group**: pick one         (or 'optional': at most one)
          - Option, +5 pts, FF 4+, Armour 4+, CC 4+, needs Upgrade: Option
            - Sheet row name          the option's weapons, when they aren't the row named like the option
            - Name | 30cm | AP5+      a weapon row of its own
            - (no weapons)
    """
    groups = []
    for text, line, kids in doc.items('Weapon options'):
        m = re.match(r'^\*\*(.+?)\*\*: (pick one|optional)$', text)
        if not m:
            raise doc.error(f'expected "**Group**: pick one" or "**Group**: optional", got {text!r}', line)
        options = []
        for otext, oline, rows in kids:
            bits = otext.split(', ')
            attrs = {'cost': 0, 'ff': None, 'armour': None, 'cc': None, 'requires': None}
            while len(bits) > 1 and (a := OPTION_ATTR.match(bits[-1])):
                bits.pop()
                if a.group(1):
                    attrs['cost'] = number(a.group(1))
                elif a.group(2):
                    attrs[a.group(2).lower()] = a.group(3)
                else:
                    attrs['requires'] = (a.group(4), a.group(5))
            label = ', '.join(bits)
            if not rows:
                got = [label]
            elif [r[0] for r in rows] == ['(no weapons)']:
                got = []
            else:
                got = []
                for rtext, rline, _ in rows:
                    cells = [c.strip() for c in rtext.split(' | ')]
                    if len(cells) == 1:
                        got.append(cells[0])
                    elif len(cells) == 3:
                        got.append({'name': cells[0], 'range': cells[1], 'firepower': cells[2]})
                    else:
                        raise doc.error(f'a weapon row is "Name | Range | Firepower", got {rtext!r}', rline)
            options.append({'label': label, 'rows': got, **attrs})
        groups.append({'label': m.group(1), 'optional': m.group(2) == 'optional', 'options': options})
    return groups


def titan_slots(doc):
    """[(mount, count, [(weapon, cost)])] from the unit's 'Titan weapons' section ('- **Arm** x 2:')."""
    slots = []
    for text, line, kids in doc.items('Titan weapons'):
        m = re.match(r'^\*\*(\w+)\*\*(?: x (\d+))?:$', text)
        if not m:
            raise doc.error(f'expected "**Arm** x 2:" or "**Carapace**:", got {text!r}', line)
        weapons = []
        for wtext, wline, _ in kids:
            w = re.match(rf'^\[\[([^\]|]+)\]\](?:, \+?({NUM}) pts)?$', wtext)
            if not w:
                raise doc.error(f'expected "[[Weapon]], +25 pts", got {wtext!r}', wline)
            weapons.append((w.group(1), number(w.group(2)) if w.group(2) else 0))
        slots.append((m.group(1), int(m.group(2) or 1), weapons))
    return slots


STAT_COLUMNS = ['Type', 'Speed', 'Armour', 'CC', 'FF']


def unit(doc):
    check_keys(doc, {'sheet', 'section', 'fan-made', 'replaced-rows'} | SITE_KEYS)
    stats = doc.table('Profile')
    if len(stats) != 1 or list(stats[0]) != STAT_COLUMNS:
        raise doc.error(f'the Profile section needs one table row under | {" | ".join(STAT_COLUMNS)} |')
    weapons = []
    for row in doc.table('Weapons'):
        if list(row) != ['Weapon', 'Range', 'Firepower']:
            raise doc.error('the Weapons table needs the columns | Weapon | Range | Firepower |')
        weapons.append({'name': row['Weapon'], 'range': row['Range'], 'firepower': row['Firepower']})
    s = stats[0]
    record = {'name': doc.title, 'type': s['Type'], 'speed': s['Speed'], 'armour': s['Armour'], 'cc': s['CC'],
              'ff': s['FF'], 'weapons': weapons, 'notes': doc.text('Notes')}
    if doc.get('section'):
        record['section'] = doc.get('section')
    return record


def titan_weapon(doc):
    check_keys(doc, {'fan-made'} | SITE_KEYS)
    rows = doc.table('Profile')
    if len(rows) != 1 or list(rows[0]) != ['Range', 'Firepower']:
        raise doc.error('the Profile section needs one table row under | Range | Firepower |')
    return {'name': doc.title, 'range': rows[0]['Range'], 'firepower': rows[0]['Firepower'],
            'notes': doc.text('Notes')}


def fraction(doc, key):
    text = doc.get(key)
    if text is None:
        return None
    m = re.fullmatch(r'(\d+)/(\d+)', str(text))
    if not m:
        raise doc.error(f'{key} {text!r} should be a fraction such as 1/3')
    return int(m.group(1)) / int(m.group(2))


ARMY_KEYS = {'sheets', 'strategy', 'initiative', 'supports-per-line', 'upgrade-cap', 'support-upgrade-cap',
             'lord-of-war-upgrade-cap', 'allies-fraction', 'rules', 'cohesive', 'disruptive',
             'tactical-transport-space', 'choice-folder', 'choices', 'choice', 'choice-none', 'choice-none-rule',
             'choice-none-text', 'choice-text', 'choice-sets-allies'} | SITE_KEYS
CHOICE_KEYS = {'allegiance', 'cohesive', 'disruptive', 'remove'} | SITE_KEYS


def norm(name):
    """Core and Legion formations match on their names without 'the' and a leading 'Legion'."""
    n = name.lower().replace('the ', '')
    if n.startswith('legion '):
        n = n[len('legion '):]
    return n.strip()


def army(folder):
    doc = Doc(os.path.join(folder, 'index.md'))
    check_keys(doc, ARMY_KEYS)
    cap = doc.get('upgrade-cap')
    a = {'name': doc.title, 'sheets': names(doc, 'sheets') or [doc.title], 'strategy': doc.get('strategy'),
         'initiative': str(doc.get('initiative')), 'supports_per_line': doc.get('supports-per-line'),
         'upgrade_cap': cap, 'support_cap': doc.get('support-upgrade-cap', cap),
         'low_cap': doc.get('lord-of-war-upgrade-cap', cap), 'allies_fraction': fraction(doc, 'allies-fraction'),
         'formations': [formation(d) for d in docs(os.path.join(folder, 'formations'))],
         'upgrades': {u['name']: u for u in map(upgrade, docs(os.path.join(folder, 'upgrades')))},
         'cohesive': names(doc, 'cohesive'), 'disruptive': names(doc, 'disruptive'), 'rules': names(doc, 'rules'),
         'notes': [t for t, _, _ in doc.items('Notes')], 'transport_space': set(names(doc, 'tactical-transport-space'))}
    if doc.get('choices'):
        add_choices(a, doc, folder)
    return a


def add_choices(a, doc, folder):
    """The list's required choice (the Legion): each option's formations are shown only for the options that have
    them, and hide the core formations they replace (same name) or remove; its upgrades are added, or replace a core
    upgrade of the same name for that option."""
    a['choice'] = dict(label=doc.get('choice'), none=doc.get('choice-none'), none_rule=doc.get('choice-none-rule'),
                       none_text=doc.get('choice-none-text'), allegiance_text=doc.get('choice-text'),
                       tag=bool(doc.get('choice-sets-allies')))
    core = OrderedDict((norm(f['name']), dict(f, show_for=None, hide_for=[])) for f in a['formations']
                       if 'show_for' not in f)
    plain = [f for f in a['formations'] if 'show_for' in f]  # core-folder formations only some options take
    extra = OrderedDict()  # formation json -> formation shown for the options that share it
    core_up = set(a['upgrades'])
    a['upgrade_variants'], a['legions'] = OrderedDict(), []
    a['core_allies'] = (a['cohesive'], a['disruptive'])
    for name in names(doc, 'choices'):
        sub = os.path.join(folder, doc.get('choice-folder'), name)
        if not os.path.isdir(sub):
            raise doc.error(f'choice {name!r} has no folder {os.path.relpath(sub, os.path.dirname(ROOT))}')
        c = Doc(os.path.join(sub, 'index.md'))
        check_keys(c, CHOICE_KEYS)
        if c.title != name:
            raise c.error(f'title {c.title!r} should be {name!r}')
        for r in names(c, 'remove'):
            if norm(r) not in core:
                raise c.error(f'removes {r!r}, which is not a core formation')
            core[norm(r)]['hide_for'].append(name)
        for f in map(formation, docs(os.path.join(sub, 'formations'))):
            if norm(f['name']) in core:
                core[norm(f['name'])]['hide_for'].append(name)
            key = json.dumps(f, sort_keys=True, default=str)
            extra.setdefault(key, dict(f, show_for=[], hide_for=[], key=name))['show_for'].append(name)
        for u in map(upgrade, docs(os.path.join(sub, 'upgrades'))):
            if u['name'] in core_up:
                a['upgrade_variants'].setdefault(u['name'], []).append(([name], u))
            else:
                a['upgrades'][u['name']] = u
        a['legions'].append(dict(name=name, allegiance=c.get('allegiance'),
                                 cohesive=names(c, 'cohesive') if 'cohesive' in c.meta else a['cohesive'],
                                 disruptive=names(c, 'disruptive') if 'disruptive' in c.meta else a['disruptive'],
                                 notes=[t for t, _, _ in c.items('Notes')]))
    a['formations'] = list(core.values()) + plain + list(extra.values())


# ------------------------------------------------------------------ everything
def load(root=ROOT):
    data = dict(units=OrderedDict(), titan_weapons=OrderedDict(), fan_units=set(), fan_titan_weapons=set(),
                weapon_options=OrderedDict(), replaced_rows=OrderedDict(), titan_slots=OrderedDict(),
                rules=OrderedDict(), acronyms={}, aliases=[], patterns={}, armies=[], docs={})

    for d in docs(os.path.join(root, 'rules')):
        check_keys(d, {'acronym', 'pattern', 'matches'} | SITE_KEYS)
        data['rules'][d.title] = d.text()
        if d.get('acronym'):
            data['acronyms'][d.title] = d.get('acronym')
        if d.get('pattern'):
            data['patterns'][d.title] = d.get('pattern')
        data['aliases'] += [(pat, d.title) for pat in names(d, 'matches')]

    folders = sorted(f for f in os.listdir(root) if os.path.isdir(os.path.join(root, f)) and f != 'rules')
    for folder in folders:
        path = os.path.join(root, folder)
        for d in docs(os.path.join(path, 'units')):
            u = unit(d)
            sheet = d.get('sheet', folder)
            if any(x['name'] == u['name'] for x in data['units'].get(sheet, [])):
                raise d.error(f'{u["name"]!r} is on the {sheet} sheet twice')
            data['units'].setdefault(sheet, []).append(u)
            data['docs'][('unit', sheet, u['name'])] = d
            if d.get('fan-made'):
                data['fan_units'].add(u['name'])
            for key, value in (('weapon_options', weapon_options(d)), ('replaced_rows', names(d, 'replaced-rows')),
                               ('titan_slots', titan_slots(d))):
                if value:
                    if data[key].setdefault(u['name'], value) != value:
                        raise d.error(f'{u["name"]} has different {key.replace("_", " ")} on another sheet')
        for d in docs(os.path.join(path, 'weapons')):
            data['titan_weapons'][d.title] = titan_weapon(d)
            if d.get('fan-made'):
                data['fan_titan_weapons'].add(d.title)
        if os.path.exists(os.path.join(path, 'index.md')):
            data['armies'].append(army(path))
    return data
