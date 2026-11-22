"""Cross-check linear sharp bounds against exhaustive shared-label oracle.

Run only in free GitHub-hosted CI; no laptop workloads.
"""
import unittest
from itertools import product

from research.archival_bounds import Counts
from research.paired_archival_oracle import MissingCase, sharp_paired_difference
from research.paired_archival_linear import sharp_paired_difference_linear


class LinearPairedTests(unittest.TestCase):
    def test_all_single_case_decisions(self):
        for pa, aa, pb, ab in product((0, 1), repeat=4):
            missing = [MissingCase(pa, bool(aa), pb, bool(ab))]
            for ea, eb in product((0, 1), repeat=2):
                a, b = Counts(1, 1, 1, ea), Counts(1, 1, 1, eb)
                self.assertEqual(sharp_paired_difference_linear(a, b, missing),
                                 sharp_paired_difference(a, b, missing))

    def test_two_case_cartesian_product(self):
        cases = [MissingCase(pa, bool(aa), pb, bool(ab))
                 for pa, aa, pb, ab in product((0, 1), repeat=4)]
        a = Counts(1, 2, 1, 0)
        b = Counts(1, 2, 1, 1)
        for first in cases:
            for second in cases:
                missing = [first, second]
                self.assertEqual(sharp_paired_difference_linear(a, b, missing),
                                 sharp_paired_difference(a, b, missing))

    def test_no_missing(self):
        a, b = Counts(2, 0, 2, 1), Counts(2, 0, 2, 0)
        self.assertEqual(sharp_paired_difference_linear(a, b, []),
                         sharp_paired_difference(a, b, []))

    def test_undefined(self):
        a = b = Counts(0, 1, 0, 0)
        missing = [MissingCase(0, False, 1, True)]
        self.assertEqual(sharp_paired_difference_linear(a, b, missing),
                         sharp_paired_difference(a, b, missing))

    def test_invalid_frame(self):
        with self.assertRaises(ValueError):
            sharp_paired_difference_linear(Counts(0, 1, 0, 0),
                                           Counts(0, 1, 0, 0), [])

    def test_long_frame_without_enumeration(self):
        missing = [MissingCase(0, True, 0, True)] * 100
        r = sharp_paired_difference_linear(Counts(0, 100, 0, 0),
                                           Counts(0, 100, 0, 0), missing)
        self.assertEqual(r["sharp"], (0, 0))
        self.assertEqual(r["defined_assignments"], 2 ** 100)


if __name__ == "__main__":
    unittest.main()
