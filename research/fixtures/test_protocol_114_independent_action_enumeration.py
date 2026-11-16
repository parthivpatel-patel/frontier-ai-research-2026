"""Protocol 114: independent action-enumeration checks for Protocol 113.

Specifications only; not evidence of passing tests. Run in verified free cloud CI.
The reference calculation deliberately does not import decision_loss or reuse
Protocol 113's risk-minimization implementation.
"""
import itertools
import unittest
from fractions import Fraction as F
from protocol_113_exact_noisy_decision import evaluate

ACTIONS = ("accept", "reject", "abstain")

def loss(action, truth, fa, fr, ab):
    if action == "accept":
        return F(0) if truth else fa
    if action == "reject":
        return fr if truth else F(0)
    return ab

def independent_optimum(prior, sensitivity, specificity, cost, fa, fr, ab):
    """Enumerate all 3 no-test actions and 3^2 observation-contingent plans."""
    p, se, sp, c = map(F, (prior, sensitivity, specificity, cost))
    fa, fr, ab = map(F, (fa, fr, ab))
    def risk(a):
        return p * loss(a, True, fa, fr, ab) + (1-p) * loss(a, False, fa, fr, ab)
    stop = min(risk(a) for a in ACTIONS)
    def plan_risk(positive, negative):
        total = c
        for truth, prob in ((True, p), (False, 1-p)):
            for observation, likelihood in (
                (True, se if truth else 1-sp),
                (False, 1-se if truth else sp),
            ):
                action = positive if observation else negative
                total += prob * likelihood * loss(action, truth, fa, fr, ab)
        return total
    test = min(plan_risk(pos, neg) for pos, neg in itertools.product(ACTIONS, repeat=2))
    return stop, test

class IndependentEnumerationTests(unittest.TestCase):
    def check_case(self, p, se, sp, cost, fa, fr, ab):
        stop, test = independent_optimum(p, se, sp, cost, fa, fr, ab)
        observed = evaluate(p, se, sp, cost,
                            false_accept=fa, false_reject=fr, abstain=ab)
        self.assertEqual(observed["prior_risk"], stop)
        self.assertEqual(observed["posterior_risk"] + F(cost), test)
        self.assertEqual(observed["gross_value"], stop - (test - F(cost)))
        self.assertEqual(observed["buy_test"], test < stop)

    def test_protocol_112_fixture(self):
        self.check_case(F(1,2), F(4,5), F(4,5), F(1,10), 1, 1, F(1,4))

    def test_asymmetric_costs_and_abstention(self):
        self.check_case(F(2,5), F(3,4), F(2,3), F(1,20), 4, 1, F(2,5))

    def test_degenerate_prior_and_observation(self):
        self.check_case(1, 1, 0, 0, 2, 3, F(1,4))
        self.check_case(0, 0, 1, F(1,10), 2, 3, F(1,4))

    def test_bounded_rational_grid(self):
        for p, se, sp in itertools.product((F(0), F(1,2), F(1)),
                                           (F(0), F(1,2), F(1)),
                                           (F(0), F(1,2), F(1))):
            self.check_case(p, se, sp, F(1,10), 2, 1, F(1,3))

if __name__ == "__main__":
    unittest.main()
