"""No-network regression tests for bounded upstream dataset schema audit."""
import json
import lzma
import unittest

from src.qstr_schema_audit import (
    MAX_COMPRESSED,
    git_blob_sha,
    schema_summary,
    unpack_records,
)


def fixture(rows):
    raw = "\n".join(json.dumps(row) for row in rows).encode() + b"\n"
    blob = lzma.compress(raw)
    return blob, git_blob_sha(blob), len(blob)


class QSTRSchemaAuditTests(unittest.TestCase):
    def test_git_blob_digest_known_example(self):
        # Git object SHA-1 for a three-byte blob containing 'abc'.
        import hashlib
        self.assertEqual(
            git_blob_sha(b"abc"),
            hashlib.sha1(b"blob 3\0abc").hexdigest(),
        )

    def test_roundtrip_jsonl(self):
        rows = [{"id": 1, "answer": "a"}, {"id": 2, "answer": "b"}]
        self.assertEqual(unpack_records(*fixture(rows)), rows)

    def test_reject_tampered_blob(self):
        blob, sha, size = fixture([{"id": 1}])
        with self.assertRaisesRegex(ValueError, "SHA mismatch"):
            unpack_records(blob, "0" * 40, size)
        with self.assertRaisesRegex(ValueError, "size mismatch"):
            unpack_records(blob, sha, size + 1)

    def test_reject_non_object_rows(self):
        with self.assertRaisesRegex(ValueError, "JSON objects"):
            unpack_records(*fixture([{"id": 1}, 17]))

    def test_reject_empty_input(self):
        blob = lzma.compress(b"\n")
        with self.assertRaisesRegex(ValueError, "No records"):
            unpack_records(blob, git_blob_sha(blob), len(blob))

    def test_reject_oversized_compressed(self):
        blob = b"x" * (MAX_COMPRESSED + 1)
        with self.assertRaisesRegex(ValueError, "exceeded bound"):
            unpack_records(blob, git_blob_sha(blob), len(blob))

    def test_repeat_counts_and_nested_metadata_without_raw_values(self):
        rows = [
            {"id": "a", "repeat": 0, "response": {"content": "secret"}},
            {"id": "a", "repeat": 1, "response": {"content": "other"}},
            {"id": "b", "repeat": 0, "request": {"model": "test"}},
        ]
        result = schema_summary(rows)
        self.assertEqual(result["unique_identifier_values"], 2)
        self.assertEqual(result["identifier_values_with_repeats"], 1)
        self.assertEqual(result["repeat_field_distribution"], {"0": 2, "1": 1})
        self.assertEqual(result["nested_fields_present"]["response"], {"content": 2})
        self.assertNotIn("secret", json.dumps(result))

    def test_schema_only_no_accuracy_metric(self):
        result = schema_summary([{"id": 1, "answer": "x"}, {"id": 2}])
        self.assertEqual(result["rows"], 2)
        self.assertEqual(result["fields_present"]["answer"], 1)
        self.assertNotIn("accuracy", result)
        self.assertIn("no model accuracy", result["interpretation"])


if __name__ == "__main__":
    unittest.main()
