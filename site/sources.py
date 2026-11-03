"""Where each unit and rule added beyond the EpicAU wiki comes from, for the site's Sources sections.

ENTRY_SOURCES maps an entry's name (without its fan-made asterisk) to (source, what came from it) pairs.
A unit with no entry of its own takes the sources of the formations and upgrades it's in, and an EpicAU
formation with new choices shows its new units' sources. The README's data decisions give the detail;
keep the two in step when adding a unit. build_content.py warns about any new entry with no source.
"""

# key -> (name, url or None, what it is)
SOURCES = {
    'epicau': ('EpicAU wiki (archived)',
               'https://web.archive.org/web/20201111221247/http://epicau.com/mw/index.php/Main_Page',
               "The EpicAU community's Horus Heresy supplement for Net Epic Armageddon, which this data is built from."),
    'netea-rules': ('Net Epic Armageddon rulebook', 'https://tp.net-armageddon.org',
                    'The NetEA core rules that EpicAU builds on.'),
    'munitorum': ('Departmento Munitorum', 'https://munitorum.com',
                  'An online Epic army builder, used where the archived wiki has gaps.'),
    'li': ('Legions Imperialis (BSData)', 'https://github.com/BSData/Horus-Heresy-Legions-Imperialis',
           "Games Workshop's Horus Heresy Epic-scale game, read from the BSData data that New Recruit uses. "
           'Its units are converted against comparable EpicAU units.'),
    'netea-ig': ('NetEA Imperial Guard lists', 'https://tp.net-armageddon.org',
                 'The NetEA tournament pack Imperial Guard army lists.'),
    'epic-uk': ('Epic-UK army lists', 'http://epic-uk.co.uk/wp/army-lists/',
                'The Epic-UK community codices for Epic Armageddon.'),
    'dakka': ('Dakka Dakka Kratos proposal', 'https://www.dakkadakka.com/dakkaforum/posts/list/812078.page',
              'A forum proposal for an Epic Kratos squadron, last edited in November 2024.'),
    'empire-of-ashes': ('Empire of Ashes', None,
                        'A separate fan ruleset built on EpicAU ("Epic 30K AB", Public v1.0). Its candidates are '
                        'in the backlog.'),
    'derived': ('Derived from EpicAU units', None,
                'Built from existing EpicAU units and weapons, with points set against comparable units.'),
}

