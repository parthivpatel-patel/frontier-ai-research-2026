"""Fail-closed equal-exposure gate for source-paired formalization evaluation.

Protocol 020. Classical repeated-sampling and paired-testing design controls,
not a new statistical estimator. Caller-supplied labels are NOT authenticated.
Standard library only. No model calls, data downloads, or external services.
"""
from __future__ import annotations

import json
import math

from src.paired_unsafe_acceptance import paired_unsafe_acceptance_audit


def _roster(values: tuple[str, ...], name: str, maximum: int) -> tuple[str, ...]:
    if (not isinstance(values, tuple) or not 1 <= len(values) <= maximum
            or any(not isinstance(x, str) or not x or x.strip() != x
                   or len(x) > 256 for x in values)
            or len(set(values)) != len(values)):
        raise ValueError(f"{name} must be a nonempty tuple of unique, valid IDs")
    return values


def any_failure_probability(p: float, trials: int) -> float:
    """P(at least one failure) for independent equal-risk Bernoulli trials.

    Illustration of an assumption-dependent identity, NOT a risk estimate.
    Correlated model generations or heterogeneous sources violate its premise.
    """
    if (isinstance(p, bool) or not isinstance(p, (float, int))
            or not math.isfinite(float(p)) or not 0 <= p <= 1):
        raise ValueError("p must be finite and in [0,1]")
    if isinstance(trials, bool) or not isinstance(trials, int) or not 1 <= trials <= 10000:
        raise ValueError("trials must be an integer from 1 to 10000")
    if p == 1:
        return 1.0
    return -math.expm1(trials * math.log1p(-float(p)))


def balanced_exposure_audit(
    rows: list[dict], *, method_ids: tuple[str, str],
    source_ids: tuple[str, ...], trial_ids: tuple[str, ...],
    min_coverage: float, max_coverage_gap: float,
) -> dict:
    """Require exactly one recorded outcome for each method/source/trial.

    Each source has the same frozen trial slots for both methods. This prevents
    unequal numbers of attempts from mechanically changing an any-error rate.
    The result remains descriptive; matching slot IDs does not establish
    comparable prompts, generation policies, adjudication, or populations.
    """
    methods = _roster(method_ids, "method_ids", 2)
    if len(methods) != 2:
        raise ValueError("exactly two method IDs required")
    sources = _roster(source_ids, "source_ids", 10000)
    trials = _roster(trial_ids, "trial_ids", 32)
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")
    expected = len(methods) * len(sources) * len(trials)
    if len(rows) != expected:
        raise ValueError(f"incomplete or extra trial roster: expected {expected} rows")

    method_set, source_set, trial_set = set(methods), set(sources), set(trials)
    seen: set[tuple[str, str, str]] = set()
    old_schema_rows = []
    attempts = {m: {"accepted_attempts": 0, "unsafe_accepted_attempts": 0}
                for m in methods}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {
            "method_id", "source_id", "trial_id", "accepted", "incorrect"
        }:
            raise ValueError("invalid trial-row schema")
        method, source, trial = row["method_id"], row["source_id"], row["trial_id"]
        if (not isinstance(method, str) or method not in method_set
                or not isinstance(source, str) or source not in source_set
                or not isinstance(trial, str) or trial not in trial_set):
            raise ValueError("row outside frozen method/source/trial roster")
        key = (method, source, trial)
        if key in seen:
            raise ValueError("duplicate method/source/trial slot")
        seen.add(key)
        accepted, incorrect = row["accepted"], row["incorrect"]
        if not isinstance(accepted, bool):
            raise ValueError("accepted must be boolean")
        if accepted and not isinstance(incorrect, bool):
            raise ValueError("accepted output requires independently adjudicated boolean label")
        if not accepted and incorrect is not None:
            raise ValueError("abstained output must have incorrect=None")
        if accepted:
            attempts[method]["accepted_attempts"] += 1
            attempts[method]["unsafe_accepted_attempts"] += int(incorrect)
        old_schema_rows.append({
            "method_id": method, "source_id": source,
            "accepted": accepted, "incorrect": incorrect,
        })

    # The cardinality check plus membership and duplicate rejection proves
    # the full Cartesian product is present, without enumerating missing slots.
    assert len(seen) == expected
    paired = paired_unsafe_acceptance_audit(
        old_schema_rows, method_ids=methods,
        min_coverage=min_coverage, max_coverage_gap=max_coverage_gap,
    )
    for method in methods:
        accepted = attempts[method]["accepted_attempts"]
        attempts[method]["conditional_attempt_failure_fraction"] = (
            attempts[method]["unsafe_accepted_attempts"] / accepted
            if accepted else None
        )
    return {
        "protocol": "020_balanced_exposure",
        "analysis": "descriptive_source_paired_with_frozen_trial_roster",
        "n_eligible_sources": len(sources),
        "trial_budget_per_source_per_method": len(trials),
        "total_recorded_attempts": expected,
        "equal_exposure_roster_verified": True,
        "per_method_attempt_counts": attempts,
        "source_level_paired_audit": paired,
        "data_provenance": "caller_supplied_unverified",
        "limits": (
            "Trial IDs and equal counts alone do not prove identical generation "
            "policies, independence, equal computational effort, or valid human "
            "meaning labels. Source-level any-error and attempt-level failure "
            "have different denominators. Repeated trials are not independent "
            "sources. No model superiority or novel method established."
        ),
    }


def main() -> None:
    """Synthetic-only example: a missing B trial is rejected, not scored."""
    rows = [
        {"method_id": method, "source_id": source, "trial_id": trial,
         "accepted": True, "incorrect": trial == "r2"}
        for source in ("toy_a", "toy_b")
        for method in ("A", "B")
        for trial in ("r1", "r2")
    ]
    result = balanced_exposure_audit(
        rows, method_ids=("A", "B"), source_ids=("toy_a", "toy_b"),
        trial_ids=("r1", "r2"), min_coverage=1.0, max_coverage_gap=0.0,
    )
    print(json.dumps({
        "illustration": "synthetic_only",
        "one_attempt_failure_probability_if_iid_p_0_1": any_failure_probability(.1, 1),
        "five_attempt_any_failure_probability_if_iid_p_0_1": any_failure_probability(.1, 5),
        "audit": result,
        "novelty_established": False,
        "real_model_results": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
