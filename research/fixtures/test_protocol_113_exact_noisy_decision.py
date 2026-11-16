"""Unexecuted regression specifications for Protocol 113."""
import unittest
from fractions import Fraction as F
from protocol_113_exact_noisy_decision import evaluate, decision_loss


class NoisyDecisionTests(unittest.TestCase):
    def test_protocol_112_fixture(self):
        r = evaluate(F(1,2), F(4,5), F(4,5), F(1,10))
        self.assertEqual(r["prior_risk"], F(1,4))
        self.assertEqual(r["posterior_risk"], F(1,5))
        self.assertEqual(r["gross_value"], F(1,20))
        self.assertEqual(r["net_value"], -F(1,20))
        self.assertFalse(r["buy_test"])
        self.assertEqual(r["observations"]["positive"]["posterior_true"], F(4,5))
        self.assertEqual(r["observations"]["negative"]["posterior_true"], F(1,5))

    def test_perfect_observation_limit(self):
        r = evaluate(F(1,2), 1, 1, F(1,10))
        self.assertEqual(r["posterior_risk"], 0)
        self.assertEqual(r["gross_value"], F(1,4))
        self.assertTrue(r["buy_test"])

    def test_uninformative_test(self):
        r = evaluate(F(1,2), F(1,2), F(1,2), F(1,10))
        self.assertEqual(r["gross_value"], 0)
        self.assertFalse(r["buy_test"])

    def test_zero_mass_observation_is_skipped(self):
        r = evaluate(1, 1, 0)
        self.assertEqual(set(r["observations"]), {"positive"})
        self.assertEqual(r["observations"]["positive"]["posterior_true"], 1)

    def test_asymmetric_losses(self):
        self.assertEqual(decision_loss(F(1,4), false_accept=4,
                                       false_reject=1, abstain=2), F(1,4))

    def test_invalid_float_and_negative_cost(self):
        with self.assertRaises(ValueError):
            evaluate(0.5, 1, 1)
        with self.assertRaises(ValueError):
            evaluate(F(1,2), 1, 1, -1)

    def test_nonnegative_value_of_information(self):
        for prior in (0, F(1,4), F(1,2), F(3,4), 1):
            for se in (0, F(1,2), 1):
                for sp in (0, F(1,2), 1):
                    self.assertGreaterEqual(evaluate(prior, se, sp)["gross_value"], 0)


if __name__ == "__main__":
    unittest.main()
