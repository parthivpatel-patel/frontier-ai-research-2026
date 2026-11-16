"""Protocol 116 negative controls and exact identities; unexecuted specification."""
import unittest
from fractions import Fraction as F

from protocol_116_joint_verifier import (
    independent_model, duplicate_model, posterior, marginals,
    expected_risk, first_only_risk, joint_model
)


class JointVerifierTests(unittest.TestCase):
    def setUp(self):
        self.independent = independent_model(F(4, 5), F(4, 5))
        self.duplicate = duplicate_model(F(4, 5), F(4, 5))

    def test_equal_marginals_different_posteriors(self):
        for model in (self.independent, self.duplicate):
            for index in (0, 1):
                self.assertEqual(marginals(model, True, index), F(4, 5))
                self.assertEqual(marginals(model, False, index), F(1, 5))
        self.assertEqual(posterior(F(1, 2), self.independent, "++"), F(16, 17))
        self.assertEqual(posterior(F(1, 2), self.duplicate, "++"), F(4, 5))

    def test_duplicate_adds_no_value(self):
        self.assertEqual(first_only_risk(F(1, 2), self.duplicate),
                         expected_risk(F(1, 2), self.duplicate))

    def test_independent_second_test_can_help(self):
        self.assertLessEqual(expected_risk(F(1, 2), self.independent),
                             first_only_risk(F(1, 2), self.independent))

    def test_impossible_mixed_duplicate_observations(self):
        self.assertIsNone(posterior(F(1, 2), self.duplicate, "+-"))
        self.assertIsNone(posterior(F(1, 2), self.duplicate, "-+"))

    def test_invalid_joint_distribution_rejected(self):
        with self.assertRaises(ValueError):
            joint_model({True: {"++": 1, "+-": 1, "-+": 0, "--": 0},
                         False: {"++": 1, "+-": 0, "-+": 0, "--": 0}})

    def test_float_rejected(self):
        with self.assertRaises(ValueError):
            independent_model(0.8, F(4, 5))


if __name__ == "__main__":
    unittest.main()
