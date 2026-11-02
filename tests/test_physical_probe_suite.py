"""Regression and negative controls for deliberately constructed probe cases."""
import unittest
from fractions import Fraction

from src.physical_probe_suite import make_suite, evaluate_suite
from src.exact_domain_audit import Q


class PhysicalProbeSuiteTests(unittest.TestCase):
    def test_ten_unique_cases_and_two_independent_families(self):
        cases = make_suite()
        self.assertEqual(len(cases), 10)
        self.assertEqual(len({case.case_id for case in cases}), 10)
        self.assertEqual({case.family for case in cases}, {"reflecting", "damped"})

    def test_exact_constructed_error_pattern(self):
        results = {row["id"]: row for row in evaluate_suite()["cases"]}
        for family in ("reflecting", "damped"):
            self.assertEqual(results[f"{family}_exact"]["latent_error"], 0)
            self.assertEqual(results[f"{family}_drift"]["latent_error"], 1)
            self.assertEqual(results[f"{family}_omitted"]["latent_error"], 1)
            self.assertEqual(results[f"{family}_multiple"]["latent_error"], 1)
            self.assertEqual(results[f"{family}_restricted"]["latent_error"], 0)

    def test_omitted_reference_breaks_supplied_envelope(self):
        summary = evaluate_suite()["summary"]
        self.assertEqual(summary["latent_error_rate"], "3/5")
        self.assertEqual(summary["supplied_lower_rate"], "1/5")
        self.assertEqual(summary["supplied_upper_rate"], "2/5")
        self.assertTrue(summary["latent_outside_supplied_envelope"])

    def test_matched_reachable_ranges(self):
        rows = evaluate_suite()["cases"]
        for row in rows:
            self.assertEqual(row["reachable"],
                             ["1/2", "3/4"] if row["intervention"] == "restricted"
                             else ["1/2", "1"])

    def test_all_constructed_errors_have_exact_witness(self):
        for row in evaluate_suite()["cases"]:
            self.assertEqual(row["counterexample_coordinates"] is not None,
                             row["latent_error"] == 1)
            if row["counterexample_coordinates"] is not None:
                self.assertTrue(all(isinstance(Fraction(x), Fraction)
                                    for x in row["counterexample_coordinates"]))

    def test_supplied_reference_is_not_latent_ground_truth(self):
        rows = {row["id"]: row for row in evaluate_suite()["cases"]}
        for family in ("reflecting", "damped"):
            self.assertEqual(rows[f"{family}_omitted"]["supplied_error_set"], [0])
            self.assertEqual(rows[f"{family}_multiple"]["supplied_error_set"], [0, 1])
            self.assertEqual(rows[f"{family}_drift"]["supplied_error_set"], [1])

    def test_restricted_equivalence_is_not_global_semantic_equivalence(self):
        for case in make_suite():
            if case.case_id.endswith("_restricted"):
                self.assertNotEqual(case.latent_upper, case.candidate_upper)
                self.assertEqual(case.latent_upper, Q("9/10"))


if __name__ == "__main__":
    unittest.main()
