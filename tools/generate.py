"""Generate BattleScribe data (.gst/.cat) for the EpicAU Horus Heresy supplement.

Usage: python3 generate.py [output_dir]
Reads source/units.json (reference sheets) and source/titan_weapons.json, plus the
hand-transcribed army list specs in spec_legion.py / spec_others.py.
"""
import hashlib
import json
import os
import re
import sys
from xml.sax.saxutils import escape, quoteattr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rules import RULES, ALIASES, ACRONYMS  # noqa: E402
from spec_legion import legion_catalogue  # noqa: E402
from spec_others import OTHER_ARMIES, TITAN_WEAPON_SLOTS  # noqa: E402
from weapon_options import WEAPON_OPTIONS, REPLACED_ROWS  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
BS_VERSION = '2.03'
AUTHOR = 'EpicAU Horus Heresy (community) - BSData conversion'
SOURCE_URL = 'https://web.archive.org/web/20201111221247/http://epicau.com/mw/index.php/Main_Page'
GST_NAME = 'Epic Armageddon - EpicAU Horus Heresy'
GST_FILE = 'Epic Armageddon - EpicAU Horus Heresy.gst'


def gid(*key):
    h = hashlib.md5('|'.join(str(k) for k in key).encode()).hexdigest()
    return f'{h[0:4]}-{h[4:8]}-{h[8:12]}-{h[12:16]}'


GST_ID = gid('gst', GST_NAME)
PTS = 'points'
PT_UNIT, PT_WAR_ENGINE, PT_WEAPON = gid('pt', 'Unit'), gid('pt', 'War Engine'), gid('pt', 'Weapon')
# A unit's profile names its weapons with their counts ('Lascannons x2'), and each weapon's stats are a Weapon profile
# of its own listed under the unit. Its special rules are rules linked from the unit, not a column. War engines get
# their damage capacity, void shields and critical hit as columns of their own.
UNIT_CHARS = ['Type', 'Speed', 'Armour', 'CC', 'FF', 'Weapons']
WAR_ENGINE_CHARS = UNIT_CHARS + ['Damage Capacity', 'Void Shields', 'Critical Hit']
WEAPON_CHARS = ['Range', 'Firepower', 'Notes']
# New Recruit moves a column below the table when any of its cells is longer than 80 characters, or 52 in a profile
# with more than 5 columns (its whole text, <BR> tags included, in a window wider than 500px). A long critical hit
# goes in a rule of its own, and a weapon cell too long for the table in a '<weapon> notes' rule.
CELL_LIMIT = 80
WIDE_CELL_LIMIT = 52
SEE_RULES = 'See rules'
SEE_WEAPON_NOTES = 'See weapon notes'
CATS = ['Line Detachment', 'Support Detachment', 'Lord of War', 'Daemonic Horde', 'Greater Daemon Horde',
        'Followers of Chaos', 'Special Selection', 'Allies & Lords of War', 'Supreme Commander', 'Spacecraft',
        'Primarch', 'Character', 'Configuration', 'Tactical Transport Space', 'Upgraded Unit',
        'Not available with the chosen Configuration']
HIDDEN_CATS = {'Tactical Transport Space', 'Upgraded Unit'}  # internal bookkeeping categories


def ally_rules():
    """Primary-army key -> (cohesive armies, disruptive armies), from each list (and each Legion choice).

    Qualifiers such as '(Traitor Legions)' or '(Nurgle)' are dropped: only the army itself is checked. Lists that
    name no allies at all (Legio Custodes) are left out, so they place no restriction.
    """
    base = lambda names: {re.sub(r'\s*\(.*\)\s*$', '', n) for n in names}
    legion = legion_catalogue()
    lists = [(a['name'], a['cohesive'], a['disruptive']) for a in OTHER_ARMIES]
    lists.append(('Legion Astartes (core list)',) + legion['core_allies'])
    lists += [(f'Legion Astartes ({l["name"]})', l['cohesive'], l['disruptive']) for l in legion['legions']]
    return {f'Primary army: {name}': (base(c), base(d)) for name, c, d in lists if c or d}


ALLY_RULES = ally_rules()
ALLY_NA_CAT = 'Not an allowed ally of the primary army'
CATS += list(ALLY_RULES) + [ALLY_NA_CAT]
HIDDEN_CATS |= set(ALLY_RULES)
CAT = {c: gid('cat', c) for c in CATS}
SLOT_CAT = {'line': 'Line Detachment', 'support': 'Support Detachment', 'low': 'Lord of War',
            'horde': 'Daemonic Horde', 'greater': 'Greater Daemon Horde', 'followers': 'Followers of Chaos',
            'special': 'Special Selection'}
RULE_ID = {name: gid('rule', name) for name in RULES}
# Hidden cost types counting how much transport space a unit takes, one per weighting scheme in the transports'
# capacities: most take Tactical-sized units 1 and bulky units (Terminators, Dreadnoughts, Ogryns...) 2; the
# Caestus counts units of any size; the Kharybdis fits 4 Tactical-sized units, 2 Terminators or 1 Dreadnought.
TRANSPORT_SCHEMES = ['Transport space', 'Transport units', 'Assault Claw space']
COST_ID = {s: gid('cost', s) for s in TRANSPORT_SCHEMES}
BULKY = re.compile(r'Terminator|Dreadnought|Ogryn|Thallax|Ursarax|Myrmidon|Aquilon')
NA_CAT = 'Not available with the chosen Configuration'  # flags selections a Configuration choice has ruled out
NEW_UNITS_ID = gid('config', 'Allow fan-made units')  # game-system toggle that shows fan-made units roster-wide
# How a list's Configuration choice reads (an army may give its own as 'choice'). tag: each option names the primary
# army for ally checks, as the Legion choice sets the allies.
LEGION_CHOICE = dict(label='Legion', none='None (core list)', none_rule='Core list',
                     none_text='The core Legion list, with no unique Legion.', allegiance_text='{} Legion.', tag=True)

# Units not present on the wiki reference sheet: the Sabre from Departmento Munitorum, the Kratos from fan rules
# posted on Dakka Dakka (https://www.dakkadakka.com/dakkaforum/posts/list/812078.page, last edited 2024-11-09), and
# the Warbringer and Warmaster adapted from the Epic-UK Adeptus Titanicus codex (version 080925), and the Sicaran
# Punisher and Arcus: the Sicaran Battle Tank's hull with main guns derived from existing EpicAU weapons. The Legion
# Tarantulas use the Solar Auxilia Tarantula hulls with the Mechanicum Tarantula's weapon choice. The Ascalon, Araknae,
# Saturnine Terminators and Dreadnought and the Termite convert their Legions Imperialis rules against EpicAU units.
# Solar Auxilia: the Marauder Bomber and Thunderbolt come from the NetEA Imperial Guard lists, the Marauder Destroyer
# from the Epic-UK Imperial Guard codex (version 011026), and the Malcador Annihilator from the EpicAU Imperial Militia
# sheet on the Solar Auxilia Malcador's hull; the rest convert their Legions Imperialis rules against EpicAU units.
# The Dark Mechanicum Stalkers and Harpax, and the Arlatax, Domitar, Krios Venator and Archmagos Prime on Abeyant,
# convert the Legions Imperialis profiles in the BSData Legions Imperialis data
# (https://github.com/BSData/Horus-Heresy-Legions-Imperialis) against the EpicAU Mechanicum automata. The Acastus
# Knight Asterius and Knight Moirax convert the same data's Knights library against the EpicAU Porphyrion and Armigers.
TITAN_STEP = ("May step over impassable terrain or dangerous terrain that is lower than the titan's knees and no greater "
              "than 2cm wide.")
TITAN_CRIT = ("Critical Hit: Roll a D6 in the end phase for the remainder of the game, on a 1, the Titan's reactor explodes, "
              "destroying it completely and hitting all units within 5cm on a standard 4+ to hit, on a 2-3, the Titan "
              "loses a point of DC, 4-6 the reactor is repaired.")
WARHOUND_CRIT = ('Critical Hit: The Titan staggers D6cm in a random direction taking an additional DC, any units that come '
                 'into base contact with it as it staggers take a standard hit on a 6+.')
