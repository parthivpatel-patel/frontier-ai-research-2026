"""Protocol 026: fixed-vocabulary, aggregate-only unsupported-LTL syntax census.

This is a post-hoc diagnostic, NOT a model correctness experiment.
External bytes are fetched only on the public GitHub Actions runner.
Never return source strings, formulas, IDs, proposition metadata or unknown tokens.
"""
from __future__ import annotations

import json
import re

from src.assumption_lasso_witness import UnsupportedFormula, parse
from src.vltl_alias_audit import audit_lifted, normalize_by_grounded_aliases
from src.vltl_prediction_audit import FILES, fetch_pinned

LEX = re.compile(r"prop_[0-9]+|->|&&|\|\||[()!&|]|[A-Za-z_][A-Za-z_0-9]*|[^\s]")
OPS = {
    "!": "not", "not": "not",
    "&": "and", "&&": "and", "and": "and",
    "|": "or", "||": "or", "or": "or",
    "->": "implies", "implies": "implies",
    "u": "until", "until": "until",
    "x": "next", "next": "next",
    "f": "finally", "finally": "finally", "eventually": "finally",
    "g": "always", "always": "always", "globally": "always",
}
OP_NAMES = ("not", "and", "or", "implies", "until", "next", "finally", "always")
FAILURES = ("unknown_character", "unknown_word_or_operator",
            "length_or_token_limit", "grammar_or_operand")
SIDE = ("prediction_only", "reference_only", "both")
GROUPS = ("alias_only", "unresolved")
TOKEN_CLASSES = ("proposition", "parenthesis", "boolean_constant",
                 "unknown_word", "unknown_symbol")


def _failure_class(exc: UnsupportedFormula) -> str:
    reason = str(exc)
    if reason == "unknown token" or reason.startswith("trailing unknown"):
        return "unknown_character"
    if reason == "unsupported operator":
        return "unknown_word_or_operator"
    if reason.startswith("empty or oversized") or reason.startswith("trailing unknown characters or too many"):
        return "length_or_token_limit"
    return "grammar_or_operand"


def _lexical_counts(formula: str, operators: dict, classes: dict) -> None:
    for token in LEX.findall(formula):
        if re.fullmatch(r"prop_[0-9]+", token):
            classes["proposition"] += 1
        elif token in ("(", ")"):
            classes["parenthesis"] += 1
        elif token.lower() in ("true", "false"):
            classes["boolean_constant"] += 1
        elif token.lower() in OPS:
            operators[OPS[token.lower()]] += 1
        elif re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", token):
            classes["unknown_word"] += 1
        else:
            classes["unknown_symbol"] += 1


def audit_unsupported(data: bytes) -> dict:
    base = audit_lifted(data)  # validates JSONL, source IDs and required fields
    groups = {k: 0 for k in GROUPS}
    sides = {k: 0 for k in SIDE}
    failures = {k: 0 for k in FAILURES}
    operators = {k: 0 for k in OP_NAMES}
    classes = {k: 0 for k in TOKEN_CLASSES}
    nonmatches = 0
    supported = 0
    for line in data.decode("utf-8").splitlines():
        row = json.loads(line)
        prediction = row.get("prediction")
        if not isinstance(prediction, str) or not prediction.strip():
            continue
        pred = " ".join(prediction.split())
        reference = " ".join(row["masked_tl"])
        if pred == reference:
            continue
        nonmatches += 1
        normalized_pred = normalize_by_grounded_aliases(pred, row.get("prop_dict"))
        normalized_ref = normalize_by_grounded_aliases(reference, row.get("prop_dict"))
        group = ("alias_only" if normalized_pred is not None and
                 normalized_pred == normalized_ref else "unresolved")
        exceptions = []
        for formula in (pred, reference):
            try:
                parse(formula)
                exceptions.append(None)
            except UnsupportedFormula as exc:
                exceptions.append(exc)
        if all(exc is None for exc in exceptions):
            supported += 1
            continue
        groups[group] += 1
        sides["both" if all(exc is not None for exc in exceptions) else
              "prediction_only" if exceptions[0] is not None else
              "reference_only"] += 1
        for exc in exceptions:
            if exc is not None:
                failures[_failure_class(exc)] += 1
        _lexical_counts(pred, operators, classes)
        _lexical_counts(reference, operators, classes)
    if nonmatches != (base["metadata_alias_only_nonmatches"] +\n                      base["remaining_unresolved_nonmatches"]):
        raise AssertionError("nonmatch partition changed")
    if supported + sum(groups.values()) != nonmatches:
        raise AssertionError("unsupported partition incomplete")
    if sum(sides.values()) != sum(groups.values()):
        raise AssertionError("parse-failure sides do not sum")
    if sum(failures.values()) != sides["both"] * 2 + sides["prediction_only"] + sides["reference_only"]:
        raise AssertionError("failed formula-side accounting")
    return {
        "protocol": "026",
        "analysis": "EXPLORATORY_POST_HOC_SYNTAX_CENSUS_NOT_SEMANTIC_ACCURACY",
        "pinned_blob_sha": FILES[0]["blob_sha"],
        "nonexact_pairs": nonmatches,
        "parsed_pairs": supported,
        "unsupported_pairs": sum(groups.values()),
        "unsupported_by_prior_group": groups,
        "parse_failure_sides": sides,
        "failed_formula_side_classes": failures,
        "operator_occurrences_across_both_sides_of_unsupported_pairs": operators,
        "other_token_occurrences_across_both_sides_of_unsupported_pairs": classes,
        "external_text_or_identifiers_exposed": False,
        "physical_assumptions_validated": False,
        "semantic_accuracy_measured": False,
        "scientific_novelty_established": False,
    }


def run_audit() -> dict:
    return audit_unsupported(fetch_pinned(FILES[0]))


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
