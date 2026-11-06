"""Protocol 090: standard-library regression tests, no model calls."""
import unittest
from research.selective_risk_bounds import (
    RiskBounds, selective_risk_bounds, difference_bounds, superiority_established,
)


class SelectiveRiskBoundsTests(unittest.TestCase):
    def test_protocol_example(self):
        b = selective_risk_bounds(100, 70, 7)
        self.assertAlmostEqual(b.lower, .07)
        self.assertAlmostEqual(b.upper, .37)

    def test_complete_adjudication(self):
        self.assertEqual(selective_risk_bounds(10, 10, 3), RiskBounds(.3, .3))

    def test_no_adjudication(self):
        self.assertEqual(selective_risk_bounds(10, 0, 0), RiskBounds(0., 1.))

    def test_invalid_counts(self):
        for args in [(0, 0, 0), (-1, 0, 0), (10, 11, 1),
                     (10, 5, 6), (10, -1, 0), (10, 5, -1)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                selective_risk_bounds(*args)

    def test_invalid_types(self):
        for args in [(True, 0, 0), (10., 5, 1), (10, "5", 1)]:
            with self.subTest(args=args), self.assertRaises(TypeError):
                selective_risk_bounds(*args)

    def test_difference_and_strict_superiority(self):
        p = RiskBounds(.01, .04)
        b = RiskBounds(.10, .20)
        self.assertEqual(difference_bounds(p, b), RiskBounds(-.19, -.06))
        self.assertTrue(superiority_established(difference_bounds(p, b)))
        self.assertFalse(superiority_established(RiskBounds(-.1, 0.)))
        self.assertFalse(superiority_established(RiskBounds(-.1, .01)))

    def test_invalid_bounds(self):
        for bad in [RiskBounds(-.1, .2), RiskBounds(.2, 1.1),
                    RiskBounds(.5, .1), RiskBounds(float("nan"), 1.)]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                difference_bounds(bad, RiskBounds(0, 1))


if __name__ == "__main__":
    unittest.main()
