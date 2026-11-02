"""Exact-arithmetic tests for a second, independent toy physical family."""
import itertools
import unittest
from fractions import Fraction

from src.exact_domain_audit import Interval, Q
from src.damped_domain_audit import (
    DampedDomain, counterexample, disagreement_witness, exact_reachable,
    position_after_two_steps, threshold_disagreement,
)


def I(a, b):
    return Interval(Q(a), Q(b))


def wide():
    return DampedDomain(I("1/2", "1/2"), I(0, 0),
                        I(0, "1/3"), I(0, 0), Q("1/2"))


class DampedDomainTests(unittest.TestCase):
    def test_reachable_exactly_matches_target_interval(self):
        self.assertEqual(exact_reachable(wide()), I("1/2", 1))

    def test_dynamics_by_direct_recursion(self):
        d = wide()
        self.assertEqual(position_after_two_steps(
            d, Q("1/2"), Q(0), Q("1/3"), Q(0)), Q(1))

    def test_reachable_bounds_match_all_sixteen_corners(self):
        d = DampedDomain(I(0, 1), I("-1/2", "1/2"),
                         I("-1/4", "1/4"), I("-1/3", "1/3"), Q("3/4"))
        values = [position_after_two_steps(d, *coords) for coords in
                  itertools.product(*[(axis.low, axis.high) for axis in d.axes])]
        self.assertEqual(exact_reachable(d), Interval(min(values), max(values)))

    def test_constructed_violation_is_valid(self):
        d = wide()
        witness = counterexample(d, Q("4/5"))
        self.assertIsNotNone(witness)
        self.assertEqual(position_after_two_steps(d, *witness), Q(1))

    def test_nonviolating_threshold(self):
        self.assertIsNone(counterexample(wide(), Q(1)))

    def test_semantic_disagreement_has_exact_witness(self):
        d = wide()
        witness = disagreement_witness(d, Q("4/5"), Q("9/10"))
        self.assertIsNotNone(witness)
        y = position_after_two_steps(d, *witness)
        self.assertEqual(y, Q("9/10"))
        self.assertFalse(y <= Q("4/5"))
        self.assertTrue(y <= Q("9/10"))

    def test_negative_control_on_restricted_domain(self):
        d = DampedDomain(I("1/2", "1/2"), I(0, 0),
                         I(0, "1/6"), I(0, 0), Q("1/2"))
        self.assertEqual(exact_reachable(d), I("1/2", "3/4"))
        self.assertFalse(threshold_disagreement(d, Q("4/5"), Q("9/10")))
        self.assertIsNone(disagreement_witness(d, Q("4/5"), Q("9/10")))

    def test_equal_thresholds_and_below_domain(self):
        self.assertFalse(threshold_disagreement(wide(), Q("4/5"), Q("4/5")))
        self.assertFalse(threshold_disagreement(wide(), Q(0), Q("1/4")))
        self.assertIsNone(disagreement_witness(wide(), Q(0), Q("1/4")))

    def test_singleton_range_endpoint(self):
        d = DampedDomain(I(1, 1), I(0, 0), I(0, 0), I(0, 0), Q(0))
        witness = disagreement_witness(d, Q("9/10"), Q(1))
        self.assertEqual(position_after_two_steps(d, *witness), Q(1))

    def test_invalid_damping_rejected(self):
        for rho in (Q("-1/10"), Q("11/10"), 0.5):
            with self.subTest(rho=rho), self.assertRaises(ValueError):
                DampedDomain(I(0, 0), I(0, 0), I(0, 0), I(0, 0), rho)

    def test_out_of_domain_and_inexact_trajectory_rejected(self):
        with self.assertRaises(ValueError):
            position_after_two_steps(wide(), Q(0), Q(0), Q(0), Q(0))
        with self.assertRaises(TypeError):
            position_after_two_steps(wide(), 0.5, Q(0), Q(0), Q(0))


if __name__ == "__main__":
    unittest.main()
