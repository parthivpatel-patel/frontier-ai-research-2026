"""Protocol 140: keyed shared-lineage bootstrap probability, exact arithmetic.

This is a reference implementation for a *hypothetical* shared-key design.
It does not establish that the production sampler uses this design.
"""
from fractions import Fraction
from itertools import combinations


def keyed_shared_failure_probability(families):
    """Compute P(any positive-weight family has no accepted draw).

    families: iterable of (nonnegative exact weight, mapping lineage_id -> bool).
    All families, including zero-weight families, must have the same lineage IDs.
    Exactly n iid uniform keys are drawn with replacement and reused by every
    positive-weight family. A key is a stable identifier, not an array position.
    """
    families = tuple(families)
    if not families:
        raise ValueError("at least one family required")
    key_set = None
    included = []
    for weight, acceptance in families:
        if type(weight) not in (int, Fraction) or weight < 0:
            raise ValueError("weight must be nonnegative int or Fraction")
        if not isinstance(acceptance, dict):
            raise ValueError("acceptance must map lineage keys to booleans")
        try:
            keys = frozenset(acceptance)
        except TypeError as exc:
            raise ValueError("lineage keys must be hashable") from exc
        if len(keys) < 2 or any(type(v) is not bool for v in acceptance.values()):
            raise ValueError("at least two lineage keys with boolean flags required")
        if key_set is None:
            key_set = keys
        elif keys != key_set:
            raise ValueError("all families must have exactly the same lineage IDs")
        if weight > 0:
            included.append(acceptance)
    if not included:
        raise ValueError("at least one positive-weight family required")
    n = len(key_set)
    probability = Fraction(0)
    for size in range(1, len(included) + 1):
        for subset in combinations(included, size):
            rejected = sum(
                all(not family[key] for family in subset) for key in key_set
            )
            term = Fraction(rejected, n) ** n
            probability += term if size % 2 else -term
    assert 0 <= probability <= 1
    return probability
