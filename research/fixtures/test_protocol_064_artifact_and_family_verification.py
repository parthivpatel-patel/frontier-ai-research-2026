"""Protocol 064: independently recompute artifact digests and partition families.

This is a local *library*, not an authorization to execute on a user's laptop.
Run only on an approved, verified zero-cost cloud runner. Billing and freeze
attestation are intentionally outside this module's trust boundary.
"""
import hashlib
import json
from pathlib import Path


def verify_artifact(root, relative_path, expected_sha256):
    """Return a diagnostic; never accept a manifest's self-attested hash."""
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        return "missing or malformed expected SHA-256"
    try:
        int(expected_sha256, 16)
    except ValueError:
        return "expected SHA-256 is not hexadecimal"
    base = Path(root).resolve(strict=True)
    target = (base / relative_path).resolve(strict=True)
    if not target.is_relative_to(base) or not target.is_file():
        return "artifact is outside repository or not a regular file"
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    return None if digest == expected_sha256.lower() else "artifact SHA-256 mismatch"


def verify_family_partitions(records):
    """Check family-disjoint splits from supplied records, not a summary flag.

    Does not establish that source metadata is truthful, nor detect undeclared
    semantic duplicates. Those require an independent provenance review.
    """
    if not isinstance(records, list) or not records:
        return ["claim records missing"]
    families = {}
    errors = []
    seen = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"record {index}: not an object")
            continue
        claim_id = record.get("claim_id")
        family = record.get("family_id")
        split = record.get("split")
        if not isinstance(claim_id, str) or not claim_id.strip():
            errors.append(f"record {index}: missing claim ID")
        elif claim_id in seen:
            errors.append(f"record {index}: duplicate claim ID")
        else:
            seen.add(claim_id)
        if not isinstance(family, str) or not family.strip():
            errors.append(f"record {index}: missing family ID")
            continue
        if split not in ("calibration", "test", "train"):
            errors.append(f"record {index}: invalid split")
            continue
        families.setdefault(family, set()).add(split)
    for family, splits in families.items():
        if "test" in splits and ("calibration" in splits or "train" in splits):
            errors.append(f"family {family!r}: test/training contamination")
    if not any(r.get("split") == "calibration" for r in records if isinstance(r, dict)):
        errors.append("calibration partition empty")
    if not any(r.get("split") == "test" for r in records if isinstance(r, dict)):
        errors.append("test partition empty")
    return errors


def load_claim_records(path):
    """JSON list of claim records; caller must verify the file hash separately."""
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


# Negative controls are definitions, not claims of executed tests.
import unittest
import tempfile


class ArtifactAndPartitionNegativeControls(unittest.TestCase):
    def test_hash_recomputed_and_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            target = Path(root) / "claims.json"
            target.write_bytes(b"original")
            expected = hashlib.sha256(b"original").hexdigest()
            self.assertIsNone(verify_artifact(root, "claims.json", expected))
            target.write_bytes(b"tampered")
            self.assertEqual(verify_artifact(root, "claims.json", expected),
                             "artifact SHA-256 mismatch")

    def test_overlapping_family_rejected(self):
        records = [{"claim_id": "a", "family_id": "F1", "split": "calibration"},
                   {"claim_id": "b", "family_id": "F1", "split": "test"}]
        self.assertTrue(any("contamination" in x for x in
                            verify_family_partitions(records)))

    def test_disjoint_family_accepted(self):
        records = [{"claim_id": "a", "family_id": "F1", "split": "calibration"},
                   {"claim_id": "b", "family_id": "F2", "split": "test"}]
        self.assertEqual(verify_family_partitions(records), [])

    def test_duplicate_claim_rejected(self):
        records = [{"claim_id": "a", "family_id": "F1", "split": "calibration"},
                   {"claim_id": "a", "family_id": "F2", "split": "test"}]
        self.assertTrue(any("duplicate" in x for x in
                            verify_family_partitions(records)))


if __name__ == "__main__":
    unittest.main()
