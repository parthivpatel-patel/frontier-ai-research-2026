"""Protocol 122: seed-independent interval eligibility for admitted paired records.

Caller MUST run Protocol 113 scientific admission first. This wrapper does not
establish independent adjudication, correct chronology, nominal CI coverage,
or novelty. It preserves undefined-draw diagnostics without using them to
decide whether an interval is eligible.
"""
try:
    from .analytic_preflight import analytic_preflight
    from .common_acceptance_bootstrap import common_acceptance_bootstrap
except ImportError:
    from analytic_preflight import analytic_preflight
    from common_acceptance_bootstrap import common_acceptance_bootstrap


def preflight_gated_bootstrap(rows, weights, systems=("A", "B"), *,
                              seed=0, replicates=2000,
                              max_undefined_fraction=0.01):
    """Compute descriptive bootstrap and apply exact, seed-independent gate.

    CI may still be None when no finite bootstrap draws exist. The eligibility
    decision itself is deterministic given the paired input population.
    """
    records = list(rows)
    weights = dict(weights)
    systems = tuple(systems)
    gate = analytic_preflight(
        records, weights, systems,
        max_undefined_fraction=max_undefined_fraction,
    )
    # Disable the older Monte Carlo threshold decision; preserve its draw
    # diagnostics and apply the exact analytic decision instead.
    result = common_acceptance_bootstrap(
        records, weights, systems, seed=seed, replicates=replicates,
        max_undefined_fraction=1.0,
    )
    result["analytic_preflight"] = gate
    result["interval_eligibility_rule"] = "exact_conditional_denominator_failure"
    result["ci95"] = result["ci95"] if gate["interval_eligible"] else None
    result["interpretation"] = (
        "descriptive conditional percentile interval; analytic eligibility "
        "is not a confidence-interval coverage guarantee"
    )
    return result
