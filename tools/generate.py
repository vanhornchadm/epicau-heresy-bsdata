"""Generate BattleScribe data (.gst/.cat) for the EpicAU Horus Heresy supplement.

Usage: python3 generate.py [output_dir]
Reads source/units.json (reference sheets) and source/titan_weapons.json, plus the
hand-transcribed army list specs in spec_legion.py / spec_others.py.
"""
import hashlib
import json
import os
import re
import sys
from xml.sax.saxutils import escape, quoteattr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rules import RULES, ALIASES  # noqa: E402
from spec_legion import legion_army, LEGIONS  # noqa: E402
from spec_others import OTHER_ARMIES, TITAN_WEAPON_SLOTS  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
BS_VERSION = '2.03'
AUTHOR = 'EpicAU Horus Heresy (community) - BSData conversion'
SOURCE_URL = 'https://web.archive.org/web/20201111221247/http://epicau.com/mw/index.php/Main_Page'
GST_NAME = 'Epic Armageddon - EpicAU Horus Heresy'
GST_FILE = 'Epic Armageddon - EpicAU Horus Heresy.gst'


def gid(*key):
    h = hashlib.md5('|'.join(str(k) for k in key).encode()).hexdigest()
    return f'{h[0:4]}-{h[4:8]}-{h[8:12]}-{h[12:16]}'


GST_ID = gid('gst', GST_NAME)
PTS = 'points'
PT_UNIT, PT_WEAPON = gid('pt', 'Unit'), gid('pt', 'Weapon')
UNIT_CHARS = ['Type', 'Speed', 'Armour', 'CC', 'FF', 'Notes']
WEAPON_CHARS = ['Range', 'Firepower', 'Notes']
CATS = ['Line Detachment', 'Support Detachment', 'Lord of War', 'Daemonic Horde', 'Greater Daemon Horde',
        'Followers of Chaos', 'Special Selection', 'Allies & Lords of War', 'Supreme Commander', 'Spacecraft',
        'Primarch', 'Character', 'Configuration', 'Tactical Transport Space']
HIDDEN_CATS = {'Configuration', 'Tactical Transport Space'}  # internal bookkeeping categories
CAT = {c: gid('cat', c) for c in CATS}
SLOT_CAT = {'line': 'Line Detachment', 'support': 'Support Detachment', 'low': 'Lord of War',
            'horde': 'Daemonic Horde', 'greater': 'Greater Daemon Horde', 'followers': 'Followers of Chaos',
            'special': 'Special Selection'}
RULE_ID = {name: gid('rule', name) for name in RULES}

# Unit not present on the wiki reference sheet (stats from Departmento Munitorum).
EXTRA_UNITS = {
    'Legion Astartes': [{
        'name': 'Sabre Strike Tank', 'type': 'AV', 'speed': '35cm', 'armour': '5+', 'cc': '6+', 'ff': '5+',
        'weapons': [{'name': 'Volkite Saker', 'range': '15cm', 'firepower': '2 x AP3+, Fleshbane, FxF'},
                    {'name': 'Sabre Missiles', 'range': '30cm', 'firepower': 'AT4+, FxF'}],
        'notes': 'Reinforced Armour. (Not on the wiki reference sheet; stats from Departmento Munitorum.)'}],
}


# ------------------------------------------------------------------ XML helpers
class X:
    """Tiny XML element builder."""

    def __init__(self, tag, attrs=None, children=None, text=None):
        self.tag, self.attrs, self.children, self.text = tag, attrs or {}, children or [], text

    def add(self, *kids):
        self.children.extend(k for k in kids if k is not None)
        return self

    def render(self, ind=0):
        sp = '  ' * ind
        attrs = ''.join(f' {k}={quoteattr(str(v))}' for k, v in self.attrs.items() if v is not None)
        if self.text is not None:
            return f'{sp}<{self.tag}{attrs}>{escape(self.text)}</{self.tag}>'
        kids = [c for c in self.children if c is not None and not (isinstance(c, X) and c.empty_list())]
        if not kids:
            return f'{sp}<{self.tag}{attrs}/>'
        inner = '\n'.join(c.render(ind + 1) for c in kids)
        return f'{sp}<{self.tag}{attrs}>\n{inner}\n{sp}</{self.tag}>'

    def empty_list(self):
        return self.tag.endswith('s') and self.tag not in ('characteristics',) and not self.children and \
            not self.attrs and self.text is None and self.tag in LIST_TAGS


