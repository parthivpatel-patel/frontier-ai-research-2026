"""Protocol 137: independent, deterministic shared-index counterexamples."""
import unittest
from fractions import Fraction

from research.protocol_137_shared_index_oracle import (
    exact_shared_index_undefined,
    marginal_union_bounds,
)
from research.protocol_135_closed_form_oracle import closed_form_undefined


class SharedIndexOracleTests(unittest.TestCase):
    def test_identical_flags_coupling(self):
        families = [(1, (True, False)), (1, (True, False))]
        self.assertEqual(exact_shared_index_undefined(families), Fraction(1, 4))
        self.assertEqual(closed_form_undefined(families), Fraction(7, 16))
        self.assertEqual(marginal_union_bounds(families), (Fraction(1, 4), Fraction(1, 2)))

    def test_complementary_flags_coupling(self):
        families = [(1, (True, False)), (1, (False, True))]
        self.assertEqual(exact_shared_index_undefined(families), Fraction(1, 2))
        self.assertEqual(closed_form_undefined(families), Fraction(7, 16))

    def test_zero_weight_exclusion(self):
        families = [(1, (True, False)), (0, (False, True))]
        self.assertEqual(exact_shared_index_undefined(families), Fraction(1, 4))

    def test_positive_rescaling(self):
        base = [(1, (True, False)), (2, (False, True))]
        scaled = [(10, (True, False)), (20, (False, True))]
        self.assertEqual(exact_shared_index_undefined(base), exact_shared_index_undefined(scaled))

    def test_all_accepted(self):
        self.assertEqual(exact_shared_index_undefined([(1, (True, True))]), Fraction(0))

    def test_none_accepted(self):
        self.assertEqual(exact_shared_index_undefined([(1, (False, False))]), Fraction(1))

    def test_unequal_lineage_counts_rejected(self):
        with self.assertRaises(ValueError):
            exact_shared_index_undefined([(1, (True, False)), (1, (True, False, True))])

    def test_all_zero_weights_rejected(self):
        with self.assertRaises(ValueError):
            exact_shared_index_undefined([(0, (True, False))])

    def test_nonboolean_flags_rejected(self):
        with self.assertRaises(ValueError):
            exact_shared_index_undefined([(1, (1, False))])


if __name__ == "__main__":
    unittest.main()
