"""Independent deletion-subset reference for source-cluster identification.

Synthetic tiny frames only. Exponential enumeration; not an empirical AI result.
Run in verified free hosted CI, not on the user's laptop.
"""
from fractions import Fraction
from itertools import combinations, product

from research.archival_bounds import Counts
from research.paired_archival_oracle import MissingCase
from research.paired_archival_source_cluster_oracle import source_cluster_bounds


def deletion_feasible_set(m, records, observed, budget):
    """Enumerate the union of assignments surviving deletion of <=budget sources.

    Intentionally does NOT compute violated-source counts for an assignment.
    """
    sources = tuple(dict.fromkeys(r[3] for r in records))
    survivors = set()
    for size in range(budget + 1):
        for removed in combinations(sources, size):
            removed = set(removed)
            retained = [(i, j, p) for i, j, p, s in records if s not in removed]
            for truth in product((0, 1), repeat=m):
                if all(truth[i] == y for i, y in observed) and all(
                    (truth[i] ^ truth[j]) == p for i, j, p in retained
                ):
                    survivors.add(truth)
    return survivors


def independent_extrema(a, b, missing, feasible):
    ka = a.accepted + sum(int(c.accept_a) for c in missing)
    kb = b.accepted + sum(int(c.accept_b) for c in missing)
    if ka == 0 or kb == 0:
        return None, 0, len(feasible)
    vals = []
    for truth in feasible:
        ea = a.errors + sum(int(c.accept_a and c.predict_a != y)
                            for c, y in zip(missing, truth))
        eb = b.errors + sum(int(c.accept_b and c.predict_b != y)
                            for c, y in zip(missing, truth))
        vals.append(Fraction(ea, ka) - Fraction(eb, kb))
    return (min(vals), max(vals)) if vals else None, len(vals), 0


def test_exhaustive_deletion_equivalence():
    # Enumerate all 3^3 record-presence/source variants for two distinct
    # assertions, plus inconsistent duplicates and both hard-label states.
    missing = (MissingCase(0, True, 1, True),
               MissingCase(1, True, 0, True))
    a, b = Counts(2, 2, 1, 0), Counts(2, 2, 1, 1)
    atoms = ((0, 1, 0, "s"), (0, 1, 1, "s"),
             (0, 0, 1, "t"))
    for mask in product((0, 1), repeat=len(atoms)):
        records = tuple(r for keep, r in zip(mask, atoms) if keep)
        for observed in ((), ((0, 0),), ((0, 1),),
                         ((0, 0), (0, 1))):
            for budget in range(len({r[3] for r in records}) + 1):
                feasible = deletion_feasible_set(2, records, observed, budget)
                sharp, defined, undefined = independent_extrema(
                    a, b, missing, feasible)
                actual = source_cluster_bounds(
                    a, b, missing, records, budget, observed)
                assert actual == {
                    "sharp": sharp,
                    "feasible_assignments": len(feasible),
                    "defined_assignments": defined,
                    "undefined_assignments": undefined,
                }


def test_full_deletion_preserves_hard_labels_and_undefined_risk():
    missing = (MissingCase(0, False, 1, False),)
    a, b = Counts(1, 1, 0, 0), Counts(1, 1, 0, 0)
    records = ((0, 0, 1, "unreliable"),)
    feasible = deletion_feasible_set(1, records, ((0, 1),), 1)
    assert feasible == {(1,)}
    actual = source_cluster_bounds(a, b, missing, records, 1, ((0, 1),))
    assert actual["sharp"] is None
    assert actual["feasible_assignments"] == 1
    assert actual["undefined_assignments"] == 1


def test_deletion_does_not_make_contradictory_hard_labels_optional():
    records = ((0, 0, 1, "s"),)
    assert deletion_feasible_set(
        1, records, ((0, 0), (0, 1)), 1) == set()
