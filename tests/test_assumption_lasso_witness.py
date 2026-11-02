"""Constructed, network-free tests for Protocol 025; cloud CI only."""
import json
import unittest
from unittest.mock import patch

from src.assumption_lasso_witness import (
    UnsupportedFormula, tokenize, parse, find_counterexample,
)
from src.vltl_assumption_sensitivity_audit import audit_assumptions, run_audit


def definition(action="secure"):
    return {"action_canon": action, "args_canon": ["apple"],
            "action_ref": action, "args_ref": ["apple"]}


def row(i, pred, target, metadata=None):
    return {
        "id": i, "sentence": ["secure", "apple"],
        "tl": ["secure(apple)"],
        "masked_tl": target.split(),
        "prediction": pred,
        "prop_dict": metadata if metadata is not None else
        {"prop_1": definition(), "prop_2": definition()},
    }


def encoded(*rows):
    return ("\n".join(json.dumps(r) for r in rows) + "\n").encode()


class BoundedLassoTests(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(find_counterexample("prop_1", "prop_1")["status"],
                         "no_witness_within_bound")

    def test_distinct_atoms_witness(self):
        self.assertEqual(find_counterexample("prop_1", "prop_2")["status"], "witness")

    def test_assumed_identity_removes_witness(self):
        self.assertEqual(find_counterexample(
            "prop_1", "prop_2", equalities=(("prop_1", "prop_2"),)
        )["status"], "no_witness_within_bound")

    def test_eventually_distinct_atoms_witness(self):
        self.assertEqual(find_counterexample(
            "finally prop_1", "finally prop_2")["status"], "witness")

    def test_eventually_assumed_equal(self):
        self.assertEqual(find_counterexample(
            "finally prop_1", "finally prop_2",
            equalities=(("prop_1", "prop_2"),)
        )["status"], "no_witness_within_bound")

    def test_next_is_not_present(self):
        result = find_counterexample("next prop_1", "prop_1")
        self.assertEqual(result["status"], "witness")
        self.assertEqual(result["witness_states"], 2)

    def test_always_eventually_differ(self):
        self.assertEqual(find_counterexample(
            "always prop_1", "finally prop_1")["status"], "witness")

    def test_until_eventually_differ(self):
        self.assertEqual(find_counterexample(
            "prop_1 until prop_2", "finally prop_2")["status"], "witness")

    def test_de_morgan_temporal_duality(self):
        self.assertEqual(find_counterexample(
            "always prop_1", "not finally not prop_1")["status"],
            "no_witness_within_bound")

    def test_operator_aliases(self):
        self.assertEqual(find_counterexample(
            "G prop_1", "! F ! prop_1")["status"], "no_witness_within_bound")

    def test_implication_equivalence(self):
        self.assertEqual(find_counterexample(
            "prop_1 -> prop_2", "not prop_1 or prop_2")["status"],
            "no_witness_within_bound")

    def test_true_until(self):
        self.assertEqual(find_counterexample(
            "true until prop_1", "finally prop_1")["status"],
            "no_witness_within_bound")

    def test_budget_exhaustion_not_equivalence(self):
        self.assertEqual(find_counterexample(
            "prop_1", "prop_1", max_cases=1)["status"], "incomplete_budget")

    def test_unsupported_proposition_count(self):
        self.assertEqual(find_counterexample(
            "prop_1 and prop_2 and prop_3", "prop_4",
            max_propositions=3)["status"], "unsupported_proposition_count")

    def test_reject_unknown_operator(self):
        with self.assertRaises(UnsupportedFormula):
            parse("prop_1 weakuntil prop_2")

    def test_reject_malformed_parentheses(self):
        with self.assertRaises(UnsupportedFormula):
            parse("( prop_1 until prop_2")

    def test_reject_bad_characters(self):
        with self.assertRaises(UnsupportedFormula):
            tokenize("prop_1 ; prop_2")

    def test_reject_invalid_assumptions(self):
        with self.assertRaises(ValueError):
            find_counterexample("prop_1", "prop_2",
                                equalities=(("prop_1", "prop_9"),))

    def test_reject_invalid_budget(self):
        with self.assertRaises(ValueError):
            find_counterexample("prop_1", "prop_2", max_cases=0)

    def test_aggregate_alias_case_unconstrained_witness(self):
        result = audit_assumptions(encoded(row(
            1, "prop_1 until prop_2", "prop_2 until prop_2")))
        self.assertEqual(result["groups"]["alias_only"], 1)
        self.assertEqual(result["status_counts"]["alias_only"]
                         ["unconstrained"]["witness"], 1)
        self.assertEqual(result["status_counts"]["alias_only"]
                         ["recorded_metadata_equalities"]
                         ["no_witness_within_bound"], 1)

    def test_aggregate_residual_counterexample(self):
        result = audit_assumptions(encoded(row(
            1, "finally prop_1", "always prop_1")))
        self.assertEqual(result["groups"]["unresolved"], 1)
        self.assertEqual(result["status_counts"]["unresolved"]
                         ["unconstrained"]["witness"], 1)

    def test_aggregate_unsupported_syntax(self):
        result = audit_assumptions(encoded(row(
            1, "prop_1 weakuntil prop_2", "prop_1 until prop_2")))
        self.assertEqual(result["status_counts"]["unresolved"]
                         ["unconstrained"]["unsupported_syntax"], 1)

    def test_aggregate_no_external_text(self):
        result = audit_assumptions(encoded(row(
            1, "prop_1 until prop_2", "prop_2 until prop_2")))
        self.assertNotIn("secure apple", json.dumps(result))
        self.assertNotIn("prop_1 until prop_2", json.dumps(result))
        self.assertFalse(result["model_semantic_accuracy_measured"])

    def test_mocked_cloud_fetch(self):
        data = encoded(row(1, "prop_1 until prop_2", "prop_2 until prop_2"))
        with patch("src.vltl_assumption_sensitivity_audit.fetch_pinned",
                   return_value=data) as fetch:
            result = run_audit()
        fetch.assert_called_once()
        self.assertEqual(result["nonmatching_records"], 1)


if __name__ == "__main__":
    unittest.main()
