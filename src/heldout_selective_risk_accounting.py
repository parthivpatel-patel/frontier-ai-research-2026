"""Held-out selective-risk accounting. Descriptive only; no model or inferential claims.

Rows are frozen, source-family-labeled evaluation observations. The function
never chooses thresholds from held-out scores or outcomes.
"""
from __future__ import annotations

import math


def audit_fixed_decisions(rows: list[dict], methods: tuple[str, ...]) -> dict:
    """Return per-method achieved coverage and selective risk on identical items.

    Each row: {item_id, family_id, error, decisions}, with decisions mapping
    every method to a boolean acceptance. Undefined risk is represented by None.
    """
    if not isinstance(methods, tuple) or not methods or len(set(methods)) != len(methods):
        raise ValueError("methods must be a nonempty unique tuple")
    if any(not isinstance(m, str) or not m.strip() for m in methods):
        raise ValueError("invalid method")
    if not isinstance(rows, list) or not rows:
        raise ValueError("nonempty held-out roster required")
    seen = set()
    sums = {m: [0, 0] for m in methods}
    families = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"item_id", "family_id", "error", "decisions"}:
            raise ValueError("invalid row schema")
        item, family = row["item_id"], row["family_id"]
        if not isinstance(item, str) or not item or item in seen:
            raise ValueError("missing or duplicate item identifier")
        if not isinstance(family, str) or not family:
            raise ValueError("missing source family")
        seen.add(item)
        families.add(family)
        if type(row["error"]) is not bool:
            raise ValueError("error must be adjudicated boolean")
        decisions = row["decisions"]
        if not isinstance(decisions, dict) or set(decisions) != set(methods):
            raise ValueError("all methods must have a decision for every item")
        for m in methods:
            if type(decisions[m]) is not bool:
                raise ValueError("decisions must be boolean")
            if decisions[m]:
                sums[m][0] += 1
                sums[m][1] += int(row["error"])
    n = len(rows)
    return {"items": n, "families": len(families), "methods": {
        m: {"accepted": sums[m][0], "errors_accepted": sums[m][1],
            "coverage": sums[m][0] / n,
            "selective_risk": (sums[m][1] / sums[m][0] if sums[m][0] else None)}
        for m in methods
    }}
