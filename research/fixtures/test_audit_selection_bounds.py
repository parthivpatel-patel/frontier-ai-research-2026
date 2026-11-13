"""Exact-arithmetic audit-selection identification checks (Protocol 057).

These tests are specifications, not experimental evidence. Run only on a
verified zero-cost cloud runner; do not execute on the user's laptop.
"""
from fractions import Fraction as F
from itertools import product
import unittest


def missing_label_bounds(audited_true, audited_false, unaudited):
    """Sharp finite-population bounds for the truth fraction in one stratum."""
    if any(type(x) is not int or x < 0 for x in
           (audited_true, audited_false, unaudited)):
        raise ValueError("counts must be nonnegative integers")
    total = audited_true + audited_false + unaudited
    if total == 0:
        raise ValueError("empty target stratum")
    return (F(audited_true, total),
            F(audited_true + unaudited, total))


def weighted_audit_rate(records):
    """Hajek ratio for (audited, truth, inclusion probability) triples.

    All eligible records are passed in; truth is only used when audited.
    This estimator requires *design-known* positive inclusion probabilities.
    """
    numerator = denominator = F(0)
    for audited, truth, probability in records:
        if type(audited) is not bool:
            raise ValueError("audited must be boolean")
        if not isinstance(probability, F) or not 0 < probability <= 1:
            raise ValueError("inclusion probability must be a rational in (0,1]")
        if audited:
            if type(truth) is not bool:
                raise ValueError("audited truth must be boolean")
            weight = 1 / probability
            denominator += weight
            numerator += weight * truth
    if denominator == 0:
        raise ValueError("no audited records; ratio undefined")
    return numerator / denominator


class AuditSelectionTests(unittest.TestCase):
    def test_protocol_example(self):
        # 4 true, 4 false in the population; audit all true and one false.
        self.assertEqual(missing_label_bounds(4, 1, 3), (F(1, 2), F(7, 8)))
        self.assertEqual(F(4, 5), F(4, 4 + 1))
        self.assertEqual(F(4, 8), F(1, 2))

    def test_sharp_bounds_exhaustive_small_populations(self):
        # Every completion of unknown labels is feasible without assumptions.
        for yes in range(5):
            for no in range(5):
                for missing in range(5):
                    if yes + no + missing == 0:
                        continue
                    lo, hi = missing_label_bounds(yes, no, missing)
                    completions = [F(yes + sum(bits), yes + no + missing)
                                   for bits in product((0, 1), repeat=missing)]
                    self.assertEqual(lo, min(completions))
                    self.assertEqual(hi, max(completions))
                    self.assertTrue(all(lo <= p <= hi for p in completions))

    def test_full_audit_collapses_bounds(self):
        self.assertEqual(missing_label_bounds(2, 3, 0), (F(2, 5), F(2, 5)))

    def test_zero_audit_is_vacuous(self):
        self.assertEqual(missing_label_bounds(0, 0, 7), (F(0), F(1)))

    def test_weighted_rate_and_naive_disagreement(self):
        # Two observed labels with unequal known selection probabilities.
        records = [(True, True, F(1, 1)), (True, False, F(1, 4))]
        self.assertEqual(weighted_audit_rate(records), F(1, 5))
        self.assertNotEqual(weighted_audit_rate(records), F(1, 2))

    def test_missing_labels_not_read(self):
        self.assertEqual(weighted_audit_rate([
            (True, True, F(1, 2)), (False, None, F(1, 3))]), F(1))

    def test_rejects_invalid_inputs(self):
        for args in [(-1, 0, 1), (0, 0, 0), (1.0, 0, 0), (True, 0, 0)]:
            with self.assertRaises(ValueError):
                missing_label_bounds(*args)
        for rows in [[(False, None, F(1, 2))],
                     [(True, True, F(0))],
                     [(True, True, F(2))],
                     [(True, True, 0.5)],
                     [(True, None, F(1, 2))]]:
            with self.assertRaises(ValueError):
                weighted_audit_rate(rows)


if __name__ == "__main__":
    unittest.main()
