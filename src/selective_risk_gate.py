"""Exact one-sided selective-risk planning gate for source-clustered AI outputs.

Pre-registered in Protocol 018. Classical binomial inference, not a novel
statistical method, model-performance measurement or safety certification.
Standard library only; all included examples are synthetic.
"""
from __future__ import annotations

import json
import math

from src.source_precision_gate import _alpha, source_risk_summary, zero_failure_upper_bound


def _counts(failures: int, accepted: int) -> None:
    if (isinstance(failures, bool) or isinstance(accepted, bool)
            or not isinstance(failures, int) or not isinstance(accepted, int)
            or accepted < 1 or accepted > 10000
            or failures < 0 or failures > accepted):
        raise ValueError("require integer 0 <= failures <= accepted <= 10000, accepted >= 1")


def binomial_cdf(k: int, n: int, p: float) -> float:
    """P[Binomial(n,p) <= k], with log-sum-exp to avoid tiny PMF underflow."""
    _counts(k, n)
    if isinstance(p, bool) or not isinstance(p, (int, float)):
        raise ValueError("p must be a finite probability")
    p = float(p)
    if not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError("p must lie in [0,1]")
    if p == 0:
        return 1.0
    if p == 1:
        return 1.0 if k == n else 0.0
    if k == n:
        return 1.0
    logp, logq = math.log(p), math.log1p(-p)
    lg_n = math.lgamma(n + 1)
    terms = [
        lg_n - math.lgamma(j + 1) - math.lgamma(n - j + 1)
        + j * logp + (n - j) * logq
        for j in range(k + 1)
    ]
    highest = max(terms)
    return min(1.0, math.exp(highest) * math.fsum(math.exp(t - highest) for t in terms))


def exact_one_sided_upper(failures: int, accepted: int, *, alpha: float = 0.05) -> float:
    """One-sided Clopper-Pearson upper bound for k source failures among n accepted.

    Valid for a single fixed evaluation under the binomial model; not a paired
    method-comparison test, nor valid after arbitrary threshold search/peeking.
    """
    _counts(failures, accepted)
    a = _alpha(alpha)
    if failures == 0:
        return zero_failure_upper_bound(accepted, alpha=a)
    if failures == accepted:
        return 1.0
    if failures == accepted - 1:
        return math.exp(math.log1p(-a) / accepted)
    lo, hi = 0.0, 1.0
    for _ in range(75):
        mid = (lo + hi) / 2.0
        if binomial_cdf(failures, accepted, mid) > a:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def fixed_roster_risk_audit(
    rows: list[dict], *, method_ids: tuple[str, ...], alpha: float = 0.05
) -> dict:
    """Descriptive source-level audit with Bonferroni upper bounds.

    A fixed, declared roster and identical eligible source sets are required.
    Each row has method_id, source_id, accepted, incorrect. All repeated rows
    for the same source are collapsed with ANY accepted error counting as failure.
    """
    a = _alpha(alpha)
    if (not isinstance(method_ids, tuple) or not 1 <= len(method_ids) <= 20
            or any(not isinstance(m, str) or not m or m.strip() != m
                   or len(m) > 128 for m in method_ids)
            or len(set(method_ids)) != len(method_ids)):
        raise ValueError("provide a fixed tuple of 1 to 20 unique method IDs")
    if not isinstance(rows, list) or not rows:
        raise ValueError("at least one eligible source row is required")
    roster = set(method_ids)
    by_method: dict[str, list[dict]] = {m: [] for m in method_ids}
    source_sets: dict[str, set[str]] = {m: set() for m in method_ids}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {
            "method_id", "source_id", "accepted", "incorrect"
        }:
            raise ValueError("invalid method-row schema")
        method = row["method_id"]
        if not isinstance(method, str) or method not in roster:
            raise ValueError("method not in fixed roster")
        slim = {key: row[key] for key in ("source_id", "accepted", "incorrect")}
        by_method[method].append(slim)
        # Validate all rows via source_risk_summary below before comparing sets.
        source_sets[method].add(row["source_id"] if isinstance(row["source_id"], str)
                                else repr(row["source_id"]))
    summaries = {m: source_risk_summary(by_method[m], alpha=a)
                 for m in method_ids}
    first = source_sets[method_ids[0]]
    if any(source_sets[m] != first for m in method_ids[1:]):
        raise ValueError("all methods must share the same eligible source set")
    adjusted = a / len(method_ids)
    output = {}
    for method in method_ids:
        summary = summaries[method]
        n, k = summary["n_accepted_sources"], summary["n_failed_accepted_sources"]
        output[method] = {
            "eligible_sources": summary["n_eligible_sources"],
            "accepted_sources": n,
            "failed_accepted_sources": k,
            "coverage": summary["coverage"],
            "observed_selective_failure_fraction": summary["observed_failure_fraction"],
            "bonferroni_one_sided_upper": (
                exact_one_sided_upper(k, n, alpha=adjusted) if n else None
            ),
        }
    return {
        "analysis": "fixed_roster_source_clustered_descriptive_only",
        "nominal_alpha": a,
        "predeclared_method_count": len(method_ids),
        "per_method_alpha": adjusted,
        "methods": output,
        "real_model_results": False,
        "limitations": (
            "Classical iid conditional-on-acceptance binomial inference only; "
            "fixed thresholds and eligible sources; no optional stopping. "
            "Bounds are not a paired test, a novelty result or a safety certificate."
        ),
    }


def main() -> None:
    """Print synthetic-only sanity checks without any model inference."""
    toy = []
    for method in ("always_accept", "selective"):
        for source, bad in (("toy_a", False), ("toy_b", True), ("toy_c", False)):
            toy.append({
                "method_id": method, "source_id": source,
                "accepted": method == "always_accept" or source != "toy_b",
                "incorrect": bad if method == "always_accept" or source != "toy_b" else None,
            })
    print(json.dumps({
        "illustration": "synthetic_only",
        "audit": fixed_roster_risk_audit(
            toy, method_ids=("always_accept", "selective")
        ),
        "novelty_established": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
