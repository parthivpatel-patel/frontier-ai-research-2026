"""Fail-closed paired-intervention admission, Protocol 113.

This module validates records before inferential estimation. It does not perform
adjudication or establish independent scientific truth.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

REQUIRED = frozenset({
    "physics_family", "lineage_id", "intervention_id", "system_id",
    "prompt_truth", "proposition_hash", "evidence_hash", "intervention_kind",
    "split", "accepted", "response_unsafe", "response_hash",
    "rubric_version", "adjudicator_ids", "adjudication_timestamp",
    "adjudication_evidence_hash", "calibration_artifact_hash",
    "split_manifest_hash", "git_revision", "model_configuration_hash",
})
SPLITS = frozenset({"train", "calibration", "heldout"})


class AdmissionError(ValueError):
    """No inferential table may be emitted when admission fails."""


@dataclass(frozen=True)
class AdmissionReport:
    records: int
    interventions: int
    lineages: int
    by_family: dict[str, int]
    by_intervention_kind: dict[str, int]
    by_system: dict[str, int]
    accepted_by_system: dict[str, int]


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def admit_matched_interventions(
    rows: Iterable[Mapping[str, Any]], *, systems: tuple[str, str]
) -> AdmissionReport:
    """Validate exactly two prespecified systems on identical interventions.

    Call before any bootstrap. No silent inner joins or missing-value imputation.
    Calibration freeze chronology and genuine reviewer independence must also be
    externally audited; fields here are presence/consistency checks only.
    """
    if len(systems) != 2 or len(set(systems)) != 2 or not all(map(_nonempty, systems)):
        raise AdmissionError("Exactly two distinct named systems are required")
    records = list(rows)
    if not records:
        raise AdmissionError("Empty evaluation dataset")
    groups: dict[tuple[str, str, str], dict[str, Mapping[str, Any]]] = defaultdict(dict)
    lineage_splits: dict[tuple[str, str], set[str]] = defaultdict(set)
    response_provenance: dict[tuple[str, str], tuple[Any, ...]] = {}
    by_family: Counter[str] = Counter()
    by_kind: Counter[str] = Counter()
    by_system: Counter[str] = Counter()
    accepted_by_system: Counter[str] = Counter()
    freeze_fields = ("calibration_artifact_hash", "split_manifest_hash", "git_revision")
    freeze_values: set[tuple[Any, ...]] = set()
    for idx, row in enumerate(records):
        if not isinstance(row, Mapping):
            raise AdmissionError(f"Row {idx} is not a mapping")
        missing = REQUIRED.difference(row)
        if missing:
            raise AdmissionError(f"Row {idx} missing {sorted(missing)}")
        string_fields = REQUIRED.difference({"accepted", "response_unsafe", "prompt_truth", "adjudicator_ids"})
        if any(not _nonempty(row[k]) for k in string_fields):
            raise AdmissionError(f"Row {idx} has missing string provenance")
        if row["system_id"] not in systems or row["split"] not in SPLITS:
            raise AdmissionError(f"Row {idx} has unexpected system or split")
        if type(row["accepted"]) is not bool or type(row["prompt_truth"]) is not bool:
            raise AdmissionError(f"Row {idx} requires boolean acceptance and prompt truth")
        if row["accepted"]:
            if type(row["response_unsafe"]) is not bool:
                raise AdmissionError(f"Row {idx} accepted without boolean response adjudication")
            reviewers = row["adjudicator_ids"]
            if not isinstance(reviewers, (list, tuple)) or not reviewers or not all(map(_nonempty, reviewers)):
                raise AdmissionError(f"Row {idx} lacks independent reviewer identifiers")
        elif row["response_unsafe"] is not None:
            raise AdmissionError(f"Row {idx} labels an abstention safe or unsafe")
        key = (row["physics_family"], row["lineage_id"], row["intervention_id"])
        system = row["system_id"]
        if system in groups[key]:
            raise AdmissionError(f"Duplicate intervention/system key: {key}, {system}")
        groups[key][system] = row
        lineage_splits[key[:2]].add(row["split"])
        freeze_values.add(tuple(row[k] for k in freeze_fields))
        by_family[row["physics_family"]] += 1
        by_kind[row["intervention_kind"]] += 1
        by_system[system] += 1
        if row["accepted"]:
            accepted_by_system[system] += 1
            provenance_key = (row["response_hash"], row["rubric_version"])
            provenance = (tuple(row["adjudicator_ids"]), row["adjudication_timestamp"], row["adjudication_evidence_hash"], row["response_unsafe"])
            if provenance_key in response_provenance and response_provenance[provenance_key] != provenance:
                raise AdmissionError("Conflicting adjudication for identical response hash and rubric")
            response_provenance[provenance_key] = provenance
    if len(freeze_values) != 1:
        raise AdmissionError("Inconsistent frozen calibration/split/revision provenance")
    if any(len(splits) != 1 for splits in lineage_splits.values()):
        raise AdmissionError("Scenario lineage crosses data splits")
    shared = ("prompt_truth", "proposition_hash", "evidence_hash", "intervention_kind", "split", "physics_family", "lineage_id", "intervention_id", "calibration_artifact_hash", "split_manifest_hash", "git_revision")
    for key, pair in groups.items():
        if set(pair) != set(systems):
            raise AdmissionError(f"Missing or extra system counterpart: {key}")
        a, b = (pair[s] for s in systems)
        if any(a[field] != b[field] for field in shared):
            raise AdmissionError(f"Conflicting shared intervention fields: {key}")
    return AdmissionReport(
        records=len(records), interventions=len(groups), lineages=len(lineage_splits),
        by_family=dict(sorted(by_family.items())),
        by_intervention_kind=dict(sorted(by_kind.items())),
        by_system=dict(sorted(by_system.items())),
        accepted_by_system=dict(sorted(accepted_by_system.items())),
    )
