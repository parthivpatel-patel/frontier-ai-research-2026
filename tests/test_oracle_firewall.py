"""Protocol 022: constructed oracle-firewall and source-grouping tests."""
import copy
import unittest

from src.oracle_firewall import (
    CASE_FIELDS, constructed_identifiability_warning, prepare_cases,
    score_frozen_test, validate_splits,
)


def fixture():
    cases = [
        {"case_id": "a1", "source_family_id": "A", "trial_slot": 1,
         "instruction": "Eventually reach x", "candidate_formula": "F x",
         "assumption_family_id": "physical-v1"},
        {"case_id": "a2", "source_family_id": "A", "trial_slot": 2,
         "instruction": "Never reach y", "candidate_formula": "G !y",
         "assumption_family_id": "physical-v1"},
        {"case_id": "b1", "source_family_id": "B", "trial_slot": 1,
         "instruction": "Reach z", "candidate_formula": "F z",
         "assumption_family_id": "physical-v2"},
        {"case_id": "c1", "source_family_id": "C", "trial_slot": 1,
         "instruction": "Avoid w", "candidate_formula": "G !w",
         "assumption_family_id": "physical-v2"},
    ]
    splits = {"A": "test", "B": "test", "C": "train"}
    decisions = [{"case_id": "a1", "accept": True},
                 {"case_id": "a2", "accept": True},
                 {"case_id": "b1", "accept": False}]
    gold = [{"case_id": "a1", "correct": True},
            {"case_id": "a2", "correct": False},
            {"case_id": "b1", "correct": False}]
    return cases, splits, decisions, gold


