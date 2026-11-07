"""Protocol 123 synthetic bridge tests; not evidence of empirical validity."""
import unittest

from research.admitted_preflight_bootstrap import admitted_preflight_bootstrap
from research.matched_intervention_validator import AdmissionError
def dataset():
    records = []
    for lineage, unsafe_a in (("L1", True), ("L2", False)):
        for system in ("A", "B"):
            records.append({
                "physics_family": "mechanics", "lineage_id": lineage,
                "intervention_id": "I", "system_id": system,
                "prompt_truth": True, "proposition_hash": "p",
                "evidence_hash": "e", "intervention_kind": "replacement",
                "split": "heldout", "accepted": True,
                "response_unsafe": unsafe_a if system == "A" else False,
                "response_hash": f"response-{system}-{lineage}",
                "rubric_version": "v1", "adjudicator_ids": ["reviewer1"],
                "adjudication_timestamp": "2026-11-07T00:00:00Z",
                "adjudication_evidence_hash": "adjudication-evidence",
                "calibration_artifact_hash": "frozen-calibration",
                "split_manifest_hash": "frozen-splits", "git_revision": "revision",
                "model_configuration_hash": f"model-{system}",
            })
    return records



def estimate(rows, **kwargs):
    return admitted_preflight_bootstrap(
        rows, {"mechanics": 1.0}, seed=7, replicates=80, **kwargs
    )


class AdmittedPreflightTests(unittest.TestCase):
    def test_complete_acceptance(self):
        result = estimate(dataset())
        self.assertEqual(result["point"], 0.5)
        self.assertTrue(result["analytic_preflight"]["interval_eligible"])
        self.assertEqual(result["admission"]["interventions"], 2)

    def test_input_order_invariance(self):
        self.assertEqual(estimate(dataset()), estimate(list(reversed(dataset()))))

    def test_missing_counterpart_rejected(self):
        with self.assertRaises(AdmissionError):
            estimate(dataset()[:-1])

    def test_training_contamination_rejected(self):
        rows = dataset()
        rows[0]["split"] = "train"
        with self.assertRaises(AdmissionError):
            estimate(rows)

    def test_family_mismatch_rejected(self):
        with self.assertRaises(AdmissionError):
            admitted_preflight_bootstrap(dataset(), {"optics": 1.0})

    def test_zero_joint_acceptance_suppresses_interval(self):
        rows = dataset()
        for r in rows:
            if r["system_id"] == "B":
                r["accepted"] = False
                r["response_unsafe"] = None
        result = estimate(rows)
        self.assertIsNone(result["ci95"])
        self.assertFalse(result["analytic_preflight"]["interval_eligible"])

    def test_eligibility_independent_of_seed(self):
        a = estimate(dataset())
        b = admitted_preflight_bootstrap(
            dataset(), {"mechanics": 1.0}, seed=99, replicates=80
        )
        self.assertEqual(a["analytic_preflight"], b["analytic_preflight"])


if __name__ == "__main__":
    unittest.main()
