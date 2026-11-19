"""Synthetic regression checks; no empirical results."""
import unittest
from src.prospective_budget_equivalence import audit_budget_equivalence


class BudgetGateTests(unittest.TestCase):
    def audit(self, a, b):
        return {"unit": "tokens", "methods": {"A": {"total": a}, "B": {"total": b}}}

    def test_equal_nonzero_costs_pass(self):
        out = audit_budget_equivalence(self.audit(100, 100), "A", "B")
        self.assertTrue(out["passes_measured_budget_gate"])
        self.assertEqual(out["relative_gap"], 0)

    def test_boundary_and_outside(self):
        self.assertTrue(audit_budget_equivalence(self.audit(95, 100), "A", "B")["passes_measured_budget_gate"])
        self.assertFalse(audit_budget_equivalence(self.audit(94, 100), "A", "B")["passes_measured_budget_gate"])

    def test_zero_zero_is_uninformative(self):
        out = audit_budget_equivalence(self.audit(0, 0), "A", "B")
        self.assertIsNone(out["relative_gap"])
        self.assertFalse(out["passes_measured_budget_gate"])
        self.assertTrue(out["uninformative_zero_cost"])

    def test_one_zero_fails(self):
        self.assertFalse(audit_budget_equivalence(self.audit(0, 10), "A", "B")["passes_measured_budget_gate"])

    def test_symmetric(self):
        x = audit_budget_equivalence(self.audit(80, 100), "A", "B")
        y = audit_budget_equivalence(self.audit(80, 100), "B", "A")
        self.assertEqual(x["relative_gap"], y["relative_gap"])

    def test_bad_tolerances(self):
        for value in (-0.1, 1, True, float("nan"), float("inf"), "0.05"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                audit_budget_equivalence(self.audit(100, 100), "A", "B", value)

    def test_bad_totals_and_names(self):
        for value in (-1, True, float("inf"), float("nan"), "10"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                audit_budget_equivalence(self.audit(value, 10), "A", "B")
        with self.assertRaises(ValueError):
            audit_budget_equivalence(self.audit(1, 1), "A", "A")
        with self.assertRaises(ValueError):
            audit_budget_equivalence(self.audit(1, 1), "A", "C")


if __name__ == "__main__":
    unittest.main()
