"""Protocol 123: heldout scientific admission with deterministic interval preflight.

This bridge does not establish nominal confidence interval coverage, independent
physics adjudication, causal identification, or research novelty.
"""
from collections.abc import Iterable, Mapping
from typing import Any

from research.matched_intervention_validator import AdmissionError, admit_matched_interventions
from research.preflight_gated_bootstrap import preflight_gated_bootstrap


def admitted_preflight_bootstrap(
    rows: Iterable[Mapping[str, Any]],
    weights: Mapping[str, float],
    systems: tuple[str, str] = ("A", "B"),
    *,
    seed: int = 0,
    replicates: int = 2000,
    max_undefined_fraction: float = 0.01,
) -> dict[str, Any]:
    """Admit complete heldout pairs before deterministic bootstrap eligibility."""
    records = list(rows)
    report = admit_matched_interventions(records, systems=systems)
    if any(row["split"] != "heldout" for row in records):
        raise AdmissionError("Only frozen heldout interventions may enter inference")
    families = {row["physics_family"] for row in records}
    if set(weights) != families:
        raise AdmissionError("Weights must match the admitted physics families exactly")
    projected = [
        {key: row[key] for key in (
            "physics_family", "lineage_id", "intervention_id",
            "system_id", "accepted", "response_unsafe"
        )}
        for row in records
    ]
    result = preflight_gated_bootstrap(
        projected, weights, systems=systems, seed=seed, replicates=replicates,
        max_undefined_fraction=max_undefined_fraction,
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
            "Analytic interval eligibility is not nominal coverage. "
            "Independent adjudication, calibration chronology, lineage independence, "
            "frozen prespecification and competitive baselines remain unverified."
        ),
    }
