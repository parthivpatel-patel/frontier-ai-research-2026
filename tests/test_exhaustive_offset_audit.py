"""Complete finite-product monitor regression and falsification controls."""
import unittest

from src.admissible_lasso_audit import Actuator, FLEXIBLE, FIXED
from src.exhaustive_offset_audit import (
    SearchBudgetExceeded, _bad_at_next, audit, exact_witness,
)
from src.independent_source_audit import holds


class ExhaustiveOffsetAuditTests(unittest.TestCase):
    def test_offset_monitor_checks_the_correct_time(self):
        self.assertTrue(_bad_at_next((0,), 1, 1))
        self.assertFalse(_bad_at_next((0,), 1, 2))
        self.assertTrue(_bad_at_next((0, 1), 1, 2))
        self.assertFalse(_bad_at_next((0, 1), 2, 2))

    def test_flexible_model_has_four_forward_witnesses(self):
        for n in (1, 2, 4, 6):
            result = exact_witness(FLEXIBLE, 3, n)
            self.assertTrue(result.complete)
            self.assertIsNotNone(result.witness, msg=str(n))
            self.assertTrue(result.witness.valid(FLEXIBLE))
            trace = result.witness.propositions()
            self.assertTrue(holds('offset', 3, trace, inherited_formula=False))
            self.assertFalse(holds('offset', n, trace, inherited_formula=False))

    def test_flexible_reverse_is_exactly_impossible_for_one_step(self):
        self.assertIsNone(exact_witness(FLEXIBLE, 1, 3).witness)
        for n in (2, 4, 6):
            self.assertIsNotNone(exact_witness(FLEXIBLE, n, 3).witness)

    def test_fixed_model_is_exhaustively_checked(self):
        for n in (1, 2, 4, 6):
            self.assertEqual(exact_witness(FIXED, 3, n).witness is not None, n == 1)
            self.assertIsNone(exact_witness(FIXED, n, 3).witness)

    def test_no_separating_trace_when_both_formulas_always_false(self):
        stationary = Actuator('stuck_at_zero', ((0,), (1,), (2,)))
        self.assertIsNone(exact_witness(stationary, 3, 6).witness)
        self.assertIsNone(exact_witness(stationary, 6, 3).witness)

    def test_no_separating_trace_when_all_requirements_hold(self):
        immediate_b = Actuator('immediate_b', ((2,), (2,), (2,)))
        for n in (1, 2, 4, 6):
            self.assertIsNone(exact_witness(immediate_b, 3, n).witness)
            self.assertIsNone(exact_witness(immediate_b, n, 3).witness)

    def test_resource_exhaustion_is_explicit_not_equivalence(self):
        with self.assertRaises(SearchBudgetExceeded):
            exact_witness(FLEXIBLE, 3, 6, max_nodes=1)

    def test_invalid_parameters_are_rejected(self):
        for x, y in ((0, 3), (3, 3), (3, 7), (True, 3), (3, False)):
            with self.assertRaises(ValueError):
                exact_witness(FLEXIBLE, x, y)
        with self.assertRaises(ValueError):
            exact_witness(FLEXIBLE, 3, 6, max_nodes=0)

    def test_report_provenance_and_nonpublication_guards(self):
        result = audit()
        self.assertEqual(result['external_originals'], 1)
        self.assertEqual(result['independent_model_predictions'], 0)
        self.assertTrue(result['all_checks_complete'])
        self.assertEqual(len(result['comparisons']), 8)
        self.assertFalse(result['publication_ready'])
        self.assertTrue(all(c['inherited_true_changed_false']['complete']
                            and c['inherited_false_changed_true']['complete']
                            for c in result['comparisons']))


if __name__ == '__main__':
    unittest.main()
