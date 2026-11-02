"""Deterministic, grammar-controlled physical semantic-oracle stress suite.

Every English instruction is generated from an explicit latent threshold.
No language model is queried or evaluated. Deliberately omitted references
and candidate errors are injected by construction, not discovered in data.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction

from src.exact_domain_audit import (
    Domain, Interval, Q, exact_reachable as reflecting_reachable,
    reflect, threshold_disagreement as reflecting_disagreement,
)
from src.damped_domain_audit import (
    DampedDomain, exact_reachable as damped_reachable,
    disagreement_witness as damped_witness,
    position_after_two_steps, threshold_disagreement as damped_disagreement,
)


@dataclass(frozen=True)
class Probe:
    case_id: str
    family: str
    domain: Domain | DampedDomain
    instruction: str
    latent_upper: Fraction
    candidate_upper: Fraction
    supplied_reference_uppers: tuple[Fraction, ...]
    intervention: str

    def __post_init__(self) -> None:
        if self.family not in ("reflecting", "damped"):
            raise ValueError("unknown dynamics family")
        expected = Domain if self.family == "reflecting" else DampedDomain
        if not isinstance(self.domain, expected):
            raise TypeError("family and domain do not match")
        if not self.supplied_reference_uppers:
            raise ValueError("reference set must not be empty")


def _domain(family: str, restricted: bool):
    if family == "reflecting":
        return Domain(Interval(Q("1/2"), Q("1/2")), Interval(Q(0), Q(0)),
                      Interval(Q(0), Q("1/4") if restricted else Q("1/2")))
    return DampedDomain(
        Interval(Q("1/2"), Q("1/2")), Interval(Q(0), Q(0)),
        Interval(Q(0), Q("1/6") if restricted else Q("1/3")),
        Interval(Q(0), Q(0)), Q("1/2"),
    )


def make_suite() -> tuple[Probe, ...]:
    """Five controlled cases per family; no random sampling or model output."""
    cases = []
    # case name, latent threshold, candidate threshold, supplied references, scope
    recipes = (
        ("exact", "4/5", "4/5", ("4/5",), False),
        ("drift", "9/10", "4/5", ("9/10",), False),
        ("omitted", "9/10", "4/5", ("4/5",), False),
        ("multiple", "9/10", "4/5", ("4/5", "9/10"), False),
        ("restricted", "9/10", "4/5", ("9/10",), True),
    )
    for family in ("reflecting", "damped"):
        moment = "after one reflection update" if family == "reflecting" else "after two damped updates"
        for label, latent, candidate, references, restricted in recipes:
            cases.append(Probe(
                case_id=f"{family}_{label}",
                family=family,
                domain=_domain(family, restricted),
                instruction=f"Check whether the position {moment} is at most {latent}.",
                latent_upper=Q(latent),
                candidate_upper=Q(candidate),
                supplied_reference_uppers=tuple(Q(x) for x in references),
                intervention="restricted" if restricted else "wide",
            ))
    return tuple(cases)


def _reachable(case: Probe) -> Interval:
    if case.family == "reflecting":
        return reflecting_reachable(case.domain)
    return damped_reachable(case.domain)


def _disagrees(case: Probe, reference: Fraction) -> bool:
    if case.family == "reflecting":
        return reflecting_disagreement(case.domain, case.candidate_upper, reference)
    return damped_disagreement(case.domain, case.candidate_upper, reference)


def _reflecting_witness(case: Probe) -> tuple[Fraction, ...] | None:
    if not _disagrees(case, case.latent_upper):
        return None
    image = _reachable(case)
    low, high = sorted((case.candidate_upper, case.latent_upper))
    target = min(image.high, high)
    assert image.low <= target and target > low
    z_range = case.domain.pre_reflection()
    # Invert the piecewise-linear reflection map on [-1,2].
    for z in (target, -target, Q(2) - target):
        if not z_range.low <= z <= z_range.high or reflect(z) != target:
            continue
        axes = (case.domain.position, case.domain.velocity, case.domain.impulse)
        remaining = z - sum((axis.low for axis in axes), Q(0))
        coords = []
        for axis in axes:
            increase = min(remaining, axis.high - axis.low)
            coords.append(axis.low + increase)
            remaining -= increase
        if remaining != 0:
            raise AssertionError("failed to realize reachable sum")
        witness = tuple(coords)
        y = reflect(sum(witness, Q(0)))
        assert y == target and (y <= case.candidate_upper) != (y <= case.latent_upper)
        return witness
    raise AssertionError("reachable image has no rational inverse")


def _witness(case: Probe) -> tuple[Fraction, ...] | None:
    if case.family == "reflecting":
        return _reflecting_witness(case)
    return damped_witness(case.domain, case.candidate_upper, case.latent_upper)


def evaluate_suite() -> dict[str, object]:
    rows = []
    for case in make_suite():
        latent_error = int(_disagrees(case, case.latent_upper))
        possible = sorted({int(_disagrees(case, r))
                           for r in case.supplied_reference_uppers})
        witness = _witness(case)
        assert (witness is not None) == bool(latent_error)
        if witness is not None:
            y = (reflect(sum(witness, Q(0))) if case.family == "reflecting"
                 else position_after_two_steps(case.domain, *witness))
            assert (y <= case.candidate_upper) != (y <= case.latent_upper)
        rows.append({
            "id": case.case_id,
            "family": case.family,
            "instruction": case.instruction,
            "intervention": case.intervention,
            "latent_error": latent_error,
            "supplied_error_set": possible,
            "reachable": [str(_reachable(case).low), str(_reachable(case).high)],
            "counterexample_coordinates": [str(x) for x in witness] if witness else None,
        })
    n = len(rows)
    certain = sum(row["supplied_error_set"] == [1] for row in rows)
    possible = sum(1 in row["supplied_error_set"] for row in rows)
    actual = sum(row["latent_error"] for row in rows)
    return {
        "summary": {
            "cases": n,
            "families": 2,
            "latent_error_rate": str(Fraction(actual, n)),
            "supplied_lower_rate": str(Fraction(certain, n)),
            "supplied_upper_rate": str(Fraction(possible, n)),
            "latent_outside_supplied_envelope": not certain <= actual <= possible,
        },
        "cases": rows,
        "warning": "Deliberately constructed grammar-controlled toy suite, NOT LLM evaluation, NLP benchmark validation, or generalization evidence.",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate_suite(), indent=2, sort_keys=True))
