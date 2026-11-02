"""Negative controls and physical-admissibility tests (toy finite graph)."""
import unittest

from src.admissible_lasso_audit import (
    FIXED, FLEXIBLE, StateLasso, audit, changed_offsets,
    find_witness, unique_fixed_trace,
)
from src.independent_source_audit import holds


class AdmissibleLassoAuditTests(unittest.TestCase):
    def test_fixed_actuator_has_exactly_one_infinite_trace(self):
        word = unique_fixed_trace()
        self.assertTrue(word.valid(FIXED))
        self.assertFalse(word.valid(FLEXIBLE) is False)
        self.assertEqual(word.propositions().at(1000), frozenset({"b"}))

    def test_fixed_dynamics_restrict_disagreement_to_offset_one(self):
        for n in changed_offsets():
            found = find_witness(FIXED, n, True)
            self.assertEqual(found is not None, n == 1)
            self.assertIsNone(find_witness(FIXED, n, False))

    def test_bounded_control_admits_all_four_forward_disagreements(self):
        for n in changed_offsets():
            witness = find_witness(FLEXIBLE, n, True)
            self.assertIsNotNone(witness, msg=f"missing offset {n}")
            self.assertTrue(witness.valid(FLEXIBLE))
            trace = witness.propositions()
            self.assertTrue(holds("offset", 3, trace, inherited_formula=True))
            self.assertFalse(holds("offset", n, trace, inherited_formula=False))

    def test_bounded_control_has_reverse_witness_for_offset_two(self):
        witness = find_witness(FLEXIBLE, 2, False)
        self.assertIsNotNone(witness)
        trace = witness.propositions()
        self.assertFalse(holds("offset", 3, trace, inherited_formula=True))
        self.assertTrue(holds("offset", 2, trace, inherited_formula=False))

    def test_one_step_to_b_is_unreachable_from_initial_a(self):
        self.assertEqual(FLEXIBLE.edges[0], (0, 1))
        self.assertNotIn(2, FLEXIBLE.edges[0])
        # The target offset-1 G requirement cannot hold: a holds at t=0
        # but b cannot hold at t=1.  This is a simple exact reachability fact.
        self.assertIsNone(find_witness(FLEXIBLE, 1, False))

    def test_logical_disagreement_can_be_physically_impossible(self):
        # a at t=0, b at t=1 and t=3, no b at t=2.
        word = StateLasso((0, 2, 1, 2), (1,))
        trace = word.propositions()
        self.assertTrue(holds("offset", 3, trace, inherited_formula=True))
        self.assertFalse(holds("offset", 2, trace, inherited_formula=False))
        self.assertFalse(word.valid(FLEXIBLE))  # jump 0 -> 2 forbidden
        self.assertFalse(word.valid(FIXED))

    def test_loop_closure_is_checked(self):
        # 2 -> 0 is not an allowed transition.
        self.assertFalse(StateLasso((0, 1, 2), (0,)).valid(FLEXIBLE))
        self.assertFalse(StateLasso((), ()).valid(FLEXIBLE))

    def test_bounded_absence_is_not_equivalence(self):
        self.assertIsNone(find_witness(FLEXIBLE, 6, True, 1, 1))
        self.assertIsNotNone(find_witness(FLEXIBLE, 6, True, 9, 3))
        self.assertIn("BOUNDED_SEARCH_ONLY", audit()["comparisons"][0][
            "absence_interpretation"])

    def test_external_independence_and_report_guards(self):
        report = audit()
        self.assertEqual(changed_offsets(), (1, 2, 4, 6))
        self.assertEqual(report["external_originals_in_this_experiment"], 1)
        self.assertEqual(len(report["comparisons"]), 8)
        self.assertFalse(report["publication_ready"])
        self.assertEqual(report["status"], "TOY_DYNAMICS_FILTER_NOT_MODEL_PERFORMANCE")

    def test_unsupported_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            find_witness(FLEXIBLE, 3, True)
        with self.assertRaises(ValueError):
            list(__import__("src.admissible_lasso_audit", fromlist=["candidates"])
                 .candidates(FLEXIBLE, 0, 1))


if __name__ == "__main__":
    unittest.main()
