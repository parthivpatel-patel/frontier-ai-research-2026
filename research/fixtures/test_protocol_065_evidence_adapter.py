"""Protocol 065: evidence adapter for Protocol 063 (offline, standard library).

This module does not authorize cloud execution, verify billing, establish semantic
provenance, or freeze a manifest. Callers must separately attest those matters.
The adapter intentionally never emits positive billing/freeze evidence.
"""
from pathlib import Path
from research.fixtures.test_protocol_064_artifact_and_family_verification import (
    verify_artifact, verify_family_partitions, load_claim_records,
)


def build_artifact_family_evidence(root, artifact_specs, claims_path, claims_sha256):
    """Return (evidence, blockers) from independently read repository files.

    artifact_specs: sequence of (repository-relative path, expected SHA-256).
    Claims file must appear in the hashed set and be separately verified before
    parsing. No caller-provided 'verified' booleans are trusted.
    """
    evidence = {
        "artifact_hashes_recomputed": False,
        "family_assignments_verified_from_records": False,
        "calibration_family_ids": [],
        "test_family_ids": [],
        "freeze_commit_and_digest_verified": False,
        "account_billing_evidence_verified": False,
    }
    blockers = []
    if not isinstance(artifact_specs, (list, tuple)) or not artifact_specs:
        return evidence, ["artifact specification list empty"]
    if not isinstance(claims_path, str) or not claims_path.strip():
        return evidence, ["claims path missing"]
    if not isinstance(claims_sha256, str):
        return evidence, ["claims SHA-256 missing"]
    if (claims_path, claims_sha256) not in artifact_specs:
        return evidence, ["claims artifact not bound to verified artifact list"]
    seen = set()
    for spec in artifact_specs:
        if not isinstance(spec, (tuple, list)) or len(spec) != 2:
            blockers.append("malformed artifact specification")
            continue
        path, digest = spec
        if not isinstance(path, str) or not path.strip() or path in seen:
            blockers.append("empty or duplicate artifact path")
            continue
        seen.add(path)
        try:
            problem = verify_artifact(root, path, digest)
        except (OSError, ValueError, TypeError) as exc:
            problem = "artifact cannot be verified: " + type(exc).__name__
        if problem:
            blockers.append(f"{path}: {problem}")
    if blockers:
        return evidence, blockers
    evidence["artifact_hashes_recomputed"] = True
    try:
        base = Path(root).resolve(strict=True)
        target = (base / claims_path).resolve(strict=True)
        if not target.is_relative_to(base):
            return evidence, ["claims path escapes repository"]
        records = load_claim_records(target)
    except (OSError, ValueError, TypeError) as exc:
        return evidence, ["claim records cannot be parsed: " + type(exc).__name__]
    problems = verify_family_partitions(records)
    if problems:
        return evidence, problems
    evidence["calibration_family_ids"] = sorted({
        r["family_id"] for r in records if r["split"] == "calibration"
    })
    evidence["test_family_ids"] = sorted({
        r["family_id"] for r in records if r["split"] == "test"
    })
    evidence["family_assignments_verified_from_records"] = True
    return evidence, []


# Synthetic tests are definitions, not evidence of execution.
import hashlib
import json
import tempfile
import unittest


class EvidenceAdapterNegativeControls(unittest.TestCase):
    def test_valid_records_do_not_attest_billing_or_freeze(self):
        with tempfile.TemporaryDirectory() as directory:
            data = json.dumps([
                {"claim_id": "a", "family_id": "one", "split": "calibration"},
                {"claim_id": "b", "family_id": "two", "split": "test"},
            ]).encode()
            (Path(directory) / "claims.json").write_bytes(data)
            digest = hashlib.sha256(data).hexdigest()
            evidence, problems = build_artifact_family_evidence(
                directory, [("claims.json", digest)], "claims.json", digest)
            self.assertEqual(problems, [])
            self.assertTrue(evidence["artifact_hashes_recomputed"])
            self.assertTrue(evidence["family_assignments_verified_from_records"])
            self.assertFalse(evidence["account_billing_evidence_verified"])
            self.assertFalse(evidence["freeze_commit_and_digest_verified"])

    def test_modified_claims_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "claims.json").write_bytes(b"changed")
            digest = hashlib.sha256(b"original").hexdigest()
            evidence, problems = build_artifact_family_evidence(
                directory, [("claims.json", digest)], "claims.json", digest)
            self.assertTrue(problems)
            self.assertFalse(evidence["artifact_hashes_recomputed"])

    def test_unbound_claims_rejected(self):
        evidence, problems = build_artifact_family_evidence(
            ".", [("other.json", "0" * 64)], "claims.json", "0" * 64)
        self.assertIn("claims artifact not bound to verified artifact list", problems)
        self.assertFalse(evidence["family_assignments_verified_from_records"])


if __name__ == "__main__":
    unittest.main()
