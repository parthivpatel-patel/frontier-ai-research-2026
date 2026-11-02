"""No-network fixtures for pre-registered QSTR parser sensitivity estimands."""
import unittest

from src.qstr_scoring_replication import clean_answer, parse_answers, question_index
from src.qstr_parser_sensitivity import (
    clean_first_marker, compact_inequality_fix, paired_sensitivity,
)


def questions(answer="A"):
    return question_index([
        {"ID": 1, "ANSWER": answer, "TYPE": "converse", "CALCULUS": "PA"}
    ])


class ParserSensitivityTests(unittest.TestCase):
    def test_legacy_compact_inequality_quirk_is_real(self):
        self.assertEqual(parse_answers(clean_answer("Answer: A!=B")), ["="])
        self.assertEqual(parse_answers(compact_inequality_fix("A!=B")), ["!="])

    def test_compact_only_changes_exact_identifier_pair(self):
        self.assertEqual(compact_inequality_fix("A!=B"), "A != B")
        self.assertEqual(compact_inequality_fix("A != B"), "A != B")
        self.assertEqual(compact_inequality_fix("A<=B"), "A<=B")
        self.assertEqual(compact_inequality_fix("A!=B, C!=D"), "A != B, C != D")
        self.assertEqual(compact_inequality_fix("5!=B"), "5!=B")

    def test_first_marker_only(self):
        text = "Answer: A\nAnswer: B"
        self.assertEqual(clean_answer(text), "B")
        self.assertEqual(clean_first_marker(text), "A")
        self.assertEqual(clean_first_marker("no marker\nA"), clean_answer("no marker\nA"))

    def test_compact_gain_is_paired_and_question_clustered(self):
        rows = [{"id": 1, "repeat": 0, "answer": "Answer: A!=B"},
                {"id": 1, "repeat": 1, "answer": "Answer: A!=B"}]
        summary = paired_sensitivity(rows, questions("!="), (0, 1))
        self.assertEqual(summary["legacy_correct"], 0)
        self.assertEqual(summary["compact_candidate"], 2)
        self.assertEqual(summary["interventions"]["compact"]["gained_correct"], 2)
        self.assertEqual(summary["interventions"]["compact"]["score_flipped_question_ids"], 1)
        self.assertEqual(summary["interventions"]["first_marker"]["score_flipped_rows"], 0)

    def test_first_marker_gain(self):
        summary = paired_sensitivity(
            [{"id": 1, "repeat": 0, "answer": "Answer: A\nAnswer: B"}],
            questions("A"), (0,))
        self.assertEqual(summary["multiple_answer_markers"], 1)
        self.assertEqual(summary["legacy_correct"], 0)
        self.assertEqual(summary["interventions"]["first_marker"]["gained_correct"], 1)

    def test_first_marker_loss(self):
        summary = paired_sensitivity(
            [{"id": 1, "repeat": 0, "answer": "Answer: A\nAnswer: B"}],
            questions("B"), (0,))
        self.assertEqual(summary["legacy_correct"], 1)
        self.assertEqual(summary["interventions"]["first_marker"]["lost_correct"], 1)

    def test_null_result_and_duplicate_diagnostic(self):
        summary = paired_sensitivity(
            [{"id": 1, "repeat": 0, "answer": "A, A"}],
            questions("A"), (0,))
        self.assertEqual(summary["no_answer_marker"], 1)
        self.assertEqual(summary["legacy_duplicate_relations"], 1)
        self.assertEqual(summary["interventions"]["compact"]["score_flipped_rows"], 0)
        self.assertEqual(summary["interventions"]["first_marker"]["score_flipped_rows"], 0)

    def test_fail_closed_missing_repeat(self):
        with self.assertRaisesRegex(ValueError, "Missing"):
            paired_sensitivity([{"id": 1, "repeat": 0, "answer": "A"}],
                               questions(), (0, 1))

    def test_fail_closed_duplicate_repeat(self):
        rows = [{"id": 1, "repeat": 0, "answer": "A"}] * 2
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            paired_sensitivity(rows, questions(), (0,))

    def test_fail_closed_unexpected_repeat_and_unknown_id(self):
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            paired_sensitivity([{"id": 1, "repeat": 2, "answer": "A"}],
                               questions(), (0,))
        with self.assertRaisesRegex(ValueError, "without matching"):
            paired_sensitivity([{"id": 2, "repeat": 0, "answer": "A"}],
                               questions(), (0,))

    def test_no_raw_response_in_summary(self):
        result = paired_sensitivity(
            [{"id": 1, "repeat": 0, "answer": "private response sentinel"}],
            questions(), (0,))
        self.assertNotIn("private response sentinel", str(result))


if __name__ == "__main__":
    unittest.main()
