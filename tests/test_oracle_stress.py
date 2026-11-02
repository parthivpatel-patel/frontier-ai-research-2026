"""Regression checks for known limitations of semantic-oracle diagnostics."""
import unittest
from fractions import Fraction

from src.oracle_stress import denominator_stress, reference_omission_witness, run_stress


class OracleStressTests(unittest.TestCase):
    def test_omitted_reference_invalidates_a_pass(self):
        case = reference_omission_witness()
        self.assertEqual(case["observed_supplied_error_set"], [0])
        self.assertFalse(case["candidate_predicate_true_at_witness"])
        self.assertTrue(case["alternative_predicate_true_at_witness"])

    def test_witness_exact(self):
        case = reference_omission_witness()
        self.assertEqual(Fraction(case["witness_next_position"]), Fraction(17, 20))
        self.assertEqual([Fraction(x) for x in case["physical_witness"]],
                         [Fraction(1, 2), Fraction(0), Fraction(7, 20)])

    def test_joint_risk_can_be_small_when_accepted_risk_is_one(self):
        case = denominator_stress(100)
        self.assertEqual(case["accepted_error_rate"], "1")
        self.assertEqual(case["joint_error_rate"], "1/100")
        self.assertEqual(case["acceptance_fraction"], "1/100")

    def test_single_instruction_denominators_agree(self):
        case = denominator_stress(1)
        self.assertEqual(case["joint_error_rate"], case["accepted_error_rate"])

    def test_invalid_total_rejected(self):
        for value in (0, -1, True, 1.5):
            with self.subTest(value=value), self.assertRaises(ValueError):
                denominator_stress(value)

    def test_complete_supplied_set_is_ambiguous(self):
        self.assertEqual(
            run_stress()["complete_supplied_set_decision_at_zero_tolerance"],
            "depends_on_unresolved_interpretation",
        )


if __name__ == "__main__":
    unittest.main()
