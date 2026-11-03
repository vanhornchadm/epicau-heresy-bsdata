# Writing data

The BattleScribe files are built from the Markdown files in this folder. Each army list, formation, upgrade, unit, Titan weapon and special rule is one file. Edit them, then run `python3 tools/generate.py` (or push to `main` and let the build do it).

Every file has the same shape:

- **Front matter** between `---` lines: the entry's settings, as `key: value` lines or a `key:` line followed by `  - item` lines. Quote a value that starts with a digit but is text (`initiative: '2'`) or contains `: `.
- **`# Name`**: the entry's name, exactly as BattleScribe shows it. The file name doesn't matter, but keep it the same as the name.
- **A description**: the paragraph under the name, if the entry has one.
- **`## ` sections**: the parts the generator reads, listed below. Others, such as `## Sources` and `## Design notes`, are for people and the site.

Links such as `[[Tactical Squad]]` name a unit. They are matched against the army's reference sheets, so they need no folder.

## Folders

| Path | What it holds |
|---|---|
| `rules/<rule>.md` | A special rule |
| `<Army>/index.md` | An army list's settings and notes |
| `<Army>/units/` | The units on the army's reference sheet |
| `<Army>/formations/`, `<Army>/upgrades/` | The army's formations and upgrades |
| `<Army>/weapons/` | Titan weapons (Legio Titanicus) |
| `<Army>/legions/<Legion>/` | One option of the list's required choice: an `index.md`, plus `formations/` and `upgrades/` only that option takes |
| `sources.md` | The sources that `## Sources` sections name |

## A unit

```markdown
---
fan-made: true
---
# Kratos Heavy Tank

## Profile

| Type | Speed | Armour | CC | FF |
|---|---|---|---|---|
| WE | 25cm | 4+ | 6+ | 5+ |

## Weapons

| Weapon | Range | Firepower |
|---|---|---|
| Kratos Battlecannon OR | 45cm | 2 x AP3+/AT3+, Armourbane |
| Melta Cannon | 30cm | 4 x MW5+, Armourbane |

## Notes

DC2, Reinforced Armour, Thick Rear Armour. Critical Hit: Unit is destroyed.

## Weapon options

- **Main gun**: pick one
  - Kratos Battlecannon
  - Melta Cannon, +10 pts

## Sources

- Dakka Dakka Kratos proposal: stat line and weapons
```

- **Front matter:** `fan-made: true` hides the unit until a roster takes **Allow fan-made units** and adds an asterisk to its name. `sheet:` names its reference sheet when that isn't the folder's army (the Loyalist and Traitor Legions sheets). `section:` is the sheet section it came from. `replaced-rows:` lists weapon rows the weapon options take over entirely.
- **Notes:** written as on the reference sheet. Rule names in the notes and weapon firepower (`Reinforced Armour`, `MW`, `Disrupt`) link the unit to those rules. `DC`, `Void Shields` and `Critical Hit:` fill a war engine's columns, and a sentence starting `Label:` becomes a rule of the unit's own.
- **Weapon options:** each group is `pick one` (required, starting on the cheapest) or `optional` (at most one). An option names the weapon row it adds; a trailing `OR` on the row is ignored. After the name it may give `+5 pts`, `FF 4+`, `Armour 4+`, `CC 4+`, or `needs Upgrade: Option` to be offered only in formations that took that upgrade option. When an option's weapons aren't the row it's named after, list them below it: a row name, `Name | Range | Firepower` for a weapon of its own, or `(no weapons)`.
- **Titan weapons** (Titans only): one group per mount, `- **Arm** x 2:` or `- **Carapace**:`, listing `[[Weapon]], +25 pts` from `Legio Titanicus/weapons/`.

## A formation

```markdown
---
slot: support
cost: 0
upgrades:
  - Centurion
  - Heavy Transport OR Teleport
extra-upgrades:
  - Legate Commander
limit: 1 per 2000 pts
rules:
  - Demi-God
fan-made: true
---
# Legion Kratos Heavy Tank Squadron

## Composition

- 2-4 [[Kratos Heavy Tank]], +100 pts each
```

