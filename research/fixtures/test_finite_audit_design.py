"""Finite-design counterexample: the Hájek audit ratio is not unbiased.

Exact enumeration of a two-unit independent Bernoulli audit design. These
are mathematical fixtures, not AI experiments. Execute only on a verified
zero-cost cloud runner, never on the user's laptop.
"""
from fractions import Fraction as F
from itertools import product
import unittest


def enumerate_design(labels, probabilities):
    if not labels or len(labels) != len(probabilities):
        raise ValueError("nonempty equal-length inputs required")
    if any(type(y) is not bool for y in labels):
        raise ValueError("truth labels must be boolean")
    if any(not isinstance(p, F) or not F(0) < p <= F(1)
           for p in probabilities):
        raise ValueError("strictly positive rational probabilities required")
    result = []
    for mask in product((False, True), repeat=len(labels)):
        mass = F(1)
        for selected, p in zip(mask, probabilities):
            mass *= p if selected else 1 - p
        if not mass:
            continue
        ht_total = sum((F(y, 1) / p for y, p, a
                        in zip(labels, probabilities, mask) if a), F(0))
        ht_count = sum((F(1) / p for p, a in
                        zip(probabilities, mask) if a), F(0))
        ratio = ht_total / ht_count if ht_count else None
        result.append((mass, ht_total, ht_count, ratio))
    return result


class FiniteDesignTests(unittest.TestCase):
    def test_ht_totals_are_design_unbiased(self):
        for labels in [(False, True), (True, True), (False, False)]:
            rows = enumerate_design(labels, [F(1, 2), F(1, 4)])
            self.assertEqual(sum((r[0] for r in rows), F(0)), F(1))
            self.assertEqual(sum((r[0]*r[1] for r in rows), F(0)),
                             sum(labels))
            self.assertEqual(sum((r[0]*r[2] for r in rows), F(0)), F(2))

    def test_ratio_can_be_undefined_and_conditionally_biased(self):
        rows = enumerate_design([True, False], [F(1, 2), F(1, 4)])
        empty = sum((mass for mass, _, _, ratio in rows
                     if ratio is None), F(0))
        self.assertEqual(empty, F(3, 8))
        observed = F(1) - empty
        conditional_mean = sum((mass*ratio for mass, _, _, ratio in rows
                                if ratio is not None), F(0)) / observed
        self.assertEqual(conditional_mean, F(3, 5))
        self.assertNotEqual(conditional_mean, F(1, 2))

    def test_census_collapses_to_population_mean(self):
        rows = enumerate_design([True, False, True],
                                [F(1), F(1), F(1)])
        self.assertEqual(rows, [(F(1), F(2), F(3), F(2, 3))])

    def test_invalid_designs_rejected(self):
        for labels, probs in [([], []), ([True], []),
                              ([1], [F(1, 2)]),
                              ([True], [F(0)]),
                              ([True], [F(3, 2)]),
                              ([True], [0.5])]:
            with self.assertRaises(ValueError):
                enumerate_design(labels, probs)


if __name__ == "__main__":
    unittest.main()
