"""Parse wiki reference sheets into units.json: {sheet: [unit,...]}."""
import json, os, re, sys
P = sys.argv[1]
SHEETS = {
 'Legion Astartes': 'Legion_Astartes_Reference_Sheet', 'Loyalist Legions': 'Loyalist_Legion_Reference_List',
 'Traitor Legions': 'Traitor_Legion_Reference_Sheet', 'Legio Custodes': 'Legio_Custodes_Reference_List',
 'Solar Auxilia': 'Solar_Auxilia_Reference_List', 'Mechanicum Taghmata': 'Mechanicum_Taghmata_Reference_List',
 'Legio Titanicus': 'Legio_Titanicus_Reference_List', 'Knight Household': 'Knight_Household_Reference_List',
 'Imperial Militia': 'Imperial_Militia_Reference_List', 'Daemons Of The Ruinstorm': 'Daemons_Of_The_Ruinstorm_Reference_List',
 'Orks of Telon Reach': 'Orks_of_Telon_Reach_Reference_Sheet'}
TYPES = re.compile(r'^(CH|INF|LV|AV|WE|AC|SC|AC/WE|WE/AC|Special|DG|Demi-God|INF/CH|CH/INF|LV/WE|AV/WE)\b', re.I)
def lines(t): return [l.strip() for l in t.split('\n')] if t else []
out = {}
for army, page in SHEETS.items():
    d = json.load(open(os.path.join(P, page + '.json')))
    units = []; section = ''
    for x in d:
        if 'h' in x: section = x['text']; continue
        if 'table' not in x: continue
        rows = x['table']
        hdr = [c['text'].strip().lower() for c in rows[0]]
        if 'name' not in hdr or 'weapons' not in hdr: continue
        for r in rows[1:]:
            cells = [c['text'] for c in r]
            if len(cells) < len(hdr):
                cells += [''] * (len(hdr) - len(cells))
            rec = dict(zip(hdr, cells))
            # header order of type/speed is inconsistent; detect by value
            t, s = rec.get('type', ''), rec.get('speed', '')
            if not TYPES.match(t.strip()) and TYPES.match(s.strip()): t, s = s, t
            w, rg, fp = lines(rec.get('weapons', '')), lines(rec.get('range', '')), lines(rec.get('firepower', ''))
            n = max(len(w), len(rg), len(fp))
            aligned = len(w) == len(rg) == len(fp)
            weapons = []
            if aligned:
                for i in range(n): weapons.append({'name': w[i], 'range': rg[i], 'firepower': fp[i]})
            else:
                weapons.append({'name': ' / '.join(w), 'range': ' / '.join(rg), 'firepower': ' / '.join(fp), 'misaligned': True})
            notes = rec.get('notes', rec.get('note', ''))
            units.append({'name': re.sub(r'\s+', ' ', rec['name']).strip(), 'section': section,
                          'type': ' / '.join(lines(t)), 'speed': ' / '.join(lines(s)),
                          'armour': ' / '.join(lines(rec.get('armour', ''))), 'cc': ' / '.join(lines(rec.get('cc', ''))),
                          'ff': ' / '.join(lines(rec.get('ff', ''))), 'weapons': weapons,
                          'notes': re.sub(r'\s+', ' ', notes.replace('\n', ' ')).strip().rstrip('"')})
    out[army] = units
json.dump(out, open(os.path.join(P, '..', 'units.json'), 'w'), indent=1, ensure_ascii=False)
for a, us in out.items():
    bad = [u['name'] for u in us if any(w.get('misaligned') for w in u['weapons'])]
    print(f'{a}: {len(us)} units, {len(bad)} misaligned weapons: {bad}')
    print('   ', '; '.join(f"{u['name']} [{u['type']}]" for u in us))
