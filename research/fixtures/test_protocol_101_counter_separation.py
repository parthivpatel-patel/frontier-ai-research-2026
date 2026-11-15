"""Regression checks for Protocol 100 counter separation. Cloud execution only."""
import unittest
from fractions import Fraction as F
from protocol_099_bounded_certificate import bounded_certify
from test_protocol_093_complete_policy_trees import Intractable


class CounterSeparation(unittest.TestCase):
    def test_one_claim_two_policies_four_events(self):
        worlds = {(0,): F(1, 2), (1,): F(1, 2)}
        value, witness, count = bounded_certify(
            (1,), 1, worlds, max_trees=2, max_generator_events=4)
        self.assertEqual(value, F(1, 2))
        self.assertEqual(count, 2)

    def test_independent_generator_cap_refuses(self):
        worlds = {(0,): F(1, 2), (1,): F(1, 2)}
        with self.assertRaises(Intractable):
            bounded_certify((1,), 1, worlds, max_trees=2,
                            max_generator_events=3)

    def test_invalid_generator_cap(self):
        worlds = {(0,): F(1, 2), (1,): F(1, 2)}
        with self.assertRaises(ValueError):
            bounded_certify((1,), 1, worlds, max_generator_events=0)


if __name__ == "__main__":
    unittest.main()