EXTRA_UNITS = {
    'Legion Astartes': [{
        'name': 'Sabre Strike Tank', 'type': 'AV', 'speed': '35cm', 'armour': '5+', 'cc': '6+', 'ff': '5+',
        'weapons': [{'name': 'Volkite Saker', 'range': '15cm', 'firepower': '2 x AP3+, Fleshbane, FxF'},
                    {'name': 'Sabre Missiles', 'range': '30cm', 'firepower': 'AT4+, FxF'}],
        'notes': 'Reinforced Armour.'}, {
        'name': 'Kratos Heavy Tank', 'type': 'WE', 'speed': '25cm', 'armour': '4+', 'cc': '6+', 'ff': '5+',
        'weapons': [{'name': 'Kratos Battlecannon OR', 'range': '45cm', 'firepower': '2 x AP3+/AT3+, Armourbane'},
                    {'name': 'Melta Cannon', 'range': '30cm',
                     'firepower': '4 x MW5+, Armourbane'},
                    {'name': 'Co-axial Autocannon', 'range': '45cm', 'firepower': 'AP5+/AT6+'},
                    {'name': '2 x Hull Heavy Bolters OR', 'range': '30cm', 'firepower': 'AP5+, Fwd'},
                    {'name': '2 x Hull Lascannons', 'range': '45cm',
                     'firepower': 'AT5+, Fwd'},
                    {'name': '2 x Sponson Heavy Bolters OR', 'range': '30cm', 'firepower': 'AP5+'},
                    {'name': '2 x Sponson Lascannons', 'range': '45cm',
                     'firepower': 'AT5+'}],
        'notes': 'DC2, Reinforced Armour, Thick Rear Armour. A Kratos must select either a Kratos Battlecannon OR Melta '
                 'Cannon, and either Heavy Bolters OR Lascannons for its hull and for its sponsons, before the start of '
                 'the game. Critical Hit: Unit is destroyed.'}, {
        'name': 'Sicaran Punisher', 'type': 'AV', 'speed': '35cm', 'armour': '5+', 'cc': '6+', 'ff': '3+',
        'weapons': [{'name': 'Punisher Rotary Cannon', 'range': '30cm', 'firepower': '3 x AP3+/AT6+'},
                    {'name': '3 x Heavy Bolter', 'range': '30cm', 'firepower': 'AP5+'}],
        'notes': 'Reinforced Armour'}, {
        'name': 'Sicaran Arcus', 'type': 'AV', 'speed': '35cm', 'armour': '5+', 'cc': '6+', 'ff': '3+',
        'weapons': [{'name': 'Arcus Missile Launcher', 'range': '45cm', 'firepower': '2 x AT4+/AA5+'},
                    {'name': '3 x Heavy Bolter', 'range': '30cm', 'firepower': 'AP5+'}],
        'notes': 'Reinforced Armour'}, {
        'name': 'Legion Tarantula', 'type': 'LV', 'speed': 'Immobile', 'armour': '6+', 'cc': '6+', 'ff': '5+',
        'weapons': [{'name': 'TL Lascannon OR', 'range': '45cm', 'firepower': 'AT4+'},
                    {'name': 'TL Heavy Bolter', 'range': '30cm', 'firepower': 'AP4+'}],
        'notes': 'Teleport, Scout. A Legion Tarantula must select either a TL Lascannon OR TL Heavy Bolter before the '
                 'start of the game.'}, {
        'name': 'Legion Tarantula Hyperios', 'type': 'LV', 'speed': 'Immobile', 'armour': '6+', 'cc': '6+', 'ff': '5+',
        'weapons': [{'name': 'Missile Rack', 'range': '30cm', 'firepower': 'AA4+'}],
        'notes': 'Teleport, Scout.'}, {
        'name': 'Ascalon', 'type': 'WE', 'speed': '25cm', 'armour': '4+', 'cc': '5+', 'ff': '4+',
        'weapons': [{'name': 'Ascalon Inferno Gun', 'range': '30cm AND (15cm)',
                     'firepower': '2 x AP3+/AT6+, Ignore Cover AND (small arms) Ignore Cover'}],
        'notes': 'DC3, Reinforced Armour, Thick Rear Armour. Critical Hit: Unit is destroyed and all units within 5cm '
                 'suffer a standard hit on a 6+'}, {
        'name': 'Araknae Weapons Platform', 'type': 'LV', 'speed': 'Immobile', 'armour': '5+', 'cc': '6+', 'ff': '5+',
        'weapons': [{'name': 'Quad Accelerator Autocannon OR', 'range': '45cm', 'firepower': '3 x AP4+/AT5+'},
                    {'name': 'Twin Punisher Cannon OR', 'range': '30cm', 'firepower': '4 x AP3+/AT6+/AA5+'},
                    {'name': 'Orias Heavy Frag Missiles', 'range': '45cm', 'firepower': '2 BP, Indirect Fire, Single Shot'}],
        'notes': 'Invulnerable Save. An Araknae Weapons Platform must select one weapon system before the start of '
                 'the game.'}, {
        'name': 'Saturnine Terminators', 'type': 'INF', 'speed': '15cm', 'armour': '4+', 'cc': '4+', 'ff': '3+',
        'weapons': [{'name': 'Plasma Bombards OR', 'range': '30cm', 'firepower': 'AP4+/AT5+, Indirect Fire'},
                    {'name': 'Twin Heavy Disintegrators OR', 'range': '15cm', 'firepower': 'AP4+/AT4+, MW'},
                    {'name': 'Disruption Fists', 'range': '(base contact)', 'firepower': '(assault weapons) MW, EA(+1)'}],
        'notes': 'Reinforced Armour, Thick Rear Armour, Invulnerable Save. A Saturnine Terminator unit must select two '
                 'weapons (the same one twice, or two different ones) before the start of the game.'}, {
        'name': 'Saturnine Dreadnought', 'type': 'AV', 'speed': '15cm', 'armour': '3+', 'cc': '5+', 'ff': '4+',
        'weapons': [{'name': 'Heavy Plasma Bombard OR', 'range': '30cm', 'firepower': '2 x AP4+/AT5+, Indirect Fire'},
                    {'name': 'Graviton Pulveriser', 'range': '15cm', 'firepower': 'AP3+/AT4+, Disrupt'},
                    {'name': 'Inversion Beamer', 'range': '30cm', 'firepower': 'AP5+/AT4+'}],
        'notes': 'Invulnerable Save, Walker, Reinforced Armour. A Saturnine Dreadnought must select either a Heavy '
                 'Plasma Bombard OR Graviton Pulveriser before the start of the game.'}, {
        'name': 'Termite Assault Drill', 'type': 'AV', 'speed': '15cm', 'armour': '5+', 'cc': '6+', 'ff': '5+',
        'weapons': [{'name': 'Twin-linked Bolters', 'range': '(15cm)', 'firepower': '(small arms)'}],
        'notes': 'Transport: May carry 2 of the following units Tactical, Breacher, Assault OR 1 Terminator. A '
                 'formation transported entirely in Termites may deploy as if it had the Teleport special rule.'}],
    'Solar Auxilia': [{
        'name': 'Imperial Navy Marauder Bomber', 'type': 'AC', 'speed': 'Bomber', 'armour': '4+', 'cc': '', 'ff': '',
        'weapons': [{'name': 'Twin Lascannon', 'range': '45cm', 'firepower': 'AT4+/AA4+, FxF'},
                    {'name': 'Bomb Racks', 'range': '15cm', 'firepower': '3 BP, FxF'},
                    {'name': '2 x Twin Heavy Bolter', 'range': '15cm', 'firepower': 'AA5+'}],
        'notes': ''}, {
        'name': 'Imperial Navy Thunderbolt Fighter', 'type': 'AC', 'speed': 'Fighter-Bomber', 'armour': '6+',
        'cc': '', 'ff': '',
        'weapons': [{'name': 'Multilaser', 'range': '30cm', 'firepower': 'AP5+/AT6+/AA5+, FxF'},
                    {'name': 'Underwing Rockets', 'range': '30cm', 'firepower': 'AT4+, FxF'},
                    {'name': 'Storm Bolters', 'range': '15cm', 'firepower': 'AP4+/AA5+, FxF'}],
        'notes': ''}, {
        'name': 'Imperial Navy Marauder Destroyer', 'type': 'AC', 'speed': 'Bomber', 'armour': '3+', 'cc': '', 'ff': '',
        'weapons': [{'name': 'Twin Heavy Bolter', 'range': '15cm', 'firepower': 'AA5+'},
                    {'name': 'Twin Assault Cannon', 'range': '15cm', 'firepower': 'AA4+, Rear Arc'},
                    {'name': '3 x Twin Autocannon', 'range': '45cm', 'firepower': 'AP4+/AT5+, FxF'},
                    {'name': '2 x Underwing Rockets', 'range': '30cm', 'firepower': 'AT4+, FxF'}],
        'notes': ''}, {
        'name': 'Imperial Navy Marauder Colossus', 'type': 'AC', 'speed': 'Bomber', 'armour': '4+', 'cc': '', 'ff': '',
        'weapons': [{'name': 'Colossus Bomb', 'range': '15cm', 'firepower': '3 BP, MW, Single Shot, FxF'},
                    {'name': 'Hellstrike Missiles', 'range': '30cm', 'firepower': 'AT4+, FxF'},
                    {'name': '2 x Twin Heavy Bolter', 'range': '15cm', 'firepower': 'AA5+'}],
        'notes': ''}, {
        'name': 'Imperial Navy Marauder Pathfinder', 'type': 'AC', 'speed': 'Bomber', 'armour': '4+', 'cc': '',
        'ff': '',
        'weapons': [{'name': '2 x Hellstrike Missiles', 'range': '30cm', 'firepower': 'AT4+, FxF'},
                    {'name': '2 x Twin Heavy Bolter', 'range': '15cm', 'firepower': 'AA5+'}],
        'notes': 'Auger Array: friendly formations making Indirect Fire attacks against an enemy formation within '
                 '30cm of a Marauder Pathfinder on the table get the +1 to hit for Sustained Fire.'}, {
        'name': 'Malcador Annihilator', 'type': 'AV', 'speed': '15cm', 'armour': '4+', 'cc': '6+', 'ff': '5+',
        'weapons': [{'name': 'Twin Lascannon', 'range': '45cm', 'firepower': 'AT4+'},
                    {'name': '2 x Lascannon', 'range': '45cm', 'firepower': 'AT5+'},
                    {'name': 'Demolisher Cannon', 'range': '30cm AND (15cm)',
                     'firepower': 'AP3+/AT4+, Disrupt, Ignore Cover AND (small arms) Ignore Cover'}],
        'notes': 'Reinforced Armour, Thick Rear Armour.'}, {
        'name': 'Malcador Vanquisher', 'type': 'AV', 'speed': '15cm', 'armour': '4+', 'cc': '6+', 'ff': '5+',
        'weapons': [{'name': 'Vanquisher Cannon', 'range': '75cm', 'firepower': 'AP4+/AT2+'},
                    {'name': '2 x Autocannons', 'range': '45cm', 'firepower': 'AP5+/AT6+'},
                    {'name': 'Heavy Bolter', 'range': '30cm', 'firepower': 'AP5+'}],
        'notes': 'Reinforced Armour, Thick Rear Armour.'}, {
        'name': 'Leman Russ Annihilator', 'type': 'AV', 'speed': '25cm', 'armour': '4+', 'cc': '6+', 'ff': '5+',
        'weapons': [{'name': 'Annihilator Twin Lascannon', 'range': '45cm', 'firepower': 'AT3+'},
                    {'name': 'Lascannon', 'range': '45cm', 'firepower': 'AT5+'}],
        'notes': 'Reinforced Armour.'}, {
        'name': 'Hellhammer', 'type': 'WE', 'speed': '15cm', 'armour': '4+', 'cc': '6+', 'ff': '4+',
        'weapons': [{'name': '3 x TL Heavy Bolters', 'range': '30cm', 'firepower': 'AP4+'},
                    {'name': 'Autocannon', 'range': '45cm', 'firepower': 'AP5+/AT6+'},
                    {'name': '2 x Lascannon', 'range': '45cm', 'firepower': 'AT5+'},
                    {'name': 'Hellhammer Cannon', 'range': '45cm', 'firepower': 'AP3+/AT3+, Ignore Cover'},
                    {'name': 'Demolisher Cannon', 'range': '30cm',
                     'firepower': 'AP3+/AT4+ Ignore Cover AND (small arms) Ignore Cover, FxF'}],
        'notes': 'DC 3, Reinforced Armour. Critical Hit: The unit is destroyed. All units within 5cm take a standard '
                 'hit on a 6+.'}, {
        'name': 'Aethon Heavy Sentinel', 'type': 'LV', 'speed': '20cm', 'armour': '5+', 'cc': '6+', 'ff': '5+',
        'weapons': [{'name': 'Multilaser', 'range': '30cm', 'firepower': 'AP5+/AT6+'},
                    {'name': 'Sentinel Missile Launcher', 'range': '45cm', 'firepower': 'AP5+/AT6+'}],
        'notes': 'Scout, Walker.'}, {
        'name': 'Cyclops Demolition Vehicle', 'type': 'LV', 'speed': '25cm', 'armour': '6+', 'cc': '6+', 'ff': '-',
        'weapons': [{'name': 'Demolition Charge OR', 'range': '5cm', 'firepower': '1 BP, MW, Single Shot'},
                    {'name': 'Incineration Charge', 'range': '5cm', 'firepower': '1 BP, Ignore Cover, Single Shot'}],
        'notes': 'Remote Detonation: a Cyclops may only fire its charge while within 30cm of a friendly Leader, '
                 'Commander or Supreme Commander, and is destroyed once it has fired. A Cyclops must select either a '
                 'Demolition Charge OR Incineration Charge before the start of the game.'}],
    'Mechanicum Taghmata': [{
        'name': 'Arlatax Battle-Automata', 'type': 'AV', 'speed': '20cm', 'armour': '3+', 'cc': '3+', 'ff': '5+',
        'weapons': [{'name': 'Autocannon OR', 'range': '45cm', 'firepower': 'AP5+/AT6+'},
                    {'name': 'Plasma Cannon', 'range': '30cm', 'firepower': 'AP4+/AT5+'},
                    {'name': 'Power Claws', 'range': '(base contact)', 'firepower': '(assault weapons) EA(+1), MW'}],
        'notes': 'Cybernetica Cortex, Fearless, Invulnerable Save, Jump Packs. Dread Aura: enemy formations within '
                 '15cm subtract 1 from their rally tests. An Arlatax must select either an Autocannon OR a Plasma '
                 'Cannon before the start of the game.'}, {
        'name': 'Domitar Battle-Automata', 'type': 'AV', 'speed': '15cm', 'armour': '3+', 'cc': '4+', 'ff': '5+',
        'weapons': [{'name': 'Domitar Missile Launcher', 'range': '45cm', 'firepower': 'AP5+/AT5+'},
                    {'name': 'Graviton Hammers', 'range': '(base contact)', 'firepower': '(assault weapons) EA(+1), MW'}],
        'notes': 'Cybernetica Cortex, Fearless, Invulnerable Save, Walker. Dread Aura: enemy formations within 15cm '
                 'subtract 1 from their rally tests.'}, {
        'name': 'Krios Venator', 'type': 'AV', 'speed': '25cm', 'armour': '4+', 'cc': '6+', 'ff': '4+',
        'weapons': [{'name': 'Pulsar Fusil', 'range': '30cm', 'firepower': 'AP5+/AT3+'},
                    {'name': 'Volkite Caliver Sponsons', 'range': '15cm', 'firepower': 'AP5+, Disrupt'}],
        'notes': 'Invulnerable Save, Reinforced Armour, Walker.'}, {
        'name': 'Archmagos Prime on Abeyant', 'type': 'AV', 'speed': '15cm', 'armour': '4+', 'cc': '4+', 'ff': '5+',
        'weapons': [{'name': 'Meltagun', 'range': '15cm', 'firepower': 'MW5+'},
                    {'name': 'Power Weapons', 'range': '(base contact)', 'firepower': '(assault weapons) EA(+1), MW'}],
        'notes': 'Supreme Commander, Reinforced Armour, Invulnerable Save, Cortex Controller.'}, {
        'name': 'Scintillax', 'type': 'AV', 'speed': '20cm', 'armour': '4+', 'cc': '4+', 'ff': '5+',
        'weapons': [{'name': 'Scintillax Lascutter', 'range': '(base contact)', 'firepower': '(assault weapons) EA(+1), MW'},
                    {'name': 'Exo-planar Cannon OR', 'range': '15cm', 'firepower': 'AP4+, Ignore Cover'},
                    {'name': 'Storm Laser', 'range': '30cm', 'firepower': 'AP5+/AT5+'}],
        'notes': 'Invulnerable Save, Walker, Cortex Controller, Leader. A Scintillax must select either an Exo-planar '
                 'Cannon OR a Storm Laser before the start of the game.'}, {
        'name': 'Errax', 'type': 'AV', 'speed': '25cm', 'armour': '4+', 'cc': '3+', 'ff': '5+',
        'weapons': [{'name': 'Errax Lascutters OR', 'range': '(base contact)', 'firepower': '(assault weapons) MW'},
                    {'name': 'Errax Meltagun', 'range': '15cm', 'firepower': 'MW5+'},
                    {'name': 'Stalker Maxima Bolters', 'range': '15cm', 'firepower': 'AP4+'}],
        'notes': 'Cybernetica Cortex, Fearless, Invulnerable Save, Walker. An Errax must select either Errax '
                 'Lascutters OR an Errax Meltagun before the start of the game.'}, {
        'name': 'Tenebrax', 'type': 'LV', 'speed': '25cm', 'armour': '4+', 'cc': '6+', 'ff': '5+',
        'weapons': [{'name': 'Storm Laser Flenser', 'range': '45cm', 'firepower': 'AP4+/AT5+'},
                    {'name': 'Stalker Volkite Culverins OR', 'range': '30cm', 'firepower': 'AP4+, Disrupt'},
                    {'name': 'Exo-planar Cannon OR', 'range': '15cm', 'firepower': 'AP4+, Ignore Cover'},
                    {'name': 'Stalker Maxima Bolters', 'range': '15cm', 'firepower': 'AP4+'}],
        'notes': 'Cybernetica Cortex, Fearless, Walker. A Tenebrax must select Stalker Volkite Culverins OR an Exo-planar '
                 'Cannon OR Stalker Maxima Bolters before the start of the game.'}, {
        'name': 'Serperos', 'type': 'WE', 'speed': '20cm', 'armour': '3+', 'cc': '4+', 'ff': '4+',
        'weapons': [{'name': 'Storm Laser Array OR', 'range': '30cm', 'firepower': '2 x AP4+/AT5+'},
                    {'name': 'Exo-planar Bombard', 'range': '30cm', 'firepower': '2 x AP4+, Ignore Cover'},
                    {'name': 'Serperos Lascutters OR', 'range': '(base contact)',
                     'firepower': '(assault weapons) EA(+1), MW'},
                    {'name': 'Irradiation Engine', 'range': '15cm', 'firepower': 'MW4+, Ignore Cover'}],
        'notes': 'DC2, 1 Void Shield, Cybernetica Cortex, Fearless, Reinforced Armour, Walker. Construct Shield: its '
                 'Void Shield is never repaired, in the end phase or by a regroup. A Serperos must select a Storm Laser '
                 'Array OR an Exo-planar Bombard, and Serperos Lascutters OR an Irradiation Engine, before the start '
                 'of the game. Critical Hit: Unit is destroyed.'}, {
        'name': 'Harpax', 'type': 'INF', 'speed': '30cm', 'armour': '6+', 'cc': '6+', 'ff': '5+',
        'weapons': [{'name': 'Exo-planar Repeaters OR', 'range': '15cm', 'firepower': 'AP5+, Ignore Cover'},
                    {'name': 'Harpax Lascutters', 'range': '(base contact)', 'firepower': '(assault weapons) MW'}],
        'notes': 'Jump Packs, Scout. A Harpax unit must select either Exo-planar Repeaters OR Harpax Lascutters '
                 'before the start of the game.'}],
    'Knight Household': [{
        'name': 'Acastus Knight Asterius', 'type': 'WE', 'speed': '20cm', 'armour': '4+', 'cc': '6+', 'ff': '4+',
        'weapons': [{'name': '2 x Conversion Beam Cannon', 'range': '75cm', 'firepower': 'MW3+'},
                    {'name': 'Volkite Culverin', 'range': '45cm', 'firepower': 'AP4+, Disrupt'},
                    {'name': 'Karacnos Mortar Battery', 'range': '45cm', 'firepower': 'BP 1, Ignore Cover, Fleshbane'}],
        'notes': 'DC3, Ion Shield, Reinforced Armour, Walker. Ionic Flare Shield: its Ion Shield saves are 1 better '
                 'against Barrage hits, to a maximum of 2+. Critical hit effect: Destroyed.'}, {
        'name': 'Knight Moirax', 'type': 'LV', 'speed': '30cm', 'armour': '5+', 'cc': '4+ / 5+', 'ff': '5+',
        'weapons': [{'name': 'Volkite Veuglair', 'range': '30cm', 'firepower': 'AP4+/AT6+, Disrupt'},
                    {'name': 'Gyges Siege Claw OR', 'range': '(base contact)',
                     'firepower': '(assault weapons) MW, EA(+1), TK(1)'},
                    {'name': 'Armiger Lightning Locks', 'range': '30cm', 'firepower': '2 x AP4+/AT5+'}],
        'notes': 'Ion Shield (5+), Scout, Walker. Ionic Flare Shield: its Ion Shield saves are 1 better against '
                 'Barrage hits, to a maximum of 2+. A Knight Moirax must select either a Volkite Veuglair and Gyges '
                 'Siege Claw OR Armiger Lightning Locks before the start of the game.'}],
    'Legio Titanicus': [{
        'name': 'Warbringer Nemesis Titan', 'type': 'WE', 'speed': '20cm', 'armour': '4+', 'cc': '3+', 'ff': '3+',
        'weapons': [{'name': 'Quake Cannon OR Volcano Cannon', 'range': '-', 'firepower': '1 x Carapace, Fixed Forward'},
                    {'name': '2 x Scout or Battle Titan Weapon Variants', 'range': '-', 'firepower': '2 x Arm, Forward Arc'},
                    {'name': 'Carapace AA Guns', 'range': '45cm', 'firepower': '4 x AA5+'}],
        'notes': f'DC 6, 6 Void Shields, Fearless, Reinforced Armour, Walker, Cortex Controller. {TITAN_STEP} {TITAN_CRIT}'}, {
        'name': 'Warmaster Heavy Battle Titan', 'type': 'WE', 'speed': '15cm', 'armour': '4+', 'cc': '3+', 'ff': '3+',
        'weapons': [{'name': '4 x Revelator Missile', 'range': '60cm', 'firepower': '1 BP, Single Shot, Fixed Forward'},
                    {'name': '2 x Suzerain Plasma Destructor', 'range': '60cm',
                     'firepower': '4 x MW3+, Slow Firing, Forward Arc'},
                    {'name': 'Carapace AA Guns', 'range': '45cm', 'firepower': '4 x AA5+'},
                    {'name': '1 x Scout or Battle Titan Weapon Variant', 'range': '-',
                     'firepower': '1 x Carapace, Fixed Forward'}],
        'notes': f'DC 10, 7 Void Shields, Fearless, Reinforced Armour, Walker, Cortex Controller. {TITAN_STEP} '
                 f'{TITAN_CRIT}'}, {
        'name': 'Dire Wolf Heavy Scout Titan', 'type': 'WE', 'speed': '30cm', 'armour': '5+', 'cc': '4+', 'ff': '4+',
        'weapons': [{'name': 'Ardex Mega-Bolters', 'range': '30cm', 'firepower': '4 x AP4+/AT6+'},
                    {'name': 'Volcano Cannon OR Neutron Laser OR Conversion Beam Dissipator', 'range': '-', 'firepower': '1 x Carapace, Fixed Forward'}],
        'notes': 'DC 3, 2 Void Shields, Fearless, Reinforced Armour, Walker, Cortex Controller, Infiltrator. '
                 f'{TITAN_STEP} {WARHOUND_CRIT}'}, {
        'name': 'Warlord-Sinister Battle Titan', 'type': 'WE', 'speed': '15cm', 'armour': '4+', 'cc': '2+', 'ff': '3+',
        'weapons': [{'name': 'Sinistramanus Tenebrae', 'range': '75cm', 'firepower': '3 x MW3+, TK(1), Fwd'},
                    {'name': 'Antipathic Tempest', 'range': '45cm', 'firepower': '2 BP, Ignore Cover, Disrupt'},
                    {'name': 'Death Pulse', 'range': '(15cm)', 'firepower': '(small arms), EA(+2)'}],
        'notes': 'DC 8, 6 Void Shields, Fearless, Reinforced Armour, Walker, Cortex Controller. Dread Aura: enemy '
                 'formations within 15cm subtract 1 from their rally tests. A Psi-Titan for Loyalist Legions only. '
                 f'{TITAN_STEP} {TITAN_CRIT}'}, {
        'name': 'Warmaster Iconoclast Titan', 'type': 'WE', 'speed': '20cm', 'armour': '4+', 'cc': '3+', 'ff': '3+',
        'weapons': [{'name': 'Desolator Chainsword', 'range': '(base contact)',
                     'firepower': '(assault weapons) EA(+3), TK(D3)'},
                    {'name': 'Cruciator Gatling Array', 'range': '45cm', 'firepower': '6 x AP4+/AT5+, Fwd'},
                    {'name': 'Kirus Siege Drill OR Kirus Grav Imploder', 'range': '-', 'firepower': '1 x Arm'}],
        'notes': 'DC 10, 7 Void Shields, Fearless, Reinforced Armour, Walker, Cortex Controller. '
                 f'{TITAN_STEP} {TITAN_CRIT}'}],
}
# Fan-made Titan weapons for the Titans above, converted from Legions Imperialis against EpicAU's Titan weapons.
FAN_TITAN_WEAPONS = {
    'Neutron Laser': {'name': 'Neutron Laser', 'range': '60cm', 'firepower': 'MW3+, Disrupt', 'notes': ''},
    'Conversion Beam Dissipator': {'name': 'Conversion Beam Dissipator', 'range': '60cm', 'firepower': '3 x MW3+',
                                   'notes': 'Within 15cm it fires 2 x AP4+/AT4+ instead.'},
    'Kirus Siege Drill': {'name': 'Kirus Siege Drill', 'range': '(base contact)',
                          'firepower': '(assault weapons) EA(+2), TK(D6), Siege', 'notes': ''},
    'Kirus Grav Imploder': {'name': 'Kirus Grav Imploder', 'range': '15cm AND (base contact)',
                            'firepower': '2 x MW3+, Disrupt, Ignore Cover AND (assault weapons) EA(+1), TK(D3)', 'notes': ''},
}


