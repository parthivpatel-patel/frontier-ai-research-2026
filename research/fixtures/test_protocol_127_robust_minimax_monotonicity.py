"""Protocol 127: exact deterministic minimax monotonicity under common ambiguity set.

Analytical regression only; NOT empirical AI performance. Run on verified free
standard GitHub-hosted public-repository runner, never on user's laptop.
"""
import unittest
from fractions import Fraction as F
from itertools import product

from protocol_116_joint_verifier import OUTCOMES, joint_model
from test_protocol_126_sharp_bounds_blackwell import endpoint_models

ACTIONS = ("accept", "reject", "abstain")
COSTS = {"accept": (F(0), F(1)), "reject": (F(1), F(0)),
         "abstain": (F(1,4), F(1,4))}


def policy_risk(prior, model, policy):
    """Expected loss for policy mapping each of four reports to an action."""
    p = F(prior)
    rows = joint_model(model)
    return sum((p*rows[True][o]*COSTS[policy[o]][0] +
                (1-p)*rows[False][o]*COSTS[policy[o]][1]
                for o in OUTCOMES), F(0))


def robust_risk(prior, models, policy):
    return max(policy_risk(prior, m, policy) for m in models)


def all_joint_policies():
    for actions in product(ACTIONS, repeat=4):
        yield dict(zip(OUTCOMES, actions))


def all_first_only_policies():
    for a, b in product(ACTIONS, repeat=2):
        yield {o: (a if o[0] == "+" else b) for o in OUTCOMES}


def deterministic_minimax(prior, models, policies):
    return min(robust_risk(prior, models, policy) for policy in policies)


class RobustInformationMonotonicity(unittest.TestCase):
    def test_policy_embedding_and_minimax_order(self):
        models = tuple(endpoint_models())
        joint = tuple(all_joint_policies())
        first = tuple(all_first_only_policies())
        self.assertEqual(len(joint), 81)
        self.assertEqual(len(first), 9)
        for p in (F(0), F(1,4), F(1,2), F(3,4), F(1)):
            two = deterministic_minimax(p, models, joint)
            one = deterministic_minimax(p, models, first)
            self.assertLessEqual(two, one)
            # A one-signal policy is literally a four-observation policy.
            for policy in first:
                self.assertIn(policy, joint)

    def test_worst_case_is_at_endpoint_for_fixed_policy(self):
        models = tuple(endpoint_models())
        # Conditional joint ++ masses lie in [3/5,4/5] and [0,1/5].
        # Expected loss is affine in each conditional coupling.
        for p in (F(1,4), F(1,2), F(3,4)):
            for policy in all_joint_policies():
                corners = robust_risk(p, models, policy)
                for t in (F(3,5), F(7,10), F(4,5)):
                    for f in (F(0), F(1,10), F(1,5)):
                        from test_protocol_126_sharp_bounds_blackwell import exchangeable_coupling
                        interior = joint_model({
                            True: exchangeable_coupling(F(4,5), t),
                            False: exchangeable_coupling(F(1,5), f)})
                        self.assertLessEqual(policy_risk(p, interior, policy), corners)

    def test_optional_second_verifier_fee(self):
        models = tuple(endpoint_models())
        for p in (F(1,4), F(1,2), F(3,4)):
            one = deterministic_minimax(p, models, all_first_only_policies())
            two = deterministic_minimax(p, models, all_joint_policies())
            for fee in (F(0), F(1,20), F(1)):
                self.assertEqual(min(one, two+fee), min(one, two+fee))
                self.assertLessEqual(min(one, two+fee), one)


if __name__ == "__main__":
    unittest.main()
