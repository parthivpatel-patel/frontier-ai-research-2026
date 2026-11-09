"""Protocol 170: held-out descriptive gate for frozen Protocol 169 thresholds.

No inference or significance calculation. Never recalibrates on test data.
Standard library only. Prospective; cloud execution not yet verified.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable

from research.protocol_169_calibration_selector import FrozenThreshold


@dataclass(frozen=True)
class TestRow:
    source_id: str
    family_id: str
    variant_id: str
    method_id: str
    score: float
    correct: bool


def evaluate_heldout(
    rows: Iterable[TestRow],
    frozen: dict[str, FrozenThreshold],
    calibration_source_ids: set[str],
    epsilon: float,
) -> dict:
    """Evaluate matched source/variant sets with equal source weights.

    Returns descriptive metrics and INVALID/INCONCLUSIVE/ELIGIBLE status.
    Malformed data raises ValueError and must be reported as INVALID upstream.
    """
    if isinstance(epsilon, bool) or not isinstance(epsilon, (int, float)) or not isfinite(epsilon) or not 0 <= epsilon <= 1:
        raise ValueError("epsilon must be finite and within [0,1]")
    if not frozen or any(not isinstance(k, str) or not isinstance(v, FrozenThreshold) or k != v.method_id for k, v in frozen.items()):
        raise ValueError("invalid frozen thresholds")
    if any(not isinstance(x, str) or not x.strip() for x in calibration_source_ids):
        raise ValueError("invalid calibration source IDs")
    records = list(rows)
    if not records:
        raise ValueError("empty test set")
    by_method = {method: {} for method in frozen}
    family = {}
    for r in records:
        if not isinstance(r, TestRow):
            raise ValueError("invalid test row")
        if any(not isinstance(x, str) or not x.strip() for x in (r.source_id, r.family_id, r.variant_id, r.method_id)):
            raise ValueError("missing identifier")
        if r.source_id in calibration_source_ids:
            raise ValueError("calibration/test source leakage")
        if r.method_id not in frozen:
            raise ValueError("unexpected method")
        if isinstance(r.score, bool) or not isinstance(r.score, (int, float)) or not isfinite(r.score):
            raise ValueError("invalid score")
        if not isinstance(r.correct, bool):
            raise ValueError("missing or invalid correctness")
        if r.source_id in family and family[r.source_id] != r.family_id:
            raise ValueError("inconsistent physics family")
        family[r.source_id] = r.family_id
        key = (r.source_id, r.variant_id)
        if key in by_method[r.method_id]:
            raise ValueError("duplicate test observation")
        by_method[r.method_id][key] = r
    expected = set(next(iter(by_method.values())))
    if not expected or any(set(v) != expected for v in by_method.values()):
        raise ValueError("methods have mismatched test observations")
    metrics = {}
    for method, observations in sorted(by_method.items()):
        threshold = frozen[method].threshold
        if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) or threshold != threshold:
            raise ValueError("invalid frozen threshold")
        per_source = {}
        for r in observations.values():
            per_source.setdefault(r.source_id, []).append(r)
        source_coverage = []
        source_yield = []
        accepted = 0
        accepted_correct = 0
        correct_total = 0
        rejected_correct = 0
        for variants in per_source.values():
            accepts = [r.score >= threshold for r in variants]
            source_coverage.append(sum(accepts) / len(variants))
            source_yield.append(sum(a and r.correct for a, r in zip(accepts, variants)) / len(variants))
            accepted += sum(accepts)
            accepted_correct += sum(a and r.correct for a, r in zip(accepts, variants))
            correct_total += sum(r.correct for r in variants)
            rejected_correct += sum((not a) and r.correct for a, r in zip(accepts, variants))
        metrics[method] = {
            "coverage": sum(source_coverage) / len(source_coverage),
            "correct_yield": sum(source_yield) / len(source_yield),
            "conditional_accuracy": accepted_correct / accepted if accepted else None,
            "false_rejection_rate": rejected_correct / correct_total if correct_total else None,
            "source_count": len(per_source),
        }
    methods = sorted(metrics)
    comparisons = {}
    for i, left in enumerate(methods):
        for right in methods[i + 1:]:
            gap = abs(metrics[left]["coverage"] - metrics[right]["coverage"])
            status = ("INCONCLUSIVE_AT_MATCHED_COVERAGE"
                      if gap > epsilon or metrics[left]["coverage"] == 0 or metrics[right]["coverage"] == 0
                      else "ELIGIBLE_FOR_INFERENCE")
            comparisons[f"{left} vs {right}"] = {
                "status": status, "absolute_coverage_gap": gap,
                "yield_difference": metrics[left]["correct_yield"] - metrics[right]["correct_yield"],
            }
    return {"methods": metrics, "comparisons": comparisons,
            "warning": "Descriptive only; eligibility is not significance or superiority."}
