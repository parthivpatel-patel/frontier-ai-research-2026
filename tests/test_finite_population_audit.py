"""Finite-population paired verifier identities; stdlib-only, tiny CPU test.

No model inference, network, downloads, or laptop computation required.
Run on a verified free standard GitHub-hosted runner when authorized.
"""
from itertools import product
from fractions import Fraction
import unittest


def accepted_risk(accepted, errors):
    """Exact conditional error rate; undefined when nothing is accepted."""
    n = sum(accepted)
    return Fraction(sum(a * e for a, e in zip(accepted, errors)), n) if n else None


def exclusive_error_identity(a, b, errors):
    """Equal-coverage identity: R(A)-R(B) = (errors A-only - B-only)/k."""
    assert len(a) == len(b) == len(errors)
    k = sum(a)
    assert k > 0 and k == sum(b)
    exclusive_a = sum(e for x, y, e in zip(a, b, errors) if x and not y)
    exclusive_b = sum(e for x, y, e in zip(a, b, errors) if y and not x)
    return Fraction(exclusive_a - exclusive_b, k)


def hypergeom_zero_error_probability(N, K, n):
    """P(no errors in n uniformly sampled without replacement from N, K errors)."""
    from math import comb
    if not (0 <= K <= N and 0 <= n <= N):
        raise ValueError("invalid finite population")
    return Fraction(comb(N - K, n), comb(N, n)) if n <= N - K else Fraction(0)


class FinitePopulationAuditTests(unittest.TestCase):
    def test_paired_identity_exhaustive(self):
        for n in range(1, 6):
            masks = list(product((0, 1), repeat=n))
            for a in masks:
                for b in masks:
                    if sum(a) != sum(b) or not sum(a):
                        continue
                    for e in masks:
                        self.assertEqual(
                            accepted_risk(a, e) - accepted_risk(b, e),
                            exclusive_error_identity(a, b, e),
                        )

    def test_zero_error_hypergeometric_exhaustive(self):
        from itertools import combinations
        for N in range(1, 9):
            for K in range(N + 1):
                for n in range(N + 1):
                    total = 0
                    errors = set(range(K))
                    for sample in combinations(range(N), n):
                        total += not any(i in errors for i in sample)
                    from math import comb
                    self.assertEqual(
                        Fraction(total, comb(N, n)),
                        hypergeom_zero_error_probability(N, K, n),
                    )

    def test_boundary_cases(self):
        self.assertEqual(hypergeom_zero_error_probability(10, 0, 10), 1)
        self.assertEqual(hypergeom_zero_error_probability(10, 10, 1), 0)
        self.assertEqual(hypergeom_zero_error_probability(10, 5, 0), 1)
        self.assertIsNone(accepted_risk((0, 0), (1, 0)))


if __name__ == "__main__":
    unittest.main()
