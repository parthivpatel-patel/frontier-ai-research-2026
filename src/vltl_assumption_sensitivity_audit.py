"""Protocol 025: aggregate-only bounded-lasso sensitivity audit of pinned VLTL.

Run only on the standard public GitHub Actions runner. The external file is
byte-verified, fetched transiently and never committed or printed. Lasso
witnesses distinguish *formulas*, not the model from human intent.
"""
from __future__ import annotations

import json

from src.assumption_lasso_witness import (
    UnsupportedFormula, find_counterexample, parse, atoms,
)
from src.vltl_alias_audit import (
    _signature, normalize_by_grounded_aliases, audit_lifted,
)
from src.vltl_prediction_audit import FILES, fetch_pinned

STATUSES = (
    "witness", "no_witness_within_bound",
    "incomplete_budget", "unsupported_proposition_count",
    "unsupported_syntax", "metadata_unavailable",
)


def _identities(prop_dict: object, used: set[str]):
    if not isinstance(prop_dict, dict) or not prop_dict:
        return None
    signatures: dict[str, list[str]] = {}
    for key, value in prop_dict.items():
        if not isinstance(key, str):
            return None
        signature = _signature(value)
        if signature is None:
            return None
        signatures.setdefault(signature, []).append(key)
    if not used.issubset(prop_dict):
        return None
    return tuple(tuple(sorted(set(group) & used)) for group in signatures.values()
                 if len(set(group) & used) > 1)


def audit_assumptions(data: bytes) -> dict:
    base = audit_lifted(data)
    results = {
        category: {
            mode: {status: 0 for status in STATUSES}
            for mode in ("unconstrained", "recorded_metadata_equalities")
        } for category in ("alias_only", "unresolved")
    }
    counts = {"alias_only": 0, "unresolved": 0}
    for line in data.decode("utf-8").splitlines():
        row = json.loads(line)
        prediction = row.get("prediction")
        if not isinstance(prediction, str) or not prediction.strip():
            continue
        pred = " ".join(prediction.split())
        ref = " ".join(row["masked_tl"])
        if pred == ref:
            continue
        canonical_pred = normalize_by_grounded_aliases(pred, row.get("prop_dict"))
        canonical_ref = normalize_by_grounded_aliases(ref, row.get("prop_dict"))
        category = ("alias_only" if canonical_pred is not None and
                    canonical_pred == canonical_ref else "unresolved")
        counts[category] += 1
        try:
            left, right = parse(pred), parse(ref)
        except UnsupportedFormula:
            results[category]["unconstrained"]["unsupported_syntax"] += 1
            results[category]["recorded_metadata_equalities"]["unsupported_syntax"] += 1
            continue
        used = atoms(left) | atoms(right)
        try:
            free = find_counterexample(pred, ref)
        except UnsupportedFormula:
            results[category]["unconstrained"]["unsupported_syntax"] += 1
            results[category]["recorded_metadata_equalities"]["unsupported_syntax"] += 1
            continue
        results[category]["unconstrained"][free["status"]] += 1
        groups = _identities(row.get("prop_dict"), used)
        if groups is None:
            results[category]["recorded_metadata_equalities"]["metadata_unavailable"] += 1
            continue
        coupled = find_counterexample(pred, ref, equalities=groups)
        results[category]["recorded_metadata_equalities"][coupled["status"]] += 1
    if counts["alias_only"] != base["metadata_alias_only_nonmatches"]:
        raise AssertionError("alias partition changed")
    if counts["unresolved"] != base["remaining_unresolved_nonmatches"]:
        raise AssertionError("residual partition changed")
    for category in counts:
        for mode in results[category]:
            if sum(results[category][mode].values()) != counts[category]:
                raise AssertionError("bounded-witness accounting failure")
    return {
        "protocol": "025",
        "classification": "EXPLORATORY_POST_HOC_BOUNDED_SEMANTIC_DIAGNOSTIC",
        "pinned_blob_sha": FILES[0]["blob_sha"],
        "total_records": base["records"],
        "nonmatching_records": sum(counts.values()),
        "groups": counts,
        "status_counts": results,
        "max_lasso_states": 3,
        "max_distinct_propositions": 3,
        "max_enumerated_lassos_per_comparison": 20000,
        "witness_means": "formulas differ on an enumerated infinite lasso",
        "no_witness_means": "inconclusive outside the searched bounds",
        "metadata_equalities_independently_verified": False,
        "model_semantic_accuracy_measured": False,
        "novelty_established": False,
    }


def run_audit() -> dict:
    return audit_assumptions(fetch_pinned(FILES[0]))


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
