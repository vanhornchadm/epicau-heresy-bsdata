"""Legion Astartes core list and the 18 unique Legion variations (EpicAU wiki)."""
import json

from dsl import U, Opt, Or, Mix, Swap, Fill, Carry, F, UP, ARMY

LEGION_SHEETS = ['Legion Astartes', 'Loyalist Legions', 'Traitor Legions']

SICARANS = [('Sicaran Battle Tank', 75), ('Sicaran Venator', 75), ('Sicaran Omega Tank Destroyer', 75)]
NEW_SICARANS = [U((0, 6), 'Sicaran Punisher', 75, new=True), U((0, 6), 'Sicaran Arcus', 75, new=True)]  # fan-made


def heavy_transport(*types):
    # (cost, capacity in transport space: Tactical-sized units take 1, Terminators and Dreadnoughts 2)
    specs = {'Land Raider Phobos': (75, 2), 'Land Raider Proteus': (75, 2), 'Spartan Assault Tank': (125, 4),
             'Mastodon Heavy Assault Transport': (200, 8)}
    return Or(*[Opt(t, Carry(specs[t][1], t, specs[t][0])) for t in types], label='Transport')


CORE_UPGRADES = [
    UP('Armoury Assets', parts=[Swap(1, 2,
        ('Predator', 'Predator Infernus', 20), ('Predator', 'Predator Executioner', 20),
        ('Predator', 'Whirlwind Scorpius', 20),
        (('Land Raider Proteus', 'Land Raider Phobos'), 'Land Raider Achilles', 25),
        ('Contemptor Dreadnought', 'Deredeo Dreadnought', 40), ('Vindicator', 'Vindicator Laser Destroyer', 20))]),
    UP('Assault Claw', parts=[Carry(4, 'Kharybdis Assault Claw', 75, space='Assault Claw space')],
       desc='Add enough Kharybdis Assault Claws to transport the entire formation. Each carries 4 Tactical-sized '
            'units, 2 Terminators or 1 Dreadnought; the count is set from the formation.'),
    UP('Assault Ram', parts=[Carry(2, 'Caestus Assault Ram', 50, space='Transport units')],
       desc='Add enough Caestus Assault Rams to transport the entire formation. Each carries 2 Breacher or '
            'Terminator units; the count is set from the formation.'),
    UP('Centurion', 50, parts=[Or(Opt('Librarian', U(1, 'Librarian')), Opt('Chaplain', U(1, 'Chaplain')),
                                  Opt('Champion', U(1, 'Champion')), label='Centurion')]),
    UP('Dreadnought', parts=[Mix(1, 2, ('Dreadnought', 50), ('Contemptor Dreadnought', 60),
                                 ('Deredeo Dreadnought', 100), ('Leviathan Siege Dreadnought', 100))]),
    UP('Drop Assault', 0, parts=[U(1, 'Drop Pod', label='Drop Pods')], rules=['Drop Assault'],
       desc='Transport the entire formation in Drop Pods.'),
    UP('Heavy Transport', parts=[heavy_transport('Land Raider Phobos', 'Land Raider Proteus',
                                                 'Spartan Assault Tank', 'Mastodon Heavy Assault Transport')],
       desc='Add enough transports to carry the entire formation. Land Raiders carry 2 Tactical-sized units or 1 '
            'Terminator, Spartans twice that and Mastodons four times (Dreadnoughts count as Terminators); the '
            'count is set from the formation.'),
    UP('Hyperios', 75, parts=[U(1, 'Whirlwind Hyperios')]),
    UP('Praetor', parts=[Or(Opt('Lieutenant Commander', U(1, 'Lieutenant Commander'), cost=50),
                            Opt('Lord Commander', U(1, 'Lord Commander'), cost=100), label='Praetor')],
       desc='You cannot take a Lord Commander if your army includes a Primarch.'),
    UP('Rapier Battery', parts=[U((1, 4), 'Rapier', 50)]),
    UP('Support Squads', parts=[Or(Opt('Tactical Support', U((1, 4), 'Tactical Support Squad', 25)),
                                   Opt('Heavy Support', U((1, 4), 'Heavy Support Squad', 50)), label='Support Squads')]),
    UP('Standard Transport', 0, parts=[Fill(2, ('Rhino Armoured Carrier', 0), ('Damocles Command Rhino', 0, 1))],
       desc='Add enough Rhino Armoured Carriers to transport the entire formation after all other upgrades are chosen. '
            'Each Rhino carries 2 Tactical-sized units; one of them may be a Damocles Command Rhino. The count is set from the '
            'formation; add this upgrade last, or adjust the transports if you change units afterwards.'),
    UP('Tank', parts=[Mix(1, 2, ('Vindicator', 50), ('Predator', 60), ('Sicaran Battle Tank', 80),
                          ('Typhon Siege Tank', 150), ('Cerberus Tank Destroyer', 150))]),
    UP('Teleport', 50, rules=['Teleport'], desc='Add the Teleport special rule to each INF unit in the formation.'),
]

