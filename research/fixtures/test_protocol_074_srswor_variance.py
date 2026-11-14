"""Protocol 074: exact SRSWOR variance-estimator identity tests.

Synthetic finite-population algebra only; no model experiments or empirical claims.
Do not execute on user's laptop. Cloud execution requires verified $0 eligibility.
"""
import itertools
import math
import unittest


def srswor_exact(z, k):
    """Return true design variance and expected unbiased sample variance estimate."""
    if not isinstance(z, (list, tuple)) or not 2 <= len(z) <= 10:
        raise ValueError("finite population must contain 2..10 families")
    if any(not isinstance(x, (int, float)) or isinstance(x, bool)
           or not math.isfinite(x) for x in z):
        raise ValueError("family contributions must be finite real numbers")
    n = len(z)
    if not isinstance(k, int) or isinstance(k, bool) or not 2 <= k <= n:
        raise ValueError("sample size must be integer in [2, N]")
    estimates, variance_estimates = [], []
    for idx in itertools.combinations(range(n), k):
        observed = [z[i] for i in idx]
        mean = sum(observed) / k
        s2 = sum((x - mean) ** 2 for x in observed) / (k - 1)
        estimates.append(n * mean)
        variance_estimates.append(n * n * (1 - k / n) * s2 / k)
    expectation = sum(estimates) / len(estimates)
    true_variance = sum((v - expectation) ** 2 for v in estimates) / len(estimates)
    expected_estimate = sum(variance_estimates) / len(variance_estimates)
    return expectation, true_variance, expected_estimate


class Protocol074Tests(unittest.TestCase):
    def test_nontrivial_fixed_size_unbiased_variance_estimator(self):
        mean, var, expected_vhat = srswor_exact([0.1, 0.2, -0.1], 2)
        self.assertAlmostEqual(mean, 0.2)
        self.assertAlmostEqual(var, 0.035)
        self.assertAlmostEqual(expected_vhat, var)

    def test_heterogeneous_four_family_population(self):
        z = [0.3, -0.2, 0.7, 0.1]
        for k in (2, 3, 4):
            with self.subTest(k=k):
                mean, var, expected_vhat = srswor_exact(z, k)
                self.assertAlmostEqual(mean, sum(z))
                self.assertAlmostEqual(expected_vhat, var)

    def test_equal_family_contributions(self):
        mean, var, expected_vhat = srswor_exact([0.2] * 5, 2)
        self.assertAlmostEqual(mean, 1.0)
        self.assertAlmostEqual(var, 0.0)
        self.assertAlmostEqual(expected_vhat, 0.0)

    def test_census_variance_zero(self):
        _, var, expected_vhat = srswor_exact([0.2, -0.1, 0.4], 3)
        self.assertAlmostEqual(var, 0.0)
        self.assertAlmostEqual(expected_vhat, 0.0)

    def test_one_draw_not_identifiable_from_sample_variance(self):
        with self.assertRaises(ValueError):
            srswor_exact([0.2, -0.1], 1)

    def test_invalid_inputs_rejected(self):
        bad = [([0.1], 1), ([0.1, float("nan")], 2),
               ([0.1, float("inf")], 2), ([True, 0.1], 2),
               ([0.1, 0.2], True), ([0.1, 0.2], 3),
               ([0.0] * 11, 2)]
        for z, k in bad:
            with self.subTest(z=z, k=k), self.assertRaises(ValueError):
                srswor_exact(z, k)


if __name__ == "__main__":
    unittest.main()
