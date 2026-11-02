"""Exact three-domain stress test for domain-sensitive LTL disagreement.

This is a constructed, one-source classical model-checking diagnostic, NOT
human-intent adjudication, real physics, or measured AI-model performance.
See experiments/PROTOCOL_013_DOMAIN_UNCERTAINTY_PREREGISTRATION.md.
"""
from __future__ import annotations

import json
from collections import Counter

from src.admissible_lasso_audit import Actuator, FLEXIBLE, FIXED
from src.dynamics_masking_audit import is_restriction, satisfiable_on_model
from src.exhaustive_offset_audit import exact_witness

MONOTONE_WAIT = Actuator(
    "monotone_forward_with_waiting",
    ((0, 1), (1, 2), (2,)),
)
DOMAINS = (FLEXIBLE, MONOTONE_WAIT, FIXED)
OFFSETS = (1, 2, 4, 6)
DIRECTIONS = (
    ("source_true_changed_false", True),
    ("changed_true_source_false", False),
)


def domain_ladder_report(
    domains: tuple[Actuator, ...] = DOMAINS,
    offsets: tuple[int, ...] = OFFSETS,
    *,
    max_nodes: int = 100_000,
) -> dict[str, object]:
    """Compare exact directional witnesses on a strictly nested domain ladder.

    Missing witnesses are exact only when the underlying finite-state search
    completes. Budget exhaustion propagates as an exception, never as a null.
    """
    if len(domains) < 2 or any(
        not is_restriction(wide, narrow) or wide.edges == narrow.edges
        for wide, narrow in zip(domains, domains[1:])
    ):
        raise ValueError("domains must form a strictly nested transition ladder")
    if not offsets or len(set(offsets)) != len(offsets) or any(
        type(offset) is not int or offset not in OFFSETS for offset in offsets
    ):
        raise ValueError("offsets must be distinct members of {1,2,4,6}")
    if type(max_nodes) is not int or max_nodes < 1:
        raise ValueError("max_nodes must be a positive integer")

    comparisons = []
    classes = Counter()
    lost_by_step = Counter()
    for changed in offsets:
        for label, source_required in DIRECTIONS:
            required = 3 if source_required else changed
            violated = changed if source_required else 3
            statuses = []
            for domain in domains:
                result = exact_witness(
                    domain, required, violated, max_nodes=max_nodes
                )
                exists = result.witness is not None
                if exists and not result.witness.valid(domain):
                    raise AssertionError("reported witness violates dynamics")
                realizable = satisfiable_on_model(
                    domain, required, max_nodes=max_nodes
                )
                if exists and not realizable:
                    raise AssertionError("separating trace requires realizability")
                statuses.append({
                    "domain": domain.name,
                    "witness_exists": exists,
                    "required_realizable": realizable,
                    "required_unrealizable": not realizable,
                    "complete": result.complete,
                    "reachable_product_states": result.reachable_product_states,
                })
            flags = [s["witness_exists"] for s in statuses]
            if any(not wide and narrow for wide, narrow in zip(flags, flags[1:])):
                raise AssertionError("witness monotonicity violated")
            category = (
                "all_domains" if all(flags) else
                "no_domain_witness" if not any(flags) else
                "assumption_sensitive"
            )
            classes[category] += 1
            for i, (wide, narrow) in enumerate(zip(flags, flags[1:])):
                if wide and not narrow:
                    lost_by_step[f"{domains[i].name} -> {domains[i+1].name}"] += 1
            comparisons.append({
                "changed_offset": changed,
                "direction": label,
                "classification": category,
                "domains": statuses,
            })
    return {
        "status": "EXACT_CONSTRUCTED_DOMAIN_UNCERTAINTY_AUDIT",
        "source_requirements": 1,
        "independent_model_predictions": 0,
        "comparisons": comparisons,
        "classification_counts": {
            name: classes[name]
            for name in ("all_domains", "assumption_sensitive", "no_domain_witness")
        },
        "witness_losses_by_transition": dict(sorted(lost_by_step.items())),
        "H1_assumption_sensitivity_supported_on_toy": classes["assumption_sensitive"] > 0,
        "H2_intermediate_not_fixed_supported_on_toy": any(
            c["domains"][-2]["witness_exists"] and
            not c["domains"][-1]["witness_exists"]
            for c in comparisons
        ),
        "publication_ready": False,
        "interpretation": (
            "Exact finite-state disagreement under declared synthetic dynamics; "
            "absence does not establish human-intent fidelity or physical truth."
        ),
    }


def audit() -> dict[str, object]:
    return domain_ladder_report()


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
