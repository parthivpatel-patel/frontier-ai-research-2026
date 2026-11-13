"""Protocol 061 leakage firewall: synthetic negative controls, standard library only.

These tests validate split/audit/threshold policies, not AI performance.
No datasets, models, network, or GPU are required.
"""
import unittest


def assert_family_disjoint(partitions):
    """Reject provenance families appearing in more than one split."""
    seen = {}
    for split, records in partitions.items():
        for record in records:
            family = record.get("family")
            if not isinstance(family, str) or not family.strip():
                raise ValueError("missing provenance family")
            previous = seen.setdefault(family, split)
            if previous != split:
                raise ValueError("provenance family crosses partitions")
    return True


def assert_audit_design_label_blind(records, audit_keys):
    """An audit-design input may not include truth labels or adjudications."""
    forbidden = {"truth", "label", "is_correct", "adjudication", "heldout_truth"}
    if forbidden.intersection(audit_keys):
        raise ValueError("audit design uses forbidden label field")
    for record in records:
        if not set(audit_keys).issubset(record):
            raise ValueError("missing audit-design field")
    return True


def assert_threshold_provenance(threshold_record, test_partition="test"):
    """A threshold must be selected without accessing held-out labels."""
    if threshold_record.get("selected_on") == test_partition:
        raise ValueError("test-label threshold tuning")
    if threshold_record.get("used_test_labels") is not False:
        raise ValueError("test-label access not explicitly excluded")
    if threshold_record.get("selected_on") not in {"train", "calibration"}:
        raise ValueError("threshold selection provenance not established")
    return True


class FirewallTests(unittest.TestCase):
    def test_same_family_paraphrase_leakage(self):
        partitions = {
            "train": [{"family": "theorem-17", "text": "original"}],
            "test": [{"family": "theorem-17", "text": "paraphrase"}],
        }
        with self.assertRaises(ValueError):
            assert_family_disjoint(partitions)

    def test_disjoint_domains(self):
        partitions = {
            "train": [{"family": "nlp-source-1"}],
            "calibration": [{"family": "math-proof-2"}],
            "test": [{"family": "physics-model-3"}],
        }
        self.assertTrue(assert_family_disjoint(partitions))

    def test_missing_family_rejected(self):
        with self.assertRaises(ValueError):
            assert_family_disjoint({"test": [{"text": "unknown"}]})

    def test_label_dependent_audit_rejected(self):
        rows = [{"family": "a", "score": 0.3, "truth": True}]
        with self.assertRaises(ValueError):
            assert_audit_design_label_blind(rows, ("score", "truth"))
        self.assertTrue(assert_audit_design_label_blind(rows, ("score",)))

    def test_test_tuned_threshold_rejected(self):
        with self.assertRaises(ValueError):
            assert_threshold_provenance({"selected_on": "test", "used_test_labels": True})
        with self.assertRaises(ValueError):
            assert_threshold_provenance({"selected_on": "calibration"})
        self.assertTrue(assert_threshold_provenance(
            {"selected_on": "calibration", "used_test_labels": False}
        ))


if __name__ == "__main__":
    unittest.main()
