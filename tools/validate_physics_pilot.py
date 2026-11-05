"""Validate candidate physics benchmark JSONL records without model inference.

Protocol 063. This is an admission *syntax and provenance* gate, not a
physical-truth adjudicator. No network, model, or third-party dependencies.
Usage: python tools/validate_physics_pilot.py candidates.jsonl
Exit 0 means schema/provenance checks pass, not that physics is correct.
"""
import json
import re
import sys
from pathlib import Path

DOMAINS = {"mechanics", "electromagnetism", "thermodynamics", "quantum"}
LABELS = {"correct", "incorrect", "unknown"}
SPLITS = {"development", "validation", "test"}
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{2,100}$")
REQUIRED = (
    "claim_id", "source_family_id", "source_uri", "source_license",
    "domain", "split", "claim_text", "assumptions", "truth_label",
    "adjudication_method", "adjudication_evidence", "adjudicator_id",
    "certificate_text", "certificate_assumptions", "certificate_status",
)
CERT_STATUSES = {"valid", "invalid", "unverified", "not_applicable"}


def validate(records):
    errors = []
    seen_ids = set()
    family_splits = {}
    for line, record in records:
        prefix = f"line {line}"
        if not isinstance(record, dict):
            errors.append(f"{prefix}: record must be an object")
            continue
        missing = [k for k in REQUIRED if k not in record]
        if missing:
            errors.append(f"{prefix}: missing fields: {', '.join(missing)}")
            continue
        for field in ("claim_id", "source_family_id"):
            value = record[field]
            if not isinstance(value, str) or not ID.fullmatch(value):
                errors.append(f"{prefix}: invalid {field}")
        claim_id = record["claim_id"]
        if isinstance(claim_id, str):
            if claim_id in seen_ids:
                errors.append(f"{prefix}: duplicate claim_id {claim_id}")
            seen_ids.add(claim_id)
        for field in ("source_uri", "source_license", "claim_text",
                      "adjudication_method", "adjudicator_id"):
            if not isinstance(record[field], str) or not record[field].strip():
                errors.append(f"{prefix}: empty or invalid {field}")
        if not isinstance(record["domain"], str) or record["domain"] not in DOMAINS:
            errors.append(f"{prefix}: unsupported domain")
        split = record["split"]
        if not isinstance(split, str) or split not in SPLITS:
            errors.append(f"{prefix}: unsupported split")
        family = record["source_family_id"]
        if isinstance(family, str) and isinstance(split, str) and split in SPLITS:
            family_splits.setdefault(family, set()).add(split)
        for field in ("assumptions", "certificate_assumptions"):
            value = record[field]
            if not isinstance(value, list) or not value or any(
                not isinstance(x, str) or not x.strip() for x in value
            ):
                errors.append(f"{prefix}: {field} must be nonempty string list")
        if not isinstance(record["truth_label"], str) or record["truth_label"] not in LABELS:
            errors.append(f"{prefix}: invalid truth_label")
        if not isinstance(record["certificate_status"], str) or record["certificate_status"] not in CERT_STATUSES:
            errors.append(f"{prefix}: invalid certificate_status")
        if not isinstance(record["certificate_text"], str):
            errors.append(f"{prefix}: certificate_text must be a string")
        evidence = record["adjudication_evidence"]
        if not isinstance(evidence, list) or any(
            not isinstance(x, str) or not x.strip() for x in evidence
        ):
            errors.append(f"{prefix}: adjudication_evidence must be a string list")
        if record["truth_label"] != "unknown" and not evidence:
            errors.append(f"{prefix}: known truth requires adjudication evidence")
        if record["certificate_status"] == "valid" and (not isinstance(record["certificate_text"], str) or not record["certificate_text"].strip()):
            errors.append(f"{prefix}: valid certificate requires certificate text")
        if record["certificate_status"] == "valid" and record["truth_label"] == "unknown":
            # Permitted: formal derivation validity does not prove physical truth.
            pass
    for family, splits in sorted(family_splits.items()):
        if len(splits) > 1:
            errors.append(f"source family {family} leaks across splits: {sorted(splits)}")
    return errors


def main(argv):
    if len(argv) != 2:
        print("usage: validate_physics_pilot.py FILE.jsonl", file=sys.stderr)
        return 2
    path = Path(argv[1])
    records = []
    try:
        with path.open(encoding="utf-8") as stream:
            for number, raw in enumerate(stream, 1):
                if not raw.strip():
                    continue
                try:
                    records.append((number, json.loads(raw)))
                except json.JSONDecodeError as exc:
                    print(f"line {number}: invalid JSON: {exc}", file=sys.stderr)
                    return 1
    except OSError as exc:
        print(f"cannot read file: {exc}", file=sys.stderr)
        return 2
    if not records:
        print("empty benchmark rejected", file=sys.stderr)
        return 1
    errors = validate(records)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"REJECTED: {len(errors)} admission errors", file=sys.stderr)
        return 1
    print(f"SCHEMA PASS: {len(records)} records; physics truth NOT verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
