"""Non-Legion EpicAU Horus Heresy army lists."""
from dsl import U, Opt, Or, Mix, Swap, F, UP, ARMY

NAVY_SHEET = 'Solar Auxilia'  # Avenger / Primaris-Lightning profiles live on the Solar Auxilia sheet

# ---------------------------------------------------------------- Legio Custodes
CUSTODES = ARMY(
    'Legio Custodes', ['Legio Custodes'], 5, '1+', 3, None, 1 / 2,
    formations=[
        F('Hykanatoi Detachment', 'line', 350,
          [Or(Opt('Sentinel Guard', U(6, 'Sentinel Guard')), Opt('Custodian Guard', U(6, 'Custodian Guard')),
              Opt('Sagittarum Custodes', U(6, 'Sagittarum Custodes')))],
          'Captain-General OR Senior Officer, Teleport, Carrier'),
        F('Kataphraktoi Detachment', 'line', 300, [U(6, 'Custodes Agamatus')], 'Senior Officer'),
        F('Tharanatoi Detachment', 'support', 375, [U(4, 'Aquilon Terminator')],
          'Captain-General OR Senior Officer, Carrier OR Teleport'),
        F('Ephoroi Detachment', 'support', 325, [U(4, 'Ephoroi Custodes')], 'Carrier'),
        F('Venatari Detachment', 'support', 350, [U(4, 'Venatari Squad')]),
        F('Sisters Detachment', 'support', 250, [U(4, 'Sisters of Silence')], 'Teleport'),
        F('Morotoi Detachment', 'support', 350,
          [Mix(4, 4, ('Contemptor-Achilles Dreadnought', 0), ('Contemptor-Galatus Dreadnought', 0),
               ('Telemon Heavy Dreadnought', 0), label='Custodes Dreadnoughts')]),
        F('Pallas Grav-Attack Squadron', 'support', 250, [U(3, 'Pallas Grav-Attack Vehicle')]),
        F('Caladius Grav-Tank Squadron', 'support', 325, [U(3, 'Callidus Grav-Tank')]),
        F('Orion Assault Squadron', 'low', 0, [U((1, 2), 'Orion Assault Dropship', 300)]),
        F('Ares Strike Squadron', 'low', 275, [U(2, 'Ares Gunship')]),
    ],
    upgrades=[
        UP('Captain-General', 100, parts=[U(1, 'Captain-General')], maxn=1),
        UP('Senior Officer', 25, parts=[U(1, 'Tribune')]),
        UP('Teleport', 50, rules=['Teleport'], desc='Add the Teleport special rule to each unit in the formation.'),
        UP('Carrier', parts=[U((1, None), 'Coronus Grav-Carrier', 75)],
           desc='Add enough Coronus Grav-Carriers to transport the whole detachment.'),
    ],
    cohesive=[], disruptive=[],
    rules=["The Emperor's Chosen", 'Allies'],
    notes=['Each upgrade may only be taken once per detachment.',
           'Up to 1/2 of the army\'s points may be spent on Allies and/or Lords of War.',
           'The wiki gives the strategy rating as "1+", which appears to be a typo; Departmento Munitorum uses 5.',
           'The wiki does not list which armies are cohesive or disruptive allies for Legio Custodes.'])

# ---------------------------------------------------------------- Solar Auxilia
SA_TRANSPORT = Or(Opt('Dracosan Armoured Transport', U((1, None), 'Dracosan Armoured Transport', 75)),
                  Opt('Stormlord', U((1, None), 'Stormlord', 200)),
                  Opt('Arvus Lighter', U((1, None), 'Arvus Lighter Orbital Shuttle', 25)), label='Transport')
