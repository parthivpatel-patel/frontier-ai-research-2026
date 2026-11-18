#!/usr/bin/env python3
"""Adversarial unit tests for Git-object freeze provenance.

No network, model inference, or external dataset is needed. Git is mocked;
these tests establish local checker behavior, not external freeze timing.
"""
import hashlib
import importlib.util
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

MODULE = pathlib.Path(__file__).with_name("check_git_freeze_provenance.py")
spec = importlib.util.spec_from_file_location("check_git_freeze_provenance", MODULE)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
COMMIT = "a" * 40
HISTORICAL = b'{"study":"frozen"}\n'


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.manifest = self.root / "manifest.json"
        self.manifest.write_bytes(HISTORICAL)
        self.attestation = self.root / "attestation.json"
        self.data = {
            "git_commit": COMMIT,
            "manifest_path": str(self.manifest),
            "sha256": hashlib.sha256(HISTORICAL).hexdigest(),
        }
        # The checker intentionally rejects absolute manifest paths.
        self.data["manifest_path"] = "manifest.json"

    def run_check(self, historical=HISTORICAL, resolved=COMMIT):
        self.attestation.write_text(json.dumps(self.data), encoding="utf-8")
        def fake_git(*args):
            if args[0] == "rev-parse":
                return (resolved + "\n").encode()
            if args[0] == "show":
                return historical
            raise AssertionError(args)
        old_cwd = pathlib.Path.cwd()
        import os
        try:
            os.chdir(self.root)
            with patch.object(checker, "git", side_effect=fake_git):
                return checker.check(self.attestation)
        finally:
            os.chdir(old_cwd)

    def test_matching_commit_and_bytes_pass(self):
        self.assertEqual(self.run_check(), [])

    def test_fabricated_commit_resolution_rejected(self):
        self.assertTrue(self.run_check(resolved="b" * 40))

    def test_historical_digest_mismatch_rejected(self):
        self.assertTrue(self.run_check(historical=b"tampered"))

    def test_current_manifest_drift_rejected(self):
        self.manifest.write_bytes(b"changed")
        self.assertTrue(self.run_check())

    def test_path_traversal_rejected(self):
        self.data["manifest_path"] = "../manifest.json"
        self.assertTrue(self.run_check())

    def test_absolute_path_rejected(self):
        self.data["manifest_path"] = str(self.manifest)
        self.assertTrue(self.run_check())

    def test_malformed_commit_rejected(self):
        self.data["git_commit"] = "not-a-commit"
        self.assertTrue(self.run_check())

    def test_malformed_digest_rejected(self):
        self.data["sha256"] = "0" * 63
        self.assertTrue(self.run_check())

    def test_nonobject_attestation_rejected(self):
        self.attestation.write_text("[]", encoding="utf-8")
        self.assertTrue(checker.check(self.attestation))


if __name__ == "__main__":
    unittest.main()
