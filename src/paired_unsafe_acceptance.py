"""Paired unsafe-acceptance audit for independent source clusters (Protocol 019).

Classical exact McNemar testing, not novel statistics or real model results.
Input provenance is caller-supplied and unverified. Standard library only.
"""
from __future__ import annotations

import json
import math


def _threshold(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number in [0,1]")
    result = float(value)
    if not math.isfinite(result) or not 0 <= result <= 1:
        raise ValueError(f"{name} must be a finite number in [0,1]")
    return result


def exact_mcnemar(b: int, c: int) -> dict:
    """Exact two-sided binomial McNemar test for A-only and B-only unsafe pairs.

    The log10 p-value is returned so extreme evidence is not silently rounded
    to zero by floating-point underflow. No asymptotic chi-square approximation.
    """
    if (isinstance(b, bool) or isinstance(c, bool)
            or not isinstance(b, int) or not isinstance(c, int)
            or b < 0 or c < 0 or b + c > 10000):
        raise ValueError("discordant counts must be nonnegative integers with sum <= 10000")
    n = b + c
    if n == 0:
        return {"discordant_pairs": 0, "two_sided_p": 1.0, "log10_two_sided_p": 0.0}
    k = min(b, c)
    log_terms = [
        math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1)
        - n * math.log(2)
        for j in range(k + 1)
    ]
    top = max(log_terms)
    log_tail = top + math.log(math.fsum(math.exp(t - top) for t in log_terms))
    log_p = min(0.0, math.log(2) + log_tail)
    return {
        "discordant_pairs": n,
        "two_sided_p": math.exp(log_p),
        "log10_two_sided_p": log_p / math.log(10),
    }


def paired_unsafe_acceptance_audit(
    rows: list[dict], *, method_ids: tuple[str, str],
    min_coverage: float, max_coverage_gap: float,
) -> dict:
    """Aggregate repeated predictions, then compare two frozen methods.

    Rows contain method_id, source_id, accepted, incorrect. A source is unsafe
    if ANY accepted prediction is independently adjudicated incorrect.
    Both methods must have rows for exactly the same eligible source IDs.
    The coverage gate is descriptive, not an equivalence test.
    """
    if (not isinstance(method_ids, tuple) or len(method_ids) != 2
            or any(not isinstance(m, str) or not m or m.strip() != m
                   or len(m) > 128 for m in method_ids)
            or method_ids[0] == method_ids[1]):
        raise ValueError("exactly two distinct fixed method IDs are required")
    minimum = _threshold(min_coverage, "min_coverage")
    gap_limit = _threshold(max_coverage_gap, "max_coverage_gap")
    if not isinstance(rows, list) or not rows:
        raise ValueError("at least one eligible source row is required")

    by_method: dict[str, dict[str, dict[str, bool]]] = {m: {} for m in method_ids}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {
            "method_id", "source_id", "accepted", "incorrect"
        }:
            raise ValueError("invalid method-row schema")
        method, source = row["method_id"], row["source_id"]
        accepted, incorrect = row["accepted"], row["incorrect"]
        if not isinstance(method, str) or method not in by_method:
            raise ValueError("method not in fixed roster")
        if (not isinstance(source, str) or not source or source.strip() != source
                or len(source) > 256):
            raise ValueError("invalid source ID")
        if not isinstance(accepted, bool):
            raise ValueError("accepted must be boolean")
        if incorrect is not None and not isinstance(incorrect, bool):
            raise ValueError("incorrect must be boolean or None")
        if accepted and incorrect is None:
            raise ValueError("accepted output requires independent correctness adjudication")
        state = by_method[method].setdefault(source, {"accepted": False, "unsafe": False})
        if accepted:
            state["accepted"] = True
            state["unsafe"] = state["unsafe"] or incorrect

    a_id, b_id = method_ids
    sources = set(by_method[a_id])
    if not sources or sources != set(by_method[b_id]):
        raise ValueError("methods must share identical nonempty eligible source sets")
    n = len(sources)
    if n > 10000:
        raise ValueError("maximum 10000 independent sources supported")

    stats = {}
    for method in method_ids:
        states = by_method[method].values()
        accepted_count = sum(s["accepted"] for s in states)
        unsafe_count = sum(s["unsafe"] for s in states)
        stats[method] = {
            "eligible_sources": n,
            "accepted_sources": accepted_count,
            "unsafe_accepted_sources": unsafe_count,
            "coverage": accepted_count / n,
            "selective_failure_fraction": (
                unsafe_count / accepted_count if accepted_count else None
            ),
            "unsafe_acceptance_per_eligible": unsafe_count / n,
        }

    both = a_only = b_only = neither = 0
    for source in sources:
        x = by_method[a_id][source]["unsafe"]
        y = by_method[b_id][source]["unsafe"]
        if x and y:
            both += 1
        elif x:
            a_only += 1
        elif y:
            b_only += 1
        else:
            neither += 1

    gap = abs(stats[a_id]["coverage"] - stats[b_id]["coverage"])
    gate = (gap <= gap_limit
            and all(stats[m]["coverage"] >= minimum for m in method_ids))
    exact = exact_mcnemar(a_only, b_only)
    return {
        "analysis": "paired_source_level_descriptive_only",
        "method_order": list(method_ids),
        "n_eligible_sources": n,
        "methods": stats,
        "coverage_absolute_gap": gap,
        "declared_min_coverage": minimum,
        "declared_max_coverage_gap": gap_limit,
        "descriptive_coverage_gate_passed": gate,
        "paired_table": {
            "both_unsafe": both,
            "A_only_unsafe": a_only,
            "B_only_unsafe": b_only,
            "neither_unsafe": neither,
        },
        "difference_unsafe_acceptance_A_minus_B": (a_only - b_only) / n,
        "exact_mcnemar": exact,
        "comparison_status": (
            "descriptive_coverage_gate_passed_not_equivalence"
            if gate else "coverage_gate_failed_no_matched_coverage_claim"
        ),
        "data_provenance": "caller_supplied_unverified",
        "limitations": (
            "Exact McNemar tests paired unsafe-acceptance marginal rates, not "
            "conditional selective risk. Abstention can trivially lower unsafe "
            "acceptance. Coverage gate is not population equivalence; no post-hoc "
            "threshold tuning, optional stopping, or unblinded labels. "
            "No novelty, model superiority, or safety guarantee established."
        ),
    }


def main() -> None:
    """Small constructed demonstration; not an actual model comparison."""
    rows = [
        {"method_id": m, "source_id": source, "accepted": accepted,
         "incorrect": bad if accepted else None}
        for m, examples in (
            ("baseline", [("toy1", True, True), ("toy2", True, False),
                          ("toy3", True, False), ("toy4", True, True)]),
            ("candidate", [("toy1", True, False), ("toy2", True, False),
                           ("toy3", True, False), ("toy4", False, False)]),
        )
        for source, accepted, bad in examples
    ]
    print(json.dumps({
        "illustration": "synthetic_only",
        "audit": paired_unsafe_acceptance_audit(
            rows, method_ids=("baseline", "candidate"),
            min_coverage=0.75, max_coverage_gap=0.25,
        ),
        "novelty_established": False,
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
