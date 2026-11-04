"""Constructed mathematical controls, not empirical physics results."""
import unittest
from research.paired_partial_identification import paired_truth_bounds


def row(i, b, c, y, source=None):
    return {"id": str(i), "source_id": source or str(i),
            "baseline": b, "candidate": c, "false_claim": y}


class PairedPartialIdentificationTests(unittest.TestCase):
    def test_protocol_057_falsification(self):
        result = paired_truth_bounds([
            row(1, True, False, True), row(2, True, True, False),
            row(3, False, True, None), row(4, True, False, None)])
        self.assertEqual(result["candidate_minus_baseline_unsafe_bounds"], [-0.5, 0.0])
        self.assertFalse(result["strict_improvement_identified"])

    def test_identical_decisions_cancel_unknown_truth(self):
        result = paired_truth_bounds([row(1, True, True, None)])
        self.assertEqual(result["candidate_minus_baseline_unsafe_bounds"], [0, 0])
        self.assertEqual(result["baseline_unsafe_bounds"], [0, 1])

    def test_all_unknown_opposing(self):
        result = paired_truth_bounds([row(1, True, False, None),
                                      row(2, False, True, None)])
        self.assertEqual(result["candidate_minus_baseline_unsafe_bounds"], [-0.5, 0.5])

    def test_fully_known_point_identified(self):
        result = paired_truth_bounds([row(1, True, False, True),
                                      row(2, True, True, False)])
        self.assertEqual(result["candidate_minus_baseline_unsafe_bounds"], [-0.5, -0.5])
        self.assertTrue(result["strict_improvement_identified"])

    def test_reject_all_has_no_accepted_error_denominator(self):
        result = paired_truth_bounds([row(1, False, False, None)])
        self.assertIsNone(result["observed_only_error_among_accepted"]["candidate"])
        self.assertEqual(result["candidate_coverage"], 0)

    def test_duplicate_id_rejected(self):
        with self.assertRaises(ValueError):
            paired_truth_bounds([row(1, True, False, None),
                                 row(1, False, True, True)])

    def test_invalid_truth_rejected(self):
        with self.assertRaises(ValueError):
            paired_truth_bounds([row(1, True, False, 1)])

    def test_source_clusters_counted_without_false_independence(self):
        result = paired_truth_bounds([row(1, True, False, True, "paperA"),
                                      row(2, True, False, True, "paperA")])
        self.assertEqual(result["n_source_clusters"], 1)


if __name__ == "__main__":
    unittest.main()
