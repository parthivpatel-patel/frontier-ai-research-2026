"""Protocol 073: cross-check production paired bounds against an independent oracle.

Constructed finite cases only. No physical ground truth or model results.
Run in eligible zero-cost cloud CI: python -m unittest tests.test_protocol_073_crosscheck
"""
import itertools
import unittest

from research.paired_partial_identification import paired_truth_bounds
from tests.test_protocol_072_paired_oracles import sharp_bounds


class ProductionOracleCrosscheck(unittest.TestCase):
    def test_all_small_decision_truth_patterns(self):
        # Exhaustively check 4 decision pairs x 3 truth states per claim.
        # n=1..3 gives 12 + 144 + 1728 constructed inputs.
        choices = list(itertools.product((False, True), repeat=2))
        for n in (1, 2, 3):
            for patterns in itertools.product(
                [(b, c, y) for b, c in choices for y in (False, True, None)],
                repeat=n,
            ):
                baseline = [p[0] for p in patterns]
                candidate = [p[1] for p in patterns]
                truth = [p[2] for p in patterns]
                rows = [
                    {"id": str(i), "source_id": str(i),
                     "baseline": b, "candidate": c, "false_claim": y}
                    for i, (b, c, y) in enumerate(patterns)
                ]
                actual = paired_truth_bounds(rows)
                expected = sharp_bounds(candidate, baseline, truth)
                self.assertEqual(
                    actual["candidate_minus_baseline_unsafe_bounds"],
                    list(expected), msg=f"patterns={patterns}",
                )
                self.assertEqual(
                    actual["strict_improvement_identified"],
                    expected[1] < 0, msg=f"patterns={patterns}",
                )

    def test_duplicate_claim_id_is_rejected(self):
        row = {"id": "same", "source_id": "source", "baseline": True,
               "candidate": False, "false_claim": None}
        with self.assertRaises(ValueError):
            paired_truth_bounds([row, dict(row)])

    def test_source_clustering_is_not_claim_independence(self):
        rows = [
            {"id": str(i), "source_id": "shared", "baseline": True,
             "candidate": False, "false_claim": None}
            for i in range(3)
        ]
        result = paired_truth_bounds(rows)
        self.assertEqual(result["n_source_clusters"], 1)
        self.assertEqual(result["n_claims"], 3)


if __name__ == "__main__":
    unittest.main()
