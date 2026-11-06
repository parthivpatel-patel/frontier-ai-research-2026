"""Protocol 107: descriptive risk estimators. No calibration or inference claims.

This module intentionally accepts *counts*, not model predictions. It cannot
select thresholds or establish matched coverage; those require separate audits.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite, fsum
from typing import Mapping


@dataclass(frozen=True)
class Cell:
    accepted_safe: int
    accepted_unsafe: int

    def __post_init__(self) -> None:
        for value in (self.accepted_safe, self.accepted_unsafe):
            if type(value) is not int or value < 0:
                raise ValueError("counts must be nonnegative integers (not bool)")

    @property
    def accepted(self) -> int:
        return self.accepted_safe + self.accepted_unsafe

    @property
    def risk(self) -> float | None:
        return self.accepted_unsafe / self.accepted if self.accepted else None


def summarize(cells: Mapping[str, Cell], weights: Mapping[str, float]) -> dict:
    """Report pooled and prespecified family-standardized unsafe risk.

    A positive-weight family with zero accepted claims makes standardized
    risk undefined. A zero-acceptance total makes pooled risk undefined.
    This function does not calculate confidence intervals or causal effects.
    """
    if not cells or set(cells) != set(weights):
        raise ValueError("nonempty identical family sets required")
    if any(not isinstance(f, str) or not f.strip() for f in cells):
        raise ValueError("family names must be nonempty strings")
    if any(not isinstance(c, Cell) for c in cells.values()):
        raise ValueError("all cells must be Cell instances")
    if any(type(w) not in (int, float) or not isfinite(w) or w < 0
           for w in weights.values()):
        raise ValueError("weights must be finite nonnegative numbers")
    if not abs(fsum(weights.values()) - 1.0) <= 1e-12:
        raise ValueError("weights must sum to one")
    accepted = sum(c.accepted for c in cells.values())
    unsafe = sum(c.accepted_unsafe for c in cells.values())
    pooled = unsafe / accepted if accepted else None
    standardized = (
        None if any(weights[f] > 0 and cells[f].risk is None for f in cells)
        else fsum(weights[f] * (cells[f].risk or 0.0) for f in cells)
    )
    return {
        "families": {
            f: {"accepted_safe": c.accepted_safe,
                "accepted_unsafe": c.accepted_unsafe,
                "accepted_total": c.accepted,
                "unsafe_risk": c.risk}
            for f, c in cells.items()
        },
        "pooled_unsafe_risk": pooled,
        "standardized_unsafe_risk": standardized,
        "accepted_total": accepted,
        "accepted_unsafe_total": unsafe,
        "weights": dict(weights),
    }