LIST_TAGS = {'modifiers', 'constraints', 'profiles', 'rules', 'infoLinks', 'categoryLinks', 'selectionEntries',
             'selectionEntryGroups', 'entryLinks', 'costs', 'repeats', 'conditions', 'conditionGroups',
             'characteristics', 'forceEntries', 'sharedSelectionEntries', 'sharedProfiles', 'sharedRules',
             'catalogueLinks', 'categoryEntries', 'publications'}


def ordered(tag, attrs, **parts):
    """Build an element with child lists in schema order."""
    order = ['comment', 'readme', 'publications', 'costTypes', 'profileTypes', 'categoryEntries', 'forceEntries',
             'modifiers', 'constraints', 'profiles', 'rules', 'infoGroups', 'infoLinks', 'categoryLinks',
             'selectionEntries', 'selectionEntryGroups', 'entryLinks', 'costs', 'sharedSelectionEntries',
             'sharedSelectionEntryGroups', 'sharedRules', 'sharedProfiles', 'catalogueLinks']
    el = X(tag, attrs)
    # force entries put forceEntries after infoLinks; handled by caller passing key 'forceEntries_late'
    for key in order:
        if key in parts and parts[key] is not None:
            v = parts[key]
            el.add(v if isinstance(v, X) else X(key, children=list(v)) if isinstance(v, list) else X(key, text=v))
        if key == 'infoLinks' and parts.get('forceEntries_late'):
            el.add(X('forceEntries', children=parts['forceEntries_late']))
    return el


def cost(value):
    return X('costs', children=[X('cost', {'name': 'pts', 'typeId': PTS, 'value': fmt(value)})])


def fmt(v):
    s = f'{float(v):.4f}'.rstrip('0')
    return s + '0' if s.endswith('.') else s


def constraint(cid, ctype, value, scope='parent', field='selections', shared=True, child=False, forces=False,
               percent=False):
    return X('constraint', {'field': field, 'scope': scope, 'value': fmt(value), 'percentValue': str(percent).lower(),
                            'shared': str(shared).lower(), 'includeChildSelections': str(child).lower(),
                            'includeChildForces': str(forces).lower(), 'id': cid, 'type': ctype})


def repeat(child_id, value, scope, field='selections', round_up=False, child=False, forces=False):
    return X('repeat', {'field': field, 'scope': scope, 'value': fmt(value), 'percentValue': 'false', 'shared': 'true',
                        'includeChildSelections': str(child).lower(), 'includeChildForces': str(forces).lower(),
                        'childId': child_id, 'repeats': '1', 'roundUp': str(round_up).lower()})


def condition(ctype, child_id, value, scope, field='selections', child=False, forces=False):
    return X('condition', {'field': field, 'scope': scope, 'value': fmt(value), 'percentValue': 'false',
                           'shared': 'true', 'includeChildSelections': str(child).lower(),
                           'includeChildForces': str(forces).lower(), 'childId': child_id, 'type': ctype})


def rule_el(rid, name, desc):
    return X('rule', {'id': rid, 'name': name, 'hidden': 'false'}, [X('description', text=desc)])


def info_rule(owner, name):
    return X('infoLink', {'id': gid('il', owner, name), 'name': name, 'hidden': 'false',
                          'targetId': RULE_ID[name], 'type': 'rule'})


def cat_link(owner, cat, primary=False):
    return X('categoryLink', {'id': gid('cl', owner, cat), 'name': cat, 'hidden': 'false', 'targetId': CAT[cat],
                              'primary': str(primary).lower()})


def per_points_limit(owner, maxn, per, round_up, scope='roster'):
    """0-maxn per full `per` points (or per army when per is None)."""
    cid = gid('con', owner, 'limit')
    if per is None:
        return [], [constraint(cid, 'max', maxn, scope=scope, child=True, forces=True)]
    mod = X('modifier', {'type': 'increment', 'field': cid, 'value': fmt(maxn)},
            [X('repeats', children=[repeat('any', per, 'roster', field=PTS, round_up=round_up, child=True,
                                           forces=True)])])
    return [mod], [constraint(cid, 'max', 0, scope=scope, child=True, forces=True)]


# ------------------------------------------------------------------ units & profiles
UNITS = json.load(open(os.path.join(HERE, 'source', 'units.json')))
for sheet, extra in EXTRA_UNITS.items():
    UNITS[sheet].extend(extra)
TITAN_WEAPONS = json.load(open(os.path.join(HERE, 'source', 'titan_weapons.json')))
# Rule keywords are capitalised on the wiki, so match case-sensitively to avoid hits like "transport capacity".
PATTERN_OVERRIDES = {'Scout': r'Scout(?! Titan)', 'Commander': r'(?<!Supreme )(?<!Lieutenant )(?<!Lord )Commander',
                     'Transport': r'Transport(?= ?[:.])'}
