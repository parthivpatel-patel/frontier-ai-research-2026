"""Synthetic family-shift diagnostic tests; not empirical evidence."""
import unittest

from src.source_family_risk_diagnostics import audit_by_family


class SourceFamilyDiagnosticsTests(unittest.TestCase):
    def test_unequal_family_sizes_change_macro_coverage(self):
        rows = [
            {"item_id": "a", "family_id": "large", "error": False,
             "decisions": {"m": True}},
            {"item_id": "b", "family_id": "large", "error": False,
             "decisions": {"m": True}},
            {"item_id": "c", "family_id": "large", "error": True,
             "decisions": {"m": True}},
            {"item_id": "d", "family_id": "small", "error": True,
             "decisions": {"m": False}},
        ]
        out = audit_by_family(rows, ("m",))
        self.assertEqual(out["pooled"]["methods"]["m"]["coverage"], 0.75)
        self.assertEqual(out["macro"]["m"]["equal_family_coverage"], 0.5)
        self.assertEqual(out["macro"]["m"]["families_with_defined_risk"], 1)
        self.assertIsNone(out["per_family"]["small"]["m"]["selective_risk"])
        self.assertEqual(out["macro"]["m"]["equal_family_risk_defined_only"], 1/3)

    def test_no_accepted_items_keeps_macro_risk_undefined(self):
        rows = [{"item_id": "a", "family_id": "f", "error": True,
                 "decisions": {"m": False}}]
        out = audit_by_family(rows, ("m",))
        self.assertIsNone(out["macro"]["m"]["equal_family_risk_defined_only"])
        self.assertEqual(out["macro"]["m"]["families_with_defined_risk"], 0)

    def test_duplicate_identifiers_rejected_before_family_slicing(self):
        rows = [
            {"item_id": "same", "family_id": f, "error": False,
             "decisions": {"m": True}}
            for f in ("f1", "f2")
        ]
        with self.assertRaises(ValueError):
            audit_by_family(rows, ("m",))


if __name__ == "__main__":
    unittest.main()
