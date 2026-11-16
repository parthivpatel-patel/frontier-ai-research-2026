"""Protocol 119: exact fixed-marginal dependence stress tests.

Analytical regression specification, not empirical model evidence.
Standard library only. Execute only on verified zero-cost cloud runners.
"""
import unittest
from fractions import Fraction as F

from protocol_116_joint_verifier import (
    joint_model, independent_model, duplicate_model, posterior,
    marginals, expected_risk, first_only_risk,
)
from test_protocol_117_independent_joint_decision_enumeration import (
    enumerate_plans, swapped,
)

GRID = (F(0), F(1, 5), F(1, 2), F(1))


def coupled_model(lam):
    """Exchangeable Frechet-feasible coupling with fixed 4/5 accuracy."""
    if not isinstance(lam, F) or not F(0) <= lam <= F(1):
        raise ValueError("lambda must be a Fraction in [0,1]")
    rows = {}
    for truth, q, c in (
        (True, F(4, 5), F(3, 5) + lam / 5),
        (False, F(1, 5), lam / 5),
    ):
        rows[truth] = {
            "++": c, "+-": q-c, "-+": q-c, "--": 1-2*q+c
        }
    return joint_model(rows)


class FixedMarginalDependence(unittest.TestCase):
    def test_normalization_and_fixed_marginals(self):
        for lam in GRID:
            model = coupled_model(lam)
            for truth, q in ((True, F(4, 5)), (False, F(1, 5))):
                self.assertEqual(sum(model[truth].values()), 1)
                self.assertTrue(all(v >= 0 for v in model[truth].values()))
                for idx in (0, 1):
                    self.assertEqual(marginals(model, truth, idx), q)

    def test_independence_and_duplicate_endpoints(self):
        self.assertEqual(coupled_model(F(1, 5)),
                         independent_model(F(4, 5), F(4, 5)))
        self.assertEqual(coupled_model(F(1)),
                         duplicate_model(F(4, 5), F(4, 5)))

    def test_posterior_identifiability_counterexample(self):
        expected = {F(0): F(1), F(1, 5): F(16, 17), F(1): F(4, 5)}
        for lam, target in expected.items():
            self.assertEqual(posterior(F(1, 2), coupled_model(lam), "++"),
                             target)
        self.assertIsNone(posterior(F(1, 2), coupled_model(F(1)), "+-"))

    def test_cross_oracle_risk_agreement(self):
        for lam in GRID:
            model = coupled_model(lam)
            for prior in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
                with self.subTest(lam=lam, prior=prior):
                    full = enumerate_plans(prior, model)
                    first = enumerate_plans(prior, model, False)
                    self.assertEqual(full, expected_risk(prior, model))
                    self.assertEqual(first, first_only_risk(prior, model))
                    self.assertLessEqual(full, first)
                    self.assertEqual(full, enumerate_plans(prior, swapped(model)))
        duplicate = coupled_model(F(1))
        for prior in (F(1, 4), F(1, 2), F(3, 4)):
            self.assertEqual(expected_risk(prior, duplicate),
                             first_only_risk(prior, duplicate))

    def test_independence_misspecification_is_detectable(self):
        independent = coupled_model(F(1, 5))
        reference = posterior(F(1, 2), independent, "++")
        self.assertEqual(reference, F(16, 17))
        for lam in (F(0), F(1, 2), F(1)):
            self.assertNotEqual(
                posterior(F(1, 2), coupled_model(lam), "++"), reference
            )

    def test_reject_invalid_couplings(self):
        for lam in (F(-1, 10), F(11, 10), 0.5):
            with self.assertRaises(ValueError):
                coupled_model(lam)


if __name__ == "__main__":
    unittest.main()
