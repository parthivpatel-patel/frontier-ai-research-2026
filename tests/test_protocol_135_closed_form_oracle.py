"""Protocol 135: deterministic tests of closed-form denominator probabilities.

These are authored tests only until verified on an eligible free cloud runner.
"""
from fractions import Fraction
from itertools import product

import pytest

from research.protocol_135_closed_form_oracle import closed_form_undefined


def independent_enumeration(families):
    all_defined = Fraction(1)
    for weight, flags in families:
        if not weight:
            continue
        n = len(flags)
        count = sum(any(flags[i] for i in draw) for draw in product(range(n), repeat=n))
        all_defined *= Fraction(count, n ** n)
    return 1 - all_defined


@pytest.mark.parametrize("families", [
    [(1, (True, False))],
    [(1, (True, True))],
    [(1, (False, False))],
    [(1, (True, False)), (1, (True, True, False))],
    [(Fraction(3, 2), (True, False)), (0, (False, False))],
    [(1, (True, False, False)), (2, (False, True, True))],
])
def test_matches_independent_small_enumeration(families):
    assert closed_form_undefined(families) == independent_enumeration(families)


def test_exact_two_family_reference():
    assert closed_form_undefined([
        (1, (True, False)),
        (1, (True, True, False)),
    ]) == Fraction(5, 18)


def test_large_lineage_family_without_enumeration():
    flags = (True,) + (False,) * 99
    assert closed_form_undefined([(1, flags)]) == Fraction(99, 100) ** 100


@pytest.mark.parametrize("families", [
    [],
    [(0, (True, False))],
    [(-1, (True, False))],
    [(1.0, (True, False))],
    [(True, (True, False))],
    [(1, (True,))],
    [(1, (1, False))],
])
def test_invalid_inputs(families):
    with pytest.raises(ValueError):
        closed_form_undefined(families)
