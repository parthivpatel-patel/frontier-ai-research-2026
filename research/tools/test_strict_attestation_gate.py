"""Strict freeze gate regression tests; standard library only."""
import importlib.util
import pathlib
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent / "validate_preregistration.py"
spec = importlib.util.spec_from_file_location("validator_strict", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class StrictAttestationTests(unittest.TestCase):
    def test_strict_gate_rejects_missing_attestation(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "manifest.json"
            path.write_text('{"status":"FROZEN"}', encoding="utf-8")
            errors = validator.validate(path, require_attestation=True)
            self.assertIn("strict freeze gate requires separate attestation", errors)

    def test_strict_cli_rejects_missing_attestation(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "manifest.json"
            path.write_text('{"status":"FROZEN"}', encoding="utf-8")
            self.assertEqual(validator.main(["validator.py", "--require-attestation", str(path)]), 2)

    def test_strict_gate_rejects_nonexistent_attestation(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "manifest.json"
            path.write_text('{"status":"FROZEN"}', encoding="utf-8")
            errors = validator.validate(path, pathlib.Path(d) / "absent.json", require_attestation=True)
            self.assertTrue(any("invalid attestation:" in e for e in errors), errors)



if __name__ == "__main__":
    unittest.main()