# A following capital is allowed so run-together text like "Ignore CoverAND" still matches.
RULE_PATTERNS = [(name, re.compile(r'(?<![A-Za-z])' + PATTERN_OVERRIDES.get(name, re.escape(name)) + r'(?![a-z])'))
                 for name in RULES]
ALIAS_PATTERNS = [(target, re.compile(r'(?<![A-Za-z])(?:' + pat + r')(?![a-z])')) for pat, target in ALIASES]
for _, target in ALIASES:
    assert target in RULES, f'alias target {target!r} has no rule'


def rules_in(text):
    found = [n for n, p in RULE_PATTERNS if p.search(text)]
    found += [t for t, p in ALIAS_PATTERNS if p.search(text) and t not in found]
    return list(dict.fromkeys(found))


class Catalogue:
    """Collects shared profiles for one catalogue (or library)."""

    def __init__(self, scope):
        self.scope = scope
        self.profiles = {}  # pid -> X

    def unit_profiles(self, unit):
        """Return (profile ids, rule names, categories) for a unit record, registering shared profiles."""
        key = (self.scope, unit['name'])
        uid = gid('prof', *key, 'unit')
        if uid not in self.profiles:
            vals = [unit['type'], unit['speed'], unit['armour'], unit['cc'], unit['ff'], unit['notes']]
            self.profiles[uid] = profile(uid, unit['name'], PT_UNIT, 'Unit', UNIT_CHARS, vals)
        ids = [(uid, unit['name'])]
        for i, w in enumerate(unit['weapons']):
            if not (w['name'] or w['firepower']) or w['name'] in ('-',):
                continue
            wid = gid('prof', *key, 'weapon', i)
            if wid not in self.profiles:
                self.profiles[wid] = profile(wid, w['name'] or 'Weapons', PT_WEAPON, 'Weapon', WEAPON_CHARS,
                                             [w['range'], w['firepower'], 'Weapon lines are combined; check the wiki sheet.' if w.get('misaligned') else ''])
            ids.append((wid, w['name'] or 'Weapons'))
        text = unit['notes'] + ' ' + ' '.join(w['firepower'] for w in unit['weapons'])
        cats = []
        if unit['type'].startswith('CH'):
            cats.append('Character')
        if unit['type'] == 'SC':
            cats.append('Spacecraft')
        if 'Supreme Commander' in unit['notes']:
            cats.append('Supreme Commander')
        if 'Demi-God' in unit['notes']:
            cats.append('Primarch')
        return ids, rules_in(text), cats

    def weapon_profile(self, w):
        wid = gid('prof', self.scope, 'titan-weapon', w['name'])
        if wid not in self.profiles:
            self.profiles[wid] = profile(wid, w['name'], PT_WEAPON, 'Weapon', WEAPON_CHARS,
                                         [w['range'], w['firepower'], w['notes']])
        return wid


def profile(pid, name, type_id, type_name, chars, vals):
    return X('profile', {'id': pid, 'name': name, 'hidden': 'false', 'typeId': type_id, 'typeName': type_name}, [
        X('characteristics', children=[X('characteristic', {'name': c, 'typeId': gid('ct', type_name, c)},
                                         text=v or '-') for c, v in zip(chars, vals)])])


