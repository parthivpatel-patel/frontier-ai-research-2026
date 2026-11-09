"""Protocol 169: calibration-only, equal-source coverage threshold selector.

Pure standard-library implementation. Prospective and not yet executed.
No held-out data or correctness labels are accepted by this interface.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, inf
from typing import Iterable


@dataclass(frozen=True)
class CalibrationRow:
    source_id: str
    family_id: str
    variant_id: str
    method_id: str
    score: float


@dataclass(frozen=True)
class FrozenThreshold:
    method_id: str
    threshold: float
    target_coverage: float
    achieved_coverage: float
    source_count: int
    variant_count: int


def freeze_thresholds(
    rows: Iterable[CalibrationRow], target_coverage: float
) -> dict[str, FrozenThreshold]:
    """Choose thresholds independently per method, using calibration scores only.

    Score orientation: higher means more likely correct. Acceptance is score >=
    threshold. An infinite positive threshold is the all-abstain sentinel.
    All-answer is represented by the smallest observed finite score.
    """
    if isinstance(target_coverage, bool) or not isinstance(target_coverage, (int, float)):
        raise ValueError("target coverage must be numeric")
    if not isfinite(target_coverage) or not 0 <= target_coverage <= 1:
        raise ValueError("target coverage must be finite and within [0, 1]")

    records = list(rows)
    if not records:
        raise ValueError("empty calibration rows")
    by_method: dict[str, dict[tuple[str, str], CalibrationRow]] = {}
    family_by_source: dict[str, str] = {}
    for row in records:
        if not isinstance(row, CalibrationRow):
            raise ValueError("expected CalibrationRow")
        if any(not isinstance(x, str) or not x.strip() for x in (
            row.source_id, row.family_id, row.variant_id, row.method_id
        )):
            raise ValueError("identifiers must be nonempty strings")
        if isinstance(row.score, bool) or not isinstance(row.score, (int, float)) or not isfinite(row.score):
            raise ValueError("scores must be finite numbers")
        previous_family = family_by_source.setdefault(row.source_id, row.family_id)
        if previous_family != row.family_id:
            raise ValueError("source assigned to multiple families")
        method_rows = by_method.setdefault(row.method_id, {})
        key = (row.source_id, row.variant_id)
        if key in method_rows:
            raise ValueError("duplicate source/variant/method")
        method_rows[key] = row

    expected = set(next(iter(by_method.values())))
    if any(set(method_rows) != expected for method_rows in by_method.values()):
        raise ValueError("methods must have identical source/variant sets")
    sources = {key[0] for key in expected}
    result: dict[str, FrozenThreshold] = {}
    for method_id, method_rows in sorted(by_method.items()):
        scores = sorted({float(row.score) for row in method_rows.values()})
        source_scores: dict[str, list[float]] = {source: [] for source in sources}
        for row in method_rows.values():
            source_scores[row.source_id].append(float(row.score))

        def coverage(threshold: float) -> float:
            return sum(
                sum(score >= threshold for score in values) / len(values)
                for values in source_scores.values()
            ) / len(source_scores)

        # Ties: minimum distance, then lower achieved coverage, then higher threshold.
        # +inf is valid only as an abstention sentinel, not an input score.
        choices = [(abs(coverage(t) - target_coverage), coverage(t), -t, t)
                   for t in [*scores, inf]]
        _, achieved, _, selected = min(choices)
        result[method_id] = FrozenThreshold(
            method_id, selected, float(target_coverage), achieved,
            len(sources), len(expected)
        )
    return result
