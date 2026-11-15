"""Protocol 102: metamorphic and adversarial checks for bounded certificates.

Standard library only. Do not execute on the user's laptop.
Run only in a verified zero-cost, process-limited cloud environment.
These are proposed tests, NOT reported passing results.
"""
import unittest
from fractions import Fraction as F
from itertools import product
from protocol_099_bounded_certificate import bounded_certify, score_witness
from protocol_098_structural_preflight import PreflightRefusal
from test_protocol_093_complete_policy_trees import STOP


def independent_worlds(probabilities):
    return {
        bits: _mass(bits, probabilities)
        for bits in product((0, 1), repeat=len(probabilities))
    }


def _mass(bits, probabilities):
    out = F(1)
    for bit, p in zip(bits, probabilities):
        out *= p if bit else 1 - p
    return out


class Protocol102(unittest.TestCase):
    def test_independent_two_claims_budget_one(self):
        worlds = independent_worlds((F(1, 4), F(3, 4)))
        value, witness, count = bounded_certify(
            (1, 1), 1, worlds, max_trees=3, max_generator_events=100)
        self.assertEqual(value, F(3, 4))
        self.assertEqual(count, 3)
        self.assertEqual(score_witness(witness, (1, 1), 1, worlds), value)

    def test_claim_permutation_invariance(self):
        original = independent_worlds((F(1, 4), F(3, 4)))
        swapped = {(bits[1], bits[0]): mass for bits, mass in original.items()}
        a = bounded_certify((1, 2), 2, original,
                            max_trees=10, max_generator_events=100)
        b = bounded_certify((2, 1), 2, swapped,
                            max_trees=10, max_generator_events=100)
        self.assertEqual(a[0], b[0])
        self.assertEqual(a[2], b[2])

    def test_zero_budget_only_stop(self):
        worlds = independent_worlds((F(1, 2), F(1, 2)))
        value, witness, count = bounded_certify(
            (1, 1), 0, worlds, max_trees=1, max_generator_events=10)
        self.assertEqual((value, witness, count), (F(0), STOP, 1))

    def test_branch_swap_changes_witness_reward(self):
        worlds = {(0, 0): F(1, 2), (0, 1): F(0),
                  (1, 0): F(0), (1, 1): F(1, 2)}
        good = (0, STOP, (1, STOP, STOP))
        corrupted = (0, (1, STOP, STOP), STOP)
        self.assertEqual(score_witness(good, (1, 1), 2, worlds), F(3, 2))
        self.assertEqual(score_witness(corrupted, (1, 1), 2, worlds), F(1))

    def test_illegal_repeated_claim_is_rejected(self):
        worlds = independent_worlds((F(1, 2),))
        with self.assertRaises(ValueError):
            score_witness((0, (0, STOP, STOP), STOP),
                          (1,), 2, worlds)

    def test_preflight_refusal_is_not_certificate(self):
        worlds = independent_worlds((F(1, 2), F(1, 2)))
        with self.assertRaises(PreflightRefusal):
            bounded_certify((1, 1), 1, worlds,
                            max_trees=2, max_generator_events=100)


if __name__ == "__main__":
    unittest.main()