# ------------------------------------------------------------------ list -> XML
class Builder:
    def __init__(self, army, cat_id, profiles, allied_force_id):
        self.army, self.cat_id, self.prof, self.allied_force_id = army, cat_id, profiles, allied_force_id
        self.missing = []
        self.formation_id = None  # set while a formation is being built (scope for transport counts)

    def find_unit(self, name):
        for sheet in self.army['sheets']:
            for u in UNITS.get(sheet, []):
                if u['name'] == name:
                    return u
        self.missing.append(name)
        return {'name': name, 'type': '?', 'speed': '', 'armour': '', 'cc': '', 'ff': '', 'weapons': [],
                'notes': 'Unit not found on the reference sheet.'}

    # -- unit entries
    def unit_entry(self, path, part, name=None):
        unit = self.find_unit(part['unit'])
        eid = gid('se', self.cat_id, path)
        ids, rules, cats = self.prof.unit_profiles(unit)
        space = self.army['transport_space']
        if space and (unit['name'] in space or 'Demi-God' in unit['notes']):
            cats = cats + ['Tactical Transport Space']
        cons = []
        if part['min'] is not None and part['min'] > 0:
            cons.append(constraint(gid('con', eid, 'min'), 'min', part['min']))
        if part['max'] is not None:
            cons.append(constraint(gid('con', eid, 'max'), 'max', part['max']))
        links = [X('infoLink', {'id': gid('il', eid, pid), 'name': pname, 'hidden': 'false', 'targetId': pid,
                                'type': 'profile'}) for pid, pname in ids]
        links += [info_rule(eid, r) for r in rules]
        return ordered('selectionEntry', {'id': eid, 'name': name or part['label'] or unit['name'], 'hidden': 'false',
                                          'collective': 'false', 'import': 'true', 'type': 'model'},
                       constraints=cons, infoLinks=links,
                       categoryLinks=[cat_link(eid, c) for c in cats], costs=cost(part['each']))

    def parts(self, path, parts):
        """Convert DSL parts to (selectionEntries, selectionEntryGroups)."""
        ses, grps = [], []
        for i, p in enumerate(parts):
            pp = f'{path}/{i}'
            if p['kind'] == 'unit':
                ses.append(self.unit_entry(pp, p))
            elif p['kind'] == 'or':
                gid_ = gid('seg', self.cat_id, pp)
                opts = []
                for j, o in enumerate(p['opts']):
                    oid = gid('se', self.cat_id, pp, j)
                    s2, g2 = self.parts(f'{pp}/{j}', o['parts'])
                    opts.append(ordered('selectionEntry', {'id': oid, 'name': o['label'], 'hidden': 'false',
                                                           'collective': 'false', 'import': 'true', 'type': 'upgrade'},
                                        constraints=[constraint(gid('con', oid, 'max'), 'max', 1)],
                                        selectionEntries=s2, selectionEntryGroups=g2, costs=cost(o['cost'])))
                grps.append(ordered('selectionEntryGroup',
                                    {'id': gid_, 'name': p['label'], 'hidden': 'false', 'collective': 'false',
                                     'import': 'true', 'defaultSelectionEntryId': opts[0].attrs['id']},
                                    constraints=[constraint(gid('con', gid_, 'min'), 'min', 1),
                                                 constraint(gid('con', gid_, 'max'), 'max', 1)],
                                    selectionEntries=opts))
            elif p['kind'] == 'mix':
                gid_ = gid('seg', self.cat_id, pp)
                cons = []
                if p['min']:
                    cons.append(constraint(gid('con', gid_, 'min'), 'min', p['min']))
                if p['max'] is not None:
                    cons.append(constraint(gid('con', gid_, 'max'), 'max', p['max']))
                kids = [self.unit_entry(f'{pp}/{j}', dict(u, min=0)) for j, u in enumerate(p['units'])]
                grps.append(ordered('selectionEntryGroup', {'id': gid_, 'name': p['label'], 'hidden': 'false',
                                                            'collective': 'false', 'import': 'true'},
                                    constraints=cons, selectionEntries=kids))
            elif p['kind'] == 'fill':
                grps.append(self.fill_group(pp, p))
            elif p['kind'] == 'swap':
                gid_ = gid('seg', self.cat_id, pp)
                cons = [constraint(gid('con', gid_, 'min'), 'min', p['min'])] if p['min'] else []
                if p['max'] is not None:
                    cons.append(constraint(gid('con', gid_, 'max'), 'max', p['max']))
                kids = []
                for j, (frm, to, each) in enumerate(p['swaps']):
                    e = self.unit_entry(f'{pp}/{j}', {'unit': to, 'min': 0, 'max': p['max'], 'each': each, 'label': None},
                                        name=f'{to} (replaces {frm})')
                    e.attrs['type'] = 'upgrade'
                    kids.append(e)
                grps.append(ordered('selectionEntryGroup', {'id': gid_, 'name': p['label'], 'hidden': 'false',
                                                            'collective': 'false', 'import': 'true'},
                                    constraints=cons, selectionEntries=kids))
        return ses, grps

    def fill_group(self, path, p):
        """Transports sized to the formation: min = max = ceil(tagged units / per), any mix of types."""
        if not self.formation_id:
            raise ValueError(f'{self.army["name"]}: transport fill outside a formation ({path})')
        g = gid('seg', self.cat_id, path)
        kids = [self.unit_entry(f'{path}/{j}', u) for j, u in enumerate(p['units'])]
        cmin, cmax = gid('con', g, 'min'), gid('con', g, 'max')
        mods = [X('modifier', {'type': 'increment', 'field': c, 'value': '1'},
                  [X('repeats', children=[repeat(CAT[p['space']], p['per'], self.formation_id, round_up=True,
                                                 child=True)])]) for c in (cmin, cmax)]
        return ordered('selectionEntryGroup', {'id': g, 'name': p['label'], 'hidden': 'false', 'collective': 'false',
                                               'import': 'true', 'defaultSelectionEntryId': kids[0].attrs['id']},
                       modifiers=mods, constraints=[constraint(cmin, 'min', 0), constraint(cmax, 'max', 0)],
                       selectionEntries=kids)

    # -- upgrades
    @staticmethod
    def formation_bound(u):
        """Upgrades whose contents depend on the formation are built inline rather than shared."""
        return any(p['kind'] == 'fill' for p in u['parts'])

    def upgrade_entry(self, uid, name, u, path, extra_cons=()):
        ses, grps = self.parts(path, u['parts'])
        mods, cons = ([], [])
        if u['maxn'] is not None:
            mods, cons = per_points_limit(uid, u['maxn'], u['per'], u['round_up'])
        cons = cons + list(extra_cons)
        rules = [rule_el(gid('r', uid), name, u['desc'])] if u['desc'] else []
        return ordered('selectionEntry', {'id': uid, 'name': name, 'hidden': 'false', 'collective': 'false',
                                          'import': 'true', 'type': 'upgrade'},
                       modifiers=mods, constraints=cons, rules=rules,
                       infoLinks=[info_rule(uid, r) for r in u['rules']],
                       selectionEntries=ses, selectionEntryGroups=grps, costs=cost(u['cost']))

    def shared_upgrades(self):
        return [self.upgrade_entry(self.upgrade_id(name), name, u, f'upgrade/{name}')
                for name, u in self.army['upgrades'].items() if not self.formation_bound(u)]

    def upgrade_id(self, name):
        return gid('upgrade', self.cat_id, name)

    def upgrade_link(self, owner, name):
        """An entryLink to the shared upgrade, or an inline copy for formation-bound upgrades."""
        if name not in self.army['upgrades']:
            raise KeyError(f'{self.army["name"]}: unknown upgrade {name!r} in {owner}')
        u = self.army['upgrades'][name]
        if self.formation_bound(u):
            uid = gid('upgrade', owner, name)
            return self.upgrade_entry(uid, name, u, f'{owner}/upgrade/{name}',
                                      extra_cons=[constraint(gid('con', uid, 'max'), 'max', 1)])
        lid = gid('el', owner, name)
        return X('entryLink', {'id': lid, 'name': name, 'hidden': 'false', 'collective': 'false', 'import': 'true',
                               'targetId': self.upgrade_id(name), 'type': 'selectionEntry'},
                 [X('constraints', children=[constraint(gid('con', lid, 'max'), 'max', 1)])])

    @staticmethod
    def split(items):
        return [i for i in items if i.tag == 'selectionEntry'], [i for i in items if i.tag == 'entryLink']

    def upgrades_group(self, fid, f):
        cap = {'support': self.army['support_cap'], 'low': self.army['low_cap']}.get(f['slot'], self.army['upgrade_cap'])
        links, groups = [], []
        for chunk in [c.strip() for c in f['up'].split(',') if c.strip()]:
            names = [n.strip() for n in chunk.split(' OR ')]
            if len(names) == 1:
                links.append(self.upgrade_link(fid, names[0]))
            else:
                sg = gid('seg', fid, chunk)
                ses, els = self.split([self.upgrade_link(sg, n) for n in names])
                groups.append(ordered('selectionEntryGroup', {'id': sg, 'name': ' / '.join(names), 'hidden': 'false',
                                                              'collective': 'false', 'import': 'true'},
                                      constraints=[constraint(gid('con', sg, 'max'), 'max', 1)],
                                      selectionEntries=ses, entryLinks=els))
        if not links and not groups:
            return None
        g = gid('seg', fid, 'upgrades')
        cons = [constraint(gid('con', g, 'max'), 'max', cap)] if cap else []
        ses, els = self.split(links)
        return ordered('selectionEntryGroup', {'id': g, 'name': 'Upgrades', 'hidden': 'false', 'collective': 'false',
                                               'import': 'true'},
                       constraints=cons, selectionEntries=ses, selectionEntryGroups=groups, entryLinks=els)

    def titan_weapons(self, fid, f):
        count = 0
        slots = None
        for p in f['units']:
            if p['kind'] == 'unit' and p['unit'] in TITAN_WEAPON_SLOTS:
                n, weapons = TITAN_WEAPON_SLOTS[p['unit']]
                count += n * p['min']
                slots = weapons
        if not count:
            return None
        g = gid('seg', fid, 'titan-weapons')
        kids = []
        for name, each in slots:
            w = TITAN_WEAPONS[name]
            eid = gid('se', fid, 'tw', name)
            pid = self.prof.weapon_profile(w)
            kids.append(ordered('selectionEntry', {'id': eid, 'name': name, 'hidden': 'false', 'collective': 'false',
                                                   'import': 'true', 'type': 'upgrade'},
                                constraints=[constraint(gid('con', eid, 'max'), 'max', count)],
                                infoLinks=[X('infoLink', {'id': gid('il', eid), 'name': name, 'hidden': 'false',
                                                          'targetId': pid, 'type': 'profile'})]
                                + [info_rule(eid, r) for r in rules_in(w['firepower'] + ' ' + w['notes'])],
                                costs=cost(each)))
        return ordered('selectionEntryGroup', {'id': g, 'name': 'Titan Weapons', 'hidden': 'false',
                                               'collective': 'false', 'import': 'true'},
                       constraints=[constraint(gid('con', g, 'min'), 'min', count),
                                    constraint(gid('con', g, 'max'), 'max', count)], selectionEntries=kids)

    # -- formations
    def formation(self, f):
        fid = gid('formation', self.cat_id, f['slot'], f['name'])
        self.formation_id = fid
        primary = SLOT_CAT[f['slot']]
        cats = [cat_link(fid, primary, True)]
        if f['slot'] == 'low':
            cats.append(cat_link(fid, 'Allies & Lords of War'))
        if any(p['kind'] == 'or' and any('Battleship' in o['label'] or 'Cruiser' in o['label'] or 'Barge' in o['label']
                                         for o in p['opts']) for p in f['units']):
            cats.append(cat_link(fid, 'Spacecraft'))
        if f['name'] == 'Daemonic Overlord':
            cats.append(cat_link(fid, 'Supreme Commander'))
        mods, cons = [], []
        if f['maxn'] is not None:
            mods, cons = per_points_limit(fid, f['maxn'], f['per'], f['round_up'])
        # Formations bought for an allied contingent count towards the Allies & Lords of War allowance.
        if f['slot'] != 'low':
            mods.append(X('modifier', {'type': 'add', 'field': 'category', 'value': CAT['Allies & Lords of War']},
                          [X('conditions', children=[condition('instanceOf', self.allied_force_id, 1, 'force')])]))
        if f['name'] == 'Daemonic Overlord':
            cid = gid('con', fid, 'required')
            cons.append(constraint(cid, 'min', 1, scope='force'))
            mods.append(X('modifier', {'type': 'set', 'field': cid, 'value': '0'},
                          [X('conditions', children=[condition('instanceOf', self.allied_force_id, 1, 'force')])]))
        rules = [rule_el(gid('r', fid), f['name'], f['note'])] if f['note'] else []
        ses, grps = self.parts(f'formation/{f["slot"]}/{f["name"]}', f['units'])
        tw = self.titan_weapons(fid, f)
        up = self.upgrades_group(fid, f)
        extra = [self.upgrade_link(fid + '/extra', n) for n in f['extra_up']]
        return ordered('selectionEntry', {'id': fid, 'name': f['name'], 'hidden': 'false', 'collective': 'false',
                                          'import': 'true', 'type': 'unit'},
                       modifiers=mods, constraints=cons, rules=rules,
                       infoLinks=[info_rule(fid, r) for r in f['rules']], categoryLinks=cats,
                       selectionEntries=ses, selectionEntryGroups=grps + [g for g in (tw, up) if g],
                       entryLinks=extra, costs=cost(f['cost']))

    # -- forces
    def force(self, allied):
        a = self.army
        fid = self.allied_force_id if allied else gid('force', self.cat_id, 'primary')
        name = f'{a["name"]} (Allied Contingent)' if allied else a['name']
        slots = sorted({f['slot'] for f in a['formations']}, key=list(SLOT_CAT).index)
        links = []
        for slot in slots:
            cname = SLOT_CAT[slot]
            lid = gid('cl', fid, cname)
            mods, cons = [], []
            dependent = {'support': ('Line Detachment', a['supports_per_line']),
                         'followers': ('Daemonic Horde', 1), 'greater': ('Daemonic Horde', 1)}.get(slot)
            if dependent:
                cid = gid('con', lid, 'ratio')
                cons.append(constraint(cid, 'max', 0))
                mods.append(X('modifier', {'type': 'increment', 'field': cid, 'value': fmt(dependent[1])},
                              [X('repeats', children=[repeat(CAT[dependent[0]], 1, 'parent')])]))
            links.append(ordered('categoryLink', {'id': lid, 'name': cname, 'hidden': 'false', 'targetId': CAT[cname],
                                                  'primary': 'false'}, modifiers=mods, constraints=cons))
        sc_id = gid('cl', fid, 'Supreme Commander')
        if allied:
            sc = [constraint(gid('con', sc_id, 'max'), 'max', 0, scope='parent', child=True)]
            extra = []
        else:
            sc = [constraint(gid('con', sc_id, 'max'), 'max', 1, scope='roster', child=True, forces=True)]
            sp_id = gid('cl', fid, 'Spacecraft')
            extra = [ordered('categoryLink', {'id': sp_id, 'name': 'Spacecraft', 'hidden': 'false',
                                              'targetId': CAT['Spacecraft'], 'primary': 'false'},
                             constraints=[constraint(gid('con', sp_id, 'max'), 'max', 1, scope='roster', child=True,
                                                     forces=True)])]
            if a['allies_fraction']:
                al = gid('cl', fid, 'Allies & Lords of War')
                extra.append(ordered('categoryLink', {'id': al, 'name': 'Allies & Lords of War', 'hidden': 'false',
                                                      'targetId': CAT['Allies & Lords of War'], 'primary': 'false'},
                                     constraints=[constraint(gid('con', al, 'max'), 'max',
                                                             round(a['allies_fraction'] * 100, 2), scope='roster',
                                                             field=PTS, child=True, forces=True, percent=True)]))
        links.append(ordered('categoryLink', {'id': sc_id, 'name': 'Supreme Commander', 'hidden': 'false',
                                              'targetId': CAT['Supreme Commander'], 'primary': 'false'},
                             constraints=sc))
        links += extra
        desc = self.army_summary(allied)
        return ordered('forceEntry', {'id': fid, 'name': name, 'hidden': 'false'},
                       rules=[rule_el(gid('r', fid), 'Army List', desc)],
                       infoLinks=[info_rule(fid, r) for r in a['rules']], categoryLinks=links)

    def army_summary(self, allied):
        a = self.army
        lines = [f'Strategy Rating {a["strategy"]}. Formation initiative {a["initiative"]}.']
        if a['supports_per_line']:
            lines.append(f'{a["supports_per_line"]} Support Detachments may be taken per Line Detachment.')
        lines += a['notes']
        if a['cohesive'] or a['disruptive']:
            lines.append('Cohesive allies: ' + (', '.join(a['cohesive']) or 'none') + '.')
            lines.append('Disruptive allies: ' + (', '.join(a['disruptive']) or 'none') + '.')
        if allied:
            lines.append('Allied Contingent: formations here count towards the primary army\'s Allies & Lords of War '
                         'allowance. Supreme Commanders must come from the primary army.')
        return '\n'.join(lines)


XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
ROOT_REV = re.compile(r'(<(?:gameSystem|catalogue)\b[^>]*?) (?:gameSystemRevision|revision)="\d+"')
GST_REVISION = [1]  # set once the game system is written; catalogues record it as gameSystemRevision


def without_revisions(text):
    """File text with the root element's revision attributes removed, for change detection."""
    prev = None
    while prev != text:
        prev, text = text, ROOT_REV.sub(r'\1', text, count=1)
    return text


def write(path, root, ns):
    """Write a data file, bumping its revision only when its content changed.

    Unchanged files are left untouched; new files start at revision 1. A changed catalogue
    also records the game system revision it was built against.
    """
    root.attrs['xmlns'] = ns
    old = open(path, encoding='utf-8').read() if os.path.exists(path) else None
    m = old and re.search(r'<(?:gameSystem|catalogue)\b[^>]*?\brevision="(\d+)"', old)
    old_rev = int(m.group(1)) if m else 0
    root.attrs['revision'] = max(old_rev, 1)
    if 'gameSystemId' in root.attrs:
        root.attrs['gameSystemRevision'] = GST_REVISION[0]
    text = XML_DECL + root.render() + '\n'
    if old is not None and without_revisions(old) == without_revisions(text):
        return old_rev
    root.attrs['revision'] = old_rev + 1
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(XML_DECL + root.render() + '\n')
    return old_rev + 1


