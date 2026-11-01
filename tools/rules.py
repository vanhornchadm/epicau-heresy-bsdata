"""Special rules referenced by the EpicAU Horus Heresy lists.

Descriptions are short paraphrased summaries of the mechanics; consult the
EpicAU wiki (archived) and the Net Epic Armageddon rulebook for full wording.
"""

# name -> summary. Names are matched case-insensitively against unit and
# weapon notes so units get links to the rules they use.
RULES = {
    # --- EpicAU supplement rules (Special Rules page) ---
    'Allies': "Formations from a Disruptive ally reduce the army's strategy rating by 1, and Supreme Commander re-rolls cannot be used on them. Allied formations follow their own list's restrictions (an allied Line Detachment is needed before an allied Support Detachment). Spacecraft and Supreme Commander limits apply across the whole army; only one Supreme Commander may be taken and it must come from the primary list.",
    'Armorbane': "Hits from this weapon's AT, CC or FF value reduce the target's save by 1 when allocated to LV, AV or WE units. No effect against INF.",
    'Armoured Spearhead': "The army may garrison one formation made up only of AV units per full 2000 points, ignoring the usual garrison restrictions. These formations may start on overwatch but count towards the normal limit of garrisoned formations on overwatch.",
    'Berserk': "The unit may double its move when taking an Engage action.",
    'Brutal': "When a formation containing Brutal units wins an assault, it counts one extra hit when working out hack-downs. This does not help decide who won the assault.",
    'Chain of Command': "The army may add one free Lieutenant Commander per full 1000 points to formations able to take the Praetor upgrade. Each counts towards that formation's upgrade limit and cannot join a formation with another Praetor upgrade; unused ones are lost.",
    'Demi-God': "Has three wounds and may be allocated hits up to its starting wounds. Must stay within 5cm of its formation unless it has Scout. Needs two Blast markers to be suppressed or broken, takes no Blast marker for losing a wound, suffers no critical hits and cannot barge. When destroyed, every friendly formation within 30cm takes two Blast markers. Counts as its retinue's unit type for transport.",
    'Exploratory Augury Web': "Friendly units arriving by Teleport within 15cm of this unit do not roll for Blast markers.",
    'Feedback': "If the weapon hits but causes no damage, roll a D6 for each successful save the target made; the firing unit takes a Blast marker for each 1.",
    'Ferocity': "The unit adds 5cm to its counter-charge move in an assault.",
    'Fleshbane': "Hits from this weapon's AP, CC or FF value reduce the target's save by 1 when allocated to INF or LV units. No effect against AV or WE.",
    'Lance': "AV units with Reinforced Armour may not re-roll saves against hits from this weapon. No effect against INF or LV.",
    'Legion Astartes': "Two Blast markers are needed to suppress a unit or kill one in a broken formation. The formation breaks at two Blast markers per unit, counts half its Blast markers (rounded down) in assault resolution, takes Blast markers equal to its units (not half) when it rallies, and Leaders remove 2 Blast markers instead of 1.",
    'Macro-Weapon': "Targets get no save unless they have Reinforced Armour or an Invulnerable Save, and even then cannot re-roll. Only applies to the unit type matching the to-hit value used.",
    'Remorseless': "A broken formation suffers only -1 (not -2) to its rally roll for being broken.",
    'Siege': "The weapon counts as a Macro-Weapon against units with 0cm speed.",
    'Singularity': "Each unmodified to-hit roll of 6 generates another attack dice; further 6s keep generating dice.",
    'Sniper': "Roll to hit separately for sniper attacks; hits may be allocated to any valid target the attacker chooses.",
    'Void Shields': "Each shield stops one point of damage before saves and Blast markers, then goes down. Close combat hits ignore shields; firefight hits must knock them down first. One downed shield is repaired each end phase, and a regroup roll can repair shields instead of removing Blast markers.",
    # --- list-specific rules ---
    "The Emperor's Chosen": "As Legion Astartes (two Blast markers to suppress or kill when broken, break at two Blast markers per unit, half Blast markers in assault resolution, full Blast markers on rallying, Leaders remove 2). In addition, Legio Custodes formations halve the hack-downs they suffer after losing an assault.",
    'Automaton': "The formation takes no Blast marker when this unit is destroyed (including crossfire and out-of-coherency losses). Disrupt hits still place Blast markers. Hits from Blast markers on a broken formation may be saved normally.",
    'Cortex Controller': "Formations with Cybernetica Cortex units operate normally if they have a unit within 15cm of a unit with this rule.",
    'Cybernetica Cortex': "Unless a friendly Cortex Controller is within 15cm, the formation suffers -1 initiative and may not March or Overwatch.",
    'Ion Gauntlet': "4+ save against normal, MW and TK shooting and firefight hits, and 5+ against normal, MW and TK close combat hits. Each point of TK damage is saved separately. Failed saves may still use Reinforced Armour where allowed. Not usable in a crossfire.",
    'Ion Shield': "4+ save against normal, MW and TK shooting and firefight hits. Each point of TK damage is saved separately. Failed saves may still use Reinforced Armour where allowed. Not usable in a crossfire.",
    'Instability': "A Daemonic Horde that fails an initiative test loses D3 Lesser Daemon (INF) units. These losses cause no Blast markers but can break the formation.",
    'Chaos Gate': "Up to three detachments may be kept in the Warp and enter play through the Gate, measuring their first move from its centre. Only one detachment may come through each turn.",
    'Daemonic Assault': "Before deployment, nominate one detachment per full 1000 points (or per 1000 points of allied allowance) to arrive by Teleport from turn two. Each may contain only one Greater Daemon.",
    'Provenance': "Applies to all INF units in the formation. Warrior Elite: +1 FF. Survivors of the Dark Age: +1 armour save. Feral Warriors: +1 CC. Traitors: Berserk. Only two Provenance types may be used across the army.",
    'Discipline Masters / Rogue Psykers': "One free Discipline Master (or Rogue Psyker) per 500 points or part thereof, added before set-up. The first must join the Force Commander's formation, or the most expensive Imperial Militia formation if there is no Force Commander.",
    'Legate Commander': "One free Legate Commander per 500 points or part thereof. If the army has a Lord Marshall, the first joins the Lord Marshall's formation. No more than one per formation, and none in Imperial Navy or allied formations; excess Legates are lost.",
    'Dedicated War Engine Transports': "Gorgon, Dracosan and Stormlord transports may only carry units from their own formation; the normal war engine transport rules do not apply.",
    'Drop Assault': "The formation is transported in Drop Pods (Planetfall) at no cost.",
    'Teleport': "Core Epic Armageddon rule: the unit may deploy by teleporting onto the battlefield, rolling for Blast markers on arrival.",
    'Knight Household': "Formations get +1 to action tests when taking an Engage action and +1 to rally tests.",
    # --- core Epic Armageddon abilities (brief reminders only) ---
    'Reinforced Armour': "Core rule: may re-roll a failed save, except against Macro-Weapons, Titan Killers or in a crossfire.",
    'Thick Rear Armour': "Core rule: crossfire does not reduce this unit's save.",
    'Invulnerable Save': "Core rule: gets a 6+ save (or the value listed) even when no save would normally be allowed.",
    'Walker': "Core rule: may re-roll failed dangerous terrain tests.",
    'Skimmer': "Core rule: may hover over terrain and pop up; can only be hit in assault by units able to engage skimmers.",
    'Scout': "Core rule: may deploy forward and has a wider zone of control and coherency spacing.",
    'Infiltrator': "Core rule: may double its move when taking an Engage action and ignores enemy zones of control when doing so.",
    'Jump Packs': "Core rule: may move over terrain and other units as if skimming.",
    'Mounted': "Core rule: counts as a vehicle for terrain purposes while remaining INF.",
    'Fearless': "Core rule: not destroyed by Blast markers when broken and not killed by hack-downs.",
    'Leader': "Core rule: removes an extra Blast marker when the formation rallies or marshals.",
    'Commander': "Core rule: may bring in up to three formations within 5cm when it takes an Engage action.",
    'Supreme Commander': "Core rule: as Commander, plus one re-roll per turn for a failed initiative test.",
    'Inspiring': "Core rule: each unit counts as an extra unit when working out assault resolution modifiers.",
    'Planetfall': "Core rule: may enter play from orbit using a planetfall move.",
    'Transport': "Core rule: carries the listed units.",
    'Indirect Fire': "Core rule: may fire at targets out of line of fire at reduced range and without sustained-fire bonuses.",
    'Ignore Cover': "Core rule: targets get no cover save modifiers.",
    'Disrupt': "Core rule: every hit places a Blast marker even if saved.",
    'Single Shot': "Core rule: may only be fired once per battle.",
    'Slow Firing': "Core rule: may only fire every other turn.",
    'Titan Killer': "Core rule: each hit causes the listed number of damage points to a war engine.",
    'Extra Attacks': "Core rule: grants the listed number of additional close combat or firefight attacks.",
}

# Short tokens used in weapon/unit notes that map onto the rules above.
ALIASES = {
    'MW': 'Macro-Weapon', 'TK': 'Titan Killer', 'EA': 'Extra Attacks',
    'Void Shield': 'Void Shields', 'Teleport special rule': 'Teleport',
}
