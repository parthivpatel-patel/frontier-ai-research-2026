"""Arithmetic regression tests; examples are synthetic, not research outcomes."""
import unittest
from fractions import Fraction
from research.archival_bounds import Counts, bounds, paired_difference


class BoundsTests(unittest.TestCase):
    def test_documented_example(self):
        r = bounds(Counts(100, 20, 40, 4))
        self.assertEqual(r["observed_risk"], Fraction(1, 10))
        self.assertEqual(r["risk"], (Fraction(1, 15), Fraction(2, 5)))
        self.assertEqual(r["coverage"], (Fraction(1, 3), Fraction(1, 2)))

    def test_no_missing_collapses(self):
        r = bounds(Counts(10, 0, 5, 1))
        self.assertEqual(r["risk"], (Fraction(1, 5), Fraction(1, 5)))

    def test_zero_acceptance_unresolved(self):
        self.assertEqual(bounds(Counts(5, 2, 0, 0))["risk"],
                         (Fraction(0), Fraction(1)))

    def test_zero_acceptance_no_missing(self):
        self.assertIsNone(bounds(Counts(5, 0, 0, 0))["risk"])

    def test_empty_frame(self):
        r = bounds(Counts(0, 0, 0, 0))
        self.assertIsNone(r["coverage"])
        self.assertIsNone(r["risk"])

    def test_invalid_counts(self):
        for args in [(-1, 0, 0, 0), (1, -1, 0, 0),
                     (1, 0, 2, 0), (1, 0, 1, 2)]:
            with self.assertRaises(ValueError):
                Counts(*args)

    def test_noninteger_and_bool(self):
        for args in [(1.0, 0, 0, 0), (True, 0, 0, 0)]:
            with self.assertRaises(TypeError):
                Counts(*args)

    def test_paired_conservative(self):
        a = Counts(10, 2, 5, 1)
        b = Counts(10, 2, 5, 2)
        self.assertEqual(paired_difference(a, b),
                         (Fraction(1, 7)-Fraction(4, 7),
                          Fraction(3, 7)-Fraction(2, 7)))

    def test_mismatched_frames(self):
        with self.assertRaises(ValueError):
            paired_difference(Counts(10, 2, 5, 1), Counts(10, 3, 5, 1))


if __name__ == "__main__":
    unittest.main()