CAT_NS = 'http://www.battlescribe.net/schema/catalogueSchema'
GST_NS = 'http://www.battlescribe.net/schema/gameSystemSchema'


def header(cid, name, library=False):
    return {'id': cid, 'name': name, 'revision': 1, 'battleScribeVersion': BS_VERSION, 'authorName': AUTHOR,
            'authorContact': '', 'authorUrl': SOURCE_URL, 'library': str(library).lower(), 'gameSystemId': GST_ID,
            'gameSystemRevision': GST_REVISION[0]}


def build_gst():
    readme = ('Horus Heresy supplement for Net Epic Armageddon developed by the EpicAU community. Converted from the '
              f'archived EpicAU wiki ({SOURCE_URL}). Rules text is summarised; see the wiki and the NetEA rulebook '
              'for full wording. Add a primary army force, then optionally an Allied Contingent force from another '
              'catalogue.')
    root = ordered('gameSystem', {'id': GST_ID, 'name': GST_NAME, 'revision': 1, 'battleScribeVersion': BS_VERSION,
                                  'authorName': AUTHOR, 'authorContact': '', 'authorUrl': SOURCE_URL},
                   readme=readme,
                   publications=[X('publication', {'id': gid('pub', 'wiki'), 'name': 'EpicAU Wiki - Horus Heresy Supplement',
                                                   'publisherUrl': SOURCE_URL})],
                   costTypes=X('costTypes', children=[X('costType', {'id': PTS, 'name': 'pts', 'defaultCostLimit': '-1.0',
                                                                    'hidden': 'false'})]),
                   profileTypes=X('profileTypes', children=[
                       X('profileType', {'id': PT_UNIT, 'name': 'Unit'}, [X('characteristicTypes', children=[
                           X('characteristicType', {'id': gid('ct', 'Unit', c), 'name': c}) for c in UNIT_CHARS])]),
                       X('profileType', {'id': PT_WEAPON, 'name': 'Weapon'}, [X('characteristicTypes', children=[
                           X('characteristicType', {'id': gid('ct', 'Weapon', c), 'name': c}) for c in WEAPON_CHARS])])]),
                   categoryEntries=[X('categoryEntry', {'id': CAT[c], 'name': c, 'hidden': str(c in HIDDEN_CATS).lower()})
                                    for c in CATS],
                   sharedRules=[rule_el(RULE_ID[n], n, d) for n, d in RULES.items()])
    GST_REVISION[0] = write(os.path.join(OUT, GST_FILE), root, GST_NS)


