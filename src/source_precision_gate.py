"""Exact zero-failure feasibility arithmetic for independent source clusters.

Planning-only. Not a model evaluation, novel statistical method or safety guarantee.
No external dependencies or data downloads.
"""
from __future__ import annotations

import json
import math


def _alpha(value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError("alpha must be a number")
    value = float(value)
    if not math.isfinite(value) or not 0 < value < 1:
        raise ValueError("alpha must lie strictly between 0 and 1")
    return value


def zero_failure_upper_bound(n_accepted_sources: int, *, alpha: float = 0.05) -> float:
    """Exact one-sided binomial upper bound when ZERO source failures occur.

    Requires independent, identically distributed source-level Bernoulli outcomes,
    a fixed evaluation protocol and no optional stopping.
    """
    a = _alpha(alpha)
    if (isinstance(n_accepted_sources, bool)
            or not isinstance(n_accepted_sources, int)
            or n_accepted_sources < 1):
        raise ValueError("at least one accepted independent source is required")
    return -math.expm1(math.log(a) / n_accepted_sources)


def minimum_accepted_sources(target_risk: float, *, alpha: float = 0.05) -> int:
    """Smallest integer n with zero-failure upper bound <= target_risk."""
    a = _alpha(alpha)
    if isinstance(target_risk, bool) or not isinstance(target_risk, (int, float)):
        raise ValueError("target_risk must be numeric")
    r = float(target_risk)
    if not math.isfinite(r) or not 0 < r < 1:
        raise ValueError("target_risk must lie strictly between 0 and 1")
    estimate = math.ceil(math.log(a) / math.log1p(-r))
    n = max(1, estimate)
    # Guard against a floating-point off-by-one near exact boundaries.
    while zero_failure_upper_bound(n, alpha=a) > r:
        n += 1
    while n > 1 and zero_failure_upper_bound(n - 1, alpha=a) <= r:
        n -= 1
    return n


def source_risk_summary(rows: list[dict], *, alpha: float = 0.05) -> dict:
    """Collapse repeated outputs into source-level ANY-incorrect accepted decisions.

    Each row: source_id (canonical nonempty string), accepted (bool),
    incorrect (bool for accepted rows; None or bool for abstained rows).
    Never use repeated predictions as independent samples.
    """
    a = _alpha(alpha)
    if not isinstance(rows, list) or not rows:
        raise ValueError("at least one eligible source row is required")
    groups: dict[str, dict[str, bool]] = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"source_id", "accepted", "incorrect"}:
            raise ValueError("rows require exactly source_id, accepted and incorrect")
        source = row["source_id"]
        accepted = row["accepted"]
        incorrect = row["incorrect"]
        if (not isinstance(source, str) or not source
                or source.strip() != source or len(source) > 256):
            raise ValueError("invalid source ID")
        if not isinstance(accepted, bool):
            raise ValueError("accepted must be a boolean")
        if incorrect is not None and not isinstance(incorrect, bool):
            raise ValueError("incorrect must be a boolean or None")
        if accepted and incorrect is None:
            raise ValueError("accepted predictions require adjudicated correctness")
        state = groups.setdefault(source, {"accepted": False, "failed": False})
        if accepted:
            state["accepted"] = True
            state["failed"] = state["failed"] or incorrect
    n_sources = len(groups)
    n_accepted = sum(s["accepted"] for s in groups.values())
    n_failed = sum(s["failed"] for s in groups.values())
    return {
        "analysis": "source_clustered_descriptive_only",
        "n_eligible_sources": n_sources,
        "n_accepted_sources": n_accepted,
        "n_failed_accepted_sources": n_failed,
        "coverage": n_accepted / n_sources,
        "observed_failure_fraction": (n_failed / n_accepted if n_accepted else None),
        "one_sided_upper_if_zero_failures": (
            zero_failure_upper_bound(n_accepted, alpha=a)
            if n_accepted and n_failed == 0 else None
        ),
        "limitations": (
            "Zero-failure bound applies only with independent iid sources, "
            "fixed selection and no multiple testing. Nonzero failures require "
            "a separately implemented exact interval; no actual model evaluation."
        ),
    }


def main() -> None:
    """Print hypothetical design figures only; never score real predictions."""
    print(json.dumps({
        "analysis": "hypothetical_zero_failure_precision_planning",
        "alpha": 0.05,
        "source_count_upper_bounds": {
            str(n): round(zero_failure_upper_bound(n), 8)
            for n in (4, 15, 30, 59, 299)
        },
        "minimum_accepted_sources": {
            str(target): minimum_accepted_sources(target)
            for target in (0.10, 0.05, 0.01)
        },
        "real_model_results": False,
        "scientific_novelty_established": False,
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
