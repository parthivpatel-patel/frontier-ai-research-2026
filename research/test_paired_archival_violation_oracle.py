"""Pytest-discoverable independent checks for the bounded-violation oracle.

No model inference, external data, or nonstandard dependencies are needed.
These tests deliberately avoid importing the oracle's __main__ test suite,
which pytest does not collect on module import.
"""
from fractions import Fraction
from itertools import product

from research.archival_bounds import Counts
from research.paired_archival_oracle import MissingCase
from research.paired_archival_violation_oracle import violation_budget_bounds
from research.paired_archival_parity import sharp_paired_difference_parity


def fixture():
    a = Counts(0, 3, 0, 0)
    b = Counts(0, 3, 0, 0)
    cases = (
        MissingCase(0, True, 1, True),
        MissingCase(1, True, 0, True),
        MissingCase(0, True, 0, True),
    )
    return a, b, cases


def test_contradictory_records_and_minimum_repair():
    a, b, cases = fixture()
    records = ((0, 1, 0), (0, 1, 1))
    assert violation_budget_bounds(a, b, cases, records, 0)["feasible_assignments"] == 0
    assert violation_budget_bounds(a, b, cases, records, 1)["feasible_assignments"] == 8


def test_duplicate_records_have_record_level_cost():
    a, b, cases = fixture()
    records = ((0, 1, 0), (0, 1, 0))
    assert violation_budget_bounds(a, b, cases, records, 1)["feasible_assignments"] == 4
    assert violation_budget_bounds(a, b, cases, records, 2)["feasible_assignments"] == 8


def test_budget_nesting_and_full_relaxation():
    a, b, cases = fixture()
    records = ((0, 1, 0), (1, 2, 1))
    intervals = [violation_budget_bounds(a, b, cases, records, k)["sharp"] for k in range(3)]
    assert all(interval is not None for interval in intervals)
    for narrow, wide in zip(intervals, intervals[1:]):
        assert wide[0] <= narrow[0] <= narrow[1] <= wide[1]
    assert intervals[-1] == violation_budget_bounds(a, b, cases)["sharp"]


def test_zero_budget_agrees_with_component_solver():
    a, b, cases = fixture()
    for records in ((), ((0, 1, 0),), ((0, 1, 1), (1, 2, 0))):
        exact = violation_budget_bounds(a, b, cases, records, 0)["sharp"]
        fast = sharp_paired_difference_parity(a, b, cases, records)["sharp"]
        assert exact == fast


def test_record_permutation_invariance():
    a, b, cases = fixture()
    records = ((0, 1, 0), (1, 2, 1), (0, 2, 0))
    for k in range(4):
        lhs = violation_budget_bounds(a, b, cases, records, k)
        rhs = violation_budget_bounds(a, b, cases, records[::-1], k)
        assert lhs == rhs


def test_exact_rational_endpoints_and_assignment_count():
    a, b, cases = fixture()
    result = violation_budget_bounds(a, b, cases)
    assert result["feasible_assignments"] == 2 ** len(cases)
    assert result["defined_assignments"] == 2 ** len(cases)
    assert all(isinstance(v, Fraction) for v in result["sharp"])


def test_budget_type_and_range_validation():
    a, b, cases = fixture()
    for invalid in (-1, 1, True, 0.0):
        try:
            violation_budget_bounds(a, b, cases, (), invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Accepted invalid budget: {invalid!r}")
