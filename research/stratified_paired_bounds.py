"""Exact stratified paired selective-risk identification bounds.

This is a reference evaluator, not a confidence interval or a claim of novelty.
Each record is (stratum, accept_a, accept_b, unsafe_label), where an
unsafe_label is True, False, or None (unadjudicated).
"""
from fractions import Fraction


def stratified_bounds(records, weights=None):
    """Return per-stratum and optionally fixed-mixture sharp bounds.

    All strata must be comparable (both methods accept at least one record).
    Rejects empty data, non-boolean decisions, invalid labels and weights.
    """
    records = list(records)
    if not records:
        raise ValueError("at least one record required")
    groups = {}
    for record in records:
        if not isinstance(record, (tuple, list)) or len(record) != 4:
            raise ValueError("each record must have four fields")
        family, a, b, label = record
        if not isinstance(family, str) or not family:
            raise ValueError("nonempty string family required")
        if type(a) is not bool or type(b) is not bool:
            raise TypeError("acceptance decisions must be boolean")
        if label is not None and type(label) is not bool:
            raise TypeError("unsafe label must be boolean or None")
        groups.setdefault(family, []).append((a, b, label))
    bounds = {}
    for family, rows in groups.items():
        na = sum(a for a, _, _ in rows)
        nb = sum(b for _, b, _ in rows)
        if not na or not nb:
            raise ValueError("noncomparable stratum: " + family)
        lower = upper = Fraction(0)
        for a, b, label in rows:
            coefficient = Fraction(int(a), na) - Fraction(int(b), nb)
            if label is None:
                lower += min(coefficient, 0)
                upper += max(coefficient, 0)
            elif label:
                lower += coefficient
                upper += coefficient
        bounds[family] = (lower, upper)
    if weights is None:
        return bounds, None
    if not isinstance(weights, dict) or set(weights) != set(groups):
        raise ValueError("weights must cover exactly the observed strata")
    parsed = {}
    for family, value in weights.items():
        if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
            raise TypeError("weights must be nonnegative exact rationals")
        weight = Fraction(value)
        if weight < 0:
            raise ValueError("negative mixture weight")
        parsed[family] = weight
    if sum(parsed.values()) != 1:
        raise ValueError("mixture weights must sum to one")
    return bounds, (
        sum((parsed[k] * bounds[k][0] for k in groups), Fraction(0)),
        sum((parsed[k] * bounds[k][1] for k in groups), Fraction(0)),
    )
