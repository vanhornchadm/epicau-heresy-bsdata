"""Weapon choices for units whose reference-sheet rows list alternatives ("X OR Y").

Each unit's choices are groups picked on the unit: a required group takes exactly one option (the first is the
default), an optional group takes at most one. An option names the sheet rows it adds to the unit's profile (trailing
"OR" dropped), or gives rows of its own with R() where the sheet runs several weapons into one row; those combined
sheet rows are listed in REPLACED_ROWS. `ff`, `armour` and `cc` set the unit's stat when the sheet gives one value per
option. `requires` (upgrade, option) offers the option only in formations that took that option of that upgrade.
Titans pick their weapons the same way, one pick per slot, from TITAN_WEAPON_SLOTS in spec_others.py.
"""


def R(name, rng, firepower):
    return {'name': name, 'range': rng, 'firepower': firepower}


def O(label, rows=None, cost=0, ff=None, armour=None, cc=None, requires=None):
    return {'label': label, 'rows': [label] if rows is None else rows, 'cost': cost, 'ff': ff, 'armour': armour,
            'cc': cc, 'requires': requires}


def G(label, *options, optional=False):
    return {'label': label, 'optional': optional, 'options': [O(o) if isinstance(o, str) else o for o in options]}


RAPIER = ['Laser Destroyer', 'Quad Mortar', 'Quad Heavy Bolter']
CONTEMPTOR_ARMS = ['Close Combat Weapon', 'TL Heavy Bolter', 'Plasma Cannon', 'Heavy Conversion Beamer',
                   'Kheres Assault Cannon', 'TL Autocannon', 'Multi-Melta', 'TL Lascannon']
LEVIATHAN_ARMS = ['Siege Claw', 'Siege Drill', 'Cyclonic Melta Lance', 'Storm Cannon', 'Grav-flux Bombard']
SATURNINE_WEAPONS = ['Plasma Bombards', 'Twin Heavy Disintegrators', 'Disruption Fists']

