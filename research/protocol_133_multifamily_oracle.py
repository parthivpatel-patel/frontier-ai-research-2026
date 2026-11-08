"""Protocol 133: independent exact oracle for multi-family denominator failure.

Enumerates independent ordered lineage resamples for small frozen families.
No production preflight or bootstrap code is imported.
"""
from fractions import Fraction
from itertools import product


def exact_multifamily_undefined(families):
    """Return exact probability at least one positive-weight family is undefined.

    families: iterable of (weight, lineage_joint_acceptance_flags).
    Every family independently draws n indices with replacement from n lineages.
    This oracle intentionally checks denominator existence only, not the
    production statistic, interval coverage, or physics performance.
    """
    families = tuple(families)
    if not families:
        raise ValueError("at least one family required")
    defined_probabilities = []
    for weight, flags in families:
        if type(weight) not in (int, Fraction) or weight < 0:
            raise ValueError("weights must be nonnegative exact numbers")
        flags = tuple(flags)
        if len(flags) < 2 or any(type(x) is not bool for x in flags):
            raise ValueError("at least two boolean lineage flags required")
        if weight == 0:
            continue
        n = len(flags)
        defined = sum(
            any(flags[j] for j in indices)
            for indices in product(range(n), repeat=n)
        )
        defined_probabilities.append(Fraction(defined, n ** n))
    if not defined_probabilities:
        raise ValueError("at least one positive-weight family required")
    all_defined = Fraction(1)
    for p in defined_probabilities:
        all_defined *= p
    return 1 - all_defined
