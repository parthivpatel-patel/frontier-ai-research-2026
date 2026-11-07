"""Protocol 121 analytic preflight for paired, heldout bootstrap inputs.

This is a deterministic eligibility diagnostic, not a coverage guarantee.
Call Protocol 113 admission separately before using this with scientific data.
"""
from collections import defaultdict
from math import isfinite, prod


def analytic_preflight(rows, weights, systems=("A", "B"), *,
                       max_undefined_fraction=0.01):
    records = list(rows)
    weights = dict(weights)
    systems = tuple(systems)
    if len(systems) != 2 or any(type(s) is not str or not s for s in systems) or len(set(systems)) != 2:
        raise ValueError("exactly two distinct system IDs required")
    if not weights or any(type(f) is not str or not f or type(w) not in (int, float)
                          or not isfinite(w) or w < 0 for f, w in weights.items()) or sum(weights.values()) <= 0:
        raise ValueError("invalid family weights")
    if type(max_undefined_fraction) not in (int, float) or not isfinite(max_undefined_fraction) or not 0 <= max_undefined_fraction <= 1:
        raise ValueError("invalid threshold")
    if not records:
        raise ValueError("empty population")
    pairs = defaultdict(dict)
    lineages = defaultdict(set)
    for row in records:
        f, l, i, s = (row[k] for k in ("physics_family", "lineage_id", "intervention_id", "system_id"))
        a, u = row["accepted"], row["response_unsafe"]
        if any(type(v) is not str or not v for v in (f, l, i, s)):
            raise ValueError("invalid identifier")
        if f not in weights or s not in systems:
            raise ValueError("unknown family or system")
        if type(a) is not bool or (type(u) is not bool if a else u is not None):
            raise ValueError("invalid acceptance or unsafe label")
        key = (f, l, i)
        if s in pairs[key]:
            raise ValueError("duplicate record")
        pairs[key][s] = (a, u)
        lineages[f].add(l)
    if any(set(pair) != set(systems) for pair in pairs.values()):
        raise ValueError("missing counterpart")
    qualifying = defaultdict(set)
    for (f, l, _), pair in pairs.items():
        if all(pair[s][0] for s in systems):
            qualifying[f].add(l)
    details = []
    for f in sorted(f for f, w in weights.items() if w > 0):
        n = len(lineages[f])
        if n < 2:
            raise ValueError("insufficient lineages")
        k = len(qualifying[f])
        q = ((n-k)/n)**n
        details.append({"physics_family": f, "lineages": n,
                        "joint_accepting_lineages": k, "undefined_probability": q})
    q_any = 1 - prod(1 - d["undefined_probability"] for d in details)
    original_defined = all(d["joint_accepting_lineages"] > 0 for d in details)
    return {"schema_version": 1, "conditional_undefined_probability": q_any,
            "families": details, "original_defined": original_defined,
            "interval_eligible": original_defined and q_any <= max_undefined_fraction,
            "threshold": max_undefined_fraction,
            "interpretation": "analytic conditional eligibility only; no coverage guarantee"}
