"""Protocol 109: executable accounting for Protocol 107 cross-oracle coverage.

Standard-library-only. Counting replaces the expensive compare method with a
recorder; it does NOT execute either optimization oracle or claim they pass.
Run on an approved free cloud runner, never on the user's laptop.
"""
import unittest
from unittest.mock import patch

from test_protocol_107_cross_oracle import CrossOracleTests


class CrossOracleCoverageAccounting(unittest.TestCase):
    def test_comparison_case_counts_and_uniqueness(self):
        recorded = []
        suite = CrossOracleTests()
        def record(self, costs, budget, worlds):
            # Canonicalize the rational world table; keep zero-mass worlds.
            signature = (tuple(costs), budget, tuple(sorted(worlds.items())))
            recorded.append(signature)

        # patch.object installs a function descriptor on the class; calls bind
        # the CrossOracleTests instance as the first argument.
        with patch.object(CrossOracleTests, "compare", record):
            suite.test_one_claim_extreme_and_fractional()
            self.assertEqual(len(recorded), 12)
            suite.test_two_claim_joint_distributions()
            self.assertEqual(len(recorded), 57)
            suite.test_three_claim_sparse_correlated()
            self.assertEqual(len(recorded), 58)

        self.assertEqual(len(set(recorded)), 58, "duplicate optimization cases")
        self.assertEqual(sum(len(x[0]) == 1 for x in recorded), 12)
        self.assertEqual(sum(len(x[0]) == 2 for x in recorded), 45)
        self.assertEqual(sum(len(x[0]) == 3 for x in recorded), 1)

    def test_stop_witness_not_counted_as_cross_oracle_case(self):
        # STOP's legal-but-suboptimal assertion is a separate test method.
        self.assertTrue(hasattr(CrossOracleTests, "test_suboptimal_legal_stop_witness"))


if __name__ == "__main__":
    unittest.main()
