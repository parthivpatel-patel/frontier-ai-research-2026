"""Adversarial JSON parsing checks for preregistration validator. Standard library only."""
import importlib.util
import json
import pathlib
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent / "validate_preregistration.py"
spec = importlib.util.spec_from_file_location("prereg_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class DuplicateKeyTests(unittest.TestCase):
    def test_duplicate_top_level_key_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "manifest.json"
            path.write_text('{"status":"FROZEN","status":"DRAFT"}', encoding="utf-8")
            errors = validator.validate(path)
            self.assertTrue(any("duplicate JSON key: status" in e for e in errors), errors)

    def test_duplicate_nested_key_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "manifest.json"
            path.write_text('{"domains":{"nlp":{"target_population":"a","target_population":"b"}}}', encoding="utf-8")
            errors = validator.validate(path)
            self.assertTrue(any("duplicate JSON key: target_population" in e for e in errors), errors)

    def test_duplicate_attestation_key_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "manifest.json"
            att = pathlib.Path(directory) / "attestation.json"
            path.write_text('{"status":"FROZEN"}', encoding="utf-8")
            att.write_text('{"sha256":"first","sha256":"second"}', encoding="utf-8")
            errors = validator.validate(path, att)
            self.assertTrue(any("duplicate JSON key: sha256" in e for e in errors), errors)

    def test_unique_keys_parse_normally(self):
        self.assertEqual(validator.reject_duplicate_keys([("a", 1), ("b", 2)]), {"a": 1, "b": 2})


if __name__ == "__main__":
    unittest.main()
