"""Deterministic stress tests for incomplete semantic reference sets.

Educational falsification fixture, NOT a new calibration algorithm or
population-level statistical guarantee. Standard library only.
"""
from __future__ import annotations

import json
from fractions import Fraction

from src.exact_domain_audit import Domain, Interval, Q, reflect, threshold_disagreement
from src.semantic_oracle_bounds import (
    OracleCase, joint_error_bounds, sample_error_bounds, sample_risk_decision,
)


def _domain() -> Domain:
    # Reachable next-position interval is exactly [1/2, 1].
    return Domain(
        Interval(Q("0.5"), Q("0.5")),
        Interval(Q("0"), Q("0")),
        Interval(Q("0"), Q("0.5")),
    )


def reference_omission_witness() -> dict[str, object]:
    """Identical observed references can conceal different true semantics."""
    domain = _domain()
    candidate = Q("0.8")
    supplied = OracleCase(domain, candidate, (Q("0.8"),))
    omitted_truth = Q("0.9")
    witness = (Q("0.5"), Q("0"), Q("0.35"))
    observed_value = reflect(sum(witness, Q(0)))
    assert observed_value == Q("0.85")
    assert supplied.possible_errors() == frozenset({0})
    assert threshold_disagreement(domain, candidate, omitted_truth)
    assert candidate < observed_value <= omitted_truth
    return {
        "observed_supplied_error_set": sorted(supplied.possible_errors()),
        "supplied_reference": str(Q("0.8")),
        "unobserved_alternative_reference": str(omitted_truth),
        "physical_witness": [str(x) for x in witness],
        "witness_next_position": str(observed_value),
        "candidate_predicate_true_at_witness": observed_value <= candidate,
        "alternative_predicate_true_at_witness": observed_value <= omitted_truth,
        "interpretation": "Completeness of the supplied reference set is an assumption, not a verified fact.",
    }


def denominator_stress(total_instructions: int = 100) -> dict[str, object]:
    """One accepted wrong translation can have tiny joint and maximal selected risk."""
    if isinstance(total_instructions, bool) or not isinstance(total_instructions, int) or total_instructions < 1:
        raise ValueError("total_instructions must be a positive integer")
    accepted = (OracleCase(_domain(), Q("1"), (Q("0.8"),)),)
    conditional = sample_error_bounds(accepted)
    joint = joint_error_bounds(accepted, total_instructions)
    return {
        "total_instructions": total_instructions,
        "accepted": 1,
        "accepted_error_rate": str(conditional["upper_error_rate"]),
        "joint_error_rate": str(joint["upper_joint_error_rate"]),
        "acceptance_fraction": str(Fraction(1, total_instructions)),
        "interpretation": "Finite-sample arithmetic only. Does not refute any published guarantee.",
    }


def run_stress() -> dict[str, object]:
    domain = _domain()
    complete = (OracleCase(domain, Q("0.8"), (Q("0.8"), Q("0.9"))),)
    return {
        "reference_omission": reference_omission_witness(),
        "denominator": denominator_stress(),
        "complete_supplied_set_decision_at_zero_tolerance": sample_risk_decision(complete, Q(0)),
        "guarantee_scope": "Constructed toy dynamics; no statistical or semantic completeness guarantee",
    }


if __name__ == "__main__":
    print(json.dumps(run_stress(), sort_keys=True, indent=2))
