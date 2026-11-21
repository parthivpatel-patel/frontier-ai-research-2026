"""Exact small-frame paired selective-risk identification oracle.

Reference implementation only: exponential in unresolved-case count.
Do not use for large frames or model inference. Execute tests only on
verified free cloud infrastructure, never on the user's laptop.
"""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

from research.archival_bounds import Counts, paired_difference


@dataclass(frozen=True)
class MissingCase:
    predict_a: int
    accept_a: bool
    predict_b: int
    accept_b: bool

    def __post_init__(self):
        if type(self.predict_a) is not int or self.predict_a not in (0, 1):
            raise ValueError("predict_a must be binary integer")
        if type(self.predict_b) is not int or self.predict_b not in (0, 1):
            raise ValueError("predict_b must be binary integer")
        if type(self.accept_a) is not bool or type(self.accept_b) is not bool:
            raise TypeError("accept indicators must be booleans")


def sharp_paired_difference(a: Counts, b: Counts, missing, max_missing=16):
    """Exact bounds conditional on FIXED predictions/acceptances and shared truth.

    Returns endpoints, feasible and undefined assignment counts, and the
    conservative marginal-difference envelope. None endpoints mean that
    no assignment defines both risks. This is not a confidence interval.
    """
    missing = tuple(missing)
    if a.n != b.n or a.m != b.m or len(missing) != a.m:
        raise ValueError("Verified and unresolved sampling frames must agree")
    if type(max_missing) is not int or max_missing < 0 or len(missing) > max_missing:
        raise ValueError("Enumeration limit exceeded")
    if any(not isinstance(c, MissingCase) for c in missing):
        raise TypeError("All missing cases must be MissingCase instances")
    ka = a.accepted + sum(c.accept_a for c in missing)
    kb = b.accepted + sum(c.accept_b for c in missing)
    if not ka or not kb:
        return {"sharp": None, "defined_assignments": 0,
                "undefined_assignments": 2 ** len(missing),
                "conservative": paired_difference(a, b)}
    values = []
    for truth in product((0, 1), repeat=len(missing)):
        ea = a.errors + sum(c.accept_a and c.predict_a != y
                            for c, y in zip(missing, truth))
        eb = b.errors + sum(c.accept_b and c.predict_b != y
                            for c, y in zip(missing, truth))
        values.append(Fraction(ea, ka) - Fraction(eb, kb))
    result = (min(values), max(values))
    conservative = paired_difference(a, b)
    if conservative is not None and not (
        conservative[0] <= result[0] <= result[1] <= conservative[1]
    ):
        raise AssertionError("Sharp bounds escaped conservative envelope")
    return {"sharp": result, "defined_assignments": len(values),
            "undefined_assignments": 0, "conservative": conservative}
