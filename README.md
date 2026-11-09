# EpicAU Horus Heresy — BattleScribe data

BattleScribe (v2.03 schema) data for the EpicAU community's Horus Heresy supplement for Net Epic Armageddon, converted from the [archived EpicAU wiki](https://web.archive.org/web/20201111221247/http://epicau.com/mw/index.php/Main_Page). Where the wiki had gaps, [Departmento Munitorum](https://munitorum.com) was used, and each such case is listed below.

## Contents

| File | What it is |
|---|---|
| `Epic Armageddon - EpicAU Horus Heresy.gst` | Game system: costs, Unit, War Engine and Weapon profile types, categories, shared special rules |
| `EpicAU - Legion Astartes.cat` | The Legion list: the core formations plus all 18 Legions' formations, Primarchs, allies and restrictions, chosen with a Legion selection |
| `EpicAU - Legio Custodes / Solar Auxilia / Mechanicum Taghmata / Legio Titanicus / Knight Household / Imperial Militia / Daemons Of The Ruinstorm.cat` | The other army lists |
| `data/` | The source: every army list, formation, upgrade, unit, Titan weapon and rule as a Markdown file (see [`data/README.md`](data/README.md)) |
| `tools/` | The generator that builds the `.gst` and `.cat` files from `data/`, and the integrity checks |
| `site/` | The [Quartz](https://quartz.jzhao.xyz) site that publishes `data/` |

The `.gst` and `.cat` files are generated: edit `data/`, not them.

## Using the data

Add this data index in New Recruit or BattleScribe:

```
https://github.com/vanhornchadm/epicau-heresy-bsdata/releases/latest/download/epicau-heresy-bsdata.latest.bsi
```

It always points at the latest release, so the app picks up each update. You can also load the repository itself as a custom game system, or copy the `.gst` and `.cat` files into a BattleScribe data folder.

## Building a roster

Each catalogue provides two forces:

- **`<Army>`**: the primary army.
- **`<Army> (Allied Contingent)`**: add one of these from another catalogue for allies.

In either Legion Astartes force, the required **Legion** entry picks the Legion, or "None (core list)". The choice shows that Legion's own formations and hides the core formations it replaces or removes. Space Wolves also get their own Centurion upgrade. The description on each Legion option lists what it adds and replaces, plus its allies. If you change the Legion after adding formations, formations that no longer belong are flagged.

In either Mechanicum Taghmata force, the required **Allegiance** entry picks Loyalist (the default) or Dark Mechanicum. Dark Mechanicum keeps the whole Taghmata list and adds the Dark Mechanicum formations, which are fan-made, so they also need "Allow fan-made units". Allies are the same for both allegiances.

**Allow fan-made units** is a Configuration entry in the Legion Astartes, Solar Auxilia, Mechanicum Taghmata, Legio Titanicus, Knight Household and Imperial Militia forces. It shows the fan-made units and options that aren't part of EpicAU: Legion formations (Kratos, Arquitor, Tarantula, Air Defence, Ascalon, Araknae, Saturnine Terminators, Saturnine Dreadnoughts and Deredeo Dreadnoughts), the Sicaran Punisher and Arcus, the Kratos as a Tank upgrade choice, the Termite Assault and Palisade Drop Pod upgrades, the Solar Auxilia aircraft, tanks, Aethon Heavy Sentinels and Cyclops, the Arlatax and Domitar Maniples, Krios Venator and Archmagos Prime on Abeyant, the Dark Mechanicum formations, the Acastus Knight Asterius, Knight Moirax and Dominus Knights, the Militia Flak Battery, and the Warbringer Nemesis, Warmaster, Dire Wolf, Warlord-Sinister and Warmaster Iconoclast Titans. They're marked with an asterisk (*) after their names, and stay hidden until it's taken. Taking it in any force turns them on for the whole roster. If you remove it, or change a Legion or allegiance, anything that no longer fits is flagged under "Not available with the chosen Configuration".

These rules are enforced:

- Support Detachments: up to the list's number per Line Detachment (3 for Legion, Custodes and Mechanicum; 2 for Solar Auxilia, Militia and Knights). Daemons get 1 Followers of Chaos and 1 Greater Daemon Horde per Daemonic Horde.
- Allies + Lords of War share a points allowance, as a percentage of total roster points: 1/3 for most lists, 1/2 for Custodes, and none for Titanicus.
- One Supreme Commander per roster, and none in an Allied Contingent. One Spacecraft per roster.
- Formation limits such as "0-1" and "0-1 per full 2000 pts". These count the roster's current points total. When a roster is too small for what it contains, the entry's name gains the reason, for example "Warhound Titan (not enough points: 0-1 per full 4000 pts)". BattleScribe's error then names the limit. This labelling covers rosters up to 20,000 pts.
- Per-formation upgrade caps (four for Legion, Mechanicum and Militia; three for Solar Auxilia; uncapped elsewhere), each upgrade once, and OR-groups such as one transport option.
- Army-wide caps on upgrades: one Legate, one Captain-General, one Archmagos Prime, one Seneschal. Free Legate Commanders and Discipline Masters are limited to one per 500 points or part thereof.
- Titan weapon slots, picked on each Titan with their costs: Warhound 2 arm; Reaver 2 arm and 1 carapace; Warlord 2 arm and 2 carapace. Arm-only weapons (Close Combat Weapon) and carapace-only weapons (Carapace Landing Pad, Support Missile) are offered only in those slots.
- Standard Transport (Legion lists) requires exactly enough transports: one per 2 Tactical-sized units in the formation, rounded up. That counts squads added by upgrades such as Support Squads, and a Primarch, who takes his retinue's space. Characters, Dreadnoughts and Rapiers take no space. The transports are Rhino Armoured Carriers, and one of them per formation may be a Damocles Command Rhino instead. Both cost 0 pts. Add Standard Transport last; if units change afterwards, BattleScribe flags the transport count until you fix it.
- Every other transport upgrade also requires exactly enough transports for the formation. This covers Heavy Transport, Assault Claw and Assault Ram (Legion), Carrier (Custodes), Transport (Solar Auxilia, Mechanicum, Militia) and Heavy Transport (Militia). Units take transport space according to each transport's capacity on the reference sheets.
  - **Space per unit:** infantry take 1 space. Bulky units take 2: Terminators, Dreadnoughts, Ogryns, Thallax, Ursarax, Myrmidons and Aquilon Terminators. A Primarch takes his retinue's space, and characters and other vehicles take none.
  - **Capacity:** a Land Raider carries 2 spaces, a Spartan 4, and a Mastodon or Gorgon 8.
  - **Exceptions:** a Caestus carries any 2 units. A Kharybdis carries 4 Tactical-sized units, 2 Terminators or 1 Dreadnought.
  - **How it works:** the space is counted with hidden cost types, so it never shows in the roster. As with Standard Transport, add transports after the formation's other units, or adjust them afterwards. Drop Assault and Teleport need no count.
- Allies: an Allied Contingent must come from an army the primary army lists as an ally. For a Legion primary army, that means the chosen Legion's list. Otherwise its formations fall under "Not an allowed ally of the primary army", which the contingent allows none of. Formations from a disruptive ally get "(disruptive ally: -1 strategy rating)" added to their names. Legio Custodes lists no allies on the wiki, so it isn't restricted.
- Swap upgrades (Armoury Assets, Scythes of the Khan, Vanquisher, Executioner, Hyperios, Expanded Armoury, Enhanced Forge and the Daemon Prince upgrades) replace units one-for-one. The upgraded units are listed next to the units they replace, including units added by other upgrades such as Tank or Heavy Transport. Each upgraded unit takes an original's place and costs the original's price plus the swap cost. Free swaps (all but the Daemon Prince upgrades) have no toggle: their upgraded units are always listed, and picking any of them uses one of the formation's upgrade slots. A swap with its own cost, such as a Daemon Prince, is taken as an upgrade first, which reveals its upgraded units; it only appears while the formation holds a unit it can upgrade. The swap's maximum (such as 2 units for Armoury Assets) is enforced, but its minimum isn't. Only swaps for units the formation can contain are offered. A swap is left out where another upgrade already sells the upgraded unit: the Dreadnought upgrade offers Deredeos directly, so Armoury Assets doesn't swap its Contemptors.

These rules are shown as text only, not enforced:

- Ally qualifiers such as "Legion Astartes (Traitor Legions)" or "Daemons Of The Ruinstorm (Nurgle)": only the army is checked, not the Legion's allegiance or the Daemons' god. The strategy rating itself isn't changed; the disruptive label shows the penalty.
- Which units each transport may carry (for example, Rhinos can't carry Terminators): only the amount of space is checked.
- Daemon god-matching (Followers or Greater Daemons must share their Horde's god), the 3-9 minimum per Followers unit type, and one Daemon Prince per Chaos faction.
- Militia Provenance: only two types per army, and the Traitor Militia requirement.

## Data decisions and gaps

- **A unit's profile names its weapons, and each weapon has its own profile below it.** The Unit profile has Type, Speed, Armour, CC, FF and Weapons. War engines use a War Engine profile, which adds Damage Capacity, Void Shields and Critical Hit. The Weapons column lists the weapons by name with their counts, such as "Lascannons x2", with repeated weapons combined. Each weapon is a Weapon profile, with Range, Firepower and Notes.
- **A unit's special rules are in its Rules section, not a profile column.** Rules the sheet names (Walker, Cortex Controller and so on) link to the shared rule. The rest of the sheet's notes become the unit's own rules, named after the unit:
  - **Labelled text** keeps its label, for example "Transport (Strike Cruiser)", "Dread Aura (Warlord-Sinister Battle Titan*)" or "Slow and Steady (Battle Barge)".
  - **Weapon Options (<unit>)** holds the sheet's weapon-choice sentences, and **Transport Space (<unit>)** sentences such as "Counts as Tactical Marines for transport capacity purposes".
  - **Special Rules (<unit>)** holds rule values such as "Invulnerable Save (6+)" or "Ion Shield (5+)", and any other text.
  - **Critical Hit (<unit>)** holds a critical hit too long for the War Engine's Critical Hit column, which then says "See rules".
  - **Titan Movement** is one rule shared by all Titans, covering stepping over terrain.
- **Rules the sheets abbreviate are named by their abbreviation:** MW (Macro-Weapon), TK (Titan Killer), EA (Extra Attacks), BP (Barrage), and the fire arcs FxF, Fwd, LF and RF. That way New Recruit links the abbreviation in weapon profiles to its rule. Each description starts with the full name.
- **Profile cells are kept short.** New Recruit moves a column below the table when any of its cells is longer than 80 characters, or 52 in a profile with more than 5 columns. It counts the whole cell, line breaks included.
  - **Weapon cells too long for the table:** the cell goes into a "<weapon> notes" rule, and it says "See weapon notes" instead.
  - **Weapons column:** about 40 units with many or long-named weapons still go over 52 characters, so New Recruit shows that column below their table. These include Titans, super-heavy tanks, Knights and gunships.
  - `tools/check.py` reports any other cell over these limits.
- **Weapon choices are picked on the unit.** Where a reference sheet lists alternative weapons ("X OR Y"), the unit has a pick for each choice, which starts on the first option. The Weapons column lists the fixed weapons and only the chosen ones, in sheet order, with no "OR". Only the chosen weapons' Weapon profiles are shown.
  - Some units pick twice: the Contemptor and Leviathan Dreadnoughts' two arm weapons, and the Saturnine Terminators' two weapons. Each pick may take the same weapon. The Contemptor's Havoc Launcher is an optional +5 pts pick.
  - Where the sheet gives one FF per option (Predator sponsons, Dreadnought, Veletaris, Mechanicum Tarantula and Land Raider, Militia Auxiliary), the choice sets the unit's FF.
  - The choices are listed in each unit's "Weapon options" section in `data/`. Rules that every unit in a formation must choose the same weapon (Solar Auxilia Rapiers, Veletaris, Militia Auxiliary) are not enforced.
  - Titans work the same way, with one pick per weapon slot (for example Arm weapon 1, Carapace weapon 1). Each pick starts on the cheapest weapon. A chosen weapon's Notes give its arc, Fwd for arm weapons and FxF for carapace weapons, as the sheets give for each mount. Its mount restriction or other notes follow. Picks don't combine counts, so a Titan with two Inferno Guns lists "Inferno Gun" twice.
- **Orks of Telon Reach is not included.** The Internet Archive never captured the army list page, only its unit reference sheet, so there are no formations to build from.
- **Sabre Strike Tank** is in the Legion list but missing from the wiki reference sheet. Its stats come from Departmento Munitorum.
- **Solar Auxilia Tank Hunter Squadron** (3 Valdor Tank Hunters, 250 pts, support) comes from Departmento Munitorum. The Valdor is on the wiki reference sheet, but the archived army list has no formation for it.
- **Legion Kratos Heavy Tank Squadron** is fan-made, not part of EpicAU. It's a support detachment of 2 Kratos for 200 pts, plus up to 2 more at 100 pts each, taken from a [Dakka Dakka proposal](https://www.dakkadakka.com/dakkaforum/posts/list/812078.page) last edited in November 2024. The proposal gives no critical-hit effect or upgrades, so the critical hit is TODO and the squadron has no upgrades until they are written. Its weapon choices (battlecannon or melta cannon, and heavy bolters or lascannons on the hull and sponsons) are picked on each Kratos. The Legion Tank upgrade may also add 1-2 Kratos at 100 pts each, the squadron price, as it does for the Predator and Vindicator.
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
- **Legion Arquitor Bombard Squadron** is a fan-made TODO: 4-6 Arquitors at +0 pts each, with no upgrades. The Arquitor's stats are on the wiki reference sheet, but no source gives it a usable formation.
- **Legion Deredeo Dreadnought Talon** is a fan-made TODO: 3-6 Deredeos at +0 pts each, with no upgrades. EpicAU has the Deredeo only as an upgrade, and no source gives it a formation.
- **Legion Air Defence Battery** is a fan-made TODO: 3 EpicAU Whirlwind Hyperios for 0 pts, with no upgrades. The formation was adapted from Empire of Ashes.
- **Legion Tarantula Battery** is a fan-made TODO: 4 Tarantulas and 1 Tarantula Hyperios for 0 pts, with the Solar Auxilia Tarantulas' profiles and no weapon choice. No source gives the Legions this formation.
- **TODO entries converted from Legions Imperialis.** No Epic source has these, and their conversions from Legions Imperialis have been cleared out. Each keeps its name, unit type and place in the lists, with stats of "-", no weapons, weapon options, Titan weapon slots or upgrades, and 0 pts, until it is rewritten by hand. A TODO upgrade adds nothing. The Termite keeps its transport note and the Archmagos Prime on Abeyant its Supreme Commander role.
  - **Legion Astartes:** the Legion Ascalon Squadron, Legion Araknae Weapons Battery, Legion Saturnine Terminator Detachment, Legion Saturnine Dreadnought Talon, Termite Assault and Palisade Drop Pod.
  - **Solar Auxilia:** the Marauder Colossus and Marauder Pathfinder (choices in the Marauder Squadron), Leman Russ Annihilator, Hellhammer, Aethon Heavy Sentinel Patrol and Cyclops Battery.
  - **Legio Titanicus:** the Dire Wolf, Warlord-Sinister and Warmaster Iconoclast Titans, and the Neutron Laser, Conversion Beam Dissipator, Kirus Siege Drill and Kirus Grav Imploder.
  - **Mechanicum Taghmata:** the Arlatax and Domitar Maniples, Krios Venator, Archmagos Prime on Abeyant, and the Dark Mechanicum formations (Errax, Tenebrax, Harpax and Serperos, and the Errax and Scintillax upgrades). Dark Mechanicum stays an allegiance of the Taghmata list.
  - **Knight Household:** the Acastus Knight Asterius and Knight Moirax.
  - **Not added:** the Dreadnought Drop Pod and Deathstorm Drop Pod. EpicAU's Drop Pod already carries Dreadnoughts and has a Deathstorm Bombardment.
- **Solar Auxilia aircraft** are fan-made, not part of EpicAU. The Thunderbolt, Marauder Bomber and Marauder Destroyer are taken unchanged from published Epic lists; the Colossus and Pathfinder are TODO.
  - **Thunderbolt Squadron:** 2 Thunderbolts for 150 pts, from the [NetEA](https://tp.net-armageddon.org) Imperial Guard lists.
  - **Marauder Squadron:** 2 Marauder Bombers for 250 pts, from the NetEA Imperial Guard lists. The Colossus and Pathfinder choices are TODO.
  - **Marauder Destroyer Squadron:** 2 Destroyers for 275 pts, from the [Epic-UK](http://epic-uk.co.uk/wp/army-lists/) Imperial Guard codex (version 011026), armour 3+ as there.
- **Solar Auxilia tanks** are fan-made, offered next to the units they're variants of:
  - **Malcador Annihilator:** a TODO choice in the Malcador Squadron, with no stats or weapons. It put the EpicAU Imperial Militia sheet's weapons on the Solar Auxilia Malcador, a combination no source makes.
  - **Malcador Vanquisher:** a TODO choice in the Malcador Squadron at +0 pts. It keeps the Solar Auxilia Malcador's hull and secondary weapons, but has no main gun until one is written.
- **Auxilia Flak Battery** is a fan-made TODO: 3 Hydras for 0 pts, with no upgrades. The formation was adapted from Empire of Ashes, and the Hydra has no stats or weapons until they are rewritten.
- **Dominus Knights** are fan-made TODOs. The Dominus Knight-Castellan and Knight-Valiant keep their stat lines from the wiki reference sheet (WE, 15cm, armour 4+, CC 4+, FF 4+, DC2, Ion Shield), which gives them no weapons. Their formation, points and weapons were adapted from Empire of Ashes and have been cleared out: the Dominus Knights formation (3 Castellans or 3 Valiants) costs 0 pts with no upgrades, and the Knights have no weapons.
- **Legio Custodes strategy rating:** the wiki says "1+", which looks like a typo for the initiative value. The data uses 5, matching Departmento Munitorum. The wiki also lists no Custodes allies.
- **Knight Household Allies/LoW allowance:** the wiki doesn't state one. The data uses 1/3, matching Departmento Munitorum.
- Where the wiki writes "X OR Y" units, they are modelled as an exclusive choice. "In any combination" or "of any configuration" lets you mix them.
- Some reference-sheet rows have weapon columns that don't line up, including Tactical Support Squad and some Knights and Militia units. Those units get a single combined weapon profile with a note. The Land Speeder's and Javelin's combined rows are split into their weapon choices.
- **Rules text is summarised in my own words**, not copied. Use the wiki and the NetEA rulebook for full wording. Flavour text is omitted.

## Validation status

Every file validates against the BattleScribe v2.03 XSD. `tools/check.py` confirms that IDs are unique and that every link, condition and modifier target resolves. **The data has not been opened in the BattleScribe app.** The Allied Contingent points allowance relies on BattleScribe's `instanceOf` force condition, so check it in-app first.

## Editing the data

Each entry is a Markdown file in `data/`: a unit's stat line and weapons are tables, a formation's composition is a bullet list, and its slot, cost and upgrades are settings at the top. [`data/README.md`](data/README.md) describes the format. Edit or add a file, then rebuild:

```bash
cd tools
python3 generate.py ..    # build the .gst/.cat files from data/
python3 check.py ..       # integrity checks
```

The generator stops with the file and line of anything it can't read. IDs are built from names, so they stay stable across rebuilds; renaming a unit, formation or upgrade gives it a new ID, which saved rosters won't recognise.

The data started as a conversion of the archived wiki's reference sheets and army lists. The scraper and the Python specs it replaced are in the git history before `data/` was added.

Revisions are bumped automatically. `generate.py` compares each file with the copy already on disk and only rewrites files whose content changed; each rewrite raises that file's `revision` by one. A changed catalogue also records the current game system revision as `gameSystemRevision`. Running the generator twice in a row changes nothing. Always run it against the committed files rather than a fresh folder, otherwise every file starts again at revision 1.

### Automatic builds

The `Build data and site` workflow runs on every push to `main`:

1. It rebuilds the `.gst` and `.cat` files from `data/`, runs the checks and commits any change, so the files in the repository always match `data/`.
2. If the push changed the data files, it publishes a GitHub release with each file zipped (`.gstz`/`.catz`) and the `epicau-heresy-bsdata.latest.bsi` data index. `tools/release_assets.sh` builds them with BSData's `wham` tool, as BSData's own repositories do.
3. It rebuilds and deploys the site.

Pull requests only build and check the data. To publish a release without a data change, run the workflow by hand with "Publish a data release" ticked. The workflow pushes to `main` with the built-in token, so `main` must not require pull requests for the `github-actions` bot.

## Docs

`docs/` holds working notes kept alongside the data:

- [`TODO.md`](docs/TODO.md): fan-made candidates from Empire of Ashes to revisit.
- [`MISSING_UNITS.md`](docs/MISSING_UNITS.md): Legions Imperialis units still to port.
- [`EMPIRE_OF_ASHES_COMPARISON.md`](docs/EMPIRE_OF_ASHES_COMPARISON.md): how the Empire of Ashes PDF and web builder differ from this data, and the Departmento Munitorum cross-check.

## Site

`site/` publishes `data/` as a [Quartz](https://quartz.jzhao.xyz) site at <https://vanhornchadm.github.io/epicau-heresy-bsdata/>. Every army, Legion, formation, upgrade, unit, Titan weapon and special rule has a page, with fan-made entries marked. The site also has the sources, this README's roster rules and data decisions, the format guide, the backlog in `docs/TODO.md` and `docs/MISSING_UNITS.md`, and a changelog built from the git history. `site/build_content.py` writes the pages from `data/`, `README.md`, the docs and `git log`. It adds each page's settings, points its links at the right army's pages and adds its design notes from the README. It warns about any fan-made entry without a `## Sources` section.

```bash
site/build.sh            # build into site/public
site/build.sh --serve    # preview at http://localhost:8080
```

`build.sh` fetches the Quartz release pinned in it into `site/.quartz` and copies `site/quartz.config.ts` and `site/quartz.layout.ts` over its own. It needs git, Node 22 or later and Python 3. The `Build data and site` workflow rebuilds and publishes the site on every push to `main`; set the repository's Pages source to GitHub Actions once to turn it on.