SA_SUPER_HEAVIES = ['Baneblade', 'Shadowsword', 'Stormsword', 'Stormblade', 'Stormhammer']
LEGATE = ['Legate Commander']
SOLAR_AUXILIA = ARMY(
    'Solar Auxilia', ['Solar Auxilia'], 3, '2+', 2, 3, 1 / 3,
    formations=[
        F('Solar Auxilia Command Retinue', 'line', 300, [U(1, 'Lord Marshall'), U(7, 'Veletaris Storm Section')],
          'Infantry Support Tank, Ogryn Charonite Squad, Solar Auxilia Support, Transport', maxn=1, extra_up=LEGATE),
        F('Solar Auxilia Strike Squadron', 'line', 350,
          [Mix(6, 6, ('Leman Russ Battle Tank', 0), ('Leman Russ Exterminator', 0))], 'Vanquisher', extra_up=LEGATE),
        F('Solar Auxilia Infantry Tercio', 'line', 150,
          [U(1, 'Solar Auxilia Command Section'), U(7, 'Solar Auxilia Infantry Section')],
          'Infantry Support Tank, Ogryn Charonite Squad, Rapier Battery, Solar Auxilia Support, Transport', extra_up=LEGATE),
        F('Solar Auxilia Veletaris Storm Cohort', 'line', 200,
          [U(1, 'Solar Auxilia Command Section'), U(7, 'Veletaris Storm Section')],
          'Infantry Support Tank, Ogryn Charonite Squad, Transport', extra_up=LEGATE),
        F('Solar Auxilia Orbital Support', 'support', 0,
          [Or(Opt('Emperor Class Battleship', U(1, 'Emperor Class Battleship'), cost=300),
              Opt('Dauntless Class Light Cruiser', U(1, 'Dauntless Class Light Cruiser'), cost=150))], maxn=1),
        F('Solar Auxilia Artillery Tank Battery', 'support', 250,
          [Or(Opt('Basilisks', U(3, 'Basilisk')), Opt('Bombards', U(3, 'Bombard')), Opt('Medusas', U(3, 'Medusa')))],
          extra_up=LEGATE),
        F('Solar Auxilia Malcador Squadron', 'support', 350,
          [Mix(5, 5, ('Malcador Heavy Tank', 0), ('Malcador Infernus Special Weapons Tank', 0))], extra_up=LEGATE),
        F('Solar Auxilia Super Heavy Tank', 'support', 200, [Or(*[Opt(t, U(1, t)) for t in SA_SUPER_HEAVIES])],
          extra_up=LEGATE),
        F('Solar Auxilia Super Heavy Tank Squadron', 'support', 500, [Or(*[Opt(t, U(3, t)) for t in SA_SUPER_HEAVIES])],
          extra_up=LEGATE),
        F('Solar Auxilia Close Support Squadron', 'support', 200,
          [Mix(3, 3, ('Leman Russ Demolisher', 0), ('Leman Russ Incinerator', 0))], 'Executioner', extra_up=LEGATE),
        F('Solar Auxilia Tank Hunter Squadron', 'support', 250,
          [U(3, 'Valdor Tank hunter', label='Valdor Tank Hunter')], extra_up=LEGATE,
          note='The Valdor is on the wiki reference sheet, but the archived army list has no formation for it; '
               'this formation is taken from Departmento Munitorum.'),
        F('Solar Auxilia Tarantula Battery', 'support', 125, [U(4, 'Tarantula'), U(1, 'Tarantula Hyperios')],
          extra_up=LEGATE),
        F('Solar Auxilia Avenger Wing', 'low', 250, [U(2, 'Imperial Navy Avenger Strike Fighter')]),
        F('Solar Auxilia Primaris-Lightning Wing', 'low', 225, [U(2, 'Imperial Navy Primaris-Lightning Strike Fighter')]),
    ],
    upgrades=[
        UP('Solar Auxilia Support', 75,
           parts=[Mix(4, 4, ('Solar Auxilia Close Support Section', 0), ('Veletaris Storm Section', 0))],
           desc='Add 4 Auxilia Flamer Section (Close Support Section) or Veletaris Storm units in any combination.'),
        UP('Executioner', parts=[Swap(1, 1, (('Leman Russ Demolisher', 'Leman Russ Incinerator'),
                                             'Leman Russ Executioner', 25))]),
        UP('Infantry Support Tank', parts=[Mix(1, 2, ('Leman Russ Demolisher', 50), ('Malcador Infernus Special Weapons Tank', 50))]),
        UP('Ogryn Charonite Squad', 75, parts=[U(2, 'Ogryn Charonite Squad')]),
        UP('Rapier Battery', 100, parts=[U(4, 'Solar Auxilia Rapier Platform')]),
        UP('Transport', parts=[SA_TRANSPORT], desc='Add enough transports to carry the entire detachment.'),
        UP('Vanquisher', parts=[Swap(1, 1, (('Leman Russ Battle Tank', 'Leman Russ Exterminator'),
                                            'Leman Russ Vanquisher', 25))]),
        UP('Legate Commander', 0, parts=[U(1, 'Legate Commander')], rules=['Legate Commander'], maxn=1, per=500,
           round_up=True),
    ],
    cohesive=['Legio Titanicus', 'Legion Astartes', 'Knight Household'],
    disruptive=['Mechanicum Taghmata', 'Daemons Of The Ruinstorm'],
    rules=['Allies', 'Legate Commander', 'Dedicated War Engine Transports'],
    notes=['Each detachment may purchase up to three upgrades, each only once.',
           'Up to 1/3 of the army\'s points may be spent on Allies or Lords of War.'])

