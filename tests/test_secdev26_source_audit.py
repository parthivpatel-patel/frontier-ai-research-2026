"""Protocol 021 tests. All in-memory rows are constructed, not model outputs."""
import csv
import hashlib
import io
import unittest

from src.secdev26_source_audit import (
    HEADER, MAX_BYTES, audit_csv_bytes, git_blob_sha1, normalized_formula,
    normalized_nl,
)


def make_csv(rows, header=HEADER):
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


def audit(rows, header=HEADER):
    raw = make_csv(rows, header)
    return audit_csv_bytes(raw, expected_blob_sha=git_blob_sha1(raw))


class SourceAuditTests(unittest.TestCase):
    def test_git_blob_hash_is_byte_exact(self):
        self.assertEqual(
            git_blob_sha1(b"test content\n"),
            hashlib.sha1(b"blob 13\0test content\n").hexdigest(),
        )

    def test_valid_two_row_fixture(self):
        result = audit([
            ("if a then b", "G(a -> b)", "a : a"),
            ("if b then a", "G(b -> a)", "b : b"),
        ])
        self.assertEqual(result["input_rows"], 2)
        self.assertEqual(result["distinct_normalized_nl_strings"], 2)
        self.assertEqual(result["distinct_nl_formula_pairs"], 2)
        self.assertEqual(result["duplicate_nl_formula_pair_occurrences"], 0)

    def test_duplicate_pair_occurrences_not_independent(self):
        result = audit([("A is true", "G(a)", "a")]*3)
        self.assertEqual(result["input_rows"], 3)
        self.assertEqual(result["distinct_normalized_nl_strings"], 1)
        self.assertEqual(result["duplicate_nl_formula_pair_occurrences"], 2)
        self.assertEqual(result["nl_strings_repeated_across_rows"], 1)
        self.assertFalse(result["source_family_independence_verified"])

    def test_whitespace_and_case_normalization_only(self):
        result = audit([
            ("  A   is True  ", "G ( a )", "a"),
            ("a is true", "G(a)", "a"),
        ])
        self.assertEqual(result["distinct_normalized_nl_strings"], 1)
        self.assertEqual(result["distinct_nl_formula_pairs"], 1)
        self.assertEqual(result["duplicate_nl_formula_pair_occurrences"], 1)

    def test_same_nl_different_formulas_flagged_not_called_error(self):
        result = audit([
            ("a eventually", "F(a)", "a"),
            ("A eventually", "G(a)", "a"),
        ])
        self.assertEqual(result["normalized_nl_strings_with_multiple_lexical_formulas"], 1)
        self.assertEqual(result["semantic_mismatch_claims"], 0)

    def test_same_formula_different_nl(self):
        result = audit([
            ("a eventually", "F(a)", "a"),
            ("eventually a", "F(a)", "a"),
        ])
        self.assertEqual(result["lexical_formulas_with_multiple_normalized_nl_strings"], 1)

    def test_quoted_comma_is_parsed_as_one_cell(self):
        result = audit([("if a, then b", "G(a -> b)", "a : a, b : b")])
        self.assertEqual(result["input_rows"], 1)

    def test_reject_wrong_schema(self):
        with self.assertRaisesRegex(ValueError, "schema"):
            audit([("a", "F(a)", "a")], ("Natural Language", "Formula", "AP"))

    def test_reject_empty_dataset(self):
        with self.assertRaisesRegex(ValueError, "empty CSV"):
            audit([])

    def test_reject_empty_required_cells(self):
        for rows in ([("", "F(a)", "a")], [("a", "", "a")]):
            with self.assertRaisesRegex(ValueError, "empty NL"):
                audit(rows)

    def test_optional_atomic_proposition_cell_is_not_ground_truth(self):
        result = audit([("a", "F(a)", "")])
        self.assertEqual(result["input_rows"], 1)

    def test_reject_extra_or_missing_cells(self):
        for rows in ([("a", "F(a)")], [("a", "F(a)", "a", "extra")]):
            with self.assertRaisesRegex(ValueError, "malformed CSV row"):
                audit(rows)

    def test_reject_altered_blob(self):
        raw = make_csv([("a", "F(a)", "a")])
        with self.assertRaisesRegex(ValueError, "pinned Git blob"):
            audit_csv_bytes(raw + b"x", expected_blob_sha=git_blob_sha1(raw))

    def test_reject_bad_sha_format(self):
        raw = make_csv([("a", "F(a)", "a")])
        for sha in ("abc", "z"*40, "", None):
            with self.assertRaisesRegex(ValueError, "invalid expected"):
                audit_csv_bytes(raw, expected_blob_sha=sha)

    def test_reject_invalid_utf8(self):
        raw = b"\xff\xfe"
        with self.assertRaisesRegex(ValueError, "invalid UTF-8"):
            audit_csv_bytes(raw, expected_blob_sha=git_blob_sha1(raw))

    def test_reject_invalid_csv_quoting(self):
        raw = b'Natural Language,Ground Truth,Atomic Proposition\n"unterminated,F(a),a\n'
        with self.assertRaisesRegex(ValueError, "malformed CSV"):
            audit_csv_bytes(raw, expected_blob_sha=git_blob_sha1(raw))

    def test_reject_oversized_input(self):
        raw = b"x"*(MAX_BYTES+1)
        with self.assertRaisesRegex(ValueError, "oversized"):
            audit_csv_bytes(raw, expected_blob_sha=git_blob_sha1(raw))

    def test_reject_nonbytes(self):
        with self.assertRaises(ValueError):
            audit_csv_bytes("not bytes", expected_blob_sha="a"*40)

    def test_no_model_accuracy_or_novelty_inferred(self):
        result = audit([("a", "F(a)", "a")])
        self.assertEqual(result["authenticated_nl2futureltl_model_predictions"], 0)
        self.assertEqual(result["independent_human_intent_adjudications"], 0)
        self.assertFalse(result["novelty_established"])

    def test_normalizers_are_lexical_only(self):
        self.assertEqual(normalized_nl("  IF  A "), "if a")
        self.assertEqual(normalized_formula("G ( a -> F b )"), "G(a->Fb)")
        self.assertNotEqual(normalized_formula("F(a)"), normalized_formula("G(a)"))


if __name__ == "__main__":
    unittest.main()
