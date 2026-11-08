"""Synthetic, mocked reporting-contract tests; no model calls or simulation."""
import unittest
from unittest.mock import patch

from research.safeguarded_admitted_bootstrap import safeguarded_admitted_bootstrap


class SafeguardTests(unittest.TestCase):
    def run_mock(self, result, minimum=1000):
        with patch(
            "research.safeguarded_admitted_bootstrap.admitted_preflight_bootstrap",
            return_value=result,
        ):
            return safeguarded_admitted_bootstrap(
                [], {}, min_defined_replicates=minimum
            )

    def test_one_draw_suppresses_degenerate_interval(self):
        r = self.run_mock({"defined_replicates": 1, "ci95": (0.0, 0.0)})
        self.assertIsNone(r["ci95"])
        self.assertEqual(r["interval_suppression_reason"],
                         "insufficient_defined_bootstrap_draws")

    def test_below_threshold_suppresses(self):
        self.assertIsNone(self.run_mock(
            {"defined_replicates": 999, "ci95": (-.2, .2)}
        )["ci95"])

    def test_at_threshold_preserves(self):
        r = self.run_mock({"defined_replicates": 1000,
                           "ci95": (-.2, .2)})
        self.assertEqual(r["ci95"], (-.2, .2))
        self.assertTrue(r["interval_reported"])

    def test_upstream_suppression_preserved(self):
        r = self.run_mock({"defined_replicates": 2000, "ci95": None})
        self.assertFalse(r["interval_reported"])
        self.assertEqual(r["interval_suppression_reason"],
                         "upstream_eligibility_or_undefined_estimate")

    def test_reject_invalid_minimum(self):
        for value in (True, 1, 0, 1.5, "1000"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    safeguarded_admitted_bootstrap(
                        [], {}, min_defined_replicates=value
                    )

    def test_reject_malformed_interval(self):
        for interval in ((1.0, -1.0), (float("nan"), 1.0), (0.0,)):
            with self.subTest(interval=interval):
                with self.assertRaises(ValueError):
                    self.run_mock({"defined_replicates": 1000,
                                   "ci95": interval})

    def test_does_not_mutate_upstream_result(self):
        original = {"defined_replicates": 1, "ci95": (0.0, 0.0)}
        self.run_mock(original)
        self.assertEqual(original["ci95"], (0.0, 0.0))


if __name__ == "__main__":
    unittest.main()
