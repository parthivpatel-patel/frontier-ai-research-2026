"""Paired source-cluster bootstrap for prospective selective verification.

Research implementation; not a validated physical benchmark. Standard library only.
Each record has: id, source_id, truth (0 safe, 1 unsafe, or None),
baseline_accept, certificate_accept (booleans).
All operating thresholds must be frozen on validation data upstream.
"""
from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from pathlib import Path


def validate(records):
    if not isinstance(records, list) or not records:
        raise ValueError("nonempty list required")
    ids = set()
    for r in records:
        if not isinstance(r, dict):
            raise ValueError("records must be objects")
        if not isinstance(r.get("id"), str) or not r["id"] or r["id"] in ids:
            raise ValueError("missing or duplicate id")
        ids.add(r["id"])
        if not isinstance(r.get("source_id"), str) or not r["source_id"]:
            raise ValueError("missing source_id")
        if r.get("truth") not in (0, 1, None) or isinstance(r.get("truth"), bool):
            raise ValueError("truth must be 0, 1, or null")
        for name in ("baseline_accept", "certificate_accept"):
            if type(r.get(name)) is not bool:
                raise ValueError(name + " must be boolean")
    if len({r["source_id"] for r in records}) < 2:
        raise ValueError("at least two independent source clusters required")


def metrics(records):
    n = len(records)
    known = [r for r in records if r["truth"] is not None]
    result = {"n": n, "n_known": len(known), "n_unknown": n - len(known)}
    for method, field in (("baseline", "baseline_accept"), ("certificate", "certificate_accept")):
        accepted = [r for r in records if r[field]]
        accepted_known = [r for r in known if r[field]]
        unsafe = sum(r["truth"] == 1 for r in accepted_known)
        result[method] = {
            "coverage": len(accepted) / n,
            "known_label_coverage": len(accepted_known) / len(known) if known else None,
            "unsafe_acceptance_known": unsafe / len(known) if known else None,
            "conditional_unsafe_known": unsafe / len(accepted_known) if accepted_known else None,
            "unknown_accepted": sum(r["truth"] is None for r in accepted),
        }
    result["difference_certificate_minus_baseline"] = {
        k: (result["certificate"][k] - result["baseline"][k])
        if result["certificate"][k] is not None and result["baseline"][k] is not None
        else None
        for k in ("coverage", "known_label_coverage", "unsafe_acceptance_known", "conditional_unsafe_known")
    }
    return result


def evaluate(records, *, replicates=2000, seed=2026):
    validate(records)
    if type(replicates) is not int or replicates < 100:
        raise ValueError("replicates must be integer >= 100")
    if type(seed) is not int:
        raise ValueError("seed must be integer")
    clusters = defaultdict(list)
    for r in records:
        clusters[r["source_id"]].append(r)
    groups = list(clusters.values())
    rng = random.Random(seed)
    keys = ("coverage", "known_label_coverage", "unsafe_acceptance_known", "conditional_unsafe_known")
    draws = {k: [] for k in keys}
    for _ in range(replicates):
        sample = [r for _j in range(len(groups)) for r in groups[rng.randrange(len(groups))]]
        diffs = metrics(sample)["difference_certificate_minus_baseline"]
        for k in keys:
            if diffs[k] is not None and math.isfinite(diffs[k]):
                draws[k].append(diffs[k])
    intervals = {}
    for k, values in draws.items():
        values.sort()
        if len(values) < max(30, int(replicates * 0.8)):
            intervals[k] = {"lower": None, "upper": None, "valid_draws": len(values), "warning": "insufficient defined replicates"}
        else:
            intervals[k] = {
                "lower": values[int(0.025 * (len(values) - 1))],
                "upper": values[int(0.975 * (len(values) - 1))],
                "valid_draws": len(values),
            }
    return {
        "schema": "frontier.paired_cluster_bootstrap.v1",
        "method": "paired source-cluster percentile bootstrap",
        "seed": seed,
        "replicates": replicates,
        "clusters": len(groups),
        "point": metrics(records),
        "intervals": intervals,
        "limitations": [
            "No causal interpretation; clusters must be genuinely independent.",
            "Unknown physical truth is excluded from error denominators, not silently counted safe.",
            "Conditional risk is undefined for zero accepted known-label examples.",
            "Percentile intervals may be unreliable with few or highly unequal clusters.",
            "Coverage differences must be interpreted alongside unsafe-acceptance differences.",
            "Frozen validation thresholds and source-disjoint splits are external prerequisites.",
        ],
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="JSON array of held-out paired examples")
    parser.add_argument("--replicates", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()
    print(json.dumps(evaluate(json.loads(args.input.read_text()), replicates=args.replicates, seed=args.seed), indent=2, sort_keys=True))
