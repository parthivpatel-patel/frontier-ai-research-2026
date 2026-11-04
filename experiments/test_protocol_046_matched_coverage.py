"""Regression tests for Protocol 046. Execute on a confirmed free cloud runner."""
import unittest
from experiments.protocol_046_matched_coverage import evaluate


def sample():
    return {"examples": [
        {"id": "v1", "group_id": "g1", "split": "validation", "ground_truth": "verified",
         "methods": {"base": {"score": 0.9, "decision": "verified"}, "cert": {"score": 0.8, "decision": "verified"}}},
        {"id": "v2", "group_id": "g2", "split": "validation", "ground_truth": "falsified",
         "methods": {"base": {"score": 0.8, "decision": "verified"}, "cert": {"score": 0.9, "decision": "falsified"}}},
        {"id": "t1", "group_id": "g3", "split": "test", "ground_truth": "inconclusive",
         "methods": {"base": {"score": 0.9, "decision": "verified"}, "cert": {"score": 0.1, "decision": "inconclusive"}}},
        {"id": "t2", "group_id": "g4", "split": "test", "ground_truth": "verified",
         "methods": {"base": {"score": 0.8, "decision": "verified"}, "cert": {"score": 0.9, "decision": "verified"}}},
    ]}


class MatchedCoverageTests(unittest.TestCase):
    def test_equal_counts_and_unsafe_abstention(self):
        result = evaluate(sample(), 0.5)
        test = result["splits"]["test"]
        self.assertEqual(test["base"]["accepted"], test["cert"]["accepted"])
        self.assertEqual(test["base"]["unsafe"], 1)
        self.assertEqual(test["cert"]["unsafe"], 0)

    def test_group_leakage_rejected(self):
        data = sample()
        data["examples"][-1]["group_id"] = "g1"
        with self.assertRaisesRegex(ValueError, "leakage"):
            evaluate(data, 0.5)

    def test_nan_rejected(self):
        data = sample()
        data["examples"][0]["methods"]["base"]["score"] = float("nan")
        with self.assertRaisesRegex(ValueError, "score"):
            evaluate(data, 0.5)

    def test_missing_method_rejected(self):
        data = sample()
        del data["examples"][0]["methods"]["base"]
        with self.assertRaisesRegex(ValueError, "identical"):
            evaluate(data, 0.5)

    def test_duplicate_id_rejected(self):
        data = sample()
        data["examples"][1]["id"] = "v1"
        with self.assertRaisesRegex(ValueError, "id"):
            evaluate(data, 0.5)

    def test_zero_selection_rejected(self):
        with self.assertRaisesRegex(ValueError, "zero"):
            evaluate(sample(), 0.1)


if __name__ == "__main__":
    unittest.main()
