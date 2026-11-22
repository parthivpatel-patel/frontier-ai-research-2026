"""Independent exhaustive-oracle stress tests for parity-constrained selective risk.

Run in hosted CI only. These tests do not establish novelty or empirical AI results.
"""
import itertools
import unittest
from fractions import Fraction

from research.archival_bounds import Counts
from research.paired_archival_oracle import MissingCase
from research.paired_archival_parity import sharp_paired_difference_parity


def oracle(a, b, cases, edges):
    values = []
    for labels in itertools.product((0, 1), repeat=len(cases)):
        if any((labels[i] ^ labels[j]) != parity for i, j, parity in edges):
            continue
        ka = a.accepted + sum(c.accept_a for c in cases)
        kb = b.accepted + sum(c.accept_b for c in cases)
        if not ka or not kb:
            continue
        ea = a.errors + sum(int(c.accept_a and c.predict_a != y)
                            for c, y in zip(cases, labels))
        eb = b.errors + sum(int(c.accept_b and c.predict_b != y)
                            for c, y in zip(cases, labels))
        values.append(Fraction(ea, ka) - Fraction(eb, kb))
    return (min(values), max(values)) if values else None


class IndependentParityOracleTests(unittest.TestCase):
    def test_disconnected_components_and_verified_error_asymmetry(self):
        patterns = [
            MissingCase(0, True, 1, True),
            MissingCase(1, True, 1, False),
            MissingCase(0, False, 0, True),
            MissingCase(1, False, 0, False),
        ]
        edgesets = [(), ((0, 1, 0),), ((0, 1, 1),),
                    ((0, 1, 0), (2, 3, 1)),
                    ((0, 1, 1), (1, 2, 0), (2, 3, 1))]
        verified = [
            (Counts(3, 4, 2, 1), Counts(3, 4, 3, 2)),
            (Counts(2, 4, 0, 0), Counts(2, 4, 1, 1)),
        ]
        for chosen in itertools.product(patterns, repeat=4):
            for a, b in verified:
                for edges in edgesets:
                    with self.subTest(chosen=chosen, a=a, b=b, edges=edges):
                        result = sharp_paired_difference_parity(a, b, chosen, edges)
                        self.assertEqual(result["sharp"], oracle(a, b, chosen, edges))

    def test_self_constraints_and_repeated_edges(self):
        cases = (MissingCase(0, True, 1, True), MissingCase(1, True, 0, True))
        a = b = Counts(0, 2, 0, 0)
        expected = sharp_paired_difference_parity(a, b, cases, ((0, 1, 1),))
        actual = sharp_paired_difference_parity(
            a, b, cases, ((0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)))
        self.assertEqual(actual, expected)
        with self.assertRaisesRegex(ValueError, "Infeasible"):
            sharp_paired_difference_parity(a, b, cases, ((0, 0, 1),))

    def test_one_policy_zero_acceptance(self):
        cases = (MissingCase(0, False, 1, True), MissingCase(1, False, 0, True))
        a = Counts(0, 2, 0, 0)
        b = Counts(0, 2, 0, 0)
        result = sharp_paired_difference_parity(a, b, cases, ((0, 1, 0),))
        self.assertIsNone(result["sharp"])
        self.assertEqual(result["undefined_assignments"], 2)
        self.assertEqual(result["defined_assignments"], 0)


if __name__ == "__main__":
    unittest.main()
