"""Protocol 046: matched-coverage selective-risk evaluator (standard library only).

Input JSON: {"examples":[{"id":"...", "group_id":"...", "split":"validation"|"test",
"ground_truth":"verified"|"falsified"|"inconclusive",
"methods":{"baseline":{"score":0.7,"decision":"verified"},
           "certificate":{"score":0.6,"decision":"verified"}}}, ...]}

Score is a predeclared confidence in accepting a decision, not a correctness label.
The evaluator selects the top k scores per method, with k=floor(coverage*n).
Ties are broken by example id; matched coverage does not imply matched examples.
Validation and test must have disjoint group IDs. No test-derived threshold tuning.
Inconclusive ground truth is counted unsafe if accepted.
Outputs descriptive counts only; no significance or causal claim.
"""
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

LABELS = {"verified", "falsified", "inconclusive"}
SPLITS = {"validation", "test"}


def evaluate(data, coverage):
    if not isinstance(coverage, (float, int)) or not math.isfinite(coverage) or not 0 < coverage <= 1:
        raise ValueError("coverage must be in (0,1]")
    rows = data.get("examples")
    if not isinstance(rows, list) or not rows:
        raise ValueError("nonempty examples list required")
    seen, groups, methods = set(), defaultdict(set), None
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each example must be an object")
        ident, group, split = row.get("id"), row.get("group_id"), row.get("split")
        if not isinstance(ident, str) or not ident or ident in seen:
            raise ValueError("duplicate or invalid id")
        seen.add(ident)
        if not isinstance(group, str) or not group or split not in SPLITS:
            raise ValueError("invalid group or split")
        groups[group].add(split)
        if row.get("ground_truth") not in LABELS:
            raise ValueError("invalid ground truth")
        predictions = row.get("methods")
        if not isinstance(predictions, dict) or not predictions:
            raise ValueError("methods required")
        if methods is None:
            methods = set(predictions)
        if set(predictions) != methods:
            raise ValueError("all examples must have identical methods")
        for name, pred in predictions.items():
            if not isinstance(pred, dict) or pred.get("decision") not in LABELS:
                raise ValueError(f"invalid decision for {name}")
            score = pred.get("score")
            if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score) or not 0 <= score <= 1:
                raise ValueError(f"invalid score for {name}")
    if any(len(splits) > 1 for splits in groups.values()):
        raise ValueError("group leakage across validation/test")
    output = {"target_coverage": coverage, "splits": {}}
    for split in ("validation", "test"):
        subset = [r for r in rows if r["split"] == split]
        if not subset:
            continue
        k = math.floor(coverage * len(subset))
        if k == 0:
            raise ValueError("coverage selects zero examples")
        result = {}
        for method in sorted(methods):
            selected = sorted(subset, key=lambda r: (-r["methods"][method]["score"], r["id"]))[:k]
            unsafe = sum(r["methods"][method]["decision"] != r["ground_truth"] or r["ground_truth"] == "inconclusive" for r in selected)
            result[method] = {"accepted": k, "total": len(subset), "unsafe": unsafe,
                              "unsafe_rate": unsafe / k,
                              "selected_ids": [r["id"] for r in selected]}
        output["splits"][split] = result
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--coverage", type=float, required=True)
    args = parser.parse_args()
    print(json.dumps(evaluate(json.loads(args.input.read_text()), args.coverage), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
