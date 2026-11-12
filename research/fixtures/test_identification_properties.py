"""Independent property checks for Protocol 050's exact identification interval.

Synthetic arithmetic only. Execute in verified zero-cost cloud CI, not on the
user's laptop. No external packages, downloads, or model calls.
"""
from fractions import Fraction as F
from itertools import product
from unittest import TestCase, main
from exact_dependence_checks import bounds_given_q, feasible_joint, posterior


class IdentificationProperties(TestCase):
    def test_exhaustive_small_grid(self):
        grid = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
        for pi in (F(1, 4), F(1, 2), F(3, 4)):
            for s1, s2, f1, f2 in product(grid, repeat=4):
                alo, ahi = feasible_joint(s1, s2)
                blo, bhi = feasible_joint(f1, f2)
                # Check all attainable endpoint combinations, including
                # degenerate and perfect-dependence cases.
                for a, b in product((alo, ahi), (blo, bhi)):
                    q = pi*a + (1-pi)*b
                    if q == 0:
                        continue
                    low, high = bounds_given_q(pi, s1, s2, f1, f2, q)
                    p = posterior(pi, a, b)
                    self.assertLessEqual(low, p)
                    self.assertLessEqual(p, high)
                    self.assertGreaterEqual(low, 0)
                    self.assertLessEqual(high, 1)
                    self.assertEqual(
                        (low, high),
                        bounds_given_q(pi, s2, s1, f2, f1, q),
                    )

    def test_impossible_high_joint_frequency(self):
        with self.assertRaises(ValueError):
            bounds_given_q(F(1, 2), F(1, 4), F(1, 4),
                           F(1, 4), F(1, 4), F(3, 4))

    def test_zero_prevalence_boundary_rejected(self):
        with self.assertRaises(ValueError):
            bounds_given_q(F(0), F(1, 2), F(1, 2),
                           F(1, 2), F(1, 2), F(1, 4))


if __name__ == "__main__":
    main()
