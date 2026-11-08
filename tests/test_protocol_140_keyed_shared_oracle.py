"""Protocol 140 preregistered exact keyed-lineage contract checks."""
from fractions import Fraction
import pytest
from research.protocol_140_keyed_shared_oracle import keyed_shared_failure_probability as p


def test_aligned_acceptance():
    assert p([(1, {"a": True, "b": False}),
              (1, {"a": True, "b": False})]) == Fraction(1, 4)


def test_complementary_acceptance():
    assert p([(1, {"a": True, "b": False}),
              (1, {"a": False, "b": True})]) == Fraction(1, 2)


def test_permuting_insertion_order_does_not_change_result():
    first = [(1, {"a": True, "b": False, "c": False}),
             (1, {"a": False, "b": True, "c": False})]
    reordered = [(1, {"c": False, "b": False, "a": True}),
                 (1, {"b": True, "c": False, "a": False})]
    assert p(first) == p(reordered)


def test_zero_weight_ignored():
    assert p([(1, {"a": True, "b": False}),
              (0, {"a": False, "b": True})]) == Fraction(1, 4)


def test_positive_weight_rescaling_invariant():
    families = [(1, {"a": True, "b": False}),
                (2, {"a": False, "b": True})]
    scaled = [(Fraction(1, 3), families[0][1]),
              (Fraction(2, 3), families[1][1])]
    assert p(families) == p(scaled)


@pytest.mark.parametrize("families", [
    [], [(0, {"a": True, "b": False})],
    [(1, {"a": True})],
    [(1, {"a": True, "b": 1})],
    [(-1, {"a": True, "b": False})],
    [(1.0, {"a": True, "b": False})],
    [(1, {"a": True, "b": False}), (1, {"a": True, "c": False})],
])
def test_invalid_contracts_rejected(families):
    with pytest.raises(ValueError):
        p(families)
