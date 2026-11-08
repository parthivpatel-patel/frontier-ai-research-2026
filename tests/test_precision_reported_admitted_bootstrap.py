"""Synthetic, no-inference contract tests for Protocol 128. Not yet executed."""
from unittest.mock import patch
import pytest
from research.precision_reported_admitted_bootstrap import precision_reported_admitted_bootstrap


def fake_result(defined, requested, interval):
    return {
        "defined_replicates": defined,
        "requested_replicates": requested,
        "ci95": interval,
        "interval_reported": interval is not None,
        "interval_suppression_reason": None if interval else "upstream",
    }


def test_precision_attached_without_changing_interval():
    original = fake_result(1000, 1200, (0.1, 0.3))
    with patch(
        "research.precision_reported_admitted_bootstrap.safeguarded_admitted_bootstrap",
        return_value=original,
    ):
        result = precision_reported_admitted_bootstrap()
    assert result["ci95"] == (0.1, 0.3)
    assert result["monte_carlo_precision"]["defined_replicates"] == 1000
    assert result["monte_carlo_precision"]["dkw_simultaneous_cdf_rank_error"] > 0.04
    assert "monte_carlo_precision" not in original


def test_suppressed_interval_stays_suppressed():
    with patch(
        "research.precision_reported_admitted_bootstrap.safeguarded_admitted_bootstrap",
        return_value=fake_result(0, 1000, None),
    ):
        result = precision_reported_admitted_bootstrap()
    assert result["ci95"] is None
    assert result["monte_carlo_precision"]["dkw_simultaneous_cdf_rank_error"] is None


def test_invalid_counts_fail_closed():
    with patch(
        "research.precision_reported_admitted_bootstrap.safeguarded_admitted_bootstrap",
        return_value=fake_result(1200, 1000, None),
    ):
        with pytest.raises(ValueError):
            precision_reported_admitted_bootstrap()


def test_alpha_validation():
    with patch(
        "research.precision_reported_admitted_bootstrap.safeguarded_admitted_bootstrap",
        return_value=fake_result(1000, 1000, None),
    ):
        with pytest.raises(ValueError):
            precision_reported_admitted_bootstrap(dkw_alpha=1.0)
