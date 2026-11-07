"""Protocol 118: admitted, heldout-only common-acceptance inference.

This bridge enforces Protocol 113 admission before the Protocol 117 estimator.
It does not certify independent adjudication or calibration chronology.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from research.matched_intervention_validator import (
    AdmissionError, admit_matched_interventions,
)
from research.common_acceptance_bootstrap import common_acceptance_bootstrap


def admitted_common_acceptance_bootstrap(
    rows: Iterable[Mapping[str, Any]],
    weights: Mapping[str, float],
    systems: tuple[str, str] = ("A", "B"),
    *,
    seed: int = 0,
    replicates: int = 2000,
    max_undefined_fraction: float = 0.01,
    min_lineages_per_family: int = 2,
) -> dict[str, Any]:
    """Return only the admitted heldout common-acceptance estimand and CI.

    No filtering, imputation or post hoc selection of evaluation rows is allowed.
    """
    records = list(rows)
    report = admit_matched_interventions(records, systems=systems)
    if any(row["split"] != "heldout" for row in records):
        raise AdmissionError("Only frozen heldout interventions may enter inference")
    observed_families = {row["physics_family"] for row in records}
    if set(weights) != observed_families:
        raise AdmissionError("Family weights must match the admitted population exactly")
    projected = [
        {key: row[key] for key in (
            "physics_family", "lineage_id", "intervention_id",
            "system_id", "accepted", "response_unsafe"
        )}
        for row in records
    ]
    result = common_acceptance_bootstrap(
        projected, weights, systems=systems, seed=seed, replicates=replicates,
        max_undefined_fraction=max_undefined_fraction,
        min_lineages_per_family=min_lineages_per_family,
    )
    return {
        **result,
        "admission": {
            "records": report.records,
            "interventions": report.interventions,
            "lineages": report.lineages,
            "by_family": report.by_family,
        },
        "scope": "heldout admitted common-acceptance descriptive inference",
        "limitations": (
            "Percentile intervals assume independent sampled lineages within families. "
            "Reviewer independence, calibration chronology and frozen prespecification "
            "require external audit. Neither causal identification nor novelty is established."
        ),
    }