# ---------------------------------------------------------------- Mechanicum Taghmata
MECH_TRANSPORT = Or(Opt('Triaros Armoured Conveyor', U((1, None), 'Triaros Armoured Conveyor', 75)),
                    Opt('Mechanicum Land Raider', U((1, None), 'Mechanicum Land Raider', 75)), label='Transport')
MECHANICUM = ARMY(
    'Mechanicum Taghmata', ['Mechanicum Taghmata', NAVY_SHEET], 3, '2+', 3, 4, 1 / 3,
    formations=[
        F('Adsecularis Covenant', 'line', 150, [U(10, 'Tech Thralls'), U(2, 'Tech Priests')],
          'Krios, Magos, Scyllax, Transport'),
        F('Thallax Cohort', 'line', 300, [U(6, 'Thallax')], 'Krios, Magos, Scyllax, Tech-Priest, Transport'),
        F('Ursarax Cohort', 'line', 250, [U(6, 'Ursarax')], 'Tech-Priest, Transport'),
        F('Vorax Maniple', 'line', 250, [U(6, 'Vorax Battle-Automata')], 'Tech-Priest'),
        F('Castellax Maniple', 'line', 275, [U(5, 'Castellax Battle-Automata'), U(2, 'Tech Priests')],
          'Magos, Scyllax, Thanatar'),
        F('Vultarax Maniple', 'support', 250, [U(6, 'Vultarax Stratos-Automata')]),
        F('Thanatar Maniple', 'support', 200, [U(3, 'Thanatar Battle-Automata')], 'Magos, Scyllax, Tech-Priest'),
        F('Krios Battle Tank Squadron', 'support', 300, [U(5, 'Krios Battle Tank')], 'Krios'),
        F('Karacnos Assault Squadron', 'support', 300, [U(4, 'Karacnos Assault Tank')]),
        F('Myrmidon Sect', 'support', 300,
          [Or(Opt('Myrmidon Secutors', U(6, 'Myrmidon Secutors')), Opt('Myrmidon Destructors', U(6, 'Myrmidon Destructors')))],
          'Krios, Magos, Scyllax, Transport'),
        F('Tarantula Battery', 'support', 125, [U(5, 'Tarantula Platform')], 'Hyperios'),
        F('Minotaur Artillery Battery', 'support', 350, [U(3, 'Minotaur Artillery Tank')]),
        F('Ordinatus Minorus Tormenta', 'support', 500, [U(3, 'Ordinatus Minoris')], maxn=1, per=2000),
        F('Imperial Navy Avenger Wing', 'low', 250, [U(2, 'Imperial Navy Avenger Strike Fighter')]),
        F('Imperial Navy Primaris-Lightning Wing', 'low', 225, [U(2, 'Imperial Navy Primaris-Lightning Strike Fighter')]),
        F('Super Heavy Tank Destroyer', 'low', 250, [U(1, 'Falchion')]),
        F('Ordinatus Majoris', 'low', 450, [U(1, 'Ordinatus Majoris')], maxn=1),
    ],
    upgrades=[
        UP('Magos', parts=[Or(Opt('Archmagos Prime', U(1, 'Archmagos Prime'), cost=100),
                              Opt('Magos Prime', U(1, 'Magos Prime'), cost=50), label='Magos')],
           desc='Upgrade 1 Tech-Priest or Myrmidon unit in the formation to an Archmagos Prime (0-1 per army) or a Magos Prime.'),
        UP('Tech-Priest', parts=[U((1, 3), 'Tech Priests', 25)]),
        UP('Transport', parts=[MECH_TRANSPORT], desc='Add enough transports to carry the entire formation.'),
        UP('Krios', parts=[U((1, 3), 'Krios Battle Tank', 50)]),
        UP('Karacnos', parts=[U((1, 3), 'Karacnos Assault Tank', 75)]),
        UP('Thanatar', parts=[U((1, 3), 'Thanatar Battle-Automata', 75)]),
        UP('Hyperios', parts=[Swap(1, 3, ('Tarantula Platform', 'Hyperios Platform', 50))]),
        UP('Scyllax', parts=[U((1, 4), 'Scyllax Guardian-Automata', 50)]),
    ],
    cohesive=['Legion Astartes', 'Knight Household', 'Legio Titanicus'],
    disruptive=['Imperial Militia', 'Solar Auxilia'],
    rules=['Allies', 'Automaton', 'Cortex Controller', 'Cybernetica Cortex', 'Lance', 'Singularity', 'Void Shields'],
    notes=['A detachment may choose up to four upgrades, each only once, and only one transport option.',
           'Up to 1/3 of the army\'s points may be spent on Allies or Lords of War.',
           'Only one Archmagos Prime may be included in the army.'])

