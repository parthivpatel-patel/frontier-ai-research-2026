"""Metamorphic checks for exact shared-label paired identification.

Designed for standard free GitHub Actions; no model inference or downloads.
"""
import unittest

from research.archival_bounds import Counts
from research.paired_archival_oracle import MissingCase
from research.paired_archival_linear import sharp_paired_difference_linear


class LinearMetamorphicTests(unittest.TestCase):
    def setUp(self):
        self.a = Counts(3, 3, 2, 1)
        self.b = Counts(3, 3, 2, 0)
        self.missing = [
            MissingCase(0, True, 1, True),
            MissingCase(1, False, 0, True),
            MissingCase(1, True, 1, False),
        ]

    def test_policy_swap_negates_and_reverses_interval(self):
        original = sharp_paired_difference_linear(self.a, self.b, self.missing)
        swapped = [MissingCase(c.predict_b, c.accept_b, c.predict_a, c.accept_a)
                   for c in self.missing]
        reverse = sharp_paired_difference_linear(self.b, self.a, swapped)
        self.assertEqual(reverse["sharp"], (-original["sharp"][1], -original["sharp"][0]))
        self.assertEqual(reverse["defined_assignments"], original["defined_assignments"])

    def test_case_permutation_preserves_interval(self):
        original = sharp_paired_difference_linear(self.a, self.b, self.missing)
        reversed_cases = sharp_paired_difference_linear(self.a, self.b, list(reversed(self.missing)))
        self.assertEqual(original, reversed_cases)

    def test_complement_predictions_with_complemented_verified_errors(self):
        # For accepted verified binary examples, complementing predictions
        # changes each error into a correct decision and vice versa.
        ac = Counts(self.a.n, self.a.m, self.a.accepted, self.a.accepted - self.a.errors)
        bc = Counts(self.b.n, self.b.m, self.b.accepted, self.b.accepted - self.b.errors)
        complemented = [MissingCase(1-c.predict_a, c.accept_a,
                                   1-c.predict_b, c.accept_b) for c in self.missing]
        original = sharp_paired_difference_linear(self.a, self.b, self.missing)
        transformed = sharp_paired_difference_linear(ac, bc, complemented)
        self.assertEqual(transformed["sharp"], (-original["sharp"][1], -original["sharp"][0]))

    def test_shared_labels_can_be_strictly_tighter_than_independent_envelope(self):
        a = Counts(0, 1, 0, 0)
        b = Counts(0, 1, 0, 0)
        missing = [MissingCase(0, True, 0, True)]
        result = sharp_paired_difference_linear(a, b, missing)
        self.assertEqual(result["sharp"], (0, 0))
        self.assertEqual(result["conservative"], (-1, 1))


if __name__ == "__main__":
    unittest.main()
