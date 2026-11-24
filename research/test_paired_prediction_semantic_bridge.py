"""Synthetic regression tests; not empirical model evaluation.
Run with pytest research/test_paired_prediction_semantic_bridge.py.
"""
from fractions import Fraction
from itertools import product

import pytest


def direct(a, b, truth):
    def risk(pred):
        errors = [int(p != t) for p, t in zip(pred, truth) if p is not None]
        if not errors:
            raise ValueError("undefined selective risk")
        return Fraction(sum(errors), len(errors))
    return risk(a) - risk(b)


def affine(a, b):
    def coefficients(pred):
        k = sum(p is not None for p in pred)
        if not k:
            raise ValueError("undefined selective risk")
        return (Fraction(sum(p for p in pred if p is not None), k),
                tuple(Fraction(1 - 2*p, k) if p is not None else Fraction(0)
                      for p in pred))
    ca, wa = coefficients(a)
    cb, wb = coefficients(b)
    return ca - cb, tuple(x-y for x,y in zip(wa,wb))


def evaluate(c, w, truth):
    return c + sum(x*t for x,t in zip(w,truth))


@pytest.mark.parametrize("n", [1, 2, 3])
def test_exhaustive_paired_patterns(n):
    patterns = [p for p in product((None, 0, 1), repeat=n)
                if any(x is not None for x in p)]
    truths = list(product((0, 1), repeat=n))
    for a, b in product(patterns, repeat=2):
        c, w = affine(a,b)
        values = []
        for t in truths:
            actual = direct(a,b,t)
            assert actual == evaluate(c,w,t)
            values.append(actual)
        assert min(values) == c + sum(min(0,x) for x in w)
        assert max(values) == c + sum(max(0,x) for x in w)


def test_undefined_denominators():
    for a,b in [((None,), (0,)), ((1,), (None,))]:
        with pytest.raises(ValueError):
            direct(a,b,(0,))
        with pytest.raises(ValueError):
            affine(a,b)


def test_source_budget_fixture():
    a,b = (0,0),(0,1)
    c,w = affine(a,b)
    for budget, expected in [(0, {Fraction(-1,2)}),
                             (1, {Fraction(-1,2), Fraction(1,2)})]:
        feasible = [t for t in product((0,1), repeat=2)
                    if t[0] == 0 and int(t[0] != t[1]) <= budget]
        assert {evaluate(c,w,t) for t in feasible} == expected
        assert {direct(a,b,t) for t in feasible} == expected
    # Contradictory hard labels: no feasible truth, not a point interval.
    feasible = [t for t in product((0,1), repeat=2)
                if t[0] == 0 and t[0] == 1]
    assert not feasible
