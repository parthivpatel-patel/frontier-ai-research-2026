"""Protocol 128: attach conditional Monte Carlo rank diagnostics to admitted bootstrap reporting.

Pure reporting wrapper; does not change interval eligibility or execute additional
bootstrap draws. DKW is not an interval coverage or quantile-value guarantee.
"""
try:
    from .safeguarded_admitted_bootstrap import safeguarded_admitted_bootstrap
    from .monte_carlo_rank_diagnostic import percentile_rank_diagnostic
except ImportError:
    from safeguarded_admitted_bootstrap import safeguarded_admitted_bootstrap
    from monte_carlo_rank_diagnostic import percentile_rank_diagnostic


def precision_reported_admitted_bootstrap(*args, dkw_alpha=0.05, **kwargs):
    """Return the existing admitted estimate with an explicit precision diagnostic.

    The original interval and its suppression rule are preserved. This diagnostic
    assumes iid *defined* draws from a fixed conditional bootstrap distribution.
    """
    result = dict(safeguarded_admitted_bootstrap(*args, **kwargs))
    diagnostic = percentile_rank_diagnostic(
        result["defined_replicates"], result["requested_replicates"], dkw_alpha
    )
    result["monte_carlo_precision"] = diagnostic
    result["monte_carlo_precision_warning"] = (
        "DKW bounds conditional CDF rank error under iid defined draws. "
        "It does not validate nominal confidence interval coverage, correct "
        "selection bias, or bound quantile endpoint value error."
    )
    return result
