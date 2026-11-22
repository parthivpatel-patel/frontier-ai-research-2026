"""Linear-time exact sharp bounds for fixed paired binary decisions.

No model inference. Unknown binary truths are shared across policies.
The resulting interval is an identification region, NOT a confidence interval.
"""
from fractions import Fraction

from research.archival_bounds import Counts, paired_difference
from research.paired_archival_oracle import MissingCase


def sharp_paired_difference_linear(a: Counts, b: Counts, missing):
    """Return exact endpoints; O(m) time and O(m) input storage.

    Denominators are fixed because acceptance is fixed before truth assignment.
    Each missing truth contributes independently to the difference.
    """
    missing = tuple(missing)
    if a.n != b.n or a.m != b.m or len(missing) != a.m:
        raise ValueError("Verified and unresolved sampling frames must agree")
    if any(not isinstance(c, MissingCase) for c in missing):
        raise TypeError("All missing cases must be MissingCase instances")
    ka = a.accepted + sum(c.accept_a for c in missing)
    kb = b.accepted + sum(c.accept_b for c in missing)
    conservative = paired_difference(a, b)
    if not ka or not kb:
        return {"sharp": None, "conservative": conservative,
                "defined_assignments": 0,
                "undefined_assignments": 2 ** len(missing)}
    base = Fraction(a.errors, ka) - Fraction(b.errors, kb)
    lo = hi = base
    for c in missing:
        # Evaluate the same missing label for both policies, never independently.
        def contribution(y):
            return (Fraction(int(c.predict_a != y), ka) if c.accept_a else Fraction(0)) - (Fraction(int(c.predict_b != y), kb) if c.accept_b else Fraction(0))
        z, o = contribution(0), contribution(1)
        lo += min(z, o)
        hi += max(z, o)
    if conservative is not None and not (conservative[0] <= lo <= hi <= conservative[1]):
        raise AssertionError("Sharp bounds escaped conservative envelope")
    return {"sharp": (lo, hi), "conservative": conservative,
            "defined_assignments": 2 ** len(missing),
            "undefined_assignments": 0}