ENTRY_SOURCES = {
    # Departmento Munitorum gap-fills
    'Sabre Strike Tank': [('munitorum', 'stat line, missing from the wiki reference sheet')],
    'Solar Auxilia Tank Hunter Squadron': [('munitorum', 'formation and points'),
                                           ('epicau', 'Valdor Tank Hunter stat line')],

    # Legion Astartes
    'Legion Kratos Heavy Tank Squadron': [('dakka', 'formation, stat line, weapons and points'),
                                          ('derived', 'critical hit and upgrades, as on the other Legion tank squadrons')],
    'Kratos Heavy Tank': [('dakka', 'stat line and weapons'),
                          ('empire-of-ashes', 'the Kratos as a Legion Tank upgrade choice')],
    'Sicaran Punisher': [('derived', "the Sicaran Battle Tank's hull and points, with a main gun from EpicAU weapons"),
                         ('li', 'checked against its Legions Imperialis profile')],
    'Sicaran Arcus': [('derived', "the Sicaran Battle Tank's hull and points, with a main gun from EpicAU weapons"),
                      ('li', 'checked against its Legions Imperialis profile')],
    'Legion Arquitor Bombard Squadron': [('epicau', "the Arquitor's stat line, from the wiki reference sheet"),
                                         ('derived', 'formation and points, priced against the Predator')],
    'Legion Air Defence Battery': [('derived', "the EpicAU Whirlwind Hyperios at the Hyperios upgrade's price"),
                                   ('empire-of-ashes', 'the idea of a Legion air defence formation')],
    'Legion Tarantula Battery': [('derived', 'mirrors the EpicAU Solar Auxilia Tarantula Battery'),
                                 ('li', "the Tarantulas' weapon choice")],
    'Legion Ascalon Squadron': [('li', 'converted against the EpicAU Spartan and Knight-Acheron')],
    'Legion Araknae Weapons Battery': [('li', 'converted against the EpicAU Tarantula')],
    'Legion Saturnine Terminator Detachment': [('li', 'converted against EpicAU Terminators')],
    'Legion Saturnine Dreadnought Talon': [('li', 'converted against the EpicAU Deredeo')],
    'Termite Assault': [('li', 'converted against EpicAU transports'),
                        ('netea-rules', 'the Tunneler rule (2.1.23), as on the Squat Termite')],
    'Termite Assault Drill': [('li', 'converted against EpicAU transports'),
                              ('netea-rules', 'the Tunneler rule (2.1.23), as on the Squat Termite')],
    'Palisade Drop Pod': [('li', 'converted against the EpicAU Drop Pod')],

    # Solar Auxilia
    'Solar Auxilia Thunderbolt Squadron': [('netea-ig', 'unchanged')],
    'Imperial Navy Thunderbolt Fighter': [('netea-ig', 'unchanged')],
    'Solar Auxilia Marauder Squadron': [('netea-ig', 'formation, points and the Marauder Bomber'),
                                        ('li', 'the Colossus and Pathfinder variants')],
    'Imperial Navy Marauder Bomber': [('netea-ig', 'unchanged')],
    'Imperial Navy Marauder Colossus': [('li', "converted onto the NetEA Marauder's hull"),
                                        ('netea-ig', 'hull and heavy bolters')],
    'Imperial Navy Marauder Pathfinder': [('li', "converted onto the NetEA Marauder's hull"),
                                          ('netea-ig', 'hull and heavy bolters')],
    'Solar Auxilia Marauder Destroyer Squadron': [('epic-uk', 'Imperial Guard codex, version 011026')],
    'Imperial Navy Marauder Destroyer': [('epic-uk', 'Imperial Guard codex, version 011026')],
    'Malcador Annihilator': [('epicau', "the Imperial Militia sheet's weapons on the Solar Auxilia Malcador")],
    'Malcador Vanquisher': [('derived', "the Solar Auxilia Malcador with the Leman Russ Vanquisher's cannon")],
    'Leman Russ Annihilator': [('li', 'converted against the EpicAU Leman Russ')],
    'Hellhammer': [('li', 'converted against the EpicAU Baneblade')],
    'Solar Auxilia Aethon Heavy Sentinel Patrol': [('li', 'converted against the EpicAU Militia Sentinel')],
    'Aethon Heavy Sentinel': [('li', 'converted against the EpicAU Militia Sentinel')],
    'Cyclops Battery': [('li', 'converted against EpicAU units')],
    'Cyclops Demolition Vehicle': [('li', 'converted against EpicAU units')],

    # Imperial Militia
    'Auxilia Flak Battery': [('netea-ig', 'the Hydra and its price, unchanged'),
                             ('empire-of-ashes', 'the idea of a Militia flak formation')],

    # Mechanicum Taghmata
    'Arlatax Maniple': [('li', 'Mechanicum library, converted against the EpicAU Castellax')],
    'Domitar Maniple': [('li', 'Mechanicum library, converted against the EpicAU Castellax')],
    'Krios Venator': [('li', 'Mechanicum library, converted against the EpicAU Krios')],
    'Archmagos Prime on Abeyant': [('li', 'Mechanicum library, converted against the EpicAU Archmagos Prime')],
    'Errax Assault Stalker Cohort': [('li', 'Dark Mechanicum catalogue, converted against the EpicAU automata')],
    'Errax': [('li', 'Dark Mechanicum catalogue, converted against the EpicAU automata')],
    'Tenebrax Battle Stalker Cohort': [('li', 'Dark Mechanicum catalogue, converted against the EpicAU automata')],
    'Harpax Scout Host': [('li', 'Dark Mechanicum catalogue, converted against the EpicAU automata')],
    'Serperos Heavy Stalker Maniple': [('li', 'Dark Mechanicum catalogue, converted against the EpicAU automata')],
    'Scintillax': [('li', 'Dark Mechanicum catalogue, converted against the EpicAU automata')],

    # Knight Household
    'Acastus Knight Asterius': [('li', 'Knights library, converted against the EpicAU Porphyrion')],
    'Knight Moirax': [('li', 'Knights library, converted against the EpicAU Armigers')],

    # Legio Titanicus
    'Warbringer Nemesis Titan': [('epic-uk', 'Adeptus Titanicus codex version 080925: stat line and fixed weapons'),
                                 ('derived', "EpicAU's Cortex Controller, critical hit and priced weapon slots")],
    'Warmaster Titan': [('epic-uk', 'Adeptus Titanicus codex version 080925: stat line and fixed weapons'),
                        ('derived', "EpicAU's Cortex Controller, critical hit and priced weapon slots")],
    'Dire Wolf Titan': [('li', 'converted against the EpicAU Warhound')],
    'Warlord-Sinister Titan': [('li', 'converted against the EpicAU Warlord')],
    'Warmaster Iconoclast Titan': [('li', 'converted against the Warmaster')],
    'Neutron Laser': [('li', 'the Dire Wolf weapon, converted')],
    'Conversion Beam Dissipator': [('li', 'the Dire Wolf weapon, converted')],
    'Kirus Siege Drill': [('li', 'the Warmaster Iconoclast weapon, converted')],
    'Kirus Grav Imploder': [('li', 'the Warmaster Iconoclast weapon, converted')],

    # Rules only the new units use
    'Tunneler': [('netea-rules', 'rule 2.1.23')],
}

# Rules the new units share with EpicAU units
EPICAU_RULE_SOURCES = [('epicau', 'the Special Rules page and reference sheets'), ('netea-rules', 'core rules')]