WEAPON_OPTIONS = {
    # Legion Astartes
    'Rapier': [G('Weapon', *RAPIER, 'Graviton Cannon')],
    'Land Speeder': [G('Weapon', O('Multi-Melta', [R('Multi-Melta', '15cm AND (15cm)', 'AP5+/AT5+, MW AND (small arms) MW')]),
                       O('Plasma Cannon & Heavy Bolter', [R('Plasma Cannon', '30cm', 'AP5+/AT5+, Fleshbane'),
                                                          R('Heavy Bolter', '30cm', 'AP5+')]))],
    'Javelin Attack Speeder': [G('Weapon', O('TL Lascannon', [R('TL Lascannon', '45cm', 'AT4+')]),
                                 O('TL Cyclone Missile Launcher', [R('TL Cyclone Missile Launcher', '45cm', 'AP3+/AT5+')]))],
    'Contemptor Dreadnought': [G('Arm weapon 1', *CONTEMPTOR_ARMS), G('Arm weapon 2', *CONTEMPTOR_ARMS),
                               G('Carapace weapon', O('Havoc Launcher', cost=5), optional=True)],
    'Deredeo Dreadnought': [G('Weapon', 'Anvilus Autocannon Battery', 'Hellfire Plasma Cannon')],
    'Dreadnought': [G('Weapons', O('TL Lascannon & TL Missile Launcher', ['TL Lascannon', 'TL Missile Launcher'], ff='4+'),
                      O('TL Autocannon & Power Fist', ['TL Autocannon', 'Power Fist'], ff='5+'))],
    'Land Raider Achilles': [G('Weapons', '2 x TL Multi-Melta', '2 x TL Volkite Culverin')],
    'Leviathan Siege Dreadnought': [G('Arm weapon 1', *LEVIATHAN_ARMS), G('Arm weapon 2', *LEVIATHAN_ARMS)],
    'Predator': [G('Turret', 'TL Lascannon', 'Predator Cannon', 'Flamestorm Cannon'),
                 G('Sponsons', O('2 x Heavy Bolters', ff='3+'), O('2 x Lascannon', ff='5+'),
                   O('2 x Heavy Flamers', ff='3+'))],
    'Predator Executioner': [G('Weapon', 'Plasma Destroyer', 'Heavy Conversion Beamer')],
    'Mastodon Heavy Assault Transport': [G('Carapace', 'Skyreaper Battery', O('Command Relay', []))],
    'Fire Raptor Gunship': [G('Weapons', '2 x Quad Heavy Bolter', '2 x Reaper Autocannon Battery')],
    'Thunderhawk Gunship': [G('Main gun', 'Thunderhawk Cannon', 'Thunderhawk Laser Destroyer')],
    'Kratos Heavy Tank': [G('Main gun', 'Kratos Battlecannon', 'Melta Cannon'),
                          G('Hull', '2 x Hull Heavy Bolters', '2 x Hull Lascannons'),
                          G('Sponsons', '2 x Sponson Heavy Bolters', '2 x Sponson Lascannons')],
    'Legion Tarantula': [G('Weapon', 'TL Lascannon', 'TL Heavy Bolter')],
    'Araknae Weapons Platform': [G('Weapon', 'Quad Accelerator Autocannon', 'Twin Punisher Cannon',
                                   'Orias Heavy Frag Missiles')],
    'Saturnine Terminators': [G('Weapon 1', *SATURNINE_WEAPONS), G('Weapon 2', *SATURNINE_WEAPONS)],
    'Saturnine Dreadnought': [G('Weapon', 'Heavy Plasma Bombard', 'Graviton Pulveriser')],
    # Legio Custodes
    'Telemon Heavy Dreadnought': [G('Weapons', '2 x Telemon Caestus', 'Arachnus Storm Cannon')],
    # Solar Auxilia
    'Solar Auxilia Rapier Platform': [G('Weapon', *RAPIER)],
    'Veletaris Storm Section': [G('Weapons', O('Volkite Chargers', ff='4+'), O('Power Axes', ff='6+'))],
    'Cyclops Demolition Vehicle': [G('Charge', 'Demolition Charge', 'Incineration Charge')],
    # Mechanicum Taghmata
    'Tarantula Platform': [G('Weapon', O('TL Lascannon', ff='6+'), O('TL Heavy Bolter', ff='5+'))],
    'Krios Battle Tank': [G('Weapon', 'Lightning Cannon', 'Pulsar Fusil')],
    'Mechanicum Land Raider': [G('Weapons', O('2 x Twin Lascannon', ff='4+'), O('2 x Flamestorm Cannon', ff='3+'),
                                 O('2 x Twin Multimelta', ff='4+'))],
    'Thanatar Battle-Automata': [G('Weapon', 'Hellex Plasma Mortar', 'Sollex Heavy Lascannon')],
    'Ordinatus Majoris': [G('Main gun', 'Sonic Disruptor', '6 x Golgothan Missiles', 'Nova Cannon')],
    'Ordinatus Minoris': [G('Main gun', 'Bellacosa Volcano Cannon', 'Ulator Sonic Destroyer')],
    'Scintillax': [G('Weapon', 'Exo-planar Cannon', 'Storm Laser')],
    'Errax': [G('Weapon', 'Errax Lascutters', 'Errax Meltagun')],
    'Tenebrax': [G('Weapon', 'Stalker Volkite Culverins', 'Exo-planar Cannon', 'Stalker Maxima Bolters')],
    'Serperos': [G('Weapon 1', 'Storm Laser Array', 'Exo-planar Bombard'),
                 G('Weapon 2', 'Serperos Lascutters', 'Irradiation Engine')],
    'Harpax': [G('Weapons', 'Exo-planar Repeaters', 'Harpax Lascutters')],
    # Imperial Militia
    'Auxilia Rapier Platform': [G('Weapon', *RAPIER)],
    'Militia Auxiliary': [G('Weapons', O('Rifles', ff='5+'), O('Pistol and Combat Weapon', ff='6+'))],
    'Auxilia Gorgon': [G('Weapons', 'Gorgon Mortars', '2 x TL Heavy Bolters')],
    'Ogryn Brute Squad': [G('Weapons', O('Power weapons', armour='4+', cc='4+'), O('Ripper Guns', armour='4+', cc='5+'),
                            O('Chaos Spawn Mutations', armour='3+', cc='3+', requires=('Provenance', 'Traitors')))],
}

# Sheet rows that run several weapons together; the options above give their weapons as rows of their own.
REPLACED_ROWS = {
    'Land Speeder': ['Multi-Melta OR Plasma Cannon / Heavy Bolter'],
    'Javelin Attack Speeder': ['TL Lascannon OR TL Cyclone Missile Launcher'],
    # Titans: the rows naming their weapon slots
    'Warhound Scout Titan': ['2 Scout Titan Weapon Variants'],
    'Reaver Battle Titan': ['3 x Scout or Battle Titan Weapon Variants'],
    'Warlord Battle Titan': ['4 x Scout or Battle Titan Weapon Variants'],
    'Warbringer Nemesis Titan': ['Quake Cannon OR Volcano Cannon', '2 x Scout or Battle Titan Weapon Variants'],
    'Warmaster Heavy Battle Titan': ['1 x Scout or Battle Titan Weapon Variant'],
    'Dire Wolf Heavy Scout Titan': ['Volcano Cannon OR Neutron Laser OR Conversion Beam Dissipator'],
    'Warmaster Iconoclast Titan': ['Kirus Siege Drill OR Kirus Grav Imploder'],
}
