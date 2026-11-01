# EpicAU Horus Heresy — BattleScribe data

BattleScribe (v2.03 schema) data for the EpicAU community's Horus Heresy supplement for Net Epic Armageddon, converted from the [archived EpicAU wiki](https://web.archive.org/web/20201111221247/http://epicau.com/mw/index.php/Main_Page). Where the wiki had gaps, [Departmento Munitorum](https://munitorum.com) was used, and each such case is listed below.

## Contents

| File | What it is |
|---|---|
| `Epic Armageddon - EpicAU Horus Heresy.gst` | Game system: costs, Unit/Weapon profile types, categories, shared special rules |
| `EpicAU - Legion Astartes.cat` | Core Legion list (no unique Legion) |
| `EpicAU - Legion Astartes - <Legion>.cat` ×18 | Core list overlaid with that Legion's formations, Primarch, allies and restrictions |
| `EpicAU - Legion Astartes Library.cat` | Library of Legion unit profiles shared by the 19 Legion catalogues |
| `EpicAU - Legio Custodes / Solar Auxilia / Mechanicum Taghmata / Legio Titanicus / Knight Household / Imperial Militia / Daemons Of The Ruinstorm.cat` | The other army lists |
| `tools/` | The scraper, list specs and generator used to build the files |

To use it, copy the `.gst` and `.cat` files into a BattleScribe data folder, or zip them as a data index.

## Building a roster

Each catalogue provides two forces:

- **`<Army>`**: the primary army.
- **`<Army> (Allied Contingent)`**: add one of these from another catalogue for allies.

These rules are enforced:

- Support Detachments: up to the list's number per Line Detachment (3 for Legion, Custodes and Mechanicum; 2 for Solar Auxilia, Militia and Knights). Daemons get 1 Followers of Chaos and 1 Greater Daemon Horde per Daemonic Horde.
- Allies + Lords of War share a points allowance, as a percentage of total roster points: 1/3 for most lists, 1/2 for Custodes, and none for Titanicus.
- One Supreme Commander per roster, and none in an Allied Contingent. One Spacecraft per roster.
- Formation limits such as "0-1" and "0-1 per full 2000 pts". These count the roster's current points total.
- Per-formation upgrade caps (four for Legion, Mechanicum and Militia; three for Solar Auxilia; uncapped elsewhere), each upgrade once, and OR-groups such as one transport option.
- Army-wide caps on upgrades: one Legate, one Captain-General, one Archmagos Prime, one Seneschal. Free Legate Commanders and Discipline Masters are limited to one per 500 points or part thereof.
- Titan weapon slots: Warhound 2, Warhound pack 4, Reaver 3, Warlord 4, with their costs.
- Standard Transport (Legion lists) requires exactly enough transports: one per 2 Tactical-sized units in the formation, rounded up. That counts squads added by upgrades such as Support Squads, and a Primarch, who takes his retinue's space. Characters, Dreadnoughts and Rapiers take no space. The transports can be any mix of Rhino Armoured Carriers and Damocles Command Rhinos, both 0 pts. Add Standard Transport last; if units change afterwards, BattleScribe flags the transport count until you fix it.

These rules are shown as text only, not enforced:

- Ally compatibility (cohesive or disruptive) and the -1 strategy penalty for a disruptive ally.
- "Enough transports to carry the formation" for every transport upgrade other than Standard Transport (Heavy Transport, Assault Claw, Drop Assault and so on).
- Daemon god-matching (Followers or Greater Daemons must share their Horde's god), the 3-9 minimum per Followers unit type, and one Daemon Prince per Chaos faction.
- Militia Provenance: only two types per army, and the Traitor Militia requirement.
- Mount restrictions on Titan weapons (arm or carapace).
- Swap upgrades such as Armoury Assets can't check that the unit being replaced is actually in the formation.

## Data decisions and gaps

- **Orks of Telon Reach is not included.** The Internet Archive never captured the army list page, only its unit reference sheet, so there are no formations to build from.
- **Sabre Strike Tank** is in the Legion list but missing from the wiki reference sheet. Its stats come from Departmento Munitorum.
- **Legio Custodes strategy rating:** the wiki says "1+", which looks like a typo for the initiative value. The data uses 5, matching Departmento Munitorum. The wiki also lists no Custodes allies.
- **Knight Household Allies/LoW allowance:** the wiki doesn't state one. The data uses 1/3, matching Departmento Munitorum.
- Where the wiki writes "X OR Y" units, they are modelled as an exclusive choice. "In any combination" or "of any configuration" lets you mix them.
- Some reference-sheet rows have weapon columns that don't line up, including Land Speeder, Tactical Support Squad and some Knights and Militia units. Those units get a single combined weapon profile with a note.
- **Rules text is summarised in my own words**, not copied. Use the wiki and the NetEA rulebook for full wording. Flavour text is omitted.

## Validation status

Every file validates against the BattleScribe v2.03 XSD. `tools/check.py` confirms that IDs are unique and that every link, condition and modifier target resolves. **The data has not been opened in the BattleScribe app.** The Allied Contingent points allowance relies on BattleScribe's `instanceOf` force condition, so check it in-app first.

## Regenerating

```bash
cd tools
python3 crawl.py <raw_dir>                        # fetch wiki pages from the Internet Archive
python3 parse_tables.py <raw_dir> <parsed_dir>    # wiki HTML -> JSON tables
python3 units.py <parsed_dir>                     # reference sheets -> units.json (move into source/)
python3 titan_weapons.py <parsed_dir>             # titan weapon variants -> source/titan_weapons.json
python3 generate.py ..                            # write .gst/.cat files
python3 check.py ..                               # integrity checks
```

The army lists are transcribed by hand in `spec_legion.py` and `spec_others.py`, using the small DSL in `dsl.py`. Edit those files and re-run `generate.py`. IDs are deterministic, so they stay stable across rebuilds.
