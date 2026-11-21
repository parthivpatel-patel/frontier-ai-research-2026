"""Dependency-free identification bounds for enumerated archival missingness.

Analytical arithmetic only; not model inference or a confidence interval.
Run tests in an explicitly authorized free cloud environment:
    python -m unittest research.test_archival_bounds
"""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Counts:
    n: int
    m: int
    accepted: int
    errors: int

    def __post_init__(self):
        vals = (self.n, self.m, self.accepted, self.errors)
        if any(type(v) is not int for v in vals):
            raise TypeError("All counts must be integers, not booleans or floats")
        if not (0 <= self.errors <= self.accepted <= self.n and self.m >= 0):
            raise ValueError("Require 0 <= errors <= accepted <= n and m >= 0")


def bounds(c: Counts):
    """Return exact rational endpoints; None denotes undefined conditional risk.

    Assumes a fixed, enumerated unresolved frame of m cases, with unconstrained
    acceptance/error assignments. Endpoints are *identification*, not sampling,
    intervals. If no example can be accepted, risk is undefined.
    """
    denominator = c.accepted + c.m
    risk = (Fraction(c.errors, denominator),
            Fraction(c.errors + c.m, denominator)) if denominator else None
    population = c.n + c.m
    coverage = (Fraction(c.accepted, population),
                Fraction(c.accepted + c.m, population)) if population else None
    observed_risk = Fraction(c.errors, c.accepted) if c.accepted else None
    return {"observed_risk": observed_risk, "risk": risk, "coverage": coverage}


def paired_difference(a: Counts, b: Counts):
    """Conservative (generally non-sharp) interval for risk(A)-risk(B).

    Both policies must be evaluated on the SAME n verified cases and SAME m
    enumerated unresolved cases. A None result means an endpoint is undefined.
    """
    if a.n != b.n or a.m != b.m:
        raise ValueError("Paired comparisons require identical sampling frames")
    ra, rb = bounds(a)["risk"], bounds(b)["risk"]
    if ra is None or rb is None:
        return None
    return (ra[0] - rb[1], ra[1] - rb[0])
