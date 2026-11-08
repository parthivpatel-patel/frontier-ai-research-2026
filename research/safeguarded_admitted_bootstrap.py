"""Protocol 125: conservative reporting safeguard for Protocol 123 output.

This is a reporting filter, not a calibrated confidence interval or a
substitute for scientific admission. No new bootstrap simulations are run.
"""
from math import isfinite

try:
    from .admitted_preflight_bootstrap import admitted_preflight_bootstrap
except ImportError:
    from admitted_preflight_bootstrap import admitted_preflight_bootstrap


def safeguarded_admitted_bootstrap(*args, min_defined_replicates=1000, **kwargs):
    """Suppress unreliable percentile endpoints when defined draws are too few.

    A minimum count is necessary but insufficient for nominal coverage.
    In particular, this does not fix selection bias, conditional resampling,
    or lineage dependence.
    """
    if type(min_defined_replicates) is not int or min_defined_replicates < 2:
        raise ValueError("min_defined_replicates must be an integer >= 2")
    result = admitted_preflight_bootstrap(*args, **kwargs)
    result = dict(result)
    n = result["defined_replicates"]
    if type(n) is not int or n < 0:
        raise ValueError("invalid defined bootstrap count")
    original_interval = result.get("ci95")
    if original_interval is not None:
        if (not isinstance(original_interval, (tuple, list))
                or len(original_interval) != 2
                or any(type(v) not in (int, float) or not isfinite(v)
                       for v in original_interval)
                or original_interval[0] > original_interval[1]):
            raise ValueError("invalid percentile interval")
    sufficient = n >= min_defined_replicates
    if not sufficient:
        result["ci95"] = None
    result["minimum_defined_replicates"] = min_defined_replicates
    result["defined_draw_count_sufficient"] = sufficient
    result["interval_reported"] = result["ci95"] is not None
    result["interval_suppression_reason"] = (
        "insufficient_defined_bootstrap_draws" if not sufficient
        else ("upstream_eligibility_or_undefined_estimate"
              if result["ci95"] is None else None)
    )
    result["coverage_warning"] = (
        "Minimum draw count is a reporting safeguard only; nominal "
        "coverage and Monte Carlo quantile accuracy remain unverified."
    )
    return result