- **slot:** `line`, `support`, `low` (Lord of War), `horde`, `greater`, `followers` or `special`.
- **cost:** the formation's base points. Per-unit costs go on the composition lines.
- **upgrades:** one line per upgrade; `A OR B` means only one of them. **extra-upgrades** don't count toward the upgrade cap.
- **limit:** `1 per army`, `1 per 2000 pts`, or `1 per 500 pts or part thereof`.
- **only-with:** the choices (such as `Dark Mechanicum`) that show the formation.
- **The description** is shown as the formation's note.

## Composition

`## Composition` (formations) and `## Adds` (upgrades) list what the entry contains, one part per bullet:

```markdown
- 6 [[Unit]]                                   exactly 6 (or 2-4, or 1+ for no maximum)
- 0-2 [[Unit]], +100 pts each                  a cost per unit
- 3 [[Unit|Shown name]] (fan-made)             a label; fan-made units need 'Allow fan-made units'
- One of:                                      pick exactly one option
  - **Option**, +50 pts: 4 [[Unit]]            an option's parts after the colon, or nested below it
- 4 in any mix of:                             4 units in any combination of these
  - [[Unit]], +25 pts each                     each may be 0 up to the group's maximum, or give its own count
- Transports carrying 2 Transport space each:  exactly enough transports for the formation
  - [[Transport]], +75 pts each
- Upgrade 1-2:                                 swap units already in the formation
  - [[Unit]] or [[Other Unit]] -> [[Upgraded Unit]], +20 pts each
- **Label**: one of:                           any group may start with a bold label
```

The transport space is `Tactical Transport Space` (units listed in the army's `tactical-transport-space`, 1 each) or a transport-space cost: `Transport space` (bulky units such as Terminators, Dreadnoughts and Ogryns count 2), `Transport units` (every unit counts 1) or `Assault Claw space` (Dreadnoughts 4, other bulky units 2).

## An upgrade

```markdown
---
cost: 50
limit: 1 per army
rules:
  - Teleport
---
# Teleport

Add the Teleport special rule to each unit in the formation.
```

The description is shown on the upgrade. `## Adds` lists any units it adds, as in a composition.

## An army list

`<Army>/index.md` holds `sheets` (the reference sheets its units come from, in order), `strategy`, `initiative`, `supports-per-line`, `upgrade-cap` (with `support-upgrade-cap` and `lord-of-war-upgrade-cap` when those differ; leave it out for no cap), `allies-fraction`, `rules`, `cohesive` and `disruptive` allies and `tactical-transport-space`. Its `## Notes` bullets are shown on the force.

A list with a required choice (the Legion, or the Mechanicum's allegiance) also gives the choice's wording (`choice`, `choice-none`, `choice-none-rule`, `choice-none-text`, `choice-text`, `choice-sets-allies`), the folder its options live in (`choice-folder`), and `choices`, the options in the order they are shown. Keep that order: entries shared by several options take their IDs from the first, so reordering them breaks saved rosters.

Each option's `index.md` gives its `allegiance`, its `cohesive` and `disruptive` allies (an empty `disruptive:` means none), `remove` (core formations it may not take) and `## Notes`. A formation in its `formations/` folder replaces the core formation of the same name, ignoring "the" and a leading "Legion", or is added. An upgrade in its `upgrades/` folder replaces the core upgrade of the same name for that option.

## A rule

```markdown
---
acronym: MW
matches:
  - MW
---
# Macro-Weapon

Targets get no save unless they have Reinforced Armour or an Invulnerable Save...
```

`acronym` is the name BattleScribe shows. `matches` lists regular expressions for other ways the reference sheets write the rule, and `pattern` replaces the rule's own name when matching. Matching is case-sensitive.

## Sources

Fan-made and Departmento Munitorum entries list where they come from:

```markdown
## Sources

- Legions Imperialis (BSData): converted against the EpicAU Castellax
```

Each name must be a heading in `sources.md`. The site build warns about a fan-made entry with no sources.
