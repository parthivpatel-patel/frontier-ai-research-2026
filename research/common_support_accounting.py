"""Descriptive common-support accounting for paired AI verification outcomes.

Standard-library only. This module does not establish causal effects or novelty.
Rows are dictionaries with keys: intervention_key, system, accepted, unsafe.
unsafe must be a boolean for accepted responses and None for abstentions.
Shared-truth, provenance, lineage and split admission must be independently
validated BEFORE calling summarize; this function does not replace Protocol 113.
"""
from collections import defaultdict


def summarize(rows, systems=("A", "B")):
    """Return acceptance cells and descriptive selective-risk estimands.

    Raises ValueError on malformed, duplicate, or unmatched system records.
    Undefined risks are represented by None, never zero.
    """
    if len(systems) != 2 or systems[0] == systems[1]:
        raise ValueError("two distinct systems required")
    pairs = defaultdict(dict)
    for row in rows:
        key = row["intervention_key"]
        system = row["system"]
        accepted = row["accepted"]
        unsafe = row["unsafe"]
        if system not in systems or not isinstance(accepted, bool):
            raise ValueError("invalid system or acceptance")
        if not isinstance(key, str) or not key:
            raise ValueError("invalid intervention key")
        if accepted and not isinstance(unsafe, bool):
            raise ValueError("accepted response requires boolean unsafe")
        if not accepted and unsafe is not None:
            raise ValueError("abstention cannot have unsafe label")
        if system in pairs[key]:
            raise ValueError("duplicate system observation")
        pairs[key][system] = (accepted, unsafe)
    if not pairs:
        raise ValueError("empty evaluation population")
    if any(set(pair) != set(systems) for pair in pairs.values()):
        raise ValueError("missing system counterpart")
    a, b = systems
    counts = {"11": 0, "10": 0, "01": 0, "00": 0}
    accepted_n = {a: 0, b: 0}
    unsafe_n = {a: 0, b: 0}
    paired_diff = 0
    for pair in pairs.values():
        za, ua = pair[a]
        zb, ub = pair[b]
        counts[f"{int(za)}{int(zb)}"] += 1
        for s in systems:
            z, u = pair[s]
            accepted_n[s] += int(z)
            unsafe_n[s] += int(z and u)
        if za and zb:
            paired_diff += int(ua) - int(ub)
    n = len(pairs)
    return {
        "n": n,
        "acceptance_cells": counts,
        "coverage": {s: accepted_n[s] / n for s in systems},
        "accepted_n": accepted_n,
        "selective_risk": {
            s: unsafe_n[s] / accepted_n[s] if accepted_n[s] else None
            for s in systems
        },
        "common_support_coverage": counts["11"] / n,
        "common_support_difference": (
            paired_diff / counts["11"] if counts["11"] else None
        ),
        "interpretation": "descriptive; not causal",
    }