# Fan-made units (not on the EpicAU wiki or Departmento Munitorum). They, and fan-made formations and upgrades, show
# an asterisk after their names.
FAN_UNITS = {'Kratos Heavy Tank', 'Sicaran Punisher', 'Sicaran Arcus', 'Legion Tarantula', 'Legion Tarantula Hyperios',
             'Ascalon', 'Araknae Weapons Platform', 'Saturnine Terminators', 'Saturnine Dreadnought',
             'Termite Assault Drill', 'Warbringer Nemesis Titan', 'Warmaster Heavy Battle Titan',
             'Dire Wolf Heavy Scout Titan', 'Warlord-Sinister Battle Titan', 'Warmaster Iconoclast Titan',
             'Imperial Navy Marauder Bomber', 'Imperial Navy Thunderbolt Fighter', 'Imperial Navy Marauder Destroyer',
             'Imperial Navy Marauder Colossus', 'Imperial Navy Marauder Pathfinder', 'Malcador Annihilator',
             'Malcador Vanquisher', 'Leman Russ Annihilator', 'Hellhammer', 'Aethon Heavy Sentinel',
             'Cyclops Demolition Vehicle', 'Scintillax', 'Errax', 'Tenebrax', 'Serperos', 'Harpax',
             'Arlatax Battle-Automata', 'Domitar Battle-Automata', 'Krios Venator', 'Archmagos Prime on Abeyant',
             'Acastus Knight Asterius', 'Knight Moirax'}


def star(name, fan):
    return f'{name}*' if fan and not name.endswith('*') else name


# ------------------------------------------------------------------ XML helpers
class X:
    """Tiny XML element builder."""

    def __init__(self, tag, attrs=None, children=None, text=None):
        self.tag, self.attrs, self.children, self.text = tag, attrs or {}, children or [], text

    def add(self, *kids):
        self.children.extend(k for k in kids if k is not None)
        return self

    def render(self, ind=0):
        sp = '  ' * ind
        attrs = ''.join(f' {k}={quoteattr(str(v))}' for k, v in self.attrs.items() if v is not None)
        if self.text is not None:
            return f'{sp}<{self.tag}{attrs}>{escape(self.text)}</{self.tag}>'
        kids = [c for c in self.children if c is not None and not (isinstance(c, X) and c.empty_list())]
        if not kids:
            return f'{sp}<{self.tag}{attrs}/>'
        inner = '\n'.join(c.render(ind + 1) for c in kids)
        return f'{sp}<{self.tag}{attrs}>\n{inner}\n{sp}</{self.tag}>'

    def iter_tag(self, tag):
        for c in self.children:
            if isinstance(c, X):
                if c.tag == tag:
                    yield c
                yield from c.iter_tag(tag)

    def list_child(self, tag, first=False):
        """The child list element `tag`, created (first, or last) if missing."""
        for c in self.children:
            if isinstance(c, X) and c.tag == tag:
                return c
        el = X(tag)
        self.children.insert(0, el) if first else self.children.append(el)
        return el

    def empty_list(self):
        return self.tag.endswith('s') and self.tag not in ('characteristics',) and not self.children and \
            not self.attrs and self.text is None and self.tag in LIST_TAGS


LIST_TAGS = {'modifiers', 'constraints', 'profiles', 'rules', 'infoLinks', 'categoryLinks', 'selectionEntries',
             'selectionEntryGroups', 'entryLinks', 'costs', 'repeats', 'conditions', 'conditionGroups',
             'characteristics', 'forceEntries', 'sharedSelectionEntries', 'sharedProfiles', 'sharedRules',
             'catalogueLinks', 'categoryEntries', 'publications'}


def ordered(tag, attrs, **parts):
    """Build an element with child lists in schema order."""
    order = ['comment', 'readme', 'publications', 'costTypes', 'profileTypes', 'categoryEntries', 'forceEntries',
             'modifiers', 'constraints', 'profiles', 'rules', 'infoGroups', 'infoLinks', 'categoryLinks',
             'selectionEntries', 'selectionEntryGroups', 'entryLinks', 'costs', 'sharedSelectionEntries',
             'sharedSelectionEntryGroups', 'sharedRules', 'sharedProfiles', 'catalogueLinks']
    el = X(tag, attrs)
    # force entries put forceEntries after infoLinks; handled by caller passing key 'forceEntries_late'
    for key in order:
        if key in parts and parts[key] is not None:
            v = parts[key]
            el.add(v if isinstance(v, X) else X(key, children=list(v)) if isinstance(v, list) else X(key, text=v))
        if key == 'infoLinks' and parts.get('forceEntries_late'):
            el.add(X('forceEntries', children=parts['forceEntries_late']))
    return el


def cost(value):
    return X('costs', children=[X('cost', {'name': 'pts', 'typeId': PTS, 'value': fmt(value)})])


def fmt(v):
    s = f'{float(v):.4f}'.rstrip('0')
    return s + '0' if s.endswith('.') else s


def constraint(cid, ctype, value, scope='parent', field='selections', shared=True, child=False, forces=False,
               percent=False):
    return X('constraint', {'field': field, 'scope': scope, 'value': fmt(value), 'percentValue': str(percent).lower(),
                            'shared': str(shared).lower(), 'includeChildSelections': str(child).lower(),
                            'includeChildForces': str(forces).lower(), 'id': cid, 'type': ctype})


