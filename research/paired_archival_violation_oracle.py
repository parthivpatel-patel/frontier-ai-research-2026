"""Exact exhaustive reference for record-budget parity sensitivity.

Small-frame oracle only; exponential in the number of unresolved labels.
Not a scalable optimizer, statistical confidence interval, or novelty claim.
Run on a free hosted runner after verifying account entitlement.
"""
from fractions import Fraction
from itertools import product

from research.archival_bounds import Counts
from research.paired_archival_oracle import MissingCase


def violation_budget_bounds(a, b, missing, records=(), budget=0):
    """Sharp finite-frame contrast over labels violating <= budget records.

    Each record is counted separately, including duplicates. An empty feasible
    set returns sharp=None and feasible_assignments=0. A zero acceptance
    denominator returns sharp=None with undefined_assignments counted.
    """
    missing = tuple(missing)
    records = tuple(records)
    if not isinstance(a, Counts) or not isinstance(b, Counts):
        raise TypeError("Expected Counts instances")
    if a.n != b.n or a.m != b.m or a.m != len(missing):
        raise ValueError("Sampling frames disagree")
    if any(not isinstance(c, MissingCase) for c in missing):
        raise TypeError("Expected MissingCase instances")
    if type(budget) is not int or budget < 0 or budget > len(records):
        raise ValueError("Budget must be an integer from zero to record count")
    for edge in records:
        if not isinstance(edge, (tuple, list)) or len(edge) != 3:
            raise ValueError("Expected (i,j,parity) records")
        i, j, d = edge
        if any(type(x) is not int for x in (i, j, d)) or not (0 <= i < len(missing) and 0 <= j < len(missing) and d in (0, 1)):
            raise ValueError("Invalid parity record")
    ka = a.accepted + sum(c.accept_a for c in missing)
    kb = b.accepted + sum(c.accept_b for c in missing)
    values = []
    feasible = undefined = 0
    for labels in product((0, 1), repeat=len(missing)):
        violations = sum((labels[i] ^ labels[j]) != d for i, j, d in records)
        if violations > budget:
            continue
        feasible += 1
        if ka == 0 or kb == 0:
            undefined += 1
            continue
        ea = a.errors + sum(int(c.accept_a and c.predict_a != y) for c, y in zip(missing, labels))
        eb = b.errors + sum(int(c.accept_b and c.predict_b != y) for c, y in zip(missing, labels))
        values.append(Fraction(ea, ka) - Fraction(eb, kb))
    return {"sharp": (min(values), max(values)) if values else None,
            "feasible_assignments": feasible,
            "defined_assignments": len(values),
            "undefined_assignments": undefined}


if __name__ == "__main__":
    import unittest
    from research.paired_archival_parity import sharp_paired_difference_parity

    class ViolationBudgetOracleTests(unittest.TestCase):
        def setUp(self):
            self.a = self.b = Counts(0, 2, 0, 0)
            self.cases = (MissingCase(0, True, 1, True),
                          MissingCase(1, True, 0, True))

        def test_conflicting_records_require_repair(self):
            edges = ((0, 1, 0), (0, 1, 1))
            self.assertEqual(violation_budget_bounds(self.a, self.b, self.cases, edges, 0)["feasible_assignments"], 0)
            self.assertEqual(violation_budget_bounds(self.a, self.b, self.cases, edges, 1)["feasible_assignments"], 4)

        def test_duplicates_consume_individual_budget(self):
            edges = ((0, 1, 0), (0, 1, 0))
            self.assertEqual(violation_budget_bounds(self.a, self.b, self.cases, edges, 1)["feasible_assignments"], 2)
            self.assertEqual(violation_budget_bounds(self.a, self.b, self.cases, edges, 2)["feasible_assignments"], 4)

        def test_nested_and_unrestricted(self):
            edges = ((0, 1, 0), (0, 1, 1))
            outputs = [violation_budget_bounds(self.a, self.b, self.cases, edges, k) for k in range(3)]
            self.assertEqual(outputs[0]["sharp"], None)
            self.assertTrue(outputs[1]["sharp"][0] >= outputs[2]["sharp"][0])
            self.assertTrue(outputs[1]["sharp"][1] <= outputs[2]["sharp"][1])
            self.assertEqual(outputs[2]["sharp"], violation_budget_bounds(self.a, self.b, self.cases)["sharp"])

        def test_zero_budget_matches_parity_solver(self):
            edges = ((0, 1, 1),)
            expected = sharp_paired_difference_parity(self.a, self.b, self.cases, edges)["sharp"]
            self.assertEqual(violation_budget_bounds(self.a, self.b, self.cases, edges)["sharp"], expected)

        def test_undefined_denominator(self):
            a = Counts(0, 2, 0, 0)
            b = Counts(0, 2, 0, 0)
            cases = (MissingCase(0, False, 1, True), MissingCase(1, False, 0, True))
            result = violation_budget_bounds(a, b, cases)
            self.assertIsNone(result["sharp"])
            self.assertEqual(result["undefined_assignments"], 4)

    unittest.main()
