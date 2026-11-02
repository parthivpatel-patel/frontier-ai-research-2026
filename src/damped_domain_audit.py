"""Exact two-step damped-motion oracle, independent of the reflecting-particle map.

v[t+1] = rho*v[t] + u[t]; x[t+1] = x[t] + v[t+1].
rho is a fixed rational in [0,1]. Independent rational box inputs.
The affine reachable interval is exact; this is elementary mathematics,
not a new scientific algorithm or a validated physical simulator.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from src.exact_domain_audit import Interval


@dataclass(frozen=True)
class DampedDomain:
    position: Interval
    velocity: Interval
    impulse_0: Interval
    impulse_1: Interval
    damping: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.damping, Fraction) or not 0 <= self.damping <= 1:
            raise ValueError("damping must be an exact Fraction in [0,1]")
        if any(not isinstance(axis, Interval) for axis in self.axes):
            raise TypeError("all state and action axes must be exact Intervals")

    @property
    def axes(self) -> tuple[Interval, Interval, Interval, Interval]:
        return (self.position, self.velocity, self.impulse_0, self.impulse_1)


def position_after_two_steps(
    domain: DampedDomain, x0: Fraction, v0: Fraction,
    u0: Fraction, u1: Fraction,
) -> Fraction:
    """Evaluate one admissible rational trajectory, not an approximate solver."""
    values = (x0, v0, u0, u1)
    if any(not isinstance(value, Fraction) for value in values):
        raise TypeError("trajectory coordinates must be exact Fractions")
    if any(not axis.low <= value <= axis.high
           for axis, value in zip(domain.axes, values)):
        raise ValueError("trajectory is outside the declared physical domain")
    v1 = domain.damping * v0 + u0
    v2 = domain.damping * v1 + u1
    return x0 + v1 + v2


def exact_reachable(domain: DampedDomain) -> Interval:
    """Exact image of a rational input box for nonnegative affine coefficients."""
    rho = domain.damping
    weights = (Fraction(1), rho + rho * rho, Fraction(1) + rho, Fraction(1))
    low = sum((w * axis.low for w, axis in zip(weights, domain.axes)), Fraction(0))
    high = sum((w * axis.high for w, axis in zip(weights, domain.axes)), Fraction(0))
    return Interval(low, high)


def counterexample(domain: DampedDomain, upper: Fraction) -> tuple[Fraction, ...] | None:
    """A rational trajectory violating x2 <= upper, or None if none exists."""
    if not isinstance(upper, Fraction):
        raise TypeError("upper must be a Fraction")
    if exact_reachable(domain).high <= upper:
        return None
    witness = tuple(axis.high for axis in domain.axes)
    assert position_after_two_steps(domain, *witness) > upper
    return witness


def threshold_disagreement(domain: DampedDomain, first: Fraction, second: Fraction) -> bool:
    """Whether x2 <= first and x2 <= second differ on the entire domain."""
    if not isinstance(first, Fraction) or not isinstance(second, Fraction):
        raise TypeError("thresholds must be exact Fractions")
    if first == second:
        return False
    lower, upper = sorted((first, second))
    image = exact_reachable(domain)
    return image.high > lower and image.low <= upper


def disagreement_witness(
    domain: DampedDomain, first: Fraction, second: Fraction,
) -> tuple[Fraction, ...] | None:
    """Construct a rational trajectory separating two threshold predicates."""
    if not threshold_disagreement(domain, first, second):
        return None
    lower, upper = sorted((first, second))
    image = exact_reachable(domain)
    target = min(image.high, upper)
    assert image.low <= target and target > lower
    fraction = ((target - image.low) / (image.high - image.low)
                if image.high > image.low else Fraction(0))
    witness = tuple(axis.low + fraction * (axis.high - axis.low)
                    for axis in domain.axes)
    actual = position_after_two_steps(domain, *witness)
    assert actual == target and (actual <= first) != (actual <= second)
    return witness
