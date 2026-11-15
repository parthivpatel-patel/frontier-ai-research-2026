"""Protocol 098: bounded structural preflight for Protocol 093.
Pure standard-library implementation; not executed at publication.
This module does NOT claim to bound process memory or wall time.
"""
from functools import lru_cache
from fractions import Fraction

class PreflightRefusal(Exception):
    """Instance is not admitted; no optimality certificate was computed."""

def structural_count(costs, budget, limit):
    """Saturated count of complete binary-observation policy trees.

    Returns min(actual_count, limit + 1). Does not generate policy trees.
    """
    if type(limit) is not int or limit < 1:
        raise ValueError("invalid limit")
    if type(budget) is not int or budget < 0:
        raise ValueError("invalid budget")
    if not isinstance(costs, (tuple, list)) or not costs or any(
            type(c) is not int or c <= 0 for c in costs):
        raise ValueError("invalid costs")
    costs = tuple(costs)
    ceiling = limit + 1

    @lru_cache(None)
    def count(mask, b):
        total = 1
        for i, cost in enumerate(costs):
            if mask & (1 << i) and cost <= b:
                sub = count(mask ^ (1 << i), b - cost)
                total = min(ceiling, total + min(ceiling, sub * sub))
                if total == ceiling:
                    break
        return total
    return count((1 << len(costs)) - 1, budget)

def admit(costs, budget, worlds, *, max_claims=6, max_trees=10000,
          max_worlds=64, max_budget=12, max_cost=12):
    """Fail closed before invoking the original enumerator.

    A successful admission is only a structural check, not resource certification.
    The caller must separately impose cloud process memory/time limits.
    """
    if any(type(x) is not int or x < 1 for x in
           (max_claims, max_trees, max_worlds, max_budget, max_cost)):
        raise ValueError("invalid limits")
    if not isinstance(costs, (tuple, list)) or not costs or any(
            type(c) is not int or c <= 0 for c in costs):
        raise ValueError("invalid costs")
    if type(budget) is not int or budget < 0:
        raise ValueError("invalid budget")
    n = len(costs)
    if n > max_claims or (1 << n) > max_worlds or budget > max_budget or max(costs) > max_cost:
        raise PreflightRefusal("instance exceeds structural limits")
    if not isinstance(worlds, dict) or len(worlds) != (1 << n):
        raise ValueError("incomplete world table")
    mass = Fraction(0)
    seen = set()
    for bits, p in worlds.items():
        if (not isinstance(bits, tuple) or len(bits) != n
                or any(type(bit) is not int or bit not in (0, 1) for bit in bits)):
            raise ValueError("invalid world key")
        if bits in seen:
            raise ValueError("duplicate world key")
        seen.add(bits)
        if type(p) not in (int, Fraction) or p < 0:
            raise ValueError("invalid mass")
        mass += Fraction(p)
    if mass != 1:
        raise ValueError("masses must sum to one")
    count = structural_count(costs, budget, max_trees)
    if count > max_trees:
        raise PreflightRefusal("policy tree count exceeds cap")
    return count
