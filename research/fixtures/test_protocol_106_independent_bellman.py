"""Protocol 106 oracle hand-checkable fixtures. Run on verified free cloud only."""
import unittest
from fractions import Fraction as F
from protocol_106_independent_bellman import optimal_value, Refused


class BellmanOracleTests(unittest.TestCase):
    def test_single_fair_claim(self):
        self.assertEqual(optimal_value((1,), 1, {(0,): F(1, 2), (1,): F(1, 2)}), F(1, 2))

    def test_correlated_pair(self):
        prior = {(0, 0): F(1, 2), (1, 1): F(1, 2)}
        self.assertEqual(optimal_value((1, 1), 2, prior), F(3, 2))

    def test_independent_pair(self):
        prior = {(a, b): F(1, 4) for a in (0, 1) for b in (0, 1)}
        self.assertEqual(optimal_value((1, 1), 2, prior), F(1))

    def test_zero_budget(self):
        self.assertEqual(optimal_value((1,), 0, {(0,): F(1, 2), (1,): F(1, 2)}), F(0))

    def test_permutation(self):
        prior = {(0, 0): F(1, 3), (1, 0): F(2, 3)}
        permuted = {(b, a): p for (a, b), p in prior.items()}
        self.assertEqual(optimal_value((1, 2), 2, prior),
                         optimal_value((2, 1), 2, permuted))

    def test_reject_float_and_unnormalized(self):
        with self.assertRaises(ValueError):
            optimal_value((1,), 1, {(0,): 0.5, (1,): 0.5})
        with self.assertRaises(ValueError):
            optimal_value((1,), 1, {(0,): F(1, 4), (1,): F(1, 4)})

    def test_state_cap_refusal(self):
        with self.assertRaises(Refused):
            optimal_value((1,), 1, {(0,): F(1, 2), (1,): F(1, 2)}, max_states=1)


if __name__ == "__main__":
    unittest.main()
