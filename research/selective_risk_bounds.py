"""Finite-sample, assumption-free selective-risk identification bounds.

These are deterministic arithmetic utilities, not statistical confidence intervals.
No adjudication or model inference is performed here.
"""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class RiskBounds:
    lower: float
    upper: float


def selective_risk_bounds(accepted: int, adjudicated: int, unsafe: int) -> RiskBounds:
    """Bound unsafe acceptance among accepted claims with missing reference labels.

    Requires 0 <= unsafe <= adjudicated <= accepted, accepted > 0.
    Booleans and noninteger counts are rejected.
    """
    for name, value in (("accepted", accepted), ("adjudicated", adjudicated), ("unsafe", unsafe)):
        if type(value) is not int:
            raise TypeError(f"{name} must be an integer count")
    if accepted <= 0 or not (0 <= unsafe <= adjudicated <= accepted):
        raise ValueError("require accepted > 0 and 0 <= unsafe <= adjudicated <= accepted")
    missing = accepted - adjudicated
    return RiskBounds(unsafe / accepted, (unsafe + missing) / accepted)


def difference_bounds(proposed: RiskBounds, baseline: RiskBounds) -> RiskBounds:
    """Conservative, not necessarily sharp bounds for proposed minus baseline."""
    for name, bounds in (("proposed", proposed), ("baseline", baseline)):
        if not isinstance(bounds, RiskBounds):
            raise TypeError(f"{name} must be RiskBounds")
        if not all(isfinite(x) for x in (bounds.lower, bounds.upper)):
            raise ValueError("bounds must be finite")
        if not 0 <= bounds.lower <= bounds.upper <= 1:
            raise ValueError("risk bounds must lie within [0,1]")
    return RiskBounds(proposed.lower - baseline.upper, proposed.upper - baseline.lower)


def superiority_established(delta: RiskBounds) -> bool:
    """True only when even the conservative upper risk difference is negative."""
    if not isinstance(delta, RiskBounds):
        raise TypeError("delta must be RiskBounds")
    if not all(isfinite(x) for x in (delta.lower, delta.upper)) or delta.lower > delta.upper:
        raise ValueError("invalid difference bounds")
    return delta.upper < 0
