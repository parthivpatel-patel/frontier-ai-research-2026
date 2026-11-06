"""Dependency-free regression tests for Protocol 093 (not yet cloud executed)."""
import itertools
import unittest
from fractions import Fraction
from research.stratified_paired_bounds import stratified_bounds


class StratifiedBoundsTests(unittest.TestCase):
    def test_identical_acceptance(self):
        bounds, mixture = stratified_bounds([("mechanics", True, True, None)])
        self.assertEqual(bounds["mechanics"], (Fraction(0), Fraction(0)))
        self.assertIsNone(mixture)

    def test_missing_label_extrema(self):
        rows = [("circuits", True, False, None),
                ("circuits", False, True, None)]
        bounds, _ = stratified_bounds(rows)
        self.assertEqual(bounds["circuits"], (Fraction(-1), Fraction(1)))

    def test_exact_mixture(self):
        rows = [("a", True, False, None), ("a", False, True, None),
                ("b", True, True, True)]
        bounds, mixture = stratified_bounds(
            rows, {"a": Fraction(1, 4), "b": Fraction(3, 4)})
        self.assertEqual(mixture, (Fraction(-1, 4), Fraction(1, 4)))
        self.assertEqual(bounds["b"], (Fraction(0), Fraction(0)))

    def test_exhaustive_oracle(self):
        patterns = list(itertools.product((False, True), repeat=4))
        for aa in patterns:
            for bb in patterns:
                if not any(aa) or not any(bb):
                    continue
                rows = [("x", a, b, None) for a, b in zip(aa, bb)]
                (lo, hi) = stratified_bounds(rows)[0]["x"]
                brute = []
                for labels in patterns:
                    risk_a = Fraction(sum(a and y for a, y in zip(aa, labels)), sum(aa))
                    risk_b = Fraction(sum(b and y for b, y in zip(bb, labels)), sum(bb))
                    brute.append(risk_a - risk_b)
                self.assertEqual((lo, hi), (min(brute), max(brute)))

    def test_undefined_stratum(self):
        with self.assertRaises(ValueError):
            stratified_bounds([("x", True, False, None)])

    def test_reject_bad_inputs(self):
        for rows in ([("x", 1, True, None)],
                     [("x", True, True, 0)],
                     [("", True, True, None)]):
            with self.assertRaises((ValueError, TypeError)):
                stratified_bounds(rows)

    def test_reject_bad_mixture(self):
        rows = [("x", True, True, None)]
        for weights in ({"x": Fraction(1, 2)}, {"x": -1},
                        {"x": 1, "extra": 0}, {"x": 1.0}):
            with self.assertRaises((ValueError, TypeError)):
                stratified_bounds(rows, weights)


if __name__ == "__main__":
    unittest.main()
