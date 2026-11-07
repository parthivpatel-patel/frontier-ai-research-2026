"""Synthetic Protocol 118 admission-to-bootstrap tests; no model evaluation."""
import unittest

from research.admitted_common_acceptance_bootstrap import admitted_common_acceptance_bootstrap
from research.matched_intervention_validator import AdmissionError
from tests.test_admitted_common_support import row


def dataset():
    return [
        row("A", lineage="L1", unsafe=True),
        row("B", lineage="L1", unsafe=False),
        row("A", lineage="L2", unsafe=False),
        row("B", lineage="L2", unsafe=False),
    ]


def estimate(rows, **kwargs):
    return admitted_common_acceptance_bootstrap(
        rows, {"mechanics": 1.0}, seed=7, replicates=80, **kwargs
    )


class AdmissionBootstrapIntegrationTests(unittest.TestCase):
    def test_paired_point_and_metadata(self):
        result = estimate(dataset())
        self.assertEqual(result["point"], 0.5)
        self.assertEqual(result["admission"]["interventions"], 2)
        self.assertEqual(result["estimand"], "common_acceptance_paired_difference")

    def test_permutation_is_deterministic(self):
        self.assertEqual(estimate(dataset()), estimate(list(reversed(dataset()))))

    def test_missing_counterpart_fails(self):
        with self.assertRaises(AdmissionError):
            estimate(dataset()[:-1])

    def test_mixed_split_fails(self):
        rows = dataset()
        rows[0]["split"] = "train"
        with self.assertRaises(AdmissionError):
            estimate(rows)

    def test_inconsistent_truth_fails(self):
        rows = dataset()
        rows[1]["prompt_truth"] = False
        with self.assertRaises(AdmissionError):
            estimate(rows)

    def test_family_weights_must_match(self):
        with self.assertRaises(AdmissionError):
            admitted_common_acceptance_bootstrap(dataset(), {"optics": 1.0})

    def test_no_joint_acceptance_is_undefined(self):
        rows = dataset()
        for r in rows:
            if r["system_id"] == "B":
                r["accepted"] = False
                r["response_unsafe"] = None
        result = estimate(rows)
        self.assertIsNone(result["point"])
        self.assertIsNone(result["ci95"])

    def test_single_lineage_fails(self):
        with self.assertRaises(ValueError):
            estimate(dataset()[:2])


if __name__ == "__main__":
    unittest.main()
