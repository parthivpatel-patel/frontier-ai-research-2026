"""Protocol 060: exact complete-design witness checks.

A feasible witness is a probability distribution over all subsets, not merely
a matrix satisfying pairwise Frechet bounds. Standard-library only.
These are specification tests, not AI performance measurements.
"""
from fractions import Fraction as F
from itertools import combinations
import unittest


def moments_from_witness(n, masses):
    """Return exact first/second inclusion moments from a complete witness."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")
    if not isinstance(masses, dict) or not masses:
        raise ValueError("nonempty probability dictionary required")
    total = F(0)
    normalized = {}
    for subset, mass in masses.items():
        if not isinstance(subset, (tuple, frozenset)):
            raise ValueError("subsets must be tuples or frozensets")
        if not isinstance(mass, F) or mass < 0:
            raise ValueError("masses must be nonnegative exact fractions")
        if any(not isinstance(i, int) or isinstance(i, bool) or i < 0 or i >= n for i in subset):
            raise ValueError("invalid index")
        s = frozenset(subset)
        if len(s) != len(subset) or s in normalized:
            raise ValueError("duplicate subset")
        normalized[s] = mass
        total += mass
    if total != 1:
        raise ValueError("witness masses must sum to one")
    pi = [sum((mass for s, mass in normalized.items() if i in s), F(0))
          for i in range(n)]
    pair = [[sum((mass for s, mass in normalized.items() if i in s and j in s), F(0))
             for j in range(n)] for i in range(n)]
    return pi, pair


def certify_moments(pi, pair, witness):
    """Certify a supplied complete design; does not search for a witness."""
    n = len(pi)
    a, b = moments_from_witness(n, witness)
    if a != pi or b != pair:
        raise ValueError("witness does not match requested moments")
    return True


def triangle_necessary(pi, pair):
    """Necessary three-event union inequality; not a sufficiency test."""
    n = len(pi)
    if len(pair) != n or any(len(row) != n for row in pair):
        raise ValueError("invalid matrix")
    for i, j, k in combinations(range(n), 3):
        # 1_{A_i}+1_{A_j}+1_{A_k}
        # <= 1 + 1_{A_i A_j}+1_{A_i A_k}+1_{A_j A_k}
        if pi[i] + pi[j] + pi[k] > 1 + pair[i][j] + pair[i][k] + pair[j][k]:
            return False
    return True


class CompleteDesignWitnessTests(unittest.TestCase):
    def test_independent_three_unit_design(self):
        witness = {tuple(i for i in range(3) if mask & (1 << i)): F(1, 8)
                   for mask in range(8)}
        pi, pair = moments_from_witness(3, witness)
        self.assertEqual(pi, [F(1, 2)] * 3)
        self.assertEqual(pair[0][1], F(1, 4))
        self.assertTrue(certify_moments(pi, pair, witness))
        self.assertTrue(triangle_necessary(pi, pair))

    def test_impossible_mutually_exclusive_triplet(self):
        pi = [F(1, 2)] * 3
        pair = [[F(1, 2) if i == j else F(0) for j in range(3)]
                for i in range(3)]
        self.assertFalse(triangle_necessary(pi, pair))
        # A supplied valid design cannot match the impossible moments.
        witness = {(): F(1, 2), (0, 1, 2): F(1, 2)}
        with self.assertRaises(ValueError):
            certify_moments(pi, pair, witness)

    def test_clustered_three_unit_design(self):
        witness = {(): F(1, 2), (0, 1, 2): F(1, 2)}
        pi, pair = moments_from_witness(3, witness)
        self.assertEqual(pair[0][2], F(1, 2))
        self.assertTrue(certify_moments(pi, pair, witness))

    def test_invalid_witness(self):
        for witness in [
            {(): F(1, 3)}, {(): F(1, 2), (0,): F(-1, 2)},
            {(0, 0): F(1)}, {(3,): F(1)}, {(): 1},
        ]:
            with self.assertRaises(ValueError):
                moments_from_witness(3, witness)

    def test_mismatched_claimed_matrix(self):
        witness = {(): F(1, 2), (0,): F(1, 2)}
        pi, pair = moments_from_witness(2, witness)
        pi[0] = F(3, 4)
        with self.assertRaises(ValueError):
            certify_moments(pi, pair, witness)


if __name__ == "__main__":
    unittest.main()
