"""Protocol 098 lineage integrity checks. Standard library only.

This validates dataset structure, not physical truth or scientific novelty.
Records are dictionaries with keys: scenario_id, source_id, family,
assumptions, claim, intervention_id, adjudicator, label, split.
A label of None means unresolved and requires no adjudicator.
"""
from collections import defaultdict
import json

LABELS = {"supported", "refuted", "underdetermined", "outside_model"}
SPLITS = {"train", "development", "test"}
REQUIRED = {"scenario_id", "source_id", "family", "assumptions",
            "claim", "intervention_id", "adjudicator", "label", "split"}


def validate_lineages(records):
    """Raise ValueError on leakage or inconsistent adjudication; return count."""
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    ids = set()
    scenario_splits = defaultdict(set)
    source_splits = defaultdict(set)
    truth_by_key = {}
    for index, row in enumerate(records):
        if not isinstance(row, dict) or not REQUIRED.issubset(row):
            raise ValueError(f"missing or invalid fields at row {index}")
        for field in ("scenario_id", "source_id", "family", "claim",
                      "intervention_id", "split"):
            if not isinstance(row[field], str) or not row[field].strip():
                raise ValueError(f"invalid {field} at row {index}")
        if row["split"] not in SPLITS:
            raise ValueError("unknown split")
        if not isinstance(row["assumptions"], dict):
            raise ValueError("assumptions must be a dictionary")
        try:
            canonical = json.dumps(row["assumptions"], sort_keys=True,
                                   allow_nan=False, separators=(",", ":"))
        except (TypeError, ValueError) as exc:
            raise ValueError("noncanonical assumptions") from exc
        if row["label"] is not None and row["label"] not in LABELS:
            raise ValueError("invalid label")
        if row["label"] is not None and (
            not isinstance(row["adjudicator"], str)
            or not row["adjudicator"].strip()
        ):
            raise ValueError("observed label lacks adjudicator provenance")
        identifier = (row["scenario_id"], row["intervention_id"], row["claim"])
        if identifier in ids:
            raise ValueError("duplicate record identifier")
        ids.add(identifier)
        scenario_splits[row["scenario_id"]].add(row["split"])
        source_splits[row["source_id"]].add(row["split"])
        key = (row["scenario_id"], canonical, row["claim"])
        if row["label"] is not None:
            previous = truth_by_key.setdefault(key, row["label"])
            if previous != row["label"]:
                raise ValueError("contradictory observed truth labels")
    if any(len(splits) > 1 for splits in scenario_splits.values()):
        raise ValueError("scenario lineage crosses splits")
    if any(len(splits) > 1 for splits in source_splits.values()):
        raise ValueError("source lineage crosses splits")
    return len(records)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path", help="JSON array of lineage records")
    args = parser.parse_args()
    with open(args.json_path, encoding="utf-8") as handle:
        print(f"validated {validate_lineages(json.load(handle))} records")
