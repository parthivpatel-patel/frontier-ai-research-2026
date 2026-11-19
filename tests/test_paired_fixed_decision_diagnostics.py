"""Synthetic regression checks for descriptive paired decisions (no model runs)."""
import unittest

from src.paired_fixed_decision_diagnostics import paired_fixed_decisions


def row(i, family, error, a, b):
    return {"item_id": str(i), "family_id": family, "error": error,
            "decisions": {"A": a, "B": b}}


class PairedDiagnosticsTests(unittest.TestCase):
    def test_discordant_and_shared_cells(self):
        rows = [row(1, "nlp", True, True, True),
                row(2, "nlp", False, True, False),
                row(3, "math", True, False, True),
                row(4, "physics", False, False, False)]
        x = paired_fixed_decisions(rows, "A", "B")
        self.assertEqual(x["decision_cells"], {"both": 1, "a_only": 1, "b_only": 1, "neither": 1})
        self.assertEqual(x["error_cells"], {"both": 1, "a_only": 0, "b_only": 1})
        self.assertEqual(x["coverage_difference_a_minus_b"], 0)
        self.assertEqual(x["selective_risk_difference_a_minus_b"], -0.5)
        self.assertEqual(x["source_families"]["physics"]["neither"], 1)

    def test_all_abstain_is_undefined(self):
        x = paired_fixed_decisions([row(1, "math", True, False, False)], "A", "B")
        self.assertIsNone(x["both_accepted_error_rate"])
        self.assertIsNone(x["selective_risk_difference_a_minus_b"])

    def test_order_invariance(self):
        rows = [row(1, "nlp", False, True, False), row(2, "math", True, False, True)]
        self.assertEqual(paired_fixed_decisions(rows, "A", "B"),
                         paired_fixed_decisions(list(reversed(rows)), "A", "B"))

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            paired_fixed_decisions([row(1, "nlp", False, True, True),
                                    row(1, "math", True, False, False)], "A", "B")

    def test_identical_methods_rejected(self):
        with self.assertRaises(ValueError):
            paired_fixed_decisions([row(1, "nlp", False, True, True)], "A", "A")

    def test_non_boolean_rejected(self):
        with self.assertRaises(ValueError):
            paired_fixed_decisions([row(1, "nlp", False, 1, True)], "A", "B")


if __name__ == "__main__":
    unittest.main()
