"""Protocol 108: calibration-only familywise coverage selection.

Pure standard-library implementation. No test labels, test scores, or inference.
A score threshold accepts score >= threshold. Exact ties are never split.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite, nextafter
from typing import Mapping, Sequence


@dataclass(frozen=True)
class CalibrationRow:
    claim_id: str
    family: str
    score: float

    def __post_init__(self):
        if not isinstance(self.claim_id, str) or not self.claim_id.strip():
            raise ValueError("invalid claim_id")
        if not isinstance(self.family, str) or not self.family.strip():
            raise ValueError("invalid family")
        if type(self.score) not in (float, int) or not isfinite(self.score):
            raise ValueError("score must be finite numeric, not bool")


@dataclass(frozen=True)
class Selection:
    family: str
    threshold: float
    accepted: int
    total: int
    achieved_coverage: float
    target_coverage: float
    within_tolerance: bool


def calibrate(rows: Sequence[CalibrationRow],
              targets: Mapping[str, float],
              tolerance: float) -> dict[str, Selection]:
    """Choose nearest feasible coverage for each family, ties favor fewer accepts.

    Selection uses calibration scores only. A threshold above maximum score
    yields zero acceptance. Thresholds are intended for subsequent frozen
    application to held-out scores; no test data enter this function.
    """
    if type(tolerance) not in (float, int) or not isfinite(tolerance) or not 0 <= tolerance <= 1:
        raise ValueError("invalid tolerance")
    if not targets or any(not isinstance(f, str) or not f.strip() or
                          type(t) not in (int, float) or not isfinite(t) or not 0 <= t <= 1
                          for f, t in targets.items()):
        raise ValueError("invalid targets")
    if any(not isinstance(r, CalibrationRow) for r in rows):
        raise ValueError("invalid calibration row")
    ids = [r.claim_id for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate calibration claim_id")
    families = {r.family for r in rows}
    if families != set(targets):
        raise ValueError("each target family must have calibration rows")
    result = {}
    for family, target in targets.items():
        scores = sorted((r.score for r in rows if r.family == family), reverse=True)
        n = len(scores)
        # Each unique score is a feasible inclusive threshold. The value
        # immediately above the maximum score represents accepting none.
        maximum = scores[0]
        none_threshold = nextafter(maximum, float("inf"))
        if not isfinite(none_threshold):
            raise ValueError("maximum score too large for finite zero-accept threshold")
        candidates = [(0, none_threshold)]
        for score in sorted(set(scores), reverse=True):
            count = sum(s >= score for s in scores)
            candidates.append((count, score))
        count, threshold = min(candidates, key=lambda x: (abs(x[0] / n - target), x[0]))
        coverage = count / n
        result[family] = Selection(family, threshold, count, n, coverage,
                                   float(target), abs(coverage - target) <= tolerance)
    return result


def apply_frozen_threshold(rows: Sequence[CalibrationRow],
                           thresholds: Mapping[str, Selection]) -> dict[str, bool]:
    """Apply prespecified thresholds; never recalibrate on held-out data."""
    if any(not isinstance(r, CalibrationRow) for r in rows):
        raise ValueError("invalid row")
    if len({r.claim_id for r in rows}) != len(rows):
        raise ValueError("duplicate claim_id")
    if any(r.family not in thresholds for r in rows):
        raise ValueError("unknown family")
    if any(not isinstance(s, Selection) for s in thresholds.values()):
        raise ValueError("invalid selection")
    return {r.claim_id: r.score >= thresholds[r.family].threshold for r in rows}