T_STD = 'Standard Transport OR Drop Assault OR Assault Claw OR Heavy Transport'

CORE_FORMATIONS = [
    # Line
    F('Legion Tactical Detachment', 'line', 275,
      [Or(Opt('Tactical Squads', U(8, 'Tactical Squad')), Opt('Despoiler Squads', U(8, 'Despoiler Squad')))],
      T_STD + ', Centurion OR Praetor, Armoury Assets, Dreadnought, Rapier Battery, Support Squads, Hyperios, Tank'),
    F('Legion Terminator Detachment', 'line', 0, [U((4, 6), 'Terminators', 75)],
      'Assault Claw OR Assault Ram OR Heavy Transport OR Teleport, Centurion OR Praetor, Armoury Assets, Dreadnought, Hyperios, Tank'),
    F('Legion Assault Marine Detachment', 'line', 300, [U(8, 'Assault Squad')], 'Drop Assault, Centurion OR Praetor'),
    F('Legion Breacher Detachment', 'line', 300, [U(8, 'Breacher Squad')],
      'Drop Assault OR Assault Claw OR Assault Ram OR Heavy Transport, Centurion OR Praetor, Armoury Assets, Dreadnought, Hyperios, Tank'),
    # Support
    F('Legion Artillery Battery', 'support', 0,
      [Or(Opt('Medusa', U(4, 'Medusa'), cost=250), Opt('Whirlwinds', U(4, 'Whirlwind'), cost=300),
          Opt('Basilisks', U(4, 'Basilisk'), cost=325))], 'Hyperios', maxn=1, per=2000),
    F('Legion Assault Marine Squad', 'support', 175, [U(4, 'Assault Squad')], 'Drop Assault, Centurion'),
    F('Legion Breacher Marine Squad', 'support', 225, [U(4, 'Breacher Squad')],
      'Drop Assault OR Assault Claw OR Assault Ram OR Heavy Transport, Centurion'),
    F('Legion Dreadnought Talon', 'support', 0, [U((4, 6), 'Dreadnought', 50)], 'Drop Assault, Centurion'),
    F('Legion Leviathan Dreadnought Talon', 'support', 0, [U(3, 'Leviathan Siege Dreadnought', 75)], 'Drop Assault, Centurion'),
    F('Legion Destroyer Detachment', 'support', 225, [U(4, 'Destroyer Squad')], 'Drop Assault, Centurion', maxn=1, per=4000),
    F('Legion Contemptor Dreadnought Talon', 'support', 0, [U((4, 6), 'Contemptor Dreadnought', 60)],
      'Drop Assault, Centurion, Armoury Assets'),
    F('Legion Javelin Attack Squadron', 'support', 250, [U(5, 'Javelin Attack Speeder')], 'Centurion'),
    F('Legion Land Speeder Squadron', 'support', 200, [U(5, 'Land Speeder')], 'Centurion'),
    F('Legion Land Raider Squadron', 'support', 0,
      [Or(Opt('Land Raider Phobos', U((4, 6), 'Land Raider Phobos', 80)),
          Opt('Land Raider Proteus', U((4, 6), 'Land Raider Proteus', 80)))], 'Centurion, Armoury Assets, Hyperios'),
    F('Legion Outrider Detachment', 'support', 175,
      [Or(Opt('Outrider Bikes', U(5, 'Outrider Squad')), Opt('Attack Bikes', U(5, 'Attack Bike')))], 'Centurion'),
    F('Legion Predator Strike Squadron', 'support', 0, [U((4, 6), 'Predator', 60)], 'Centurion, Armoury Assets, Hyperios'),
    F('Legion Rapier Weapons Battery', 'support', 240, [U(6, 'Rapier')], 'Drop Assault'),
    F('Legion Reconnaissance Squad', 'support', 150, [U(4, 'Reconnaissance Squad')],
      'Standard Transport OR Drop Assault OR Assault Claw, Centurion'),
    F('Legion Sicaran Battle Squadron', 'support', 0, [Mix(4, 6, *SICARANS, *NEW_SICARANS)], 'Centurion, Hyperios'),
    F('Legion Sabre Strike Squadron', 'support', 275, [U(4, 'Sabre Strike Tank')], 'Centurion',
      note='Sabre Strike Tank stats are not on the wiki reference sheet; taken from Departmento Munitorum.'),
    F('Legion Kratos Heavy Tank Squadron', 'support', 0, [U((2, 4), 'Kratos Heavy Tank', 100)], 'Centurion, Hyperios',
      new=True,
      note='Fan rules, not part of EpicAU: proposed on Dakka Dakka (November 2024) as 2 Kratos for 200 pts plus up to '
           '2 more at 100 pts each. The upgrades follow the other Legion tank squadrons.'),
    F('Legion Sky Hunter Attack Squadron', 'support', 175, [U(5, 'Scimitar Jetbike')], 'Centurion'),
    F('Legion Storm Eagle Attack Wing', 'support', 0, [U((1, 3), 'Storm Eagle Attack Ship', 125)]),
    F('Legion Spacecraft', 'support', 0,
      [Or(Opt('Strike Cruiser', U(1, 'Strike Cruiser'), cost=200), Opt('Battle Barge', U(1, 'Battle Barge'), cost=300))],
      maxn=1),
    F('Legion Thunderhawk Gunship', 'support', 250, [U(1, 'Thunderhawk Gunship')]),
    F('Legion Thunderhawk Transport Wing', 'support', 0, [U((1, 3), 'Thunderhawk Transporter', 100)]),
    F('Legion Vindicator Squadron', 'support', 0, [U((4, 6), 'Vindicator', 50)], 'Centurion, Armoury Assets, Hyperios'),
    # Lords of War
    F('Legion Gunship Wing', 'low', 300, [U(2, 'Fire Raptor Gunship')]),
    F('Legion Interceptor Attack Wing', 'low', 250, [U(2, 'Xiphon Interceptor')]),
    F('Legion Stormbird', 'low', 450, [U(1, 'Sokar Pattern Storm Bird Heavy Attack Ship')]),
    F('Legion Super Heavy Tank', 'low', 250,
      [Or(Opt('Fellblade', U(1, 'Fellblade Super Heavy Tank')), Opt('Glaive', U(1, 'Glaive Super Heavy Tank')))]),
    F('Legion Super Heavy Tank Destroyer', 'low', 300, [U(1, 'Falchion Super Heavy Tank Destroyer')]),
    F('Legion Super Heavy Tank Battery', 'low', 400,
      [Or(Opt('Typhon', U(3, 'Typhon Siege Tank')), Opt('Cerberus', U(3, 'Cerberus Tank Destroyer')))]),
]

