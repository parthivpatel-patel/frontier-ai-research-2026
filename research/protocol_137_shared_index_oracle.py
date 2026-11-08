"""Protocol 137: exact joint denominator-failure oracle for shared-index resampling.

This oracle models a *specified* common-index contract, not an assertion
about the production sampler. No random draws or external dependencies.
"""
from fractions import Fraction
from itertools import product


def exact_shared_index_undefined(families):
    """Enumerate n**n equally likely common index vectors across families.

    Each positive-weight family has the same n ordered lineages. One index
    vector of length n is drawn with replacement and reused by all families.
    Return P(any included family has no accepted lineage in the draw).
    """
    families = tuple(families)
    if not families:
        raise ValueError("at least one family required")
    included = []
    n = None
    for weight, flags in families:
        if type(weight) not in (int, Fraction) or weight < 0:
            raise ValueError("weights must be nonnegative exact numbers")
        flags = tuple(flags)
        if len(flags) < 2 or any(type(x) is not bool for x in flags):
            raise ValueError("at least two boolean lineage flags required")
        if n is None:
            n = len(flags)
        elif len(flags) != n:
            raise ValueError("shared indices require equal lineage counts")
        if weight > 0:
            included.append(flags)
    if not included:
        raise ValueError("at least one positive-weight family required")
    undefined = sum(
        any(not any(flags[j] for j in indices) for flags in included)
        for indices in product(range(n), repeat=n)
    )
    return Fraction(undefined, n ** n)


def marginal_union_bounds(families):
    """Frechet/union bounds assuming independent draws *within* each family."""
    families = tuple(families)
    included = []
    for weight, flags in families:
        if type(weight) not in (int, Fraction) or weight < 0:
            raise ValueError("weights must be nonnegative exact numbers")
        flags = tuple(flags)
        if len(flags) < 2 or any(type(x) is not bool for x in flags):
            raise ValueError("at least two boolean lineage flags required")
        if weight > 0:
            n = len(flags)
            included.append(Fraction(n - sum(flags), n) ** n)
    if not included:
        raise ValueError("at least one positive-weight family required")
    return max(included), min(Fraction(1), sum(included))
