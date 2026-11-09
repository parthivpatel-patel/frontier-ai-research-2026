"""Prospective regression tests for Protocol 170; execution not yet verified."""
import unittest

from research.protocol_169_calibration_selector import FrozenThreshold
from research.protocol_170_heldout_gate import TestRow, evaluate_heldout


def frozen():
    return {m: FrozenThreshold(m, 0.5, 0.5, 0.5, 2, 2) for m in ("a", "b")}


class HeldoutGateTests(unittest.TestCase):
    def test_matched_coverage_is_only_eligible(self):
        rows = [TestRow("s1", "physics", "v", m, 0.8, True) for m in ("a", "b")]
        rows += [TestRow("s2", "physics", "v", m, 0.2, False) for m in ("a", "b")]
        result = evaluate_heldout(rows, frozen(), {"cal"}, 0.0)
        self.assertEqual(result["comparisons"]["a vs b"]["status"], "ELIGIBLE_FOR_INFERENCE")

    def test_unequal_test_coverage_is_inconclusive(self):
        rows = [TestRow("s1", "physics", "v", "a", 0.8, True),
                TestRow("s1", "physics", "v", "b", 0.8, True),
                TestRow("s2", "physics", "v", "a", 0.8, False),
                TestRow("s2", "physics", "v", "b", 0.2, False)]
        result = evaluate_heldout(rows, frozen(), set(), 0.1)
        self.assertEqual(result["comparisons"]["a vs b"]["status"], "INCONCLUSIVE_AT_MATCHED_COVERAGE")

    def test_source_leakage_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_heldout([TestRow("cal", "p", "v", "a", 0.7, True)], frozen(), {"cal"}, 0.1)

    def test_missing_correctness_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_heldout([TestRow("s", "p", "v", "a", 0.7, None)], frozen(), set(), 0.1)

    def test_paraphrase_weighting(self):
        rows = []
        for m in ("a", "b"):
            rows += [TestRow("s1", "p", str(i), m, 0.9, True) for i in range(9)]
            rows += [TestRow("s2", "p", "v", m, 0.1, False)]
        result = evaluate_heldout(rows, frozen(), set(), 0)
        self.assertEqual(result["methods"]["a"]["coverage"], 0.5)

    def test_all_abstain_accuracy_undefined(self):
        rows = [TestRow("s", "p", "v", m, 0.1, True) for m in ("a", "b")]
        result = evaluate_heldout(rows, frozen(), set(), 0)
        self.assertIsNone(result["methods"]["a"]["conditional_accuracy"])
        self.assertEqual(result["comparisons"]["a vs b"]["status"], "INCONCLUSIVE_AT_MATCHED_COVERAGE")


if __name__ == "__main__":
    unittest.main()
