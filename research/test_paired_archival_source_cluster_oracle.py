"""Small synthetic adversarial checks for source-cluster sensitivity."""
from fractions import Fraction
import pytest

from research.archival_bounds import Counts
from research.paired_archival_oracle import MissingCase
from research.paired_archival_source_cluster_oracle import source_cluster_bounds
from research.paired_archival_violation_oracle import violation_budget_bounds


def fixture():
    a = b = Counts(0, 3, 0, 0)
    missing = (MissingCase(0, True, 1, True),
               MissingCase(1, True, 0, True),
               MissingCase(0, True, 0, True))
    return a, b, missing


def test_duplicate_same_source_is_free():
    a, b, m = fixture()
    e = ((0, 1, 0, "a"),)
    assert source_cluster_bounds(a, b, m, e, 1) == source_cluster_bounds(a, b, m, e * 3, 1)


def test_distinct_records_one_source_vs_two():
    a, b, m = fixture()
    shared = ((0, 1, 0, "a"), (1, 2, 0, "a"))
    split = ((0, 1, 0, "a"), (1, 2, 0, "b"))
    assert source_cluster_bounds(a, b, m, shared, 1)["feasible_assignments"] == 8
    assert source_cluster_bounds(a, b, m, split, 1)["feasible_assignments"] < 8


def test_contradictions_and_observed_hard_label():
    a, b, m = fixture()
    edges = ((0, 1, 0, "a"), (0, 1, 1, "a"))
    assert source_cluster_bounds(a, b, m, edges, 0)["feasible_assignments"] == 0
    assert source_cluster_bounds(a, b, m, edges, 1)["feasible_assignments"] == 8
    assert source_cluster_bounds(a, b, m, ((0, 1, 1, "a"),), 0, ((0, 0), (1, 0)))["feasible_assignments"] == 0
    assert source_cluster_bounds(a, b, m, ((0, 1, 1, "a"),), 1, ((0, 0), (1, 0)))["feasible_assignments"] == 2


def test_nesting_and_record_budget_containment():
    a, b, m = fixture()
    edges = ((0, 1, 0, "a"), (1, 2, 0, "a"), (0, 2, 1, "b"))
    intervals = [source_cluster_bounds(a, b, m, edges, k)["sharp"] for k in range(3)]
    for narrow, wide in zip(intervals, intervals[1:]):
        if narrow is not None:
            assert wide[0] <= narrow[0] <= narrow[1] <= wide[1]
    assert intervals[-1] == source_cluster_bounds(a, b, m)["sharp"]
    for k in range(3):
        rec = violation_budget_bounds(a, b, m, tuple(e[:3] for e in edges), k)
        src = source_cluster_bounds(a, b, m, edges, k)
        assert rec["feasible_assignments"] <= src["feasible_assignments"]


def test_renaming_and_order_invariance():
    a, b, m = fixture()
    edges = ((0, 1, 0, "a"), (1, 2, 1, "b"))
    renamed = ((1, 2, 1, 99), (0, 1, 0, 42))
    for k in range(3):
        assert source_cluster_bounds(a, b, m, edges, k) == source_cluster_bounds(a, b, m, renamed, k)


def test_empty_observed_and_undefined():
    a, b, m = fixture()
    assert source_cluster_bounds(a, b, m)["feasible_assignments"] == 8
    assert source_cluster_bounds(a, b, m, observed=((0, 0), (0, 1)))["feasible_assignments"] == 0
    assert isinstance(source_cluster_bounds(a, b, m)["sharp"][0], Fraction)
    a0 = Counts(0, 3, 0, 0)
    m0 = tuple(MissingCase(0, False, 0, True) for _ in range(3))
    result = source_cluster_bounds(a0, b, m0)
    assert result["sharp"] is None
    assert result["undefined_assignments"] == 8


@pytest.mark.parametrize("budget", [-1, True, 1.0, 2])
def test_invalid_budget(budget):
    a, b, m = fixture()
    with pytest.raises(ValueError):
        source_cluster_bounds(a, b, m, ((0, 1, 0, "a"),), budget)


def test_partition_coarsening_feasible_counts_and_endpoints():
    """Exhaustively verify partition monotonicity for three distinct records."""
    from itertools import product

    a, b, m = fixture()
    base = ((0, 1, 0), (1, 2, 0), (0, 2, 1))
    # Every possible assignment of three source IDs; canonical relabeling is
    # unnecessary for this small independent reference check.
    for ids in product(range(3), repeat=3):
        refined = tuple((*edge, source) for edge, source in zip(base, ids))
        coarsened = tuple((*edge, 0) for edge in base)
        for k in range(min(len(set(ids)), 1) + 1):
            narrow = source_cluster_bounds(a, b, m, refined, k)
            wide = source_cluster_bounds(a, b, m, coarsened, k)
            assert narrow["feasible_assignments"] <= wide["feasible_assignments"]
            if narrow["sharp"] is not None:
                assert wide["sharp"] is not None
                assert wide["sharp"][0] <= narrow["sharp"][0]
                assert narrow["sharp"][1] <= wide["sharp"][1]


def test_partition_strict_witness_and_zero_budget_invariance():
    a, b, m = fixture()
    split = ((0, 1, 0, "A"), (1, 2, 0, "B"))
    merged = ((0, 1, 0, "C"), (1, 2, 0, "C"))
    assert source_cluster_bounds(a, b, m, split, 1)["feasible_assignments"] < 8
    assert source_cluster_bounds(a, b, m, merged, 1)["feasible_assignments"] == 8
    assert source_cluster_bounds(a, b, m, split, 0) == source_cluster_bounds(a, b, m, merged, 0)


def test_full_source_relaxation_preserves_hard_labels():
    a, b, m = fixture()
    edges = ((0, 1, 0, "A"), (1, 2, 1, "B"))
    observed = ((0, 1),)
    unrestricted = source_cluster_bounds(a, b, m, observed=observed)
    relaxed = source_cluster_bounds(a, b, m, edges, 2, observed)
    assert relaxed == unrestricted
    assert relaxed["feasible_assignments"] == 4
    assert source_cluster_bounds(a, b, m, edges, 2, ((0, 0), (0, 1)))["feasible_assignments"] == 0
