#!/usr/bin/env python3
"""Adversarial characterization of unverified freeze metadata.

This intentionally documents a *known weakness*, not a provenance guarantee.
Run in free GitHub Actions or another approved cloud environment only.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("prereg_validator", HERE / "validate_preregistration.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class UnverifiedMetadataTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.manifest = root / "manifest.json"
        self.attestation = root / "attestation.json"
        obj = {
            "status": "FROZEN",
            "source_family_definition": "one independent source family per original work",
            "sampling_frame": "predeclared public source registry",
            "domains": {
                domain: {"target_population": "public tasks", "sample_size_feasibility": "pilot pending"}
                for domain in ("nlp", "mathematics", "physics")
            },
            "candidate_policies": [{"id": "candidate"}],
            "baselines": [{"id": "baseline"}],
            "multiplicity_family": "all candidate-by-baseline-by-domain contrasts",
            "verification_budget": "matched",
            "exclusion_rules": "preregistered",
            "adjudication_protocol": "blind review"
        }
        raw = validator.canonical_bytes(obj)
        self.manifest.write_bytes(raw)
        self.att = {
            "manifest_path": str(self.manifest),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "git_commit": "not-a-real-commit",
            "freeze_utc": "not-a-timestamp",
            "canonicalization": "invented-identifier",
            "protocol_version": "fabricated-version"
        }

    def check(self):
        self.attestation.write_text(json.dumps(self.att), encoding="utf-8")
        return validator.validate(self.manifest, self.attestation, require_attestation=True)

    def test_fabricated_nonempty_provenance_currently_passes(self):
        # A passing test here demonstrates an existing weakness, not integrity.
        self.assertEqual([], self.check())

    def test_missing_commit_is_rejected(self):
        self.att["git_commit"] = ""
        self.assertTrue(any("attestation missing git_commit" in e for e in self.check()))

    def test_wrong_digest_is_rejected(self):
        self.att["sha256"] = "0" * 64
        self.assertTrue(any("digest mismatch" in e for e in self.check()))


if __name__ == "__main__":
    unittest.main()
