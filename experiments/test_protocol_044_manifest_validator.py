"""Unit tests for Protocol 044. Run on a standard free cloud runner."""
import unittest
from protocol_044_manifest_validator import validate


def example(id="a", split="train", source_id="s1", model_id="m1"):
    return dict(id=id, split=split, family="mechanics", source_id=source_id,
                claim="bounded trajectory property", ground_truth="verified",
                model_id=model_id)


class ManifestTests(unittest.TestCase):
    def test_valid_disjoint(self):
        self.assertEqual(validate({"examples": [
            example(), example("b", "test", "s2", "m2")]}), [])

    def test_source_leakage(self):
        self.assertTrue(any("source_id" in x for x in validate({"examples": [
            example(), example("b", "test", "s1", "m2")]})))

    def test_model_leakage(self):
        self.assertTrue(any("model_id" in x for x in validate({"examples": [
            example(), example("b", "test", "s2", "m1")]})))

    def test_duplicate_id(self):
        self.assertTrue(any("duplicate id" in x for x in validate({"examples": [
            example(), example("a", "test", "s2", "m2")]})))

    def test_bad_label(self):
        row = example()
        row["ground_truth"] = "probably"
        self.assertTrue(validate({"examples": [row]}))

    def test_empty(self):
        self.assertTrue(validate({"examples": []}))

    def test_missing_fields(self):
        self.assertTrue(validate({"examples": [{"id": "x"}]}))

    def test_bad_root(self):
        self.assertTrue(validate([]))


if __name__ == "__main__":
    unittest.main()
