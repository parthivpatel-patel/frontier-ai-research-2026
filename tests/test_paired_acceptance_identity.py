"""Algebraic identity regression tests on synthetic paired decisions only.

Run with: python -m unittest tests.test_paired_acceptance_identity
No model inference, network access, or third-party dependencies.
"""
import unittest

from src.paired_fixed_decision_diagnostics import paired_fixed_decisions


def item(i, family, error, a, b):
    return {"item_id": str(i), "family_id": family, "error": error,
            "decisions": {"A": a, "B": b}}


class PairedAcceptanceIdentityTests(unittest.TestCase):
    def test_equal_coverage_discordant_error_identity(self):
        rows = (
            [item(i, "nlp", i < 3, True, True) for i in range(40)]
            + [item(40 + i, "math", i < 8, True, False) for i in range(10)]
            + [item(50 + i, "physics", i < 2, False, True) for i in range(10)]
            + [item(60 + i, "physics", False, False, False) for i in range(40)]
        )
        result = paired_fixed_decisions(rows, "A", "B")
        cells = result["decision_cells"]
        errors = result["error_cells"]
        self.assertEqual(cells, {"both": 40, "a_only": 10, "b_only": 10, "neither": 40})
        self.assertEqual(result["coverage_difference_a_minus_b"], 0.0)
        expected = (errors["a_only"] - errors["b_only"]) / (cells["both"] + cells["a_only"])
        self.assertAlmostEqual(expected, 0.12)
        self.assertAlmostEqual(result["selective_risk_difference_a_minus_b"], expected)

    def test_equal_acceptance_sets_force_equal_risk(self):
        rows = [item(1, "nlp", True, True, True),
                item(2, "math", False, True, True),
                item(3, "physics", True, False, False)]
        result = paired_fixed_decisions(rows, "A", "B")
        self.assertEqual(result["decision_cells"]["a_only"], 0)
        self.assertEqual(result["decision_cells"]["b_only"], 0)
        self.assertEqual(result["selective_risk_difference_a_minus_b"], 0.0)

    def test_shared_error_changes_absolute_risks_not_difference(self):
        def roster(shared_error):
            return [item(1, "nlp", shared_error, True, True),
                    item(2, "math", True, True, False),
                    item(3, "physics", False, False, True)]
        a = paired_fixed_decisions(roster(False), "A", "B")
        b = paired_fixed_decisions(roster(True), "A", "B")
        self.assertEqual(a["selective_risk_difference_a_minus_b"],
                         b["selective_risk_difference_a_minus_b"])
        self.assertNotEqual(a["marginal"]["A"]["selective_risk"],
                            b["marginal"]["A"]["selective_risk"])

    def test_unequal_coverage_does_not_use_equal_coverage_formula(self):
        rows = [item(1, "nlp", True, True, True),
                item(2, "math", False, True, False)]
        result = paired_fixed_decisions(rows, "A", "B")
        self.assertNotEqual(result["coverage_difference_a_minus_b"], 0)
        self.assertNotEqual(result["selective_risk_difference_a_minus_b"],
                            result["error_cells"]["a_only"] - result["error_cells"]["b_only"])

    def test_all_abstain_risk_is_undefined(self):
        result = paired_fixed_decisions([item(1, "physics", True, False, False)], "A", "B")
        self.assertIsNone(result["selective_risk_difference_a_minus_b"])
        self.assertIsNone(result["marginal"]["A"]["selective_risk"])


if __name__ == "__main__":
    unittest.main()
