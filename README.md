# EpicAU Horus Heresy — BattleScribe data

BattleScribe (v2.03 schema) data for the EpicAU community's Horus Heresy supplement for Net Epic Armageddon, converted from the [archived EpicAU wiki](https://web.archive.org/web/20201111221247/http://epicau.com/mw/index.php/Main_Page). Where the wiki had gaps, [Departmento Munitorum](https://munitorum.com) was used, and each such case is listed below.

## Contents

| File | What it is |
|---|---|
| `Epic Armageddon - EpicAU Horus Heresy.gst` | Game system: costs, Unit, War Engine and Weapon profile types, categories, shared special rules |
| `EpicAU - Legion Astartes.cat` | The Legion list: the core formations plus all 18 Legions' formations, Primarchs, allies and restrictions, chosen with a Legion selection |
| `EpicAU - Legio Custodes / Solar Auxilia / Mechanicum Taghmata / Legio Titanicus / Knight Household / Imperial Militia / Daemons Of The Ruinstorm.cat` | The other army lists |
| `tools/` | The scraper, list specs and generator used to build the files |
| `site/` | The [Quartz](https://quartz.jzhao.xyz) site listing the new units, rules and changelog |

To use it, copy the `.gst` and `.cat` files into a BattleScribe data folder, or zip them as a data index.

## Building a roster

Each catalogue provides two forces:

- **`<Army>`**: the primary army.
- **`<Army> (Allied Contingent)`**: add one of these from another catalogue for allies.

In either Legion Astartes force, the required **Legion** entry picks the Legion, or "None (core list)". The choice shows that Legion's own formations and hides the core formations it replaces or removes. Space Wolves also get their own Centurion upgrade. The description on each Legion option lists what it adds and replaces, plus its allies. If you change the Legion after adding formations, formations that no longer belong are flagged.

In either Mechanicum Taghmata force, the required **Allegiance** entry picks Loyalist (the default) or Dark Mechanicum. Dark Mechanicum keeps the whole Taghmata list and adds the Dark Mechanicum formations, which are fan-made, so they also need "Allow fan-made units". Allies are the same for both allegiances.

**Allow fan-made units** is a Configuration entry in the Legion Astartes, Solar Auxilia, Mechanicum Taghmata, Legio Titanicus, Knight Household and Imperial Militia forces. It shows the fan-made units and options that aren't part of EpicAU: Legion formations (Kratos, Arquitor, Tarantula, Air Defence, Ascalon, Araknae, Saturnine Terminators and Saturnine Dreadnoughts), the Sicaran Punisher and Arcus, the Kratos as a Tank upgrade choice, the Termite Assault and Palisade Drop Pod upgrades, the Solar Auxilia aircraft, tanks, Aethon Heavy Sentinels and Cyclops, the Arlatax and Domitar Maniples, Krios Venator and Archmagos Prime on Abeyant, the Dark Mechanicum formations, the Acastus Knight Asterius and Knight Moirax, the Militia Flak Battery, and the Warbringer Nemesis, Warmaster, Dire Wolf, Warlord-Sinister and Warmaster Iconoclast Titans. They're marked with an asterisk (*) after their names, and stay hidden until it's taken. Taking it in any force turns them on for the whole roster. If you remove it, or change a Legion or allegiance, anything that no longer fits is flagged under "Not available with the chosen Configuration".

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
- Swap upgrades (Armoury Assets, Scythes of the Khan, Vanquisher, Executioner, Hyperios, Expanded Armoury, Enhanced Forge and the Daemon Prince upgrades) replace units one-for-one. Taking the upgrade reveals the upgraded units next to the units they replace, including units added by other upgrades such as Tank or Heavy Transport. Each upgraded unit takes an original's place and costs the original's price plus the swap cost. The upgrade's own limit (such as 1-2 units for Armoury Assets) is enforced, and only swaps for units the formation can contain are offered. A swap is left out where another upgrade already sells the upgraded unit: the Dreadnought upgrade offers Deredeos directly, so Armoury Assets doesn't swap its Contemptors.

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
  - The choices are listed in `tools/weapon_options.py`. Rules that every unit in a formation must choose the same weapon (Solar Auxilia Rapiers, Veletaris, Militia Auxiliary) are not enforced.
  - Titans work the same way, with one pick per weapon slot (for example Arm weapon 1, Carapace weapon 1). Each pick starts on the cheapest weapon. A chosen weapon's Notes give its arc, Fwd for arm weapons and FxF for carapace weapons, as the sheets give for each mount. Its mount restriction or other notes follow. Picks don't combine counts, so a Titan with two Inferno Guns lists "Inferno Gun" twice.
- **Orks of Telon Reach is not included.** The Internet Archive never captured the army list page, only its unit reference sheet, so there are no formations to build from.
- **Sabre Strike Tank** is in the Legion list but missing from the wiki reference sheet. Its stats come from Departmento Munitorum.
- **Solar Auxilia Tank Hunter Squadron** (3 Valdor Tank Hunters, 250 pts, support) comes from Departmento Munitorum. The Valdor is on the wiki reference sheet, but the archived army list has no formation for it.
- **Legion Kratos Heavy Tank Squadron** is fan-made, not part of EpicAU. It's a support detachment of 2 Kratos for 200 pts, plus up to 2 more at 100 pts each, taken from a [Dakka Dakka proposal](https://www.dakkadakka.com/dakkaforum/posts/list/812078.page) last edited in November 2024. The proposal gives no critical-hit effect or upgrades. The data uses "destroyed" for the critical hit, and Centurion and Hyperios for upgrades, as on the other Legion tank squadrons. Its weapon choices (battlecannon or melta cannon, and heavy bolters or lascannons on the hull and sponsons) are picked on each Kratos. The Legion Tank upgrade may also add 1-2 Kratos at 100 pts each, the squadron price, as it does for the Predator and Vindicator.
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
- **Legion Air Defence Battery** is fan-made, not part of EpicAU: a support detachment of 3 Whirlwind Hyperios for 225 pts, with a Centurion upgrade. It's the EpicAU Hyperios at the Hyperios upgrade's 75 pts each, so a Legion army can field flak without spreading single Hyperios upgrades across its formations.
- **Legion Tarantula Battery** is fan-made, not part of EpicAU. It mirrors the Solar Auxilia Tarantula Battery: 4 Tarantulas and 1 Tarantula Hyperios for 125 pts, Immobile, with Teleport and Scout. The Tarantulas take the Mechanicum Tarantula's choice of twin lascannons or twin heavy bolters, as in Legions Imperialis.
- **Ascalon, Araknae, Saturnine Terminators, Saturnine Dreadnought, Termite and Palisade Drop Pod** are fan-made. No Epic source has them, so their Legions Imperialis rules are converted against existing EpicAU units, the same way as the Sicaran variants.
  - **Legion Ascalon Squadron:** a Lord of War of 1-3 Ascalons at 125 pts each, with no upgrades. Legions Imperialis lists it as Heavy Armour, like the Fellblade, Typhon and Cerberus, which EpicAU makes Lords of War. Each is a heavy flame tank built on the Spartan's war engine hull, with DC 3 and CC 5+ to match its extra wound and close-combat bonus in Legions Imperialis. It carries the Knight-Acheron's flame cannon (30cm, 2× AP3+/AT6+, Ignore Cover).
  - **Legion Araknae Weapons Battery:** 2-4 immobile platforms at 45 pts each. Each is a sturdier Tarantula (armour 5+, Invulnerable Save) carrying one gun:
    - quad accelerator autocannon, 45cm, 3× AP4+/AT5+
    - twin Punisher cannon, 30cm, 4× AP3+/AT6+/AA5+
    - Orias missiles, 45cm, 2 BP, Indirect Fire, single shot
  - **Legion Saturnine Terminator Detachment:** 4-6 units at 85 pts each. They're Terminators with an Invulnerable Save for their two wounds, but CC 4+. Each carries two of plasma bombards (30cm, AP4+/AT5+, Indirect Fire), twin heavy disintegrators (15cm, AP4+/AT4+, MW) or disruption fists.
  - **Legion Saturnine Dreadnought Talon:** 3-6 at 90 pts each. They're Deredeo-like walkers with an Invulnerable Save. Each carries a heavy plasma bombard (30cm, 2× AP4+/AT5+, Indirect Fire) or a graviton pulveriser (15cm, AP3+/AT4+, Disrupt), plus an inversion beamer (30cm, AP5+/AT4+).
  - **Termite Assault:** a transport option offered wherever Assault Claw is. Each Termite costs 30 pts and carries 2 Tactical-sized units or 1 Terminator. A formation carried entirely in Termites may arrive using the Tunneler rule (NetEA rulebook 2.1.23, as on the Squat Termite) instead of Teleport.
  - **Palisade Drop Pod:** a 25-pt upgrade for formations with Drop Assault. Once it lands, units within 15cm get a 6+ Invulnerable Save.
  - **Not added:** the Dreadnought Drop Pod and Deathstorm Drop Pod. EpicAU's Drop Pod already carries Dreadnoughts and has a Deathstorm Bombardment.
- **Solar Auxilia aircraft** are fan-made, not part of EpicAU. The Thunderbolt, Marauder Bomber and Marauder Destroyer are taken unchanged from published Epic lists; the Colossus and Pathfinder are converted from Legions Imperialis.
  - **Thunderbolt Squadron:** 2 Thunderbolts for 150 pts, from the [NetEA](https://tp.net-armageddon.org) Imperial Guard lists.
  - **Marauder Squadron:** 2 Marauders for 250 pts. The Marauder Bomber comes from the NetEA Imperial Guard lists. Either bomber may instead be a Marauder Colossus or Marauder Pathfinder at the same price, as in Legions Imperialis. Both use the NetEA Marauder's hull and heavy bolters:
    - **Colossus:** a single-shot Colossus Bomb (15cm, 3 BP, MW) and Hellstrike missiles (30cm, AT4+, the Thunderbolt's rockets).
    - **Pathfinder:** two Hellstrike missiles and an Auger Array. Friendly Indirect Fire attacks on an enemy formation within 30cm of it get the Sustained Fire +1 to hit, standing in for Legions Imperialis's removal of the out-of-sight penalty.
  - **Marauder Destroyer Squadron:** 2 Destroyers for 275 pts, from the [Epic-UK](http://epic-uk.co.uk/wp/army-lists/) Imperial Guard codex (version 011026), armour 3+ as there.
- **Solar Auxilia tanks** are fan-made, offered next to the units they're variants of:
  - **Malcador Annihilator:** in the Malcador Squadron at no extra cost. It uses the EpicAU Imperial Militia sheet's weapons on the Solar Auxilia Malcador's hull, which adds Thick Rear Armour.
  - **Malcador Vanquisher:** in the Malcador Squadron at +25 pts each, the Leman Russ Vanquisher's price. It's the Solar Auxilia Malcador with the Vanquisher Cannon (75cm, AP4+/AT2+) in place of the battlecannon.
  - **Leman Russ Annihilator:** in the Strike Squadron at no extra cost, as Legions Imperialis prices it close to the battle tank. Its twin lascannon is AT3+ (45cm), a step better than EpicAU's twin lascannons for Legions Imperialis's Accurate trait, with a hull lascannon.
  - **Hellhammer:** a choice for the Super Heavy Tank and Super Heavy Tank Squadron at the Baneblade's price, as in Legions Imperialis. It's a Baneblade whose main gun is the Hellhammer Cannon (45cm, AP3+/AT3+, Ignore Cover): shorter-ranged than the Baneblade cannon, but it ignores cover.
- **Solar Auxilia Aethon Heavy Sentinel Patrol** is fan-made: a support detachment of 4 Aethons for 150 pts. Each is a Militia Sentinel with armour 5+, a multilaser (30cm, AP5+/AT6+) and a Sentinel missile launcher (45cm, AP5+/AT6+, the Legion missile launcher's profile). Its Forward Deployment becomes Scout.
- **Auxilia Flak Battery** is fan-made, not part of EpicAU: a support detachment of 3 Hydras for 150 pts, taken unchanged from the [NetEA](https://tp.net-armageddon.org) Imperial Guard lists. The Hydra is AV 30cm, armour 6+, with 2× twin Hydra autocannons (45cm, AP4+/AT5+/AA5+) and a heavy bolter. The NetEA price fits the Militia list, whose Sentinel Squadron also matches NetEA's (4 for 100 pts). It gives the Militia its only dedicated anti-aircraft.
- **Cyclops Battery** is a fan-made 25-pt upgrade for the Infantry Tercio and Veletaris Storm Cohort that adds 2 Cyclops Demolition Vehicles. Each picks a Demolition Charge (1 BP, MW) or Incineration Charge (1 BP, Ignore Cover), fired at 5cm. Its Remote Detonation means it may fire only within 30cm of a friendly Leader, Commander or Supreme Commander, and is destroyed once it has fired.
- **Dire Wolf, Warlord-Sinister and Warmaster Iconoclast Titans** are fan-made. No Epic source has them, so their Legions Imperialis rules are converted against the EpicAU Titan each is built on.
  - **Dire Wolf (Line, 300 pts plus its gun):** a Warhound chassis with Infiltrator and built-in Ardex mega-bolters (30cm, 4× AP4+/AT6+). It takes one of a Volcano Cannon (50 pts), a Neutron Laser* (60cm, MW3+, Disrupt; 25 pts) or a Conversion Beam Dissipator* (60cm, 3× MW3+; 50 pts). It costs about a sixth more than an armed Warhound, as in Legions Imperialis.
  - **Warlord-Sinister (Line, 950 pts):** a Psi-Titan on the Warlord chassis, for Loyalists only. Its psi weapons are fixed: Sinistramanus Tenebrae (75cm, 3× MW3+, TK(1)), Antipathic Tempest (45cm, 2 BP) and Death Pulse. Its Dread Aura gives enemy formations within 15cm -1 to rally. It costs about an eighth more than a fully armed Warlord, as in Legions Imperialis.
  - **Warmaster Iconoclast (Lord of War, 1100 pts):** a close-assault Warmaster at 20cm. It has a Desolator Chainsword and a Cruciator Gatling Array (45cm, 6× AP4+/AT5+), plus a Kirus Siege Drill* or Kirus Grav Imploder*. It costs the same as a Warmaster with a weapon, as in Legions Imperialis, and like the Warmaster it's a Lord of War with no limit.
- **Arlatax, Domitar, Krios Venator and Archmagos Prime on Abeyant** are fan-made. Their Legions Imperialis profiles come from the [BSData Legions Imperialis](https://github.com/BSData/Horus-Heresy-Legions-Imperialis) Mechanicum library and are converted against the EpicAU Castellax and Krios, the same way as the Dark Mechanicum units below. LI's Dread Aura becomes the Warlord-Sinister's: enemy formations within 15cm subtract 1 from their rally tests.
  - **Arlatax Maniple (line, 300 pts):** like the Castellax Maniple, 5 Arlatax and 2 Tech-Priests, with the same upgrades. The Arlatax is a jump-pack Castellax (20cm, CC 3+, Dread Aura) with power claws (assault weapons, EA(+1), MW) and an autocannon (45cm, AP5+/AT6+) or plasma cannon (30cm, AP4+/AT5+). It costs 25 pts more than the Castellax Maniple, as LI prices it a little higher.
  - **Domitar Maniple (line, 275 pts):** 5 Domitar and 2 Tech-Priests, at the Castellax Maniple's price. The Domitar is a Castellax walker with Dread Aura, a missile launcher (45cm, AP5+/AT5+, its frag and krak missiles in one profile) and graviton hammers (assault weapons, EA(+1), MW).
  - **Krios Venator:** in the Krios Battle Tank Squadron at no extra cost. It's the Krios with its Pulsar Fusil and volkite caliver sponsons (15cm, AP5+, Disrupt), which raise its FF to 4+.
  - **Archmagos Prime on Abeyant (125 pts):** a choice of the Magos upgrade. Instead of upgrading a Tech-Priest, it adds an AV unit (15cm, armour 4+, CC 4+) with the Archmagos Prime's rules, power weapons and a meltagun (15cm, MW5+). It's 25 pts more than an Archmagos Prime, for its own body. As a Supreme Commander it counts towards the one per army.
- **Dark Mechanicum** formations are fan-made. Their Legions Imperialis profiles come from the [BSData Legions Imperialis](https://github.com/BSData/Horus-Heresy-Legions-Imperialis) Dark Mechanicum catalogue, the data New Recruit uses, and are converted against the EpicAU Mechanicum automata (Castellax, Vorax, Krios). Legions Imperialis gives the Dark Mechanicum a list of its own, but it keeps the Taghmata's units, so here it's an allegiance of the Taghmata list rather than a separate catalogue.
  - **How the conversion maps:** LI's Noosphere Controller becomes Cortex Controller, and the Stalkers' Networked Anima becomes Cybernetica Cortex, as on the Taghmata's other automata. A single Construct Shield becomes an Invulnerable Save. LI moves of 7" and 8" become 20cm and 25cm, Nimble becomes Walker, and LI's Shieldbane is dropped, since every Epic shot can hit void shields.
  - **Points:** about 1.3 times the LI cost per model, the ratio between the LI and EpicAU prices of the Castellax, Vultarax and Krios.
  - **Errax Assault Stalker Cohort (line, 250 pts):** 5 Errax (25cm, armour 4+, CC 3+, Invulnerable Save), each with Errax lascutters (assault weapons, MW) or an Errax meltagun (15cm, MW5+), plus Stalker maxima bolters (15cm, AP4+). It may add 1-4 more at 50 pts each.
  - **Tenebrax Battle Stalker Cohort (support, 200 pts):** 5 Tenebrax light vehicles with a storm laser flenser (45cm, AP4+/AT5+) and one of Stalker volkite culverins (30cm, AP4+, Disrupt), an exo-planar cannon (15cm, AP4+, Ignore Cover) or Stalker maxima bolters.
  - **Harpax Scout Host (support, 100 pts):** 6 Harpax infantry with Jump Packs and Scout, armed with exo-planar repeaters (15cm, AP5+, Ignore Cover) or Harpax lascutters (assault weapons, MW).
  - **Serperos Heavy Stalker Maniple (Lord of War, 125 pts each):** 2-4 Serperos. LI lists it as Heavy Armour, which EpicAU makes Lords of War, as for the Ascalon. Each is a DC2 war engine (20cm, armour 3+) whose single void shield, its two Construct Shields, is never repaired. It carries a storm laser array (30cm, 2× AP4+/AT5+) or an exo-planar bombard (30cm, 2× AP4+, Ignore Cover), and Serperos lascutters (assault weapons, EA(+1), MW) or an irradiation engine (15cm, MW4+, Ignore Cover).
  - **Scintillax (75 pts):** an upgrade for the Stalker formations. It adds 1 Scintillax (20cm, armour 4+, Invulnerable Save, Cortex Controller, Leader) with a lascutter (assault weapons, EA(+1), MW) and an exo-planar cannon or storm laser (30cm, AP5+/AT5+).
  - **Not converted:** the Harpax Controller Host, the formation rules such as Protocol - Surge, and LI's Dark Mechanicum formations such as the Sibilans Taghma.
- **Acastus Knight Asterius and Knight Moirax** are fan-made. Their Legions Imperialis profiles come from the [BSData Legions Imperialis](https://github.com/BSData/Horus-Heresy-Legions-Imperialis) Knights library and are converted against the EpicAU Acastus Knight Porphyrion and Armiger Knights, whose LI profiles they share. LI's Ionic Flare Shield becomes: its Ion Shield saves are 1 better against Barrage hits, to a maximum of 2+.
  - **Acastus Knight Asterius (Lord of War, 260 pts each):** 1-2 Asterius with the Noble upgrade, like the Porphyrion formation. It's the Porphyrion's war engine with 2 conversion beam cannons (75cm, MW3+, for LI's long-range band), a volkite culverin (45cm, AP4+, Disrupt) and the Karacnos's mortar battery (45cm, BP 1, Ignore Cover, Fleshbane). It costs 10 pts more than a Porphyrion, as in LI.
  - **Knight Moirax:** a choice of the Armiger Knights formation, 5 Moirax for 25 pts more (225 pts), as LI's Moirax banner costs about an eighth more than the Armiger banner. It's an Armiger light vehicle with a volkite veuglair (30cm, AP4+/AT6+, Disrupt) and Gyges siege claw (assault weapons, MW, EA(+1), TK(1), CC 4+), or Armiger lightning locks (30cm, 2× AP4+/AT5+, CC 5+). LI also lets the Mechanicum take it; here it's in the Knight Household only.
- **Not included:** the Dominus Knight-Castellan and Knight-Valiant have stats on the wiki reference sheets, but neither the wiki nor Departmento Munitorum gives them a formation.
- **Legio Custodes strategy rating:** the wiki says "1+", which looks like a typo for the initiative value. The data uses 5, matching Departmento Munitorum. The wiki also lists no Custodes allies.
- **Knight Household Allies/LoW allowance:** the wiki doesn't state one. The data uses 1/3, matching Departmento Munitorum.
- Where the wiki writes "X OR Y" units, they are modelled as an exclusive choice. "In any combination" or "of any configuration" lets you mix them.
- Some reference-sheet rows have weapon columns that don't line up, including Tactical Support Squad and some Knights and Militia units. Those units get a single combined weapon profile with a note. The Land Speeder's and Javelin's combined rows are split into their weapon choices.
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

## Site

`site/` builds a [Quartz](https://quartz.jzhao.xyz) site from the data files, published at <https://vanhornchadm.github.io/epicau-heresy-bsdata/>. It has a page for every fan-made or Departmento Munitorum formation, unit, upgrade and Titan weapon, the special rules they use, this README's roster rules and data decisions, the backlog in `TODO.md`, and a changelog built from the git history. Nothing in it is written by hand: `site/build_content.py` reads the `.gst` and `.cat` files, `README.md`, `TODO.md`, `MISSING_UNITS.md` and `git log`, so the site follows the data.

```bash
site/build.sh            # build into site/public
site/build.sh --serve    # preview at http://localhost:8080
```

`build.sh` fetches the Quartz release pinned in it into `site/.quartz` and copies `site/quartz.config.ts` and `site/quartz.layout.ts` over its own. It needs git, Node 22 or later and Python 3. The `Deploy site to GitHub Pages` workflow rebuilds and publishes the site on every push to `main`; set the repository's Pages source to GitHub Actions once to turn it on.
