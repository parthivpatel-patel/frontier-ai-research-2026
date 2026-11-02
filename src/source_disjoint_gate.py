"""Fail-closed source-disjoint fold planner, with no training or inference.

The unit is an independently authored original source. Repeated generations
and extracted expressions must inherit that source's fold. This module never
reads external data or interprets model accuracy.
"""
from __future__ import annotations

import hashlib
import json


def plan_folds(source_ids: list[str] | tuple[str, ...], *,
               seed: int = 20261102, n_folds: int = 5,
               min_sources: int = 30) -> dict:
    """Deterministic, group-level folds. Does not stratify by domain or label."""
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer")
    if isinstance(n_folds, bool) or not isinstance(n_folds, int) or n_folds < 2:
        raise ValueError("at least two folds required")
    if isinstance(min_sources, bool) or not isinstance(min_sources, int) or min_sources < n_folds:
        raise ValueError("minimum sources must be >= number of folds")
    if not isinstance(source_ids, (list, tuple)):
        raise ValueError("source IDs must be a list or tuple")
    if any(not isinstance(s, str) or not s or s.strip() != s or len(s) > 256
           for s in source_ids):
        raise ValueError("source IDs must be nonempty canonical strings")
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("duplicate original source ID: repeated outputs are not sources")
    if len(source_ids) < min_sources:
        raise ValueError("insufficient independent original sources")

    def key(source_id: str) -> tuple[bytes, str]:
        digest = hashlib.sha256(
            (str(seed) + "\x00" + source_id).encode("utf-8")
        ).digest()
        return digest, source_id

    ordered = sorted(source_ids, key=key)
    fold_tests = [ordered[i::n_folds] for i in range(n_folds)]
    all_ids = set(ordered)
    if any(not group for group in fold_tests):
        raise AssertionError("empty test fold")
    if set().union(*(set(group) for group in fold_tests)) != all_ids:
        raise AssertionError("lost original source")
    if sum(len(group) for group in fold_tests) != len(all_ids):
        raise AssertionError("source assigned to multiple folds")
    folds = []
    for index, test_ids in enumerate(fold_tests):
        train_ids = sorted(all_ids - set(test_ids))
        if set(train_ids) & set(test_ids):
            raise AssertionError("source leakage")
        folds.append({
            "fold": index,
            "test_source_ids": test_ids,
            "train_source_ids": train_ids,
        })
    return {
        "analysis": "source_disjoint_split_only",
        "seed": seed,
        "n_original_sources": len(all_ids),
        "n_folds": n_folds,
        "folds": folds,
        "limitations": (
            "Only original-source grouping is guaranteed. No domain balance, "
            "sample size adequacy, labels, model evaluation or independent "
            "adjudication is established."
        ),
    }


def main() -> None:
    # Synthetic IDs only. This is a sanity check, NOT a real evaluation.
    result = plan_folds([f"synthetic-source-{i:02d}" for i in range(30)])
    summary = {
        "analysis": result["analysis"],
        "synthetic_only": True,
        "n_original_sources": result["n_original_sources"],
        "test_sources_per_fold": [len(x["test_source_ids"]) for x in result["folds"]],
        "no_source_leakage": all(
            not set(x["test_source_ids"]) & set(x["train_source_ids"])
            for x in result["folds"]),
        "real_nl2mtl_source_count": 4,
        "real_nl2mtl_passes_minimum_gate": False,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
