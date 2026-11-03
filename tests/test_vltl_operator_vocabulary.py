"""Protocol 027 constructed, network-free regression tests for GitHub cloud CI."""
import json
import unittest
from unittest.mock import patch

from src.vltl_operator_vocabulary import (
    CANDIDATES, FAMILIES, _unknown_vocabulary,
    audit_candidate_vocabulary, run_audit,
)


def definition():
    return {"action_canon": "secure", "args_canon": ["apple"],
            "action_ref": "secure", "args_ref": ["apple"]}


def record(i, prediction, reference):
    return {"id": i, "sentence": ["secure", "apple"],
            "tl": ["secure(apple)"], "masked_tl": reference.split(),
            "prediction": prediction,
            "prop_dict": {"prop_1": definition(), "prop_2": definition()}}


def pack(*rows):
    return ("\n".join(json.dumps(row) for row in rows) + "\n").encode()


class FrozenVocabularyTests(unittest.TestCase):
    def test_candidate_family_dictionary_is_frozen(self):
        self.assertEqual(set(CANDIDATES.values()), set(FAMILIES))
        self.assertEqual(CANDIDATES["v"], "release")
        self.assertEqual(CANDIDATES["weak_until"], "weak_until")

    def test_release_aliases(self):
        counts = _unknown_vocabulary("R prop_1 release prop_2 V prop_1")
        self.assertEqual(counts["candidate_counts"]["release"], 3)
        self.assertEqual(counts["unclassified_word_count"], 0)

    def test_weak_until_aliases(self):
        counts = _unknown_vocabulary("W weakuntil weak_until")
        self.assertEqual(counts["candidate_counts"]["weak_until"], 3)

    def test_strong_release_aliases(self):
        counts = _unknown_vocabulary("M strongrelease strong_release")
        self.assertEqual(counts["candidate_counts"]["strong_release"], 3)

    def test_boolean_candidate_aliases(self):
        counts = _unknown_vocabulary("XOR iff equiv equivalent")
        self.assertEqual(counts["candidate_counts"]["xor"], 1)
        self.assertEqual(counts["candidate_counts"]["equivalence"], 3)

    def test_existing_operators_and_atoms_excluded(self):
        counts = _unknown_vocabulary("G ( prop_1 -> F prop_2 ) and true")
        self.assertEqual(sum(counts["candidate_counts"].values()), 0)
        self.assertEqual(counts["unclassified_word_count"], 0)
        self.assertEqual(counts["unclassified_symbol_count"], 0)

    def test_candidate_only_pair_is_lexically_covered(self):
        result = audit_candidate_vocabulary(pack(
            record(1, "weakuntil prop_1", "weakuntil prop_2")))
        self.assertEqual(result["unsupported_pairs"], 1)
        self.assertEqual(result["candidate_operator_occurrences_by_family"]["weak_until"], 2)
        self.assertEqual(result["pairs_with_candidate_only_unknown_vocabulary"], 1)
        self.assertFalse(result["semantic_accuracy_measured"])

    def test_unclassified_word_pair_remains_unresolved(self):
        result = audit_candidate_vocabulary(pack(
            record(1, "MYSTERYTOKEN prop_1", "prop_2")))
        self.assertEqual(result["unclassified_word_occurrences"], 1)
        self.assertEqual(result["pairs_with_unclassified_or_nonoperator_unknown_vocabulary"], 1)
        self.assertNotIn("MYSTERYTOKEN", json.dumps(result))

    def test_unknown_symbol_remains_unresolved(self):
        result = audit_candidate_vocabulary(pack(
            record(1, "prop_1 ; prop_2", "prop_1")))
        self.assertEqual(result["unclassified_symbol_occurrences"], 1)
        self.assertEqual(result["pairs_with_candidate_only_unknown_vocabulary"], 0)

    def test_candidate_plus_unknown_is_not_covered(self):
        result = audit_candidate_vocabulary(pack(
            record(1, "W MYSTERYTOKEN prop_1", "prop_2")))
        self.assertEqual(result["candidate_operator_occurrences_by_family"]["weak_until"], 1)
        self.assertEqual(result["pairs_with_candidate_only_unknown_vocabulary"], 0)

    def test_exact_and_supported_nonexact_pairs_excluded(self):
        result = audit_candidate_vocabulary(pack(
            record(1, "prop_1", "prop_1"),
            record(2, "finally prop_1", "always prop_1")))
        self.assertEqual(result["unsupported_pairs"], 0)
        self.assertEqual(sum(result["candidate_operator_occurrences_by_family"].values()), 0)

    def test_reference_only_candidate_failure(self):
        result = audit_candidate_vocabulary(pack(
            record(1, "prop_1", "prop_1 R prop_2")))
        self.assertEqual(result["candidate_operator_occurrences_by_family"]["release"], 1)
        self.assertEqual(result["pairs_with_candidate_only_unknown_vocabulary"], 1)

    def test_duplicate_ids_fail_closed(self):
        with self.assertRaises(ValueError):
            audit_candidate_vocabulary(pack(
                record(1, "prop_1", "prop_2"),
                record(1, "prop_2", "prop_1")))

    def test_mocked_cloud_fetch(self):
        data = pack(record(1, "prop_1", "prop_1 W prop_2"))
        with patch("src.vltl_operator_vocabulary.fetch_pinned", return_value=data) as fetch:
            result = run_audit()
        fetch.assert_called_once()
        self.assertEqual(result["unsupported_pairs"], 1)
        self.assertFalse(result["source_text_or_identifiers_exposed"])

    def test_privacy_for_identifiers_and_text(self):
        result = audit_candidate_vocabulary(pack(
            record(1, "SECRETWORD prop_1", "prop_2")))
        output = json.dumps(result)
        for secret in ("SECRETWORD", "prop_1", "prop_2", "secure", "apple"):
            self.assertNotIn(secret, output)


if __name__ == "__main__":
    unittest.main()
