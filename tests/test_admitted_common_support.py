"""Synthetic integration checks; no empirical physics claims."""
import unittest

from research.admitted_common_support import admitted_common_support
from research.matched_intervention_validator import AdmissionError


def row(system, *, lineage="L", intervention="I", accepted=True, unsafe=False, split="heldout"):
    return {
        "physics_family": "mechanics", "lineage_id": lineage,
        "intervention_id": intervention, "system_id": system,
        "prompt_truth": True, "proposition_hash": "p",
        "evidence_hash": "e", "intervention_kind": "replacement",
        "split": split, "accepted": accepted,
        "response_unsafe": unsafe if accepted else None,
        "response_hash": f"response-{system}-{lineage}-{intervention}",
        "rubric_version": "v1", "adjudicator_ids": ["reviewer1"],
        "adjudication_timestamp": "2026-11-07T00:00:00Z",
        "adjudication_evidence_hash": "adjudication-evidence",
        "calibration_artifact_hash": "frozen-calibration",
        "split_manifest_hash": "frozen-splits", "git_revision": "revision",
        "model_configuration_hash": f"model-{system}",
    }


class AdmittedCommonSupportTests(unittest.TestCase):
    def test_valid_paired_difference(self):
        result = admitted_common_support([row("A", unsafe=True), row("B", unsafe=False)])
        self.assertEqual(result["common_support_difference"], 1.0)
        self.assertEqual(result["admission"]["interventions"], 1)

    def test_missing_counterpart_fails(self):
        with self.assertRaises(AdmissionError):
            admitted_common_support([row("A")])

    def test_truth_disagreement_fails(self):
        a, b = row("A"), row("B")
        b["prompt_truth"] = False
        with self.assertRaises(AdmissionError):
            admitted_common_support([a, b])

    def test_abstention_is_not_zero_risk(self):
        result = admitted_common_support([
            row("A", accepted=False), row("B", unsafe=True),
        ])
        self.assertIsNone(result["selective_risk"]["A"])
        self.assertIsNone(result["common_support_difference"])
        self.assertEqual(result["acceptance_cells"]["01"], 1)

    def test_nonheldout_rejected(self):
        with self.assertRaises(AdmissionError):
            admitted_common_support([row("A", split="train"), row("B", split="train")])

    def test_split_leakage_rejected(self):
        records = [row("A"), row("B"),
                   row("A", intervention="J", split="train"),
                   row("B", intervention="J", split="train")]
        with self.assertRaises(AdmissionError):
            admitted_common_support(records)

    def test_composite_key_collision_safe(self):
        records = [row("A", lineage="x:y", intervention="z"),
                   row("B", lineage="x:y", intervention="z"),
                   row("A", lineage="x", intervention="y:z"),
                   row("B", lineage="x", intervention="y:z")]
        self.assertEqual(admitted_common_support(records)["n"], 2)

    def test_generator_and_order_invariance(self):
        records = [row("A", unsafe=True), row("B")]
        a = admitted_common_support(iter(records))
        b = admitted_common_support(iter(reversed(records)))
        self.assertEqual(a["acceptance_cells"], b["acceptance_cells"])
        self.assertEqual(a["common_support_difference"], b["common_support_difference"])


if __name__ == "__main__":
    unittest.main()
