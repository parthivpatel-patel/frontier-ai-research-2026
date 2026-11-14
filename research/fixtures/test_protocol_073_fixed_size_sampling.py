"""Protocol 073: exact fixed-size sampling design collision tests.

Standard library only; synthetic algebraic checks, NOT AI performance results.
Execution is restricted to independently verified zero-cost cloud infrastructure.
"""
import itertools
import math
import unittest


def exact_fixed_size(z, sample_size):
    """Enumerate uniform subsets; return mean and design variance of HT total."""
    if not z or len(z) > 12 or not all(math.isfinite(float(x)) for x in z):
        raise ValueError("finite nonempty family vector of at most 12 required")
    n = len(z)
    if not isinstance(sample_size, int) or isinstance(sample_size, bool) or not 1 <= sample_size <= n:
        raise ValueError("sample size must be integer in [1, family count]")
    pi = sample_size / n
    estimates = [
        sum(z[i] / pi for i in indices)
        for indices in itertools.combinations(range(n), sample_size)
    ]
    mean = sum(estimates) / len(estimates)
    variance = sum((x - mean) ** 2 for x in estimates) / len(estimates)
    return mean, variance


def independent_bernoulli_variance(z, pi):
    """Formula only valid for independent Bernoulli inclusion."""
    return sum((1 - pi) * x * x / pi for x in z)


class Protocol073FixedSizeTests(unittest.TestCase):
    def test_two_family_counterexample(self):
        mean, variance = exact_fixed_size([0.2, -0.1], 1)
        self.assertAlmostEqual(mean, 0.1)
        self.assertAlmostEqual(variance, 0.09)
        self.assertAlmostEqual(independent_bernoulli_variance([0.2, -0.1], 0.5), 0.05)
        self.assertNotAlmostEqual(variance, 0.05)

    def test_census_has_zero_variance(self):
        self.assertEqual(exact_fixed_size([0.2, -0.1, 0.3], 3)[1], 0)

    def test_equal_family_values_fixed_size(self):
        mean, variance = exact_fixed_size([0.2, 0.2, 0.2], 1)
        self.assertAlmostEqual(mean, 0.6)
        self.assertAlmostEqual(variance, 0)

    def test_nontrivial_three_family_exact_design(self):
        z = [0.1, 0.2, -0.1]
        mean, variance = exact_fixed_size(z, 2)
        self.assertAlmostEqual(mean, sum(z))
        # Enumerated HT totals are 0.45, 0, 0.15.
        self.assertAlmostEqual(variance, 0.035)

    def test_reject_invalid_designs(self):
        for z, k in [([], 1), ([0.1], 0), ([0.1], 2),
                     ([0.1], True), ([float("nan")], 1),
                     ([float("inf")], 1), ([0.0] * 13, 1)]:
            with self.subTest(z=z, k=k), self.assertRaises(ValueError):
                exact_fixed_size(z, k)


if __name__ == "__main__":
    unittest.main()
