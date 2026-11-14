"""Protocol 063: compositional readiness gate; no cloud execution authorized.

This module deliberately rejects self-attested family partitions and unverified
artifact hashes. It extends (does not replace) the Protocol 061 readiness gate.
Only run tests on independently verified $0 cloud infrastructure.
"""
import unittest
from research.fixtures.test_evaluation_manifest_gate import check_manifest
from research.fixtures.test_protocol_062_adversarial_controls import (
    validate_audit_budget, verify_disjoint_families, validate_coverage,
)

def check_manifest_strict(manifest, verified_evidence=None):
    """Return blockers. External evidence is required, not just manifest flags.

    verified_evidence is a mapping produced by a separate trusted artifact
    verifier; this function does NOT itself recompute hashes or attest billing.
    """
    blockers = list(check_manifest(manifest))
    evaluation = manifest.get("evaluation") or {}
    claims = manifest.get("claims") or {}
    evidence = verified_evidence or {}
    budget_problem = validate_audit_budget(evaluation.get("audit_budget"))
    if budget_problem:
        blockers.append(budget_problem)
    coverage_problem = validate_coverage(
        evaluation.get("target_release_coverage"),
        evaluation.get("coverage_tolerance"),
    )
    if coverage_problem:
        blockers.append(coverage_problem)
    family_problem = verify_disjoint_families(
        evidence.get("calibration_family_ids"),
        evidence.get("test_family_ids"),
    )
    if family_problem:
        blockers.append(family_problem)
    # Hash format and self-reported disjointness are not provenance evidence.
    if evidence.get("artifact_hashes_recomputed") is not True:
        blockers.append("artifact contents not independently hash-verified")
    if evidence.get("family_assignments_verified_from_records") is not True:
        blockers.append("family provenance not verified from claim records")
    if evidence.get("freeze_commit_and_digest_verified") is not True:
        blockers.append("freeze commit and manifest digest not independently bound")
    if evidence.get("account_billing_evidence_verified") is not True:
        blockers.append("account-specific $0 cloud billing evidence not independently verified")
    return blockers

class StrictGateNegativeControls(unittest.TestCase):
    def test_draft_rejected_even_with_self_attestation(self):
        candidate = {"status": "FROZEN", "claims": {"family_disjoint_verified": True},
                     "evaluation": {"audit_budget": 0, "target_release_coverage": 0.95,
                                    "coverage_tolerance": 0.1}}
        failures = check_manifest_strict(candidate)
        self.assertIn("audit_budget must be a positive integer", failures)
        self.assertIn("absolute coverage interval exceeds [0,1]", failures)
        self.assertIn("artifact contents not independently hash-verified", failures)

    def test_overlap_rejected_despite_claimed_verification(self):
        evidence = {"calibration_family_ids": ["a", "b"],
                    "test_family_ids": ["b", "c"],
                    "artifact_hashes_recomputed": True,
                    "family_assignments_verified_from_records": True}
        failures = check_manifest_strict({"evaluation": {"audit_budget": 1,
                 "target_release_coverage": 0.8, "coverage_tolerance": 0.05}}, evidence)
        self.assertIn("calibration and test share provenance families", failures)

    def test_boolean_is_not_billing_evidence(self):
        failures = check_manifest_strict({"infrastructure": {
            "cloud_execution_authorized": True}})
        self.assertIn("account-specific $0 cloud billing evidence not independently verified", failures)

if __name__ == "__main__":
    unittest.main()
