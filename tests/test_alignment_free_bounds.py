"""Synthetic-only regression tests for cardinality bounds (no network)."""
import itertools
import unittest
from fractions import Fraction

from src.alignment_free_bounds import PUBLISHED_COUNTS, audit, pair_bounds


class CardinalityBoundsTests(unittest.TestCase):
    def test_pair_bounds_are_symmetric_and_tight(self):
        for n in range(6):
            for m in range(6):
                left, right = pair_bounds(n, m), pair_bounds(m, n)
                self.assertEqual(left, right)
                self.assertEqual(left["unavoidable_unmatched_occurrences"], abs(n - m))
                self.assertEqual(left["possible_matched_record_count"], [0, min(n, m)])

    def test_nonzero_overlap_upper_bound_is_exact(self):
        self.assertEqual(pair_bounds(2, 3)["max_matched_fraction"], Fraction(2, 3))
        self.assertEqual(pair_bounds(3, 3)["max_matched_fraction"], Fraction(1, 1))
        self.assertEqual(pair_bounds(0, 3)["max_matched_fraction"], Fraction(0, 1))

    def test_both_empty_is_not_perfect_agreement(self):
        self.assertIsNone(pair_bounds(0, 0)["max_matched_fraction"])
        result = audit({"toy": (0, 0, 1)})
        self.assertEqual(result["by_source"]["toy"]["both_empty_pairs"], 1)
        self.assertAlmostEqual(result["mean_max_matched_fraction_decimal"], 0.0)

    def test_invalid_counts_fail_closed(self):
        for invalid in (-1, 2.5, True, "3", None):
            with self.assertRaises(ValueError):
                pair_bounds(invalid, 1)

    def test_equal_counts_do_not_identify_semantic_alignment(self):
        # Two unobserved interpretations yield identical observed count vectors:
        # a complete one-to-one match or no semantic correspondence at all.
        observed = pair_bounds(3, 3)
        self.assertEqual(observed["possible_matched_record_count"], [0, 3])
        self.assertEqual(observed["unavoidable_unmatched_occurrences"], 0)

    def test_published_vectors_exactly_four_sources_five_runs(self):
        self.assertEqual(len(PUBLISHED_COUNTS), 4)
        self.assertTrue(all(len(v) == 5 for v in PUBLISHED_COUNTS.values()))
        self.assertEqual(PUBLISHED_COUNTS["article_78"], (4, 6, 6, 5, 3))

    def test_locked_aggregate_from_published_vectors(self):
        result = audit()
        self.assertEqual(result["source_documents"], 4)
        self.assertEqual(result["unordered_within_source_run_pairs"], 40)
        self.assertEqual(result["unequal_count_pairs"], 30)
        self.assertEqual(result["sum_unavoidable_unmatched_occurrences_all_pairs"], 66)
        self.assertEqual(result["sum_unavoidable_unmatched_occurrences_adjacent_pairs"], 26)
        self.assertAlmostEqual(result["mean_max_matched_fraction_decimal"],
                               0.7058035714285716)

    def test_locked_source_breakdown(self):
        result = audit()["by_source"]
        expected = {
            "article_78": (16, 5),
            "article_80": (12, 6),
            "cara_pump_requirements": (22, 8),
            "harvesting_process": (16, 7),
        }
        for source, (all_pairs, adjacent) in expected.items():
            self.assertEqual(result[source]["sum_unavoidable_unmatched_occurrences"],
                             all_pairs)
            self.assertEqual(result[source]["adjacent_unavoidable_unmatched_occurrences"],
                             adjacent)

    def test_all_pairs_invariant_to_run_order(self):
        original = audit({"toy": (1, 2, 3, 4)})
        for order in itertools.permutations((1, 2, 3, 4)):
            reordered = audit({"toy": order})
            self.assertEqual(
                original["sum_unavoidable_unmatched_occurrences_all_pairs"],
                reordered["sum_unavoidable_unmatched_occurrences_all_pairs"])
            self.assertEqual(original["mean_max_matched_fraction_exact"],
                             reordered["mean_max_matched_fraction_exact"])

    def test_adjacent_metric_is_order_dependent(self):
        self.assertNotEqual(
            audit({"toy": (1, 2, 3)})[
                "sum_unavoidable_unmatched_occurrences_adjacent_pairs"],
            audit({"toy": (1, 3, 2)})[
                "sum_unavoidable_unmatched_occurrences_adjacent_pairs"])

    def test_invalid_source_structure(self):
        with self.assertRaises(ValueError):
            audit({})
        with self.assertRaises(ValueError):
            audit({"toy": (1,)})
        with self.assertRaises(ValueError):
            audit({"": (1, 2)})


if __name__ == "__main__":
    unittest.main()
