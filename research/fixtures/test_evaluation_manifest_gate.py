"""Conservative, dependency-free readiness gate for the draft evaluation manifest.

Usage (only on an approved, verified zero-cost cloud runner):
    python -m unittest research.fixtures.test_evaluation_manifest_gate

This test intentionally passes while the study is blocked: it verifies that a draft
cannot be mistaken for a frozen, executable experiment. It does not authorize jobs.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "research" / "manifests" / "evaluation_manifest_v0_1_DRAFT.json"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
DOMAINS = ("nlp", "mathematics", "physics")


def check_manifest(m):
    """Return readiness blockers; fail closed on missing or malformed fields."""
    blockers = []
    if m.get("schema_version") != "0.1.0":
        blockers.append("unsupported schema_version")
    if m.get("status") != "FROZEN":
        blockers.append("manifest not FROZEN")
    claims = m.get("claims") or {}
    verifiers = m.get("verifiers") or {}
    evaluation = m.get("evaluation") or {}
    infra = m.get("infrastructure") or {}
    freeze = m.get("freeze") or {}
    publication = m.get("publication") or {}
    hashes = {
        "claims": ("population_sha256", "family_assignment_sha256",
                   "source_corpus_sha256", "partition_manifest_sha256"),
        "verifiers": ("model_and_revision_manifest_sha256", "prompt_manifest_sha256",
                      "sampling_settings_sha256"),
        "evaluation": ("baseline_manifest_sha256", "calibration_families_sha256",
                       "test_families_sha256", "audit_sampling_design_sha256",
                       "audit_inclusion_witness_sha256"),
    }
    for name, fields in hashes.items():
        obj = {"claims": claims, "verifiers": verifiers, "evaluation": evaluation}[name]
        for field in fields:
            if not isinstance(obj.get(field), str) or not SHA256.fullmatch(obj[field]):
                blockers.append(f"{name}.{field} missing/invalid sha256")
    counts = claims.get("domain_counts")
    if not isinstance(counts, dict) or any(type(counts.get(d)) is not int or counts[d] < 1 for d in DOMAINS):
        blockers.append("positive integer counts required for all three domains")
    if claims.get("family_disjoint_verified") is not True:
        blockers.append("family disjointness not verified")
    if evaluation.get("primary_endpoint") != "false_acceptance_among_released_at_fixed_coverage":
        blockers.append("primary endpoint changed")
    for key in ("target_release_coverage", "coverage_tolerance"):
        value = evaluation.get(key)
        if type(value) not in (int, float) or not (0 < value < 1):
            blockers.append(f"evaluation.{key} must be in (0,1)")
    weights = evaluation.get("domain_weights")
    if not isinstance(weights, dict) or any(type(weights.get(d)) not in (int, float) or weights[d] < 0 for d in DOMAINS) or abs(sum(weights.get(d, 0) for d in DOMAINS) - 1) > 1e-9:
        blockers.append("domain_weights must be nonnegative and sum to one")
    if evaluation.get("threshold_selection_partition") not in ("development", "calibration"):
        blockers.append("threshold selection partition not independent of test")
    for key in ("family_cluster_uncertainty_method", "missing_label_policy", "multiplicity_policy"):
        if not isinstance(evaluation.get(key), str) or not evaluation[key].strip():
            blockers.append(f"evaluation.{key} unspecified")
    if type(evaluation.get("audit_budget")) is not int or evaluation["audit_budget"] < 0:
        blockers.append("audit budget unspecified")
    if evaluation.get("heldout_labels_accessed") is not False:
        blockers.append("heldout labels accessed or unknown")
    if evaluation.get("test_set_single_use") is not True:
        blockers.append("test-set single-use policy missing")
    if infra.get("external_paid_api_allowed") is not False or infra.get("local_compute_allowed") is not False:
        blockers.append("zero-cost/local-compute prohibition changed")
    for key in ("account_specific_zero_cost_verified", "standard_free_runner_verified",
                "billing_and_card_exposure_verified", "cloud_execution_authorized"):
        if infra.get(key) is not True:
            blockers.append(f"infrastructure.{key} not verified")
    if not isinstance(infra.get("provider"), str) or not infra["provider"].strip():
        blockers.append("cloud provider unspecified")
    if freeze.get("frozen") is not True or not isinstance(freeze.get("freeze_commit_sha"), str) or not re.fullmatch(r"[0-9a-f]{40}", freeze["freeze_commit_sha"]):
        blockers.append("freeze evidence absent")
    if not isinstance(freeze.get("freeze_utc_timestamp"), str) or not freeze["freeze_utc_timestamp"].endswith("Z"):
        blockers.append("freeze timestamp absent")
    if publication.get("ai_assistance_disclosure_required") is not True:
        blockers.append("AI-assistance disclosure requirement missing")
    return blockers


class ManifestGateTests(unittest.TestCase):
    def test_current_draft_is_blocked(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "DRAFT_NOT_FROZEN")
        self.assertTrue(check_manifest(manifest))
        self.assertIn("infrastructure.cloud_execution_authorized not verified", check_manifest(manifest))

    def test_missing_and_malformed_inputs_fail_closed(self):
        for candidate in ({}, {"status": "FROZEN"}, {"claims": {"domain_counts": {"nlp": True}}}):
            with self.subTest(candidate=candidate):
                self.assertTrue(check_manifest(candidate))

    def test_unapproved_cloud_cannot_be_overridden_by_frozen_label(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        manifest["status"] = "FROZEN"
        manifest["freeze"]["frozen"] = True
        self.assertIn("infrastructure.cloud_execution_authorized not verified", check_manifest(manifest))


if __name__ == "__main__":
    unittest.main()
