"""Offline, synthetic-only tests for the pinned external schema auditor."""
import hashlib
import unittest

from src.nl2mtl_pinned_schema_audit import (
    SOURCES, audit, manifest, nonempty, verify_blob,
)


def synthetic_records():
    result = {}
    for path in manifest():
        result[path] = {
            "context": "synthetic",
            "MTL_expressions": [
                {"id": "MTL_1", "MTL_expression": "G(p)",
                 "propositions": [
                     {"id": "p", "assumptions": ["synthetic"],
                      "ambiguities": "", "description": "synthetic"}]}
            ],
            "dependency_sequence": [],
            "non_formalized_parts": [],
        }
    return result


class PinnedAuditTests(unittest.TestCase):
    def test_manifest_exactly_20_unique_sha1_blobs(self):
        entries = manifest()
        self.assertEqual(len(entries), 20)
        self.assertEqual(len(SOURCES), 4)
        self.assertTrue(all(len(v) == 40 and all(c in "0123456789abcdef" for c in v)
                            for v in entries.values()))

    def test_complete_synthetic_inventory(self):
        result = audit(synthetic_records())
        self.assertEqual(result["files_verified"], 20)
        self.assertEqual(result["source_documents"], 4)
        self.assertEqual(result["totals"]["expression_records"], 20)
        self.assertEqual(result["totals"]["propositions_with_nonempty_assumptions"], 20)
        self.assertEqual(result["sources_with_variable_expression_counts"], 0)

    def test_missing_file_rejected(self):
        records = synthetic_records()
        records.pop(next(iter(records)))
        with self.assertRaisesRegex(ValueError, "incomplete"):
            audit(records)

    def test_variable_counts_not_inferred_as_semantic_error(self):
        records = synthetic_records()
        key = next(iter(records))
        records[key]["MTL_expressions"].append(
            {"id": "MTL_2", "MTL_expression": "F(q)", "propositions": []}
        )
        result = audit(records)
        self.assertEqual(result["sources_with_variable_expression_counts"], 1)
        self.assertEqual(result["totals"]["expression_records"], 21)

    def test_dangling_local_dependencies_counted_not_scored(self):
        records = synthetic_records()
        key = next(iter(records))
        records[key]["dependency_sequence"] = [
            {"preceding_id": "MTL_1", "following_id": "UNKNOWN"}
        ]
        result = audit(records)
        self.assertEqual(result["totals"]["unresolved_local_dependency_endpoints"], 1)

    def test_empty_and_mixed_annotations(self):
        self.assertFalse(nonempty(""))
        self.assertFalse(nonempty([]))
        self.assertFalse(nonempty(None))
        self.assertTrue(nonempty(["uncertain"]))
        self.assertTrue(nonempty("  perhaps  "))

    def test_exact_git_blob_hash_and_tamper_detection(self):
        data = b'{"MTL_expressions":[]}'
        sha = hashlib.sha1(b"blob " + str(len(data)).encode() + bytes([0]) + data).hexdigest()
        self.assertEqual(verify_blob(data, sha), {"MTL_expressions": []})
        with self.assertRaisesRegex(ValueError, "SHA mismatch"):
            verify_blob(data + b" ", sha)

    def test_integer_and_string_identifiers_are_supported_and_counted(self):
        records = synthetic_records()
        key = next(iter(records))
        records[key]["MTL_expressions"][0]["id"] = 7
        records[key]["dependency_sequence"] = [
            {"preceding_id": "7", "following_id": 7}
        ]
        result = audit(records)
        self.assertEqual(result["expression_id_json_types"]["int"], 1)
        self.assertEqual(result["dependency_endpoint_json_types"]["int"], 1)
        self.assertEqual(result["dependency_endpoint_json_types"]["str"], 1)
        self.assertEqual(result["totals"]["unresolved_local_dependency_endpoints"], 0)

    def test_malformed_formula_rejected(self):
        records = synthetic_records()
        key = next(iter(records))
        records[key]["MTL_expressions"][0]["MTL_expression"] = None
        with self.assertRaisesRegex(ValueError, "malformed"):
            audit(records)


if __name__ == "__main__":
    unittest.main()
