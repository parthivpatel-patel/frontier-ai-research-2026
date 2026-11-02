"""Tests for the deliberately limited learned NLP offset baseline."""
import unittest

from src.learned_offset_baseline import (
    MultinomialNB, TRAIN_TEMPLATES, held_out_rows,
    run_exploratory_baseline, tokenize, training_examples,
)


class LearnedOffsetBaselineTests(unittest.TestCase):
    def test_real_supervised_fit_and_prediction(self):
        model = MultinomialNB().fit(training_examples())
        self.assertEqual(model.predict(
            "If event a occurs, require event b six discrete intervals afterward."), 6)
        self.assertEqual(model.predict(
            "Following event a, ensure b holds exactly two time units later."), 2)

    def test_not_hardcoded_external_sentence_in_training(self):
        train = {text.lower() for text, _ in training_examples()}
        for text, _, _ in held_out_rows():
            self.assertNotIn(text.lower(), train)
        self.assertEqual(len(TRAIN_TEMPLATES), 5)
        self.assertEqual(len(training_examples()), 45)

    def test_external_data_is_one_independent_source(self):
        rows = held_out_rows()
        self.assertEqual(len(rows), 5)
        self.assertEqual(len({source for _, _, source in rows}), 1)
        self.assertEqual([target for _, target, _ in rows], [2, 1, 4, 6, 4])

    def test_number_mask_is_an_ablation(self):
        self.assertEqual(tokenize("one two nine", True),
                         ["__number__", "__number__", "__number__"])
        model = MultinomialNB(mask_numbers=True).fit(training_examples())
        predictions = {model.predict(text) for text, _, _ in held_out_rows()}
        self.assertEqual(predictions, {1})

    def test_explicit_no_publication_gate(self):
        result = run_exploratory_baseline()
        self.assertEqual(result["training_examples"], 45)
        self.assertEqual(result["held_out_external_rows"], 5)
        self.assertEqual(result["independent_external_source_instructions"], 1)
        self.assertEqual(result["learned_correct_rows"], 5)
        self.assertEqual(result["masked_correct_rows"], 1)
        self.assertEqual(result["inherited_label_mismatches"], 5)
        self.assertFalse(result["publication_ready"])
        self.assertIn("INSUFFICIENT_INDEPENDENT_SOURCES", result["evaluation_status"])

    def test_unfitted_and_empty_training_rejected(self):
        with self.assertRaises(ValueError):
            MultinomialNB().predict("two steps")
        with self.assertRaises(ValueError):
            MultinomialNB().fit([])


if __name__ == "__main__":
    unittest.main()
