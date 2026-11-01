"""Extract Legio Titanicus weapon variants (their table layout differs from unit rows)."""
import json, os, re, sys
P = sys.argv[1]  # directory of parsed wiki JSON
d = json.load(open(os.path.join(P, 'Legio_Titanicus_Reference_List.json')))
out, inside = {}, False
FIX = {'Apocalypse Missile Launcer': 'Apocalypse Missile Launcher'}
for x in d:
    if 'h' in x:
        inside = x['text'].startswith('Weapon Variants')
        continue
    if not inside or 'table' not in x:
        continue
    for r in x['table'][1:]:
        cells = [c['text'] for c in r]
        if len(cells) == 5:  # first row carries the group label ("Scout Titan Weapons")
            cells = cells[1:]
        if len(cells) < 4:
            continue
        name, rng, fp, note = cells[:4]
        if 'Reference' in name:
            continue
        lines = name.split('\n')
        name, extra = lines[0], lines[1:]
        m = re.match(r'(.*?)\s*\((.*)\)$', name)
        notes = []
        if m:
            name, notes = m.group(1), [m.group(2)]
        name = FIX.get(name, name)
        if extra:
            # Support Missile: warhead names on extra lines, firepower lines pair with them
            fps = fp.split('\n')
            fp = fps[0] + '; ' + '; '.join(f'{w}: {f}' for w, f in zip(extra[1:], fps[1:]))
        if note.strip() not in ('-', ''):
            notes.append(note.strip())
        out[name] = {'name': name, 'range': rng.replace('\n', ' '), 'firepower': fp.replace('\n', ' '),
                     'notes': '; '.join(notes)}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source', 'titan_weapons.json'), 'w'),
          indent=1, ensure_ascii=False)
for k, v in out.items(): print(k, '|', v['range'], '|', v['firepower'], '|', v['notes'])
