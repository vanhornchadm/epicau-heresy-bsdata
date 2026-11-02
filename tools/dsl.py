"""Small DSL used by spec.py to describe EpicAU army lists.

Unit references are reference-sheet unit names (see source/units.json).
"""


def U(n, unit, each=0, label=None):
    """n units of `unit`. n is an int or (min, max); max None = unlimited."""
    lo, hi = (n, n) if isinstance(n, int) else n
    return {'kind': 'unit', 'unit': unit, 'min': lo, 'max': hi, 'each': each, 'label': label}


def Opt(label, *parts, cost=0):
    """One option of an Or(): a labelled bundle of U()/Mix() parts with an optional cost."""
    return {'label': label, 'parts': list(parts), 'cost': cost}


def Or(*opts, label='Units'):
    """Choose exactly one of the options."""
    return {'kind': 'or', 'opts': list(opts), 'label': label}


def Mix(lo, hi, *units, label='Units'):
    """lo..hi units in any combination; units are (unit, each_cost) or U() with per-unit limits."""
    us = [u if isinstance(u, dict) else U((0, hi), u[0], u[1]) for u in units]
    return {'kind': 'mix', 'min': lo, 'max': hi, 'units': us, 'label': label}


def Fill(per, *units, space='Tactical Transport Space', label='Transports'):
    """Exactly enough transports for the formation: one per `per` units tagged with `space`.

    units are (name, cost) or (name, cost, max_per_formation), in any mix.
    """
    return {'kind': 'fill', 'per': per, 'space': space,
            'units': [U((0, u[2] if len(u) > 2 else None), u[0], u[1]) for u in units], 'label': label}


def Swap(lo, hi, *swaps, label='Upgrades'):
    """Upgrade lo..hi units already in the formation: swaps are (from, to_unit, each_cost).

    `from` is a unit name or a tuple of unit names.
    The upgraded unit replaces the original one-for-one, at the original's cost plus each_cost.
    """
    return {'kind': 'swap', 'min': lo, 'max': hi, 'swaps': list(swaps), 'label': label}


def F(name, slot, cost=0, units=(), up='', maxn=None, per=None, round_up=False, rules=(), note=None,
      extra_up=(), weapons=None):
    """A formation.

    slot: line | support | low | horde | greater | followers | special
    up: upgrade names, comma separated; 'A OR B' means only one of A/B.
    maxn/per: '0-maxn per full `per` points' (per None = per army).
    extra_up: upgrades outside the formation's upgrade cap (e.g. free characters).
    """
    return {'name': name, 'slot': slot, 'cost': cost, 'units': list(units), 'up': up, 'maxn': maxn,
            'per': per, 'round_up': round_up, 'rules': list(rules), 'note': note,
            'extra_up': list(extra_up)}


def UP(name, cost=0, parts=(), rules=(), desc=None, maxn=None, per=None, round_up=False):
    """An upgrade. maxn/per limit how many times it may be taken across the army."""
    return {'name': name, 'cost': cost, 'parts': list(parts), 'rules': list(rules), 'desc': desc,
            'maxn': maxn, 'per': per, 'round_up': round_up}


def ARMY(name, sheets, strategy, initiative, supports_per_line, upgrade_cap, allies_fraction,
         formations, upgrades, cohesive=(), disruptive=(), rules=(), notes=(), support_cap=None,
         low_cap=None, transport_space=()):
    """An army list.

    sheets: reference sheets searched (in order) for unit names.
    upgrade_cap: max upgrades per formation (None = no cap, each once).
    support_cap/low_cap: different caps for support/LoW formations when they differ.
    allies_fraction: fraction of army points usable on Allies + Lords of War (None = no limit).
    transport_space: unit names that take a Tactical transport space (Demi-Gods count as their retinue).
    """
    return {'name': name, 'sheets': list(sheets), 'strategy': strategy, 'initiative': initiative,
            'supports_per_line': supports_per_line, 'upgrade_cap': upgrade_cap,
            'support_cap': support_cap if support_cap is not None else upgrade_cap,
            'low_cap': low_cap if low_cap is not None else upgrade_cap,
            'allies_fraction': allies_fraction, 'formations': formations,
            'upgrades': {u['name']: u for u in upgrades}, 'cohesive': list(cohesive),
            'disruptive': list(disruptive), 'rules': list(rules), 'notes': list(notes),
            'transport_space': set(transport_space)}
