"""Protocol 027: frozen, aggregate-only candidate LTL operator vocabulary audit.

Exploratory lexical diagnostic on pinned external predictions. It never prints
or returns individual tokens, formulas, source IDs or physical grounding data.
It DOES NOT extend the parser or claim semantic correctness.
"""
from __future__ import annotations

import json
import re

from src.assumption_lasso_witness import UnsupportedFormula, parse
from src.vltl_unsupported_syntax_census import LEX, OPS, audit_unsupported
from src.vltl_prediction_audit import FILES, fetch_pinned

# Frozen in experiments/PROTOCOL_027_FROZEN_OPERATOR_VOCABULARY.md
CANDIDATES = {
    "r": "release", "release": "release", "v": "release",
    "w": "weak_until", "weakuntil": "weak_until",
    "weak_until": "weak_until",
    "m": "strong_release", "strongrelease": "strong_release",
    "strong_release": "strong_release",
    "xor": "xor",
    "iff": "equivalence", "equiv": "equivalence",
    "equivalent": "equivalence",
}
FAMILIES = ("release", "weak_until", "strong_release", "xor", "equivalence")
WORD = re.compile(r"[A-Za-z_][A-Za-z_0-9]*\Z")
ATOM = re.compile(r"prop_[0-9]+\Z")


def _unknown_vocabulary(formula: str) -> dict:
    """Classify tokens into *fixed labels*, without returning source tokens."""
    counts = {name: 0 for name in FAMILIES}
    unknown_words = 0
    unknown_symbols = 0
    for token in LEX.findall(formula):
        lower = token.lower()
        if (ATOM.fullmatch(token) or token in ("(", ")") or
                lower in OPS or lower in ("true", "false")):
            continue
        if WORD.fullmatch(token):
            if lower in CANDIDATES:
                counts[CANDIDATES[lower]] += 1
            else:
                unknown_words += 1
        else:
            unknown_symbols += 1
    return {
        "candidate_counts": counts,
        "unclassified_word_count": unknown_words,
        "unclassified_symbol_count": unknown_symbols,
    }


def audit_candidate_vocabulary(data: bytes) -> dict:
    """Only six previously unsupported nonexact pairs enter the census.

    Validation, source integrity and prior exact-match partitions are inherited
    from Protocol 026. All returned values are aggregate numbers/static labels.
    """
    previous = audit_unsupported(data)
    families = {name: 0 for name in FAMILIES}
    unclassified_words = 0
    unclassified_symbols = 0
    supported_by_dictionary = 0
    remaining_unclassified = 0
    unsupported_pairs = 0

    for line in data.decode("utf-8").splitlines():
        row = json.loads(line)
        prediction = row.get("prediction")
        if not isinstance(prediction, str) or not prediction.strip():
            continue
        predicted = " ".join(prediction.split())
        reference = " ".join(row["masked_tl"])
        if predicted == reference:
            continue
        try:
            parse(predicted)
            left_supported = True
        except UnsupportedFormula:
            left_supported = False
        try:
            parse(reference)
            right_supported = True
        except UnsupportedFormula:
            right_supported = False
        if left_supported and right_supported:
            continue
        unsupported_pairs += 1
        pair_candidate = 0
        pair_unclassified = 0
        for formula in (predicted, reference):
            result = _unknown_vocabulary(formula)
            for family in FAMILIES:
                count = result["candidate_counts"][family]
                families[family] += count
                pair_candidate += count
            unclassified_words += result["unclassified_word_count"]
            unclassified_symbols += result["unclassified_symbol_count"]
            pair_unclassified += (result["unclassified_word_count"] +
                                  result["unclassified_symbol_count"])
        if pair_unclassified == 0 and pair_candidate > 0:
            supported_by_dictionary += 1
        else:
            remaining_unclassified += 1

    previous_tokens = previous["other_token_occurrences_across_both_sides_of_unsupported_pairs"]
    if unsupported_pairs != previous["unsupported_pairs"]:
        raise AssertionError("unsupported pair partition changed")
    if supported_by_dictionary + remaining_unclassified != unsupported_pairs:
        raise AssertionError("candidate pair partition changed")
    if sum(families.values()) + unclassified_words != previous_tokens["unknown_word"]:
        raise AssertionError("unknown word accounting changed")
    if unclassified_symbols != previous_tokens["unknown_symbol"]:
        raise AssertionError("unknown symbol accounting changed")

    return {
        "protocol": "027",
        "analysis": "EXPLORATORY_LEXICAL_COVERAGE_NOT_SEMANTIC_VALIDATION",
        "pinned_blob_sha": FILES[0]["blob_sha"],
        "unsupported_pairs": unsupported_pairs,
        "candidate_operator_occurrences_by_family": families,
        "unclassified_word_occurrences": unclassified_words,
        "unclassified_symbol_occurrences": unclassified_symbols,
        "pairs_with_candidate_only_unknown_vocabulary": supported_by_dictionary,
        "pairs_with_unclassified_or_nonoperator_unknown_vocabulary": remaining_unclassified,
        "parser_extended": False,
        "physical_grounding_independently_validated": False,
        "semantic_accuracy_measured": False,
        "novelty_established": False,
        "source_text_or_identifiers_exposed": False,
    }


def run_audit() -> dict:
    return audit_candidate_vocabulary(fetch_pinned(FILES[0]))


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
