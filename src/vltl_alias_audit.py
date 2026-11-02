"""Exploratory, metadata-conditional alias audit of pinned VLTL lifted predictions.

This is a POST-HOC diagnostic motivated by inspecting Protocol 023 mismatches,
not a preregistered confirmatory experiment. Run external data access on the
public GitHub-hosted runner only. No external rows are printed or redistributed.
"""
from __future__ import annotations

import json
import re

from src.vltl_prediction_audit import FILES, audit_jsonl, fetch_pinned

PROP = re.compile(r"prop_[0-9]+")
MAX_ROWS = 1000


def _signature(definition: object) -> str | None:
    """Only complete, nonempty grounded metadata can certify a candidate alias."""
    if not isinstance(definition, dict):
        return None
    action = definition.get("action_canon")
    args = definition.get("args_canon")
    if not isinstance(action, str) or not action.strip():
        return None
    if not isinstance(args, list) or not args or any(
        not isinstance(arg, str) or not arg.strip() for arg in args
    ):
        return None
    try:
        return json.dumps(definition, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError):
        return None


def normalize_by_grounded_aliases(text: str, prop_dict: object) -> str | None:
    """Canonicalize only whole proposition tokens with identical full metadata.

    Returns None if a proposition is undeclared or any mapping is malformed.
    Does not reorder connectives, remove temporal operators, or parse LTL.
    """
    if not isinstance(text, str) or not isinstance(prop_dict, dict) or not prop_dict:
        return None
    signatures: dict[str, list[str]] = {}
    for symbol, definition in prop_dict.items():
        if not isinstance(symbol, str) or PROP.fullmatch(symbol) is None:
            return None
        signature = _signature(definition)
        if signature is None:
            return None
        signatures.setdefault(signature, []).append(symbol)
    representatives = {}
    for aliases in signatures.values():
        representative = min(aliases, key=lambda s: (int(s[5:]), s))
        for symbol in aliases:
            representatives[symbol] = representative
    normalized = []
    for token in text.split():
        if PROP.fullmatch(token):
            if token not in representatives:
                return None
            normalized.append(representatives[token])
        else:
            normalized.append(token)
    return " ".join(normalized)


def audit_lifted(data: bytes) -> dict:
    """Return only aggregate counts, never the external examples."""
    basic = audit_jsonl(data, "masked_tl")
    rows = data.decode("utf-8").splitlines()
    if len(rows) > MAX_ROWS:
        raise ValueError("too many rows for bounded pilot")
    alias_only = 0
    unresolved = 0
    for line in rows:
        row = json.loads(line)
        prediction = row.get("prediction")
        if not isinstance(prediction, str) or not prediction.strip():
            continue
        pred = " ".join(prediction.split())
        target = " ".join(row["masked_tl"])
        if pred == target:
            continue
        normalized_pred = normalize_by_grounded_aliases(pred, row.get("prop_dict"))
        normalized_target = normalize_by_grounded_aliases(
            target, row.get("prop_dict")
        )
        if normalized_pred is not None and normalized_pred == normalized_target:
            alias_only += 1
        else:
            unresolved += 1
    if alias_only + unresolved != basic["nonmatching_token_strings"]:
        raise AssertionError("mismatch accounting failure")
    total = basic["nonblank_predictions"]
    conditional = basic["exact_token_string_matches"] + alias_only
    return {
        "protocol": "024",
        "analysis_type": "EXPLORATORY_POST_HOC_NOT_CONFIRMATORY",
        "upstream_commit": "383baea8210b93fe9fa7d14edd4757e5b3464e82",
        "upstream_file": FILES[0]["path"],
        "pinned_blob_sha": FILES[0]["blob_sha"],
        "records": basic["records"],
        "nonblank_predictions": total,
        "exact_token_string_matches": basic["exact_token_string_matches"],
        "metadata_alias_only_nonmatches": alias_only,
        "remaining_unresolved_nonmatches": unresolved,
        "conditional_metadata_agreement_count": conditional,
        "conditional_metadata_agreement_fraction": conditional / total if total else None,
        "interpretation": "CONDITIONAL_ON_UNVERIFIED_UPSTREAM_GROUNDING_METADATA",
        "model_semantic_accuracy_measured": False,
        "independent_human_ground_truth": False,
        "independent_source_families_verified": False,
        "redistribution_permission_verified": False,
        "scientific_novelty_established": False,
    }


def run_audit() -> dict:
    return audit_lifted(fetch_pinned(FILES[0]))


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
