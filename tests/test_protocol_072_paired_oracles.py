"""Protocol 072: exact, dependency-free paired partial-identification oracles.

These tests verify mathematical examples independently of the production
implementation. They are NOT evidence of physical ground truth or model quality.
Run on a confirmed zero-cost cloud runner: python -m unittest discover -s tests.
"""
import itertools
import unittest


def sharp_bounds(accept_a, accept_b, truth):
    """Enumerate all assignments for unresolved binary unsafe labels."""
    if not (len(accept_a) == len(accept_b) == len(truth)) or not truth:
        raise ValueError("nonempty equally sized arrays required")
    if any(type(x) is not bool for x in (*accept_a, *accept_b)):
        raise ValueError("acceptance values must be bool")
    if any(x is not None and type(x) is not bool for x in truth):
        raise ValueError("truth values must be bool or None")
    missing = [i for i, x in enumerate(truth) if x is None]
    values = []
    for assignment in itertools.product((False, True), repeat=len(missing)):
        labels = list(truth)
        for i, value in zip(missing, assignment):
            labels[i] = value
        values.append(sum((int(a) - int(b)) * int(y)
                          for a, b, y in zip(accept_a, accept_b, labels))
                      / len(truth))
    return min(values), max(values)


class PairedOracleTests(unittest.TestCase):
    def test_shared_unknown_cancels(self):
        self.assertEqual(sharp_bounds([True], [True], [None]), (0, 0))

    def test_both_reject_unknown_cancels(self):
        self.assertEqual(sharp_bounds([False], [False], [None]), (0, 0))

    def test_a_only_unknown(self):
        self.assertEqual(sharp_bounds([True], [False], [None]), (0, 1))

    def test_b_only_unknown(self):
        self.assertEqual(sharp_bounds([False], [True], [None]), (-1, 0))

    def test_known_unsafe_a_only(self):
        self.assertEqual(sharp_bounds([True], [False], [True]), (1, 1))

    def test_known_safe_a_only(self):
        self.assertEqual(sharp_bounds([True], [False], [False]), (0, 0))

    def test_equal_coverage_unequal_safety(self):
        # Each verifier accepts exactly one of two claims.
        self.assertEqual(sharp_bounds([True, False], [False, True],
                                      [True, False]), (0.5, 0.5))

    def test_paired_opposing_unknowns(self):
        self.assertEqual(sharp_bounds([True, False], [False, True],
                                      [None, None]), (-0.5, 0.5))

    def test_invalid_empty(self):
        with self.assertRaises(ValueError):
            sharp_bounds([], [], [])

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            sharp_bounds([True], [], [None])

    def test_invalid_acceptance_type(self):
        with self.assertRaises(ValueError):
            sharp_bounds([1], [False], [None])

    def test_invalid_truth_type(self):
        with self.assertRaises(ValueError):
            sharp_bounds([True], [False], ["unknown"])


if __name__ == "__main__":
    unittest.main()
