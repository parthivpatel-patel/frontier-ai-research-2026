"""Protocol 138: exact shared-index failure probability by inclusion-exclusion.

No random sampling or third-party dependencies. Assumes a common ordered panel
of n lineages, n independent uniform draws with replacement, and the SAME draw
index vector for all positive-weight families. Exponential in number of families,
not number of lineage draws; intended for small-family audits.
"""
from fractions import Fraction
from itertools import combinations


def shared_index_inclusion_exclusion(families):
    """Return exact probability at least one included family has no accepted draw."""
    families = tuple(families)
    if not families:
        raise ValueError("at least one family required")
    n = None
    included = []
    for weight, flags in families:
        if type(weight) not in (int, Fraction) or weight < 0:
            raise ValueError("weights must be nonnegative exact numbers")
        flags = tuple(flags)
        if len(flags) < 2 or any(type(flag) is not bool for flag in flags):
            raise ValueError("at least two boolean lineage flags required")
        if n is None:
            n = len(flags)
        elif len(flags) != n:
            raise ValueError("shared indices require equal lineage counts")
        if weight > 0:
            included.append(flags)
    if not included:
        raise ValueError("at least one positive-weight family required")
    result = Fraction(0)
    for k in range(1, len(included) + 1):
        for subset in combinations(included, k):
            # Intersection of failure events: every draw must choose an index
            # rejected by EACH family in this subset.
            rejected_by_all = sum(
                all(not flags[j] for flags in subset) for j in range(n)
            )
            term = Fraction(rejected_by_all, n) ** n
            result += term if k % 2 else -term
    assert 0 <= result <= 1
    return result
