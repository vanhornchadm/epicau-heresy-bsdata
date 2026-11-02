# EpicAU Horus Heresy — BattleScribe data

BattleScribe (v2.03 schema) data for the EpicAU community's Horus Heresy supplement for Net Epic Armageddon, converted from the [archived EpicAU wiki](https://web.archive.org/web/20201111221247/http://epicau.com/mw/index.php/Main_Page). Where the wiki had gaps, [Departmento Munitorum](https://munitorum.com) was used, and each such case is listed below.

## Contents

| File | What it is |
|---|---|
| `Epic Armageddon - EpicAU Horus Heresy.gst` | Game system: costs, Unit, War Engine and Weapon profile types, categories, shared special rules |
| `EpicAU - Legion Astartes.cat` | The Legion list: the core formations plus all 18 Legions' formations, Primarchs, allies and restrictions, chosen with a Legion selection |
| `EpicAU - Legio Custodes / Solar Auxilia / Mechanicum Taghmata / Legio Titanicus / Knight Household / Imperial Militia / Daemons Of The Ruinstorm.cat` | The other army lists |
| `tools/` | The scraper, list specs and generator used to build the files |

To use it, copy the `.gst` and `.cat` files into a BattleScribe data folder, or zip them as a data index.

## Building a roster

Each catalogue provides two forces:

- **`<Army>`**: the primary army.
- **`<Army> (Allied Contingent)`**: add one of these from another catalogue for allies.

In either Legion Astartes force, the required **Legion** entry picks the Legion, or "None (core list)". The choice shows that Legion's own formations and hides the core formations it replaces or removes. Space Wolves also get their own Centurion upgrade. The description on each Legion option lists what it adds and replaces, plus its allies. If you change the Legion after adding formations, formations that no longer belong are flagged.

**Allow fan-made units** is a Configuration entry in the Legion Astartes and Legio Titanicus forces. It shows the fan-made units and options that aren't part of EpicAU: Legion formations (Kratos, Arquitor, Tarantula, Ascalon, Araknae, Saturnine Terminators and Saturnine Dreadnoughts), the Sicaran Punisher and Arcus, the Termite Assault and Palisade Drop Pod upgrades, and the Warbringer Nemesis, Warmaster, Dire Wolf, Warlord-Sinister and Warmaster Iconoclast Titans. They're marked with an asterisk (*) after their names, and stay hidden until it's taken. Taking it in any force turns them on for the whole roster. If you remove it, or change a Legion, anything that no longer fits is flagged under "Not available with the chosen Configuration".

These rules are enforced:

- Support Detachments: up to the list's number per Line Detachment (3 for Legion, Custodes and Mechanicum; 2 for Solar Auxilia, Militia and Knights). Daemons get 1 Followers of Chaos and 1 Greater Daemon Horde per Daemonic Horde.
- Allies + Lords of War share a points allowance, as a percentage of total roster points: 1/3 for most lists, 1/2 for Custodes, and none for Titanicus.
- One Supreme Commander per roster, and none in an Allied Contingent. One Spacecraft per roster.
- Formation limits such as "0-1" and "0-1 per full 2000 pts". These count the roster's current points total. When a roster is too small for what it contains, the entry's name gains the reason, for example "Warhound Titan (not enough points: 0-1 per full 4000 pts)". BattleScribe's error then names the limit. This labelling covers rosters up to 20,000 pts.
- Per-formation upgrade caps (four for Legion, Mechanicum and Militia; three for Solar Auxilia; uncapped elsewhere), each upgrade once, and OR-groups such as one transport option.
- Army-wide caps on upgrades: one Legate, one Captain-General, one Archmagos Prime, one Seneschal. Free Legate Commanders and Discipline Masters are limited to one per 500 points or part thereof.
- Titan weapon slots: Warhound 2, Warhound pack 4, Reaver 3, Warlord 4, with their costs.
- Standard Transport (Legion lists) requires exactly enough transports: one per 2 Tactical-sized units in the formation, rounded up. That counts squads added by upgrades such as Support Squads, and a Primarch, who takes his retinue's space. Characters, Dreadnoughts and Rapiers take no space. The transports are Rhino Armoured Carriers, and one of them per formation may be a Damocles Command Rhino instead. Both cost 0 pts. Add Standard Transport last; if units change afterwards, BattleScribe flags the transport count until you fix it.
- Every other transport upgrade also requires exactly enough transports for the formation. This covers Heavy Transport, Assault Claw and Assault Ram (Legion), Carrier (Custodes), Transport (Solar Auxilia, Mechanicum, Militia) and Heavy Transport (Militia). Units take transport space according to each transport's capacity on the reference sheets.
  - **Space per unit:** infantry take 1 space. Bulky units take 2: Terminators, Dreadnoughts, Ogryns, Thallax, Ursarax, Myrmidons and Aquilon Terminators. A Primarch takes his retinue's space, and characters and other vehicles take none.
  - **Capacity:** a Land Raider carries 2 spaces, a Spartan 4, and a Mastodon or Gorgon 8.
  - **Exceptions:** a Caestus carries any 2 units. A Kharybdis carries 4 Tactical-sized units, 2 Terminators or 1 Dreadnought.
  - **How it works:** the space is counted with hidden cost types, so it never shows in the roster. As with Standard Transport, add transports after the formation's other units, or adjust them afterwards. Drop Assault and Teleport need no count.
