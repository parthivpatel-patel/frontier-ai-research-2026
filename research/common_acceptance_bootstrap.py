"""Descriptive common-acceptance, family-stratified lineage bootstrap.

Input MUST first pass Protocol 113 admission. This module performs an additional
complete-pair check, but does not certify adjudicator independence or chronology.
No causal or novelty inference is implied.
"""
from collections import defaultdict
from math import isfinite
from random import Random


def common_acceptance_bootstrap(rows, weights, systems=("A", "B"), *,
                                seed=0, replicates=2000,
                                max_undefined_fraction=0.01,
                                min_lineages_per_family=2):
    """Bootstrap the weighted within-family joint-acceptance paired difference.

    Rows are mappings with physics_family, lineage_id, intervention_id,
    system_id, accepted and response_unsafe. Abstentions use None for unsafe.
    Undefined original or resampled denominators never become zero estimates.
    """
    records = list(rows)
    weights = dict(weights)
    systems = tuple(systems)
    if len(systems) != 2 or len(set(systems)) != 2:
        raise ValueError("two distinct systems required")
    if not records or not weights or any(
        type(w) not in (int, float) or not isfinite(w) or w < 0
        for w in weights.values()
    ) or sum(weights.values()) <= 0:
        raise ValueError("invalid weights or empty population")
    if type(seed) is not int or type(replicates) is not int or replicates < 1:
        raise ValueError("invalid bootstrap configuration")
    if type(min_lineages_per_family) is not int or min_lineages_per_family < 2:
        raise ValueError("at least two lineages per positive-weight family required")
    if type(max_undefined_fraction) not in (int, float) or not (
        isfinite(max_undefined_fraction) and 0 <= max_undefined_fraction <= 1
    ):
        raise ValueError("invalid undefined fraction tolerance")

    pairs = defaultdict(dict)
    lineages = defaultdict(set)
    for row in records:
        family, lineage, intervention = (
            row["physics_family"], row["lineage_id"], row["intervention_id"]
        )
        system, accepted, unsafe = (
            row["system_id"], row["accepted"], row["response_unsafe"]
        )
        if any(type(v) is not str or not v for v in
               (family, lineage, intervention, system)):
            raise ValueError("invalid identifier")
        if family not in weights or system not in systems:
            raise ValueError("unknown family or system")
        if type(accepted) is not bool or (
            type(unsafe) is not bool if accepted else unsafe is not None
        ):
            raise ValueError("invalid acceptance/unsafe semantics")
        key = (family, lineage, intervention)
        if system in pairs[key]:
            raise ValueError("duplicate system record")
        pairs[key][system] = (accepted, unsafe)
        lineages[family].add(lineage)
    if any(set(p) != set(systems) for p in pairs.values()):
        raise ValueError("missing system counterpart")
    active = sorted(f for f, w in weights.items() if w > 0)
    if any(len(lineages[f]) < min_lineages_per_family for f in active):
        raise ValueError("insufficient independent lineages")

    by_lineage = defaultdict(list)
    for (family, lineage, intervention), pair in pairs.items():
        za, ua = pair[systems[0]]
        zb, ub = pair[systems[1]]
        by_lineage[(family, lineage)].append(
            (int(za and zb), int(ua) - int(ub) if za and zb else 0)
        )

    def contrast(multiplicity):
        total = 0.0
        denom_weights = sum(weights[f] for f in active)
        for family in active:
            joint = difference = 0
            for lineage in sorted(lineages[family]):
                n = multiplicity.get((family, lineage), 0)
                for accepted, delta in by_lineage[(family, lineage)]:
                    joint += n * accepted
                    difference += n * delta
            if joint == 0:
                return None
            total += weights[family] / denom_weights * difference / joint
        return total

    original = {(f, l): 1 for f in active for l in lineages[f]}
    point = contrast(original)
    rng = Random(seed)
    draws = []
    undefined = 0
    for _ in range(replicates):
        multiplicity = defaultdict(int)
        for family in active:
            ids = sorted(lineages[family])
            for _ in ids:
                multiplicity[(family, ids[rng.randrange(len(ids))])] += 1
        estimate = contrast(multiplicity)
        if estimate is None:
            undefined += 1
        else:
            draws.append(estimate)
    fraction = undefined / replicates
    interval = None
    if point is not None and draws and fraction <= max_undefined_fraction:
        ordered = sorted(draws)
        def quantile(p):
            index = (len(ordered) - 1) * p
            lo = int(index)
            hi = min(lo + 1, len(ordered) - 1)
            return ordered[lo] + (index - lo) * (ordered[hi] - ordered[lo])
        interval = (quantile(.025), quantile(.975))
    return {
        "estimand": "common_acceptance_paired_difference",
        "point": point, "ci95": interval,
        "defined_replicates": len(draws),
        "undefined_replicates": undefined,
        "undefined_fraction": fraction,
        "replicates": replicates,
        "sampling_unit": "composite physics-family/lineage",
        "interpretation": "descriptive conditional percentile interval; not causal",
    }
