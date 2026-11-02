"""No-network tests for upstream-compatible QSTRBench strict scoring."""
import unittest

from src.qstr_scoring_replication import (
    clean_answer, extract_relation, parse_answers, question_index,
    reference_set, score_rows,
)


class QSTRScoringReplicationTests(unittest.TestCase):
    def test_upstream_extraction_fixtures(self):
        cases = [
            ("A < B", ["<"]),
            ("TPPi(x, y), x NTPP y", ["TPPi", "NTPP"]),
            ("A >B, C<D,E=F)", [">", "<", "="]),
            ("###>(x,z)", [">"]),
            (">(x,z)", [">"]),
            ("PP(x,y) and PP(y,z) means a relation.\n\n### Answer: PP, PP, EQ",
             ["PP", "PP", "EQ"]),
            ("\n\n### Answer: ID(y,x)\n\nDisclaimer: Ignore", ["ID"]),
            ('\n\n### Answer: ID(y,x),PPi(x,y)".', ["ID", "PPi"]),
        ]
        for answer, expected in cases:
            with self.subTest(answer=answer):
                self.assertEqual(parse_answers(clean_answer(answer)), expected)

    def test_last_answer_marker_controls_extraction(self):
        self.assertEqual(clean_answer("Answer: wrong\nAnswer: right"), "right")
        self.assertEqual(clean_answer("line one\nline two"), "line two")

    def test_exact_set_equality_not_jaccard(self):
        questions = question_index([{"ID": 1, "ANSWER": ["A", "B"],
                                     "TYPE": "ct", "CALCULUS": "IA"}])
        result = score_rows([{"id": "1", "repeat": 0, "answer": "Answer: A"}],
                            questions, (0,))
        self.assertEqual(result["strict_correct"], 0)

    def test_single_reference_string(self):
        self.assertEqual(reference_set("DC"), frozenset({"DC"}))
        self.assertEqual(reference_set(["DC", "EC"]), frozenset({"DC", "EC"}))

    def test_relation_extraction(self):
        self.assertEqual(extract_relation("A == B"), "=")
        self.assertEqual(extract_relation("A DC B"), "DC")
        self.assertEqual(extract_relation("A!=B"), "!=")

    def test_repeated_questions_not_independent(self):
        questions = question_index([
            {"ID": 1, "ANSWER": "A", "TYPE": "converse", "CALCULUS": "PA"},
            {"ID": 2, "ANSWER": "B", "TYPE": "converse", "CALCULUS": "PA"},
        ])
        rows = [
            {"id": "1", "repeat": 0, "answer": "Answer: A"},
            {"id": "1", "repeat": 1, "answer": "Answer: B"},
            {"id": "2", "repeat": 0, "answer": "Answer: B"},
            {"id": "2", "repeat": 1, "answer": "Answer: B"},
        ]
        result = score_rows(rows, questions, (0, 1))
        self.assertEqual(result["rows"], 4)
        self.assertEqual(result["questions"], 2)
        self.assertEqual(result["strict_correct"], 3)
        self.assertEqual(result["question_level"]["distinct_parsed_predictions_across_repeats"], 1)
        self.assertEqual(result["question_level"]["all_repeats_correct"], 1)
        self.assertEqual(result["question_level"]["any_repeat_correct"], 2)

    def test_missing_repeat_fails_closed(self):
        questions = question_index([{"ID": 1, "ANSWER": "A",
                                     "TYPE": "ct", "CALCULUS": "PA"}])
        with self.assertRaisesRegex(ValueError, "Missing"):
            score_rows([{"id": "1", "repeat": 0, "answer": "A"}],
                       questions, (0, 1))

    def test_duplicate_answer_fails_closed(self):
        questions = question_index([{"ID": 1, "ANSWER": "A",
                                     "TYPE": "ct", "CALCULUS": "PA"}])
        rows = [{"id": "1", "repeat": 0, "answer": "A"}] * 2
        with self.assertRaisesRegex(ValueError, "Duplicate model"):
            score_rows(rows, questions, (0,))

    def test_unmatched_id_fails_closed(self):
        questions = question_index([{"ID": 1, "ANSWER": "A",
                                     "TYPE": "ct", "CALCULUS": "PA"}])
        with self.assertRaisesRegex(ValueError, "without matching"):
            score_rows([{"id": "2", "repeat": 0, "answer": "A"}],
                       questions, (0,))

    def test_duplicate_question_fails_closed(self):
        row = {"ID": 1, "ANSWER": "A", "TYPE": "ct", "CALCULUS": "PA"}
        with self.assertRaisesRegex(ValueError, "Duplicate question"):
            question_index([row, row])

    def test_unexpected_repeat_fails_closed(self):
        questions = question_index([{"ID": 1, "ANSWER": "A",
                                     "TYPE": "ct", "CALCULUS": "PA"}])
        with self.assertRaisesRegex(ValueError, "Unexpected repeat"):
            score_rows([{"id": "1", "repeat": 2, "answer": "A"}],
                       questions, (0,))

    def test_aggregate_only_no_raw_model_answers(self):
        questions = question_index([{"ID": 1, "ANSWER": "A",
                                     "TYPE": "ct", "CALCULUS": "PA"}])
        result = score_rows([{"id": "1", "repeat": 0,
                              "answer": "confidential-response-text"}],
                            questions, (0,))
        self.assertNotIn("confidential-response-text", str(result))


if __name__ == "__main__":
    unittest.main()
