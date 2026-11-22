"""Metamorphic falsification checks for exact parity-constrained identification.

Pure standard-library unit tests. Run on verified zero-cost hosted CI only.
These tests do not establish scientific novelty or empirical AI effects.
"""
import unittest
from research.archival_bounds import Counts
from research.paired_archival_oracle import MissingCase
from research.paired_archival_parity import sharp_paired_difference_parity as solve


class ParityMetamorphicTests(unittest.TestCase):
    def setUp(self):
        self.a = Counts(5, 4, 3, 1)
        self.b = Counts(5, 4, 4, 2)
        self.cases = (
            MissingCase(0, True, 1, True),
            MissingCase(1, True, 0, False),
            MissingCase(1, False, 0, True),
            MissingCase(0, True, 0, True),
        )
        self.edges = ((0, 1, 1), (1, 2, 0))

    def test_policy_exchange_negates_interval(self):
        r = solve(self.a, self.b, self.cases, self.edges)["sharp"]
        flipped = tuple(MissingCase(c.predict_b, c.accept_b,
                                    c.predict_a, c.accept_a) for c in self.cases)
        s = solve(self.b, self.a, flipped, self.edges)["sharp"]
        self.assertEqual(s, (-r[1], -r[0]))

    def test_joint_binary_complement_preserves_interval(self):
        r = solve(self.a, self.b, self.cases, self.edges)["sharp"]
        complemented = tuple(MissingCase(1-c.predict_a, c.accept_a,
                                         1-c.predict_b, c.accept_b)
                             for c in self.cases)
        self.assertEqual(solve(self.a, self.b, complemented, self.edges)["sharp"], r)

    def test_permutation_invariance(self):
        r = solve(self.a, self.b, self.cases, self.edges)["sharp"]
        order = (2, 0, 3, 1)
        old_to_new = {old: new for new, old in enumerate(order)}
        reordered = tuple(self.cases[i] for i in order)
        edges = tuple((old_to_new[i], old_to_new[j], d)
                      for i, j, d in reversed(self.edges))
        self.assertEqual(solve(self.a, self.b, reordered, edges)["sharp"], r)

    def test_more_constraints_cannot_expand_identification_set(self):
        previous = solve(self.a, self.b, self.cases, ())["sharp"]
        for edges in (self.edges[:1], self.edges,
                      self.edges + ((2, 3, 1),)):
            current = solve(self.a, self.b, self.cases, edges)["sharp"]
            self.assertLessEqual(previous[0], current[0])
            self.assertLessEqual(current[1], previous[1])
            previous = current

    def test_singletons_match_unconstrained_parity(self):
        baseline = solve(self.a, self.b, self.cases, ())["sharp"]
        self.assertEqual(solve(self.a, self.b, self.cases,
                               ((0, 0, 0), (3, 3, 0)))["sharp"], baseline)


if __name__ == "__main__":
    unittest.main()
