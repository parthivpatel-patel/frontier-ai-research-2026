"""Fail-closed structural oracle firewall for source-disjoint NL-to-formal evaluation.

Protocol 022. Constructed fixtures only; no model calls, external data, or
claims of semantic correctness. This interface is not a security sandbox:
it cannot detect leakage through a verifier's code, weights, or side channels.
"""
from __future__ import annotations

import json
from collections import Counter
from collections.abc import Mapping

CASE_FIELDS = frozenset({
    "case_id", "source_family_id", "trial_slot", "instruction",
    "candidate_formula", "assumption_family_id",
})
DECISION_FIELDS = frozenset({"case_id", "accept"})
GOLD_FIELDS = frozenset({"case_id", "correct"})
SPLITS = frozenset({"train", "calibration", "test"})


def _exact_fields(record: object, expected: frozenset[str], kind: str) -> dict:
    if not isinstance(record, dict) or set(record) != expected:
        raise ValueError(f"{kind} must have exactly the declared fields")
    return record


def _identifier(value: object, name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError(f"{name} must be a nonempty, trimmed string")
    return value


def prepare_cases(records: object) -> list[dict]:
    """Create isolated verifier-visible records with no gold/trace fields."""
    if not isinstance(records, (list, tuple)) or not records:
        raise ValueError("cases must be a nonempty list or tuple")
    seen_ids: set[str] = set()
    seen_trials: set[tuple[str, int]] = set()
    out: list[dict] = []
    for raw in records:
        row = _exact_fields(raw, CASE_FIELDS, "verifier case")
        cid = _identifier(row["case_id"], "case_id")
        family = _identifier(row["source_family_id"], "source_family_id")
        _identifier(row["assumption_family_id"], "assumption_family_id")
        for name in ("instruction", "candidate_formula"):
            if not isinstance(row[name], str) or not row[name].strip():
                raise ValueError(f"{name} must be nonempty text")
        slot = row["trial_slot"]
        if type(slot) is not int or slot <= 0:
            raise ValueError("trial_slot must be a positive integer")
        if cid in seen_ids:
            raise ValueError("duplicate case_id")
        if (family, slot) in seen_trials:
            raise ValueError("duplicate source-family trial slot")
        seen_ids.add(cid)
        seen_trials.add((family, slot))
        out.append(dict(row))  # no alias to caller's mutable dictionary
    return out


def validate_splits(cases: list[dict], assignments: object) -> dict:
    """Reject missing or extraneous source assignments and absent test set."""
    if not isinstance(assignments, Mapping):
        raise ValueError("source split assignments must be a mapping")
    families = {case["source_family_id"] for case in cases}
    if set(assignments) != families:
        raise ValueError("source split assignments must match all families")
    if any(split not in SPLITS for split in assignments.values()):
        raise ValueError("invalid source split")
    counts = Counter(assignments.values())
    if counts["test"] == 0:
        raise ValueError("at least one test source family is required")
    return {name: counts[name] for name in ("train", "calibration", "test")}


def _indexed_boolean_records(records: object, fields: frozenset[str],
                             value_name: str) -> dict[str, bool]:
    if not isinstance(records, (list, tuple)):
        raise ValueError(f"{value_name} records must be a list or tuple")
    result: dict[str, bool] = {}
    for raw in records:
        row = _exact_fields(raw, fields, value_name)
        cid = _identifier(row["case_id"], "case_id")
        if type(row[value_name]) is not bool:
            raise ValueError(f"{value_name} must be Boolean")
        if cid in result:
            raise ValueError(f"duplicate {value_name} case_id")
        result[cid] = row[value_name]
    return result


def score_frozen_test(cases: object, assignments: object,
                      decisions: object, gold: object) -> dict:
    """Score *test* cases only, after decisions have been frozen externally.

    Gold is passed only to this post-hoc scorer, never to prepare_cases.
    Callers must enforce temporal separation and blind verifier operation.
    """
    prepared = prepare_cases(cases)
    split_counts = validate_splits(prepared, assignments)
    test_cases = [row for row in prepared
                  if assignments[row["source_family_id"]] == "test"]
    test_ids = {row["case_id"] for row in test_cases}
    frozen = _indexed_boolean_records(decisions, DECISION_FIELDS, "accept")
    labels = _indexed_boolean_records(gold, GOLD_FIELDS, "correct")
    if set(frozen) != test_ids or set(labels) != test_ids:
        raise ValueError("decisions and gold must exactly match test cases")
    accepted = sum(frozen[cid] for cid in test_ids)
    unsafe = sum(frozen[cid] and not labels[cid] for cid in test_ids)
    test_families = {row["source_family_id"] for row in test_cases}
    accepted_families: set[str] = set()
    unsafe_families: set[str] = set()
    for row in test_cases:
        cid = row["case_id"]
        if frozen[cid]:
            accepted_families.add(row["source_family_id"])
            if not labels[cid]:
                unsafe_families.add(row["source_family_id"])
    return {
        "status": "CONSTRUCTED_OR_POSTHOC_TEST_SCORING_NOT_SEMANTIC_VALIDATION",
        "test_only": True,
        "source_family_split_counts": split_counts,
        "test_cases": len(test_cases),
        "test_source_families": len(test_families),
        "accepted_cases": accepted,
        "unsafe_accepted_cases": unsafe,
        "case_coverage": accepted / len(test_cases),
        "case_unsafe_acceptance_rate": unsafe / len(test_cases),
        "conditional_error_among_accepted": unsafe / accepted if accepted else None,
        "accepted_source_families": len(accepted_families),
        "unsafe_accepted_source_families": len(unsafe_families),
        "source_family_unsafe_acceptance_rate":
            len(unsafe_families) / len(test_families),
        "independent_human_adjudication_verified": False,
        "novelty_established": False,
    }


def constructed_identifiability_warning() -> dict:
    """Same observable case/decision, opposite synthetic correctness labels."""
    case = {
        "case_id": "toy-1", "source_family_id": "toy-source",
        "trial_slot": 1, "instruction": "Eventually visit room A",
        "candidate_formula": "F room_A",
        "assumption_family_id": "toy-dynamics",
    }
    decisions = [{"case_id": "toy-1", "accept": True}]
    splits = {"toy-source": "test"}
    yes = score_frozen_test([case], splits, decisions,
                            [{"case_id": "toy-1", "correct": True}])
    no = score_frozen_test([case], splits, decisions,
                           [{"case_id": "toy-1", "correct": False}])
    return {
        "status": "CONSTRUCTED_LABEL_NONIDENTIFIABILITY_WARNING",
        "identical_verifier_observations": True,
        "identical_frozen_decisions": True,
        "unsafe_acceptance_if_correct": yes["unsafe_accepted_cases"],
        "unsafe_acceptance_if_incorrect": no["unsafe_accepted_cases"],
        "interpretation": (
            "Without independent semantic ground truth, a frozen candidate "
            "and physical-model identifier do not themselves certify whether "
            "the human-intended interpretation was preserved. This is a "
            "constructed logical warning, not a model-performance result."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(constructed_identifiability_warning(),
                     indent=2, sort_keys=True))
