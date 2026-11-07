"""Exact conditional denominator-failure diagnostic for Protocol 120.

No simulation, inference, or confidence-interval coverage guarantee is provided.
The diagnostic matches independent, uniform, with-replacement lineage resampling
within each positive-weight physics family.
"""
from collections import defaultdict
from math import exp, log1p, isfinite, prod


def denominator_failure_probability(rows, weights):
    """Return exact conditional failure probability and family diagnostics.

    Each row supplies physics_family, lineage_id, intervention_id, system_id,
    and accepted. Every intervention must have exactly two distinct system rows.
    Zero-weight families are validated but excluded from the failure probability.
    """
    weights = dict(weights)
    if not weights or any(type(w) not in (int, float) or not isfinite(w) or w < 0
                          for w in weights.values()) or sum(weights.values()) <= 0:
        raise ValueError("invalid weights")
    pairs = defaultdict(dict)
    lineages = defaultdict(set)
    for row in rows:
        f, l, i, s, a = (row[k] for k in
                         ("physics_family", "lineage_id", "intervention_id",
                          "system_id", "accepted"))
        if any(type(v) is not str or not v for v in (f, l, i, s)):
            raise ValueError("invalid identifier")
        if f not in weights or type(a) is not bool:
            raise ValueError("unknown family or invalid acceptance")
        key = (f, l, i)
        if s in pairs[key]:
            raise ValueError("duplicate system record")
        pairs[key][s] = a
        lineages[f].add(l)
    if not pairs:
        raise ValueError("empty dataset")
    system_sets = {frozenset(p) for p in pairs.values()}
    if len(system_sets) != 1 or len(next(iter(system_sets))) != 2:
        raise ValueError("incomplete or inconsistent system pairs")
    qualifying = defaultdict(set)
    for (f, l, _), pair in pairs.items():
        if all(pair.values()):
            qualifying[f].add(l)
    details = []
    for f in sorted(f for f, w in weights.items() if w > 0):
        n = len(lineages[f])
        if n < 2:
            raise ValueError("insufficient lineages in positive-weight family")
        k = len(qualifying[f])
        q = ((n - k) / n) ** n
        details.append({"physics_family": f, "lineages": n,
                        "joint_accepting_lineages": k,
                        "undefined_probability": q})
    # Products of per-family success probabilities, matching Protocol 120.
    q_any = 1 - prod(1 - d["undefined_probability"] for d in details)
    return {"conditional_undefined_probability": q_any,
            "families": details,
            "interpretation": "conditional resampling diagnostic; not CI coverage"}
