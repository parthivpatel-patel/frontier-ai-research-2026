"""Synthetic-only regression tests for pre-registered Protocol 018."""
import math
import unittest

from src.selective_risk_gate import (
    binomial_cdf, exact_one_sided_upper, fixed_roster_risk_audit,
)
from src.source_precision_gate import zero_failure_upper_bound


def row(method, source, accepted, incorrect):
    return {
        "method_id": method, "source_id": source,
        "accepted": accepted, "incorrect": incorrect,
    }


class ExactNonzeroFailureTests(unittest.TestCase):
    def test_zero_failures_agree_with_previous_protocol(self):
        for n in (1, 4, 30, 59, 299):
            self.assertAlmostEqual(
                exact_one_sided_upper(0, n), zero_failure_upper_bound(n),
                places=13,
            )

    def test_all_failures_bound_is_one(self):
        for n in (1, 2, 10, 100):
            self.assertEqual(exact_one_sided_upper(n, n), 1.0)

    def test_n_minus_one_failure_closed_form(self):
        for n in (2, 3, 10, 100):
            expected = math.exp(math.log1p(-0.05) / n)
            self.assertAlmostEqual(exact_one_sided_upper(n - 1, n), expected, places=13)

    def test_single_failure_two_trials(self):
        self.assertAlmostEqual(exact_one_sided_upper(1, 2), math.sqrt(.95), places=13)

    def test_interior_roots_satisfy_cdf(self):
        for n, k in ((10, 1), (20, 5), (59, 2), (100, 20)):
            upper = exact_one_sided_upper(k, n)
            self.assertGreater(upper, k / n)
            self.assertAlmostEqual(binomial_cdf(k, n, upper), 0.05, places=9)

    def test_more_failures_cannot_lower_bound(self):
        bounds = [exact_one_sided_upper(k, 20) for k in range(21)]
        self.assertEqual(bounds, sorted(bounds))

    def test_more_accepted_sources_zero_failures_tightens_bound(self):
        self.assertGreater(exact_one_sided_upper(0, 20),
                           exact_one_sided_upper(0, 30))

    def test_cdf_boundaries(self):
        self.assertEqual(binomial_cdf(1, 3, 0), 1.0)
        self.assertEqual(binomial_cdf(1, 3, 1), 0.0)
        self.assertEqual(binomial_cdf(3, 3, 1), 1.0)

    def test_invalid_counts(self):
        for k, n in ((-1, 2), (3, 2), (0, 0), (1, -1), (0, 10001),
                     (True, 3), (0, False), (1.0, 2)):
            with self.assertRaises(ValueError):
                exact_one_sided_upper(k, n)

    def test_invalid_alpha(self):
        for a in (0, 1, -1, math.nan, math.inf, True, "0.05"):
            with self.assertRaises(ValueError):
                exact_one_sided_upper(1, 3, alpha=a)

    def test_invalid_probability(self):
        for p in (-0.1, 1.1, math.nan, math.inf, True, "0.1"):
            with self.assertRaises(ValueError):
                binomial_cdf(1, 3, p)


class FixedRosterTests(unittest.TestCase):
    def test_duplicate_predictions_are_one_source(self):
        data = [
            row("A", "s1", True, False),
            row("A", "s1", True, True),
            row("A", "s2", True, False),
            row("B", "s1", True, False),
            row("B", "s2", False, None),
        ]
        out = fixed_roster_risk_audit(data, method_ids=("A", "B"))
        self.assertEqual(out["predeclared_method_count"], 2)
        self.assertEqual(out["per_method_alpha"], 0.025)
        self.assertEqual(out["methods"]["A"]["accepted_sources"], 2)
        self.assertEqual(out["methods"]["A"]["failed_accepted_sources"], 1)
        self.assertEqual(out["methods"]["B"]["accepted_sources"], 1)
        self.assertEqual(out["methods"]["B"]["failed_accepted_sources"], 0)

    def test_multiplicity_bounds_are_not_narrower(self):
        data = [
            row("A", f"s{i}", True, i == 0) for i in range(10)
        ] + [
            row("B", f"s{i}", True, False) for i in range(10)
        ]
        out = fixed_roster_risk_audit(data, method_ids=("A", "B"))
        self.assertGreaterEqual(out["methods"]["A"]["bonferroni_one_sided_upper"],
                                exact_one_sided_upper(1, 10))
        self.assertGreaterEqual(out["methods"]["B"]["bonferroni_one_sided_upper"],
                                exact_one_sided_upper(0, 10))

    def test_abstain_all_risk_undefined(self):
        out = fixed_roster_risk_audit([
            row("A", "s1", False, None),
        ], method_ids=("A",))
        self.assertEqual(out["methods"]["A"]["coverage"], 0)
        self.assertIsNone(out["methods"]["A"]["bonferroni_one_sided_upper"])

    def test_missing_adjudication_rejected(self):
        with self.assertRaisesRegex(ValueError, "adjudicated"):
            fixed_roster_risk_audit([
                row("A", "s1", True, None),
            ], method_ids=("A",))

    def test_source_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError, "same eligible source set"):
            fixed_roster_risk_audit([
                row("A", "s1", True, False),
                row("B", "s2", True, False),
            ], method_ids=("A", "B"))

    def test_unlisted_method_rejected(self):
        with self.assertRaisesRegex(ValueError, "fixed roster"):
            fixed_roster_risk_audit([
                row("A", "s1", True, False),
                row("B", "s1", True, False),
            ], method_ids=("A",))

    def test_duplicate_roster_rejected(self):
        with self.assertRaises(ValueError):
            fixed_roster_risk_audit([
                row("A", "s1", True, False),
            ], method_ids=("A", "A"))

    def test_missing_roster_member_rejected(self):
        with self.assertRaises(ValueError):
            fixed_roster_risk_audit([
                row("A", "s1", True, False),
            ], method_ids=("A", "B"))

    def test_invalid_schema_rejected(self):
        with self.assertRaises(ValueError):
            fixed_roster_risk_audit([
                {"method_id": "A", "source_id": "s1", "accepted": 1, "incorrect": False},
            ], method_ids=("A",))

    def test_bonferroni_coverage_not_superiority_test(self):
        data = [
            row("A", "s1", True, False),
            row("B", "s1", True, False),
        ]
        result = fixed_roster_risk_audit(data, method_ids=("A", "B"))
        self.assertIn("not a paired test", result["limitations"])


if __name__ == "__main__":
    unittest.main()
