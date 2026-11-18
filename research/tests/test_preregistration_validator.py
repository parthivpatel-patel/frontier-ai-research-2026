#!/usr/bin/env python3
"""Adversarial standard-library tests for preregistration validation.

Run in a cloud CI runner: python -m unittest discover -s research/tests -p 'test_preregistration_validator.py'
These are structural tests; passing them cannot establish a pre-outcome freeze.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "tools" / "validate_preregistration.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def example_manifest():
    return {
        "status": "FROZEN",
        "source_family_definition": "Independent original authoring sources; audit dependencies",
        "sampling_frame": "Prospectively enumerated eligible sources",
        "domains": {
            d: {"target_population": d + " independently authored tasks",
                "sample_size_feasibility": "Pending evidence; no efficacy claim"}
            for d in ("nlp", "mathematics", "physics")
        },
        "candidate_policies": [{"id": "policy_A"}],
        "baselines": [{"id": "baseline_A"}],
        "multiplicity_family": "All three domains and all confirmatory comparisons",
        "verification_budget": "Equal calls and tokens",
        "exclusion_rules": "Exclude duplicates before outcomes are inspected",
        "adjudication_protocol": "Independent blinded review",
    }


class PreregistrationValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.manifest_path = Path(self.tmp.name) / "manifest.json"
        self.attestation_path = Path(self.tmp.name) / "attestation.json"

    def write_manifest(self, obj, canonical=True):
        if canonical:
            raw = validator.canonical_bytes(obj)
        else:
            raw = json.dumps(obj, indent=2).encode("utf-8")
        self.manifest_path.write_bytes(raw)
        return raw

    def write_attestation(self, raw, **changes):
        att = {
            "manifest_path": str(self.manifest_path),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "git_commit": "a" * 40,
            "freeze_utc": "2026-11-18T10:00:00Z",
            "canonicalization": "UTF-8 sorted compact JSON",
            "protocol_version": "159",
        }
        att.update(changes)
        self.attestation_path.write_text(json.dumps(att), encoding="utf-8")

    def test_valid_structure_and_matching_digest(self):
        raw = self.write_manifest(example_manifest())
        self.write_attestation(raw)
        self.assertEqual([], validator.validate(self.manifest_path, self.attestation_path))

    def test_draft_not_frozen(self):
        obj = example_manifest()
        obj["status"] = "DRAFT"
        self.write_manifest(obj)
        self.assertTrue(any("FROZEN" in x for x in validator.validate(self.manifest_path)))

    def test_self_hash_rejected(self):
        obj = example_manifest()
        obj["frozen_manifest_sha256"] = "0" * 64
        self.write_manifest(obj)
        self.assertTrue(any("self-referential" in x for x in validator.validate(self.manifest_path)))

    def test_noncanonical_json_rejected(self):
        self.write_manifest(example_manifest(), canonical=False)
        self.assertTrue(any("canonical" in x for x in validator.validate(self.manifest_path)))

    def test_duplicate_policy_ids_rejected(self):
        obj = example_manifest()
        obj["candidate_policies"].append({"id": "policy_A"})
        self.write_manifest(obj)
        self.assertTrue(any("unique" in x for x in validator.validate(self.manifest_path)))

    def test_missing_domain_rejected(self):
        obj = example_manifest()
        del obj["domains"]["physics"]
        self.write_manifest(obj)
        self.assertTrue(any("exactly" in x for x in validator.validate(self.manifest_path)))

    def test_nested_null_rejected(self):
        obj = example_manifest()
        obj["extra"] = {"nested": [None]}
        self.write_manifest(obj)
        self.assertTrue(any("null" in x for x in validator.validate(self.manifest_path)))

    def test_changed_manifest_breaks_digest(self):
        original = self.write_manifest(example_manifest())
        self.write_attestation(original)
        changed = example_manifest()
        changed["verification_budget"] = "Unlimited calls"
        self.write_manifest(changed)
        self.assertTrue(any("digest mismatch" in x for x in validator.validate(self.manifest_path, self.attestation_path)))

    def test_wrong_attestation_path_rejected(self):
        raw = self.write_manifest(example_manifest())
        self.write_attestation(raw, manifest_path="other.json")
        self.assertTrue(any("manifest_path mismatch" in x for x in validator.validate(self.manifest_path, self.attestation_path)))

    def test_missing_attestation_field_rejected(self):
        raw = self.write_manifest(example_manifest())
        self.write_attestation(raw, git_commit="")
        self.assertTrue(any("attestation missing git_commit" in x for x in validator.validate(self.manifest_path, self.attestation_path)))

    def test_invalid_json_rejected(self):
        self.manifest_path.write_bytes(b'{"broken":')
        self.assertTrue(any("invalid JSON" in x for x in validator.validate(self.manifest_path)))


if __name__ == "__main__":
    unittest.main()
