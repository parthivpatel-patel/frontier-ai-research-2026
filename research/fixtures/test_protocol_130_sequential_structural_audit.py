"""Protocol 130: independent structural audit of sequential acquisition.

Synthetic exact-rational checks, not empirical AI results.
Intended for verified zero-charge remote execution only.
"""
import unittest
from fractions import Fraction as F
from itertools import product
from test_protocol_129_sequential_acquisition import (
    POLICIES, NEVER, ALWAYS, CONDITIONAL, corners, joint, risk, minimax,
)

class Protocol130Tests(unittest.TestCase):
    def test_conditional_acquisition_probability_uses_first_marginal(self):
        # First signal positive has P(+)=0.5*0.8+0.5*0.2=0.5,
        # independent of coupling between first and second signals.
        acquire_if_first_positive = (0, 3)
        for c in corners():
            delta = risk(acquire_if_first_positive, c, fee=F(1)) - risk(
                acquire_if_first_positive, c, fee=F(0))
            self.assertEqual(delta, F(1, 2))
        acquire_if_first_negative = (3, 0)
        for c in corners():
            delta = risk(acquire_if_first_negative, c, fee=F(1)) - risk(
                acquire_if_first_negative, c, fee=F(0))
            self.assertEqual(delta, F(1, 2))

    def test_stop_decisions_cannot_use_unseen_second_signal(self):
        # In each stop choice, both possible second outcomes must
        # produce the same terminal decision; compare with direct sum.
        for policy in NEVER:
            for c in corners():
                direct = F(0)
                for truth, weight, positive, both in (
                    (1, F(1, 2), F(4, 5), c[0]),
                    (0, F(1, 2), F(1, 5), c[1]),
                ):
                    first_marginal = (1-positive, positive)
                    for first, probability in enumerate(first_marginal):
                        action = policy[first]
                        penalty = F(1, 4) if action == 2 else (
                            F(0) if action == truth else F(1))
                        direct += weight * probability * penalty
                self.assertEqual(risk(policy, c, fee=F(7)), direct)

    def test_coupling_affinity_at_midpoints(self):
        # For any policy, affine dependence implies midpoint risk
        # equals the mean of endpoint risks in each coordinate.
        lo1, hi1 = F(3, 5), F(4, 5)
        lo0, hi0 = F(0), F(1, 5)
        for policy in POLICIES:
            for other in (lo0, hi0):
                middle = ((lo1+hi1)/2, other)
                self.assertEqual(
                    2*risk(policy, middle, fee=F(1, 20)),
                    risk(policy, (lo1, other), fee=F(1, 20)) +
                    risk(policy, (hi1, other), fee=F(1, 20)))
            for other in (lo1, hi1):
                middle = (other, (lo0+hi0)/2)
                self.assertEqual(
                    2*risk(policy, middle, fee=F(1, 20)),
                    risk(policy, (other, lo0), fee=F(1, 20)) +
                    risk(policy, (other, hi0), fee=F(1, 20)))

    def test_nonnegative_fee_monotonicity(self):
        for cls in (POLICIES, NEVER, ALWAYS, CONDITIONAL):
            previous = None
            for fee in (F(0), F(1, 20), F(1, 4), F(1)):
                value = minimax(cls, fee=fee)
                if previous is not None:
                    self.assertGreaterEqual(value, previous)
                previous = value

    def test_relabel_second_verifier_does_not_change_always_optimum(self):
        # Under exchangeable marginals and the same joint law, the
        # two signal coordinates are symmetric. For always-acquire
        # policies the full risk must be invariant to swapping them.
        for p in ALWAYS:
            # map terminal decision table a(y1,y2) -> a(y2,y1)
            def table(choice):
                return ((choice-3)//3, (choice-3)%3)
            t0, t1 = table(p[0]), table(p[1])
            swapped = (3 + 3*t0[0] + t1[0],
                       3 + 3*t0[1] + t1[1])
            for c in corners():
                self.assertEqual(risk(p, c, fee=F(1, 20)),
                                 risk(swapped, c, fee=F(1, 20)))

if __name__ == "__main__":
    unittest.main()
