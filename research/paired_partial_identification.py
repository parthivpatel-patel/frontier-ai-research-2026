"""Protocol 058: sharp finite-sample paired bounds with unresolved physical truth.

No inference, model results, or novelty claims. Caller-supplied data are unverified.
"""
from __future__ import annotations


def paired_truth_bounds(rows: list[dict]) -> dict:
    """Compute exact identification bounds; candidate minus baseline.

    Each row has id, source_id, baseline, candidate, false_claim.
    Decisions are booleans; false_claim is bool or None (unresolved).
    This is descriptive identification, NOT a confidence interval.
    """
    if not isinstance(rows, list) or not rows:
        raise ValueError("nonempty list required")
    ids, sources = set(), set()
    known_baseline = known_candidate = known_difference = 0
    unresolved_baseline = unresolved_candidate = 0
    unresolved_negative = unresolved_positive = 0
    baseline_accepted = candidate_accepted = unresolved = 0
    observed_baseline_accepted = observed_candidate_accepted = 0
    observed_baseline_errors = observed_candidate_errors = 0
    for row in rows:
        if not isinstance(row, dict) or set(row) != {
            "id", "source_id", "baseline", "candidate", "false_claim"
        }:
            raise ValueError("invalid row schema")
        identifier, source = row["id"], row["source_id"]
        if any(not isinstance(s, str) or not s or s.strip() != s or len(s) > 256
               for s in (identifier, source)):
            raise ValueError("invalid identifier or source")
        if identifier in ids:
            raise ValueError("duplicate claim identifier")
        ids.add(identifier)
        sources.add(source)
        b, c, y = row["baseline"], row["candidate"], row["false_claim"]
        if not isinstance(b, bool) or not isinstance(c, bool):
            raise ValueError("acceptance decisions must be booleans")
        if y is not None and not isinstance(y, bool):
            raise ValueError("physical truth must be boolean or unresolved")
        baseline_accepted += b
        candidate_accepted += c
        if y is None:
            unresolved += 1
            unresolved_baseline += b
            unresolved_candidate += c
            unresolved_negative += c < b
            unresolved_positive += c > b
        else:
            known_baseline += b and y
            known_candidate += c and y
            known_difference += (int(c) - int(b)) * int(y)
            observed_baseline_accepted += b
            observed_candidate_accepted += c
            observed_baseline_errors += b and y
            observed_candidate_errors += c and y
    n = len(rows)
    return {
        "analysis": "sharp_finite_sample_partial_identification_not_inference",
        "n_claims": n,
        "n_source_clusters": len(sources),
        "n_unresolved": unresolved,
        "unresolved_fraction": unresolved / n,
        "baseline_coverage": baseline_accepted / n,
        "candidate_coverage": candidate_accepted / n,
        "baseline_unsafe_bounds": [known_baseline / n,
                                   (known_baseline + unresolved_baseline) / n],
        "candidate_unsafe_bounds": [known_candidate / n,
                                    (known_candidate + unresolved_candidate) / n],
        "candidate_minus_baseline_unsafe_bounds": [
            (known_difference - unresolved_negative) / n,
            (known_difference + unresolved_positive) / n,
        ],
        "observed_only_error_among_accepted": {
            "baseline": (observed_baseline_errors / observed_baseline_accepted
                         if observed_baseline_accepted else None),
            "candidate": (observed_candidate_errors / observed_candidate_accepted
                          if observed_candidate_accepted else None),
        },
        "observed_accepted_denominators": {
            "baseline": observed_baseline_accepted,
            "candidate": observed_candidate_accepted,
        },
        "strict_improvement_identified": (
            known_difference + unresolved_positive < 0
        ),
        "provenance": "caller_supplied_unverified",
        "warning": "Bounds are not confidence intervals; coverage and independent physical adjudication remain mandatory.",
    }
