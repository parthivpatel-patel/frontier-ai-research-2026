"""Protocol 111: deterministic paired, family-stratified lineage bootstrap.

Descriptive percentile inference only; no distribution-free safety guarantee.
All thresholds and acceptance decisions must be frozen before calling this module.
"""
from dataclasses import dataclass
from math import isfinite
from random import Random


@dataclass(frozen=True)
class Observation:
    lineage_id: str
    family: str
    intervention_id: str
    system_id: str
    unsafe: bool
    accepted: bool


def _validate(rows, weights, systems):
    if len(systems) != 2 or len(set(systems)) != 2:
        raise ValueError("exactly two distinct systems required")
    if not rows or not weights or any(
        not isinstance(w, (int, float)) or isinstance(w, bool)
        or not isfinite(w) or w < 0 for w in weights.values()
    ) or sum(weights.values()) <= 0:
        raise ValueError("nonempty rows and finite nonnegative weights required")
    seen = set()
    family_by_lineage = {}
    for r in rows:
        if not isinstance(r, Observation):
            raise TypeError("expected Observation")
        if not all(isinstance(v, str) and v for v in
                   (r.lineage_id, r.family, r.intervention_id, r.system_id)):
            raise ValueError("missing identifier")
        if type(r.unsafe) is not bool or type(r.accepted) is not bool:
            raise TypeError("unsafe and accepted must be booleans")
        if r.system_id not in systems or r.family not in weights:
            raise ValueError("unknown system or family")
        key = (r.lineage_id, r.intervention_id, r.system_id)
        if key in seen:
            raise ValueError("duplicate lineage/intervention/system key")
        seen.add(key)
        previous = family_by_lineage.setdefault(r.lineage_id, r.family)
        if previous != r.family:
            raise ValueError("lineage crosses physics families")
    return family_by_lineage


def _contrast(rows, multiplicities, weights, systems):
    risks = {}
    total_weight = sum(weights.values())
    for family, weight in weights.items():
        if weight == 0:
            continue
        for system in systems:
            accepted = unsafe_accepted = 0
            for r in rows:
                if r.family == family and r.system_id == system and r.accepted:
                    n = multiplicities.get(r.lineage_id, 0)
                    accepted += n
                    unsafe_accepted += n * int(r.unsafe)
            if accepted == 0:
                return None
            risks[(family, system)] = unsafe_accepted / accepted
    return sum(
        weight / total_weight *
        (risks[(family, systems[0])] - risks[(family, systems[1])])
        for family, weight in weights.items() if weight > 0
    )


def paired_lineage_bootstrap(rows, weights, systems, *, seed=0,
                             replicates=2000, max_undefined_fraction=0.01,
                             calibration_feasible=True):
    """Return point estimate, descriptive CI, and undefined-replicate diagnostics.

    CI is suppressed if calibration is infeasible, original contrast undefined,
    or too many replicates have undefined denominators. No threshold tuning.
    """
    rows = tuple(rows)
    weights = dict(weights)
    systems = tuple(systems)
    families = _validate(rows, weights, systems)
    if type(seed) is not int or type(replicates) is not int or replicates < 1:
        raise ValueError("invalid seed or replicate count")
    if not isinstance(max_undefined_fraction, (float, int)) or not (
        0 <= max_undefined_fraction <= 1
    ):
        raise ValueError("invalid undefined-fraction threshold")
    if type(calibration_feasible) is not bool:
        raise TypeError("calibration_feasible must be boolean")
    by_family = {
        f: sorted(l for l, assigned in families.items() if assigned == f)
        for f, weight in weights.items() if weight > 0
    }
    if any(not ids for ids in by_family.values()):
        raise ValueError("positive-weight family has no lineages")
    point = _contrast(rows, {l: 1 for l in families}, weights, systems)
    rng = Random(seed)
    draws = []
    undefined = 0
    for _ in range(replicates):
        multiplicities = {}
        for ids in by_family.values():
            for _ in ids:
                chosen = ids[rng.randrange(len(ids))]
                multiplicities[chosen] = multiplicities.get(chosen, 0) + 1
        value = _contrast(rows, multiplicities, weights, systems)
        if value is None:
            undefined += 1
        else:
            draws.append(value)
    fraction = undefined / replicates
    interval = None
    if calibration_feasible and point is not None and (
        fraction <= max_undefined_fraction
    ) and draws:
        ordered = sorted(draws)
        def quantile(p):
            index = (len(ordered) - 1) * p
            low = int(index)
            high = min(low + 1, len(ordered) - 1)
            return ordered[low] + (index - low) * (ordered[high] - ordered[low])
        interval = (quantile(0.025), quantile(0.975))
    return {
        "point": point,
        "ci95": interval,
        "undefined_replicates": undefined,
        "undefined_fraction": fraction,
        "defined_replicates": len(draws),
        "replicates": replicates,
        "calibration_feasible": calibration_feasible,
        "sampling_unit": "physics-family-stratified lineage",
        "interpretation": "descriptive percentile bootstrap, not a safety guarantee",
    }