# Units that take one Tactical space in a Rhino. Most say "counts as Tactical" on the reference sheet;
# Mor Deythan and Templar Brethren have no note but are offered Standard Transport, so they are included.
# Demi-Gods count as their retinue's type and are tagged by the generator.
TACTICAL_SPACE = [
    'Tactical Squad', 'Despoiler Squad', 'Tactical Support Squad', 'Heavy Support Squad', 'Reconnaissance Squad',
    'Mor Deythan Strike Squad', 'Templar Brethren', 'Grey Slayer Pack', 'Deathsworn Pack', 'Terror Squad',
    'Rampager Squad', 'Palatine Blades', 'Kakophoni Squad', 'Havoc Support Squad', 'Gal Vorbak Dark Brethren',
    'Reaver Attack Squad', 'Headhunter Kill Team', 'Khenetai Blades', 'Ammitara Intercessor Squad',
]

LEGION_RULES = ['Legion Astartes', 'Allies', 'Demi-God', 'Exploratory Augury Web', 'Feedback', 'Fleshbane',
                'Sniper', 'Void Shields']


def primarch(name, primarch_unit, retinue, up, cost=450, alt=None):
    units = alt or [U(1, primarch_unit), *retinue]
    return F(name, 'low', cost, units, up, maxn=1, rules=['Demi-God'])


DESTROYER = lambda per: F('Destroyer Detachment', 'support', 225, [U(4, 'Destroyer Squad')], 'Drop Assault, Centurion',
                          maxn=1, per=per)
SHT_SQUADRON = lambda *tanks: F('Legion Super Heavy Tank Squadron', 'low', 700,
                                [Or(*[Opt(t.split()[0], U(3, t)) for t in tanks])], 'Centurion')
BOLTGUNS = U(7, 'Tactical Squad', label='Tactical Marines (Boltguns)')

