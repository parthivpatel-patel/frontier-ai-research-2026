"""Protocol 019: synthetic paired audit regression tests."""
import math
import unittest

from src.paired_unsafe_acceptance import exact_mcnemar, paired_unsafe_acceptance_audit


def row(m, s, accepted, incorrect):
    return {"method_id": m, "source_id": s,
            "accepted": accepted, "incorrect": incorrect}


def audit(rows, minimum=0.5, gap=0.1):
    return paired_unsafe_acceptance_audit(
        rows, method_ids=("A", "B"),
        min_coverage=minimum, max_coverage_gap=gap)


class ExactMcNemarTests(unittest.TestCase):
    def test_six_vs_zero(self):
        self.assertAlmostEqual(exact_mcnemar(6, 0)["two_sided_p"], .03125)

    def test_balanced_and_zero(self):
        self.assertAlmostEqual(exact_mcnemar(3, 3)["two_sided_p"], 1)
        self.assertEqual(exact_mcnemar(0, 0)["two_sided_p"], 1)
        self.assertEqual(exact_mcnemar(1, 0)["two_sided_p"], 1)

    def test_symmetry(self):
        for b, c in ((0, 7), (2, 10), (9, 3)):
            self.assertAlmostEqual(exact_mcnemar(b, c)["two_sided_p"],
                                   exact_mcnemar(c, b)["two_sided_p"])

    def test_log_p_underflow(self):
        r = exact_mcnemar(10000, 0)
        self.assertAlmostEqual(r["log10_two_sided_p"],
                               -9999 * math.log10(2), places=8)
        self.assertEqual(r["two_sided_p"], 0)

    def test_invalid_counts(self):
        for b, c in ((-1, 0), (0, -1), (True, 2),
                     (1.0, 0), (10001, 0)):
            with self.assertRaises(ValueError):
                exact_mcnemar(b, c)


class PairedSourceTests(unittest.TestCase):
    def test_any_error_and_source_dedup(self):
        rows = [
            row("A", "s1", True, False), row("A", "s1", True, True),
            row("A", "s2", True, False),
            row("B", "s1", True, False), row("B", "s2", True, False)]
        r = audit(rows)
        self.assertEqual(r["n_eligible_sources"], 2)
        self.assertEqual(r["paired_table"]["A_only_unsafe"], 1)
        self.assertEqual(r["methods"]["A"]["unsafe_accepted_sources"], 1)
        self.assertEqual(r["difference_unsafe_acceptance_A_minus_B"], .5)
        self.assertTrue(r["descriptive_coverage_gate_passed"])

    def test_method_swap_changes_sign_not_p(self):
        rows = [row("A", "s1", True, True), row("B", "s1", True, False),
                row("A", "s2", True, False), row("B", "s2", True, False)]
        x = audit(rows)
        y = audit([{**r, "method_id":
                    "B" if r["method_id"] == "A" else "A"} for r in rows])
        self.assertEqual(x["difference_unsafe_acceptance_A_minus_B"],
                         -y["difference_unsafe_acceptance_A_minus_B"])
        self.assertEqual(x["exact_mcnemar"]["two_sided_p"],
                         y["exact_mcnemar"]["two_sided_p"])

    def test_abstain_all_fails_coverage(self):
        r = audit([row("A", "s1", True, True),
                   row("B", "s1", False, None)])
        self.assertIsNone(r["methods"]["B"]["selective_failure_fraction"])
        self.assertFalse(r["descriptive_coverage_gate_passed"])
        self.assertIn("no_matched_coverage_claim", r["comparison_status"])

    def test_coverage_gap(self):
        rows = [row("A", "s1", True, False),
                row("A", "s2", True, False),
                row("B", "s1", True, False),
                row("B", "s2", False, None)]
        self.assertFalse(audit(rows)["descriptive_coverage_gate_passed"])
        self.assertTrue(audit(rows, gap=.5)["descriptive_coverage_gate_passed"])

    def test_missing_sources_and_labels(self):
        with self.assertRaisesRegex(ValueError, "identical"):
            audit([row("A", "s1", True, False),
                   row("B", "s2", True, False)])
        with self.assertRaisesRegex(ValueError, "adjudication"):
            audit([row("A", "s1", True, None),
                   row("B", "s1", True, False)])

    def test_invalid_roster(self):
        rows = [row("A", "s1", True, False),
                row("B", "s1", True, False)]
        for ids in (("A", "A"), ("A",), ["A", "B"], ("A", " ")):
            with self.assertRaises(ValueError):
                paired_unsafe_acceptance_audit(
                    rows, method_ids=ids, min_coverage=.5,
                    max_coverage_gap=.1)

    def test_invalid_thresholds(self):
        rows = [row("A", "s1", True, False),
                row("B", "s1", True, False)]
        for invalid in (-.1, 1.1, math.inf, math.nan, True, "0.5"):
            with self.assertRaises(ValueError):
                audit(rows, minimum=invalid)
            with self.assertRaises(ValueError):
                audit(rows, gap=invalid)

    def test_bad_schema_and_flags(self):
        base = [row("A", "s1", True, False),
                row("B", "s1", True, False)]
        for bad in ({**base[0], "accepted": 1},
                    {**base[0], "incorrect": "false"},
                    {**base[0], "source_id": " "},
                    {**base[0], "method_id": "C"},
                    {**base[0], "extra": 1}):
            with self.assertRaises(ValueError):
                audit([bad, base[1]])

    def test_four_table_cells(self):
        rows = []
        for i, (a, b) in enumerate(
                ((True, True), (True, False),
                 (False, True), (False, False))):
            rows += [row("A", f"s{i}", True, a),
                     row("B", f"s{i}", True, b)]
        r = audit(rows)
        self.assertEqual(r["paired_table"], {
            "both_unsafe": 1, "A_only_unsafe": 1,
            "B_only_unsafe": 1, "neither_unsafe": 1})
        self.assertEqual(r["exact_mcnemar"]["two_sided_p"], 1)

    def test_provenance_disclaimer(self):
        r = audit([row("A", "s1", True, False),
                   row("B", "s1", True, False)])
        self.assertEqual(r["data_provenance"], "caller_supplied_unverified")
        self.assertIn("not population equivalence", r["limitations"])


if __name__ == "__main__":
    unittest.main()
