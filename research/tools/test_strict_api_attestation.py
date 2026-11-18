"""Regression: direct Python API must enforce strict attestation (stdlib only)."""
import importlib.util
import pathlib
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent / "validate_preregistration.py"
spec = importlib.util.spec_from_file_location("prereg_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class StrictApiTests(unittest.TestCase):
    def test_direct_api_strict_without_attestation_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = pathlib.Path(directory) / "manifest.json"
            manifest.write_text('{"status":"FROZEN"}', encoding="utf-8")
            errors = validator.validate(manifest, require_attestation=True)
            self.assertTrue(any("requires a separate attestation" in e for e in errors), errors)

    def test_non_strict_api_does_not_require_attestation(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = pathlib.Path(directory) / "manifest.json"
            manifest.write_text('{"status":"FROZEN"}', encoding="utf-8")
            errors = validator.validate(manifest)
            self.assertFalse(any("requires a separate attestation" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
