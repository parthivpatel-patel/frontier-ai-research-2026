"""Protocol 048: validation-frozen selective risk, standard-library only.

Input rows are mappings with: split, group, label, and one score per method.
label=1 denotes unsafe/incorrect acceptance, label=0 denotes safe.
Scores are confidence values: larger means more likely to accept.
This module never trains models or changes the evaluation set.
"""
from __future__ import annotations

import math
from collections import defaultdict


def validate(rows, methods):
    if not methods or len(set(methods)) != len(methods):
        raise ValueError("methods must be distinct and nonempty")
    seen_ids = set()
    groups = defaultdict(set)
    counts = defaultdict(int)
    for row in rows:
        for key in ("id", "split", "group", "label", *methods):
            if key not in row:
                raise ValueError(f"missing field: {key}")
        if row["id"] in seen_ids:
            raise ValueError("duplicate id")
        seen_ids.add(row["id"])
        if row["split"] not in ("validation", "test"):
            raise ValueError("unknown split")
        if row["label"] not in (0, 1) or type(row["label"]) is not int:
            raise ValueError("label must be 0 or 1")
        for method in methods:
            score = row[method]
            if type(score) not in (int, float) or not math.isfinite(score) or not 0 <= score <= 1:
                raise ValueError("invalid confidence")
        groups[row["group"]].add(row["split"])
        counts[row["split"]] += 1
    if not all(counts[s] for s in ("validation", "test")):
        raise ValueError("both splits required")
    if any(len(splits) > 1 for splits in groups.values()):
        raise ValueError("group leakage across splits")


def fit_threshold(validation, method, target_coverage):
    """Select a threshold using validation only; accept score >= threshold.

    Ties are never broken using test outcomes. Coverage may differ from target.
    Threshold is the largest attainable cutoff meeting target coverage.
    """
    if not 0 < target_coverage <= 1:
        raise ValueError("target coverage must be in (0,1]")
    scores = sorted((r[method] for r in validation), reverse=True)
    n = len(scores)
    if n == 0:
        raise ValueError("empty validation set")
    index = math.ceil(n * target_coverage) - 1
    return scores[index]


def evaluate(rows, methods, coverages=(0.25, 0.5, 0.75)):
    """Return actual test coverage and selective risk; no test-time tuning."""
    rows = list(rows)
    methods = tuple(methods)
    validate(rows, methods)
    val = [r for r in rows if r["split"] == "validation"]
    test = [r for r in rows if r["split"] == "test"]
    output = []
    for coverage in coverages:
        for method in methods:
            threshold = fit_threshold(val, method, coverage)
            accepted = [r for r in test if r[method] >= threshold]
            output.append({
                "method": method,
                "target_validation_coverage": coverage,
                "frozen_threshold": threshold,
                "test_count": len(test),
                "accepted_count": len(accepted),
                "test_coverage": len(accepted) / len(test),
                "unsafe_accepted_count": sum(r["label"] for r in accepted),
                "selective_risk": (
                    sum(r["label"] for r in accepted) / len(accepted)
                    if accepted else None
                ),
            })
    return output
