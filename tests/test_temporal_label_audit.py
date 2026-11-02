"""Independent regression checks for the pinned external temporal dataset."""
import unittest

from src.temporal_label_audit import (
    FORMULA, audit_rows, audit_snapshot, number_of_steps,
    verify_upstream_snapshot, UPSTREAM_GIT_BLOB_SHA1,
)


class TemporalLabelAuditTests(unittest.TestCase):
    def test_pinned_upstream_blob_is_byte_exact(self):
        self.assertEqual(verify_upstream_snapshot(), UPSTREAM_GIT_BLOB_SHA1)

    def test_real_dataset_strict_subset(self):
        result = audit_snapshot()
        self.assertEqual(result["source_rows"], 25)
        self.assertEqual(result["strict_template_rows"], 5)
        self.assertEqual(result["witnessed_mismatch_rows"], 5)
        self.assertEqual(result["distinct_mutated_steps"], [1, 2, 4, 6])
        self.assertEqual(result["distinct_source_instructions"], 1)

    def test_every_witness_has_different_time_requirement(self):
        for row in audit_snapshot()["findings"]:
            self.assertNotEqual(row["mutated_steps"], row["formula_steps"])
            self.assertEqual(row["witness_a_true_at"], [0])
            self.assertEqual(row["witness_b_true_at"], [row["mutated_steps"]])
            self.assertTrue(row["english_true_on_witness"])
            self.assertFalse(row["inherited_formula_true_on_witness"])

    def test_unchanged_number_is_negative_control(self):
        rows = [{
            "requirement": "Whenever a is enabled, b is enabled three steps later.",
            "Original_Requirement": "Whenever a is enabled, b is enabled three steps later.",
            "formula": "G(a -> X (X (X b)))",
        }]
        result = audit_rows(rows)
        self.assertEqual(result["strict_template_rows"], 1)
        self.assertEqual(result["witnessed_mismatch_rows"], 0)

    def test_unsupported_language_and_formula_abstain(self):
        rows = [{
            "requirement": "If a then b sometime soon",
            "Original_Requirement": "If a then b",
            "formula": "G(a -> F b)",
        }, {
            "requirement": "Whenever a is enabled, b is enabled two steps later.",
            "Original_Requirement": "Whenever a is enabled, b is enabled three steps later.",
            "formula": "G(a -> X X b)",
        }]
        result = audit_rows(rows)
        self.assertEqual(result["strict_template_rows"], 0)
        self.assertEqual(result["witnessed_mismatch_rows"], 0)

    def test_template_parser_is_strict(self):
        self.assertEqual(number_of_steps("Whenever a is enabled, b is enabled two steps later."), 2)
        self.assertIsNone(number_of_steps("b eventually follows a"))
        self.assertEqual(FORMULA, "G(a->X(X(Xb)))")


if __name__ == "__main__":
    unittest.main()
