"""Dependency-free parity-bound regression tests; intended for free cloud CI."""
import itertools
import unittest
from fractions import Fraction

from research.archival_bounds import Counts
from research.paired_archival_oracle import MissingCase
from research.paired_archival_linear import sharp_paired_difference_linear
from research.paired_archival_parity import sharp_paired_difference_parity


class ParityIdentificationTests(unittest.TestCase):
    def test_singletons_reproduce_linear(self):
        cases = (MissingCase(0, True, 1, True), MissingCase(1, False, 0, True))
        a, b = Counts(0, 2, 0, 0), Counts(0, 2, 0, 0)
        self.assertEqual(sharp_paired_difference_parity(a, b, cases),
                         sharp_paired_difference_linear(a, b, cases))

    def test_equality_shrinks_interval(self):
        cases = (MissingCase(0, True, 1, True), MissingCase(1, True, 0, True))
        a = b = Counts(0, 2, 0, 0)
        self.assertEqual(sharp_paired_difference_linear(a, b, cases)["sharp"],
                         (Fraction(-1), Fraction(1)))
        self.assertEqual(sharp_paired_difference_parity(a, b, cases, [(0, 1, 0)])["sharp"],
                         (Fraction(0), Fraction(0)))

    def test_contradictory_cycle(self):
        cases = (MissingCase(0, True, 0, True),) * 3
        with self.assertRaisesRegex(ValueError, "Infeasible"):
            sharp_paired_difference_parity(Counts(0, 3, 0, 0), Counts(0, 3, 0, 0),
                                           cases, [(0, 1, 0), (1, 2, 0), (0, 2, 1)])

    def test_order_and_duplicate_invariance(self):
        cases = (MissingCase(0, True, 1, True),) * 3
        a = b = Counts(0, 3, 0, 0)
        first = sharp_paired_difference_parity(a, b, cases, [(0, 1, 1), (1, 2, 0)])
        second = sharp_paired_difference_parity(a, b, cases, [(1, 2, 0), (0, 1, 1), (0, 1, 1)])
        self.assertEqual(first, second)

    def test_undefined_and_infeasible_distinct(self):
        cases = (MissingCase(0, False, 0, False),) * 2
        a = b = Counts(0, 2, 0, 0)
        result = sharp_paired_difference_parity(a, b, cases, [(0, 1, 0)])
        self.assertIsNone(result["sharp"])
        self.assertEqual(result["undefined_assignments"], 2)
        with self.assertRaises(ValueError):
            sharp_paired_difference_parity(a, b, cases, [(0, 1, 0), (0, 1, 1)])

    def test_exhaustive_small_frames(self):
        # Deterministic exhaustive oracle: enumerate feasible truths, not all combinations of policy arms.
        patterns = [(0, True, 1, True), (1, True, 0, True),
                    (0, True, 0, False), (1, False, 1, True)]
        edges = [(0, 1, 0), (1, 2, 1)]
        for choice in itertools.product(patterns, repeat=3):
            cases = tuple(MissingCase(*p) for p in choice)
            a = b = Counts(1, 3, 1, 0)
            got = sharp_paired_difference_parity(a, b, cases, edges)
            vals = []
            for ys in itertools.product((0, 1), repeat=3):
                if any((ys[i] ^ ys[j]) != d for i, j, d in edges):
                    continue
                ka = a.accepted + sum(c.accept_a for c in cases)
                kb = b.accepted + sum(c.accept_b for c in cases)
                ea = a.errors + sum(c.accept_a and c.predict_a != y for c, y in zip(cases, ys))
                eb = b.errors + sum(c.accept_b and c.predict_b != y for c, y in zip(cases, ys))
                vals.append(Fraction(ea, ka) - Fraction(eb, kb))
            self.assertEqual(got["sharp"], (min(vals), max(vals)))
            self.assertEqual(got["defined_assignments"], len(vals))


if __name__ == "__main__":
    unittest.main()
