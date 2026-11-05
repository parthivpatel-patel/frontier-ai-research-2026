"""Protocol 078: production integration for selective-adjudication controls.

Constructed counterexamples, not model or physics observations. Standard library.
The hidden oracle labels are used only to construct fixtures, never supplied to
the production estimator when independent adjudication is absent.
"""
import unittest
from fractions import Fraction

from research.paired_partial_identification import paired_truth_bounds


def record(i, a, b, hidden_truth, adjudicated):
    return {
        "id": f"synthetic-{i}", "source_id": f"synthetic-{i}",
        "baseline": a, "candidate": b,
        "false_claim": bool(hidden_truth) if adjudicated else None,
    }


class Protocol078Integration(unittest.TestCase):
    def test_selective_adjudication_cannot_establish_direction(self):
        # Both systems truly accept two unsafe and two safe claims.
        # A's safe outcomes and B's unsafe outcomes are selectively visible.
        specification = [
            (1, 0, 0, True), (1, 0, 0, True),
            (1, 0, 1, False), (1, 0, 1, False),
            (0, 1, 0, False), (0, 1, 0, False),
            (0, 1, 1, True), (0, 1, 1, True),
        ]
        rows = [record(i, *entry) for i, entry in enumerate(specification)]
        result = paired_truth_bounds(rows)
        lo, hi = result["candidate_minus_baseline_unsafe_bounds"]
        self.assertLess(lo, 0)
        self.assertGreater(hi, 0)
        self.assertFalse(result["strict_improvement_identified"])
        self.assertEqual(result["baseline_coverage"], result["candidate_coverage"])

    def test_shared_unknown_truth_cancels_in_difference(self):
        result = paired_truth_bounds([
            record(0, True, True, 1, False),
            record(1, False, False, 0, False),
        ])
        self.assertEqual(result["candidate_minus_baseline_unsafe_bounds"], [0, 0])

    def test_equal_coverage_with_unknown_disagreement_is_ambiguous(self):
        result = paired_truth_bounds([
            record(0, True, False, 1, False),
            record(1, False, True, 0, False),
        ])
        self.assertEqual(result["candidate_minus_baseline_unsafe_bounds"],
                         [-0.5, 0.5])
        self.assertFalse(result["strict_improvement_identified"])

    def test_complete_adjudication_identifies_difference(self):
        result = paired_truth_bounds([
            record(0, True, False, 1, True),
            record(1, False, True, 0, True),
        ])
        self.assertEqual(result["candidate_minus_baseline_unsafe_bounds"],
                         [-0.5, -0.5])
        self.assertTrue(result["strict_improvement_identified"])

    def test_truth_not_exposed_by_fixture(self):
        row = record(0, True, False, 1, False)
        self.assertIsNone(row["false_claim"])


if __name__ == "__main__":
    unittest.main()
