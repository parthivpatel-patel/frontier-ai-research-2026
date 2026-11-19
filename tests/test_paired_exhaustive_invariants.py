"""Exhaustive small-roster algebra checks; synthetic data, no model inference.

Run: python -m unittest tests.test_paired_exhaustive_invariants
Uses only Python standard library; appropriate for a standard free public-repo CI runner.
"""
import itertools
import unittest

from src.paired_fixed_decision_diagnostics import paired_fixed_decisions


class ExhaustivePairedInvariants(unittest.TestCase):
    def test_all_four_item_boolean_rosters(self):
        # Each item has a shared error label and two accept decisions (2^3 states).
        states = list(itertools.product((False, True), repeat=3))
        for configuration in itertools.product(states, repeat=4):
            rows = [
                {"item_id": str(i), "family_id": ("nlp", "math", "physics", "nlp")[i],
                 "error": error, "decisions": {"A": a, "B": b}}
                for i, (error, a, b) in enumerate(configuration)
            ]
            result = paired_fixed_decisions(rows, "A", "B")
            cells = result["decision_cells"]
            errors = result["error_cells"]
            self.assertEqual(sum(cells.values()), 4)
            self.assertEqual(sum(v["items"] for v in result["source_families"].values()), 4)
            self.assertEqual(
                result["coverage_difference_a_minus_b"],
                (cells["a_only"] - cells["b_only"]) / 4,
            )
            a_n = cells["both"] + cells["a_only"]
            b_n = cells["both"] + cells["b_only"]
            a_e = errors["both"] + errors["a_only"]
            b_e = errors["both"] + errors["b_only"]
            expected = a_e / a_n - b_e / b_n if a_n and b_n else None
            self.assertEqual(result["selective_risk_difference_a_minus_b"], expected)
            if a_n == b_n and a_n:
                # Common accepted errors cancel ONLY at exactly equal accepted counts.
                self.assertAlmostEqual(
                    expected, (errors["a_only"] - errors["b_only"]) / a_n
                )

    def test_method_swap_antisymmetry(self):
        rows = [
            {"item_id": "1", "family_id": "nlp", "error": True,
             "decisions": {"A": True, "B": False}},
            {"item_id": "2", "family_id": "math", "error": False,
             "decisions": {"A": False, "B": True}},
            {"item_id": "3", "family_id": "physics", "error": True,
             "decisions": {"A": True, "B": True}},
        ]
        ab = paired_fixed_decisions(rows, "A", "B")
        ba = paired_fixed_decisions(rows, "B", "A")
        self.assertAlmostEqual(ab["coverage_difference_a_minus_b"],
                               -ba["coverage_difference_a_minus_b"])
        self.assertAlmostEqual(ab["selective_risk_difference_a_minus_b"],
                               -ba["selective_risk_difference_a_minus_b"])


if __name__ == "__main__":
    unittest.main()
