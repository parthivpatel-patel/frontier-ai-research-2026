"""Deterministic contract tests for Protocol 127; no model inference."""
import math
import unittest

from research.monte_carlo_rank_diagnostic import (
    dkw_rank_error,
    minimum_defined_draws,
    percentile_rank_diagnostic,
)


class MonteCarloRankDiagnosticTests(unittest.TestCase):
    def test_zero_draws_is_undefined(self):
        self.assertIsNone(dkw_rank_error(0))

    def test_one_draw_bound_is_vacuous(self):
        self.assertGreater(dkw_rank_error(1), 1)

    def test_thousand_draws(self):
        self.assertAlmostEqual(dkw_rank_error(1000), math.sqrt(math.log(40) / 2000))

    def test_required_draws_boundary(self):
        self.assertEqual(minimum_defined_draws(0.01), 18445)
        self.assertGreater(dkw_rank_error(18444), 0.01)
        self.assertLessEqual(dkw_rank_error(18445), 0.01)

    def test_monotonicity(self):
        self.assertGreater(dkw_rank_error(1000), dkw_rank_error(2000))
        self.assertGreater(dkw_rank_error(2000), dkw_rank_error(10000))

    def test_invalid_counts(self):
        for count in (-1, 1.5, True):
            with self.subTest(count=count), self.assertRaises((TypeError, ValueError)):
                dkw_rank_error(count)

    def test_invalid_alpha(self):
        for alpha in (0, 1, -0.1, float("nan"), float("inf"), True):
            with self.subTest(alpha=alpha), self.assertRaises((TypeError, ValueError)):
                dkw_rank_error(10, alpha)

    def test_invalid_tolerance(self):
        for tolerance in (0, 1, float("nan"), True):
            with self.subTest(tolerance=tolerance), self.assertRaises((TypeError, ValueError)):
                minimum_defined_draws(tolerance)

    def test_requested_draws_consistency(self):
        with self.assertRaises(ValueError):
            percentile_rank_diagnostic(10, 9)

    def test_report_explicitly_disclaims_coverage(self):
        report = percentile_rank_diagnostic(1000, 2000)
        self.assertEqual(report["defined_fraction"], 0.5)
        self.assertIn("NOT interval coverage", report["interpretation"])

    def test_empty_requested_draws(self):
        report = percentile_rank_diagnostic(0, 0)
        self.assertIsNone(report["defined_fraction"])
        self.assertIsNone(report["dkw_simultaneous_cdf_rank_error"])


if __name__ == "__main__":
    unittest.main()
