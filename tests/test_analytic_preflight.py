"""Synthetic specifications; execution status must be verified in cloud CI."""
import pytest
from research.analytic_preflight import analytic_preflight


def rows(patterns, family="mechanics"):
    out = []
    for idx, (a, b) in enumerate(patterns):
        for system, accepted in (("A", a), ("B", b)):
            out.append({"physics_family": family, "lineage_id": str(idx),
                        "intervention_id": "i", "system_id": system,
                        "accepted": accepted,
                        "response_unsafe": False if accepted else None})
    return out


def test_two_family_counterexample():
    data = rows([(True, True), (False, False)], "f1") + rows([(True, True), (False, False)], "f2")
    result = analytic_preflight(data, {"f1": 1, "f2": 1})
    assert result["conditional_undefined_probability"] == 0.4375
    assert result["original_defined"]
    assert not result["interval_eligible"]


def test_complete_acceptance():
    result = analytic_preflight(rows([(True, True)] * 3), {"mechanics": 1})
    assert result["conditional_undefined_probability"] == 0
    assert result["interval_eligible"]


def test_no_joint_acceptance():
    result = analytic_preflight(rows([(True, False), (False, True)]), {"mechanics": 1})
    assert result["conditional_undefined_probability"] == 1
    assert not result["original_defined"]
    assert not result["interval_eligible"]


def test_order_invariance():
    data = rows([(True, True), (False, False), (True, False)])
    assert analytic_preflight(data, {"mechanics": 1}) == analytic_preflight(list(reversed(data)), {"mechanics": 1})


def test_missing_counterpart():
    with pytest.raises(ValueError):
        analytic_preflight(rows([(True, True), (False, False)])[:-1], {"mechanics": 1})


def test_unknown_system():
    data = rows([(True, True), (False, False)])
    data[0]["system_id"] = "C"
    with pytest.raises(ValueError):
        analytic_preflight(data, {"mechanics": 1})


def test_invalid_unsafe_label():
    data = rows([(True, True), (False, False)])
    data[2]["response_unsafe"] = False
    with pytest.raises(ValueError):
        analytic_preflight(data, {"mechanics": 1})


def test_zero_weight_family_excluded():
    data = rows([(True, True), (True, True)], "f1") + rows([(False, False), (False, False)], "f2")
    result = analytic_preflight(data, {"f1": 1, "f2": 0})
    assert result["conditional_undefined_probability"] == 0
    assert result["interval_eligible"]
