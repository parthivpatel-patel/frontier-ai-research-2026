"""Prospective budget-equivalence gate for frozen full-roster cost audits.

Descriptive validation only: never infer equal computational work from equal
wall-clock times or equal billed tokens. No held-out threshold optimization.
"""
from __future__ import annotations
import math


def audit_budget_equivalence(cost_audit: dict, left: str, right: str,
                             tolerance: float = 0.05) -> dict:
    """Compare measured full-roster totals under a preregistered tolerance.

    Equivalence is defined relative to the larger total. Both-zero totals
    are flagged as uninformative rather than proof of resource equivalence.
    The input audit must come from audit_verification_costs; provenance and
    physical comparability of units require external validation.
    """
    if type(tolerance) not in (float, int) or not math.isfinite(tolerance) or not 0 <= tolerance < 1:
        raise ValueError("tolerance must be a finite fraction in [0,1)")
    if not isinstance(cost_audit, dict) or not isinstance(cost_audit.get("unit"), str) or not cost_audit["unit"].strip():
        raise ValueError("cost audit requires a declared unit")
    methods = cost_audit.get("methods")
    if not isinstance(methods, dict) or not isinstance(left, str) or not isinstance(right, str) or left == right:
        raise ValueError("two distinct method names required")
    if left not in methods or right not in methods:
        raise ValueError("methods absent from audit")
    totals = []
    for method in (left, right):
        record = methods[method]
        if not isinstance(record, dict):
            raise ValueError("invalid method record")
        value = record.get("total")
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
            raise ValueError("invalid full-roster total")
        totals.append(value)
    a, b = totals
    maximum = max(a, b)
    gap = abs(a - b) / maximum if maximum else None
    return {
        "left": left, "right": right, "unit": cost_audit["unit"],
        "left_total": a, "right_total": b,
        "relative_gap": gap, "tolerance": float(tolerance),
        "passes_measured_budget_gate": gap is not None and gap <= tolerance,
        "uninformative_zero_cost": maximum == 0,
        "warning": ("Measured-cost equivalence only; not proof of equal compute, "
                    "equal verification quality, or statistical superiority. "
                    "Tolerance must be frozen before held-out evaluation."),
    }
