# EpicAU Horus Heresy — BattleScribe data

BattleScribe (v2.03 schema) data for the EpicAU community's Horus Heresy supplement for Net Epic Armageddon, converted from the [archived EpicAU wiki](https://web.archive.org/web/20201111221247/http://epicau.com/mw/index.php/Main_Page). Where the wiki had gaps, [Departmento Munitorum](https://munitorum.com) was used, and each such case is listed below.

## Contents

| File | What it is |
|---|---|
| `Epic Armageddon - EpicAU Horus Heresy.gst` | Game system: costs, Unit/Weapon profile types, categories, shared special rules |
| `EpicAU - Legion Astartes.cat` | The Legion list: the core formations plus all 18 Legions' formations, Primarchs, allies and restrictions, chosen with a Legion selection |
| `EpicAU - Legio Custodes / Solar Auxilia / Mechanicum Taghmata / Legio Titanicus / Knight Household / Imperial Militia / Daemons Of The Ruinstorm.cat` | The other army lists |
| `tools/` | The scraper, list specs and generator used to build the files |

To use it, copy the `.gst` and `.cat` files into a BattleScribe data folder, or zip them as a data index.

## Building a roster

Each catalogue provides two forces:

- **`<Army>`**: the primary army.
- **`<Army> (Allied Contingent)`**: add one of these from another catalogue for allies.

In either Legion Astartes force, the required **Legion** entry picks the Legion, or "None (core list)". The choice shows that Legion's own formations and hides the core formations it replaces or removes. Space Wolves also get their own Centurion upgrade. The description on each Legion option lists what it adds and replaces, plus its allies. If you change the Legion after adding formations, formations that no longer belong are flagged.

These rules are enforced:

- Support Detachments: up to the list's number per Line Detachment (3 for Legion, Custodes and Mechanicum; 2 for Solar Auxilia, Militia and Knights). Daemons get 1 Followers of Chaos and 1 Greater Daemon Horde per Daemonic Horde.
- Allies + Lords of War share a points allowance, as a percentage of total roster points: 1/3 for most lists, 1/2 for Custodes, and none for Titanicus.
- One Supreme Commander per roster, and none in an Allied Contingent. One Spacecraft per roster.
- Formation limits such as "0-1" and "0-1 per full 2000 pts". These count the roster's current points total. When a roster is too small for what it contains, the entry's name gains the reason, for example "Warhound Titan (not enough points: 0-1 per full 4000 pts)". BattleScribe's error then names the limit. This labelling covers rosters up to 20,000 pts.
- Per-formation upgrade caps (four for Legion, Mechanicum and Militia; three for Solar Auxilia; uncapped elsewhere), each upgrade once, and OR-groups such as one transport option.
- Army-wide caps on upgrades: one Legate, one Captain-General, one Archmagos Prime, one Seneschal. Free Legate Commanders and Discipline Masters are limited to one per 500 points or part thereof.
- Titan weapon slots: Warhound 2, Warhound pack 4, Reaver 3, Warlord 4, with their costs.
- Standard Transport (Legion lists) requires exactly enough transports: one per 2 Tactical-sized units in the formation, rounded up. That counts squads added by upgrades such as Support Squads, and a Primarch, who takes his retinue's space. Characters, Dreadnoughts and Rapiers take no space. The transports are Rhino Armoured Carriers, and one of them per formation may be a Damocles Command Rhino instead. Both cost 0 pts. Add Standard Transport last; if units change afterwards, BattleScribe flags the transport count until you fix it.
- Swap upgrades (Armoury Assets, Scythes of the Khan, Vanquisher, Executioner, Hyperios, Expanded Armoury, Enhanced Forge and the Daemon Prince upgrades) replace units one-for-one. Taking the upgrade reveals the upgraded units next to the units they replace, including units added by other upgrades such as Tank or Heavy Transport. Each upgraded unit takes an original's place and costs the original's price plus the swap cost. The upgrade's own limit (such as 1-2 units for Armoury Assets) is enforced, and only swaps for units the formation can contain are offered. A swap is left out where another upgrade already sells the upgraded unit: the Dreadnought upgrade offers Deredeos directly, so Armoury Assets doesn't swap its Contemptors.

These rules are shown as text only, not enforced:

- Ally compatibility (cohesive or disruptive) and the -1 strategy penalty for a disruptive ally.
- "Enough transports to carry the formation" for every transport upgrade other than Standard Transport (Heavy Transport, Assault Claw, Drop Assault and so on).
- Daemon god-matching (Followers or Greater Daemons must share their Horde's god), the 3-9 minimum per Followers unit type, and one Daemon Prince per Chaos faction.
- Militia Provenance: only two types per army, and the Traitor Militia requirement.
- Mount restrictions on Titan weapons (arm or carapace).

## Data decisions and gaps

- **Orks of Telon Reach is not included.** The Internet Archive never captured the army list page, only its unit reference sheet, so there are no formations to build from.
- **Sabre Strike Tank** is in the Legion list but missing from the wiki reference sheet. Its stats come from Departmento Munitorum.
- **Solar Auxilia Tank Hunter Squadron** (3 Valdor Tank Hunters, 250 pts, support) comes from Departmento Munitorum. The Valdor is on the wiki reference sheet, but the archived army list has no formation for it.
- **Legion Kratos Heavy Tank Squadron** is fan-made, not part of EpicAU. It's a support detachment of 2 Kratos for 200 pts, plus up to 2 more at 100 pts each, taken from a [Dakka Dakka proposal](https://www.dakkadakka.com/dakkaforum/posts/list/812078.page) last edited in November 2024. The proposal gives no critical-hit effect or upgrades. The data uses "destroyed" for the critical hit, and Centurion and Hyperios for upgrades, as on the other Legion tank squadrons. Weapon choices (battlecannon or melta cannon, and heavy bolters or lascannons on the hull and sponsons) are shown on the unit profile rather than picked as options.
- **Warbringer Nemesis Titan and Warmaster Titan** are fan-made, not part of EpicAU. Both are adapted from the [Epic-UK](http://epic-uk.co.uk/wp/army-lists/) Adeptus Titanicus codex (version 080925).
  - **What's kept:** the Epic-UK stat lines and fixed weapons.
  - **What's changed to fit EpicAU:** Cortex Controller, EpicAU's reactor critical-hit wording, and EpicAU's priced Titan weapon slots in place of Epic-UK's weapon tables.
  - **Warbringer (650 pts):** a Quake or Volcano Cannon on the carapace, plus 2 weapons.
  - **Warmaster (0-1, 1050 pts):** 1 carapace weapon.
  - **Points:** Epic-UK's prices include weapons (750 and 1500 pts). The Warbringer's is scaled down by about the same ratio as EpicAU's Reaver and Warlord prices. The Warmaster is priced between a fully armed Warlord and the 1350 pt Emperor-class Titans. Epic-UK's own Warmaster price is marked as unsettled, and this one is weaker than an Emperor (DC 10 and 7 shields against 12 and 8, no Inspiring, no transport).
  - **Upgrades:** both have built-in AA guns, so neither takes Air Defence.
- **Not included:** the Arquitor Bombard (Legion) and the Dominus Knight-Castellan and Knight-Valiant have stats on the wiki reference sheets, but neither the wiki nor Departmento Munitorum gives them a formation.
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

Revisions are bumped automatically. `generate.py` compares each file with the copy already on disk and only rewrites files whose content changed; each rewrite raises that file's `revision` by one. A changed catalogue also records the current game system revision as `gameSystemRevision`. Running the generator twice in a row changes nothing. Always run it against the committed files rather than a fresh folder, otherwise every file starts again at revision 1.
