"""Protocol 044: validate a preregistered benchmark manifest without running models.

Usage: python experiments/protocol_044_manifest_validator.py manifest.json
Exit 0 only for a structurally valid, leakage-screened manifest.
This is a schema gate, not evidence of dataset correctness or novelty.
"""
import json
import sys
from collections import Counter
from pathlib import Path

SPLITS = {"train", "validation", "test"}
REQUIRED = {"id", "split", "family", "source_id", "claim", "ground_truth", "model_id"}
LABELS = {"verified", "falsified", "inconclusive"}


def validate(data):
    errors = []
    if not isinstance(data, dict) or not isinstance(data.get("examples"), list):
        return ["root must contain an examples list"]
    examples = data["examples"]
    if not examples:
        errors.append("examples must not be empty")
    ids = set()
    source_splits = {}
    model_splits = {}
    for i, row in enumerate(examples):
        prefix = f"examples[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        missing = REQUIRED - row.keys()
        if missing:
            errors.append(f"{prefix}: missing {sorted(missing)}")
            continue
        for key in ("id", "family", "source_id", "claim", "model_id"):
            if not isinstance(row[key], str) or not row[key].strip():
                errors.append(f"{prefix}: {key} must be nonempty text")
        if row["split"] not in SPLITS:
            errors.append(f"{prefix}: invalid split")
        if row["ground_truth"] not in LABELS:
            errors.append(f"{prefix}: invalid ground_truth")
        if row["id"] in ids:
            errors.append(f"{prefix}: duplicate id")
        ids.add(row["id"])
        if isinstance(row["split"], str) and row["split"] in SPLITS:
            for field, dest in (("source_id", source_splits), ("model_id", model_splits)):
                val = row[field]
                if isinstance(val, str) and val.strip():
                    dest.setdefault(val, set()).add(row["split"])
    for name, mapping in (("source_id", source_splits), ("model_id", model_splits)):
        for key, splits in sorted(mapping.items()):
            if len(splits) > 1:
                errors.append(f"{name} {key!r} crosses splits: {sorted(splits)}")
    return errors


def main(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}))
        return 2
    errors = validate(data)
    print(json.dumps({"valid": not errors, "examples": len(data["examples"]) if isinstance(data, dict) and isinstance(data.get("examples"), list) else 0, "errors": errors}, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python experiments/protocol_044_manifest_validator.py manifest.json", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
