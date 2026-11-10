"""Adversarial synthetic fixtures for Protocol 183. No model inference.

Run on an independently verified zero-charge cloud runner:
python -m unittest discover -s research -p 'test_protocol_183_integrity_validator.py'
"""
import copy
import hashlib
import json
import unittest

from protocol_183_integrity_validator import validate, strict_json, canonical


def sha(data):
    return hashlib.sha256(data).hexdigest()


def arm(invariant, links):
    transmitted = canonical({"invariant": invariant, "links": links}).decode("utf-8")
    return {
        "invariant": copy.deepcopy(invariant),
        "links": copy.deepcopy(links),
        "full_input_utf8": transmitted,
        "invariant_prompt_sha256": sha(canonical(invariant)),
        "intervention_payload_sha256": sha(canonical(links)),
        "full_input_sha256": sha(transmitted.encode()),
        "blinded_input_artifact_sha256": sha(transmitted.encode()),
    }


def fixture():
    invariant = {
        "problem": "Synthetic dimensional-consistency check, not an observation",
        "allowed_target_ids": ["constraint_A", "constraint_B"],
        "tolerance": 0.001,
    }
    correct = [{"source": "step_1", "target": "constraint_A",
                "type": "depends_on", "scope": "step"}]
    shuffled = [{"source": "step_1", "target": "constraint_B",
                 "type": "depends_on", "scope": "step"}]
    return {"schema_version": "183.1",
            "assignment": {"synthetic_1": ["correct", "matched_shuffle"]},
            "pairs": [{"item_key": "synthetic_1", "arms": {
                "correct": arm(invariant, correct),
                "matched_shuffle": arm(invariant, shuffled)}}]}


class IntegrityTests(unittest.TestCase):
    def assert_rejected(self, doc):
        with self.assertRaises((ValueError, TypeError, KeyError)):
            validate(doc)

    def test_valid_structural_fixture(self):
        self.assertEqual(validate(fixture())["accepted_pairs"], 1)

    def test_duplicate_json_keys(self):
        with self.assertRaises(ValueError):
            strict_json('{"a":1,"a":2}')

    def test_nonfinite_json(self):
        with self.assertRaises(ValueError):
            strict_json('{"x":NaN}')

    def test_same_payload_not_delivered(self):
        doc = fixture()
        doc["pairs"][0]["arms"]["matched_shuffle"] = copy.deepcopy(
            doc["pairs"][0]["arms"]["correct"])
        self.assert_rejected(doc)

    def test_changed_tolerance_even_with_rehashed_artifacts(self):
        doc = fixture()
        changed = doc["pairs"][0]["arms"]["matched_shuffle"]
        changed["invariant"]["tolerance"] = 0.1
        doc["pairs"][0]["arms"]["matched_shuffle"] = arm(
            changed["invariant"], changed["links"])
        self.assert_rejected(doc)

    def test_out_of_universe_target(self):
        doc = fixture()
        a = doc["pairs"][0]["arms"]["matched_shuffle"]
        a["links"][0]["target"] = "not_a_constraint"
        doc["pairs"][0]["arms"]["matched_shuffle"] = arm(a["invariant"], a["links"])
        self.assert_rejected(doc)

    def test_changed_scope(self):
        doc = fixture()
        a = doc["pairs"][0]["arms"]["matched_shuffle"]
        a["links"][0]["scope"] = "document"
        doc["pairs"][0]["arms"]["matched_shuffle"] = arm(a["invariant"], a["links"])
        self.assert_rejected(doc)

    def test_leaked_gold_label_field(self):
        doc = fixture()
        a = doc["pairs"][0]["arms"]["correct"]
        a["invariant"]["gold_label"] = "valid"
        doc["pairs"][0]["arms"]["correct"] = arm(a["invariant"], a["links"])
        self.assert_rejected(doc)

    def test_missing_transmitted_artifact(self):
        doc = fixture()
        del doc["pairs"][0]["arms"]["correct"]["full_input_utf8"]
        self.assert_rejected(doc)

    def test_wrong_hash(self):
        doc = fixture()
        doc["pairs"][0]["arms"]["correct"]["full_input_sha256"] = "0" * 64
        self.assert_rejected(doc)

    def test_unregistered_attrition(self):
        doc = fixture()
        doc["assignment"]["missing_2"] = ["correct", "matched_shuffle"]
        self.assert_rejected(doc)

    def test_duplicate_item(self):
        doc = fixture()
        doc["pairs"].append(copy.deepcopy(doc["pairs"][0]))
        self.assert_rejected(doc)

    @unittest.expectedFailure
    def test_manifest_must_be_cryptographically_bound(self):
        # Known gap: current validator trusts mutable in-document assignment.
        doc = fixture()
        doc["assignment"] = {"synthetic_1": ["correct", "matched_shuffle"]}
        self.assert_rejected(doc)

    @unittest.expectedFailure
    def test_nested_answer_leakage_must_be_rejected(self):
        # Known gap: top-level denylist does not inspect nested visible content.
        doc = fixture()
        for condition in ("correct", "matched_shuffle"):
            a = doc["pairs"][0]["arms"][condition]
            a["invariant"]["metadata"] = {"gold_answer": "yes"}
            doc["pairs"][0]["arms"][condition] = arm(a["invariant"], a["links"])
        self.assert_rejected(doc)


if __name__ == "__main__":
    unittest.main()
