"""Exact rational continuous-domain baseline for one-step reflecting dynamics.

Standard interval/reachability reasoning, NOT a new algorithm or theorem.
No dependencies, network, models, or paid services. Valid only for z in [-1,2].
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction

def Q(value: str | int | Fraction) -> Fraction:
    """Convert decimal strings or integers to exact rationals."""
    return Fraction(value)

@dataclass(frozen=True)
class Interval:
    low: Fraction
    high: Fraction
    def __post_init__(self) -> None:
        if not isinstance(self.low, Fraction) or not isinstance(self.high, Fraction):
            raise TypeError("interval endpoints must be Fraction; use Q()")
        if self.low > self.high:
            raise ValueError("interval endpoints must be ordered")
    def contains(self, other: "Interval") -> bool:
        return self.low <= other.low and other.high <= self.high

@dataclass(frozen=True)
class Domain:
    position: Interval
    velocity: Interval
    impulse: Interval
    def __post_init__(self) -> None:
        if self.position.low < 0 or self.position.high > 1:
            raise ValueError("initial position must be within [0,1]")
        z = self.pre_reflection()
        if z.low < -1 or z.high > 2:
            raise ValueError("only one reflection supported: z must lie in [-1,2]")
    def pre_reflection(self) -> Interval:
        return Interval(
            self.position.low + self.velocity.low + self.impulse.low,
            self.position.high + self.velocity.high + self.impulse.high,
        )
    def contains(self, other: "Domain") -> bool:
        return all((
            self.position.contains(other.position),
            self.velocity.contains(other.velocity),
            self.impulse.contains(other.impulse),
        ))

def reflect(z: Fraction) -> Fraction:
    if z < -1 or z > 2:
        raise ValueError("reflection formula restricted to [-1,2]")
    if z < 0:
        return -z
    if z > 1:
        return 2-z
    return z

def exact_reachable(domain: Domain) -> Interval:
    """Exact image of interval box; evaluate sum endpoints and breakpoints."""
    z = domain.pre_reflection()
    candidates = [z.low, z.high]
    candidates.extend(k for k in (Q(0), Q(1)) if z.low <= k <= z.high)
    values = [reflect(k) for k in candidates]
    return Interval(min(values), max(values))

def _realize_sum(domain: Domain, z: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    """Construct a rational witness inside the box with x+v+a=z."""
    axes = (domain.position, domain.velocity, domain.impulse)
    lo = sum((axis.low for axis in axes), Q(0))
    hi = sum((axis.high for axis in axes), Q(0))
    if not lo <= z <= hi:
        raise ValueError("target outside domain")
    remaining = z-lo
    coords = []
    for axis in axes:
        increase = min(remaining, axis.high-axis.low)
        coords.append(axis.low+increase)
        remaining -= increase
    if remaining:
        raise AssertionError("unallocated interval sum")
    return tuple(coords)  # type: ignore[return-value]

def counterexample(domain: Domain, upper: Fraction) -> tuple[Fraction, Fraction, Fraction] | None:
    """Exact witness for violating next_position <= upper, if one exists."""
    if exact_reachable(domain).high <= upper:
        return None
    z = domain.pre_reflection()
    candidates = [z.low, z.high]
    if z.low <= 1 <= z.high:
        candidates.append(Q(1))
    target = max(candidates, key=reflect)
    witness = _realize_sum(domain, target)
    assert reflect(sum(witness, Q(0))) > upper
    return witness

def threshold_disagreement(domain: Domain, first: Fraction, second: Fraction) -> bool:
    """Whether two <= threshold predicates differ anywhere in this box."""
    if first == second:
        return False
    low, high = sorted((first, second))
    image = exact_reachable(domain)
    return image.high > low and image.low <= high

def audit_scope(certified: Domain, asserted: Domain, upper: Fraction) -> dict:
    """Separate validity, inclusion, and truth for this exact toy dynamics."""
    cert_range = exact_reachable(certified)
    asserted_range = exact_reachable(asserted)
    valid = cert_range.high <= upper
    included = certified.contains(asserted)
    witness = counterexample(asserted, upper)
    if not valid:
        status = "invalid_certificate"
    elif witness is not None:
        status = "asserted_claim_falsified"
    elif not included:
        status = "asserted_claim_true_but_scope_unsupported"
    else:
        status = "supported_on_asserted_scope"
    return {
        "status": status,
        "certificate_valid_on_certified_domain": valid,
        "asserted_domain_subset_of_certified": included,
        "asserted_claim_true_for_this_toy_dynamics": witness is None,
        "certified_reachable_range": tuple(map(str, (cert_range.low, cert_range.high))),
        "asserted_reachable_range": tuple(map(str, (asserted_range.low, asserted_range.high))),
        "counterexample": tuple(map(str, witness)) if witness else None,
        "interpretation": "Exact for one-step rational box domain and one-bounce toy model only.",
    }
