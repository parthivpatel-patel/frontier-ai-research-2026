"""Acceptance-set diagnostics for paired frozen-policy evaluations.

Pure standard-library arithmetic; no model inference or external dependencies.
This is evaluation infrastructure, not empirical evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class PairedDecision:
    item_id: str
    family_id: str
    temporal_accept: bool
    baseline_accept: bool
    temporal_error: int
    baseline_error: int


def _validate(rows: Iterable[PairedDecision]) -> list[PairedDecision]:
    items = list(rows)
    if not items:
        raise ValueError("At least one paired item is required")
    seen = set()
    for r in items:
        if not isinstance(r, PairedDecision):
            raise TypeError("Each row must be PairedDecision")
        if not isinstance(r.item_id, str) or not r.item_id.strip():
            raise ValueError("Invalid item_id")
        if r.item_id in seen:
            raise ValueError("Duplicate item_id")
        seen.add(r.item_id)
        if not isinstance(r.family_id, str) or not r.family_id.strip():
            raise ValueError("Invalid family_id")
        if type(r.temporal_accept) is not bool or type(r.baseline_accept) is not bool:
            raise TypeError("Acceptance decisions must be bool")
        if type(r.temporal_error) is not int or r.temporal_error not in (0, 1):
            raise ValueError("temporal_error must be 0 or 1")
        if type(r.baseline_error) is not int or r.baseline_error not in (0, 1):
            raise ValueError("baseline_error must be 0 or 1")
    return items


def acceptance_diagnostics(rows: Iterable[PairedDecision]) -> dict:
    """Return exact paired policy counts and descriptive error diagnostics.

    All error labels are required, including on rejected items, so full-coverage
    comparisons are not silently computed on different subsets. Undefined
    conditional risks are represented by None, never zero.
    """
    items = _validate(rows)
    n = len(items)
    both = [r for r in items if r.temporal_accept and r.baseline_accept]
    t_only = [r for r in items if r.temporal_accept and not r.baseline_accept]
    b_only = [r for r in items if r.baseline_accept and not r.temporal_accept]
    neither = [r for r in items if not r.temporal_accept and not r.baseline_accept]
    t = both + t_only
    b = both + b_only

    def risk(group, arm):
        return sum(getattr(r, arm + "_error") for r in group) / len(group) if group else None

    return {
        "n": n,
        "n_families": len({r.family_id for r in items}),
        "both": len(both),
        "temporal_only": len(t_only),
        "baseline_only": len(b_only),
        "neither": len(neither),
        "temporal_coverage": len(t) / n,
        "baseline_coverage": len(b) / n,
        "temporal_selective_risk": risk(t, "temporal"),
        "baseline_selective_risk": risk(b, "baseline"),
        "common_temporal_error": risk(both, "temporal"),
        "common_baseline_error": risk(both, "baseline"),
        "temporal_only_error": risk(t_only, "temporal"),
        "baseline_only_error": risk(b_only, "baseline"),
        "full_temporal_error": risk(items, "temporal"),
        "full_baseline_error": risk(items, "baseline"),
        "paired_full_discordance_t_wrong_b_right": sum(
            r.temporal_error == 1 and r.baseline_error == 0 for r in items
        ),
        "paired_full_discordance_b_wrong_t_right": sum(
            r.baseline_error == 1 and r.temporal_error == 0 for r in items
        ),
    }
