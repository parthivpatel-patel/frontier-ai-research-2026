"""Protocol 117: independent joint-verifier decision-plan enumeration.

Pure standard-library regression specification; no empirical evidence.
Run only on verified no-charge cloud infrastructure.
"""
import unittest
from fractions import Fraction as F
from itertools import product

from protocol_116_joint_verifier import (
    independent_model, duplicate_model, joint_model, expected_risk,
    first_only_risk, posterior,
)

ACTIONS = ("accept", "reject", "abstain")
OUTCOMES = ("++", "+-", "-+", "--")


def direct_loss(action, true_mass, false_mass):
    """Unnormalized joint expected loss; equal unit errors and 1/4 abstention."""
    if action == "accept":
        return false_mass
    if action == "reject":
        return true_mass
    return (true_mass + false_mass) * F(1, 4)


def enumerate_plans(prior, model, observe_second=True):
    """Explicitly enumerate all contingent policies, without Bayes-risk helpers.

    Full observation: 3**4 = 81 policies; first-only: 3**2 = 9.
    """
    rows = joint_model(model)
    groups = tuple(OUTCOMES) if observe_second else ("+", "-")
    masses = {}
    for group in groups:
        outcomes = (group,) if observe_second else tuple(
            o for o in OUTCOMES if o[0] == group
        )
        masses[group] = (
            prior * sum(rows[True][o] for o in outcomes),
            (1-prior) * sum(rows[False][o] for o in outcomes),
        )
    return min(
        sum((direct_loss(action, *masses[group])
             for group, action in zip(groups, policy)), F(0))
        for policy in product(ACTIONS, repeat=len(groups))
    )


def swapped(model):
    rows = joint_model(model)
    return joint_model({
        truth: {o: rows[truth][o[::-1]] for o in OUTCOMES}
        for truth in (True, False)
    })


class IndependentJointDecisionEnumeration(unittest.TestCase):
    def test_full_plan_agreement(self):
        for model in (
            independent_model(F(4, 5), F(4, 5)),
            duplicate_model(F(4, 5), F(4, 5)),
        ):
            for prior in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
                with self.subTest(prior=prior, model=model):
                    self.assertEqual(enumerate_plans(prior, model),
                                     expected_risk(prior, model))
                    self.assertEqual(enumerate_plans(prior, model, False),
                                     first_only_risk(prior, model))

    def test_second_observation_never_increases_optimal_risk(self):
        for model in (
            independent_model(F(4, 5), F(4, 5)),
            duplicate_model(F(4, 5), F(4, 5)),
        ):
            for prior in (F(1, 4), F(1, 2), F(3, 4)):
                self.assertLessEqual(enumerate_plans(prior, model),
                                     enumerate_plans(prior, model, False))

    def test_swapping_verifier_order_preserves_full_risk(self):
        asymmetric = joint_model({
            True: {"++": F(1, 2), "+-": F(1, 4),
                   "-+": F(1, 8), "--": F(1, 8)},
            False: {"++": F(1, 8), "+-": F(1, 8),
                    "-+": F(1, 4), "--": F(1, 2)},
        })
        for prior in (F(1, 4), F(1, 2), F(3, 4)):
            self.assertEqual(enumerate_plans(prior, asymmetric),
                             enumerate_plans(prior, swapped(asymmetric)))
            for outcome in OUTCOMES:
                self.assertEqual(posterior(prior, asymmetric, outcome),
                                 posterior(prior, swapped(asymmetric),
                                           outcome[::-1]))

    def test_no_extra_information_from_duplicate(self):
        model = duplicate_model(F(4, 5), F(4, 5))
        for prior in (F(1, 4), F(1, 2), F(3, 4)):
            self.assertEqual(enumerate_plans(prior, model),
                             enumerate_plans(prior, model, False))


if __name__ == "__main__":
    unittest.main()
