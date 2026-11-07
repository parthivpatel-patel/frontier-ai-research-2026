"""Synthetic contract tests; no empirical model outputs or cloud run implied."""
import copy
import unittest

from research.matched_intervention_validator import (
    AdmissionError, admit_matched_interventions,
)

SYSTEMS = ("candidate", "baseline")


def fixture():
    common = dict(
        physics_family="mechanics", lineage_id="L1", intervention_id="I1",
        prompt_truth=True, proposition_hash="prop1", evidence_hash="evidence1",
        intervention_kind="complete", split="heldout", accepted=True,
        rubric_version="rubric1", adjudicator_ids=["blind_reviewer_1"],
        adjudication_timestamp="2026-11-07T00:00:00Z",
        adjudication_evidence_hash="adjudication1",
        calibration_artifact_hash="calibration1", split_manifest_hash="manifest1",
        git_revision="revision1", model_configuration_hash="config1",
    )
    return [
        dict(common, system_id="candidate", response_unsafe=False, response_hash="response1"),
        dict(common, system_id="baseline", response_unsafe=True, response_hash="response2"),
    ]


class MatchedInterventionAdmissionTests(unittest.TestCase):
    def admit(self, rows):
        return admit_matched_interventions(rows, systems=SYSTEMS)

    def reject(self, rows):
        with self.assertRaises(AdmissionError):
            self.admit(rows)

    def test_valid_distinct_response_outcomes(self):
        result = self.admit(fixture())
        self.assertEqual((result.records, result.interventions, result.lineages), (2, 1, 1))

    def test_row_order_independence(self):
        rows = fixture()
        self.assertEqual(self.admit(rows), self.admit(list(reversed(rows))))

    def test_missing_counterpart(self):
        self.reject(fixture()[:1])

    def test_extra_unmatched_intervention(self):
        rows = fixture()
        rows.append(dict(rows[0], intervention_id="I2", response_hash="response3"))
        self.reject(rows)

    def test_duplicate_system_key(self):
        rows = fixture()
        rows.append(dict(rows[0]))
        self.reject(rows)

    def test_conflicting_prompt_truth(self):
        rows = fixture()
        rows[1]["prompt_truth"] = False
        self.reject(rows)

    def test_conflicting_evidence_hash(self):
        rows = fixture()
        rows[1]["evidence_hash"] = "different"
        self.reject(rows)

    def test_missing_adjudication(self):
        rows = fixture()
        rows[0]["adjudicator_ids"] = []
        self.reject(rows)

    def test_abstention_must_have_null_outcome(self):
        rows = fixture()
        rows[0]["accepted"] = False
        self.reject(rows)

    def test_valid_abstention(self):
        rows = fixture()
        rows[0]["accepted"] = False
        rows[0]["response_unsafe"] = None
        self.assertEqual(self.admit(rows).accepted_by_system["candidate"], 0) if "candidate" in self.admit(rows).accepted_by_system else self.assertNotIn("candidate", self.admit(rows).accepted_by_system)

    def test_lineage_leakage(self):
        rows = fixture()
        for row in fixture():
            row["intervention_id"] = "I2"
            row["split"] = "calibration"
            row["response_hash"] += "_new"
            rows.append(row)
        self.reject(rows)

    def test_frozen_artifact_mismatch(self):
        rows = fixture()
        rows[1]["calibration_artifact_hash"] = "changed"
        self.reject(rows)

    def test_reused_response_conflicting_adjudication(self):
        rows = fixture()
        rows[1]["response_hash"] = rows[0]["response_hash"]
        self.reject(rows)

    def test_boolean_not_integer(self):
        rows = fixture()
        rows[0]["accepted"] = 1
        self.reject(rows)


if __name__ == "__main__":
    unittest.main()
