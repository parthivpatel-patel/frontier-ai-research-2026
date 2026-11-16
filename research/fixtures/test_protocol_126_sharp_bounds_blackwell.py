"""Protocol 126: sharp Frechet posterior bounds and Blackwell negative controls.

Exact-rational analytical tests, not empirical AI results.
Execute remotely only after the zero-cost GitHub Actions gate is verified.
"""
import unittest
from fractions import Fraction as F
from itertools import product

from protocol_116_joint_verifier import (
    joint_model, posterior, marginals, expected_risk, first_only_risk,
    independent_model, duplicate_model,
)

Q_TRUE = F(4, 5)
Q_FALSE = F(1, 5)
PRIOR = F(1, 2)


def exchangeable_coupling(positive_marginal, joint_positive):
    q, c = F(positive_marginal), F(joint_positive)
    if not max(F(0), 2*q-1) <= c <= q:
        raise ValueError("outside sharp Frechet interval")
    return {"++": c, "+-": q-c, "-+": q-c, "--": 1-2*q+c}


def endpoint_models():
    # Conditional coupling endpoints can vary independently across truth states.
    for t, f in product((F(3, 5), F(4, 5)), (F(0), F(1, 5))):
        yield joint_model({
            True: exchangeable_coupling(Q_TRUE, t),
            False: exchangeable_coupling(Q_FALSE, f),
        })


class SharpBoundsAndInformationMonotonicity(unittest.TestCase):
    def test_endpoint_marginals(self):
        for model in endpoint_models():
            for truth, q in ((True, Q_TRUE), (False, Q_FALSE)):
                for idx in (0, 1):
                    self.assertEqual(marginals(model, truth, idx), q)

    def test_sharp_posterior_range(self):
        values = [posterior(PRIOR, m, "++") for m in endpoint_models()]
        self.assertEqual(min(values), F(3, 4))
        self.assertEqual(max(values), F(1))
        self.assertEqual(posterior(PRIOR, independent_model(Q_TRUE, Q_TRUE), "++"), F(16, 17))

    def test_information_cannot_increase_optimal_gross_risk(self):
        for model in (*tuple(endpoint_models()), independent_model(Q_TRUE, Q_TRUE),
                      duplicate_model(Q_TRUE, Q_TRUE)):
            for p in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
                self.assertLessEqual(expected_risk(p, model), first_only_risk(p, model))

    def test_exact_duplicate_adds_no_gross_value(self):
        model = duplicate_model(Q_TRUE, Q_TRUE)
        for p in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
            self.assertEqual(expected_risk(p, model), first_only_risk(p, model))
        self.assertIsNone(posterior(PRIOR, model, "+-"))

    def test_positive_incremental_fee_can_be_avoided(self):
        # Optional acquisition: skip second verifier, or pay fee for both.
        fee = F(1, 20)
        for model in endpoint_models():
            for p in (F(1, 4), F(1, 2), F(3, 4)):
                optional = min(first_only_risk(p, model), expected_risk(p, model) + fee)
                self.assertLessEqual(optional, first_only_risk(p, model))

    def test_reject_infeasible_frechet_couplings(self):
        for q, c in ((F(4, 5), F(1, 2)), (F(1, 5), F(1, 4))):
            with self.assertRaises(ValueError):
                exchangeable_coupling(q, c)


if __name__ == "__main__":
    unittest.main()
