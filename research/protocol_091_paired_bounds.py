"""Protocol 091: paired unsafe-acceptance difference bounds.

Reference implementation. No empirical results or independent adjudication implied.
Only valid for a *shared, identical accepted set* for both methods. Each case
has one unknown binary unsafe truth; the two methods' unsafe outcomes may differ
only when their acceptance policies differ, which is ruled out here. Thus the
difference in unsafe risk on an identical accepted set is exactly zero.

For differing acceptance sets, use the general finite-population enumerator
below. The truth of each claim is shared across methods. No MAR assumption.
"""
from fractions import Fraction
from itertools import product
import unittest


def paired_difference_bounds(proposed_accept, baseline_accept, truth):
    """Sharp bounds for empirical risk difference under shared binary truth.

    Each sequence is indexed over the same fixed evaluation universe.
    Accept values must be bool. truth is bool or None for unadjudicated.
    Unsafe-acceptance risk is unsafe accepted / number accepted.
    Enumeration is exact but exponential in unresolved claims; use only
    small constructed examples. Do not run on large benchmarks.
    """
    n = len(truth)
    if len(proposed_accept) != n or len(baseline_accept) != n:
        raise ValueError("length mismatch")
    if any(type(x) is not bool for x in (*proposed_accept, *baseline_accept)):
        raise TypeError("acceptance must be bool")
    if any(x is not None and type(x) is not bool for x in truth):
        raise TypeError("truth must be bool or None")
    na = sum(proposed_accept)
    nb = sum(baseline_accept)
    if not na or not nb:
        raise ValueError("risk undefined at zero acceptance")
    missing = [i for i, x in enumerate(truth) if x is None]
    if len(missing) > 16:
        raise ValueError("enumeration limited to 16 missing labels")
    diffs = []
    for assignment in product((False, True), repeat=len(missing)):
        resolved = list(truth)
        for i, x in zip(missing, assignment):
            resolved[i] = x
        pa = sum(x for a, x in zip(proposed_accept, resolved) if a)
        ba = sum(x for a, x in zip(baseline_accept, resolved) if a)
        diffs.append(Fraction(pa, na) - Fraction(ba, nb))
    return min(diffs), max(diffs)


class PairedBoundsTests(unittest.TestCase):
    def test_same_accepted_set_cancels_unknown_truth(self):
        self.assertEqual(
            paired_difference_bounds([True, True], [True, True], [None, False]),
            (Fraction(0), Fraction(0)),
        )

    def test_disjoint_acceptance_sets(self):
        self.assertEqual(
            paired_difference_bounds([True, False], [False, True], [None, None]),
            (Fraction(-1), Fraction(1)),
        )

    def test_known_truth(self):
        self.assertEqual(
            paired_difference_bounds([True, False], [False, True], [True, False]),
            (Fraction(1), Fraction(1)),
        )

    def test_shared_missing_case_cancels(self):
        self.assertEqual(
            paired_difference_bounds([True, True], [True, False], [None, True]),
            (Fraction(0), Fraction(1, 2)),
        )

    def test_no_acceptance_rejected(self):
        with self.assertRaises(ValueError):
            paired_difference_bounds([False], [True], [None])

    def test_type_rejected(self):
        with self.assertRaises(TypeError):
            paired_difference_bounds([1], [True], [None])


if __name__ == "__main__":
    unittest.main()
