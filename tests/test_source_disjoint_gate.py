"""Synthetic-only tests for the original-source leakage guard."""
import unittest

from src.source_disjoint_gate import plan_folds


class SourceDisjointGateTests(unittest.TestCase):
    def setUp(self):
        self.ids = [f"source-{i:02d}" for i in range(30)]

    def test_four_source_external_collection_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "insufficient"):
            plan_folds(["article_78", "article_80", "cara_pump_requirements",
                        "harvesting_process"])

    def test_exactly_thirty_independent_sources_pass(self):
        result = plan_folds(self.ids)
        self.assertEqual(result["n_original_sources"], 30)
        self.assertEqual([len(f["test_source_ids"]) for f in result["folds"]],
                         [6, 6, 6, 6, 6])

    def test_no_leakage_and_exactly_one_test_fold_per_source(self):
        result = plan_folds(self.ids)
        test_ids = []
        for fold in result["folds"]:
            self.assertFalse(set(fold["test_source_ids"]) &
                             set(fold["train_source_ids"]))
            self.assertEqual(set(fold["test_source_ids"]) |
                             set(fold["train_source_ids"]), set(self.ids))
            test_ids.extend(fold["test_source_ids"])
        self.assertEqual(sorted(test_ids), sorted(self.ids))

    def test_order_independence(self):
        a = plan_folds(self.ids)
        b = plan_folds(list(reversed(self.ids)))
        self.assertEqual(a, b)

    def test_reproducible_seed(self):
        self.assertEqual(plan_folds(self.ids, seed=11),
                         plan_folds(self.ids, seed=11))

    def test_duplicate_source_rejected_even_if_thirty_rows(self):
        repeated = self.ids[:29] + [self.ids[0]]
        with self.assertRaisesRegex(ValueError, "duplicate"):
            plan_folds(repeated)

    def test_noncanonical_or_invalid_source_id_rejected(self):
        for invalid in ("", " source", "source ", None, 123, "x" * 257):
            with self.assertRaises(ValueError):
                plan_folds(self.ids[:29] + [invalid])

    def test_bad_split_settings_rejected(self):
        for kwargs in ({"seed": True}, {"n_folds": 1},
                       {"n_folds": True}, {"min_sources": 2},
                       {"min_sources": False}):
            with self.assertRaises(ValueError):
                plan_folds(self.ids, **kwargs)

    def test_custom_minimum_and_folds(self):
        result = plan_folds(self.ids[:12], min_sources=12, n_folds=3)
        self.assertEqual([len(f["test_source_ids"]) for f in result["folds"]],
                         [4, 4, 4])


if __name__ == "__main__":
    unittest.main()
