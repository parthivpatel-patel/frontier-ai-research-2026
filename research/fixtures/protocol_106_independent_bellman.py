"""Protocol 106: independent finite-world Bellman value oracle.

Standard library only. Not a runtime sandbox: execute exclusively on a
verified free cloud runner with external memory and wall-time limits.
Does not import or call the Protocol 093 policy enumerator.
"""
from fractions import Fraction
from functools import lru_cache


class Refused(ValueError):
    """Instance exceeds an explicit admission or state limit."""


def optimal_value(costs, budget, worlds, *, max_claims=8,
                  max_worlds=128, max_budget=20, max_states=20000):
    """Return exact optimal conditional reward for noiseless binary checks.

    worlds maps binary tuples to normalized rational probabilities.
    Each claim can be verified once; verification i costs costs[i],
    reveals its bit, and rewards one if and only if the bit is true.
    """
    if type(budget) is not int or budget < 0 or budget > max_budget:
        raise Refused("invalid or oversized budget")
    if type(max_states) is not int or max_states < 1:
        raise Refused("invalid state cap")
    if not isinstance(costs, (list, tuple)) or not (1 <= len(costs) <= max_claims):
        raise Refused("invalid or oversized claim set")
    if any(type(c) is not int or c <= 0 for c in costs):
        raise ValueError("costs must be positive integers")
    if not isinstance(worlds, dict) or not (1 <= len(worlds) <= max_worlds):
        raise Refused("invalid or oversized world table")
    n = len(costs)
    masses = {}
    for world, raw in worlds.items():
        if not isinstance(world, tuple) or len(world) != n or any(type(x) is not int or x not in (0, 1) for x in world):
            raise ValueError("world must be a binary tuple of claim length")
        if isinstance(raw, float) or isinstance(raw, bool):
            raise ValueError("use exact rational probabilities, not floats")
        try:
            mass = Fraction(raw)
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            raise ValueError("invalid probability") from exc
        if mass < 0:
            raise ValueError("negative probability")
        masses[world] = mass
    if sum(masses.values(), Fraction(0)) != 1:
        raise ValueError("prior probabilities must sum to one")
    positive = tuple((w, p) for w, p in masses.items() if p > 0)
    states = 0

    @lru_cache(maxsize=None)
    def solve(observed, true_bits, remaining_budget):
        nonlocal states
        states += 1
        if states > max_states:
            raise Refused("Bellman state cap exceeded")
        compatible = [(w, p) for w, p in positive
                      if all(w[i] == bool(true_bits & (1 << i))
                             for i in range(n) if observed & (1 << i))]
        total = sum((p for _, p in compatible), Fraction(0))
        if total == 0:
            raise AssertionError("unreachable posterior state")
        best = Fraction(0)
        for i, cost in enumerate(costs):
            bit = 1 << i
            if observed & bit or cost > remaining_budget:
                continue
            yes = sum((p for w, p in compatible if w[i] == 1), Fraction(0))
            no = total - yes
            value = Fraction(0)
            if yes:
                value += yes * (1 + solve(observed | bit, true_bits | bit, remaining_budget - cost)) / total
            if no:
                value += no * solve(observed | bit, true_bits, remaining_budget - cost) / total
            if value > best:
                best = value
        return best

    return solve(0, 0, budget)