def repeat(child_id, value, scope, field='selections', round_up=False, child=False, forces=False):
    return X('repeat', {'field': field, 'scope': scope, 'value': fmt(value), 'percentValue': 'false', 'shared': 'true',
                        'includeChildSelections': str(child).lower(), 'includeChildForces': str(forces).lower(),
                        'childId': child_id, 'repeats': '1', 'roundUp': str(round_up).lower()})


def condition(ctype, child_id, value, scope, field='selections', child=False, forces=False):
    return X('condition', {'field': field, 'scope': scope, 'value': fmt(value), 'percentValue': 'false',
                           'shared': 'true', 'includeChildSelections': str(child).lower(),
                           'includeChildForces': str(forces).lower(), 'childId': child_id, 'type': ctype})


def rule_el(rid, name, desc):
    return X('rule', {'id': rid, 'name': name, 'hidden': 'false'}, [X('description', text=desc)])


def info_rule(owner, name):
    return X('infoLink', {'id': gid('il', owner, name), 'name': ACRONYMS.get(name, name), 'hidden': 'false',
                          'targetId': RULE_ID[name], 'type': 'rule'})


def cat_link(owner, cat, primary=False):
    return X('categoryLink', {'id': gid('cl', owner, cat), 'name': cat, 'hidden': 'false', 'targetId': CAT[cat],
                              'primary': str(primary).lower()})


def per_points_limit(owner, maxn, per, round_up, scope='roster'):
    """0-maxn per full `per` points (or per army when per is None)."""
    cid = gid('con', owner, 'limit')
    if per is None:
        return [], [constraint(cid, 'max', maxn, scope=scope, child=True, forces=True)]
    mod = X('modifier', {'type': 'increment', 'field': cid, 'value': fmt(maxn)},
            [X('repeats', children=[repeat('any', per, 'roster', field=PTS, round_up=round_up, child=True,
                                           forces=True)])])
    return [mod, points_limit_label(owner, maxn, per, round_up)], \
        [constraint(cid, 'max', 0, scope=scope, child=True, forces=True)]


LABEL_UP_TO = 20000  # roster size up to which an over-limit entry is labelled