class OracleFirewallTests(unittest.TestCase):
    def test_exact_verifier_fields(self):
        cases, _, _, _ = fixture()
        self.assertEqual(set(cases[0]), CASE_FIELDS)
        self.assertEqual(len(prepare_cases(cases)), 4)

    def test_rejects_gold_in_verifier_input(self):
        cases, _, _, _ = fixture()
        for key in ("correct", "gold", "ground_truth", "tl",
                    "label", "good_trace", "bad_trace"):
            altered = copy.deepcopy(cases)
            altered[0][key] = True
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "fields"):
                prepare_cases(altered)

    def test_rejects_missing_verifier_field(self):
        cases, _, _, _ = fixture()
        del cases[0]["instruction"]
        with self.assertRaisesRegex(ValueError, "fields"):
            prepare_cases(cases)

    def test_rejects_duplicate_case_id(self):
        cases, _, _, _ = fixture()
        cases[1]["case_id"] = "a1"
        with self.assertRaisesRegex(ValueError, "duplicate case_id"):
            prepare_cases(cases)

    def test_rejects_duplicate_family_trial(self):
        cases, _, _, _ = fixture()
        cases[1]["trial_slot"] = 1
        with self.assertRaisesRegex(ValueError, "trial slot"):
            prepare_cases(cases)

    def test_rejects_boolean_and_nonpositive_trial(self):
        cases, _, _, _ = fixture()
        for slot in (True, False, 0, -1, 1.0, "1"):
            altered = copy.deepcopy(cases)
            altered[0]["trial_slot"] = slot
            with self.subTest(slot=slot), self.assertRaisesRegex(ValueError, "trial_slot"):
                prepare_cases(altered)

    def test_rejects_invalid_identifiers_and_text(self):
        cases, _, _, _ = fixture()
        for field, value in (("case_id", " a1"), ("source_family_id", ""),
                             ("assumption_family_id", None),
                             ("instruction", " "), ("candidate_formula", 3)):
            altered = copy.deepcopy(cases)
            altered[0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                prepare_cases(altered)

    def test_rejects_empty_and_bad_collection(self):
        for value in ([], (), {}, None, "not cases"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                prepare_cases(value)

    def test_isolated_copy_prevents_mutation_alias(self):
        cases, _, _, _ = fixture()
        prepared = prepare_cases(cases)
        cases[0]["instruction"] = "mutated"
        self.assertEqual(prepared[0]["instruction"], "Eventually reach x")

    def test_source_split_counts(self):
        cases, splits, _, _ = fixture()
        self.assertEqual(validate_splits(prepare_cases(cases), splits),
                         {"train": 1, "calibration": 0, "test": 2})

    def test_rejects_missing_extra_and_invalid_split(self):
        cases, splits, _, _ = fixture()
        for bad in ({"A": "test", "B": "test"},
                    {**splits, "D": "test"},
                    {**splits, "A": "validation"},
                    {"A": "train", "B": "calibration", "C": "train"}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                validate_splits(prepare_cases(cases), bad)

    def test_correct_case_and_source_risk(self):
        cases, splits, decisions, gold = fixture()
        r = score_frozen_test(cases, splits, decisions, gold)
        self.assertTrue(r["test_only"])
        self.assertEqual(r["test_cases"], 3)
        self.assertEqual(r["test_source_families"], 2)
        self.assertEqual(r["accepted_cases"], 2)
        self.assertEqual(r["unsafe_accepted_cases"], 1)
        self.assertAlmostEqual(r["case_coverage"], 2 / 3)
        self.assertAlmostEqual(r["conditional_error_among_accepted"], .5)
        self.assertAlmostEqual(r["case_unsafe_acceptance_rate"], 1 / 3)
        self.assertEqual(r["accepted_source_families"], 1)
        self.assertEqual(r["unsafe_accepted_source_families"], 1)
        self.assertEqual(r["source_family_unsafe_acceptance_rate"], .5)
        self.assertFalse(r["independent_human_adjudication_verified"])

    def test_rejects_missing_or_extra_decisions(self):
        cases, splits, decisions, gold = fixture()
        for bad in (decisions[:-1], decisions + [{"case_id": "c1", "accept": True}]):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, "exactly match"):
                score_frozen_test(cases, splits, bad, gold)

    def test_rejects_missing_or_extra_gold(self):
        cases, splits, decisions, gold = fixture()
        for bad in (gold[:-1], gold + [{"case_id": "c1", "correct": True}]):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, "exactly match"):
                score_frozen_test(cases, splits, decisions, bad)

    def test_rejects_duplicate_decisions_and_gold(self):
        cases, splits, decisions, gold = fixture()
        with self.assertRaisesRegex(ValueError, "duplicate accept"):
            score_frozen_test(cases, splits, decisions + [decisions[0]], gold)
        with self.assertRaisesRegex(ValueError, "duplicate correct"):
            score_frozen_test(cases, splits, decisions, gold + [gold[0]])

    def test_rejects_non_boolean_and_extra_decision_gold_fields(self):
        cases, splits, decisions, gold = fixture()
        for value in (1, 0, "yes", None):
            altered = copy.deepcopy(decisions)
            altered[0]["accept"] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "Boolean"):
                score_frozen_test(cases, splits, altered, gold)
        altered = copy.deepcopy(gold)
        altered[0]["correct"] = 1
        with self.assertRaisesRegex(ValueError, "Boolean"):
            score_frozen_test(cases, splits, decisions, altered)
        altered = copy.deepcopy(decisions)
        altered[0]["confidence"] = .9
        with self.assertRaisesRegex(ValueError, "fields"):
            score_frozen_test(cases, splits, altered, gold)

    def test_all_abstain_has_undefined_conditional_error(self):
        cases, splits, decisions, gold = fixture()
        decisions = [{"case_id": d["case_id"], "accept": False} for d in decisions]
        r = score_frozen_test(cases, splits, decisions, gold)
        self.assertIsNone(r["conditional_error_among_accepted"])
        self.assertEqual(r["case_coverage"], 0)
        self.assertEqual(r["source_family_unsafe_acceptance_rate"], 0)

    def test_same_observables_opposite_synthetic_labels(self):
        r = constructed_identifiability_warning()
        self.assertTrue(r["identical_verifier_observations"])
        self.assertTrue(r["identical_frozen_decisions"])
        self.assertEqual(r["unsafe_acceptance_if_correct"], 0)
        self.assertEqual(r["unsafe_acceptance_if_incorrect"], 1)


if __name__ == "__main__":
    unittest.main()
