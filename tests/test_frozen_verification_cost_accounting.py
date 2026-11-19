"""Synthetic checks; no empirical verifier results are claimed."""
import unittest
from src.frozen_verification_cost_accounting import audit_verification_costs


class FrozenCostTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"item_id": "x", "family_id": "nlp", "error": False,
             "decisions": {"A": True, "B": False}},
            {"item_id": "y", "family_id": "physics", "error": True,
             "decisions": {"A": False, "B": True}},
        ]
        self.costs = {"A": {"x": 1.0, "y": 3.0},
                      "B": {"x": 2.0, "y": 2.0}}

    def test_full_roster_includes_abstentions(self):
        out = audit_verification_costs(self.rows, ("A", "B"), self.costs, "seconds")
        self.assertEqual(out["methods"]["A"]["total"], 4.0)
        self.assertEqual(out["methods"]["B"]["total"], 4.0)
        self.assertEqual(out["methods"]["A"]["selective_risk"], 0.0)
        self.assertEqual(out["methods"]["B"]["selective_risk"], 1.0)

    def test_missing_cost_rejected(self):
        costs = {"A": {"x": 1.0}, "B": self.costs["B"]}
        with self.assertRaises(ValueError):
            audit_verification_costs(self.rows, ("A", "B"), costs, "seconds")

    def test_extra_cost_rejected(self):
        costs = {"A": {**self.costs["A"], "z": 0.0}, "B": self.costs["B"]}
        with self.assertRaises(ValueError):
            audit_verification_costs(self.rows, ("A", "B"), costs, "seconds")

    def test_invalid_values_rejected(self):
        for bad in (float("nan"), float("inf"), -1.0, True, "2"):
            costs = {"A": {"x": bad, "y": 3.0}, "B": self.costs["B"]}
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                audit_verification_costs(self.rows, ("A", "B"), costs, "seconds")

    def test_empty_unit_rejected(self):
        with self.assertRaises(ValueError):
            audit_verification_costs(self.rows, ("A", "B"), self.costs, "")


if __name__ == "__main__":
    unittest.main()
