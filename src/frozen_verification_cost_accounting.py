"""Frozen, per-item verification-cost accounting; descriptive, not causal.

Costs must be measured in one declared nonnegative unit (e.g. billed tokens,
wall-clock seconds on a fixed runner, or API dollars). Never combine units.
"""
from __future__ import annotations
import math
from .heldout_selective_risk_accounting import audit_fixed_decisions


def audit_verification_costs(rows: list[dict], methods: tuple[str, ...],
                             costs: dict[str, dict[str, float]],
                             unit: str) -> dict:
    """Audit full-roster costs, including abstentions and failed verifications.

    costs[method][item_id] is the complete measured verification cost for
    that method and item, independent of whether its decision is acceptance.
    Missing, negative, nonfinite, boolean, or extra cost entries are errors.
    """
    summary = audit_fixed_decisions(rows, methods)
    if not isinstance(unit, str) or not unit.strip():
        raise ValueError("one explicit cost unit required")
    ids = {r["item_id"] for r in rows}
    if not isinstance(costs, dict) or set(costs) != set(methods):
        raise ValueError("cost methods must match decisions")
    totals = {}
    for method in methods:
        by_item = costs[method]
        if not isinstance(by_item, dict) or set(by_item) != ids:
            raise ValueError("costs must cover exactly the held-out roster")
        vals = list(by_item.values())
        if any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 for v in vals):
            raise ValueError("costs must be finite nonnegative numbers")
        total = math.fsum(vals)
        if not math.isfinite(total):
            raise ValueError("total cost overflow")
        totals[method] = {
            "total": total, "per_question": total / len(rows),
            "accepted": summary["methods"][method]["accepted"],
            "coverage": summary["methods"][method]["coverage"],
            "selective_risk": summary["methods"][method]["selective_risk"],
        }
    return {
        "unit": unit, "items": len(rows), "methods": totals,
        "interpretation": (
            "Measured full-roster cost only; matched budget requires an "
            "externally preregistered tolerance and common measurement protocol. "
            "Equal totals do not establish equal compute or causal superiority."
        ),
    }
