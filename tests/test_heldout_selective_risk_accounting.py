"""Synthetic regression checks; not evidence of verifier performance."""
import unittest

from src.heldout_selective_risk_accounting import audit_fixed_decisions


class HeldoutAccountingTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"item_id": "a", "family_id": "f1", "error": True,
             "decisions": {"all": True, "none": False, "safe": False}},
            {"item_id": "b", "family_id": "f2", "error": False,
             "decisions": {"all": True, "none": False, "safe": True}},
        ]

    def test_coverage_and_risk_and_undefined(self):
        result = audit_fixed_decisions(self.rows, ("all", "none", "safe"))
        self.assertEqual(result["families"], 2)
        self.assertEqual(result["methods"]["all"]["selective_risk"], 0.5)
        self.assertEqual(result["methods"]["safe"]["coverage"], 0.5)
        self.assertEqual(result["methods"]["safe"]["selective_risk"], 0.0)
        self.assertIsNone(result["methods"]["none"]["selective_risk"])
        self.assertEqual(result["methods"]["none"]["coverage"], 0.0)

    def test_duplicate_id_rejected(self):
        rows = [self.rows[0], dict(self.rows[0])]
        with self.assertRaises(ValueError):
            audit_fixed_decisions(rows, ("all", "none", "safe"))

    def test_missing_method_rejected(self):
        rows = [dict(self.rows[0]), dict(self.rows[1])]
        rows[1]["decisions"] = {"all": True, "none": False}
        with self.assertRaises(ValueError):
            audit_fixed_decisions(rows, ("all", "none", "safe"))

    def test_nonboolean_error_rejected(self):
        rows = [dict(self.rows[0]), dict(self.rows[1])]
        rows[0]["error"] = 1
        with self.assertRaises(ValueError):
            audit_fixed_decisions(rows, ("all", "none", "safe"))

    def test_nonboolean_acceptance_rejected(self):
        rows = [dict(self.rows[0]), dict(self.rows[1])]
        rows[0]["decisions"] = {"all": 1, "none": False, "safe": False}
        with self.assertRaises(ValueError):
            audit_fixed_decisions(rows, ("all", "none", "safe"))


if __name__ == "__main__":
    unittest.main()
