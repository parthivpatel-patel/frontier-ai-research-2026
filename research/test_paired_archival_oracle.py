"""Deterministic reference cases; intended for verified free-cloud CI."""
import unittest
from fractions import Fraction

from research.archival_bounds import Counts
from research.paired_archival_oracle import MissingCase, sharp_paired_difference


class PairedOracleTests(unittest.TestCase):
    def test_same_prediction_cancels(self):
        a = Counts(1, 1, 1, 0)
        b = Counts(1, 1, 1, 0)
        r = sharp_paired_difference(a, b, [MissingCase(0, True, 0, True)])
        self.assertEqual(r["sharp"], (Fraction(0), Fraction(0)))
        self.assertEqual(r["defined_assignments"], 2)

    def test_opposite_prediction(self):
        a = Counts(0, 1, 0, 0)
        b = Counts(0, 1, 0, 0)
        r = sharp_paired_difference(a, b, [MissingCase(0, True, 1, True)])
        self.assertEqual(r["sharp"], (Fraction(-1), Fraction(1)))

    def test_one_sided_abstention(self):
        a = Counts(1, 1, 1, 0)
        b = Counts(1, 1, 1, 0)
        r = sharp_paired_difference(a, b, [MissingCase(0, True, 0, False)])
        self.assertEqual(r["sharp"], (Fraction(0), Fraction(1, 2)))

    def test_no_missing(self):
        r = sharp_paired_difference(Counts(2, 0, 2, 1),
                                    Counts(2, 0, 2, 0), [])
        self.assertEqual(r["sharp"], (Fraction(1, 2), Fraction(1, 2)))

    def test_undefined_risk(self):
        r = sharp_paired_difference(Counts(0, 1, 0, 0),
                                    Counts(0, 1, 0, 0),
                                    [MissingCase(0, False, 1, True)])
        self.assertIsNone(r["sharp"])
        self.assertEqual(r["undefined_assignments"], 2)

    def test_mismatched_frame(self):
        with self.assertRaises(ValueError):
            sharp_paired_difference(Counts(1, 1, 1, 0),
                                    Counts(1, 1, 1, 0), [])

    def test_limit(self):
        with self.assertRaises(ValueError):
            sharp_paired_difference(Counts(0, 1, 0, 0),
                                    Counts(0, 1, 0, 0),
                                    [MissingCase(0, True, 1, True)],
                                    max_missing=0)

    def test_invalid_case(self):
        with self.assertRaises(TypeError):
            MissingCase(0, 1, 1, True)


if __name__ == "__main__":
    unittest.main()
