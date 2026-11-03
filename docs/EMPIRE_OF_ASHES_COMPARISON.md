# Empire of Ashes compared with this data

Empire of Ashes is a fan ruleset for Epic Armageddon set in the Horus Heresy. It comes in two forms:

- **The rules PDF:** *Epic 30K AB: Empire of Ashes*, public v1.0, dated 25/04/02, 75 pages. It covers the same 25 armies as these catalogues: the 18 Legions, Solar Auxilia, Imperialis Militia, Knight Households, Legio Titanicus, Mechanicum Taghmata, Legio Custodes and Daemons of the Ruinstorm.
- **The web builder:** [empire-of-ashes.vercel.app](https://empire-of-ashes.vercel.app/), an army builder for the PDF. It was compared using the army data bundled into the site (`static/js/main.a92b7f01.js`). Its own list validation wasn't tested.

"Ours" means the EpicAU wiki data, then in `tools/spec_legion.py`, `tools/spec_others.py` and `tools/source/units.json` and now in `data/`. Compared on 2026-11-02 (site) and 2026-11-03 (PDF).

## Summary

- **A separate game built on EpicAU.** The PDF thanks the EpicAU project as "the genesis for this whole project". It keeps EpicAU's frame: strategy ratings and initiative, 3 Support per Line, 4 upgrades per formation, a 1/3 Lords of War and allies cap (1/2 for Custodes), and most stat lines and formation points. On top of that it adds Legion traits, extra units, a Primarch slot and its own points and formation sizes. Those changes are deliberate design, not errors.
- **The site mostly follows the PDF.** Apart from the Daemons, its lists, points and upgrades match the PDF, and so do its stat lines outside the Legion core.
- **The site also has its own errors.** It doesn't match the PDF in these places:
  - Four Legion traits are different.
  - Nine Legions' allies lists are overwritten with the Sons of Horus list.
  - Several Legion core stat lines are changed.
  - Characters and most Primarchs have the wrong type.
  - Some formation limits are dropped or added.
  - The Daemons list is rebuilt.
- **Most of the problems flagged earlier are the site's.** The broken Imperial Fists, Blood Angels and Salamanders traits aren't in the PDF, and neither are the 5+ Tactical Marines or the copied allies lists. The Ultramarines trait is the PDF's own.
- **Use.** Empire of Ashes is a different game from EpicAU, so nothing in this data should change to match it. Departmento Munitorum agrees with the wiki on every disputed value checked (see [Checked against Departmento Munitorum](#checked-against-departmento-munitorum)).

## Where the site differs from the PDF

### Legion traits

The site has the PDF's trait for 14 Legions. The other four are different, and they're the traits that use mechanics Epic Armageddon doesn't have:

| Legion | PDF | Site |
|---|---|---|
| Imperial Fists | Masters of Defense: infantry and walkers without Scout get +1 to cover saves | Disciplined Doctrine: re-roll 1s "in the Firefight phase"; counts as having a Champion |
| Blood Angels | Angel's Fury: infantry get +5cm on Engage and consolidation; +1 CC on Engage the turn they arrive by Planetfall | The Red Thirst: First Strike; auto-pass "Leadership tests" to charge |
| Salamanders | Won't Back Down: infantry are Remorseless; hackdowns are 1 lower for infantry formations; characters ignore Fleshbane | Promethean Cult: never lose FF or CC from suppression; re-roll one save per turn |
| Raven Guard | Shadow Clad: infantry-only formations are Brutal; Champions, Chaplains and Commanders get Sniper | Strike From the Shadows: +5cm on turn 1; deploy with "the Infiltrate rule" |

### Allies

Nine Legions use the Sons of Horus list in place of their own: Dark Angels, Emperor's Children, Iron Warriors, White Scars, Space Wolves, Imperial Fists, Blood Angels, Salamanders and Raven Guard. That list has Daemons, Militia, Titanicus, Mechanicum and Solar Auxilia as cohesive allies and Knights as disruptive. Copying it is why the site makes Daemons a cohesive ally of loyalists such as the Dark Angels. The other nine Legions and all the non-Legion armies match the PDF.

### Unit stats

| Unit | PDF | Site | Ours |
|---|---|---|---|
| Tactical Squad | 4+ / 4+ / 4+ | 5+ / 5+ / 4+ | as PDF |
| Assault Squad | 4+ / 3+ / 5+ | 5+ / 3+ / 5+ | as PDF |
| Despoiler Squad | 4+ / 3+ / 5+ | 5+ / 4+ / 5+ | as PDF |
| Breacher Squad | 3+ / 4+ / 4+, melta-cutters (Armourbane, Lance) | 4+ / 5+ / 4+, bolters | as PDF |
| Terminators | 4+ / 3+ / 3+, power fists and reaper autocannon | 4+ / 4+ / 4+, power fists and combi-bolters | as PDF |
| Predator | TL lascannon, Predator cannon or Flamestorm, plus sponsons | single lascannon AT5+ and 2 heavy bolters | as PDF |
| Sicaran | Accelerator or Punisher cannon, heavy bolter, lascannon or heavy bolter sponsons | no sponsons | 3 heavy bolters, FF 3+ |
| Vindicator | FF 4+ | FF 5+ | |
| Predator Executioner | 30cm | 25cm | |
| Rapier | INF, 10cm, 4+ / 5+ / 5+ | AV, 30cm, 5+ / 6+ / 6+ | |
| Land Raider Achilles | WE | AV | |
| Outriders | INF | LV | |
| Reaver Attack Squad | CC 3+, Banestrike bolter (Sniper), Infiltrator | adds talons (Fleshbane), Berserk, Ferocity, Fearless, Invulnerable save | CC 4+, Sniper, Infiltrator |
| Champion, Chaplain, Librarian | CH with no Armour, CC or FF | CH with 4+ / 3+ / 4+ | as PDF |
| Primarchs | all INF with Demi-God | 11 of 18 typed CH | INF |

The White Scars and Space Wolves units also differ in many single values (Kyzagan, Ebon and Golden Keshig, the Khan, Deathsworn, Varagyr, Fenrisian Wolves and Leman Russ). The site's Solar Auxilia, Militia, Knights, Titans, Mechanicum, Custodes and Daemons stat lines match the PDF.

### Lists and upgrades

- **Missing limits:** core Destroyers, Artillery and Air Defence (each 0-1 per 2000 in the PDF) and Veterans (0-1 per 3000) have no limit on the site.
- **Added limits:** Kyzagans (0-1 per 1000) and Space Wolves Deathsworn, Wolf Guard and Fenrisian Wolves (0-1 per 2000 each) have limits the PDF doesn't give. The site also marks Crimson Paladin, Mor Deythan and Darkwing limits "TBD in source", but the PDF gives them no limit.
- **Consul:** the PDF lets Champions become Lieutenant Commanders; the site leaves this out.
- **White Scars:** the PDF's Ebon Keshig are 300 for 4, +75 per extra Ebon Keshig; the site makes the +75 extras Golden Keshig. The PDF's Khan comes with 3 Jetbikes when mounted or 3 Terminators on foot; the site gives him 3 Ebon Keshig.
- **Solar Auxilia:** the Solar Auxilia Support upgrade is 75 in the PDF and 0 on the site.

### Daemons on the site

The site rebuilds the Daemons list instead of following the PDF:

| Item | PDF | Site |
|---|---|---|
| Hordes | 250 for 5 plus a Herald, extra daemons +25 or +50 each, 0-1 Greater Daemon | 250 for 5 plus a Herald, then Small Host +150 or Large Host +300 |
| Followers | 6-9 of mixed types | one daemon type, 6 for 150 or 300, +25 or +50 each up to 9 |
| Greater Daemons | Greater Daemon Horde, 1-3 of the same god | 200 each, up to 3, 0-1 per Line |
| Warp Rift, Daemonic Overlord, Soul Grinders | included | not included |

## Where Empire of Ashes differs from EpicAU

The values in this section are the PDF's, and the site agrees with them unless noted.

### Content that isn't in EpicAU

None of these appear in the wiki or in our data:

- **Legion traits** for all 18 Legions, marked as optional rules. See [Legion traits](#legion-traits).
- **Optional army traits:** Rally 'round the Flag (Solar Auxilia), Second Greatest Predator (Knights), Heart of Steel and Warhorn (Titanicus), Targeting Algorithm (Mechanicum), Hunters of the Throne (Custodes) and Purposeful (Daemons).
- **Legion core units and formations:** Inductii Squad, Veteran Squad, Scout Detachment, Air Defence Battery (Skyreaper or Whirlwind Hyperios) and the Plutona Assault Drill. Its Castraferrum Dreadnoughts and Talon are EpicAU's Dreadnought and Legion Dreadnought Talon under the Heresy name.
- **Legion units:** Deathwing Companions (Dark Angels), Sunkiller Squad (Emperor's Children), Fenrisian Wolf Pack (Space Wolves), Luperci Pack (Sons of Horus) and Chogorian Skyhunters (White Scars).
- **Other armies:** Carnodon Squadron (Solar Auxilia), Ark Mechanicus (Mechanicum), Equinox Interceptors, Erinyes Jetcycles and the Saggitarum Detachment (Custodes), the Mechanicum and Grand Questoris Lances (Knights), Hydra Flak, Salamander Scout and Destroyer Tank Hunter squadrons (Militia), and the Determined and Void Fighters Provenances.
- **Primarchs** have their own slot, with Legion elite units as the retinue, and count toward the Lords of War allowance. Ours are Lords of War with the wiki's retinues.

Some of its units overlap with our fan-made units; see [Our fan-made units in Empire of Ashes](#our-fan-made-units-in-empire-of-ashes). Three ideas from it are now fan-made options here: the Legion Air Defence Battery (3 Whirlwind Hyperios, 225), the Kratos as a Tank upgrade choice (100 each) and the Militia Flak Battery (3 NetEA Hydras, 150). The rest are listed in TODO.md.

### Legion traits

These are the PDF's traits, checked against the rules text in our `.gst`. The PDF never says what a "Character unit" is. Its Bodyguard rule treats one as a unit hits can be allocated to, so it probably means the unit a character has joined. Read that way, most of the character traits work.

**Problems in the PDF's own text:**

- **Ultramarines (Interlocking Tactics):** gives "orders" to "units". The PDF uses "order" loosely elsewhere (Berserk says "Engage order"), so it probably means actions and formations. Even so, it lets one action test activate two formations within 10cm, for any action, all game. That is far stronger than Retaining the Initiative (at -1) or the Commander rule (Engage only). Its rally bonus (a friend within 30cm) is nearly always on.
- **Emperor's Children (Exemplars of War):** "one additional re-roll" only means something when there's already a re-roll, such as from a Supreme Commander.
- **Iron Warriors (Brick by Brick):** the PDF's Siege gives Titan Killer against 0cm units, so on characters it only matters against fortifications.
- **Word Bearers (Fanatical Zeal):** "wounds" isn't an Epic Armageddon term, but the intent (an extra Blast marker on a broken formation) is clear.
- **Thousand Sons (Might and Magic):** "+1 to any invulnerable save" probably means 5+.

**Traits that work:** Dark Angels, White Scars, Space Wolves, Imperial Fists, Night Lords, Blood Angels, Iron Hands, World Eaters, Death Guard, Sons of Horus, Salamanders, Raven Guard and Alpha Legion use real Epic Armageddon or PDF mechanics, though their strength varies a lot.

### Legion core list

#### Upgrades

| Upgrade | Empire of Ashes | Ours |
|---|---|---|
| Standard Transport | Rhino 10, Damocles 15 | both 0 |
| Heavy Transport | Phobos 75, Proteus 65, Spartan 125, Termite 75, Mastodon 225 | Phobos 75, Proteus 75, Spartan 125, Mastodon 200 |
| Assault Claw | Kharybdis 75 or Caestus 50 | Kharybdis 75; Caestus is a separate Assault Ram upgrade at 50 |
| Termite | in Heavy Transport, 75 | fan-made Termite Assault, 30 each |
| Consul / Centurion | "Consul", 50: Champion, Librarian or Chaplain; Champions may become Lieutenant Commanders; one Commander +50 | "Centurion", 50 |
| Praetor (Lieutenant or Lord Commander) | Lieutenant Commander through Consul | 50 / 100 |
| Dreadnought | Castraferrum 50, Contemptor 60, Leviathan 100 (site adds Deredeo 100) | Dreadnought 50, Contemptor 60, Leviathan 100, Deredeo 100 |
| Tank | adds Kratos 150 | no Kratos |
| Hyperios | up to 2, 75 each | 1, 75 |
| Rapier | 60 each, up to 4 | 50 each, 1-4 |
| Armoury Assets | adds Sicaran → Omega or Venator +20 and Contemptor → Deredeo +40; Achilles +20 (Phobos only) | no Sicaran swaps; Achilles +25 (Phobos or Proteus) |

#### Formations

| Formation | Empire of Ashes | Ours |
|---|---|---|
| Tactical Detachment | 275 | 275 |
| Assault Detachment | 300 for 8, +25 each up to 10 | 300 for 8 |
| Breacher Detachment | 300 for 8, +25 each up to 10 | 300 for 8 |
| Terminator Detachment | 300 for 4, +75 each up to 6 | 75 each, 4-6 (same) |
| Breacher Squad (support) | 175 | 225 |
| Destroyer Squad | 0-1 per 2000 pts (site: no limit) | 0-1 per 4000 pts |
| Recon Squad | 150 | 150 |
| Outriders or Attack Bikes | 125 for 4, +25 up to 6 | 175 for 5 |
| Scimitar Jetbikes | 150 for 4, +30 up to 6 | 175 for 5 |
| Land Speeders | 175 for 4, +40 up to 6 | 200 for 5 |
| Javelins | 200 for 4, +50 up to 6 | 250 for 5 |
| Contemptor Talon | 240 for 4, +60 up to 6 | 60 each, 4-6 (same) |
| Leviathan Talon | 300 for 3 | 225 for 3 |
| Artillery Battery | 4 for 250-325, 0-1 per 2000 pts (site: no limit); Arquitor 300 | same prices and limit; Arquitor fan-made, 55 each |
| Kratos Squadron | 400 for 3 | fan-made, 100 each, 2-4 |
| Land Raider Squadron | Phobos 320 for 4 +75, Proteus 300 for 4 +65 | 80 each, 4-6 |
| Predator Squadron | 240 for 4, +60 up to 6 | 60 each, 4-6 (same) |
| Sabre Squadron | 185 for 4, +50 up to 6 | 275 for 4 |
| Sicaran Squadron | 300 for 4, +80 up to 6 | 75 each, 4-6 |
| Vindicator Squadron | 200 for 4, +50 up to 6 | 50 each, 4-6 (same) |
| Rapier Battery | 265 | 240 |
| Gunship (Fire Raptors) | 300 for 2, +150 up to 3 | 300 for 2 |
| Xiphon Interceptors | 250 for 2, +125 up to 3 | 250 for 2 |
| Super heavy tank | 250 for 1, +250 up to 3 | 250 for 1; 700 for 3 only in some Legions |

### Legions

| Legion | Differences (Empire of Ashes vs ours) |
|---|---|
| Dark Angels | Adds Deathwing Companions (340). Lion's retinue is 3 Deathwing Companions (ours: 3 Terminators). |
| Emperor's Children | Adds Sunkiller Squad (250). Palatine Blades 275, +65 each (ours 60 each). Fulgrim's retinue is 3 Phoenix Terminators (ours: 3 Terminators). |
| Iron Warriors | Medusa battery 325 (ours 300). Adds an Arquitor battery option (400). |
| White Scars | Chogorian Brotherhood is 300 for 8 Outriders or Attack Bikes, 1-4 of which may become Land Speeders or Golden Keshig (ours 275 for 4 bikes and 4 Jetbikes). Adds Chogorian Skyhunters (225). Separate Kyzagan squadron (275; ours mixes Kyzagans into the Javelin squadron). Ebon Keshig are Lords of War, 0-1 per 2000, 300 for 4 +75 each (ours 0-1, Golden Keshig by Scythes of the Khan at +50). The Khan has 3 Jetbikes when mounted or 3 Terminators on foot (ours: 3 Terminators). |
| Space Wolves | Adds Fenrisian Wolf Pack (275). |
| Imperial Fists | Templar Brethren 300 for 3-5, 0-1 per 2000 (ours 400 for 6 plus a Champion, 0-1 per 4000). Castellum 0-1 per 2000 (ours 0-2 per 4000). Dorn may take 3 Terminators (ours: 7 Tactical only). |
| Night Lords | Curze may take 5 Terror Squads or 7 Despoilers (ours: 7 Tactical). |
| Blood Angels | Dawnbreakers 0-1 per 1000 (ours no limit). Sanguinius's retinue is 3 Dawnbreakers (ours: 5 Assault Squads). |
| Iron Hands | Matches ours. |
| World Eaters | Angron's retinue is 3 Red Butchers (ours: 3 Terminators). |
| Ultramarines | Guilliman may take 3 Invictarus or 3 Terminators (ours: 7 Tactical). |
| Death Guard | Destroyers are Line (ours Support). Deathshroud 340 (ours 300). Mortarion 500 with 3 Deathshroud (ours 450 with 3 Terminators). |
| Thousand Sons | Khenetai 250 (ours 225). Sekhmet 350 (ours 340). |
| Sons of Horus | Adds Luperci Pack (300). Horus 500 with 3 Justaerin (ours 450 with 3 Terminators). |
| Word Bearers | Ashen Circle 340 for 6-8 (ours 350 for 8). Gal Vorbak 300 (ours 250). |
| Salamanders | Matches ours. |
| Raven Guard | Scout Detachment is Line. |
| Alpha Legion | Adds a Scout Detachment as Line. Alpharius may take 3 Terminators (ours: 7 Tactical). |

### Allies

These are the PDF's lists. Six of the 18 match ours.

| Legion | Empire of Ashes cohesive / disruptive | Ours cohesive / disruptive |
|---|---|---|
| Dark Angels | Custodes, Titanicus, Mechanicum, Solar Auxilia / Militia, Knights | Titanicus, Solar Auxilia, Custodes / Militia, Knights, Mechanicum |
| Emperor's Children | Daemons (Slaanesh), Knights / Militia, Mechanicum, Titanicus, Solar Auxilia | Titanicus, Daemons (Slaanesh) / Militia, Solar Auxilia, Knights, Mechanicum |
| Iron Warriors | matches ours | Titanicus, Mechanicum / Daemons, Militia, Solar Auxilia, Knights |
| White Scars | Titanicus, Solar Auxilia / Militia, Knights, Mechanicum, Custodes | Titanicus, Solar Auxilia, Mechanicum, Knights, Custodes / Militia |
| Space Wolves | matches ours | Titanicus, Custodes / Militia, Solar Auxilia, Mechanicum, Knights |
| Imperial Fists | Militia, Custodes, Titanicus, Mechanicum, Solar Auxilia / Knights | Militia, Solar Auxilia, Knights, Mechanicum, Titanicus, Custodes / none |
| Night Lords | Mechanicum, Titanicus / Militia, Knights, Solar Auxilia | Titanicus / Daemons, Militia, Solar Auxilia, Knights, Mechanicum |
| Blood Angels | matches ours | Mechanicum, Titanicus, Custodes / Militia, Solar Auxilia, Knights |
| Iron Hands | matches ours | Titanicus, Mechanicum, Knights, Custodes / Militia, Solar Auxilia |
| World Eaters | matches ours | Titanicus, Daemons (Khorne) / Militia, Solar Auxilia, Knights, Mechanicum |
| Ultramarines | adds Daemons (traitors only) as disruptive | Militia, Solar Auxilia, Knights, Mechanicum, Titanicus, Custodes / none |
| Death Guard | matches ours | Titanicus, Daemons (Nurgle) / Mechanicum, Militia, Solar Auxilia, Knights |
| Thousand Sons | Daemons (Tzeentch), Titanicus, Solar Auxilia / Militia, Knights, Mechanicum | Titanicus, Daemons (Tzeentch) / Militia, Solar Auxilia, Mechanicum, Knights |
| Sons of Horus | Daemons, Militia, Titanicus, Mechanicum, Solar Auxilia / Knights | Titanicus, Militia, Solar Auxilia / Daemons, Mechanicum, Knights |
| Word Bearers | Daemons, Militia, Titanicus, Solar Auxilia / Knights, Mechanicum | Daemons, Militia (Traitor) / Titanicus, Mechanicum, Knights, Solar Auxilia |
| Salamanders | Militia, Mechanicum, Knights, Custodes, Titanicus, Solar Auxilia / none | Solar Auxilia, Titanicus, Custodes / Militia, Knights, Mechanicum |
| Raven Guard | Mechanicum, Custodes / Militia, Knights, Titanicus, Solar Auxilia | Custodes / Militia, Solar Auxilia, Knights, Mechanicum, Titanicus |
| Alpha Legion | Militia, Knights, Titanicus, Solar Auxilia / Daemons, Mechanicum | Titanicus, Militia, Solar Auxilia, Mechanicum, Knights / Daemons |

Outside the Legions, Empire of Ashes gives Custodes allies (cohesive Knights and Titanicus; disruptive Militia, Mechanicum and Solar Auxilia), where the wiki lists none. Its Titanicus list adds Custodes (Loyalist only) as a disruptive ally.

### Other armies

#### Solar Auxilia

| Item | Empire of Ashes | Ours |
|---|---|---|
| Strike Squadron | 200 for 4, +50 up to 6 | 350 for 6 (same per tank) |
| Tarantula Battery | 100 for 5 | 125 for 4 plus 1 Hyperios |
| Malcador Squadron | 300 for 4, +50 up to 6 | 350 for 5 |
| Tank Hunter Squadron | 200 | 250 (from Departmento Munitorum) |
| Sentinel Squadron | 125 for 4 Aethon or Hermes | fan-made Aethon Patrol, 150 for 4 |
| Super Heavy Tank Squadron | Lords of War, 500 | Support, 500 |
| Avenger Flight | 225, +125 up to 3 | 250 for 2 |
| Orbital Support | Lords of War, 150 | Support, 150 or 300 |
| Rapier Battery upgrade | 125 | 100 |
| Solar Auxilia Support upgrade | 75 (site: 0 per unit) | 75 |
| Transport | adds Aurox 10 and Termite 75 | Dracosan 75, Stormlord 200, Arvus 25 |
| Carnodon Squadron | 250 for 5, +50 up to 8 | not included |

#### Imperialis Militia

| Item | Empire of Ashes | Ours |
|---|---|---|
| Infantry Platoon | 125, +15 each up to 11 | 125 |
| Battle Tank Squadron | 300 for 4, +50 up to 6 | 350 for 5 |
| Heavy Tank (Malcador) Squadron | 300 for 4, +50 up to 6 | 350 for 5 |
| Field guns | Earthshaker or Medusa, 200, 0-1 per 1000 | Basilisk or Medusa carriages, 200, no limit |
| Rapier Battery | 125 | 100 |
| Gorgon (Heavy Transport) | 100 | 125 |
| Transport | adds Aurox 10 and Land Raider Proteus 50 | Arvus Lighter and others |
| Provenances | 6 types, including Determined and Void Fighters | 4 types |
| Hydra Flak, Salamander Scout, Destroyer Tank Hunter squadrons | included | not included |

#### Mechanicum Taghmata

| Item | Empire of Ashes | Ours |
|---|---|---|
| Castellax Maniple | 250 for 4 plus 2 Tech-Priests, +40 up to 6 | 275 for 5 plus 2 Tech-Priests |
| Arlatax Maniple | Support, 250 for 4, +60 up to 6 | fan-made Line, 300 for 5 plus 2 Tech-Priests |
| Domitar Maniple | Support, 225 for 4, +50 up to 6 | fan-made Line, 275 for 5 plus 2 Tech-Priests |
| Krios Squadron | 250 for 4, +50 up to 6 | 300 |
| Avenger Flight | 225 | 250 |
| Hyperios upgrade | adds a platform for 40 | swaps a Tarantula for +50 |
| Transport | adds Mechanicum Land Raider 75 | Triaros 75 |
| Ark Mechanicus | Lords of War, 250, 1 per army | not included |
| Dark Mechanicum | not included | fan-made allegiance |

#### Legio Titanicus

| Item | Empire of Ashes | Ours |
|---|---|---|
| Support Detachments | 2 per Line | none (the wiki gives none) |
| Lords of War and allies cap | 1/3 | none |
| Single Warhound | Support, 275, 0-1 per 2000 | Line, 275, 0-1 per 4000 |
| Dire Wolf | Support, 325, 0-1 per 2000 | fan-made Line, 300 plus its gun |
| Warbringer | Support, 700 | fan-made Line, 675 |
| Warmaster | 1175 | fan-made, 1050 |
| Psi-Titan (Warlord-Sinister) | 875 | fan-made, 950 |
| Emperor Titan | 0-1 per 7500 | no limit |
| Warhound weapons | adds Swarmer Missiles, Ursus Claw and Melta Lance | Inferno Gun, Vulcan Mega-Bolter, Plasma Blastgun, Turbo-Laser Destructor |

#### Knight Household

| Item | Empire of Ashes | Ours |
|---|---|---|
| Dominus Lance | 3 Castellans, 425 | fan-made Dominus Knights from it, 3 Castellans or Valiants, 425 |
| Mechanicum Lance | 325 for 3 Mechanicum House Knights | not included |
| Grand Questoris Lance | 375, +125 up to 4 | not included |
| Martian Support upgrade | adds Mechanicum Knights or Moirax | not included |
| Seneschal | 50 | 75 |
| Armiger Lance | Moirax in the base choice | fan-made Moirax option at 225 |

#### Legio Custodes

| Item | Empire of Ashes | Ours |
|---|---|---|
| Strategy Rating | 6 | 5 (Departmento Munitorum) |
| Main Line formation | Custodian Detachment, 350 (Custodian or Sentinel) | Hykanatoi, 350 (adds Sagittarum) |
| Agamatus Jetbikes | Line, 250 for 5 | Kataphraktoi, Line, 300 for 6 |
| Sisters of Silence | Line, 200 for 4, +50 up to 6 | Support, 250 for 4 |
| Morotoi Dreadnoughts | 340, Achilles or Galatus | 350, adds Telemon |
| Ares Gunship | 275 for 1, +275 for a second | 275 for 2 |
| Officers | Shield Captain 50, Tribune 50 | Captain-General 100 (one per army), Tribune 25 |
| Teleport / Carrier | 0 / 85 | 50 / 75 |
| Extras | Saggitarum Detachment, Erinyes Jetcycles, Equinox Interceptors, Vault Access, Oblivion Knight, Kheron Acquisitor | not included |

#### Daemons of the Ruinstorm

The PDF's Daemons list is close to ours. The site's isn't (see [Daemons on the site](#daemons-on-the-site)).

| Item | Empire of Ashes | Ours |
|---|---|---|
| Hordes | 250 for 5 plus a Herald (Putrid Legion 6), 0-6 lesser daemons +25 each, 0-6 heavier daemons +50 each, 0-1 Greater Daemon +200 | 250 for 6 plus a Herald; extra Lesser Daemons 25 each, Daemons 50 each |
| Followers | 6-9 of mixed types, +25 or +50 each | 6-9 of mixed types at unit cost |
| Greater Daemon Horde | 1-3 of the same god, 200 +200 (Bloodthirster +300) | 1-3 at 200, one per Horde of the same god |
| Undivided formations | Furies, Spawn, Soul Grinders, Harpies | |
| Warp Rift, Daemonic Overlord | 75 / free | included |

## Our fan-made units in Empire of Ashes

Our fan-made units (shown with "Allow fan-made units") come from Legions Imperialis conversions, NetEA, Epic-UK and a Dakka Dakka proposal; see the README. Empire of Ashes has its own versions of 14 of them, built from different sources, and the two rarely agree on profiles or points. The EoA values below are from the PDF.

### Formations and points

| Unit | Empire of Ashes | Ours |
|---|---|---|
| Kratos | Kratos Heavy Squadron, support, 3 for 400 (133 each); Tank upgrade 1-2 at +150 each | support, 2-4 at 100 each |
| Arquitor | Artillery Battery, 4 for 300 (75 each), 0-1 per 2000; Iron Warriors 6 for 400 | support, 4-6 at 55 each |
| Termite Assault Drill | Heavy Transport option, +75 | Termite Assault upgrade, 30 each |
| Sicaran Punisher | Punisher cannon is an alternative main gun on any Sicaran, same cost | separate Sicaran variant, 75 |
| Aethon Heavy Sentinel | Sentinel Squadron, 4 Aethon or Hermes, 125 | Aethon Patrol, 4 for 150 |
| Malcador Annihilator | Militia Heavy Tank Squadron only | also a Solar Auxilia Malcador Squadron option, free |
| Marauder Bomber | Lords of War, 2 for 325 (Solar Auxilia and Militia) | Marauder Squadron, 2 for 250 (Solar Auxilia) |
| Arlatax | support, 250 for 4, +60 up to 6, no Tech-Priests | Line, 300 for 5 plus 2 Tech-Priests |
| Domitar | support, 225 for 4, +50 up to 6, no Tech-Priests | Line, 275 for 5 plus 2 Tech-Priests |
| Knight Moirax | Armiger Lance choice, 200 for 5; also 1-3 through Martian Support (+50) | Armiger Knights choice, +25 (225 for 5) |
| Warbringer Nemesis | support, 700 | Line, 675 |
| Warmaster | Lords of War, 1175 | Lords of War, 1050 |
| Dire Wolf | support, 325, 0-1 per 2000 | Line, 300 plus its carapace gun |
| Warlord-Sinister | Lords of War, 875, loyalists only | Line, 950, loyalists only |

### Profiles

| Unit | Empire of Ashes | Ours |
|---|---|---|
| Kratos | WE 25cm 4+ / 6+ / 5+, DC2; Kratos cannon 30cm AP4+/AT3+ Armourbane, autocannon, TL lascannon or TL heavy bolter, lascannon or heavy bolter sponsons | same type and stats; Kratos battlecannon 45cm 2× AP3+/AT3+ Armourbane or melta cannon 30cm 4× MW5+, hull and sponson heavy bolters or lascannons |
| Arquitor | AV 20cm; Spicula rockets 30cm D3 BP, Indirect, Slow Firing, or graviton chargecannon 30cm 2× AP4+/AT4+, Disrupt, Indirect | AV 35cm; Spicula 30cm D3× AP5+/AT5+, no indirect fire or graviton option |
| Termite | AV 10cm 5+ / 4+ / 5+; heavy melta cutter (assault, MW), TL volkite caliver; Self-Planetfall, Walker, arrives turn 2+ | AV 15cm 5+ / 6+ / 5+; TL bolters; Tunneler |
| Sicaran Punisher | Punisher cannon 30cm 2× AP3+/AT6+ plus small arms EA(+1); heavy bolter and sponsons | Punisher rotary cannon 30cm 3× AP3+/AT6+; 3 heavy bolters |
| Aethon | AV 15cm 5+ / 6+ / 5+; missile pods 45cm 2× AP5+, multilaser 45cm AP5+/AT6+; Walker | LV 20cm 5+ / 6+ / 5+; multilaser 30cm, missile launcher 45cm, both AP5+/AT6+; Scout, Walker |
| Marauder Bomber | WE, DC2, 5+; TL lascannon 30cm, turrets AA5+, bombs 3 BP | AC, 4+; twin lascannon 45cm, bombs 3 BP, twin heavy bolters AA5+ |
| Arlatax | AV 15cm 3+ / 4+ / 4+; lightning blades (Fleshbane), TL light autocannon and plasma cannon; Jump Packs, no Cybernetica Cortex | AV 20cm 3+ / 3+ / 5+; power claws (MW, EA+1), autocannon or plasma cannon; Jump Packs, Cybernetica Cortex, Dread Aura |
| Domitar | AV 15cm 3+ / 4+ / 5+; graviton hammer (MW, EA+1), Ignis missiles 45cm AP5+/AT6+/AA6+, Ignore Cover | same stats; graviton hammers, missile launcher 45cm AP5+/AT5+; Dread Aura |
| Knight Moirax | LV 30cm 5+ / 4+ / 4+; siege claw (Siege, EA+1) and volkite veuglaire 15cm 2× AP4+/AT6+ Disrupt, Ignore Cover | LV 30cm 5+ / 4+ or 5+ / 5+; volkite veuglaire 30cm and siege claw (MW, EA+1, TK1), or lightning locks 30cm 2× AP4+/AT5+; Scout |
| Warbringer Nemesis | 15cm 4+ / 4+ / 3+, DC7, 3 void shields; carapace quake cannon 90cm 3 BP MW Indirect, flak battery, 2 Titan weapons | 20cm 4+ / 3+ / 3+, DC6, 6 void shields; quake or volcano cannon, 2 Titan weapons, AA guns |
| Warmaster | 20cm 4+ / 3+ (2+) / 3+, DC9, 7 void shields; 2 heavy plasma destructors or 2 close combat weapons, 2 carapace Titan weapons, Revelator 2× 3 BP MW one shot | 15cm 4+ / 3+ / 3+, DC10, 7 void shields; 2 Suzerain plasma destructors, 1 carapace Titan weapon, 4 Revelators 1 BP each, AA guns |
| Dire Wolf | 25cm 5+ / 4+ / 4+, DC4, 2 void shields; Ardax megabolter 30cm 2× AP3+/AT5+, 1 Titan weapon; may deploy as a garrison | 30cm 5+ / 4+ / 4+, DC3, 2 void shields; Ardex megabolters 30cm 4× AP4+/AT6+, volcano cannon, neutron laser or conversion beam dissipator; Infiltrator |
| Warlord-Sinister | 15cm 4+ / 2+ / 3+, DC8, 6 void shields; Sinistramanus 90cm AP2+/AT2+ TK(2) Singularity, ignores void shields and invulnerable saves, plus 3 Titan weapons; Inspiring, Invulnerable Save | same stats, DC8, 6 void shields; Sinistramanus 75cm 3× MW3+ TK(1), Antipathic Tempest 2 BP, Death Pulse; Dread Aura |

### Not in Empire of Ashes

Ascalon, Araknae, Saturnine Terminators and Dreadnoughts, the Legion Tarantula Battery, Sicaran Arcus, Palisade Drop Pod, Thunderbolt, Marauder Colossus, Pathfinder and Destroyer, Malcador Vanquisher, Leman Russ Annihilator, Hellhammer, Cyclops, Krios Venator, Archmagos Prime on Abeyant, the Dark Mechanicum (Errax, Tenebrax, Harpax, Serperos, Scintillax), Acastus Knight Asterius and Warmaster Iconoclast.

## Checked against Departmento Munitorum

Before the PDF turned up, the disputed values were checked in [Departmento Munitorum](https://munitorum.com)'s EpicAU Horus Heresy data (its `index.js`, read on 2026-11-02), to test whether they came from a newer EpicAU revision. Munitorum agrees with the wiki and these catalogues every time:

| Item | Munitorum | Empire of Ashes |
|---|---|---|
| Rhino | 0 | 10 |
| Land Raider Proteus transport / Mastodon | 75 / 200 | 65 / 225 |
| Outriders / Jetbikes | 175 for 5 | 125 / 150 for 4 |
| Land Speeders / Javelins | 40 / 50 each, 5 per squadron | 175 / 200 for 4 |
| Breacher Squad (support) | 225 | 175 |
| Sabre Squadron | 275 for 4 | 185 for 4 |
| Leviathan Talon | 75 each | 300 for 3 |
| Rapier upgrade / battery | 50 / 40 each | 60 / 265 |
| Assault Detachment | 300 for 8 | 300 for 8, up to 10 |
| Destroyers / Artillery | 0-1 per 4000 / 0-1 per 2000 | 0-1 per 2000 each |
| Tactical Squad | 4+ / 4+ / 4+ | 4+ / 4+ / 4+ (site: 5+ / 5+ / 4+) |
| Terminators | 4+ / 3+ / 3+ | 4+ / 3+ / 3+ (site: 4+ / 4+ / 4+) |

None of Empire of Ashes' extra content is in Munitorum either. Munitorum defines Dominus Castellan and Valiant units, but no formation uses them and they have no weapons. The fan-made Dominus Knights take their formation and the Castellan's weapons from the PDF. The PDF accounts for the points differences: they're Empire of Ashes' own, not a newer EpicAU revision.

## Other notes

- The site was made with Emergent, an AI app builder (its page title and badge say so). That probably explains its errors against the PDF: they read plausibly but don't fit the rules.
- The site's home page says lists never leave the device, but it loads PostHog analytics and its session recorder.
- The PDF says its artwork is Stable Diffusion placeholders.
