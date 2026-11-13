"""Protocol 059: design-only admissibility checks (exact rational arithmetic).

No truth labels are read by the validator. This is a specification fixture,
not evidence of empirical AI performance or of valid confidence intervals.
"""
from fractions import Fraction as F
import unittest


def validate_joint_inclusion(pi, pair, require_unbiased_variance=False):
    """Validate first/second-order inclusion probabilities before label access.

    This checks necessary consistency conditions, not realizability of the
    supplied matrix as a complete probability distribution on subsets.
    """
    n = len(pi)
    if n == 0 or len(pair) != n or any(len(row) != n for row in pair):
        raise ValueError("nonempty square inclusion matrix required")
    if any(not isinstance(p, F) or p <= 0 or p > 1 for p in pi):
        raise ValueError("first-order probabilities must be exact fractions in (0,1]")
    for i in range(n):
        if pair[i][i] != pi[i]:
            raise ValueError("diagonal must equal first-order inclusion")
        for j in range(n):
            q = pair[i][j]
            if not isinstance(q, F) or q != pair[j][i]:
                raise ValueError("joint inclusion must be exact and symmetric")
            if q < max(F(0), pi[i] + pi[j] - 1) or q > min(pi[i], pi[j]):
                raise ValueError("joint inclusion violates Frechet bounds")
            if i != j and require_unbiased_variance and q == 0:
                raise ValueError("generic unbiased pairwise variance unavailable")
    return True


def design_probabilities(design, n):
    """Construct exact inclusion probabilities from a full sampling design."""
    if n < 1 or not design or sum(design.values(), F(0)) != 1:
        raise ValueError("invalid complete design")
    if any(not isinstance(p, F) or p < 0 for p in design.values()):
        raise ValueError("design weights must be nonnegative fractions")
    if any(len(set(s)) != len(s) or any(i not in range(n) for i in s)
           for s in design):
        raise ValueError("invalid selected indices")
    pi = [sum((p for s, p in design.items() if i in s), F(0))
          for i in range(n)]
    pair = [[sum((p for s, p in design.items() if i in s and j in s), F(0))
             for j in range(n)] for i in range(n)]
    return pi, pair


class DesignOnlyGateTests(unittest.TestCase):
    def test_zero_pair_rejected_independent_of_truth(self):
        design = {(0,): F(1, 2), (1,): F(1, 2)}
        pi, pair = design_probabilities(design, 2)
        self.assertTrue(validate_joint_inclusion(pi, pair))
        with self.assertRaises(ValueError):
            validate_joint_inclusion(pi, pair, require_unbiased_variance=True)

    def test_independent_and_clustered_pass(self):
        for design in [
            {(): F(1, 4), (0,): F(1, 4), (1,): F(1, 4), (0, 1): F(1, 4)},
            {(): F(1, 2), (0, 1): F(1, 2)},
        ]:
            pi, pair = design_probabilities(design, 2)
            self.assertTrue(validate_joint_inclusion(pi, pair, True))

    def test_marginal_positivity_is_not_pair_positivity(self):
        pi, pair = design_probabilities({(0,): F(1, 2), (1,): F(1, 2)}, 2)
        self.assertEqual(pi, [F(1, 2), F(1, 2)])
        self.assertEqual(pair[0][1], 0)

    def test_invalid_matrix_and_bounds(self):
        with self.assertRaises(ValueError):
            validate_joint_inclusion([F(1, 2)], [])
        with self.assertRaises(ValueError):
            validate_joint_inclusion([F(0)], [[F(0)]])
        with self.assertRaises(ValueError):
            validate_joint_inclusion([F(1, 2), F(1, 2)],
                                     [[F(1, 2), F(3, 4)], [F(3, 4), F(1, 2)]])
        with self.assertRaises(ValueError):
            validate_joint_inclusion([F(1, 2), F(1, 2)],
                                     [[F(1, 2), F(1, 4)], [F(0), F(1, 2)]])
        with self.assertRaises(ValueError):
            validate_joint_inclusion([F(1, 2)], [[0.5]])

    def test_higher_order_consistency_not_certified(self):
        # Pairwise Frechet conditions are necessary, not sufficient.
        # Three events each with P=1/2 cannot all be mutually exclusive:
        # their union would have probability 3/2.
        pi = [F(1, 2)] * 3
        pair = [[pi[i] if i == j else F(0) for j in range(3)]
                for i in range(3)]
        self.assertTrue(validate_joint_inclusion(pi, pair))
        # Do not interpret True as a realizability certificate.


if __name__ == "__main__":
    unittest.main()
