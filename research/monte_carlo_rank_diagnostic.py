"""Distribution-free Monte Carlo CDF rank precision diagnostic (Protocol 127).

This is a conditional-bootstrap precision bound, NOT a confidence-interval
coverage guarantee. No third-party dependencies or model inference.
"""
from __future__ import annotations

import math


def dkw_rank_error(defined_replicates: int, alpha: float = 0.05) -> float | None:
    """Return the simultaneous CDF error bound, or None with no defined draws.

    Values above one are mathematically valid but vacuous. Do not clamp:
    callers should be able to detect that the bound is uninformative.
    """
    if isinstance(defined_replicates, bool) or not isinstance(defined_replicates, int):
        raise TypeError("defined_replicates must be an integer")
    if defined_replicates < 0:
        raise ValueError("defined_replicates must be nonnegative")
    if isinstance(alpha, bool) or not isinstance(alpha, (int, float)):
        raise TypeError("alpha must be a real number")
    if not math.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("alpha must be strictly between zero and one")
    if defined_replicates == 0:
        return None
    return math.sqrt(math.log(2.0 / alpha) / (2.0 * defined_replicates))


def minimum_defined_draws(rank_tolerance: float, alpha: float = 0.05) -> int:
    """Conservative sufficient independent draws for a DKW CDF tolerance."""
    if isinstance(rank_tolerance, bool) or not isinstance(rank_tolerance, (int, float)):
        raise TypeError("rank_tolerance must be a real number")
    if not math.isfinite(rank_tolerance) or not 0 < rank_tolerance < 1:
        raise ValueError("rank_tolerance must be strictly between zero and one")
    # Reuse the validation contract even when the required sample count is zero.
    dkw_rank_error(1, alpha)
    return math.ceil(math.log(2.0 / alpha) / (2.0 * rank_tolerance**2))


def percentile_rank_diagnostic(
    defined_replicates: int, requested_replicates: int, alpha: float = 0.05
) -> dict:
    """Expose Monte Carlo rank precision separately from inferential coverage."""
    if isinstance(requested_replicates, bool) or not isinstance(requested_replicates, int):
        raise TypeError("requested_replicates must be an integer")
    if requested_replicates < 0:
        raise ValueError("requested_replicates must be nonnegative")
    error = dkw_rank_error(defined_replicates, alpha)
    if defined_replicates > requested_replicates:
        raise ValueError("defined_replicates cannot exceed requested_replicates")
    return {
        "defined_replicates": defined_replicates,
        "requested_replicates": requested_replicates,
        "defined_fraction": (
            defined_replicates / requested_replicates if requested_replicates else None
        ),
        "dkw_simultaneous_cdf_rank_error": error,
        "dkw_alpha": float(alpha),
        "dkw_informative_for_two_sided_95pct_tails": (
            error is not None and error < 0.025
        ),
        "interpretation": (
            "Conditional Monte Carlo CDF precision only; NOT interval coverage "
            "or percentile value accuracy. Requires iid defined replicates."
        ),
    }
