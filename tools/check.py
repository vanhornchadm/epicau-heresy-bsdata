"""Integrity checks: unique ids and resolvable references across the data set."""
import glob, os, sys, collections
import xml.etree.ElementTree as ET
D = sys.argv[1]
def ids_and_refs(path):
    root = ET.parse(path).getroot()
    ids, refs = collections.Counter(), []
    for el in root.iter():
        tag = el.tag.split('}')[1]
        if 'id' in el.attrib and tag not in ('cost',):
            ids[el.attrib['id']] += 1
        for a in ('targetId', 'childId', 'defaultSelectionEntryId', 'typeId'):
            if a in el.attrib and el.attrib[a] not in ('any', 'points', 'model', 'unit', 'upgrade'):
                refs.append((tag, a, el.attrib[a]))
        if tag == 'modifier' and el.attrib.get('field') not in ('category', 'points', 'hidden', 'name'):
            refs.append((tag, 'field', el.attrib['field']))
    return root, ids, refs
gst = glob.glob(os.path.join(D, '*.gst'))[0]
_, gids, grefs = ids_and_refs(gst)
problems = 0
for p in sorted(glob.glob(os.path.join(D, '*.cat'))):
    root, ids, refs = ids_and_refs(p)
    dup = [i for i, n in ids.items() if n > 1]
    clash = [i for i in ids if i in gids]
    pool = set(ids) | set(gids)
    for k in ids:  # characteristic types live in gst
        pass
    unresolved = sorted({(t, a, r) for t, a, r in refs if r not in pool})
    ns = '{http://www.battlescribe.net/schema/catalogueSchema}'
    forms = root.findall(f'{ns}selectionEntries/{ns}selectionEntry')
    if dup or clash or unresolved:
        problems += 1
        print('PROBLEM', os.path.basename(p), 'dups', dup[:5], 'clash', clash[:5], 'unresolved', unresolved[:8])
    else:
        print('ok', os.path.basename(p), len(forms), 'formations')
sys.exit(1 if problems else 0)
