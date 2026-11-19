"""Descriptive paired diagnostics for frozen, identical held-out candidates.

No statistical significance or shift-robustness claim is implied. In particular,
a shared error label is valid only when both methods assess the same answer.
"""
from __future__ import annotations

from .heldout_selective_risk_accounting import audit_fixed_decisions


def paired_fixed_decisions(rows: list[dict], method_a: str, method_b: str) -> dict:
    """Compare fixed accept/reject decisions on an identical held-out roster.

    Report both methods' marginal risk and coverage, overlap and disagreement.
    The overlap error rate is NOT a matched-coverage treatment effect.
    """
    if not isinstance(method_a, str) or not isinstance(method_b, str) or not method_a or not method_b or method_a == method_b:
        raise ValueError("two distinct method names required")
    summary = audit_fixed_decisions(rows, (method_a, method_b))
    both = a_only = b_only = neither = 0
    both_errors = a_only_errors = b_only_errors = 0
    per_family = {}
    for row in rows:
        family = row["family_id"]
        counts = per_family.setdefault(family, {"items": 0, "both": 0, "a_only": 0, "b_only": 0, "neither": 0})
        counts["items"] += 1
        a, b = row["decisions"][method_a], row["decisions"][method_b]
        if a and b:
            both += 1
            both_errors += int(row["error"])
            counts["both"] += 1
        elif a:
            a_only += 1
            a_only_errors += int(row["error"])
            counts["a_only"] += 1
        elif b:
            b_only += 1
            b_only_errors += int(row["error"])
            counts["b_only"] += 1
        else:
            neither += 1
            counts["neither"] += 1
    n = summary["items"]
    return {
        "items": n,
        "method_a": method_a,
        "method_b": method_b,
        "marginal": summary["methods"],
        "decision_cells": {"both": both, "a_only": a_only, "b_only": b_only, "neither": neither},
        "error_cells": {"both": both_errors, "a_only": a_only_errors, "b_only": b_only_errors},
        "both_accepted_error_rate": both_errors / both if both else None,
        "coverage_difference_a_minus_b": (a_only - b_only) / n,
        "selective_risk_difference_a_minus_b": (
            summary["methods"][method_a]["selective_risk"] - summary["methods"][method_b]["selective_risk"]
            if summary["methods"][method_a]["selective_risk"] is not None
            and summary["methods"][method_b]["selective_risk"] is not None else None
        ),
        "source_families": {k: per_family[k] for k in sorted(per_family)},
        "interpretation": "Descriptive paired decisions only; not cost-matched, coverage-matched, causal, or inferential.",
    }
