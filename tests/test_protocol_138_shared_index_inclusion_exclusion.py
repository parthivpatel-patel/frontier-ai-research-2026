"""Protocol 138 deterministic comparisons; execute only on verified free cloud CI."""
import unittest
from fractions import Fraction
from research.protocol_137_shared_index_oracle import exact_shared_index_undefined
from research.protocol_138_shared_index_inclusion_exclusion import shared_index_inclusion_exclusion


class SharedIndexInclusionExclusionTests(unittest.TestCase):
    def test_identical_flags(self):
        families = [(1, (True, False)), (2, (True, False))]
        self.assertEqual(shared_index_inclusion_exclusion(families), Fraction(1, 4))

    def test_complementary_flags(self):
        families = [(1, (True, False)), (1, (False, True))]
        self.assertEqual(shared_index_inclusion_exclusion(families), Fraction(1, 2))

    def test_exhaustive_small_flag_patterns(self):
        from itertools import product
        for n in (2, 3):
            patterns = list(product((False, True), repeat=n))
            for a in patterns:
                for b in patterns:
                    families = [(1, a), (1, b)]
                    self.assertEqual(
                        shared_index_inclusion_exclusion(families),
                        exact_shared_index_undefined(families),
                    )

    def test_zero_weight_exclusion(self):
        self.assertEqual(
            shared_index_inclusion_exclusion([(1, (True, False)), (0, (False, False))]),
            Fraction(1, 4),
        )

    def test_large_lineage_count_without_enumeration(self):
        flags = (True,) + (False,) * 99
        self.assertEqual(
            shared_index_inclusion_exclusion([(1, flags), (2, flags)]),
            Fraction(99, 100) ** 100,
        )

    def test_reject_mismatched_panel(self):
        with self.assertRaises(ValueError):
            shared_index_inclusion_exclusion([(1, (True, False)), (1, (True, False, True))])

    def test_reject_zero_positive_families(self):
        with self.assertRaises(ValueError):
            shared_index_inclusion_exclusion([(0, (True, False))])


if __name__ == "__main__":
    unittest.main()
