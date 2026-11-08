"""Protocol 134: metamorphic checks for multi-family analytic eligibility.

These are authored regression tests, not evidence of execution or inferential coverage.
"""
import unittest
from fractions import Fraction

from research.analytic_preflight import analytic_preflight
from research.protocol_133_multifamily_oracle import exact_multifamily_undefined


def paired_rows(family, lineage_acceptances):
    """Each lineage has one intervention; acceptance is (system A, system B)."""
    result = []
    for i, (accept_a, accept_b) in enumerate(lineage_acceptances):
        for system, accepted in (("A", accept_a), ("B", accept_b)):
            result.append({
                "physics_family": family,
                "lineage_id": f"{family}_lineage_{i}",
                "intervention_id": f"{family}_intervention_{i}",
                "system_id": system,
                "accepted": accepted,
                "response_unsafe": False if accepted else None,
            })
    return result


class Protocol134MetamorphicTests(unittest.TestCase):
    def setUp(self):
        self.rows = (
            paired_rows("mechanics", [(True, True), (True, False)])
            + paired_rows("optics", [(True, True), (False, True), (True, True)])
        )
        self.weights = {"mechanics": 2, "optics": 3}

    def test_exact_oracle_agrees_with_joint_acceptance_not_union(self):
        expected = exact_multifamily_undefined((
            (2, (True, False)), (3, (True, False, True))
        ))
        self.assertEqual(expected, Fraction(5, 18))
        result = analytic_preflight(self.rows, self.weights, max_undefined_fraction=1)
        self.assertAlmostEqual(result["conditional_undefined_probability"], float(expected), places=14)

    def test_row_order_and_system_order_invariant(self):
        first = analytic_preflight(self.rows, self.weights, max_undefined_fraction=1)
        second = analytic_preflight(list(reversed(self.rows)), self.weights,
                                    systems=("B", "A"), max_undefined_fraction=1)
        self.assertEqual(first, second)

    def test_positive_weight_rescaling_does_not_change_denominator_risk(self):
        first = analytic_preflight(self.rows, self.weights, max_undefined_fraction=1)
        second = analytic_preflight(self.rows, {"mechanics": 20, "optics": 30},
                                    max_undefined_fraction=1)
        self.assertEqual(first["conditional_undefined_probability"],
                         second["conditional_undefined_probability"])
        self.assertEqual(first["families"], second["families"])

    def test_zero_weight_family_does_not_change_denominator_risk(self):
        extra = paired_rows("thermodynamics", [(False, False), (False, False)])
        first = analytic_preflight(self.rows, self.weights, max_undefined_fraction=1)
        second = analytic_preflight(self.rows + extra,
                                    {**self.weights, "thermodynamics": 0},
                                    max_undefined_fraction=1)
        self.assertEqual(first["conditional_undefined_probability"],
                         second["conditional_undefined_probability"])

    def test_threshold_crossing_does_not_change_exact_probability(self):
        low = analytic_preflight(self.rows, self.weights, max_undefined_fraction=0.27)
        high = analytic_preflight(self.rows, self.weights, max_undefined_fraction=0.28)
        self.assertFalse(low["interval_eligible"])
        self.assertTrue(high["interval_eligible"])
        self.assertEqual(low["conditional_undefined_probability"],
                         high["conditional_undefined_probability"])

    def test_one_sided_acceptance_never_counts_as_joint(self):
        rows = paired_rows("mechanics", [(True, False), (False, True)])
        result = analytic_preflight(rows, {"mechanics": 1}, max_undefined_fraction=1)
        self.assertEqual(result["conditional_undefined_probability"], 1)
        self.assertFalse(result["original_defined"])
        self.assertFalse(result["interval_eligible"])


if __name__ == "__main__":
    unittest.main()
