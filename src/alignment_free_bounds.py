"""Alignment-free bounds on *record* overlap for repeated formal extraction.

This module uses only count vectors published in Session 018. No upstream text,
model predictions, semantic labels, inference, or downloads are required.
Counts alone cannot identify correctness, intent, or true formula alignment.
"""
from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations

# Repeated runs, not independent source documents.
PUBLISHED_COUNTS = {
    "article_78": (4, 6, 6, 5, 3),
    "article_80": (2, 1, 4, 2, 2),
    "cara_pump_requirements": (8, 4, 5, 8, 8),
    "harvesting_process": (7, 7, 5, 7, 4),
}


def pair_bounds(n: int, m: int) -> dict:
    """Tight *combinatorial* bounds assuming at most one match per record.

    For both-empty outputs, overlap fraction is undefined (not 100% agreement).
    These are record matching bounds, NOT semantic similarity estimates.
    """
    if any(isinstance(x, bool) or not isinstance(x, int) or x < 0 for x in (n, m)):
        raise ValueError("counts must be nonnegative integers")
    upper_matches = min(n, m)
    denominator = max(n, m)
    fraction = Fraction(upper_matches, denominator) if denominator else None
    return {
        "unavoidable_unmatched_occurrences": denominator - upper_matches,
        "possible_matched_record_count": [0, upper_matches],
        "max_matched_fraction": fraction,
    }


def audit(counts_by_source: dict[str, tuple[int, ...]] = PUBLISHED_COUNTS) -> dict:
    """Aggregate only within-document comparisons; no inferential statistics."""
    if not counts_by_source:
        raise ValueError("at least one source is required")
    details = {}
    all_pairs = []
    adjacent_total = 0
    for source, counts in counts_by_source.items():
        if not isinstance(source, str) or not source or len(counts) < 2:
            raise ValueError("source name and at least two runs required")
        pairs = [(i, j, pair_bounds(counts[i], counts[j]))
                 for i, j in combinations(range(len(counts)), 2)]
        adjacent = sum(pair_bounds(counts[i], counts[i + 1])[
            "unavoidable_unmatched_occurrences"] for i in range(len(counts) - 1))
        adjacent_total += adjacent
        all_pairs.extend(x[2] for x in pairs)
        details[source] = {
            "runs": list(counts),
            "unordered_run_pairs": len(pairs),
            "unequal_count_pairs": sum(counts[i] != counts[j] for i, j, _ in pairs),
            "sum_unavoidable_unmatched_occurrences": sum(
                p["unavoidable_unmatched_occurrences"] for _, _, p in pairs),
            "adjacent_unavoidable_unmatched_occurrences": adjacent,
            "both_empty_pairs": sum(p["max_matched_fraction"] is None
                                    for _, _, p in pairs),
        }
    fractions = [p["max_matched_fraction"] for p in all_pairs
                 if p["max_matched_fraction"] is not None]
    mean_upper = sum(fractions, Fraction(0)) / len(fractions) if fractions else None
    return {
        "analysis": "alignment_free_cardinality_only",
        "source_documents": len(counts_by_source),
        "unordered_within_source_run_pairs": len(all_pairs),
        "unequal_count_pairs": sum(
            item["unequal_count_pairs"] for item in details.values()),
        "sum_unavoidable_unmatched_occurrences_all_pairs": sum(
            p["unavoidable_unmatched_occurrences"] for p in all_pairs),
        "sum_unavoidable_unmatched_occurrences_adjacent_pairs": adjacent_total,
        "mean_max_matched_fraction_exact": str(mean_upper) if mean_upper is not None else None,
        "mean_max_matched_fraction_decimal": float(mean_upper) if mean_upper is not None else None,
        "by_source": details,
        "limitations": (
            "Matching is hypothetical one-to-one record alignment, not semantic "
            "equivalence. Repeated runs are clustered within four original "
            "documents. Count differences can reflect splitting or merging. "
            "No formula correctness or model accuracy is inferred."
        ),
    }


def main() -> None:
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
