"""Protocol 065: deterministic adversarial tests for physics pilot admission.

These are synthetic records. Passing tests does not adjudicate physical truth.
Run only on an explicitly confirmed zero-cost hosted runner:
    python -m unittest discover -s tests -p 'test_physics_pilot_admission.py' -v
"""
import importlib.util
from pathlib import Path
import unittest

MODULE = Path(__file__).resolve().parents[1] / "tools" / "validate_physics_pilot.py"
spec = importlib.util.spec_from_file_location("physics_pilot_admission", MODULE)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def record(**changes):
    base = {
        "claim_id": "claim_001",
        "source_family_id": "family_001",
        "source_uri": "https://example.org/illustrative",
        "source_license": "synthetic-test-only",
        "domain": "mechanics",
        "split": "development",
        "claim_text": "Illustrative proposition; not a measured physics claim",
        "assumptions": ["idealized setting"],
        "truth_label": "unknown",
        "adjudication_method": "not adjudicated",
        "adjudication_evidence": [],
        "adjudicator_id": "none",
        "certificate_text": "",
        "certificate_assumptions": ["idealized setting"],
        "certificate_status": "unverified",
    }
    base.update(changes)
    return base


def errors(*items):
    return validator.validate([(i, r) for i, r in enumerate(items, 1)])


class PhysicsPilotAdmissionTests(unittest.TestCase):
    def test_unknown_truth_is_allowed(self):
        self.assertEqual(errors(record()), [])

    def test_valid_certificate_does_not_force_known_truth(self):
        self.assertEqual(errors(record(certificate_status="valid",
                                       certificate_text="Formal derivation only")), [])

    def test_known_truth_without_evidence_rejected(self):
        self.assertTrue(any("known truth requires" in e for e in errors(
            record(truth_label="correct"))))

    def test_known_truth_with_evidence_is_schema_only(self):
        self.assertEqual(errors(record(truth_label="incorrect",
                                       adjudication_evidence=["illustrative citation"])), [])

    def test_duplicate_id_rejected(self):
        self.assertTrue(any("duplicate claim_id" in e for e in errors(record(), record())))

    def test_family_leakage_rejected(self):
        self.assertTrue(any("leaks across splits" in e for e in errors(
            record(), record(claim_id="claim_002", split="test"))))

    def test_distinct_families_across_splits_allowed(self):
        self.assertEqual(errors(record(), record(claim_id="claim_002",
                          source_family_id="family_002", split="test")), [])

    def test_missing_fields_rejected(self):
        bad = record()
        del bad["source_license"]
        self.assertTrue(any("missing fields" in e for e in errors(bad)))

    def test_empty_assumptions_rejected(self):
        self.assertTrue(any("assumptions must" in e for e in errors(
            record(assumptions=[]))))

    def test_unsupported_domain_rejected(self):
        self.assertTrue(any("unsupported domain" in e for e in errors(
            record(domain="astrology")))

    def test_invalid_label_rejected(self):
        self.assertTrue(any("invalid truth_label" in e for e in errors(
            record(truth_label="probably_correct")))

    def test_empty_valid_certificate_rejected(self):
        self.assertTrue(any("valid certificate requires" in e for e in errors(
            record(certificate_status="valid", certificate_text="")))

    def test_nonobject_rejected(self):
        self.assertTrue(any("record must be an object" in e for e in errors(None)))

    def test_malformed_list_domain_should_be_rejected_not_crash(self):
        # Invalid JSON type must yield an admission error.
        self.assertTrue(errors(record(domain=[])))

    def test_malformed_list_split_should_be_rejected_not_crash(self):
        # Invalid JSON type must yield an admission error.
        self.assertTrue(errors(record(split=[])))

    def test_malformed_list_truth_label_should_be_rejected_not_crash(self):
        # Invalid JSON type must yield an admission error.
        self.assertTrue(errors(record(truth_label=[])))

    def test_malformed_list_certificate_status_should_be_rejected_not_crash(self):
        # Invalid JSON type must yield an admission error.
        self.assertTrue(errors(record(certificate_status=[])))

    def test_valid_certificate_nonstring_text_rejected_not_crash(self):
        self.assertTrue(any("certificate_text must" in e for e in errors(record(certificate_status="valid", certificate_text=[]))))

    def test_malformed_split_dictionary_rejected_not_crash(self):
        self.assertTrue(any("unsupported split" in e for e in errors(record(split={}))))


if __name__ == "__main__":
    unittest.main()
