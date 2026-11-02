"""Protocol 023: constructed tests only, never fetch external records in tests."""
import copy
import json
import unittest
from unittest.mock import patch

from src.vltl_prediction_audit import (
    FILES, MAX_BYTES, audit_jsonl, fetch_pinned, git_blob_sha,
    run_audit, verify_pinned_bytes,
)


def row(rid=1, prediction="prop_1 or prop_2"):
    return {
        "id": rid,
        "sentence": ["visit", "x"],
        "tl": ["visit(x)", "or", "visit(y)"],
        "masked_tl": ["prop_1", "or", "prop_2"],
        "prediction": prediction,
    }


def encode(*rows):
    return ("\n".join(json.dumps(x) for x in rows) + "\n").encode("utf-8")


class PinnedVLTLTests(unittest.TestCase):
    def test_git_blob_hash_includes_header(self):
        self.assertEqual(git_blob_sha(b"hello\n"),
                         "ce013625030ba8dba906f756967f9e9ca394464a")

    def test_pinned_bytes_pass_exact(self):
        b = b"hello\n"
        verify_pinned_bytes(b, len(b), git_blob_sha(b))

    def test_pinned_bytes_reject_length_change(self):
        with self.assertRaisesRegex(ValueError, "byte count"):
            verify_pinned_bytes(b"hello", 6, git_blob_sha(b"hello"))

    def test_pinned_bytes_reject_sha_change(self):
        with self.assertRaisesRegex(ValueError, "SHA mismatch"):
            verify_pinned_bytes(b"hello", 5, "0" * 40)

    def test_pinned_bytes_reject_oversized_expected(self):
        with self.assertRaisesRegex(ValueError, "expected size"):
            verify_pinned_bytes(b"a", MAX_BYTES + 1, "0" * 40)

    def test_lifted_reference_exact(self):
        r = audit_jsonl(encode(row()), "masked_tl")
        self.assertEqual((r["records"], r["exact_token_string_matches"]), (1, 1))
        self.assertEqual(r["exact_match_fraction_among_nonblank"], 1)
        self.assertFalse(r["semantic_correctness_verified"])

    def test_raw_reference_nonmatch(self):
        r = audit_jsonl(encode(row()), "tl")
        self.assertEqual(r["nonmatching_token_strings"], 1)
        self.assertEqual(r["exact_match_fraction_among_nonblank"], 0)

    def test_whitespace_only_normalization(self):
        r = audit_jsonl(encode(row(prediction="  prop_1   or\tprop_2 ")), "masked_tl")
        self.assertEqual(r["exact_token_string_matches"], 1)

    def test_missing_and_blank_separated(self):
        a = row(1)
        del a["prediction"]
        b = row(2, "  ")
        c = row(3, None)
        r = audit_jsonl(encode(a, b, c), "masked_tl")
        self.assertEqual(r["missing_predictions"], 2)
        self.assertEqual(r["blank_predictions"], 1)
        self.assertEqual(r["nonblank_predictions"], 0)
        self.assertIsNone(r["exact_match_fraction_among_nonblank"])

    def test_duplicate_id_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            audit_jsonl(encode(row(1), row(1)), "tl")

    def test_boolean_float_negative_ids_rejected(self):
        for rid in (True, 1.0, -1, None, "1"):
            with self.subTest(rid=rid), self.assertRaisesRegex(ValueError, "id"):
                audit_jsonl(encode(row(rid)), "tl")

    def test_missing_or_invalid_token_lists_rejected(self):
        for field, value in (("sentence", []), ("tl", "x"),
                             ("masked_tl", [""]), ("tl", [None])):
            a = row()
            a[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "token"):
                audit_jsonl(encode(a), "tl")

    def test_invalid_prediction_type_rejected(self):
        with self.assertRaisesRegex(ValueError, "prediction type"):
            audit_jsonl(encode(row(prediction=["prop_1"])), "tl")

    def test_bad_json_and_blank_line_rejected(self):
        for raw in (b"{not json}\n", b"\n", encode(row()) + b"\n"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                audit_jsonl(raw, "tl")

    def test_invalid_utf8_rejected(self):
        with self.assertRaisesRegex(ValueError, "UTF-8"):
            audit_jsonl(b"\xff", "tl")

    def test_oversize_and_empty_rejected(self):
        for data in (b"", b"x" * (MAX_BYTES + 1)):
            with self.subTest(length=len(data)), self.assertRaises(ValueError):
                audit_jsonl(data, "tl")

    def test_unregistered_reference_rejected(self):
        with self.assertRaisesRegex(ValueError, "reference"):
            audit_jsonl(encode(row()), "gold")

    def test_unregistered_url_never_fetched(self):
        with patch("src.vltl_prediction_audit.urllib.request.urlopen") as net:
            with self.assertRaisesRegex(ValueError, "unregistered"):
                fetch_pinned({"path": "arbitrary"})
            net.assert_not_called()

    def test_report_contains_no_original_prediction_or_sentence(self):
        r = audit_jsonl(encode(row()), "masked_tl")
        serialized = json.dumps(r)
        self.assertNotIn("prop_1", serialized)
        self.assertNotIn("visit", serialized)
        self.assertFalse(r["model_provenance_verified"])

    def test_two_tasks_reported_separately(self):
        with patch("src.vltl_prediction_audit.fetch_pinned", return_value=encode(row())):
            r = run_audit()
        self.assertEqual(len(r["reports"]), 2)
        self.assertEqual([x["reference_field"] for x in r["reports"]],
                         ["masked_tl", "tl"])
        self.assertEqual([x["exact_token_string_matches"] for x in r["reports"]],
                         [1, 0])
        self.assertEqual(len(FILES), 2)


if __name__ == "__main__":
    unittest.main()
