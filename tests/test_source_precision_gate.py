"""Synthetic-only tests for the pre-registered independent-source precision gate."""
import math
import unittest

from src.source_precision_gate import (
    minimum_accepted_sources, source_risk_summary, zero_failure_upper_bound,
)


class PrecisionGateTests(unittest.TestCase):
    def test_exact_upper_30(self):
        self.assertAlmostEqual(zero_failure_upper_bound(30), 0.09503385, places=7)

    def test_exact_upper_59(self):
        self.assertAlmostEqual(zero_failure_upper_bound(59), 0.04950761, places=7)

    def test_exact_upper_15(self):
        self.assertAlmostEqual(zero_failure_upper_bound(15), 0.18103627, places=7)

    def test_minimum_for_five_percent(self):
        self.assertEqual(minimum_accepted_sources(0.05), 59)

    def test_minimum_for_one_percent(self):
        self.assertEqual(minimum_accepted_sources(0.01), 299)

    def test_minimum_for_ten_percent(self):
        self.assertEqual(minimum_accepted_sources(0.10), 29)

    def test_minimality(self):
        for risk in (0.01, 0.05, 0.10, 0.20):
            n = minimum_accepted_sources(risk)
            self.assertLessEqual(zero_failure_upper_bound(n), risk)
            if n > 1:
                self.assertGreater(zero_failure_upper_bound(n - 1), risk)

    def test_zero_source_denominator_rejected(self):
        for bad in (0, -1, True, 2.5, "30"):
            with self.assertRaises(ValueError):
                zero_failure_upper_bound(bad)

    def test_invalid_alpha_and_target_rejected(self):
        for bad in (0, 1, -0.1, math.inf, math.nan, True, "0.05"):
            with self.assertRaises(ValueError):
                zero_failure_upper_bound(30, alpha=bad)
            with self.assertRaises(ValueError):
                minimum_accepted_sources(bad)

    def test_source_clustering_prevents_pseudoreplication(self):
        rows = [
            {"source_id": "s1", "accepted": True, "incorrect": False},
            {"source_id": "s1", "accepted": True, "incorrect": True},
            {"source_id": "s1", "accepted": True, "incorrect": False},
            {"source_id": "s2", "accepted": True, "incorrect": False},
            {"source_id": "s3", "accepted": False, "incorrect": None},
        ]
        summary = source_risk_summary(rows)
        self.assertEqual(summary["n_eligible_sources"], 3)
        self.assertEqual(summary["n_accepted_sources"], 2)
        self.assertEqual(summary["n_failed_accepted_sources"], 1)
        self.assertAlmostEqual(summary["coverage"], 2 / 3)
        self.assertEqual(summary["observed_failure_fraction"], 0.5)
        self.assertIsNone(summary["one_sided_upper_if_zero_failures"])

    def test_no_acceptances_risk_undefined(self):
        s = source_risk_summary([
            {"source_id": "s1", "accepted": False, "incorrect": None}
        ])
        self.assertEqual(s["coverage"], 0)
        self.assertIsNone(s["observed_failure_fraction"])
        self.assertIsNone(s["one_sided_upper_if_zero_failures"])

    def test_zero_failure_summary_bound(self):
        s = source_risk_summary([
            {"source_id": "s1", "accepted": True, "incorrect": False},
            {"source_id": "s1", "accepted": True, "incorrect": False},
            {"source_id": "s2", "accepted": True, "incorrect": False},
        ])
        self.assertEqual(s["n_accepted_sources"], 2)
        self.assertAlmostEqual(s["one_sided_upper_if_zero_failures"],
                               zero_failure_upper_bound(2))

    def test_unadjudicated_accepted_prediction_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "adjudicated"):
            source_risk_summary([
                {"source_id": "s1", "accepted": True, "incorrect": None}
            ])

    def test_malformed_rows_fail_closed(self):
        invalid = [
            {"source_id": "s1", "accepted": 1, "incorrect": False},
            {"source_id": " s1", "accepted": True, "incorrect": False},
            {"source_id": "s1", "accepted": True, "incorrect": 0},
            {"source_id": "s1", "accepted": True},
        ]
        for row in invalid:
            with self.assertRaises(ValueError):
                source_risk_summary([row])


if __name__ == "__main__":
    unittest.main()