# Each legion: formations that replace a same-named core formation or are added.
# 'remove' lists core formations the legion may not take; 'upgrades' adds/overrides upgrades.
LEGIONS = {
    # ---------------- Loyalists ----------------
    'Iron Hands': dict(allegiance='Loyalist', formations=[
        F('Legion Predator Detachment', 'line', 350, [U(6, 'Predator')], 'Centurion OR Praetor, Armoury Assets, Hyperios'),
        F('Legion Terminator Detachment', 'line', 0,
          [Or(Opt('Terminators', U((4, 6), 'Terminators', 75)), Opt('Gorgon Terminators', U((4, 6), 'Gorgon Terminator Squad', 85)))],
          'Heavy Transport OR Teleport OR Assault Ram, Centurion OR Praetor'),
        DESTROYER(2000),
        F('Medusan Immortals Squad', 'support', 250, [U(4, 'Medusan Immortals Squad')], 'Heavy Transport OR Assault Ram',
          maxn=1, per=1000),
        SHT_SQUADRON('Fellblade Super Heavy Tank', 'Glaive Super Heavy Tank'),
        primarch('Ferrus Manus, the Bane of Asirnoth', 'Ferrus Manus, the Bane of Asirnoth', [U(3, 'Gorgon Terminator Squad')],
                 'Assault Ram OR Heavy Transport OR Teleport, Armoury Assets, Tank, Hyperios'),
    ], cohesive=['Legio Titanicus', 'Mechanicum Taghmata', 'Knight Household', 'Legio Custodes'],
        disruptive=['Imperial Militia', 'Solar Auxilia']),
    'Raven Guard': dict(allegiance='Loyalist', formations=[
        DESTROYER(2000),
        F('Dark Fury Squad', 'support', 250, [U(4, 'Dark Fury Assault Marines')], 'Drop Assault, Centurion', maxn=1, per=2000),
        F('Mor Deythan Strike Detachment', 'support', 225, [U(4, 'Mor Deythan Strike Squad')],
          'Standard Transport OR Drop Assault OR Teleport, Centurion'),
        F('Legion Storm Eagle Attack Wing', 'support', 0, [U((1, 3), 'Darkwing Pattern Storm Eagle', 125)]),
        primarch('Corvus Corax, the Shadow Lord', 'Corvus Corax, the Shadow Lord', [U(5, 'Assault Squad')],
                 'Drop Assault OR Assault Claw', cost=400),
    ], cohesive=['Legio Custodes'],
        disruptive=['Imperial Militia', 'Solar Auxilia', 'Knight Household', 'Mechanicum Taghmata', 'Legio Titanicus']),
    'Salamanders': dict(allegiance='Loyalist', formations=[
        F('Legion Terminator Detachment', 'line', 0,
          [Or(Opt('Terminators', U((4, 6), 'Terminators', 75)), Opt('Firedrake Terminators', U((4, 6), 'Firedrake Terminator Squad', 85)))],
          'Heavy Transport OR Teleport OR Assault Ram, Centurion OR Praetor'),
        F('Pyroclast Detachment', 'support', 0, [U((4, 6), 'Pyroclast Squad', 60)], 'Heavy Transport OR Assault Ram',
          maxn=1, per=2000),
        primarch('Vulkan, the Promethean Fire', 'Vulkan, the Promethean Fire', [U(3, 'Firedrake Terminator Squad')],
                 'Assault Ram OR Heavy Transport OR Teleport, Armoury Assets, Tank, Hyperios'),
    ], cohesive=['Solar Auxilia', 'Legio Titanicus', 'Legio Custodes'],
        disruptive=['Imperial Militia', 'Knight Household', 'Mechanicum Taghmata']),
    'Ultramarines': dict(allegiance='Loyalist', formations=[
        F('Fulmentarus Strike Detachment', 'line', 0,
          [Or(Opt('Terminators', U((4, 6), 'Terminators', 75)), Opt('Fulmentarus Terminators', U((4, 6), 'Fulmentarus Terminator Squad', 85)))],
          'Heavy Transport OR Teleport OR Assault Ram, Centurion OR Praetor, Armoury Assets', maxn=1, per=2000),
        F('Locutarus Assault Detachment', 'line', 300, [U(6, 'Loctarus Storm Squad')], 'Drop Assault OR Assault Claw'),
        DESTROYER(2000),
        F('Invictarus Suzerain Detachment', 'support', 300,
          [U(4, 'Invictarus Suzerain Squad'), U(1, 'Champion', label='Centurion (Champion)')],
          'Drop Assault OR Heavy Transport, Armoury Assets, Tank, Hyperios', maxn=1, per=4000,
          note='One Invictarus Suzerain Squad carries a Centurion (Champion) upgrade.'),
        primarch('Roboute Guilliman, Master of Ultramar', 'Roboute Guilliman, Master of Ultramar', [BOLTGUNS],
                 'Standard Transport OR Drop Assault OR Heavy Transport, Tank, Armoury Assets, Hyperios'),
    ], cohesive=['Imperial Militia', 'Solar Auxilia', 'Knight Household', 'Mechanicum Taghmata', 'Legio Titanicus',
                 'Legio Custodes'], disruptive=[]),
    'Imperial Fists': dict(allegiance='Loyalist', formations=[
        DESTROYER(2000),
        F('Phalanx Warder Detachment', 'support', 350, [U(8, 'Phalanx Warder Squad')],
          'Drop Assault OR Assault Ram OR Heavy Transport, Centurion, Tank, Armoury Assets', maxn=1, per=2000),
        F('Templar Brethren Detachment', 'support', 400,
          [U(6, 'Templar Brethren'), U(1, 'Champion', label='Centurion (Champion)')],
          'Standard Transport OR Drop Assault OR Heavy Transport', maxn=1, per=4000,
          note='One Templar Brethren unit carries a Centurion (Champion) upgrade.'),
        F('Castellum Stronghold', 'support', 250, [U(1, 'Castellum Stronghold')], maxn=2, per=4000,
          note='Includes Defensive Obstacles.'),
        F('Primus Redoubt', 'support', 300, [U(1, 'Primus Redoubt')], maxn=1, per=4000, note='Includes Defensive Obstacles.'),
        F('Legion Super Heavy Tank Squadron', 'low', 700, [U(3, 'Fellblade Super Heavy Tank')], 'Centurion'),
        primarch('Rogal Dorn, Praetorian of Terra', 'Rogal Dorn, Praetorian of Terra', [BOLTGUNS],
                 'Standard Transport OR Drop Assault OR Heavy Transport, Tank, Armoury Assets, Hyperios'),
    ], cohesive=['Imperial Militia', 'Solar Auxilia', 'Knight Household', 'Mechanicum Taghmata', 'Legio Titanicus',
                 'Legio Custodes'], disruptive=[]),
    'Blood Angels': dict(allegiance='Loyalist', formations=[
        F('Dawnbreaker Cohort', 'support', 0, [U((4, 6), 'Dawnbreaker Cohort Squad', 50)], 'Drop Assault OR Assault Claw'),
        F('The Angels Tears', 'support', 0, [U((4, 6), 'Angel Tears Squad', 50)], 'Drop Assault OR Assault Claw'),
        F('Crimson Paladins', 'support', 300, [U(4, 'Crimson Paladin Squad')], 'Teleport OR Heavy Transport'),
        primarch('Sanguinius, the Angel', 'Sanguinius, the Angel', [U(5, 'Assault Squad')], 'Drop Assault OR Assault Claw'),
    ], cohesive=['Mechanicum Taghmata', 'Legio Titanicus', 'Legio Custodes'],
        disruptive=['Imperial Militia', 'Solar Auxilia', 'Knight Household']),
    'Dark Angels': dict(allegiance='Loyalist', formations=[
        DESTROYER(2000),
        F('Dreadwing Interemptor Detachment', 'support', 250, [U(4, 'Dreadwing Interemptor Squad')],
          'Drop Assault OR Heavy Transport, Centurion', maxn=1, per=2000),
        SHT_SQUADRON('Fellblade Super Heavy Tank', 'Glaive Super Heavy Tank'),
        primarch("Lion El'Johnson, the Son of the Forest", "Lion El'Johnson, the Son of the Forest", [U(3, 'Terminators')],
                 'Heavy Transport OR Teleport, Armoury Assets, Tank, Hyperios'),
    ], cohesive=['Legio Titanicus', 'Solar Auxilia', 'Legio Custodes'],
        disruptive=['Imperial Militia', 'Knight Household', 'Mechanicum Taghmata']),
    'White Scars': dict(allegiance='Loyalist', formations=[
        F('Chogorian Brotherhood', 'line', 275,
          [Or(Opt('Outrider Bikes', U(4, 'Outrider Squad')), Opt('Attack Bikes', U(4, 'Attack Bike'))), U(4, 'Scimitar Jetbike')],
          'Praetor OR Centurion, Scythes of the Khan'),
        DESTROYER(2000),
        F('Legion Javelin Attack Squadron', 'support', 250,
          [Mix(5, 5, ('Javelin Attack Speeder', 0), ('Kyzagan Assault Speeder', 0))], 'Centurion'),
        F('Ebon Keshig', 'low', 300, [U(4, 'Ebon Keshig Squad')], 'Heavy Transport OR Teleport OR Assault Claw', maxn=1),
        primarch('Jaghatai Khan, the Great Khan', 'Jaghatai Khan, the Great Khan', [U(3, 'Terminators')],
                 'Heavy Transport OR Teleport OR Assault Claw'),
    ], upgrades=[UP('Scythes of the Khan', parts=[Swap(1, 4, ('Scimitar Jetbike', 'Golden Keshig', 50))])],
        cohesive=['Legio Titanicus', 'Solar Auxilia', 'Mechanicum Taghmata', 'Knight Household', 'Legio Custodes'],
        disruptive=['Imperial Militia']),
    'Space Wolves': dict(allegiance='Loyalist', formations=[
        F('Grey Slayer Warband', 'line', 300, [U(8, 'Grey Slayer Pack')],
          'Standard Transport OR Drop Assault, Praetor OR Centurion, Hyperios, Tank, Armoury Assets'),
        F('Deathsworn Warband', 'support', 250, [U(4, 'Deathsworn Pack')], 'Standard Transport OR Drop Assault OR Heavy Transport'),
        F('Wolf Guard Detachment', 'support', 340, [U(4, 'Varagyr Wolf Guard Terminator Squad')],
          'Heavy Transport OR Teleport OR Assault Ram, Armoury Assets'),
        primarch('Leman Russ, the Wolf King', 'Leman Russ, the Wolf King', [U(3, 'Varagyr Wolf Guard Terminator Squad')],
                 'Heavy Transport OR Assault Claw OR Assault Ram OR Teleport, Armoury Assets'),
    ], upgrades=[UP('Centurion', 50, parts=[Or(Opt('Chaplain', U(1, 'Chaplain')), Opt('Champion', U(1, 'Champion')),
                                               label='Centurion')],
                    desc='A Space Wolves army cannot select a Librarian as part of a Centurion upgrade.')],
        cohesive=['Legio Titanicus', 'Legio Custodes'],
        disruptive=['Imperial Militia', 'Solar Auxilia', 'Mechanicum Taghmata', 'Knight Household']),
    # ---------------- Traitors ----------------
    'Night Lords': dict(allegiance='Traitor', formations=[
        F('Night Raptor Squad', 'support', 225, [U(4, 'Night Raptor Squad')], 'Drop Assault OR Assault Claw', maxn=1, per=1000),
        F('Terror Detachment', 'support', 250, [U(6, 'Terror Squad')],
          'Standard Transport OR Drop Assault OR Heavy Transport, Centurion OR Praetor', maxn=1, per=2000),
        DESTROYER(1000),
        primarch('Konrad Curze, The Night Haunter', 'Konrad Curze, the Night Haunter', [BOLTGUNS],
                 'Standard Transport OR Drop Assault OR Heavy Transport OR Assault Claw, Tank, Armoury Assets, Hyperios'),
    ], cohesive=['Legio Titanicus'],
        disruptive=['Daemons Of The Ruinstorm', 'Imperial Militia', 'Solar Auxilia', 'Knight Household', 'Mechanicum Taghmata']),
    'World Eaters': dict(allegiance='Traitor', formations=[
        F('Rampager Detachment', 'line', 0, [U((4, 6), 'Rampager Squad', 60)],
          'Standard Transport OR Drop Assault OR Heavy Transport, Centurion', maxn=1, per=2000),
        F('Red Butchers Detachment', 'support', 0, [U((4, 6), 'Red Butcher Terminator Squad', 85)],
          'Heavy Transport OR Teleport OR Assault Ram', maxn=1, per=2000),
        DESTROYER(1000),
        primarch('Angron, Master of the World Eaters', 'Angron, Master of the World Eaters', [U(3, 'Terminators')],
                 'Drop Assault OR Assault Claw OR Assault Ram OR Heavy Transport OR Teleport'),
    ], cohesive=['Legio Titanicus', 'Daemons Of The Ruinstorm (Khorne)'],
        disruptive=['Imperial Militia', 'Solar Auxilia', 'Knight Household', 'Mechanicum Taghmata']),
    "Emperor's Children": dict(allegiance='Traitor', formations=[
        F('Palatine Blades Detachment', 'support', 0, [U((4, 6), 'Palatine Blades', 60)],
          'Standard Transport OR Drop Assault OR Assault Claw, Centurion', maxn=1, per=2000),
        F('Kakophoni Detachment', 'support', 0, [U((4, 6), 'Kakophoni Squad', 60)],
          'Standard Transport OR Drop Assault OR Heavy Transport, Armoury Assets, Tank, Hyperios', maxn=1, per=2000),
        F('Phoenix Terminator Detachment', 'support', 340, [U(4, 'Phoenix Terminator Squad')],
          'Heavy Transport OR Teleport OR Assault Ram, Centurion OR Praetor', maxn=1, per=2000),
        primarch('Fulgrim, the Illuminator', 'Fulgrim, the Illuminator', [U(3, 'Terminators')],
                 'Assault Claw OR Assault Ram OR Heavy Transport OR Teleport'),
    ], cohesive=['Legio Titanicus', 'Daemons Of The Ruinstorm (Slaanesh)'],
        disruptive=['Imperial Militia', 'Solar Auxilia', 'Knight Household', 'Mechanicum Taghmata']),
    'Iron Warriors': dict(allegiance='Traitor', formations=[
        F('Legion Land Raider Battle Squadron', 'line', 0,
          [Mix(4, 6, ('Land Raider Proteus', 80), ('Land Raider Phobos', 80))],
          'Centurion OR Praetor, Armoury Assets, Tank, Hyperios'),
        F('Iron Havoc Detachment', 'line', 250, [U(4, 'Havoc Support Squad')],
          'Standard Transport OR Drop Assault OR Heavy Transport, Centurion, Hyperios'),
        F('Legion Terminator Detachment', 'line', 0,
          [Mix(4, 6, ('Terminators', 75), ('Tyrant Siege Terminator Squad', 85))],
          'Heavy Transport OR Teleport OR Assault Ram, Centurion OR Praetor, Tank, Armoury Assets, Dreadnought, Hyperios'),
        F('Legion Artillery Battery', 'support', 0,
          [Or(Opt('Medusa', U(6, 'Medusa'), cost=300), Opt('Whirlwinds', U(6, 'Whirlwind'), cost=400),
              Opt('Basilisks', U(6, 'Basilisk'), cost=500))], 'Hyperios', maxn=1, per=1000),
        primarch('Perturabo, Primarch of the Iron Warriors', None, None,
                 'Assault Ram OR Heavy Transport OR Teleport, Armoury Assets, Hyperios', cost=0,
                 alt=[U(1, 'Perturabo, Primarch of the Iron Warriors'),
                      Or(Opt('with Terminators', U(3, 'Terminators'), cost=450),
                         Opt('in Tormentor', U(1, 'Tormentor'), cost=400),
                         Opt('with Iron Circle', U(4, 'Iron Circle Automata'), cost=400), label='Retinue')]),
        SHT_SQUADRON('Fellblade Super Heavy Tank', 'Stormblade'),
    ], cohesive=['Legio Titanicus', 'Mechanicum Taghmata'],
        disruptive=['Daemons Of The Ruinstorm', 'Imperial Militia', 'Solar Auxilia', 'Knight Household']),
    'Death Guard': dict(allegiance='Traitor', remove=['Legion Assault Marine Detachment'], formations=[
        F('Legion Terminator Detachment', 'line', 0,
          [Or(Opt('Terminators', U((4, 6), 'Terminators', 75)), Opt('Grave Warden Terminators', U((4, 6), 'Grave Warden Terminator Squad', 85)))],
          'Heavy Transport OR Teleport OR Assault Ram, Praetor OR Centurion'),
        F('Deathshroud Terminator Detachment', 'support', 300, [U(4, 'Deathshroud Terminator')],
          'Heavy Transport OR Teleport OR Assault Ram, Centurion OR Praetor', maxn=1, per=4000),
        DESTROYER(1000),
        primarch('Mortarion, the Pale King', 'Mortarion, the Pale King', [U(3, 'Terminators')],
                 'Assault Ram OR Heavy Transport OR Teleport, Tank, Armoury Assets, Hyperios'),
    ], cohesive=['Legio Titanicus', 'Daemons Of The Ruinstorm (Nurgle)'],
        disruptive=['Mechanicum Taghmata', 'Imperial Militia', 'Solar Auxilia', 'Knight Household'],
        notes=['A Death Guard army cannot take a Legion Assault Marine Detachment as a Line Detachment.']),
    'Word Bearers': dict(allegiance='Traitor', formations=[
        F('Gal Vorbak Dark Brethren', 'support', 250, [U(6, 'Gal Vorbak Dark Brethren')],
          'Standard Transport OR Drop Assault OR Assault Claw, Centurion', maxn=1, per=1000),
        F('Ashen Circle Detachment', 'support', 350, [U(8, 'Incendiary Squad')],
          'Drop Assault OR Assault Claw, Centurion OR Praetor, Dreadnought', maxn=1, per=2000),
        DESTROYER(2000),
        F('Legion Contemptor Dreadnought Talon', 'support', 0,
          [Mix(4, 6, ('Contemptor Dreadnought', 60), ('Mal Ghara Tainted Contemptor Dreadnought', 70))],
          'Drop Assault, Centurion, Armoury Assets'),
        primarch('Lorgar, the Voice of Truth', 'Lorgar, the Voice of Truth', [BOLTGUNS],
                 'Standard Transport OR Drop Assault OR Heavy Transport, Tank, Armoury Assets, Hyperios'),
    ], cohesive=['Daemons Of The Ruinstorm', 'Imperial Militia (Traitor Militia)'],
        disruptive=['Legio Titanicus', 'Mechanicum Taghmata', 'Knight Household', 'Solar Auxilia']),
    'Sons of Horus': dict(allegiance='Traitor', formations=[
        F('Reaver Attack Detachment', 'line', 300, [U(6, 'Reaver Attack Squad')],
          T_STD + ', Centurion OR Praetor, Tank', maxn=1, per=2000),
        DESTROYER(2000),
        F('Justaerin Terminator Detachment', 'support', 350, [U(4, 'Justaerin Terminator Squad')],
          'Heavy Transport OR Teleport OR Assault Ram, Centurion OR Praetor, Tank', maxn=1, per=2000),
        primarch('Horus Lupercal, the Warmaster', 'Horus Lupercal, Breaker of Tyrants', [U(3, 'Terminators')],
                 'Assault Claw OR Heavy Transport OR Teleport, Tank, Armoury Assets, Hyperios'),
    ], cohesive=['Legio Titanicus', 'Imperial Militia', 'Solar Auxilia'],
        disruptive=['Daemons Of The Ruinstorm', 'Mechanicum Taghmata', 'Knight Household']),
    'Alpha Legion': dict(allegiance='Traitor', formations=[
        F('Headhunter Kill Squad', 'support', 200, [U(4, 'Headhunter Kill Team')],
          'Standard Transport OR Drop Assault OR Heavy Transport, Centurion OR Praetor, Tank'),
        F('Lernaean Terminator Detachment', 'support', 340, [U(4, 'Laerenaen Terminator Squad')],
          'Heavy Transport OR Teleport OR Assault Ram, Centurion OR Praetor'),
        primarch('Alpharius & Omegon', 'Alpharius & Omegon', [BOLTGUNS],
                 'Standard Transport OR Drop Assault OR Assault Claw OR Heavy Transport, Tank, Armoury Assets, Hyperios'),
    ], cohesive=['Legio Titanicus', 'Imperial Militia', 'Solar Auxilia', 'Mechanicum Taghmata', 'Knight Household'],
        disruptive=['Daemons Of The Ruinstorm']),
    'Thousand Sons': dict(allegiance='Traitor', formations=[
        F('Khenetai Occult Blade Cabal', 'support', 225, [U(4, 'Khenetai Blades')], 'Standard Transport OR Drop Assault'),
        F('Ammitara Occult Intercession Cabal', 'support', 275, [U(4, 'Ammitara Intercessor Squad')],
          'Standard Transport OR Drop Assault OR Teleport'),
        F('Sekhmet Terminator Cabal', 'support', 340, [U(4, 'Sekhmet Terminator Squad')],
          'Heavy Transport OR Teleport OR Assault Ram, Centurion'),
        primarch('Magnus the Red, the Crimson King', 'Magnus the Red, the Crimson King', [U(3, 'Sekhmet Terminator Squad')],
                 'Teleport OR Assault Claw OR Heavy Transport'),
    ], cohesive=['Legio Titanicus', 'Daemons Of The Ruinstorm (Tzeentch)'],
        disruptive=['Imperial Militia', 'Solar Auxilia', 'Mechanicum Taghmata', 'Knight Household']),
}

