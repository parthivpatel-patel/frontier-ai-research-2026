"""Fail-closed bridge from Protocol 113 admission to Protocol 116 accounting.

Descriptive only: does not validate reviewer independence or calibration chronology.
No statistical interval or causal claim is produced.
"""
from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from typing import Any

from research.matched_intervention_validator import (
    AdmissionError,
    admit_matched_interventions,
)
from research.common_support_accounting import summarize


def admitted_common_support(
    rows: Iterable[Mapping[str, Any]],
    *,
    systems: tuple[str, str] = ("A", "B"),
    evaluation_split: str = "heldout",
) -> dict[str, Any]:
    """Validate complete paired records before producing descriptive estimates.

    Reject mixed splits, non-heldout evaluation, and ambiguous composite keys.
    Materialize once to prevent generators from changing between validation
    and estimation. Never silently drop rejected records or abstentions.
    """
    records = list(rows)
    if evaluation_split != "heldout":
        raise AdmissionError("Only prespecified heldout evaluation is supported")
    report = admit_matched_interventions(records, systems=systems)
    if any(row["split"] != evaluation_split for row in records):
        raise AdmissionError("Mixed or non-heldout records cannot enter evaluation")
    projected = [
        {
            "intervention_key": json.dumps(
                [row["physics_family"], row["lineage_id"], row["intervention_id"]],
                separators=(",", ":"),
                ensure_ascii=True,
            ),
            "system": row["system_id"],
            "accepted": row["accepted"],
            "unsafe": row["response_unsafe"],
        }
        for row in records
    ]
    result = summarize(projected, systems=systems)
    if result["n"] != report.interventions:
        raise AdmissionError("Admission and estimation populations disagree")
    return {
        **result,
        "admission": {
            "records": report.records,
            "interventions": report.interventions,
            "lineages": report.lineages,
            "by_family": report.by_family,
        },
        "scope": "heldout descriptive common-support accounting",
        "limitations": (
            "Adjudicator independence and calibration chronology require external audit; "
            "acceptance-conditioned contrasts do not identify causal model effects."
        ),
    }
