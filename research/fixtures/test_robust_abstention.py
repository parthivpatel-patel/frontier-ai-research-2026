"""Exact-rational checks for Protocol 052; not an empirical AI evaluation.

Run only on verified zero-cost cloud compute:
    python -m unittest research/fixtures/test_robust_abstention.py
"""
from fractions import Fraction as F
import unittest


def worst_case_risks(lower, upper, false_accept, false_reject, abstain):
    """Return robust risks for accept, reject, abstain in that order."""
    vals = (lower, upper, false_accept, false_reject, abstain)
    if any(not isinstance(x, F) for x in vals):
        raise TypeError("Inputs must be fractions.Fraction for exact arithmetic")
    if not F(0) <= lower <= upper <= F(1):
        raise ValueError("Invalid identified probability interval")
    if false_accept <= 0 or false_reject <= 0 or abstain < 0:
        raise ValueError("Invalid costs")
    return (false_accept * (1 - lower), false_reject * upper, abstain)


def choose_action(lower, upper, false_accept, false_reject, abstain):
    risks = worst_case_risks(lower, upper, false_accept, false_reject, abstain)
    smallest = min(risks)
    # Precommitted tie rule: abstain when tied; otherwise accept before reject.
    for index in (2, 0, 1):
        if risks[index] == smallest:
            return ("accept", "reject", "abstain")[index]
    raise AssertionError("unreachable")


class RobustAbstentionTests(unittest.TestCase):
    def test_protocol_example(self):
        args = (F(3, 4), F(1), F(4), F(1), F(1, 5))
        self.assertEqual(worst_case_risks(*args), (F(1), F(1), F(1, 5)))
        self.assertEqual(choose_action(*args), "abstain")

    def test_tie_policy(self):
        self.assertEqual(choose_action(F(3, 4), F(1), F(4), F(1), F(1)), "abstain")
        self.assertEqual(choose_action(F(3, 4), F(1), F(4), F(1), F(2)), "accept")

    def test_boundary_intervals(self):
        self.assertEqual(worst_case_risks(F(0), F(1), F(2), F(3), F(1)), (F(2), F(3), F(1)))
        self.assertEqual(worst_case_risks(F(1), F(1), F(2), F(3), F(1)), (F(0), F(3), F(1)))
        self.assertEqual(choose_action(F(1), F(1), F(2), F(3), F(1)), "accept")
        self.assertEqual(choose_action(F(0), F(0), F(2), F(3), F(1)), "reject")

    def test_monotonicity_and_bruteforce_endpoints(self):
        grid = [F(i, 4) for i in range(5)]
        for lower in grid:
            for upper in grid:
                if lower > upper:
                    continue
                costs = (F(3, 2), F(5, 3), F(1, 4))
                observed = worst_case_risks(lower, upper, *costs)
                sample = [lower + (upper - lower) * F(k, 8) for k in range(9)]
                self.assertEqual(observed[0], max(costs[0] * (1 - p) for p in sample))
                self.assertEqual(observed[1], max(costs[1] * p for p in sample))
                self.assertEqual(observed[2], costs[2])

    def test_reject_invalid_inputs(self):
        invalid = [
            (F(-1, 4), F(1), F(1), F(1), F(0)),
            (F(3, 4), F(1, 2), F(1), F(1), F(0)),
            (F(0), F(1), F(0), F(1), F(0)),
            (F(0), F(1), F(1), F(1), F(-1)),
        ]
        for args in invalid:
            with self.assertRaises(ValueError):
                worst_case_risks(*args)
        with self.assertRaises(TypeError):
            worst_case_risks(0.0, F(1), F(1), F(1), F(0))


if __name__ == "__main__":
    unittest.main()
