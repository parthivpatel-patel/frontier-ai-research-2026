"""Exact small-frame source-cluster sensitivity oracle.

Synthetic validation reference only. Exponential in missing labels; not a
scalable solver, confidence interval, or empirical finding.
"""
from fractions import Fraction
from itertools import product

from research.archival_bounds import Counts
from research.paired_archival_oracle import MissingCase


def source_cluster_bounds(a, b, missing, records=(), budget=0, observed=()):
    """Return sharp risk-difference extrema under <=budget violated sources.

    records: (i, j, parity, source_id), including duplicate records.
    observed: (missing_index, binary_label) hard equalities.
    Empty feasible set and undefined acceptance denominator are distinguished.
    """
    missing, records, observed = tuple(missing), tuple(records), tuple(observed)
    if not isinstance(a, Counts) or not isinstance(b, Counts):
        raise TypeError("Expected Counts instances")
    if a.n != b.n or a.m != b.m or a.m != len(missing):
        raise ValueError("Sampling frames disagree")
    if any(not isinstance(c, MissingCase) for c in missing):
        raise TypeError("Expected MissingCase instances")
    sources = set()
    for record in records:
        if not isinstance(record, (tuple, list)) or len(record) != 4:
            raise ValueError("Expected (i,j,parity,source) records")
        i, j, parity, source = record
        if any(type(v) is not int for v in (i, j, parity)):
            raise ValueError("Indices and parity must be integers")
        if not (0 <= i < len(missing) and 0 <= j < len(missing) and parity in (0, 1)):
            raise ValueError("Invalid parity record")
        try:
            hash(source)
        except TypeError as exc:
            raise ValueError("Source identifiers must be hashable") from exc
        sources.add(source)
    if type(budget) is not int or not 0 <= budget <= len(sources):
        raise ValueError("Budget must be an integer between zero and source count")
    for item in observed:
        if not isinstance(item, (tuple, list)) or len(item) != 2:
            raise ValueError("Expected (index,label) observed equalities")
        i, y = item
        if type(i) is not int or type(y) is not int or not 0 <= i < len(missing) or y not in (0, 1):
            raise ValueError("Invalid observed equality")

    ka = a.accepted + sum(c.accept_a for c in missing)
    kb = b.accepted + sum(c.accept_b for c in missing)
    values = []
    feasible = undefined = 0
    for labels in product((0, 1), repeat=len(missing)):
        if any(labels[i] != y for i, y in observed):
            continue
        bad = {source for i, j, parity, source in records
               if (labels[i] ^ labels[j]) != parity}
        if len(bad) > budget:
            continue
        feasible += 1
        if ka == 0 or kb == 0:
            undefined += 1
            continue
        ea = a.errors + sum(int(c.accept_a and c.predict_a != y)
                            for c, y in zip(missing, labels))
        eb = b.errors + sum(int(c.accept_b and c.predict_b != y)
                            for c, y in zip(missing, labels))
        values.append(Fraction(ea, ka) - Fraction(eb, kb))
    return {"sharp": (min(values), max(values)) if values else None,
            "feasible_assignments": feasible,
            "defined_assignments": len(values),
            "undefined_assignments": undefined}
