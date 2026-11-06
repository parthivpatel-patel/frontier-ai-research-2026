"""Protocol 095: synthetic Simpson reversal regression oracle.

Standard-library only. Synthetic arithmetic, NOT empirical model evaluation.
Run via: python -m unittest discover -s tests -p 'test_protocol_096_simpson_fixture.py'
"""
from fractions import Fraction
import unittest


def compare_families(rows, weights):
    """rows: family -> (population, A accepted, A unsafe, B accepted, B unsafe)."""
    if not rows or set(rows) != set(weights):
        raise ValueError("family weights must match every family")
    if any(type(w) is not Fraction or w < 0 for w in weights.values()):
        raise ValueError("weights must be nonnegative Fractions")
    if sum(weights.values(), Fraction(0)) != 1:
        raise ValueError("weights must sum to one")
    totals = [0, 0, 0, 0, 0]
    differences = {}
    for family, values in rows.items():
        if len(values) != 5 or any(type(x) is not int for x in values):
            raise ValueError("counts must be five exact integers")
        n, a, ay, b, by = values
        if not (n > 0 and 0 <= ay <= a <= n and 0 <= by <= b <= n):
            raise ValueError("invalid counts or unsafe-label mapping")
        if a == 0 or b == 0:
            raise ValueError("selective risk undefined for zero acceptance")
        differences[family] = Fraction(ay, a) - Fraction(by, b)
        for i, x in enumerate(values):
            totals[i] += x
    n, a, ay, b, by = totals
    return {
        "coverage_a": Fraction(a, n),
        "coverage_b": Fraction(b, n),
        "pooled_difference": Fraction(ay, a) - Fraction(by, b),
        "family_differences": differences,
        "standardized_difference": sum(
            (weights[k] * differences[k] for k in rows), Fraction(0)
        ),
    }


class Protocol096SimpsonFixture(unittest.TestCase):
    def setUp(self):
        self.rows = {
            "mechanics": (100, 90, 9, 10, 0),
            "circuits": (100, 10, 9, 90, 72),
        }
        self.weights = {"mechanics": Fraction(1, 2), "circuits": Fraction(1, 2)}

    def test_reversal_exact(self):
        result = compare_families(self.rows, self.weights)
        self.assertEqual(result["coverage_a"], Fraction(1, 2))
        self.assertEqual(result["coverage_b"], Fraction(1, 2))
        self.assertEqual(result["pooled_difference"], Fraction(-27, 50))
        self.assertEqual(result["family_differences"]["mechanics"], Fraction(1, 10))
        self.assertEqual(result["family_differences"]["circuits"], Fraction(1, 10))
        self.assertEqual(result["standardized_difference"], Fraction(1, 10))

    def test_zero_acceptance_rejected(self):
        rows = dict(self.rows)
        rows["mechanics"] = (100, 0, 0, 10, 0)
        with self.assertRaises(ValueError):
            compare_families(rows, self.weights)

    def test_invalid_unsafe_count_rejected(self):
        rows = dict(self.rows)
        rows["mechanics"] = (100, 90, 91, 10, 0)
        with self.assertRaises(ValueError):
            compare_families(rows, self.weights)

    def test_missing_family_weight_rejected(self):
        with self.assertRaises(ValueError):
            compare_families(self.rows, {"mechanics": Fraction(1)})

    def test_nonunit_weight_rejected(self):
        with self.assertRaises(ValueError):
            compare_families(self.rows, {k: Fraction(1, 3) for k in self.rows})

    def test_noninteger_counts_rejected(self):
        rows = dict(self.rows)
        rows["mechanics"] = (100, 90.0, 9, 10, 0)
        with self.assertRaises(ValueError):
            compare_families(rows, self.weights)


if __name__ == "__main__":
    unittest.main()
