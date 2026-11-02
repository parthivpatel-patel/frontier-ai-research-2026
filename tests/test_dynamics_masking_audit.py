"""Regression tests for exact dynamics-masking and realizability diagnostics."""
import unittest

from src.admissible_lasso_audit import Actuator, FIXED, FLEXIBLE
from src.dynamics_masking_audit import (
    audit, compare_models, is_restriction, satisfiable_on_model,
)
from src.exhaustive_offset_audit import SearchBudgetExceeded, exact_witness


class DynamicsMaskingTests(unittest.TestCase):
    def test_nested_models_are_ordered_not_symmetric(self):
        self.assertTrue(is_restriction(FLEXIBLE, FIXED))
        self.assertFalse(is_restriction(FIXED, FLEXIBLE))

    def test_non_nested_models_are_rejected(self):
        with self.assertRaises(ValueError):
            compare_models(FIXED, FLEXIBLE)

    def test_unrealizable_one_step_is_not_equivalence(self):
        for model in (FLEXIBLE, FIXED):
            self.assertFalse(satisfiable_on_model(model, 1))
            self.assertTrue(satisfiable_on_model(model, 2))
            self.assertTrue(satisfiable_on_model(model, 3))
            self.assertTrue(satisfiable_on_model(model, 4))
            self.assertTrue(satisfiable_on_model(model, 6))

    def test_unsatisfiable_triggering_formula_is_not_counted_as_separation(self):
        self.assertIsNone(exact_witness(FLEXIBLE, 1, 3).witness)
        self.assertFalse(satisfiable_on_model(FLEXIBLE, 1))

    def test_restriction_masks_six_directional_disagreements(self):
        report = audit()
        self.assertEqual(len(report["comparisons"]), 8)
        self.assertEqual(report["masked_directions"], 6)
        self.assertEqual(sum(c["broad_witness_exists"] for c in report["comparisons"]), 7)
        self.assertEqual(sum(c["restricted_witness_exists"] for c in report["comparisons"]), 1)
        self.assertTrue(all(not c["restricted_witness_exists"] or
                            c["broad_witness_exists"] for c in report["comparisons"]))

    def test_offset_one_unrealizability_is_explicit(self):
        report = audit()
        reverse = next(c for c in report["comparisons"]
                       if c["changed_offset"] == 1
                       and c["direction"] == "changed_true_source_false")
        self.assertTrue(reverse["required_formula_unrealizable_on_broad"])
        self.assertTrue(reverse["required_formula_unrealizable_on_restricted"])
        self.assertFalse(reverse["masked_by_restriction"])

    def test_input_validation_and_budget_exhaustion(self):
        for invalid in (0, 7, True, 1.5):
            with self.assertRaises(ValueError):
                satisfiable_on_model(FLEXIBLE, invalid)
        with self.assertRaises(ValueError):
            satisfiable_on_model(FLEXIBLE, 3, max_nodes=0)
        with self.assertRaises(SearchBudgetExceeded):
            satisfiable_on_model(FLEXIBLE, 3, max_nodes=1)
        with self.assertRaises(ValueError):
            compare_models(FLEXIBLE, FIXED, offsets=(1, 1))

    def test_report_does_not_claim_new_results(self):
        report = audit()
        self.assertEqual(report["source_requirements"], 1)
        self.assertEqual(report["independent_model_predictions"], 0)
        self.assertFalse(report["publication_ready"])
        self.assertEqual(report["status"], "EXACT_TOY_DYNAMICS_MASKING_AUDIT")

    def test_stationary_at_zero_has_no_satisfying_infinite_trace(self):
        stuck = Actuator("stuck", ((0,), (1,), (2,)))
        for offset in (1, 2, 3, 4, 5, 6):
            self.assertFalse(satisfiable_on_model(stuck, offset))


if __name__ == "__main__":
    unittest.main()
