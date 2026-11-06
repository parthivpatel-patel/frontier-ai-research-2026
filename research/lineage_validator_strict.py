"""Protocol 101: strict structural gate for scientific lineage records.

Standard library only. This is a data-integrity check, not physics adjudication.
The original Protocol 099 schema remains supported; optional proposition_id and
source_family_id add explicit equivalence and holdout grouping.
"""
import json
import math
from collections import defaultdict

LABELS = frozenset(("supported", "refuted", "underdetermined", "outside_model"))
SPLITS = frozenset(("train", "development", "test"))
REQUIRED = frozenset(("scenario_id", "source_id", "family", "assumptions",
                      "claim", "intervention_id", "adjudicator", "label", "split"))
IDENTIFIERS = ("scenario_id", "source_id", "family", "claim",
               "intervention_id", "split")


def _string(value, field):
    if type(value) is not str or not value or value != value.strip():
        raise ValueError("invalid or unnormalized " + field)
    return value


def _json_value(value):
    """Validate strict JSON semantics, without coercing keys or tuples."""
    if value is None or type(value) in (str, bool, int):
        return
    if type(value) is float and math.isfinite(value):
        return
    if type(value) is list:
        for item in value:
            _json_value(item)
        return
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise ValueError("assumption keys must be strings")
            _json_value(item)
        return
    raise ValueError("unsupported assumption value")


def validate_strict_lineages(records):
    """Return record count or raise ValueError for invalid or leaking data.

    A proposition_id must be assigned from external semantic adjudication;
    this function cannot determine whether paraphrases are equivalent.
    """
    if type(records) is not list:
        raise ValueError("records must be a list")
    seen = set()
    groups = defaultdict(set)
    verdicts = {}
    for index, row in enumerate(records):
        if type(row) is not dict or not REQUIRED.issubset(row):
            raise ValueError("missing or invalid row at " + str(index))
        for field in IDENTIFIERS:
            _string(row[field], field)
        if row["split"] not in SPLITS:
            raise ValueError("unknown split")
        if type(row["assumptions"]) is not dict:
            raise ValueError("assumptions must be a dictionary")
        _json_value(row["assumptions"])
        assumptions = json.dumps(row["assumptions"], sort_keys=True,
                                 separators=(",", ":"), ensure_ascii=False,
                                 allow_nan=False)
        label = row["label"]
        if label is not None and (type(label) is not str or label not in LABELS):
            raise ValueError("invalid label")
        reviewer = row["adjudicator"]
        if label is not None:
            _string(reviewer, "adjudicator")
        elif reviewer is not None:
            _string(reviewer, "adjudicator")
        for optional in ("proposition_id", "source_family_id", "scenario_version"):
            if optional in row:
                _string(row[optional], optional)
        proposition = row.get("proposition_id", row["claim"])
        source_family = row.get("source_family_id", row["source_id"])
        scenario_version = row.get("scenario_version", row["scenario_id"])
        identity = (row["scenario_id"], row["intervention_id"], proposition)
        if identity in seen:
            raise ValueError("duplicate proposition/intervention identifier")
        seen.add(identity)
        for kind, value in (("scenario", row["scenario_id"]),
                            ("source", row["source_id"]),
                            ("source_family", source_family)):
            groups[(kind, value)].add(row["split"])
        key = (row["scenario_id"], assumptions, proposition)
        if label is not None:
            previous = verdicts.setdefault(key, label)
            if previous != label:
                raise ValueError("contradictory adjudicated proposition labels")
    if any(len(splits) > 1 for splits in groups.values()):
        raise ValueError("scenario or source family crosses splits")
    return len(records)
