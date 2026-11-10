"""Adversarial contract tests for the Protocol 181 descriptive scorer.

Standard-library only. These tests use invented fixtures, not research outcomes.
Run on an independently verified zero-charge cloud runner.
"""
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("reference_scorer", HERE / "protocol_181_reference_scorer.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def record(condition, verdict="valid", source="s1", edit="e1"):
    return {
        "source_id": source,
        "edit_id": edit,
        "candidate_step_id": "step1",
        "run_manifest_hash": "manifest1",
        "physics_family": "mechanics",
        "edit_stratum": "truth_change",
        "provenance_condition": condition,
        "label_edited": "valid",
        "label_adjudication_status": "adjudicated",
        "verifier_output": verdict,
        "eligible": True,
        "rule_inventory_hash": "rules1",
        "prompt_hash": "prompt1",
        "model_or_verifier_version": "v1",
        "token_budget": 100,
        "compute_budget": 100,
        "assignment_seed": 42,
    }


class ScorerContractTests(unittest.TestCase):
    def test_one_pair_correct_advantage(self):
        result = module.score([record("correct"), record("matched_shuffle", "invalid")])
        self.assertEqual(result["n_sources"], 1)
        self.assertEqual(result["n_pairs"], 1)
        self.assertEqual(result["source_weighted_yield_difference"], 1.0)

    def test_abstention_counts_as_incorrect(self):
        result = module.score([record("correct", "abstain"), record("matched_shuffle")])
        self.assertEqual(result["source_weighted_yield_difference"], -1.0)

    def test_equal_weight_per_source_not_per_pair(self):
        rows = [
            record("correct", source="s1"),
            record("matched_shuffle", "invalid", source="s1"),
        ]
        for edit in ("e1", "e2", "e3"):
            rows.extend([
                record("correct", "invalid", source="s2", edit=edit),
                record("matched_shuffle", source="s2", edit=edit),
            ])
        result = module.score(rows)
        self.assertEqual(result["n_pairs"], 4)
        self.assertEqual(result["source_weighted_yield_difference"], 0.0)

    def test_incomplete_pair_rejected(self):
        with self.assertRaises(module.InvalidPilot):
            module.score([record("correct")])

    def test_duplicate_condition_rejected(self):
        with self.assertRaises(module.InvalidPilot):
            module.score([record("correct"), record("correct"), record("matched_shuffle")])

    def test_unadjudicated_rejected(self):
        row = record("correct")
        row["label_adjudication_status"] = "pending"
        with self.assertRaises(module.InvalidPilot):
            module.score([row, record("matched_shuffle")])

    def test_missing_required_field_rejected(self):
        row = record("correct")
        del row["rule_inventory_hash"]
        with self.assertRaises(module.InvalidPilot):
            module.score([row, record("matched_shuffle")])

    def test_label_mismatch_rejected(self):
        row = record("matched_shuffle")
        row["label_edited"] = "invalid"
        with self.assertRaises(module.InvalidPilot):
            module.score([record("correct"), row])

    def test_mismatched_budget_rejected(self):
        row = record("matched_shuffle")
        row["token_budget"] = 101
        with self.assertRaises(module.InvalidPilot):
            module.score([record("correct"), row])

    def test_prompt_hash_mismatch_must_be_rejected(self):
        """Regression: paired prompt hashes must agree."""
        row = record("matched_shuffle")
        row["prompt_hash"] = "different"
        with self.assertRaises(module.InvalidPilot):
            module.score([record("correct"), row])

    def test_cross_edit_source_family_mismatch_must_be_rejected(self):
        """Regression: source family cannot change across edits."""
        rows = [
            record("correct"), record("matched_shuffle"),
            record("correct", edit="e2"), record("matched_shuffle", edit="e2"),
        ]
        rows[2]["physics_family"] = "optics"
        rows[3]["physics_family"] = "optics"
        with self.assertRaises(module.InvalidPilot):
            module.score(rows)


if __name__ == "__main__":
    unittest.main()