# ---------------------------------------------------------------- Legio Titanicus
SCOUT_WEAPONS = [('Inferno Gun', 0), ('Vulcan Mega Bolter', 0), ('Plasma Blastgun', 0), ('Turbo Laser Destructor', 25)]
BATTLE_WEAPONS = [('Laser Burner', 0), ('Corvus Assault Pod', 0), ('Carapace Landing Pad', 0),
                  ('Plasma Cannon', 25), ('Gatling Blaster', 25), ('Apocalypse Missile Launcher', 25),
                  ('Close Combat Weapon', 25), ('Melta Cannon', 50), ('Laser Blaster', 50), ('Volcano Cannon', 50),
                  ('Plasma Destructor', 75), ('Support Missile', 75), ('Quake Cannon', 75)]
TITANICUS = ARMY(
    'Legio Titanicus', ['Legio Titanicus'], 3, '1+', 0, None, None,
    formations=[
        F('Warhound Titan', 'line', 275, [U(1, 'Warhound Scout Titan')], 'Veteran Princeps', maxn=1, per=4000),
        F('Warhound Scout Pack', 'line', 500, [U(2, 'Warhound Scout Titan')], 'Veteran Princeps'),
        F('Reaver Titan', 'line', 575, [U(1, 'Reaver Battle Titan')], 'Legate OR Veteran Princeps, Air Defence, Sacred Icon'),
        F('Warlord Titan', 'line', 725, [U(1, 'Warlord Battle Titan')], 'Legate OR Veteran Princeps, Air Defence, Sacred Icon'),
        F('Warbringer Nemesis Titan', 'line', 650, [U(1, 'Warbringer Nemesis Titan')],
          'Legate OR Veteran Princeps, Sacred Icon',
          note='Fan rules, not part of EpicAU: adapted from the Epic-UK Adeptus Titanicus codex (version 080925), where it '
               'costs 750 pts with weapons. Here it takes a Quake or Volcano Cannon on the carapace and 2 arm weapons at '
               'EpicAU weapon costs. It has built-in AA guns, so no Air Defence upgrade.'),
        F('Warmaster Titan', 'line', 1050, [U(1, 'Warmaster Heavy Battle Titan')],
          'Legate OR Veteran Princeps, Sacred Icon', maxn=1,
          note='Fan rules, not part of EpicAU: adapted from the Epic-UK Adeptus Titanicus codex (version 080925), where it '
               'is a 0-1 Support Titan costing 1500 pts with weapons and is meant mainly for friendly games. Here its '
               'carapace weapon is chosen at EpicAU weapon costs. It has built-in AA guns, so no Air Defence upgrade. '
               'Priced between a fully armed Warlord and the 1350 pt Emperor-class Titans, which are tougher and better '
               'armed.'),
        F('Emperor Class Titan', 'low', 1350,
          [Or(Opt('Imperator', U(1, 'Imperator Support Titan (experimental)')),
              Opt('Warmonger', U(1, 'Warmonger Support Titan (experimental)')))], 'Legate OR Veteran Princeps'),
    ],
    upgrades=[
        UP('Legate', 50, parts=[U(1, 'Legate')], maxn=1, desc='You may only have one Legate upgrade in your entire army.'),
        UP('Veteran Princeps', 25, parts=[U(1, 'Veteran Princeps')]),
        UP('Air Defence', 50, parts=[U(1, 'Carapace Multi-Lasers')]),
        UP('Sacred Icon', 50, parts=[U(1, 'Sacred Icon')]),
    ],
    cohesive=['Legion Astartes', 'Knight Household', 'Mechanicum Taghmata'],
    disruptive=['Imperial Militia', 'Solar Auxilia', 'Daemons Of The Ruinstorm'],
    rules=['Allies', 'Void Shields'],
    notes=['Each upgrade may only be taken once per formation.',
           'Legio Titanicus has no Support Detachments.',
           'Warhounds carry 2 Scout Titan weapons; Reavers 3 and Warlords 4 Scout or Battle Titan weapons. '
           'The fan-made Warbringer carries a Quake or Volcano Cannon plus 2 weapons, and the Warmaster 1. '
           'Arm/carapace mount restrictions are noted on each weapon.',
           'The wiki sets no Allies/Lords of War points limit for Legio Titanicus.'])
