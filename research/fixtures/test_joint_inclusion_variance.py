"""Exact finite-design checks for Protocol 058. No dependencies or model calls.

These are mathematical fixtures, not AI experimental results.
"""
from fractions import Fraction as F
from itertools import combinations
import unittest

ONE = F(1)

def moments(design, y=(1, 1)):
    """design: mapping of tuple of selected indices to exact probability."""
    n = len(y)
    assert sum(design.values(), F(0)) == ONE
    assert all(p >= 0 for p in design.values())
    assert all(len(set(s)) == len(s) and all(0 <= i < n for i in s) for s in design)
    pi = [sum((p for s, p in design.items() if i in s), F(0)) for i in range(n)]
    if any(p == 0 for p in pi):
        raise ValueError("nonpositive first-order inclusion probability")
    pair = [[sum((p for s, p in design.items() if i in s and j in s), F(0))
             for j in range(n)] for i in range(n)]
    ht = {s: sum((F(y[i], 1) / pi[i] for i in s), F(0)) for s in design}
    mean = sum((p * ht[s] for s, p in design.items()), F(0))
    direct = sum((p * (ht[s] - mean) ** 2 for s, p in design.items()), F(0))
    identity = sum(((pair[i][j] - pi[i] * pi[j]) * y[i] * y[j] / (pi[i] * pi[j])
                    for i in range(n) for j in range(n)), F(0))
    return mean, direct, identity, pi, pair

def plug_in_variance(selected, y, pi, pair):
    """Generic HT pairwise variance estimator; reject unidentified pair terms."""
    active = [i for i in selected if y[i] != 0]
    if any(pair[i][j] == 0 for i in active for j in active):
        raise ValueError("zero joint inclusion for observed nonzero pair")
    # A design with zero pair inclusion for two nonzero population units
    # cannot support a generic design-unbiased estimator across populations.
    if any(pair[i][j] == 0 for i in range(len(y)) for j in range(len(y))
           if y[i] != 0 and y[j] != 0):
        raise ValueError("generic unbiased variance estimator unavailable")
    return sum(((pair[i][j] - pi[i] * pi[j]) * y[i] * y[j]
                / (pair[i][j] * pi[i] * pi[j])
                for i in active for j in active), F(0))

class JointInclusionTests(unittest.TestCase):
    def test_three_designs(self):
        independent = {(): F(1,4), (0,): F(1,4), (1,): F(1,4), (0,1): F(1,4)}
        exactly_one = {(0,): F(1,2), (1,): F(1,2)}
        clustered = {(): F(1,2), (0,1): F(1,2)}
        for design, expected_var, expected_pair in [
            (independent, F(2), F(1,4)),
            (exactly_one, F(0), F(0)),
            (clustered, F(4), F(1,2)),
        ]:
            mean, direct, identity, pi, pair = moments(design)
            self.assertEqual(mean, 2)
            self.assertEqual(direct, expected_var)
            self.assertEqual(identity, expected_var)
            self.assertEqual(pi, [F(1,2), F(1,2)])
            self.assertEqual(pair[0][1], expected_pair)

    def test_nonconstant_truth_labels(self):
        d = {(): F(1,4), (0,): F(1,4), (1,): F(1,4), (0,1): F(1,4)}
        for labels in [(1,0), (0,1), (0,0), (1,1)]:
            mean, direct, identity, _, _ = moments(d, labels)
            self.assertEqual(mean, sum(labels))
            self.assertEqual(direct, identity)

    def test_zero_joint_inclusion_refusal(self):
        d = {(0,): F(1,2), (1,): F(1,2)}
        _, _, _, pi, pair = moments(d)
        with self.assertRaises(ValueError):
            plug_in_variance((0,), (1,1), pi, pair)

    def test_positive_joint_inclusion_estimator_expectation(self):
        d = {(): F(1,4), (0,): F(1,4), (1,): F(1,4), (0,1): F(1,4)}
        _, variance, _, pi, pair = moments(d)
        expected = sum((p * plug_in_variance(s, (1,1), pi, pair)
                        for s, p in d.items()), F(0))
        self.assertEqual(expected, variance)

    def test_invalid_design(self):
        with self.assertRaises(AssertionError):
            moments({(): F(1,3)})
        with self.assertRaises(ValueError):
            moments({(): F(1,2), (0,): F(1,2)})

if __name__ == "__main__":
    unittest.main()
