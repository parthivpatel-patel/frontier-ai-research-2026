"""Finite-menu physical distinguishability with exact rational witnesses.

This is a conventional observational-equivalence and cost-search baseline,
NOT a novel method, a learned parser, or a way to infer human intent.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from src.exact_domain_audit import (
    Domain, Q, exact_reachable as reflecting_reachable, reflect,
    threshold_disagreement as reflecting_disagreement,
)
from src.damped_domain_audit import (
    DampedDomain, disagreement_witness as damped_witness,
    position_after_two_steps,
)


@dataclass(frozen=True)
class Intervention:
    label: str
    family: str
    domain: Domain | DampedDomain
    cost: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.label, str) or not self.label.strip():
            raise ValueError("label must be a nonempty string")
        if self.family not in ("reflecting", "damped"):
            raise ValueError("unknown physical family")
        expected = Domain if self.family == "reflecting" else DampedDomain
        if not isinstance(self.domain, expected):
            raise TypeError("domain does not match family")
        if not isinstance(self.cost, Fraction) or self.cost < 0:
            raise ValueError("cost must be a nonnegative exact Fraction")


def _check(first: Fraction, second: Fraction) -> None:
    if not isinstance(first, Fraction) or not isinstance(second, Fraction):
        raise TypeError("thresholds must be exact Fractions")


def _reflecting_witness(domain: Domain, first: Fraction,
                        second: Fraction) -> tuple[Fraction, ...] | None:
    if not reflecting_disagreement(domain, first, second):
        return None
    image = reflecting_reachable(domain)
    lower, upper = sorted((first, second))
    target = min(image.high, upper)
    assert image.low <= target and target > lower
    z_range = domain.pre_reflection()
    for z in (target, -target, Q(2) - target):
        if not z_range.low <= z <= z_range.high or reflect(z) != target:
            continue
        axes = (domain.position, domain.velocity, domain.impulse)
        remaining = z - sum((axis.low for axis in axes), Q(0))
        coords: list[Fraction] = []
        for axis in axes:
            extra = min(remaining, axis.high - axis.low)
            coords.append(axis.low + extra)
            remaining -= extra
        assert remaining == 0
        witness = tuple(coords)
        assert reflect(sum(witness, Q(0))) == target
        return witness
    raise AssertionError("reachable reflecting output had no inverse")


def trajectory_output(option: Intervention,
                      coordinates: tuple[Fraction, ...]) -> Fraction:
    """Validate the trajectory before computing its physical output."""
    if option.family == "reflecting":
        domain = option.domain
        axes = (domain.position, domain.velocity, domain.impulse)
        if len(coordinates) != 3 or any(
            not isinstance(value, Fraction) or not axis.low <= value <= axis.high
            for value, axis in zip(coordinates, axes)
        ):
            raise ValueError("invalid reflecting trajectory")
        return reflect(sum(coordinates, Q(0)))
    if len(coordinates) != 4:
        raise ValueError("invalid damped trajectory")
    return position_after_two_steps(option.domain, *coordinates)


def separating_witness(option: Intervention, first: Fraction,
                       second: Fraction) -> tuple[Fraction, ...] | None:
    """Return an exact physical trajectory where two predicates differ."""
    _check(first, second)
    witness = (_reflecting_witness(option.domain, first, second)
               if option.family == "reflecting"
               else damped_witness(option.domain, first, second))
    if witness is not None:
        y = trajectory_output(option, witness)
        assert (y <= first) != (y <= second)
    return witness


def choose_cheapest_separating_intervention(
    interventions: Iterable[Intervention], first: Fraction, second: Fraction,
) -> dict[str, object]:
    """Finite-menu minimum-cost search; costs are hypothetical inputs."""
    _check(first, second)
    menu = tuple(interventions)
    if len({item.label for item in menu}) != len(menu):
        raise ValueError("intervention labels must be unique")
    matches = []
    for option in menu:
        witness = separating_witness(option, first, second)
        if witness is not None:
            matches.append((option.cost, option.label, option, witness))
    if not matches:
        return {
            "status": "indistinguishable_under_supplied_menu",
            "menu_size": len(menu),
            "separating_options": 0,
            "meaning": "No supplied intervention separates the predicates; global equivalence is not established.",
            "intent_caveat": "Physics alone cannot establish which predicate a human intended.",
        }
    _, _, option, witness = min(matches, key=lambda x: (x[0], x[1]))
    y = trajectory_output(option, witness)
    return {
        "status": "physically_distinguishable",
        "menu_size": len(menu),
        "separating_options": len(matches),
        "selected": option.label,
        "family": option.family,
        "hypothetical_cost": str(option.cost),
        "witness": [str(x) for x in witness],
        "position": str(y),
        "first_predicate": y <= first,
        "second_predicate": y <= second,
        "intent_caveat": "A separating trajectory does not identify the intended human meaning without independent feedback.",
    }


def observational_equivalence_classes(
    interventions: Iterable[Intervention], thresholds: Iterable[Fraction],
) -> tuple[tuple[Fraction, ...], ...]:
    """Partition finite hypotheses by behavior on all supplied domains."""
    menu = tuple(interventions)
    hypotheses = tuple(thresholds)
    if not hypotheses or len(set(hypotheses)) != len(hypotheses):
        raise ValueError("thresholds must be nonempty and distinct")
    for h in hypotheses:
        _check(h, h)
    groups: list[list[Fraction]] = []
    for hypothesis in hypotheses:
        for group in groups:
            if all(separating_witness(item, hypothesis, group[0]) is None
                   for item in menu):
                group.append(hypothesis)
                break
        else:
            groups.append([hypothesis])
    return tuple(tuple(group) for group in groups)


def demonstration() -> dict[str, object]:
    """Constructed two-family example; no model inference or human data."""
    from src.physical_probe_suite import make_suite

    cases = {case.case_id: case for case in make_suite()}
    menu = (
        Intervention("reflecting_restricted", "reflecting",
                     cases["reflecting_restricted"].domain, Q(1)),
        Intervention("damped_restricted", "damped",
                     cases["damped_restricted"].domain, Q(1)),
        Intervention("reflecting_wide", "reflecting",
                     cases["reflecting_drift"].domain, Q(2)),
        Intervention("damped_wide", "damped",
                     cases["damped_drift"].domain, Q(3)),
    )
    first, second = Q("4/5"), Q("9/10")
    return {
        "restricted_only": choose_cheapest_separating_intervention(menu[:2], first, second),
        "full_menu": choose_cheapest_separating_intervention(menu, first, second),
        "restricted_equivalence_classes": [
            [str(x) for x in group]
            for group in observational_equivalence_classes(
                menu[:2], (Q("3/5"), first, second))
        ],
        "warning": "Exact constructed physics baseline, not an AI result or novel algorithm.",
    }


if __name__ == "__main__":
    print(json.dumps(demonstration(), indent=2, sort_keys=True))
