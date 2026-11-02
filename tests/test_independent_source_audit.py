"""Reproducibility and falsification tests for the narrow 3-source audit."""
import unittest

from src.independent_source_audit import (
    A, B, EMPTY, Lasso, audit_independent_sources,
    holds, recognize, witness_for,
)


class IndependentSourceAuditTests(unittest.TestCase):
    def test_pinned_data_has_three_distinct_originals_not_fifteen(self):
        result = audit_independent_sources()
        self.assertEqual(result["source_rows"], 25)
        self.assertEqual(result["supported_rows"], 15)
        self.assertEqual(result["independent_original_requirements"], 3)
        self.assertEqual(result["supported_rows_by_family"],
                         {"cardinality": 5, "offset": 5, "relative": 5})

    def test_counterexample_rows_and_duplicate_dependence(self):
        result = audit_independent_sources()
        self.assertEqual(result["witnessed_mismatch_rows"], 12)
        self.assertEqual(result["witnessed_mismatches_by_family"],
                         {"cardinality": 2, "offset": 5, "relative": 5})
        self.assertEqual(result["distinct_witnessed_mutated_texts"], 6)
        self.assertEqual(result["unsupported_rows_no_verdict"], 10)
        self.assertEqual(
            result["supported_rows_without_counterexample_no_equivalence_claim"], 3)

    def test_each_witness_separates_inherited_formula_and_changed_english(self):
        result = audit_independent_sources()
        for counterexample in result["counterexamples"]:
            family = counterexample["family"]
            n = {"offset": 2, "relative": 2, "cardinality": 2}[family]
            # The offset family also contains 1, 4, 6; use exact row text.
            if family == "offset":
                words = {"one": 1, "two": 2, "four": 4, "six": 6}
                n = next(v for word, v in words.items()
                         if " " + word + " steps later." in counterexample["mutated"])
            witness = witness_for(family)
            self.assertTrue(holds(family, n, witness, inherited_formula=True))
            self.assertFalse(holds(family, n, witness, inherited_formula=False))

    def test_cardinality_unchanged_witness_is_not_equivalence_proof(self):
        witness = witness_for("cardinality")
        self.assertTrue(holds("cardinality", 1, witness, inherited_formula=True))
        self.assertTrue(holds("cardinality", 1, witness, inherited_formula=False))
        # At-least-one and exactly-one differ on two true propositions;
        # our evaluator deliberately does not adjudicate that ambiguity.
        self.assertFalse(audit_independent_sources()["publication_ready"])

    def test_lasso_is_infinite_not_a_finite_trace_assumption(self):
        word = Lasso((A, EMPTY), (B, EMPTY))
        self.assertEqual(word.at(0), A)
        self.assertEqual(word.at(2), B)
        self.assertEqual(word.at(4), B)
        self.assertEqual(word.at(100), B)
        with self.assertRaises(ValueError):
            word.at(-1)
        with self.assertRaises(ValueError):
            Lasso((), ()).at(0)

    def test_reject_unsupported_paraphrases_and_changed_formula(self):
        base = {
            "Original_Requirement":
                "Whenever a is enabled, b is enabled three steps later.",
            "requirement":
                "Whenever a is enabled, b is enabled two steps later.",
            "formula": "G(a -> X (X (X b)))",
        }
        self.assertEqual(recognize(base), ("offset", 3, 2))
        self.assertIsNone(recognize({**base, "formula": "F b"}))
        self.assertIsNone(recognize({**base, "requirement": "Maybe b happens later"}))
        with self.assertRaises(ValueError):
            recognize({**base, "Original_Requirement":
                       "Whenever a is enabled, b is enabled four steps later."})

    def test_relative_delay_is_measured_after_b_not_after_a(self):
        word = witness_for("relative")
        self.assertTrue(holds("relative", 1, word, inherited_formula=True))
        self.assertTrue(holds("relative", 1, word, inherited_formula=False))
        self.assertFalse(holds("relative", 2, word, inherited_formula=False))

    def test_no_false_generalization_or_publication_claim(self):
        result = audit_independent_sources()
        self.assertEqual(result["status"], "EXPLORATORY_DATASET_CONSISTENCY_ONLY")
        self.assertFalse(result["publication_ready"])
        self.assertIn("three original source", result["limits"][0])


if __name__ == "__main__":
    unittest.main()
