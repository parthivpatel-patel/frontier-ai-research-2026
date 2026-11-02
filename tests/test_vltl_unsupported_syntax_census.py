"""Constructed network-free Protocol 026 tests; execute on public cloud CI."""
import json
import unittest
from unittest.mock import patch

from src.vltl_unsupported_syntax_census import (
    audit_unsupported, run_audit, _failure_class, _lexical_counts,
    OP_NAMES, TOKEN_CLASSES,
)
from src.assumption_lasso_witness import UnsupportedFormula


def definition():
    return {"action_canon": "secure", "args_canon": ["apple"],
            "action_ref": "secure", "args_ref": ["apple"]}


def record(i, prediction, reference, prop_dict=None):
    return {"id": i, "sentence": ["secure", "apple"],
            "tl": ["secure(apple)"], "masked_tl": reference.split(),
            "prediction": prediction,
            "prop_dict": prop_dict if prop_dict is not None else
            {"prop_1": definition(), "prop_2": definition()}}


def pack(*rows):
    return ("\n".join(json.dumps(row) for row in rows) + "\n").encode()


class SyntaxCensusTests(unittest.TestCase):
    def test_alias_unsupported_prediction(self):
        d = audit_unsupported(pack(record(1, "weakuntil prop_1", "weakuntil prop_2")))
        self.assertEqual(d["unsupported_pairs"], 1)
        self.assertEqual(d["unsupported_by_prior_group"]["alias_only"], 1)
        self.assertEqual(d["parse_failure_sides"]["both"], 1)

    def test_unresolved_unknown_operator(self):
        d = audit_unsupported(pack(record(1, "weakuntil prop_1", "prop_2")))
        self.assertEqual(d["unsupported_by_prior_group"]["unresolved"], 1)
        self.assertEqual(d["parse_failure_sides"]["prediction_only"], 1)
        self.assertEqual(d["failed_formula_side_classes"]["unknown_word_or_operator"], 1)

    def test_unknown_punctuation(self):
        d = audit_unsupported(pack(record(1, "prop_1 ; prop_2", "prop_1")))
        self.assertEqual(d["failed_formula_side_classes"]["unknown_character"], 1)
        self.assertEqual(d["other_token_occurrences_across_both_sides_of_unsupported_pairs"]["unknown_symbol"], 1)

    def test_reference_only_failure(self):
        d = audit_unsupported(pack(record(1, "prop_1", "prop_1 weakuntil prop_2")))
        self.assertEqual(d["parse_failure_sides"]["reference_only"], 1)

    def test_both_failure(self):
        d = audit_unsupported(pack(record(1, "weakuntil prop_1", "weakuntil prop_2")))
        self.assertEqual(d["parse_failure_sides"]["both"], 1)
        self.assertEqual(sum(d["failed_formula_side_classes"].values()), 2)

    def test_valid_mismatch_is_not_unsupported(self):
        d = audit_unsupported(pack(record(1, "finally prop_1", "always prop_1")))
        self.assertEqual(d["unsupported_pairs"], 0)
        self.assertEqual(d["parsed_pairs"], 1)

    def test_exact_is_excluded(self):
        d = audit_unsupported(pack(record(1, "prop_1", "prop_1")))
        self.assertEqual(d["nonexact_pairs"], 0)

    def test_known_operator_census(self):
        ops = {k: 0 for k in OP_NAMES}
        cls = {k: 0 for k in TOKEN_CLASSES}
        _lexical_counts("G ( prop_1 -> F prop_2 )", ops, cls)
        self.assertEqual(ops["always"], 1)
        self.assertEqual(ops["implies"], 1)
        self.assertEqual(ops["finally"], 1)
        self.assertEqual(cls["proposition"], 2)
        self.assertEqual(cls["parenthesis"], 2)

    def test_unrecognized_words_never_returned(self):
        d = audit_unsupported(pack(record(1, "SECRETWORD prop_1", "prop_2")))
        output = json.dumps(d)
        self.assertNotIn("SECRETWORD", output)
        self.assertNotIn("secure", output)
        self.assertNotIn("prop_1", output)
        self.assertEqual(d["other_token_occurrences_across_both_sides_of_unsupported_pairs"]["unknown_word"], 1)

    def test_unsupported_is_not_accuracy(self):
        d = audit_unsupported(pack(record(1, "weakuntil prop_1", "prop_1")))
        self.assertFalse(d["semantic_accuracy_measured"])
        self.assertFalse(d["scientific_novelty_established"])

    def test_invalid_source_ids_fail_closed(self):
        with self.assertRaises(ValueError):
            audit_unsupported(pack(record(1, "prop_1", "prop_2"),
                                   record(1, "prop_2", "prop_1")))

    def test_mocked_pinned_cloud_fetch(self):
        data = pack(record(1, "weakuntil prop_1", "prop_2"))
        with patch("src.vltl_unsupported_syntax_census.fetch_pinned", return_value=data) as fetch:
            result = run_audit()
        fetch.assert_called_once()
        self.assertEqual(result["unsupported_pairs"], 1)

    def test_failure_class_is_fixed_vocabulary(self):
        for raw in ("unsupported operator", "unknown token", "missing operand",
                    "empty or oversized formula"):
            self.assertIn(_failure_class(UnsupportedFormula(raw)),
                          ("unknown_character", "unknown_word_or_operator",
                           "grammar_or_operand", "length_or_token_limit"))


if __name__ == "__main__":
    unittest.main()
