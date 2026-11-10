"""Deterministic reference scorer for Protocol 181.

No external dependencies, model calls, or network access. Input is JSONL with
one record per (source, edit, step, provenance condition). This is an audit
utility, not a statistical inference engine or a physics model.
Run only on a verified no-charge cloud runner.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

CONDITIONS = {"correct", "matched_shuffle"}
LABELS = {"valid", "invalid"}
VERDICTS = LABELS | {"abstain"}
KEY_FIELDS = ("source_id", "edit_id", "candidate_step_id", "run_manifest_hash")
REQUIRED = set(KEY_FIELDS) | {
    "physics_family", "edit_stratum", "provenance_condition",
    "label_edited", "label_adjudication_status", "verifier_output",
    "eligible", "rule_inventory_hash", "prompt_hash",
    "model_or_verifier_version", "token_budget", "compute_budget",
    "assignment_seed"
}

class InvalidPilot(ValueError):
    pass

def score(rows):
    """Fail closed on incomplete pairs; return descriptive source-weighted yield."""
    pairs = defaultdict(dict)
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict) or REQUIRED - row.keys():
            raise InvalidPilot(f"row {index}: missing required fields")
        if row["eligible"] is not True:
            raise InvalidPilot(f"row {index}: ineligible row (filter with attrition manifest first)")
        if row["label_adjudication_status"] != "adjudicated":
            raise InvalidPilot(f"row {index}: unadjudicated")
        if row["label_edited"] not in LABELS or row["verifier_output"] not in VERDICTS:
            raise InvalidPilot(f"row {index}: invalid label/verdict")
        cond = row["provenance_condition"]
        if cond not in CONDITIONS:
            raise InvalidPilot(f"row {index}: unknown condition")
        key = tuple(row[field] for field in KEY_FIELDS)
        if any(v is None or v == "" for v in key):
            raise InvalidPilot(f"row {index}: empty key")
        if cond in pairs[key]:
            raise InvalidPilot(f"row {index}: duplicate condition")
        pairs[key][cond] = row

    if not pairs:
        raise InvalidPilot("no eligible pairs")
    by_source = defaultdict(list)
    by_family = defaultdict(set)
    source_family = {}
    for key, conditions in pairs.items():
        if set(conditions) != CONDITIONS:
            raise InvalidPilot(f"incomplete pair: {key}")
        a, b = (conditions[c] for c in ("correct", "matched_shuffle"))
        for field in ("label_edited", "physics_family", "edit_stratum",
                      "rule_inventory_hash", "prompt_hash", "token_budget", "compute_budget",
                      "assignment_seed", "model_or_verifier_version"):
            if a[field] != b[field]:
                raise InvalidPilot(f"pair {key}: mismatch in {field}")
        def correct(r):
            return int(r["verifier_output"] == r["label_edited"])
        source = key[0]
        family = a["physics_family"]
        if source in source_family and source_family[source] != family:
            raise InvalidPilot(f"source {source}: inconsistent physics_family")
        source_family[source] = family
        by_source[source].append(correct(a) - correct(b))
        by_family[a["physics_family"]].add(key[0])
    source_effects = {s: sum(ds)/len(ds) for s, ds in sorted(by_source.items())}
    return {
        "n_sources": len(source_effects),
        "n_pairs": len(pairs),
        "source_effects": source_effects,
        "source_weighted_yield_difference": sum(source_effects.values())/len(source_effects),
        "family_source_counts": {f: len(s) for f, s in sorted(by_family.items())},
        "note": "Descriptive observed-sample contrast only; no p-value, CI, or novelty claim."
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonl", type=Path)
    args = parser.parse_args()
    with args.jsonl.open(encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle if line.strip()]
    print(json.dumps(score(rows), sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
