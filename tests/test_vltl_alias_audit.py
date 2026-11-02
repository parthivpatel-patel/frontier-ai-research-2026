"""Constructed, network-free tests for exploratory Protocol 024."""
import json
import unittest
from unittest.mock import patch

from src.vltl_alias_audit import (
    _signature, audit_lifted, normalize_by_grounded_aliases, run_audit,
)


def definition(action="secure", arg="apple"):
    return {
        "action_canon": action, "args_canon": [arg],
        "action_ref": action, "args_ref": [arg],
    }


def row(rid=1, prediction="prop_1 until prop_2", target=None, metadata=None):
    return {
        "id": rid, "sentence": ["secure", "apple"],
        "tl": ["secure(apple)", "until", "secure(apple)"],
        "masked_tl": target or ["prop_2", "until", "prop_2"],
        "prediction": prediction,
        "prop_dict": metadata if metadata is not None else {
            "prop_1": definition(), "prop_2": definition(),
        },
    }


def encoded(*items):
    return ("\n".join(json.dumps(x) for x in items) + "\n").encode()


class AliasAuditTests(unittest.TestCase):
    def test_alias_only_equivalence(self):
        a = audit_lifted(encoded(row()))
        self.assertEqual((a["metadata_alias_only_nonmatches"],
                          a["remaining_unresolved_nonmatches"]), (1, 0))

    def test_exact_match_separate(self):
        a = audit_lifted(encoded(row(prediction="prop_2 until prop_2")))
        self.assertEqual(a["exact_token_string_matches"], 1)
        self.assertEqual(a["metadata_alias_only_nonmatches"], 0)

    def test_distinct_grounding_not_collapsed(self):
        m = {"prop_1": definition("secure"), "prop_2": definition("drop")}
        a = audit_lifted(encoded(row(metadata=m)))
        self.assertEqual(a["remaining_unresolved_nonmatches"], 1)

    def test_scope_change_not_collapsed(self):
        a = audit_lifted(encoded(row(
            prediction="finally ( prop_1 ) until prop_2")))
        self.assertEqual(a["remaining_unresolved_nonmatches"], 1)

    def test_whitespace_ignored_by_original_exact_metric(self):
        a = audit_lifted(encoded(row(prediction=" prop_2  until  prop_2 ")))
        self.assertEqual(a["exact_token_string_matches"], 1)

    def test_metadata_key_order_is_ignored(self):
        a = definition()
        b = dict(reversed(list(a.items())))
        self.assertEqual(_signature(a), _signature(b))

    def test_missing_grounding_fails_closed(self):
        self.assertIsNone(normalize_by_grounded_aliases(
            "prop_1", {"prop_2": definition()}))

    def test_malformed_grounding_fails_closed(self):
        for d in ({}, {"action_canon": "x"}, {"action_canon": "", "args_canon": ["a"]},
                  {"action_canon": "x", "args_canon": []},
                  {"action_canon": "x", "args_canon": [None]}):
            with self.subTest(d=d):
                self.assertIsNone(_signature(d))

    def test_invalid_symbol_key_fails_closed(self):
        self.assertIsNone(normalize_by_grounded_aliases(
            "prop_1", {"not_prop_1": definition()}))

    def test_partial_token_never_rewritten(self):
        d = {"prop_1": definition(), "prop_2": definition()}
        self.assertEqual(normalize_by_grounded_aliases(
            "myprop_2 prop_2", d), "myprop_2 prop_1")

    def test_proposition_numeric_order(self):
        d = {"prop_10": definition(), "prop_2": definition()}
        self.assertEqual(normalize_by_grounded_aliases(
            "prop_10 prop_2", d), "prop_2 prop_2")

    def test_metadata_full_dictionary_equality_required(self):
        d = {"prop_1": definition(), "prop_2": definition()}
        d["prop_2"]["action_ref"] = "other"
        a = audit_lifted(encoded(row(metadata=d)))
        self.assertEqual(a["remaining_unresolved_nonmatches"], 1)

    def test_blank_and_missing_predictions_not_counted(self):
        a = row(1, " ")
        b = row(2, None)
        c = row(3)
        del b["prediction"]
        result = audit_lifted(encoded(a, b, c))
        self.assertEqual(result["nonblank_predictions"], 1)
        self.assertEqual(result["metadata_alias_only_nonmatches"], 1)

    def test_mixed_accounting(self):
        a = row(1)
        b = row(2, "prop_2 until prop_2")
        c = row(3, "finally prop_1 until prop_2")
        result = audit_lifted(encoded(a, b, c))
        self.assertEqual((result["exact_token_string_matches"],
                          result["metadata_alias_only_nonmatches"],
                          result["remaining_unresolved_nonmatches"]), (1, 1, 1))
        self.assertAlmostEqual(result["conditional_metadata_agreement_fraction"], 2/3)

    def test_duplicate_id_rejected_by_underlying_integrity_gate(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            audit_lifted(encoded(row(1), row(1)))

    def test_no_external_text_in_aggregate_report(self):
        result = audit_lifted(encoded(row()))
        self.assertNotIn("secure apple", json.dumps(result))
        self.assertNotIn("prop_1 until prop_2", json.dumps(result))
        self.assertFalse(result["model_semantic_accuracy_measured"])

    def test_no_network_in_constructed_run(self):
        with patch("src.vltl_alias_audit.fetch_pinned", return_value=encoded(row())) as f:
            result = run_audit()
        f.assert_called_once()
        self.assertEqual(result["metadata_alias_only_nonmatches"], 1)

    def test_unregistered_predicted_prop_remains_unresolved(self):
        a = audit_lifted(encoded(row(prediction="prop_9 until prop_2")))
        self.assertEqual(a["remaining_unresolved_nonmatches"], 1)


if __name__ == "__main__":
    unittest.main()