- Allies: an Allied Contingent must come from an army the primary army lists as an ally. For a Legion primary army, that means the chosen Legion's list. Otherwise its formations fall under "Not an allowed ally of the primary army", which the contingent allows none of. Formations from a disruptive ally get "(disruptive ally: -1 strategy rating)" added to their names. Legio Custodes lists no allies on the wiki, so it isn't restricted.
- Swap upgrades (Armoury Assets, Scythes of the Khan, Vanquisher, Executioner, Hyperios, Expanded Armoury, Enhanced Forge and the Daemon Prince upgrades) replace units one-for-one. Taking the upgrade reveals the upgraded units next to the units they replace, including units added by other upgrades such as Tank or Heavy Transport. Each upgraded unit takes an original's place and costs the original's price plus the swap cost. The upgrade's own limit (such as 1-2 units for Armoury Assets) is enforced, and only swaps for units the formation can contain are offered. A swap is left out where another upgrade already sells the upgraded unit: the Dreadnought upgrade offers Deredeos directly, so Armoury Assets doesn't swap its Contemptors.

These rules are shown as text only, not enforced:

- Ally qualifiers such as "Legion Astartes (Traitor Legions)" or "Daemons Of The Ruinstorm (Nurgle)": only the army is checked, not the Legion's allegiance or the Daemons' god. The strategy rating itself isn't changed; the disruptive label shows the penalty.
- Which units each transport may carry (for example, Rhinos can't carry Terminators): only the amount of space is checked.
- Daemon god-matching (Followers or Greater Daemons must share their Horde's god), the 3-9 minimum per Followers unit type, and one Daemon Prince per Chaos faction.
- Militia Provenance: only two types per army, and the Traitor Militia requirement.
- Mount restrictions on Titan weapons (arm or carapace).

## Data decisions and gaps

- **Profiles follow the layout of the [Epic Armageddon BSData](https://github.com/BSData/wh40k-epic-armageddon).** Each unit's weapons are in its own profile, one line per weapon, in Weapons, Range, Firepower and Weapon Notes columns. That way every unit's row in a roster lists its own guns. War engines use a War Engine profile with Damage Capacity, Void Shields and Critical Hit columns. Chosen Titan weapons stay separate Weapon profiles, listed under the Titan that carries them.
- **Orks of Telon Reach is not included.** The Internet Archive never captured the army list page, only its unit reference sheet, so there are no formations to build from.
- **Sabre Strike Tank** is in the Legion list but missing from the wiki reference sheet. Its stats come from Departmento Munitorum.
- **Solar Auxilia Tank Hunter Squadron** (3 Valdor Tank Hunters, 250 pts, support) comes from Departmento Munitorum. The Valdor is on the wiki reference sheet, but the archived army list has no formation for it.
- **Legion Kratos Heavy Tank Squadron** is fan-made, not part of EpicAU. It's a support detachment of 2 Kratos for 200 pts, plus up to 2 more at 100 pts each, taken from a [Dakka Dakka proposal](https://www.dakkadakka.com/dakkaforum/posts/list/812078.page) last edited in November 2024. The proposal gives no critical-hit effect or upgrades. The data uses "destroyed" for the critical hit, and Centurion and Hyperios for upgrades, as on the other Legion tank squadrons. Weapon choices (battlecannon or melta cannon, and heavy bolters or lascannons on the hull and sponsons) are shown on the unit profile rather than picked as options.
- **Sicaran Punisher and Sicaran Arcus** are fan-made, not part of EpicAU. Neither main weapon exists in any Epic source, so both use the Sicaran Battle Tank's hull and points (75 pts each in the Legion Sicaran Battle Squadron), with main guns derived from existing EpicAU weapons and checked against Legions Imperialis.
  - **Punisher Rotary Cannon:** 30cm, 3× AP3+/AT6+. This matches the Knight's Avenger Gatling Cannon against infantry, as in Legions Imperialis, and is one step weaker against armour.
  - **Arcus Missile Launcher:** 45cm, 2× AT4+/AA5+. It's built from the Whirlwind Scorpius launcher and the Hellstrike Missile Pod, and fires anti-tank or Skyspear anti-aircraft missiles.
- **Warbringer Nemesis Titan and Warmaster Titan** are fan-made, not part of EpicAU. Both are adapted from the [Epic-UK](http://epic-uk.co.uk/wp/army-lists/) Adeptus Titanicus codex (version 080925).
  - **What's kept:** the Epic-UK stat lines and fixed weapons.
  - **What's changed to fit EpicAU:** Cortex Controller, EpicAU's reactor critical-hit wording, and EpicAU's priced Titan weapon slots in place of Epic-UK's weapon tables.
  - **Warbringer (675 pts):** a Quake or Volcano Cannon on the carapace, plus 2 weapons.
  - **Warmaster (1050 pts):** 1 carapace weapon. It's a Lord of War with no limit, like the bigger Emperor-class Titans. Epic-UK's 0-1 Support slot doesn't exist in EpicAU, where Legio Titanicus has no Support Detachments, and Legions Imperialis puts no per-type limit on Titans.
  - **Points:** Epic-UK's prices include weapons (750 and 1500 pts). The Warbringer costs 50 pts more than a Reaver with Air Defence carrying the same weapons, the same gap as in Epic-UK. The Warmaster is priced between a fully armed Warlord and the 1350 pt Emperor-class Titans. Epic-UK's own Warmaster price is marked as unsettled, and this one is weaker than an Emperor (DC 10 and 7 shields against 12 and 8, no Inspiring, no transport).
  - **Upgrades:** both have built-in AA guns, so neither takes Air Defence.
- **Legion Arquitor Bombard Squadron** is a fan-made formation, not part of EpicAU. The Arquitor's stats are on the wiki reference sheet, but neither the wiki nor Departmento Munitorum gives it a formation. It's a support detachment of 4-6 Arquitors at 55 pts each, with Centurion and Hyperios upgrades like the Predator Strike Squadron. It's priced against the Predator (60 pts): similar firepower at shorter range, faster, with a 5+ save. Munitorum has an unused "2 for 250 pts" entry, which is far too expensive for a tank weaker than a Sicaran.
- **Legion Tarantula Battery** is fan-made, not part of EpicAU. It mirrors the Solar Auxilia Tarantula Battery: 4 Tarantulas and 1 Tarantula Hyperios for 125 pts, Immobile, with Teleport and Scout. The Tarantulas take the Mechanicum Tarantula's choice of twin lascannons or twin heavy bolters, as in Legions Imperialis.
- **Ascalon, Araknae, Saturnine Terminators, Saturnine Dreadnought, Termite and Palisade Drop Pod** are fan-made. No Epic source has them, so their Legions Imperialis rules are converted against existing EpicAU units, the same way as the Sicaran variants.
  - **Legion Ascalon Squadron:** a Lord of War of 1-3 Ascalons at 125 pts each, with no upgrades. Legions Imperialis lists it as Heavy Armour, like the Fellblade, Typhon and Cerberus, which EpicAU makes Lords of War. Each is a heavy flame tank built on the Spartan's war engine hull, with DC 3 and CC 5+ to match its extra wound and close-combat bonus in Legions Imperialis. It carries the Knight-Acheron's flame cannon (30cm, 2× AP3+/AT6+, Ignore Cover).
  - **Legion Araknae Weapons Battery:** 2-4 immobile platforms at 45 pts each. Each is a sturdier Tarantula (armour 5+, Invulnerable Save) carrying one gun:
    - quad accelerator autocannon, 45cm, 3× AP4+/AT5+
    - twin Punisher cannon, 30cm, 4× AP3+/AT6+/AA5+
    - Orias missiles, 45cm, 2 BP, Indirect Fire, single shot
  - **Legion Saturnine Terminator Detachment:** 4-6 units at 85 pts each. They're Terminators with an Invulnerable Save for their two wounds, but CC 4+. Each carries two of plasma bombards (30cm, AP4+/AT5+, Indirect Fire), twin heavy disintegrators (15cm, AP4+/AT4+, MW) or disruption fists.
  - **Legion Saturnine Dreadnought Talon:** 3-6 at 90 pts each. They're Deredeo-like walkers with an Invulnerable Save. Each carries a heavy plasma bombard (30cm, 2× AP4+/AT5+, Indirect Fire) or a graviton pulveriser (15cm, AP3+/AT4+, Disrupt), plus an inversion beamer (30cm, AP5+/AT4+).
  - **Termite Assault:** a transport option offered wherever Assault Claw is. Each Termite costs 30 pts and carries 2 Tactical-sized units or 1 Terminator. A formation carried entirely in Termites may arrive as if it had Teleport.
  - **Palisade Drop Pod:** a 25-pt upgrade for formations with Drop Assault. Once it lands, units within 15cm get a 6+ Invulnerable Save.
  - **Not added:** the Dreadnought Drop Pod and Deathstorm Drop Pod. EpicAU's Drop Pod already carries Dreadnoughts and has a Deathstorm Bombardment.
- **Dire Wolf, Warlord-Sinister and Warmaster Iconoclast Titans** are fan-made. No Epic source has them, so their Legions Imperialis rules are converted against the EpicAU Titan each is built on.
  - **Dire Wolf (Line, 300 pts plus its gun):** a Warhound chassis with Infiltrator and built-in Ardex mega-bolters (30cm, 4× AP4+/AT6+). It takes one of a Volcano Cannon (50 pts), a Neutron Laser* (60cm, MW3+, Disrupt; 25 pts) or a Conversion Beam Dissipator* (60cm, 3× MW3+; 50 pts). It costs about a sixth more than an armed Warhound, as in Legions Imperialis.
  - **Warlord-Sinister (Line, 950 pts):** a Psi-Titan on the Warlord chassis, for Loyalists only. Its psi weapons are fixed: Sinistramanus Tenebrae (75cm, 3× MW3+, TK(1)), Antipathic Tempest (45cm, 2 BP) and Death Pulse. Its Dread Aura gives enemy formations within 15cm -1 to rally. It costs about an eighth more than a fully armed Warlord, as in Legions Imperialis.
  - **Warmaster Iconoclast (Lord of War, 1100 pts):** a close-assault Warmaster at 20cm. It has a Desolator Chainsword and a Cruciator Gatling Array (45cm, 6× AP4+/AT5+), plus a Kirus Siege Drill* or Kirus Grav Imploder*. It costs the same as a Warmaster with a weapon, as in Legions Imperialis, and like the Warmaster it's a Lord of War with no limit.
- **Not included:** the Dominus Knight-Castellan and Knight-Valiant have stats on the wiki reference sheets, but neither the wiki nor Departmento Munitorum gives them a formation.
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
