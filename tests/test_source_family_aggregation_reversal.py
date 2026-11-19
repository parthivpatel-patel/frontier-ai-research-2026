"""Synthetic regression checks for source-family selective-risk aggregation.

No model inference, external dependencies, or empirical data.
Run on an eligible no-charge standard GitHub Actions runner only.
"""
import unittest
from fractions import Fraction


def family_metrics(n, accepted, errors):
    if not (isinstance(n, int) and isinstance(accepted, int) and isinstance(errors, int)):
        raise TypeError("counts must be integers")
    if n <= 0 or not (0 <= errors <= accepted <= n):
        raise ValueError("require n > 0 and 0 <= errors <= accepted <= n")
    return {"coverage": Fraction(accepted, n),
            "risk": Fraction(errors, accepted) if accepted else None}


def micro_risk(rows):
    total_a = sum(a for n, a, e in rows)
    for n, a, e in rows:
        family_metrics(n, a, e)
    return Fraction(sum(e for n, a, e in rows), total_a) if total_a else None


def macro_risk(rows, weights=None):
    if not rows:
        raise ValueError("empty family roster")
    if weights is None:
        weights = [Fraction(1, len(rows))] * len(rows)
    if len(weights) != len(rows) or any(w < 0 for w in weights) or sum(weights) != 1:
        raise ValueError("weights must be nonnegative and sum to one")
    risks = [family_metrics(*r)["risk"] for r in rows]
    if any(r is None and w > 0 for r, w in zip(risks, weights)):
        return None
    return sum((w * r for w, r in zip(weights, risks) if r is not None), Fraction(0))


class AggregationReversalTests(unittest.TestCase):
    def setUp(self):
        # Constructed counts, not measured model performance.
        self.a = [(100, 90, 9), (100, 10, 8)]
        self.b = [(100, 10, 0), (100, 90, 63)]

    def test_micro_reversal(self):
        self.assertEqual(micro_risk(self.a), Fraction(17, 100))
        self.assertEqual(micro_risk(self.b), Fraction(63, 100))

    def test_family_and_macro_reverse_pooled_ranking(self):
        for a, b in zip(self.a, self.b):
            self.assertGreater(family_metrics(*a)["risk"], family_metrics(*b)["risk"])
        self.assertEqual(macro_risk(self.a), Fraction(45, 100))
        self.assertEqual(macro_risk(self.b), Fraction(35, 100))

    def test_global_coverage_equal_but_family_coverage_differs(self):
        self.assertEqual(sum(a for _, a, _ in self.a), sum(a for _, a, _ in self.b))
        self.assertNotEqual(family_metrics(*self.a[0])["coverage"],
                            family_metrics(*self.b[0])["coverage"])

    def test_zero_acceptance_is_undefined_not_zero(self):
        self.assertIsNone(family_metrics(5, 0, 0)["risk"])
        self.assertIsNone(micro_risk([(5, 0, 0)]))
        self.assertIsNone(macro_risk([(5, 0, 0), (5, 1, 0)]))

    def test_explicit_zero_weight_excludes_undefined_family(self):
        self.assertEqual(macro_risk([(5, 0, 0), (5, 1, 0)],
                                    [Fraction(0), Fraction(1)]), Fraction(0))

    def test_invalid_counts_and_weights_rejected(self):
        for row in [(0, 0, 0), (2, 3, 0), (2, 1, 2), (2, -1, 0)]:
            with self.assertRaises(ValueError):
                family_metrics(*row)
        with self.assertRaises(TypeError):
            family_metrics(2.5, 1, 0)
        for weights in [[Fraction(1)], [Fraction(1), Fraction(1)],
                        [Fraction(-1), Fraction(2)]]:
            with self.assertRaises(ValueError):
                macro_risk(self.a, weights)

    def test_exact_weighted_identity(self):
        for rows in [self.a, self.b, [(8, 0, 0), (7, 3, 1)]]:
            accepted = sum(a for _, a, _ in rows)
            weighted = sum((Fraction(a, accepted) * Fraction(e, a)
                            for _, a, e in rows if a), Fraction(0))
            self.assertEqual(micro_risk(rows), weighted)


if __name__ == "__main__":
    unittest.main()
