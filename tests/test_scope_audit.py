"""Finite-fixture semantic and scope audit tests."""
import unittest
from src.scope_audit import (ThresholdClaim, example_fixtures,
                             formalization_mismatch, model_discrepancy, scope_audit)
from src.toy_falsification import Case

class ScopeAuditTests(unittest.TestCase):
    def setUp(self):
        self.good = Case(0.9, 0.2, 0.2)
        self.bad = Case(0.9, 0.2, -0.2)

    def test_distinct_witnesses(self):
        r = example_fixtures()
        self.assertTrue(r["model_error_witness"])
        self.assertTrue(r["formalization_mismatch_witness"])
        self.assertTrue(r["scope"]["unsupported_scope_expansion"])
        self.assertTrue(r["scope"]["observed_counterexample_outside_scope"])

    def test_negative_controls(self):
        r = example_fixtures()
        self.assertFalse(r["equivalent_model_negative_control"])
        self.assertFalse(r["matching_formalization_negative_control"])
        self.assertFalse(model_discrepancy(self.bad, candidate_has_wall=True))
        self.assertFalse(formalization_mismatch((self.good, self.bad),
                         ThresholdClaim(0.8), ThresholdClaim(0.8)))

    def test_valid_claim_full_scope(self):
        r = scope_audit((self.good, self.bad), (self.good, self.bad), ThresholdClaim(1.0))
        self.assertTrue(r["certificate_valid_on_checked_scope"])
        self.assertTrue(r["asserted_scope_fully_checked"])
        self.assertFalse(r["unsupported_scope_expansion"])

    def test_unsupported_does_not_imply_false(self):
        r = scope_audit((self.good,), (self.good, self.bad), ThresholdClaim(1.0))
        self.assertTrue(r["unsupported_scope_expansion"])
        self.assertFalse(r["observed_counterexample_outside_scope"])

    def test_invalid_checked_claim(self):
        r = scope_audit((self.bad,), (self.bad,), ThresholdClaim(0.8))
        self.assertFalse(r["certificate_valid_on_checked_scope"])

if __name__ == "__main__":
    unittest.main()