TITAN_WEAPON_SLOTS = {'Warhound Scout Titan': (2, SCOUT_WEAPONS),
                      'Reaver Battle Titan': (3, SCOUT_WEAPONS + BATTLE_WEAPONS),
                      'Warlord Battle Titan': (4, SCOUT_WEAPONS + BATTLE_WEAPONS),
                      # Fan-made, adapted from Epic-UK: the Warbringer's carapace must take a Quake or Volcano Cannon.
                      'Warbringer Nemesis Titan': [('Carapace Weapon', 1, [('Quake Cannon', 75), ('Volcano Cannon', 50)]),
                                                   ('Titan Weapons', 2, SCOUT_WEAPONS + BATTLE_WEAPONS)],
                      'Warmaster Heavy Battle Titan': (1, SCOUT_WEAPONS + BATTLE_WEAPONS)}

# ---------------------------------------------------------------- Knight Household
QUESTORIS = ['Questorius Knight-Paladin', 'Questorius Knight-Errant']
CERASTUS = ['Cerastus Knight-Lancer', 'Cerastus Knight-Castigator']
KNIGHTS = ARMY(
    'Knight Household', ['Knight Household'], 3, '2', 2, None, 1 / 3,
    formations=[
        F('Questoris Knights', 'line', 325,
          [Or(Opt('Questoris Knight-Paladins', U(3, QUESTORIS[0])), Opt('Questoris Knight-Errants', U(3, QUESTORIS[1])))],
          'Aspirants, Noble, Seneschal, Expanded Armoury, Raise the Banners'),
        F('Cerastus Knights', 'support', 375,
          [Or(Opt('Cerastus Knight-Lancers', U(3, CERASTUS[0])), Opt('Cerastus Knight-Castigators', U(3, CERASTUS[1])))],
          'Noble, Enhanced Forge, Rally the Troops'),
        F('Armiger Knights', 'support', 200,
          [Or(Opt('Armiger Knight-Warglaives', U(5, 'Armiger Knight-Warglaive')),
              Opt('Armiger Knight-Helverins', U(5, 'Armiger Knight-Helverin')))], 'Aspirants', maxn=1, per=2000),
        F('Acastus Knight Porphyrion', 'low', 0, [U((1, 2), 'Acastus Knight Porpyhrion', 250)], 'Noble'),
    ],
    upgrades=[
        UP('Aspirants', -50, desc='The formation suffers -1 to Advance, Overwatch, March, Marshal and Sustained Fire action rolls.'),
        UP('Raise the Banners', parts=[Mix(1, 2, *[(k, 100) for k in QUESTORIS])],
           desc='Add 1-2 Knights of a type already in the formation.'),
        UP('Rally the Troops', parts=[Mix(1, 2, *[(k, 125) for k in CERASTUS])],
           desc='Add 1-2 Knights of a type already in the formation.'),
        UP('Noble', 25, parts=[Or(Opt('Lord Scion', U(1, 'Lord Scion')), Opt('Preceptor', U(1, 'Preceptor')), label='Noble')]),
        UP('Enhanced Forge', parts=[Swap(1, None, *[(tuple(CERASTUS), k, 25) for k in (
            'Cerastus Knight-Acheron', 'Cerastus Knight-Atropos')])]),
        UP('Expanded Armoury', parts=[Swap(1, None, *[(tuple(QUESTORIS), k, 25) for k in (
            'Questorius Knight-Warden', 'Questorius Knight-Styrix', 'Questorius Knight-Crusader',
            'Questorius Knight-Gallant', 'Questorius Knight-Magaera')])]),
        UP('Seneschal', 75, parts=[U(1, 'Seneschal')], maxn=1),
    ],
    cohesive=['Legio Titanicus', 'Mechanicum Taghmata'],
    disruptive=['Imperial Militia', 'Legion Astartes', 'Solar Auxilia'],
    rules=['Allies', 'Knight Household', 'Ion Gauntlet', 'Ion Shield', 'Lance', 'Singularity'],
    notes=['Detachments may choose any number of upgrades, each only once.',
           'The wiki sets no Allies/Lords of War limit for Knight Household; 1/3 is used, matching Departmento Munitorum.'])

