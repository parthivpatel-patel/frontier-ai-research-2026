"""Prospective regression tests for Protocol 169. Not yet run."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "protocol_169", Path(__file__).resolve().parents[1] / "research" / "protocol_169_calibration_selector.py"
)
module = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)
Row = module.CalibrationRow
freeze = module.freeze_thresholds


class CalibrationSelectorTests(unittest.TestCase):
    def test_equal_source_weighting(self):
        rows = [Row("a", "f1", str(i), "m", 0.9) for i in range(20)]
        rows.append(Row("b", "f2", "0", "m", 0.1))
        result = freeze(rows, 0.5)["m"]
        self.assertEqual(result.threshold, 0.9)
        self.assertEqual(result.achieved_coverage, 0.5)

    def test_tied_scores_prefer_lower_coverage(self):
        rows = [Row("a", "f", "0", "m", 0.5), Row("b", "f", "0", "m", 0.5)]
        result = freeze(rows, 0.5)["m"]
        self.assertEqual(result.threshold, float("inf"))
        self.assertEqual(result.achieved_coverage, 0.0)

    def test_all_answer(self):
        rows = [Row("a", "f", "0", "m", -3)]
        self.assertEqual(freeze(rows, 1)["m"].achieved_coverage, 1)

    def test_missing_method_row_rejected(self):
        rows = [Row("a", "f", "0", "m", 0.1), Row("a", "f", "0", "n", 0.2),
                Row("b", "f", "0", "m", 0.3)]
        with self.assertRaises(ValueError):
            freeze(rows, 0.5)

    def test_duplicate_and_nonfinite_rejected(self):
        row = Row("a", "f", "0", "m", 0.5)
        with self.assertRaises(ValueError):
            freeze([row, row], 0.5)
        with self.assertRaises(ValueError):
            freeze([Row("a", "f", "0", "m", float("nan"))], 0.5)

    def test_source_family_inconsistency_rejected(self):
        with self.assertRaises(ValueError):
            freeze([Row("a", "f1", "0", "m", 0.1),
                    Row("a", "f2", "1", "m", 0.2)], 0.5)


if __name__ == "__main__":
    unittest.main()
