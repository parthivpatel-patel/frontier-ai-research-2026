"""Audit an externally published numeric-mutation subset of NL-to-LTL data.

Uses a pinned, MIT-licensed 25-row source file. Only a five-row, strictly
matched English template is assessed. This is a dataset consistency audit,
NOT an LLM evaluation, a novel theorem, or a claim about all dataset labels.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

DATA = (Path(__file__).resolve().parents[1] / "data" / "external" /
        "robustifai_number_mutations.csv")
UPSTREAM_GIT_BLOB_SHA1 = "6f6d2e01707e777be9cd0197698f8f19b4381fc8"
SOURCE_COMMIT = "a38a73a351c07a3d17cb561098485cd4416c5375"
NUMBER = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
          "six": 6, "seven": 7, "eight": 8, "nine": 9}
TEMPLATE = re.compile(
    r"Whenever a is enabled, b is enabled (one|two|three|four|five|six|seven|eight|nine) steps later\.",
    re.IGNORECASE,
)
# This exact grammar is intentionally narrow: G(a -> X(X(X b))).
FORMULA = "G(a->X(X(Xb)))"


def number_of_steps(text: str) -> int | None:
    match = TEMPLATE.fullmatch(text.strip())
    return NUMBER[match.group(1).lower()] if match else None


def verify_upstream_snapshot(path: Path = DATA) -> str:
    raw = path.read_bytes()
    header = f"blob {len(raw)}\0".encode("ascii")
    actual = hashlib.sha1(header + raw).hexdigest()
    if actual != UPSTREAM_GIT_BLOB_SHA1:
        raise ValueError("vendored dataset differs from the pinned upstream Git blob")
    return actual


def audit_rows(rows: list[dict[str, str]]) -> dict[str, object]:
    findings = []
    matched = 0
    for index, row in enumerate(rows, start=1):
        mutated = number_of_steps(row["requirement"])
        original = number_of_steps(row["Original_Requirement"])
        normalized_formula = re.sub(r"\s+", "", row["formula"])
        if mutated is None or original is None or normalized_formula != FORMULA:
            continue  # No semantic judgment for unsupported language or formulas.
        matched += 1
        depth = 3  # Independently read from the supported exact FORMULA grammar.
        if original != depth:
            raise ValueError("source English and source formula do not match the strict template")
        if mutated == depth:
            continue  # A genuine negative control: the inherited label still fits.
        # Infinite trace: a true only at time 0; b true only at 'mutated'.
        # English requires b at time mutated; source formula requires b at time 3.
        assert mutated != depth
        findings.append({
            "csv_row": index,
            "mutated_steps": mutated,
            "original_steps": original,
            "formula_steps": depth,
            "witness_a_true_at": [0],
            "witness_b_true_at": [mutated],
            "english_true_on_witness": True,
            "inherited_formula_true_on_witness": False,
        })
    return {
        "source_rows": len(rows),
        "strict_template_rows": matched,
        "witnessed_mismatch_rows": len(findings),
        "distinct_mutated_steps": sorted({x["mutated_steps"] for x in findings}),
        "distinct_source_instructions": len({
            r["Original_Requirement"] for r in rows
            if number_of_steps(r["requirement"]) is not None
            and number_of_steps(r["Original_Requirement"]) is not None
            and re.sub(r"\s+", "", r["formula"]) == FORMULA
        }),
        "findings": findings,
        "scope": "Exact template only; the remaining rows were not semantically adjudicated.",
        "warning": "The dataset authors explicitly say inherited labels are not verified ground truth. These are expected risks of mutation, not evidence of author misconduct or measured LLM error.",
    }


def audit_snapshot(path: Path = DATA) -> dict[str, object]:
    blob = verify_upstream_snapshot(path)
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    result = audit_rows(rows)
    return {"upstream_commit": SOURCE_COMMIT, "upstream_blob_sha1": blob, **result}


if __name__ == "__main__":
    print(json.dumps(audit_snapshot(), indent=2, sort_keys=True))