def build_catalogue(army, library=None):
    cid = gid('cat', army['name'])
    profiles = library or Catalogue(army['name'])
    b = Builder(army, cid, profiles, gid('force', cid, 'allied'))
    formations = [b.formation(f) for f in army['formations']]
    upgrades = b.shared_upgrades()
    forces = [b.force(False), b.force(True)]
    links = None
    if library:
        links = [X('catalogueLink', {'id': gid('catlink', cid, 'lib'), 'name': LIB_NAME, 'targetId': LIB_ID,
                                     'type': 'catalogue', 'importRootEntries': 'false'})]
    root = ordered('catalogue', header(cid, f'EpicAU - {army["name"]}'), forceEntries=forces,
                   selectionEntries=formations, sharedSelectionEntries=upgrades,
                   sharedProfiles=None if library else sorted(profiles.profiles.values(), key=lambda p: p.attrs['name']),
                   catalogueLinks=links)
    write(os.path.join(OUT, f'EpicAU - {army["name"]}.cat'), root, CAT_NS)
    return b.missing


LIB_NAME = 'EpicAU - Legion Astartes Library'
LIB_ID = gid('cat', LIB_NAME)


def main():
    os.makedirs(OUT, exist_ok=True)
    build_gst()
    missing = {}
    lib = Catalogue('Legion Astartes Library')
    armies = [legion_army()] + [legion_army(l) for l in LEGIONS]
    for a in armies:
        m = build_catalogue(a, lib)
        if m:
            missing[a['name']] = sorted(set(m))
    root = ordered('catalogue', header(LIB_ID, LIB_NAME, library=True),
                   sharedProfiles=sorted(lib.profiles.values(), key=lambda p: p.attrs['name']))
    write(os.path.join(OUT, f'{LIB_NAME}.cat'), root, CAT_NS)
    for a in OTHER_ARMIES:
        m = build_catalogue(a)
        if m:
            missing[a['name']] = sorted(set(m))
    for k, v in missing.items():
        print(f'MISSING units in {k}: {v}')
    print(f'Wrote {len(armies) + len(OTHER_ARMIES) + 1} catalogues and 1 game system to {OUT}')
    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
