"""Protocol 049: regression controls for the frozen-threshold evaluator.

Run on a verified no-cost cloud runner:
    python -m unittest discover -s tests -p 'test_protocol_049*.py' -v
These are authored tests; their existence is not evidence of a passing run.
"""
import importlib.util
import math
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "experiments" / "protocol_048_frozen_threshold.py"
SPEC = importlib.util.spec_from_file_location("protocol_048_frozen_threshold", MODULE_PATH)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def row(identifier, split, group, label, score):
    return {"id": identifier, "split": split, "group": group,
            "label": label, "certificate": score}


class FrozenThresholdControls(unittest.TestCase):
    def test_frozen_threshold_and_distribution_shift(self):
        rows = [row("v1", "validation", "v1", 0, .9),
                row("v2", "validation", "v2", 1, .7),
                row("v3", "validation", "v3", 0, .5),
                row("v4", "validation", "v4", 1, .1),
                row("t1", "test", "t1", 1, .8),
                row("t2", "test", "t2", 0, .6)]
        result = mod.evaluate(rows, ("certificate",), (.5,))[0]
        self.assertEqual(result["frozen_threshold"], .7)
        self.assertEqual(result["accepted_count"], 1)
        self.assertEqual(result["test_coverage"], .5)
        self.assertEqual(result["selective_risk"], 1.)

    def test_validation_ties_are_not_split(self):
        val = [row("v1", "validation", "v1", 0, .9),
               row("v2", "validation", "v2", 0, .9),
               row("v3", "validation", "v3", 1, .2)]
        self.assertEqual(mod.fit_threshold(val, "certificate", 1/3), .9)
        self.assertEqual(sum(r["certificate"] >= .9 for r in val), 2)

    def test_empty_test_acceptance_has_undefined_risk(self):
        rows = [row("v1", "validation", "v1", 0, .9),
                row("v2", "validation", "v2", 1, .1),
                row("t1", "test", "t1", 1, .3)]
        result = mod.evaluate(rows, ("certificate",), (.5,))[0]
        self.assertEqual(result["accepted_count"], 0)
        self.assertEqual(result["test_coverage"], 0)
        self.assertIsNone(result["selective_risk"])

    def test_group_leakage_rejected(self):
        rows = [row("v1", "validation", "shared", 0, .9),
                row("t1", "test", "shared", 1, .2)]
        with self.assertRaisesRegex(ValueError, "group leakage"):
            mod.evaluate(rows, ("certificate",))

    def test_duplicate_id_rejected(self):
        rows = [row("same", "validation", "v", 0, .9),
                row("same", "test", "t", 1, .2)]
        with self.assertRaisesRegex(ValueError, "duplicate id"):
            mod.evaluate(rows, ("certificate",))

    def test_invalid_scores_rejected(self):
        for bad in (float("nan"), float("inf"), -0.01, 1.01, True):
            with self.subTest(score=repr(bad)):
                rows = [row("v1", "validation", "v", 0, bad),
                        row("t1", "test", "t", 1, .2)]
                with self.assertRaisesRegex(ValueError, "invalid confidence"):
                    mod.evaluate(rows, ("certificate",))

    def test_invalid_coverage_rejected(self):
        val = [row("v1", "validation", "v", 0, .9)]
        for target in (0, -0.1, 1.1):
            with self.subTest(target=target):
                with self.assertRaises(ValueError):
                    mod.fit_threshold(val, "certificate", target)

    def test_test_labels_cannot_change_threshold(self):
        rows = [row("v1", "validation", "v1", 0, .8),
                row("v2", "validation", "v2", 1, .4),
                row("t1", "test", "t1", 0, .6)]
        original = mod.evaluate(rows, ("certificate",), (.5,))[0]
        rows[-1]["label"] = 1
        changed = mod.evaluate(rows, ("certificate",), (.5,))[0]
        self.assertEqual(original["frozen_threshold"], changed["frozen_threshold"])
        self.assertEqual(original["accepted_count"], changed["accepted_count"])


if __name__ == "__main__":
    unittest.main()