# ---------------------------------------------------------------- Imperial Militia
IM_TRANSPORT = Or(Opt('Arvus Lighter', U((1, None), 'Arvus Lighter Orbital Shuttle', 25)),
                  Opt('Auxilia Rhinos', U((1, None), 'Auxilia Rhino', 12.5)),
                  Opt('Auxilia Land Raider', U((1, None), 'Land Raider Proteus', 50)), label='Transport')
PROVENANCE_TYPES = ['Warrior Elite', 'Survivors of the Dark Age', 'Feral Warriors', 'Traitors']
DM = ['Discipline Master']
MILITIA = ARMY(
    'Imperial Militia', ['Imperial Militia'], 2, '2+', 2, 4, 1 / 3,
    formations=[
        F('Militia Command Squad', 'line', 225, [U(1, 'Force Commander'), U(7, 'Militia Auxiliary')],
          'Heavy Transport OR Transport, Fire Support, Militia Auxiliary, Sniper, Ogryn Brute Squad, Provenance',
          maxn=1, extra_up=DM),
        F('Inducted Levy Squad', 'line', 100, [U(10, 'Levy Auxiliaries')], 'Ogryn Brute Squad, Provenance', extra_up=DM),
        F('Militia Motorcycle Squad', 'line', 175, [U(1, 'Motorcycle Commander'), U(7, 'Militia Bikers')],
          'Provenance (Loyal)', extra_up=DM),
        F('Militia Grenadier Squad', 'line', 175, [U(8, 'Militia Grenadier Squad')], 'Heavy Transport OR Transport, Provenance',
          extra_up=DM),
        F('Militia Infantry Squad', 'line', 125, [U(1, 'Platoon Command Squad'), U(7, 'Militia Auxiliary')],
          'Heavy Transport OR Transport, Fire Support, Militia Auxiliary, Sniper, Ogryn Brute Squad, Provenance', extra_up=DM),
        F('Orbital Support', 'support', 0,
          [Or(Opt('Emperor Class Battleship', U(1, 'Emperor Class Battleship'), cost=300),
              Opt('Dauntless Class Light Cruiser', U(1, 'Dauntless Class Light Cruiser'), cost=150))], maxn=1),
        F('Auxilia Cavalry Squad', 'support', 175, [U(6, 'Cavalry Auxiliary')], extra_up=DM),
        F('Auxilia Heavy Ordnance Battery', 'support', 200,
          [Or(Opt('Basilisks', U(3, 'Basilisk Artillery Carriage')), Opt('Medusas', U(3, 'Medusa Artillery Carriage')))],
          extra_up=DM),
        F('Auxilia Malcador Heavy Tank Squadron', 'support', 350,
          [Mix(5, 5, ('Auxilia Malcador', 0), ('Auxilia Malcador Annihalator', 0))], extra_up=DM),
        F('Auxilia Rapier Battery', 'support', 100, [U(4, 'Auxilia Rapier Platform')], extra_up=DM),
        F('Auxilia Sentinel Scout Squadron', 'support', 100, [U(4, 'Auxilia Sentinel')], extra_up=DM),
        F('Auxilia Super Heavy Tank', 'support', 200,
          [Or(Opt('Baneblade', U(1, 'Auxilia Baneblade')), Opt('Stormhammer', U(1, 'Auxilia Stormhammer')))], extra_up=DM),
        F('Auxiliary Battle Tank Attack Squadron', 'support', 350,
          [Mix(5, 5, ('Leman Russ Battle Tank', 0), ('Auxilia Leman Russ Exterminator', 0), ('Leman Russ Demolisher', 0))],
          'Vanquisher', extra_up=DM),
        F('Auxilia Super Heavy Tank Platoon', 'low', 500, [Mix(3, 3, ('Auxilia Baneblade', 0), ('Auxilia Stormhammer', 0))]),
        F('Imperial Militia Avenger Wing', 'low', 250, [U(2, 'Imperial Navy Avenger Strike Fighter')]),
        F('Imperial Militia Primaris-Lightning Wing', 'low', 225, [U(2, 'Imperial Navy Primaris-Lightning Strike Fighter')]),
    ],
    upgrades=[
        UP('Fire Support', 100, parts=[U(4, 'Militia Fire Support Squad')]),
        UP('Heavy Transport', parts=[U((1, None), 'Auxilia Gorgon', 125)],
           desc='Add enough Gorgon Heavy Transporters to transport the entire formation.'),
        UP('Militia Auxiliary', 50, parts=[U(4, 'Militia Auxiliary')]),
        UP('Ogryn Brute Squad', 150, parts=[U(4, 'Ogryn Brute Squad')]),
        UP('Provenance', 50, parts=[Or(*[Opt(p) for p in PROVENANCE_TYPES], label='Provenance')], rules=['Provenance'],
           desc='Upgrade all INF units in the detachment with one Provenance type.'),
        UP('Provenance (Loyal)', 50, parts=[Or(*[Opt(p) for p in PROVENANCE_TYPES[:3]], label='Provenance')],
           rules=['Provenance'], desc='Warrior Elite, Survivors of the Dark Age or Feral Warriors only.'),
        UP('Sniper', 75, parts=[U(4, 'Recon Auxiliary')]),
        UP('Transport', parts=[IM_TRANSPORT],
           desc='Add enough transports to carry the entire formation (Arvus 25 pts each, Rhinos 25 pts per 2, Land Raider 50 pts each).'),
        UP('Vanquisher', parts=[Swap(1, 1, (('Leman Russ Battle Tank', 'Auxilia Leman Russ Exterminator',
                                             'Leman Russ Demolisher'), 'Auxilia Leman Russ Vanquisher', 25))]),
        UP('Discipline Master', 0, parts=[Or(Opt('Discipline Master', U(1, 'Discipline Master')),
                                             Opt('Rogue Psyker', U(1, 'Rogue Psyker')), label='Character')],
           rules=['Discipline Masters / Rogue Psykers'], maxn=1, per=500, round_up=True),
    ],
    cohesive=['Legio Titanicus', 'Legion Astartes', 'Knight Household'],
    disruptive=['Solar Auxilia', 'Mechanicum Taghmata', 'Daemons Of The Ruinstorm (Traitor Militia)'],
    rules=['Allies', 'Berserk', 'Dedicated War Engine Transports', 'Discipline Masters / Rogue Psykers', 'Provenance',
           'Exploratory Augury Web'],
    notes=['Line Detachments may take up to four upgrades, one of each type. Support Detachments may take up to four upgrades, each once.',
           'Up to 1/3 of the army\'s points may be spent on Allies and/or Lords of War.',
           'When an Imperial Militia (Traitor Militia) army is chosen, at least one detachment must take the Traitors provenance.'])

