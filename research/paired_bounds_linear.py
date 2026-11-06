"""Sharp paired missing-label risk-difference bounds for frozen acceptance sets.

Reference implementation; no empirical results. Standard library only.
Each truth entry is 0 (safe), 1 (unsafe), or None (unadjudicated).
Acceptance indicators are strict booleans. The two methods share each
claim's unknown unsafe label. Complexity O(n), memory O(1) beyond inputs.
"""
from fractions import Fraction


def paired_risk_difference_bounds(proposed, baseline, unsafe):
    """Return exact (lower, upper) bounds for risk(proposed)-risk(baseline).

    Bounds are sharp conditional on the supplied fixed acceptance sets and
    observed binary labels, with no restrictions on unobserved labels.
    Neither sampling confidence intervals nor population risk bounds.
    """
    if not isinstance(proposed, (list, tuple)) or not isinstance(baseline, (list, tuple)) or not isinstance(unsafe, (list, tuple)):
        raise TypeError("inputs must be lists or tuples")
    if not (len(proposed) == len(baseline) == len(unsafe)):
        raise ValueError("length mismatch")
    if any(type(v) is not bool for v in proposed) or any(type(v) is not bool for v in baseline):
        raise TypeError("acceptance entries must be bool")
    if any(v is not None and type(v) is not int for v in unsafe):
        raise TypeError("unsafe labels must be 0, 1, or None")
    if any(v is not None and v not in (0, 1) for v in unsafe):
        raise ValueError("unsafe labels must be binary")
    na = sum(proposed)
    nb = sum(baseline)
    if na == 0 or nb == 0:
        raise ValueError("selective risk undefined for zero accepted claims")
    lower = Fraction(0)
    upper = Fraction(0)
    for a, b, y in zip(proposed, baseline, unsafe):
        coefficient = Fraction(int(a), na) - Fraction(int(b), nb)
        if y is None:
            lower += min(coefficient, 0)
            upper += max(coefficient, 0)
        else:
            lower += coefficient * y
            upper += coefficient * y
    return lower, upper
