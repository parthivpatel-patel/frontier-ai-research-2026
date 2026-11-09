"""Protocol 161: deterministic numerical-stability regression fixtures.

Execute only in cloud CI after verifying free quota and billing safeguards:
python -m unittest tests.test_protocol_161_exact_tail_stability
"""
import math
import unittest

from tests.test_protocol_159_paired_discordance_contract import (
    exact_two_sided_binomial_p,
    paired_oracle,
)


class ExactTailStability(unittest.TestCase):
    def test_no_discordance(self):
        self.assertEqual(exact_two_sided_binomial_p(0, 0), 1.0)

    def test_small_exact_reference(self):
        self.assertAlmostEqual(exact_two_sided_binomial_p(6, 0), 0.03125, places=14)
        self.assertAlmostEqual(exact_two_sided_binomial_p(7, 2), 0.453125, places=14)

    def test_large_extreme_and_balanced(self):
        for minority in (0, 1, 100, 999, 1000):
            p = exact_two_sided_binomial_p(2000, minority)
            self.assertTrue(math.isfinite(p))
            self.assertTrue(0.0 <= p <= 1.0)
        self.assertEqual(exact_two_sided_binomial_p(2000, 1000), 1.0)

    def test_symmetry_under_swapping_systems(self):
        a = {i: (True, i < 13) for i in range(20)}
        b = {i: (True, i >= 13) for i in range(20)}
        self.assertAlmostEqual(
            paired_oracle(a, b)["p_independent_pairs"],
            paired_oracle(b, a)["p_independent_pairs"],
        )

    def test_cell_accounting(self):
        a = {i: (True, i % 3 == 0) for i in range(60)}
        b = {i: (True, i % 4 == 0) for i in range(60)}
        result = paired_oracle(a, b)
        self.assertEqual(sum(result[k] for k in ("n11", "n10", "n01", "n00")), 60)
        self.assertAlmostEqual(result["delta_yield"], (result["n10"] - result["n01"]) / 60)

    def test_invalid_counts(self):
        for n, m in ((-1, 0), (5, -1), (5, 3), (True, 0), (5, 1.0)):
            with self.subTest(n=n, m=m), self.assertRaises(ValueError):
                exact_two_sided_binomial_p(n, m)


if __name__ == "__main__":
    unittest.main()