# ---------------------------------------------------------------- Daemons of the Ruinstorm
GODS = {
    'Khorne': dict(troop='Bloodletters', herald='Herald of Khorne', prince='Daemon Prince of Khorne',
                   small=['Bloodletters', 'Flesh Hounds'], big=['Bloodcrushers', 'Skull Cannon'],
                   greater='Bloodthirster (Greater Daemon)',
                   followers=[('Bloodcrushers', 50), ('Flesh Hounds', 25), ('Skull Cannon', 50)]),
    'Nurgle': dict(troop='Plaguebearers', herald='Herald of Nurgle', prince='Daemon Prince of Nurgle',
                   small=['Plaguebearers', 'Nurglings'], big=['Beasts of Nurgle', 'Plague Drones'],
                   greater='Great Unclean One (Greater Daemon)',
                   followers=[('Beasts of Nurgle', 50), ('Nurglings', 25), ('Plague Drones', 50)]),
    'Slaanesh': dict(troop='Daemonettes', herald='Herald of Slaanesh', prince='Daemon Prince of Slaanesh',
                     small=['Daemonettes', 'Seekers'], big=['Seeker Chariot', 'Fiends'],
                     greater='Keeper of Secrets (Greater Daemon)',
                     followers=[('Seekers', 50), ('Seeker Chariot', 25), ('Fiends', 50)]),
    'Tzeentch': dict(troop='Horrors', herald='Herald of Tzeentch', prince='Daemon Prince of Tzeentch',
                     small=['Horrors', 'Flamers', 'Screamers'], big=['Burning Chariot of Tzeentch'],
                     greater='Lord of Change (Greater Daemon)',
                     followers=[('Flamers', 50), ('Screamers', 25), ('Burning Chariot of Tzeentch', 50)]),
}
GIFTS = 'Daemon Prince, Chaos Spawn, Chaos Altar, Furies, Armoured Support'
FOLLOWER_GIFTS = 'Chaos Spawn, Chaos Altar, Furies, Armoured Support'


