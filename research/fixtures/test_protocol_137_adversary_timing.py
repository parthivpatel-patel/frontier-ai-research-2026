"""Protocol 137: exact-rational adversary-timing regression.

Synthetic mathematical checks only; no empirical model-performance claims.
Execute on verified zero-charge cloud infrastructure, never on user's laptop.
"""
import unittest
from fractions import Fraction as F
from itertools import product

try:
    from test_protocol_132_heterogeneous_sequential import risk, corners, POLICIES
    from test_protocol_134_independent_adversarial_oracle import independent_risk, A1, B1, A0, B0
except ImportError:
    from research.fixtures.test_protocol_132_heterogeneous_sequential import risk, corners, POLICIES
    from research.fixtures.test_protocol_134_independent_adversarial_oracle import independent_risk, A1, B1, A0, B0


def mixed_corner_risks(mixture, corner_set):
    """Mixture is a sequence of (policy, nonnegative rational weight)."""
    if not mixture or sum((weight for _, weight in mixture), F(0)) != 1:
        raise ValueError("mixture weights must sum to one")
    if any(weight < 0 for _, weight in mixture):
        raise ValueError("negative mixture weight")
    return tuple(sum((weight * risk(policy, corner) for policy, weight in mixture), F(0))
                 for corner in corner_set)


def hidden_draw_value(mixture, corner_set):
    return max(mixed_corner_risks(mixture, corner_set))


def revealed_draw_value(mixture, corner_set):
    return sum((weight * max(risk(policy, corner) for corner in corner_set)
                for policy, weight in mixture), F(0))


class Protocol137Tests(unittest.TestCase):
    def test_mixture_matches_independent_oracle_at_four_corners(self):
        cc = tuple(corners(A1, B1, A0, B0))
        self.assertEqual(len(cc), 4)
        mixture = ((POLICIES[0], F(1, 3)), (POLICIES[17], F(1, 6)),
                   (POLICIES[83], F(1, 2)))
        for c, mixed in zip(cc, mixed_corner_risks(mixture, cc)):
            independently = sum((w * independent_risk(p, *c) for p, w in mixture), F(0))
            self.assertEqual(mixed, independently)

    def test_revealed_policy_never_better_for_selected_mixtures(self):
        cc = tuple(corners(A1, B1, A0, B0))
        for i, j in product((0, 7, 35, 83, 143), repeat=2):
            mixture = ((POLICIES[i], F(2, 5)), (POLICIES[j], F(3, 5)))
            self.assertLessEqual(hidden_draw_value(mixture, cc),
                                 revealed_draw_value(mixture, cc))

    def test_single_policy_timing_agrees(self):
        cc = tuple(corners(A1, B1, A0, B0))
        for p in POLICIES:
            mixture = ((p, F(1)),)
            self.assertEqual(hidden_draw_value(mixture, cc),
                             revealed_draw_value(mixture, cc))

    def test_strict_gap_toy_matrix(self):
        losses = ((F(0), F(1)), (F(1), F(0)))
        weights = (F(1, 2), F(1, 2))
        hidden = max(sum((weights[p] * losses[p][c] for p in range(2)), F(0))
                     for c in range(2))
        revealed = sum((weights[p] * max(losses[p]) for p in range(2)), F(0))
        self.assertEqual(hidden, F(1, 2))
        self.assertEqual(revealed, F(1))

    def test_reject_invalid_mixtures(self):
        cc = tuple(corners(A1, B1, A0, B0))
        with self.assertRaises(ValueError):
            mixed_corner_risks(((POLICIES[0], F(1, 2)),), cc)
        with self.assertRaises(ValueError):
            mixed_corner_risks(((POLICIES[0], F(2)), (POLICIES[1], F(-1))), cc)


if __name__ == "__main__":
    unittest.main()
