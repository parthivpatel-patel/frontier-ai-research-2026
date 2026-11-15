"""Protocol 107: independent Bellman-versus-complete-policy cross-oracle checks.

Standard-library-only. NOT executed at publication. Execute on a verified
free standard public-repository cloud runner with external time/memory limits.
No model downloads, paid services, or laptop execution.
"""
import unittest
from fractions import Fraction as F
from itertools import product

from protocol_106_independent_bellman import optimal_value
from test_protocol_093_complete_policy_trees import certify
from protocol_099_bounded_certificate import score_witness


def full_table(n, weights):
    outcomes = tuple(product((0, 1), repeat=n))
    assert len(outcomes) == len(weights)
    assert all(type(w) is int and w >= 0 for w in weights)
    total = sum(weights)
    assert total > 0
    return {outcome: F(weight, total) for outcome, weight in zip(outcomes, weights)}


class CrossOracleTests(unittest.TestCase):
    def compare(self, costs, budget, worlds):
        bellman = optimal_value(costs, budget, worlds, max_states=20000)
        enumerated, witness, count = certify(costs, budget, worlds, cap=100000)
        self.assertEqual(bellman, enumerated)
        self.assertEqual(score_witness(witness, costs, budget, worlds), bellman)
        self.assertGreaterEqual(count, 1)

    def test_one_claim_extreme_and_fractional(self):
        for weights in ((1, 0), (0, 1), (1, 1), (3, 1)):
            for budget in (0, 1, 2):
                with self.subTest(weights=weights, budget=budget):
                    self.compare((1,), budget, full_table(1, weights))

    def test_two_claim_joint_distributions(self):
        distributions = (
            (1, 1, 1, 1),  # independent
            (1, 0, 0, 1),  # perfectly correlated
            (0, 1, 1, 0),  # anticorrelated
            (1, 2, 3, 4),  # asymmetric
            (0, 0, 0, 1),  # deterministic
        )
        for weights in distributions:
            worlds = full_table(2, weights)
            for costs in ((1, 1), (1, 2), (2, 1)):
                for budget in (0, 1, 2):
                    with self.subTest(weights=weights, costs=costs, budget=budget):
                        self.compare(costs, budget, worlds)

    def test_three_claim_sparse_correlated(self):
        # Full table required by enumerator; zero-mass worlds are legitimate.
        worlds = full_table(3, (1, 0, 0, 0, 0, 0, 0, 1))
        self.compare((1, 1, 1), 2, worlds)

    def test_suboptimal_legal_stop_witness(self):
        worlds = full_table(1, (1, 1))
        stop = ("stop",)
        self.assertEqual(score_witness(stop, (1,), 1, worlds), F(0))
        self.assertLess(score_witness(stop, (1,), 1, worlds),
                        optimal_value((1,), 1, worlds))


if __name__ == "__main__":
    unittest.main()