CORE_COHESIVE = ['Legio Titanicus']
CORE_DISRUPTIVE = ['Daemons Of The Ruinstorm', 'Imperial Militia', 'Solar Auxilia', 'Knight Household',
                   'Mechanicum Taghmata']


def norm(name):
    n = name.lower().replace("the ", "")
    for p in ('legion ',):
        if n.startswith(p):
            n = n[len(p):]
    return n.strip()


def legion_army(legion=None):
    """Build the core Legion list, overlaid with a unique Legion's formations when given."""
    formations = {norm(f['name']): f for f in CORE_FORMATIONS}
    upgrades = list(CORE_UPGRADES)
    cohesive, disruptive, notes = CORE_COHESIVE, CORE_DISRUPTIVE, []
    name = 'Legion Astartes'
    if legion:
        L = LEGIONS[legion]
        for r in L.get('remove', []):
            formations.pop(norm(r))
        for f in L['formations']:
            formations[norm(f['name'])] = f  # replaces a same-named core entry
        by_name = {u['name']: u for u in upgrades}
        for u in L.get('upgrades', []):
            by_name[u['name']] = u
        upgrades = list(by_name.values())
        cohesive, disruptive = L['cohesive'], L['disruptive']
        notes = L.get('notes', [])
        name = f'Legion Astartes - {legion}'
    return ARMY(name, LEGION_SHEETS, 5, '1+', 3, 4, 1 / 3, list(formations.values()), upgrades,
                cohesive=cohesive, disruptive=disruptive, rules=LEGION_RULES, transport_space=TACTICAL_SPACE,
                notes=['A line or support detachment may choose up to four upgrades; each upgrade only once and only one transport option.',
                       'Up to 1/3 of the army\'s points may be spent on Allies and/or Lords of War.'] + notes)


