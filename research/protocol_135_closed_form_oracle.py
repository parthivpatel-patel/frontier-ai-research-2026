"""Protocol 135: closed-form independent check for multi-family denominator failure.

This is an analytic identity, not a new statistical estimator. It intentionally
does not import the enumerating oracle or production preflight.
"""
from fractions import Fraction


def closed_form_undefined(families):
    """Exact P(any positive-weight family has zero accepted sampled lineages).

    For each family with n lineages, a accepted, and n independent uniform
    draws with replacement, P(no accepted draw) = ((n-a)/n)**n.
    Family resampling streams are assumed independent. Zero-weight families
    do not enter the event. Input sizes do not trigger exponential enumeration.
    """
    families = tuple(families)
    if not families:
        raise ValueError("at least one family required")
    all_defined = Fraction(1)
    included = 0
    for weight, flags in families:
        if type(weight) not in (int, Fraction) or weight < 0:
            raise ValueError("weights must be nonnegative exact numbers")
        flags = tuple(flags)
        if len(flags) < 2 or any(type(flag) is not bool for flag in flags):
            raise ValueError("at least two boolean lineage flags required")
        if weight == 0:
            continue
        included += 1
        n = len(flags)
        a = sum(flags)
        undefined = Fraction(n - a, n) ** n
        all_defined *= 1 - undefined
    if not included:
        raise ValueError("at least one positive-weight family required")
    return 1 - all_defined
