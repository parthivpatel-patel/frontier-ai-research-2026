"""Offline regression tests for preregistered three-domain robustness audit."""
import unittest

from src.admissible_lasso_audit import Actuator, FLEXIBLE, FIXED
from src.domain_uncertainty_audit import (
    DOMAINS, MONOTONE_WAIT, OFFSETS, audit, domain_ladder_report,
)
from src.dynamics_masking_audit import is_restriction
from src.exhaustive_offset_audit import SearchBudgetExceeded


class DomainUncertaintyTests(unittest.TestCase):
    def test_three_domains_are_strictly_nested(self):
        self.assertTrue(is_restriction(FLEXIBLE, MONOTONE_WAIT))
        self.assertTrue(is_restriction(MONOTONE_WAIT, FIXED))
        self.assertNotEqual(FLEXIBLE.edges, MONOTONE_WAIT.edges)
        self.assertNotEqual(MONOTONE_WAIT.edges, FIXED.edges)

    def test_frozen_pre_registered_offsets(self):
        self.assertEqual(OFFSETS, (1, 2, 4, 6))
        self.assertEqual(len(DOMAINS), 3)

    def test_report_has_eight_directional_comparisons(self):
        report = audit()
        self.assertEqual(len(report["comparisons"]), 8)
        self.assertEqual(report["source_requirements"], 1)
        self.assertEqual(report["independent_model_predictions"], 0)
        self.assertFalse(report["publication_ready"])

    def test_every_witness_obeys_domain_monotonicity(self):
        for comparison in audit()["comparisons"]:
            flags = [r["witness_exists"] for r in comparison["domains"]]
            self.assertEqual(flags, sorted(flags, reverse=True))
            self.assertTrue(all(r["complete"] for r in comparison["domains"]))

    def test_all_absences_have_explicit_realizability_diagnostic(self):
        for comparison in audit()["comparisons"]:
            for result in comparison["domains"]:
                self.assertEqual(result["required_unrealizable"],
                                 not result["required_realizable"])
                if result["witness_exists"]:
                    self.assertTrue(result["required_realizable"])

    def test_categories_partition_eight_comparisons(self):
        report = audit()
        self.assertEqual(sum(report["classification_counts"].values()), 8)
        for comparison in report["comparisons"]:
            flags = [r["witness_exists"] for r in comparison["domains"]]
            expected = ("all_domains" if all(flags) else
                        "no_domain_witness" if not any(flags) else
                        "assumption_sensitive")
            self.assertEqual(comparison["classification"], expected)

    def test_hypotheses_are_derived_not_hardcoded(self):
        report = audit()
        self.assertEqual(report["H1_assumption_sensitivity_supported_on_toy"],
                         report["classification_counts"]["assumption_sensitive"] > 0)
        self.assertEqual(report["H2_intermediate_not_fixed_supported_on_toy"],
                         any(c["domains"][1]["witness_exists"] and
                             not c["domains"][2]["witness_exists"]
                             for c in report["comparisons"]))

    def test_non_nested_domain_ladder_rejected(self):
        with self.assertRaisesRegex(ValueError, "nested"):
            domain_ladder_report((FIXED, MONOTONE_WAIT))
        with self.assertRaisesRegex(ValueError, "nested"):
            domain_ladder_report((FLEXIBLE, FLEXIBLE))

    def test_bad_offset_sets_rejected(self):
        for offsets in ((), (1, 1), (3,), (True,), (7,)):
            with self.subTest(offsets=offsets):
                with self.assertRaisesRegex(ValueError, "offsets"):
                    domain_ladder_report(offsets=offsets)

    def test_budget_failure_never_becomes_equivalence(self):
        with self.assertRaises(SearchBudgetExceeded):
            domain_ladder_report(max_nodes=1)

    def test_invalid_budget_rejected(self):
        for invalid in (0, True, 1.5):
            with self.assertRaises(ValueError):
                domain_ladder_report(max_nodes=invalid)

    def test_unrealizable_source_not_reported_as_semantic_correctness(self):
        result = next(c for c in audit()["comparisons"]
                      if c["changed_offset"] == 1 and
                      c["direction"] == "changed_true_source_false")
        self.assertTrue(all(not d["required_realizable"]
                            for d in result["domains"]))
        self.assertEqual(result["classification"], "no_domain_witness")


if __name__ == "__main__":
    unittest.main()
