"""Regression tests for sharp linear-time paired bounds (not executed here)."""
import itertools
import unittest
from fractions import Fraction
from research.paired_bounds_linear import paired_risk_difference_bounds


class PairedBoundsLinearTests(unittest.TestCase):
    def test_shared_unknown_cancels(self):
        self.assertEqual(
            paired_risk_difference_bounds([True], [True], [None]),
            (Fraction(0), Fraction(0)),
        )

    def test_disjoint_unknowns(self):
        self.assertEqual(
            paired_risk_difference_bounds([True, False], [False, True], [None, None]),
            (Fraction(-1), Fraction(1)),
        )

    def test_observed(self):
        self.assertEqual(
            paired_risk_difference_bounds([True, True], [True, False], [1, 0]),
            (Fraction(-1, 2), Fraction(-1, 2)),
        )

    def test_zero_acceptance_undefined(self):
        with self.assertRaises(ValueError):
            paired_risk_difference_bounds([False], [True], [None])

    def test_invalid_types(self):
        with self.assertRaises(TypeError):
            paired_risk_difference_bounds([1], [True], [None])
        with self.assertRaises(TypeError):
            paired_risk_difference_bounds([True], [True], [True])

    def test_exhaustive_oracle_up_to_three_claims(self):
        for n in range(1, 4):
            for a in itertools.product((False, True), repeat=n):
                if not any(a):
                    continue
                for b in itertools.product((False, True), repeat=n):
                    if not any(b):
                        continue
                    for labels in itertools.product((0, 1, None), repeat=n):
                        unknown = [i for i, v in enumerate(labels) if v is None]
                        outcomes = []
                        for bits in itertools.product((0, 1), repeat=len(unknown)):
                            resolved = list(labels)
                            for i, bit in zip(unknown, bits):
                                resolved[i] = bit
                            outcomes.append(
                                Fraction(sum(v for flag, v in zip(a, resolved) if flag), sum(a))
                                - Fraction(sum(v for flag, v in zip(b, resolved) if flag), sum(b))
                            )
                        self.assertEqual(
                            paired_risk_difference_bounds(a, b, labels),
                            (min(outcomes), max(outcomes)),
                        )


if __name__ == "__main__":
    unittest.main()
