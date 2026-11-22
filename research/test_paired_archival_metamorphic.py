"""Metamorphic tests for the small-frame shared-label oracle.

Run only on authorized free cloud CI; no model inference or downloads.
"""
import unittest
from fractions import Fraction

from research.archival_bounds import Counts
from research.paired_archival_oracle import MissingCase, sharp_paired_difference


class PairedOracleMetamorphicTests(unittest.TestCase):
    def test_swapping_policies_negates_and_reverses_bounds(self):
        a = Counts(2, 2, 1, 1)
        b = Counts(2, 2, 2, 0)
        cases = [MissingCase(0, True, 1, True),
                 MissingCase(1, False, 0, True)]
        forward = sharp_paired_difference(a, b, cases)["sharp"]
        swapped = [MissingCase(c.predict_b, c.accept_b,
                               c.predict_a, c.accept_a) for c in cases]
        reverse = sharp_paired_difference(b, a, swapped)["sharp"]
        self.assertEqual(reverse, (-forward[1], -forward[0]))

    def test_missing_case_permutation_invariance(self):
        a = Counts(2, 3, 1, 0)
        b = Counts(2, 3, 2, 1)
        cases = [MissingCase(0, True, 1, True),
                 MissingCase(1, True, 1, False),
                 MissingCase(0, False, 0, True)]
        original = sharp_paired_difference(a, b, cases)
        reversed_order = sharp_paired_difference(a, b, cases[::-1])
        self.assertEqual(original, reversed_order)

    def test_flipping_all_predictions_preserves_identification(self):
        a = Counts(1, 2, 1, 0)
        b = Counts(1, 2, 1, 1)
        cases = [MissingCase(0, True, 1, True),
                 MissingCase(1, True, 0, False)]
        original = sharp_paired_difference(a, b, cases)["sharp"]
        flipped = [MissingCase(1-c.predict_a, c.accept_a,
                               1-c.predict_b, c.accept_b) for c in cases]
        self.assertEqual(original,
                         sharp_paired_difference(a, b, flipped)["sharp"])

    def test_joint_bound_can_be_strictly_tighter(self):
        a = Counts(0, 1, 0, 0)
        b = Counts(0, 1, 0, 0)
        result = sharp_paired_difference(
            a, b, [MissingCase(0, True, 0, True)])
        self.assertEqual(result["sharp"], (Fraction(0), Fraction(0)))
        self.assertEqual(result["conservative"],
                         (Fraction(-1), Fraction(1)))


if __name__ == "__main__":
    unittest.main()