def horde(god, g):
    return F(f'{god} Horde', 'horde', 250,
             [U(6, g['troop']), U(1, g['herald']),
              Mix(0, 6, *[(u, 25) for u in g['small']], label='Additional Lesser Daemons'),
              Mix(0, 6, *[(u, 50) for u in g['big']], label='Additional Daemons'),
              U((0, 1), g['greater'], 200)],
             GIFTS.replace('Daemon Prince', f'Daemon Prince ({god})'),
             note=f'One {g["troop"]} unit carries the Herald; may add Lesser Daemons, Daemons and 1 Greater Daemon.')


DAEMONS = ARMY(
    'Daemons Of The Ruinstorm', ['Daemons Of The Ruinstorm'], 2, '2+', 0, None, 1 / 3,
    formations=[
        F('Warp Rift', 'special', 75, [], maxn=1, rules=['Chaos Gate'],
          note='Replaces one objective on the Daemon World side of the table. Counts as a Chaos Gate and an objective, '
               'cannot be attacked, and only Daemonic Horde and Followers of Chaos detachments may use it.'),
        F('Daemonic Overlord', 'special', 0, [], maxn=1,
          note='One Daemon Prince, Herald or Greater Daemon in the army gains Supreme Commander for free.'),
        *[horde(god, g) for god, g in GODS.items()],
        F('Greater Daemon Horde', 'greater', 0,
          [Or(*[Opt(god, U((1, 3), g['greater'], 200)) for god, g in GODS.items()], label='Chaos God')],
          note='1-3 Greater Daemons of the same Chaos god; requires a Daemonic Horde of the same god.'),
        *[F(f'Followers of {god}', 'followers', 0, [Mix(6, 9, *g['followers'], label='Followers')], FOLLOWER_GIFTS,
            note='6-9 units drawn from the listed types (3-9 of any type taken).') for god, g in GODS.items()],
        F('Undivided: Fury Flight', 'followers', 0, [U((6, 8), 'Furies', 25)], FOLLOWER_GIFTS),
        F('Undivided: Spawn Pack', 'followers', 0, [U((4, 6), 'Chaos Spawn', 50)], FOLLOWER_GIFTS),
        F('Undivided: Soulgrinder Maniple', 'followers', 0, [U((4, 6), 'Soul Grinder', 75)], FOLLOWER_GIFTS),
    ],
    upgrades=[
        *[UP(f'Daemon Prince ({god})', 50, parts=[Swap(1, 1, (g['herald'], g['prince'], 0))],
             desc='One Daemon Prince per Chaos faction in the army.')
          for god, g in GODS.items()],
        UP('Chaos Spawn', parts=[U((1, 3), 'Chaos Spawn', 50)]),
        UP('Chaos Altar', 100, parts=[U(1, 'Chaos Altar')]),
        UP('Furies', parts=[U((1, 3), 'Furies', 25)]),
        UP('Armoured Support', parts=[U((1, 3), 'Soul Grinder', 75)]),
    ],
    cohesive=['Legion Astartes (Traitor Legions)', 'Solar Auxilia', 'Imperial Militia (Traitor Militia)'],
    disruptive=['Mechanicum Taghmata', 'Legio Titanicus', 'Knight Household'],
    rules=['Allies', 'Berserk', 'Instability', 'Chaos Gate', 'Daemonic Assault'],
    notes=['One Followers of Chaos detachment (same god or Undivided) may be taken per Daemonic Horde.',
           '0-1 Greater Daemon Horde per god-affiliated Daemonic Horde of the same god.',
           'Daemonic Hordes and Followers of Chaos may take any number of Gifts of Chaos, each once per detachment.',
           'Allied units may only come from one other army list; allied Lords of War may be freely chosen.',
           'Up to 1/3 of the army\'s points may be spent on Allies and Lords of War.',
           'Berserk formations cannot claim objectives in the GT scenario.'])

OTHER_ARMIES = [CUSTODES, SOLAR_AUXILIA, MECHANICUM, TITANICUS, KNIGHTS, MILITIA, DAEMONS]