def legion_catalogue():
    """One Legion list where the Legion is a choice: core formations plus every Legion's, each shown only for
    the Legions it belongs to. Core formations a Legion replaces or removes are hidden for that Legion."""
    a = legion_army()
    a['notes'] = a['notes'][:2] + ['Choose the Legion in the Legion entry; its allies and special formations '
                                   'are listed there. "None" uses the core list only.']
    core = {norm(f['name']): dict(f, show_for=None, hide_for=[]) for f in CORE_FORMATIONS}
    extra = {}  # spec json -> formation shown for the Legions that share it
    core_up = {u['name'] for u in CORE_UPGRADES}
    a['upgrade_variants'] = {}
    for legion, L in LEGIONS.items():
        for r in L.get('remove', []):
            core[norm(r)]['hide_for'].append(legion)
        for f in L['formations']:
            if norm(f['name']) in core:
                core[norm(f['name'])]['hide_for'].append(legion)
            key = json.dumps(f, sort_keys=True, default=str)
            extra.setdefault(key, dict(f, show_for=[], hide_for=[], key=legion))['show_for'].append(legion)
        for u in L.get('upgrades', []):
            if u['name'] in core_up:
                a['upgrade_variants'].setdefault(u['name'], []).append(([legion], u))
            else:
                a['upgrades'][u['name']] = u
    a['formations'] = list(core.values()) + list(extra.values())
    a['legions'] = [dict(name=legion, allegiance=L['allegiance'], cohesive=L['cohesive'], disruptive=L['disruptive'],
                         notes=L.get('notes', [])) for legion, L in LEGIONS.items()]
    a['core_allies'] = (CORE_COHESIVE, CORE_DISRUPTIVE)
    return a
