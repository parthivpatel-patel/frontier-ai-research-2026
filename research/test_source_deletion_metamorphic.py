"""Metamorphic checks for the independent source-deletion oracle.

Tiny synthetic examples only; designed for free hosted CI.
"""
from itertools import product

from research.test_source_deletion_independent import deletion_feasible_set


def test_source_renaming_is_invariant():
    records = ((0, 1, 0, "a"), (1, 2, 1, "a"), (0, 2, 1, "b"))
    renamed = tuple((i, j, p, {"a": "z", "b": "q"}[s])
                    for i, j, p, s in records)
    for budget in (0, 1, 2):
        for observed in ((), ((0, 0),), ((2, 1),)):
            assert deletion_feasible_set(3, records, observed, budget) == (
                deletion_feasible_set(3, renamed, observed, budget)
            )


def test_deletion_budget_monotonicity_and_unrestricted_limit():
    atoms = ((0, 1, 0, "a"), (1, 2, 1, "b"), (0, 2, 0, "a"))
    for presence in product((False, True), repeat=len(atoms)):
        records = tuple(r for keep, r in zip(presence, atoms) if keep)
        for observed in ((), ((0, 1),), ((0, 0), (0, 1))):
            source_count = len({r[3] for r in records})
            sets = [deletion_feasible_set(3, records, observed, k)
                    for k in range(source_count + 1)]
            assert all(left <= right for left, right in zip(sets, sets[1:]))
            unrestricted = {
                truth for truth in product((0, 1), repeat=3)
                if all(truth[i] == y for i, y in observed)
            }
            assert sets[-1] == unrestricted


def test_duplicate_record_invariance():
    records = ((0, 1, 1, "source"), (1, 2, 0, "other"))
    for budget in (0, 1, 2):
        assert deletion_feasible_set(3, records, (), budget) == (
            deletion_feasible_set(3, records + (records[0],), (), budget)
        )