def points_limit_label(owner, maxn, per, round_up):
    """Append the points limit to the entry's name while the roster is too small for its selections.

    BattleScribe's error names the entry but not the reason, so this puts the reason in the name. Allowed is
    maxn per full `per` pts (maxn per `per` pts or part thereof with round_up); one AND group per threshold.
    """
    groups = []
    for k in range(LABEL_UP_TO // per + 1):
        pts = condition('atMost', 'any', k * per, 'roster', field=PTS, child=True, forces=True) if round_up else \
            condition('lessThan', 'any', (k + 1) * per, 'roster', field=PTS, child=True, forces=True)
        sel = condition('greaterThan', owner, k * maxn, 'roster', child=True, forces=True)
        groups.append(X('conditionGroup', {'type': 'and'}, [X('conditions', children=[pts, sel])]))
    limit = f'{maxn} per {per} pts or part thereof' if round_up else f'0-{maxn} per full {per} pts'
    return X('modifier', {'type': 'append', 'field': 'name', 'value': f' (not enough points: {limit})'},
             [X('conditionGroups', children=[X('conditionGroup', {'type': 'or'},
                                               [X('conditionGroups', children=groups)])])])


# ------------------------------------------------------------------ units & profiles
UNITS = json.load(open(os.path.join(HERE, 'source', 'units.json')))
for sheet, extra in EXTRA_UNITS.items():
    UNITS[sheet].extend(extra)
TITAN_WEAPONS = json.load(open(os.path.join(HERE, 'source', 'titan_weapons.json')))
TITAN_WEAPONS.update(FAN_TITAN_WEAPONS)
# Rule keywords are capitalised on the wiki, so match case-sensitively to avoid hits like "transport capacity".
PATTERN_OVERRIDES = {'Scout': r'Scout(?! Titan)', 'Commander': r'(?<!Supreme )(?<!Lieutenant )(?<!Lord )Commander',
                     'Transport': r'Transport(?= ?[:.])'}
# A following capital is allowed so run-together text like "Ignore CoverAND" still matches.
RULE_PATTERNS = [(name, re.compile(r'(?<![A-Za-z])' + PATTERN_OVERRIDES.get(name, re.escape(name)) + r'(?![a-z])'))
                 for name in RULES]
ALIAS_PATTERNS = [(target, re.compile(r'(?<![A-Za-z])(?:' + pat + r')(?![a-z])')) for pat, target in ALIASES]
for _, target in ALIASES:
    assert target in RULES, f'alias target {target!r} has no rule'


def rules_in(text):
    found = [n for n, p in RULE_PATTERNS if p.search(text)]
    found += [t for t, p in ALIAS_PATTERNS if p.search(text) and t not in found]
    return list(dict.fromkeys(found))


OR_END = re.compile(r',?\s*\bOR$')


def weapon_row(w, option=False):
    """[name, range, firepower, notes] for a sheet weapon row; an option's row drops the "OR" the sheet ends each
    of its cells with."""
    fp, traits = split_firepower(w['firepower'])
    cells = [w['name'] or 'Weapons', w['range'], fp, traits]
    return [(OR_END.sub('', c) if option else c) or '-' for c in cells]


COUNT_RE = re.compile(r'^(\d+) ?x ?(.+)$')


def weapon_count(name):
    """'2 x Lascannons' -> (2, 'Lascannons')."""
    m = COUNT_RE.match(name)
    return (int(m.group(1)), m.group(2)) if m else (1, name)


def weapons_text(names):
    """The Weapons column: each weapon once with its total count, as 'Lascannons x2'."""
    counts = {}
    for name in names:
        n, base = weapon_count(name)
        counts[base] = counts.get(base, 0) + n
    return ', '.join(f'{base} x{n}' if n > 1 else base for base, n in counts.items())


def shown_weapons(unit):
    """The sheet's weapon rows worth a line in the profile ('AND' rows only join two lists of options)."""
    return [w for w in unit['weapons'] if (w['name'] or w['firepower']) and w['name'] not in ('-', 'AND')]


USED_OPTIONS = set()  # units in WEAPON_OPTIONS that were built


def unit_options(unit):
    """(weapon choice groups with each option's rows resolved, sheet rows the choices take out of the profile)."""
    groups = WEAPON_OPTIONS.get(unit['name'], [])
    if groups:
        USED_OPTIONS.add(unit['name'])
    sheet = {OR_END.sub('', w['name']): w for w in unit['weapons']}
    order = [w['name'] for w in unit['weapons']]
    replaced = REPLACED_ROWS.get(unit['name'], [])
    used = set(replaced)
    resolved = []
    for g in groups:
        options, at = [], []  # at: where the group's rows sit on the sheet
        for o in g['options']:
            rows = []
            for r in o['rows']:
                if isinstance(r, dict):
                    at += [order.index(n) for n in replaced]
                else:
                    if r not in sheet:
                        raise ValueError(f'{unit["name"]}: weapon option {r!r} is not a row on its sheet')
                    used.add(sheet[r]['name'])
                    at.append(order.index(sheet[r]['name']))
                    r = sheet[r]
                rows.append(weapon_row(r, option=True))
            options.append(dict(o, rows=rows))
        resolved.append(dict(g, options=options, at=min(at, default=len(order))))
    at = min((order.index(n) for n in replaced), default=len(order))
    for mount, count, weapons in TITAN_WEAPON_SLOTS.get(unit['name'], []):
        options = [titan_option(name, each, mount) for name, each in weapons
                   if TITAN_MOUNT.get(name, mount) == mount]
        resolved += [{'label': f'{mount} weapon' + (f' {i}' if count > 1 else ''), 'optional': False,
                      'options': options, 'at': at} for i in range(1, count + 1)]
    return resolved, used


TITAN_ARC = {'Arm': 'Fwd', 'Carapace': 'FxF'}  # arm weapons fire in the forward arc, carapace weapons fixed forward
# Titan weapons whose notes restrict them to one mount ('Arm mount only', 'carapace only')
TITAN_MOUNT = {name: m.group(1).capitalize() for name, w in TITAN_WEAPONS.items()
               for m in [re.search(r'\b(arm|carapace)(?: mount)? only', w['notes'], re.I)] if m}


def titan_option(name, each, mount):
    """A Titan weapon as a weapon-choice option; its notes get the mount's arc."""
    w = TITAN_WEAPONS[name]
    fp, traits = split_firepower(w['firepower'])
    notes = ', '.join(t for t in (traits, TITAN_ARC[mount]) if t)
    if w['notes']:
        notes += '. ' + w['notes'].rstrip('.') + '.'
    return {'label': star(name, name in FAN_TITAN_WEAPONS), 'rows': [[name, w['range'] or '-', fp or '-', notes]],
            'cost': each, 'ff': None, 'rules': rules_in(w['firepower'] + ' ' + w['notes'])}


def weapon_plan(unit):
    """(choice groups, fixed sheet rows, whether the fixed weapons' names are followed by chosen ones) for a unit.

    Each group gets a 'place' in the Weapons column: 'front' for optional picks, 'before' or 'after' the fixed
    weapons as on the sheet for required ones (always 'after' when there are no fixed weapons), and 'last' marks
    the group whose name ends the column. The schema has no prepend modifier, so a unit with picks in front of its
    fixed weapons leaves its Weapons cell empty and has every name appended in order."""
    groups, chosen = unit_options(unit)
    fixed = [w for w in shown_weapons(unit) if w['name'] not in chosen]  # chosen weapons are added on the unit
    start = unit['weapons'].index(fixed[0]) if fixed else None
    for g in groups:
        g['place'] = 'front' if g['optional'] else 'before' if fixed and g['at'] < start else 'after'
        g['last'] = False
    after = [g for g in groups if g['place'] == 'after']
    if after:
        after[-1]['last'] = True
    return groups, fixed, bool(after)


def is_rule_name(item):
    """True if a notes item is just the name of a shared rule (or an alias of one), which the unit links anyway."""
    return item in RULES or any(re.fullmatch(pat, item) for pat, _ in ALIASES)


def notes_rules(notes):
    """Split a unit's notes into {rule label: text} for the unit's own rules, leaving out the names of shared rules,
    which the unit links instead. Rule names with a value ('Ion Shield (5+)') go under Special Rules; a sentence
    labelled 'X: ...' becomes rule X, and the sentences after it that carry no label of their own continue it;
    weapon-option and transport-counting sentences get rules of their own."""
    rules, current = {}, None

    def add(label, text):
        text = text[:1].upper() + text[1:].rstrip('.') + '.'
        rules[label] = (rules[label] + ' ' if label in rules else '') + text

    for sentence in re.split(r'(?<=\.)\s+(?=[A-Z(])', notes.strip()):
        items = sentence.rstrip('.').split(', ')
        while items and len(items[0]) <= 28 and rules_in(items[0]) and ':' not in items[0]:
            item = items.pop(0).strip()
            if not is_rule_name(item):
                add('Special Rules', item)
            current = None
        rest = ', '.join(items).strip()
        lead = next((r for r in RULES if rest.startswith(r + ' ') and rest[len(r) + 1:][:1].isupper()), None)
        if lead:  # a rule name run into the next sentence ('Inspiring May have wings: ...')
            rest = rest[len(lead) + 1:]
        if not rest.strip(' -'):
            continue
        label = re.match(r'([A-Z][A-Za-z\- ]{0,30}?)\s*:\s*(.+)$', rest, re.S)
        if label and not label.group(1).startswith('May ') and len(label.group(1).split()) <= 4:
            current = ' '.join(w if w in ('and', 'of', 'the') else w[:1].upper() + w[1:]
                               for w in label.group(1).split())
            add(current, label.group(2))
        elif re.search(r'\b(select|choose|armed with|may take|may exchange)', rest, re.I):
            add('Weapon Options', rest)
        elif 'transport capacity' in rest:
            add('Transport Space', rest)
        elif rest.startswith('May step over'):
            add('Titan Movement', rest)
        elif current:
            add(current, rest)
        else:
            add('Special Rules', rest)
    # drop the brackets some sheets put round a whole rule ('Transport: (May carry ...)')
    return {k: v[1:].rstrip('.')[:-1].rstrip('.') + '.' if v.startswith('(') and v.rstrip('.').endswith(')') else v
            for k, v in rules.items()}


class Catalogue:
    """Collects shared profiles for one catalogue."""

    def __init__(self, scope):
        self.scope = scope
        self.profiles = {}  # pid -> X
        self.rules = {}  # rid -> X: a unit's own rules from its notes, and '<weapon> notes' rules
        self.notes_rule = {}  # profile id -> [(rule id, rule name)] of those rules

    def unit_profiles(self, unit):
        """Return ((profile id, name) for the unit and its fixed weapons, rule names, categories) for a unit record,
        registering its shared profiles."""
        uid = gid('prof', self.scope, unit['name'], 'unit')
        display = star(unit['name'], unit['name'] in FAN_UNITS)
        groups, fixed, followed = weapon_plan(unit)
        weapons = self.weapon_profiles([weapon_row(w) for w in fixed])
        if uid not in self.profiles:
            names = weapons_text([w['name'] or 'Weapons' for w in fixed])
            names = names + (',' if followed else '') if names else None if groups else '-'
            if any(g['place'] != 'after' for g in groups):  # appended after the picks in front of them instead
                names = None
            stats = [unit['type'], unit['speed'], unit['armour'], unit['cc'], unit['ff'], names]
            if is_war_engine(unit):
                dc, shields, crit, notes = war_engine_fields(unit['notes'])
                own = notes_rules(notes if notes != '-' else '')
                if len(crit) > WIDE_CELL_LIMIT:  # long critical hits get a rule of their own
                    own['Critical Hit'], crit = crit.rstrip('.') + '.', SEE_RULES
                self.profiles[uid] = profile(uid, display, PT_WAR_ENGINE, 'War Engine', WAR_ENGINE_CHARS,
                                             stats + [dc, shields, crit])
            else:
                own = notes_rules(unit['notes'] if unit['notes'] != '-' else '')
                self.profiles[uid] = profile(uid, display, PT_UNIT, 'Unit', UNIT_CHARS, stats)
            if unit['name'] in WEAPON_OPTIONS:  # the unit's weapon choices are picked on it instead
                own.pop('Weapon Options', None)
            self.notes_rule[uid] = []
            for label, desc in own.items():
                rid, rname = gid('rule', self.scope, unit['name'], label), f'{label} ({display})'
                if label == 'Titan Movement':  # the same for every Titan
                    rid, rname = gid('rule', self.scope, label), label
                self.rules[rid] = rule_el(rid, rname, desc)
                self.notes_rule[uid].append((rid, rname))
        text = unit['notes'] + ' ' + ' '.join(w['firepower'] for w in unit['weapons'])
        cats = []
        if unit['type'].startswith('CH'):
            cats.append('Character')
        if unit['type'] == 'SC':
            cats.append('Spacecraft')
        if 'Supreme Commander' in unit['notes']:
            cats.append('Supreme Commander')
        if 'Demi-God' in unit['notes']:
            cats.append('Primarch')
        return [(uid, display)] + weapons, rules_in(text), cats

    def weapon_profiles(self, rows):
        """(profile id, name) of the shared Weapon profile for each [name, range, firepower, notes] row; the count
        in a name ('2 x Lascannons') stays in the unit's Weapons column. A cell too long for the table goes to a
        '<weapon> notes' rule instead."""
        ids = []
        for row in rows:
            name, vals = weapon_count(row[0])[1], row[1:]
            wid = gid('prof', self.scope, 'weapon', name, *vals)
            if wid not in self.profiles:
                details = ' '.join(f'{c}: {v}' for c, v in zip(WEAPON_CHARS, vals) if len(v) > CELL_LIMIT)
                cells = [SEE_WEAPON_NOTES if len(v) > CELL_LIMIT else v for v in vals]
                self.profiles[wid] = profile(wid, name, PT_WEAPON, 'Weapon', WEAPON_CHARS, cells)
                if details:
                    rid = gid('rule', self.scope, 'weapon', name, *vals, 'notes')
                    self.rules[rid] = rule_el(rid, f'{name} notes', details)
                    self.notes_rule[wid] = [(rid, f'{name} notes')]
            ids.append((wid, name))
        return list(dict.fromkeys(ids))

    def info_links(self, owner, ids):
        """infoLinks to these profiles, then to the rules holding their notes."""
        return [X('infoLink', {'id': gid('il', owner, pid), 'name': name, 'hidden': 'false', 'targetId': pid,
                               'type': 'profile'}) for pid, name in ids] + \
            [X('infoLink', {'id': gid('il', owner, rid), 'name': rname, 'hidden': 'false', 'targetId': rid,
                            'type': 'rule'}) for p, _ in ids for rid, rname in self.notes_rule.get(p, [])]


def split_firepower(text):
    """'2 x AP3+/AT3+, Armourbane, FxF' -> ('2 x AP3+/AT3+', 'Armourbane, FxF')."""
    head, _, rest = text.partition(',')
    return head.strip(), rest.strip()


DC_RE = re.compile(r'\bDC ?\(?(\d+)\)?')
SHIELDS_RE = re.compile(r'(\d+) ?(?:x )?Void Shields?', re.I)
CRIT_RE = re.compile(r'Critical [Hh]it(?: [Ee]ffect)?\s*[:\-]?\s*(.*)$', re.S)


def is_war_engine(unit):
    return 'WE' in unit['type'] or bool(DC_RE.search(unit['notes']))


def war_engine_fields(notes):
    """Split a war engine's notes into (damage capacity, void shields, critical hit, remaining notes)."""
    dc, shields, crit = DC_RE.search(notes), SHIELDS_RE.search(notes), CRIT_RE.search(notes)
    rest = notes
    for m in (crit, shields, dc):
        if m:
            rest = rest[:m.start()] + ',' + rest[m.end():]
    rest = re.sub(r'\s*([,.])\s*(?:[,.]\s*)+', r'\1 ', rest)  # tidy separators left by the removals
    rest = re.sub(r'\s+', ' ', rest).strip(' ,.')
    crit = crit.group(1).strip() if crit else ''
    return (dc.group(1) if dc else '-', shields.group(1) if shields else '-',
            (crit[:1].upper() + crit[1:]) if crit else '-', (rest + ('.' if rest[-1].isalnum() else '')) if rest else '-')


def profile(pid, name, type_id, type_name, chars, vals):
    """A profile; an empty value shows '-', and None leaves the cell blank for weapon choices to fill."""
    return X('profile', {'id': pid, 'name': name, 'hidden': 'false', 'typeId': type_id, 'typeName': type_name}, [
        X('characteristics', children=[X('characteristic', {'name': c, 'typeId': gid('ct', type_name, c)},
                                         text='' if v is None else v or '-') for c, v in zip(chars, vals)])])


# ------------------------------------------------------------------ list -> XML
def part_units(parts):
    """Names of every unit a list of DSL parts can contain."""
    names = []
    for p in parts:
        if p['kind'] == 'unit':
            names.append(p['unit'])
        elif p['kind'] == 'or':
            for o in p['opts']:
                names += part_units(o['parts'])
        elif p['kind'] in ('mix', 'fill'):
            names += [u['unit'] for u in p['units']]
    return names


def transport_space(unit, scheme):
    """Transport space a unit takes under `scheme` (characters and vehicles other than Dreadnoughts take none)."""
    if unit['type'].startswith('CH') or not (unit['type'] == 'INF' or 'Dreadnought' in unit['name']):
        return 0
    bulky = bool(BULKY.search(unit['name']))
    if scheme == 'Transport units':
        return 1
    if scheme == 'Assault Claw space':
        return 4 if 'Dreadnought' in unit['name'] else 2 if bulky else 1
    return 2 if bulky else 1


def transport_schemes(army):
    """The transport-space schemes used by the list's transport upgrades."""
    def spaces(parts):
        for p in parts:
            if p['kind'] == 'fill':
                yield p['space']
            elif p['kind'] == 'or':
                for o in p['opts']:
                    yield from spaces(o['parts'])
    found = {s for u in army['upgrades'].values() for s in spaces(u['parts'])}
    return [s for s in TRANSPORT_SCHEMES if s in found]


def has_new(army):
    """True if the army list has fan-made formations or options behind the 'Allow fan-made units' toggle."""
    def parts_new(parts):
        for p in parts:
            if p.get('new') or (p['kind'] in ('mix', 'fill') and any(u.get('new') for u in p['units'])) or \
                    (p['kind'] == 'or' and any(parts_new(o['parts']) for o in p['opts'])):
                return True
        return False
    return any(f.get('new') or parts_new(f['units']) for f in army['formations'])


def swap_matches(frm, unit):
    return unit in frm if isinstance(frm, tuple) else unit == frm


def joined(kind, *parts):
    """One condition group of `kind` ('and'/'or') over several conditions/conditionGroups elements."""
    conds = [c for p in parts if p.tag == 'conditions' for c in p.children]
    groups = [g for p in parts if p.tag == 'conditionGroups' for g in p.children]
    kids = ([X('conditions', children=conds)] if conds else []) + ([X('conditionGroups', children=groups)] if groups else [])
    return X('conditionGroups', children=[X('conditionGroup', {'type': kind}, kids)])


def both(a, b):
    """Show pair (on, off) true only while both (on, off) pairs are on."""
    return joined('and', a[0], b[0]), joined('or', a[1], b[1])


class Builder:
    def __init__(self, army, cat_id, profiles, allied_force_id):
        self.army, self.cat_id, self.prof, self.allied_force_id = army, cat_id, profiles, allied_force_id
        self.missing = []
        self.formation_id = None  # set while a formation is being built (scope for transport counts)
        self.variants = None  # the formation's swap upgrade (e.g. Armoury Assets) while it is being built
        self.offered = set()  # units offered directly by the parts being built
        self.context = None  # name of the upgrade whose parts are being built (None = the formation's own units)
        self.schemes = transport_schemes(army)  # transport-space cost types this list's transports use
        self.retinue = {}  # scheme -> space taken by a Demi-God, which counts as its retinue's unit type
        self.primary_force_id = gid('force', cat_id, 'primary')

    def find_unit(self, name):
        for sheet in self.army['sheets']:
            for u in UNITS.get(sheet, []):
                if u['name'] == name:
                    return u
        self.missing.append(name)
        return {'name': name, 'type': '?', 'speed': '', 'armour': '', 'cc': '', 'ff': '', 'weapons': [],
                'notes': 'Unit not found on the reference sheet.'}

    # -- unit entries
    def unit_entry(self, path, part, name=None, mods=(), extra_cons=(), extra_cats=(), hidden=False):
        unit = self.find_unit(part['unit'])
        eid = gid('se', self.cat_id, path)
        ids, rules, cats = self.prof.unit_profiles(unit)
        space = self.army['transport_space']
        if space and (unit['name'] in space or 'Demi-God' in unit['notes']):
            cats = cats + ['Tactical Transport Space']
        cats = cats + list(extra_cats)
        cons = []
        if part['min'] is not None and part['min'] > 0:
            cons.append(constraint(gid('con', eid, 'min'), 'min', part['min']))
        if part['max'] is not None:
            cons.append(constraint(gid('con', eid, 'max'), 'max', part['max']))
        cons += list(extra_cons)
        links = self.prof.info_links(eid, ids)  # notes rules hold text too long for the profiles' cells
        links += [info_rule(eid, r) for r in rules]
        choices, groups = self.weapon_choices(eid, unit)
        if choices:
            links[0].add(X('modifiers', children=choices))
        return ordered('selectionEntry', {'id': eid, 'name': star(name or part['label'] or unit['name'],
                                                                   unit['name'] in FAN_UNITS),
                                          'hidden': str(hidden).lower(), 'collective': 'false', 'import': 'true',
                                          'type': 'model'},
                       modifiers=list(mods), constraints=cons, infoLinks=links,
                       categoryLinks=[cat_link(eid, c) for c in cats], selectionEntryGroups=groups,
                       costs=self.unit_costs(unit, part['each']))

    def weapon_choices(self, eid, unit):
        """(modifiers for the unit's profile link, choice groups) for a unit's weapon options: a chosen option adds
        its weapons' names to the Weapons column, where the sheet lists them, and its Weapon profiles show with the
        option; it may also set the unit's FF, armour and CC, or need an upgrade option in the formation. Names are joined by commas: New Recruit adds a space when it adds
        text, so each name but the column's last carries the comma that follows it."""
        groups, fixed, followed = weapon_plan(unit)
        type_name = 'War Engine' if is_war_engine(unit) else 'Unit'
        placed, grps = {'before': [], 'front': [], 'after': []}, []
        for i, g in enumerate(groups):
            mods = []
            placed[g['place']].append(mods)
            g_id = gid('seg', eid, 'weapons', i)
            kids = []
            for j, o in enumerate(g['options']):
                oid = gid('se', eid, 'weapons', i, j)
                links = self.prof.info_links(oid, self.prof.weapon_profiles(o['rows']))
                links += [info_rule(oid, r) for r in o.get('rules', [])]
                kids.append(ordered('selectionEntry', {'id': oid, 'name': o['label'], 'hidden': 'false',
                                                       'collective': 'false', 'import': 'true', 'type': 'upgrade'},
                                    constraints=[constraint(gid('con', oid, 'max'), 'max', 1)], infoLinks=links,
                                    costs=cost(o['cost'])))
                if o.get('requires'):
                    self.gate(kids[-1], show=self.upgrade_option_taken(*o['requires']), cmax=gid('con', oid, 'max'))
                taken = [X('conditions', children=[condition('atLeast', oid, 1, eid, child=True)])]
                text = weapons_text([row[0] for row in o['rows']]) or o['label']  # e.g. a Command Relay
                mods.append(X('modifier', {'type': 'append', 'field': gid('ct', type_name, 'Weapons'),
                                           'value': text + ('' if g['last'] else ',')}, taken))
                for stat, char in (('ff', 'FF'), ('armour', 'Armour'), ('cc', 'CC')):
                    if o.get(stat):
                        mods.append(X('modifier', {'type': 'set', 'field': gid('ct', type_name, char),
                                                   'value': o[stat]}, taken))
            cons = [constraint(gid('con', g_id, 'max'), 'max', 1)]
            attrs = {'id': g_id, 'name': g['label'], 'hidden': 'false', 'collective': 'false', 'import': 'true'}
            if not g['optional']:  # starts on the cheapest option
                cons.insert(0, constraint(gid('con', g_id, 'min'), 'min', 1))
                cheapest = min(range(len(kids)), key=lambda j: g['options'][j]['cost'])
                attrs['defaultSelectionEntryId'] = kids[cheapest].attrs['id']
            grps.append(ordered('selectionEntryGroup', attrs, constraints=cons, selectionEntries=kids))
        # Appended in column order: optional picks, picks before the fixed weapons, the fixed weapons, the rest.
        names = weapons_text([w['name'] or 'Weapons' for w in fixed])
        if (placed['front'] or placed['before']) and names:
            placed['before'].append([X('modifier', {'type': 'append', 'field': gid('ct', type_name, 'Weapons'),
                                                    'value': names + (',' if followed else '')})])
        mods = placed['front'] + placed['before'] + placed['after']
        return [m for group in mods for m in group], grps

    def upgrade_option_taken(self, upgrade, option):
        """(conditions when `option` of the shared `upgrade` is taken in the formation, conditions when it isn't),
        for a selection inside a formation that may take the upgrade."""
        choice = next(p for p in self.army['upgrades'][upgrade]['parts'] if p['kind'] == 'or')
        oid = gid('se', self.cat_id, f'upgrade/{upgrade}/0', [o['label'] for o in choice['opts']].index(option))
        fids = [gid('formation', self.cat_id, f['slot'], f['name'], *([f['key']] if f.get('key') else []))
                for f in self.army['formations']
                if upgrade in [n.strip() for c in f['up'].split(',') for n in c.split(' OR ')]]
        return tuple(X('conditionGroups', children=[X('conditionGroup', {'type': t}, [X('conditions', children=[
                         condition(c, oid, 1, fid, child=True) for fid in fids])])])
                     for t, c in (('or', 'atLeast'), ('and', 'lessThan')))

    def unit_costs(self, unit, each):
        """Points plus the transport space the unit takes under each scheme this list uses."""
        costs = cost(each)
        for scheme in self.schemes:
            space = self.retinue.get(scheme, 1) if 'Demi-God' in unit['notes'] else transport_space(unit, scheme)
            if space:
                costs.add(X('cost', {'name': scheme, 'typeId': COST_ID[scheme], 'value': fmt(space)}))
        return costs

    def parts(self, path, parts):
        """Convert DSL parts to (selectionEntries, selectionEntryGroups)."""
        ses, grps = [], []
        for i, p in enumerate(parts):
            pp = f'{path}/{i}'
            if p['kind'] == 'unit':
                ses += self.unit_with_variants(pp, p)
            elif p['kind'] == 'or':
                gid_ = gid('seg', self.cat_id, pp)
                opts = []
                for j, o in enumerate(p['opts']):
                    oid = gid('se', self.cat_id, pp, j)
                    s2, g2 = self.parts(f'{pp}/{j}', o['parts'])
                    fan = any(q.get('new') for q in o['parts'])
                    opts.append(ordered('selectionEntry', {'id': oid, 'name': star(o['label'], fan), 'hidden': 'false',
                                                           'collective': 'false', 'import': 'true', 'type': 'upgrade'},
                                        constraints=[constraint(gid('con', oid, 'max'), 'max', 1)],
                                        selectionEntries=s2, selectionEntryGroups=g2, costs=cost(o['cost'])))
                    if fan:  # fan-made options appear with 'Allow fan-made units'
                        self.gate(opts[-1], show=self.new_show(), cmax=gid('con', oid, 'max'))
                grps.append(ordered('selectionEntryGroup',
                                    {'id': gid_, 'name': p['label'], 'hidden': 'false', 'collective': 'false',
                                     'import': 'true', 'defaultSelectionEntryId': opts[0].attrs['id']},
                                    constraints=[constraint(gid('con', gid_, 'min'), 'min', 1),
                                                 constraint(gid('con', gid_, 'max'), 'max', 1)],
                                    selectionEntries=opts))
            elif p['kind'] == 'mix':
                gid_ = gid('seg', self.cat_id, pp)
                cons = []
                if p['min']:
                    cons.append(constraint(gid('con', gid_, 'min'), 'min', p['min']))
                if p['max'] is not None:
                    cons.append(constraint(gid('con', gid_, 'max'), 'max', p['max']))
                kids = [self.unit_entry(f'{pp}/{j}', dict(u, min=0)) for j, u in enumerate(p['units'])]
                for kid, u in zip(kids, p['units']):  # fan-made options appear with 'Allow fan-made units'
                    if u.get('new'):
                        self.gate(kid, show=self.new_show(), cmax=gid('con', kid.attrs['id'], 'max'),
                                  allowed=u['max'] if u['max'] is not None else p['max'])
                # Upgraded units count towards the group's total, so they replace originals one-for-one.
                seen = set()
                for j, u in enumerate(p['units']):
                    for to, each in self.variants_for(u['unit']):
                        if (to, u['each'] + each) in seen:  # one entry per upgraded unit, whichever unit it replaces
                            self.variants['made'].append((u['unit'], to, each, self.context))
                            continue
                        seen.add((to, u['each'] + each))
                        kids.append(self.variant_entry(f'{pp}/{j}', u, to, each))
                grps.append(ordered('selectionEntryGroup', {'id': gid_, 'name': p['label'], 'hidden': 'false',
                                                            'collective': 'false', 'import': 'true'},
                                    constraints=cons, selectionEntries=kids))
            elif p['kind'] == 'fill':
                grps.append(self.fill_group(pp, p))
        return ses, grps

    # -- swap upgrades: upgraded units sit beside the units they replace
    def variants_for(self, unit):
        """(to_unit, extra_cost) swaps the formation's swap upgrade allows for `unit` here."""
        if not self.variants:
            return []
        targets = {to for _, to, _ in self.variants['swaps']}
        return [(to, each) for frm, to, each in self.variants['swaps']
                if swap_matches(frm, unit) and unit not in targets and to not in self.offered]

    def variant_entry(self, path, base, to, each):
        """An upgraded copy of `base`, hidden and unavailable until the swap upgrade is taken."""
        v, fid = self.variants, self.formation_id
        cmax = gid('con', self.cat_id, path, 'variant-max', to)
        taken = [X('conditions', children=[condition('atLeast', v['uid'], 1, fid, child=True)])]
        mods = [X('modifier', {'type': 'set', 'field': 'hidden', 'value': 'false'}, taken),
                X('modifier', {'type': 'set', 'field': cmax, 'value': fmt(v['hi'] or 99)}, taken)]
        if v['hi']:
            mods.append(X('modifier', {'type': 'set', 'field': cmax, 'value': '0'},
                          [X('conditions', children=[condition('greaterThan', CAT['Upgraded Unit'], v['hi'], fid,
                                                               child=True)])]))
        v['made'].append((base['unit'], to, each, self.context))
        return self.unit_entry(path + '/variant/' + to, {'unit': to, 'min': 0, 'max': None,
                                                         'each': (base['each'] or 0) + each, 'label': None},
                               mods=mods, extra_cons=[constraint(cmax, 'max', 0)], extra_cats=['Upgraded Unit'],
                               hidden=True)

    def unit_with_variants(self, path, part):
        """A unit entry plus its upgraded versions; each upgrade taken lowers the original's count by one."""
        vs = self.variants_for(part['unit'])
        if not vs:
            return [self.unit_entry(path, part)]
        variants = [self.variant_entry(path, part, to, each) for to, each in vs]
        eid = gid('se', self.cat_id, path)
        mods = []
        for field, present in (('min', part['min'] is not None and part['min'] > 0), ('max', part['max'] is not None)):
            if present:
                mods += [X('modifier', {'type': 'decrement', 'field': gid('con', eid, field), 'value': '1'},
                           [X('repeats', children=[repeat(e.attrs['id'], 1, self.formation_id, child=True)])])
                         for e in variants]
        return [self.unit_entry(path, part, mods=mods)] + variants

    def variant_marker(self, uid, name, u):
        """The swap upgrade itself: counts towards the upgrade cap and requires lo..hi upgraded units."""
        v = self.variants
        cmax = gid('con', uid, 'max')
        mods = []
        if v['lo']:
            mods.append(X('modifier', {'type': 'set', 'field': cmax, 'value': '0'},
                          [X('conditions', children=[condition('lessThan', CAT['Upgraded Unit'], v['lo'],
                                                               self.formation_id, child=True)])]))
        v['desc'] = X('description', text='')
        return ordered('selectionEntry', {'id': uid, 'name': name, 'hidden': 'false', 'collective': 'false',
                                          'import': 'true', 'type': 'upgrade'},
                       modifiers=mods, constraints=[constraint(cmax, 'max', 1)],
                       rules=[X('rule', {'id': gid('r', uid), 'name': name, 'hidden': 'false'}, [v['desc']])],
                       infoLinks=[info_rule(uid, r) for r in u['rules']], costs=cost(u['cost']))

    def variant_text(self):
        v = self.variants
        n = (str(v['lo']) if v['lo'] == v['hi'] else f"{v['lo']}-{v['hi']}") if v['hi'] else f"{v['lo']} or more"
        froms = {}
        for frm, to, each, _ in v['made']:
            froms.setdefault((to, each), [])
            if frm not in froms[(to, each)]:
                froms[(to, each)].append(frm)
        swaps = [f"{' or '.join(fs)} to {to}" + (f' (+{each:g} pts each)' if each else '')
                 for (to, each), fs in froms.items()]
        where = list(dict.fromkeys('the formation' if c is None else f'the {c} upgrade' for *_, c in v['made']))
        where = where[0] if len(where) == 1 else ', '.join(where[:-1]) + ' and ' + where[-1]
        noun = 'unit' if n == '1' else 'units'
        return (v['base_desc'] + ' ' if v['base_desc'] else '') + f'Upgrade {n} {noun} in this formation: ' + \
            '; '.join(swaps) + f'. Once this upgrade is taken, the upgraded units appear in {where}, next to the ' \
            'units they replace; pick them there.'

    def fill_group(self, path, p):
        """Transports sized to the formation: min = max = ceil(tagged units / per), any mix of types."""
        if not self.formation_id:
            raise ValueError(f'{self.army["name"]}: transport fill outside a formation ({path})')
        g = gid('seg', self.cat_id, path)
        kids = [self.unit_entry(f'{path}/{j}', u) for j, u in enumerate(p['units'])]
        for j, u in enumerate(p['units']):  # swap upgrades (e.g. Land Raider to Achilles) count within the total
            kids += [self.variant_entry(f'{path}/{j}', u, to, each) for to, each in self.variants_for(u['unit'])]
        cmin, cmax = gid('con', g, 'min'), gid('con', g, 'max')
        if p['space'] in COST_ID:  # weighted transport space, summed over the formation
            counted = repeat('any', p['per'], self.formation_id, field=COST_ID[p['space']], round_up=True, child=True)
        else:  # one per unit tagged with the category
            counted = repeat(CAT[p['space']], p['per'], self.formation_id, round_up=True, child=True)
        mods = [X('modifier', {'type': 'increment', 'field': c, 'value': '1'}, [X('repeats', children=[counted])])
                for c in (cmin, cmax)]
        return ordered('selectionEntryGroup', {'id': g, 'name': p['label'], 'hidden': 'false', 'collective': 'false',
                                               'import': 'true', 'defaultSelectionEntryId': kids[0].attrs['id']},
                       modifiers=mods, constraints=[constraint(cmin, 'min', 0), constraint(cmax, 'max', 0)],
                       selectionEntries=kids)

    # -- upgrades
    @staticmethod
    def formation_bound(u):
        """Upgrades whose contents depend on the formation are built inline rather than shared."""
        return any(p['kind'] in ('fill', 'swap') or (p['kind'] == 'or' and Builder.formation_bound(
            {'parts': [q for o in p['opts'] for q in o['parts']]})) for p in u['parts'])

    @staticmethod
    def swap_part(u):
        return next((p for p in u['parts'] if p['kind'] == 'swap'), None)

    def carries_variants(self, u):
        """True if this upgrade adds units the formation's swap upgrade can upgrade."""
        if not self.variants or self.swap_part(u):
            return False
        names = part_units(u['parts'])
        saved, self.offered = self.offered, set(names)
        try:
            return any(self.variants_for(n) for n in names)
        finally:
            self.offered = saved

    def upgrade_entry(self, uid, name, u, path, extra_cons=()):
        saved = self.offered, self.context
        self.offered, self.context = set(part_units(u['parts'])), name
        ses, grps = self.parts(path, u['parts'])
        self.offered, self.context = saved
        mods, cons = ([], [])
        if u['maxn'] is not None:
            mods, cons = per_points_limit(uid, u['maxn'], u['per'], u['round_up'])
        cons = cons + list(extra_cons)
        name = star(name, u.get('new'))
        rules = [rule_el(gid('r', uid), name, u['desc'])] if u['desc'] else []
        return ordered('selectionEntry', {'id': uid, 'name': name, 'hidden': 'false', 'collective': 'false',
                                          'import': 'true', 'type': 'upgrade'},
                       modifiers=mods, constraints=cons, rules=rules,
                       infoLinks=[info_rule(uid, r) for r in u['rules']],
                       selectionEntries=ses, selectionEntryGroups=grps, costs=cost(u['cost']))

    def shared_upgrades(self):
        specs = [(name, None, u) for name, u in self.army['upgrades'].items()]
        specs += [(name, legions[0], u) for name, vs in self.army.get('upgrade_variants', {}).items()
                  for legions, u in vs]
        return [self.upgrade_entry(self.upgrade_id(name, key), name, u, f'upgrade/{name}' + (f'/{key}' if key else ''))
                for name, key, u in specs if not self.formation_bound(u)]

    def upgrade_id(self, name, key=None):
        return gid('upgrade', self.cat_id, name, *([key] if key else []))

    def upgrade_link(self, owner, name):
        """Links for an upgrade: the core version, plus any Legion versions shown only for their Legions."""
        if name not in self.army['upgrades']:
            raise KeyError(f'{self.army["name"]}: unknown upgrade {name!r} in {owner}')
        variants = self.army.get('upgrade_variants', {}).get(name, [])
        hide = [legion for legions, _ in variants for legion in legions]
        return [self.upgrade_link_one(owner, name, self.army['upgrades'][name], hide_for=hide)] + \
            [self.upgrade_link_one(owner, name, u, key=legions[0], show_for=legions) for legions, u in variants]

    def upgrade_link_one(self, owner, name, u, key=None, show_for=(), hide_for=()):
        """An entryLink to the shared upgrade, or an inline copy for formation-bound upgrades."""
        el = self.upgrade_link_el(owner + (f'/{key}' if key else ''), name, u, key)
        if u.get('new') and show_for:
            raise ValueError(f'{name}: a fan-made Legion upgrade would need both conditions together')
        show = self.new_show() if u.get('new') else self.legion_show(show_for)
        if show or hide_for:
            self.gate(el, show=show, hide=self.legion_hide(hide_for), cmax=gid('con', el.attrs['id'], 'max'))
        return el

    def upgrade_link_el(self, owner, name, u, key):
        if self.swap_part(u):
            if not self.variants or self.variants['name'] != name:
                raise ValueError(f'{self.army["name"]}: swap upgrade {name!r} must be a single upgrade in {owner}')
            return self.variant_marker(self.variants['uid'], name, u)
        if self.formation_bound(u) or self.carries_variants(u):
            uid = gid('upgrade', owner, name)
            return self.upgrade_entry(uid, name, u, f'{owner}/upgrade/{name}',
                                      extra_cons=[constraint(gid('con', uid, 'max'), 'max', 1)])
        lid = gid('el', owner, name)
        return X('entryLink', {'id': lid, 'name': star(name, u.get('new')), 'hidden': 'false', 'collective': 'false',
                               'import': 'true',
                               'targetId': self.upgrade_id(name, key), 'type': 'selectionEntry'},
                 [X('constraints', children=[constraint(gid('con', lid, 'max'), 'max', 1)])])

    @staticmethod
    def split(items):
        return [i for i in items if i.tag == 'selectionEntry'], [i for i in items if i.tag == 'entryLink']

    def upgrades_group(self, fid, f):
        cap = {'support': self.army['support_cap'], 'low': self.army['low_cap']}.get(f['slot'], self.army['upgrade_cap'])
        links, groups = [], []
        for chunk in [c.strip() for c in f['up'].split(',') if c.strip()]:
            names = [n.strip() for n in chunk.split(' OR ')]
            if len(names) == 1:
                links += self.upgrade_link(fid, names[0])
            else:
                sg = gid('seg', fid, chunk)
                ses, els = self.split([el for n in names for el in self.upgrade_link(sg, n)])
                label = ' / '.join(n for n in names if not self.army['upgrades'].get(n, {}).get('new'))  # fan-made hidden
                groups.append(ordered('selectionEntryGroup', {'id': sg, 'name': label, 'hidden': 'false',
                                                              'collective': 'false', 'import': 'true'},
                                      constraints=[constraint(gid('con', sg, 'max'), 'max', 1)],
                                      selectionEntries=ses, entryLinks=els))
        if not links and not groups:
            return None
        g = gid('seg', fid, 'upgrades')
        cons = [constraint(gid('con', g, 'max'), 'max', cap)] if cap else []
        ses, els = self.split(links)
        return ordered('selectionEntryGroup', {'id': g, 'name': 'Upgrades', 'hidden': 'false', 'collective': 'false',
                                               'import': 'true'},
                       constraints=cons, selectionEntries=ses, selectionEntryGroups=groups, entryLinks=els)

    # -- formations
    def formation(self, f):
        key = [f['key']] if f.get('key') else []  # Legion versions share names with core formations
        fid = gid('formation', self.cat_id, f['slot'], f['name'], *key)
        self.formation_id = fid
        primary = SLOT_CAT[f['slot']]
        cats = [cat_link(fid, primary, True)]
        if f['slot'] == 'low':
            cats.append(cat_link(fid, 'Allies & Lords of War'))
        if any(p['kind'] == 'or' and any('Battleship' in o['label'] or 'Cruiser' in o['label'] or 'Barge' in o['label']
                                         for o in p['opts']) for p in f['units']):
            cats.append(cat_link(fid, 'Spacecraft'))
        if f['name'] == 'Daemonic Overlord':
            cats.append(cat_link(fid, 'Supreme Commander'))
        mods, cons = [], []
        if f['maxn'] is not None:
            mods, cons = per_points_limit(fid, f['maxn'], f['per'], f['round_up'])
        # Formations bought for an allied contingent count towards the Allies & Lords of War allowance.
        if f['slot'] != 'low':
            mods.append(X('modifier', {'type': 'add', 'field': 'category', 'value': CAT['Allies & Lords of War']},
                          [X('conditions', children=[condition('instanceOf', self.allied_force_id, 1, 'force')])]))
        mods += self.ally_modifiers()
        if f['name'] == 'Daemonic Overlord':
            cid = gid('con', fid, 'required')
            cons.append(constraint(cid, 'min', 1, scope='force'))
            mods.append(X('modifier', {'type': 'set', 'field': cid, 'value': '0'},
                          [X('conditions', children=[condition('instanceOf', self.allied_force_id, 1, 'force')])]))
        rules = [rule_el(gid('r', fid), f['name'], f['note'])] if f['note'] else []
        self.variants = self.swap_context(fid, f)
        self.offered = set(part_units(f['units']))
        retinue = [self.find_unit(n) for n in part_units(f['units'])]
        self.retinue = {scheme: max([transport_space(r, scheme) for r in retinue if 'Demi-God' not in r['notes']] or [1])
                        for scheme in self.schemes}
        ses, grps = self.parts('/'.join(['formation', f['slot'], f['name']] + key), f['units'])
        up = self.upgrades_group(fid, f)
        extra = [el for n in f['extra_up'] for el in self.upgrade_link(fid + '/extra', n)]
        if self.variants:
            if not self.variants['made']:
                raise ValueError(f'{self.army["name"]}: {f["name"]} has nothing {self.variants["name"]} can upgrade')
            self.variants['desc'].text = self.variant_text()
        self.variants, self.offered = None, set()
        el = ordered('selectionEntry', {'id': fid, 'name': star(f['name'], f.get('new')), 'hidden': 'false',
                                        'collective': 'false',
                                        'import': 'true', 'type': 'unit'},
                     modifiers=mods, constraints=cons, rules=rules,
                     infoLinks=[info_rule(fid, r) for r in f['rules']], categoryLinks=cats,
                     selectionEntries=ses, selectionEntryGroups=grps + ([up] if up else []),
                     entryLinks=extra, costs=cost(f['cost']))
        show = self.new_show() if f.get('new') else None
        if f.get('show_for'):
            show = both(show, self.legion_show(f['show_for'])) if show else self.legion_show(f['show_for'])
        if show or f.get('hide_for'):
            self.gate(el, show=show, hide=self.legion_hide(f.get('hide_for')))
        return el

    # -- allies
    def in_primary(self):
        return X('conditions', children=[condition('instanceOf', self.primary_force_id, 1, 'force')])

    def ally_modifiers(self):
        """Tag primary formations with their army, and check allied formations against the primary's ally lists.

        A primary formation of a list without a Legion choice gets the hidden 'Primary army: <list>' category
        (Legion choices tag themselves instead). An allied formation gets the ALLY_NA_CAT category, which the
        Allied Contingent allows none of, when the roster's primary army doesn't list this army as an ally, and
        has '(disruptive ally: -1 strategy rating)' added to its name when it lists it as disruptive."""
        name = self.army['name']
        mods = []
        key = f'Primary army: {name}'
        if key in CAT and not (self.army.get('legions') and self.choice()['tag']):
            mods.append(X('modifier', {'type': 'add', 'field': 'category', 'value': CAT[key]}, [self.in_primary()]))
        not_allowed = [k for k, (c, d) in ALLY_RULES.items() if name not in c | d]
        disruptive = [k for k, (c, d) in ALLY_RULES.items() if name in d]
        for keys, mod in ((not_allowed, {'type': 'add', 'field': 'category', 'value': CAT[ALLY_NA_CAT]}),
                          (disruptive, {'type': 'append', 'field': 'name',
                                        'value': ' (disruptive ally: -1 strategy rating)'})):
            if keys:
                present = [condition('atLeast', CAT[k], 1, 'roster', child=True, forces=True) for k in keys]
                group = X('conditionGroup', {'type': 'and'}, [
                    X('conditions', children=[condition('instanceOf', self.allied_force_id, 1, 'force')]),
                    X('conditionGroups', children=[X('conditionGroup', {'type': 'or'},
                                                     [X('conditions', children=present)])])])
                mods.append(X('modifier', mod, [X('conditionGroups', children=[group])]))
        return mods

    # -- Legion choice
    def legion_option_id(self, legion):
        return gid('legion', self.cat_id, legion or 'None')

    def legion_conditions(self, legions, chosen=True):
        """Conditions true when any of `legions` is chosen (or, with chosen=False, when none of them is)."""
        conds = [condition('atLeast' if chosen else 'equalTo', self.legion_option_id(l), 1 if chosen else 0, 'force',
                           child=True) for l in legions]
        if len(conds) == 1:
            return X('conditions', children=conds)
        return X('conditionGroups', children=[X('conditionGroup', {'type': 'or' if chosen else 'and'},
                                                [X('conditions', children=conds)])])

    def legion_show(self, legions):
        return (self.legion_conditions(legions), self.legion_conditions(legions, chosen=False)) if legions else None

    def legion_hide(self, legions):
        return self.legion_conditions(legions) if legions else None

    @staticmethod
    def new_show():
        """Conditions for fan-made entries: (toggle on anywhere in the roster, toggle off)."""
        return tuple(X('conditions', children=[condition(t, NEW_UNITS_ID, v, 'roster', child=True, forces=True)])
                     for t, v in (('atLeast', 1), ('equalTo', 0)))

    def gate(self, el, show=None, hide=None, cmax=None, allowed=1):
        """Show `el` only while `show` holds, and hide it while `hide` holds.

        show is a (conditions when available, conditions when not) pair; hide is the conditions under which el is
        unavailable. Hiding stops new selections. A selection left over from an earlier Configuration choice is
        flagged by dropping cmax (el's max constraint, when it has one) to 0, or otherwise by adding the NA_CAT
        category, which the force allows none of. allowed is cmax's value while el is available."""
        mods = el.list_child('modifiers', first=True)
        offs = []
        if show:
            on, off = show
            el.attrs['hidden'] = 'true'
            mods.add(X('modifier', {'type': 'set', 'field': 'hidden', 'value': 'false'}, [on]))
            if cmax:
                next(c for c in el.iter_tag('constraint') if c.attrs['id'] == cmax).attrs['value'] = '0'
                mods.add(X('modifier', {'type': 'set', 'field': cmax, 'value': fmt(allowed)}, [on]))
            offs.append(off)
        if hide:
            mods.add(X('modifier', {'type': 'set', 'field': 'hidden', 'value': 'true'}, [hide]))
            if cmax:
                mods.add(X('modifier', {'type': 'set', 'field': cmax, 'value': '0'}, [hide]))
            offs.append(hide)
        if not cmax:
            for off in offs:
                mods.add(X('modifier', {'type': 'add', 'field': 'category', 'value': CAT[NA_CAT]}, [off]))

    def choice(self):
        """How the list's Configuration choice reads: the Legion, or another list's allegiance."""
        return self.army.get('choice', LEGION_CHOICE)

    def legion_entry(self):
        """The required Configuration choice: the first option keeps the core list; the others add and replace
        formations. For Legion Astartes it picks the Legion, which also sets the army's allies."""
        c = self.choice()
        eid = gid('legion-choice', self.cat_id)
        g = gid('seg', eid, 'legion')
        core_c, core_d = self.army['core_allies']
        choices = [dict(name=None, allegiance=None, cohesive=core_c, disruptive=core_d, notes=[])] + self.army['legions']
        opts = []
        for L in choices:
            oid = self.legion_option_id(L['name'])
            lines = [c['allegiance_text'].format(L['allegiance'])] if L['allegiance'] else [c['none_text']]
            if L['name']:
                adds = [star(f['name'], f.get('new')) for f in self.army['formations']
                        if L['name'] in (f.get('show_for') or [])]
                drops = [f['name'] for f in self.army['formations'] if L['name'] in f.get('hide_for', [])]
                lines.append('Adds: ' + '; '.join(adds) + '.')
                if drops:
                    lines.append('Replaces or removes the core ' + '; '.join(drops) + '.')
                ups = [n for n, vs in self.army.get('upgrade_variants', {}).items()
                       for legions, _ in vs if L['name'] in legions]
                if ups:
                    lines.append('Uses its own version of the ' + ', '.join(ups) + ' upgrade.')
            lines += L['notes']
            tag = []
            if c['tag']:
                lines.append('Cohesive allies: ' + (', '.join(L['cohesive']) or 'none') + '.')
                lines.append('Disruptive allies: ' + (', '.join(L['disruptive']) or 'none') + '.')
                key = f'Primary army: {self.army["name"]} ({L["name"] or "core list"})'
                tag = [X('modifier', {'type': 'add', 'field': 'category', 'value': CAT[key]}, [self.in_primary()])]
            opts.append(ordered('selectionEntry', {'id': oid, 'name': L['name'] or c['none'], 'hidden': 'false',
                                                   'collective': 'false', 'import': 'true', 'type': 'upgrade'},
                                modifiers=tag, constraints=[constraint(gid('con', oid, 'max'), 'max', 1)],
                                rules=[rule_el(gid('r', oid), L['name'] or c['none_rule'], '\n'.join(lines))]))
        group = ordered('selectionEntryGroup', {'id': g, 'name': c['label'], 'hidden': 'false', 'collective': 'false',
                                                'import': 'true', 'defaultSelectionEntryId': opts[0].attrs['id']},
                        constraints=[constraint(gid('con', g, 'min'), 'min', 1),
                                     constraint(gid('con', g, 'max'), 'max', 1)], selectionEntries=opts)
        return ordered('selectionEntry', {'id': eid, 'name': c['label'], 'hidden': 'false', 'collective': 'false',
                                          'import': 'true', 'type': 'upgrade'},
                       constraints=[constraint(gid('con', eid, 'min'), 'min', 1),
                                    constraint(gid('con', eid, 'max'), 'max', 1)],
                       categoryLinks=[cat_link(eid, 'Configuration', True)], selectionEntryGroups=[group])

    def swap_context(self, fid, f):
        """Set up the formation's swap upgrade, if it has one (at most one, never inside an OR choice)."""
        found = []
        for chunk in [c.strip() for c in f['up'].split(',') if c.strip()]:
            for n in [n.strip() for n in chunk.split(' OR ')]:
                sp = self.swap_part(self.army['upgrades'][n]) if n in self.army['upgrades'] else None
                if sp:
                    if ' OR ' in chunk or found:
                        raise ValueError(f'{self.army["name"]}: unsupported swap upgrade layout in {f["name"]}')
                    found.append({'name': n, 'uid': gid('upgrade', fid, n), 'swaps': sp['swaps'], 'lo': sp['min'],
                                  'hi': sp['max'], 'made': [], 'desc': None,
                                  'base_desc': self.army['upgrades'][n]['desc']})
        return found[0] if found else None

    # -- forces
    def force(self, allied):
        a = self.army
        fid = self.allied_force_id if allied else gid('force', self.cat_id, 'primary')
        name = f'{a["name"]} (Allied Contingent)' if allied else a['name']
        slots = sorted({f['slot'] for f in a['formations']}, key=list(SLOT_CAT).index)
        links = []
        for slot in slots:
            cname = SLOT_CAT[slot]
            lid = gid('cl', fid, cname)
            mods, cons = [], []
            dependent = {'support': ('Line Detachment', a['supports_per_line']),
                         'followers': ('Daemonic Horde', 1), 'greater': ('Daemonic Horde', 1)}.get(slot)
            if dependent:
                cid = gid('con', lid, 'ratio')
                cons.append(constraint(cid, 'max', 0))
                mods.append(X('modifier', {'type': 'increment', 'field': cid, 'value': fmt(dependent[1])},
                              [X('repeats', children=[repeat(CAT[dependent[0]], 1, 'parent')])]))
            links.append(ordered('categoryLink', {'id': lid, 'name': cname, 'hidden': 'false', 'targetId': CAT[cname],
                                                  'primary': 'false'}, modifiers=mods, constraints=cons))
        sc_id = gid('cl', fid, 'Supreme Commander')
        if allied:
            sc = [constraint(gid('con', sc_id, 'max'), 'max', 0, scope='parent', child=True)]
            na = gid('cl', fid, ALLY_NA_CAT)
            extra = [ordered('categoryLink', {'id': na, 'name': ALLY_NA_CAT, 'hidden': 'false',
                                              'targetId': CAT[ALLY_NA_CAT], 'primary': 'false'},
                             constraints=[constraint(gid('con', na, 'max'), 'max', 0)])]
        else:
            sc = [constraint(gid('con', sc_id, 'max'), 'max', 1, scope='roster', child=True, forces=True)]
            sp_id = gid('cl', fid, 'Spacecraft')
            extra = [ordered('categoryLink', {'id': sp_id, 'name': 'Spacecraft', 'hidden': 'false',
                                              'targetId': CAT['Spacecraft'], 'primary': 'false'},
                             constraints=[constraint(gid('con', sp_id, 'max'), 'max', 1, scope='roster', child=True,
                                                     forces=True)])]
            if a['allies_fraction']:
                al = gid('cl', fid, 'Allies & Lords of War')
                extra.append(ordered('categoryLink', {'id': al, 'name': 'Allies & Lords of War', 'hidden': 'false',
                                                      'targetId': CAT['Allies & Lords of War'], 'primary': 'false'},
                                     constraints=[constraint(gid('con', al, 'max'), 'max',
                                                             round(a['allies_fraction'] * 100, 2), scope='roster',
                                                             field=PTS, child=True, forces=True, percent=True)]))
        links.append(ordered('categoryLink', {'id': sc_id, 'name': 'Supreme Commander', 'hidden': 'false',
                                              'targetId': CAT['Supreme Commander'], 'primary': 'false'},
                             constraints=sc))
        links += extra
        if a.get('legions') or has_new(a):
            # BattleScribe lists categories in this order; Configuration (Legion or allegiance choice, Allow fan-made
            # units) goes first.
            links.insert(0, X('categoryLink', {'id': gid('cl', fid, 'Configuration'), 'name': 'Configuration',
                                               'hidden': 'false', 'targetId': CAT['Configuration'], 'primary': 'false'}))
            na = gid('cl', fid, NA_CAT)
            links.append(ordered('categoryLink', {'id': na, 'name': NA_CAT, 'hidden': 'false', 'targetId': CAT[NA_CAT],
                                                  'primary': 'false'},
                                 constraints=[constraint(gid('con', na, 'max'), 'max', 0)]))
        desc = self.army_summary(allied)
        return ordered('forceEntry', {'id': fid, 'name': name, 'hidden': 'false'},
                       rules=[rule_el(gid('r', fid), 'Army List', desc)],
                       infoLinks=[info_rule(fid, r) for r in a['rules']], categoryLinks=links)

    def army_summary(self, allied):
        a = self.army
        lines = [f'Strategy Rating {a["strategy"]}. Formation initiative {a["initiative"]}.']
        if a['supports_per_line']:
            lines.append(f'{a["supports_per_line"]} Support Detachments may be taken per Line Detachment.')
        lines += a['notes']
        if (a['cohesive'] or a['disruptive']) and not (a.get('legions') and self.choice()['tag']):
            lines.append('Cohesive allies: ' + (', '.join(a['cohesive']) or 'none') + '.')
            lines.append('Disruptive allies: ' + (', '.join(a['disruptive']) or 'none') + '.')
        if allied:
            lines.append('Allied Contingent: formations here count towards the primary army\'s Allies & Lords of War '
                         'allowance. Supreme Commanders must come from the primary army.')
        return '\n'.join(lines)


XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
ROOT_REV = re.compile(r'(<(?:gameSystem|catalogue)\b[^>]*?) (?:gameSystemRevision|revision)="\d+"')
GST_REVISION = [1]  # set once the game system is written; catalogues record it as gameSystemRevision


def without_revisions(text):
    """File text with the root element's revision attributes removed, for change detection."""
    prev = None
    while prev != text:
        prev, text = text, ROOT_REV.sub(r'\1', text, count=1)
    return text


def write(path, root, ns):
    """Write a data file, bumping its revision only when its content changed.

    Unchanged files are left untouched; new files start at revision 1. A changed catalogue
    also records the game system revision it was built against.
    """
    root.attrs['xmlns'] = ns
    old = open(path, encoding='utf-8').read() if os.path.exists(path) else None
    m = old and re.search(r'<(?:gameSystem|catalogue)\b[^>]*?\brevision="(\d+)"', old)
    old_rev = int(m.group(1)) if m else 0
    root.attrs['revision'] = max(old_rev, 1)
    if 'gameSystemId' in root.attrs:
        root.attrs['gameSystemRevision'] = GST_REVISION[0]
    text = XML_DECL + root.render() + '\n'
    if old is not None and without_revisions(old) == without_revisions(text):
        return old_rev
    root.attrs['revision'] = old_rev + 1
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(XML_DECL + root.render() + '\n')
    return old_rev + 1


CAT_NS = 'http://www.battlescribe.net/schema/catalogueSchema'
GST_NS = 'http://www.battlescribe.net/schema/gameSystemSchema'


def header(cid, name):
    return {'id': cid, 'name': name, 'revision': 1, 'battleScribeVersion': BS_VERSION, 'authorName': AUTHOR,
            'authorContact': '', 'authorUrl': SOURCE_URL, 'library': 'false', 'gameSystemId': GST_ID,
            'gameSystemRevision': GST_REVISION[0]}


def new_units_toggle():
    """'Allow fan-made units': a Configuration entry that shows the fan-made units and options in every force."""
    return ordered('selectionEntry', {'id': NEW_UNITS_ID, 'name': 'Allow fan-made units', 'hidden': 'false',
                                      'collective': 'false', 'import': 'true', 'type': 'upgrade'},
                   constraints=[constraint(gid('con', NEW_UNITS_ID, 'max'), 'max', 1)],
                   categoryLinks=[cat_link(NEW_UNITS_ID, 'Configuration', True)])


def build_gst():
    readme = 'Add a primary army force, then optionally an Allied Contingent force from another catalogue.'
    root = ordered('gameSystem', {'id': GST_ID, 'name': GST_NAME, 'revision': 1, 'battleScribeVersion': BS_VERSION,
                                  'authorName': AUTHOR, 'authorContact': '', 'authorUrl': SOURCE_URL},
                   readme=readme,
                   publications=[X('publication', {'id': gid('pub', 'wiki'), 'name': 'EpicAU Wiki - Horus Heresy Supplement',
                                                   'publisherUrl': SOURCE_URL})],
                   costTypes=X('costTypes', children=[X('costType', {'id': PTS, 'name': 'pts', 'defaultCostLimit': '-1.0',
                                                                    'hidden': 'false'})] + [
                       X('costType', {'id': COST_ID[s], 'name': s, 'defaultCostLimit': '-1.0', 'hidden': 'true'})
                       for s in TRANSPORT_SCHEMES]),
                   profileTypes=X('profileTypes', children=[
                       X('profileType', {'id': PT_UNIT, 'name': 'Unit'}, [X('characteristicTypes', children=[
                           X('characteristicType', {'id': gid('ct', 'Unit', c), 'name': c}) for c in UNIT_CHARS])]),
                       X('profileType', {'id': PT_WAR_ENGINE, 'name': 'War Engine'}, [X('characteristicTypes', children=[
                           X('characteristicType', {'id': gid('ct', 'War Engine', c), 'name': c})
                           for c in WAR_ENGINE_CHARS])]),
                       X('profileType', {'id': PT_WEAPON, 'name': 'Weapon'}, [X('characteristicTypes', children=[
                           X('characteristicType', {'id': gid('ct', 'Weapon', c), 'name': c}) for c in WEAPON_CHARS])])]),
                   categoryEntries=[X('categoryEntry', {'id': CAT[c], 'name': c, 'hidden': str(c in HIDDEN_CATS).lower()})
                                    for c in CATS],
                   selectionEntries=[new_units_toggle()],
                   sharedRules=[rule_el(RULE_ID[n], ACRONYMS.get(n, n), d) for n, d in RULES.items()])
    GST_REVISION[0] = write(os.path.join(OUT, GST_FILE), root, GST_NS)


def build_catalogue(army):
    cid = gid('cat', army['name'])
    profiles = Catalogue(army['name'])
    b = Builder(army, cid, profiles, gid('force', cid, 'allied'))
    formations = [b.formation(f) for f in army['formations']]
    if army.get('legions'):
        formations.insert(0, b.legion_entry())
    upgrades = b.shared_upgrades()
    forces = [b.force(False), b.force(True)]
    root = ordered('catalogue', header(cid, f'EpicAU - {army["name"]}'), forceEntries=forces,
                   selectionEntries=formations, sharedSelectionEntries=upgrades,
                   sharedRules=sorted(profiles.rules.values(), key=lambda r: (r.attrs['name'], r.attrs['id'])) or None,
                   sharedProfiles=sorted(profiles.profiles.values(), key=lambda p: (p.attrs['name'], p.attrs['id'])))
    write(os.path.join(OUT, f'EpicAU - {army["name"]}.cat'), root, CAT_NS)
    return b.missing


def main():
    os.makedirs(OUT, exist_ok=True)
    build_gst()
    missing = {}
    armies = [legion_catalogue()] + OTHER_ARMIES
    for a in armies:
        m = build_catalogue(a)
        if m:
            missing[a['name']] = sorted(set(m))
    for k, v in missing.items():
        print(f'MISSING units in {k}: {v}')
    unused = sorted(set(WEAPON_OPTIONS) - USED_OPTIONS)
    if unused:
        print(f'UNUSED weapon options (no such unit): {unused}')
    print(f'Wrote {len(armies)} catalogues and 1 game system to {OUT}')
    return 1 if missing or unused else 0


if __name__ == '__main__':
    sys.exit(main())
