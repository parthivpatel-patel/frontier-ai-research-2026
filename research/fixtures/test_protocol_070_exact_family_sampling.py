"""Protocol 070: exact enumeration checks for Protocol 069.

Standard library only. Synthetic mathematical identities, NOT empirical AI results.
Execute only on separately authorized, verified $0 cloud infrastructure.
"""
import itertools
import math
import unittest


def exact_design(z, probabilities):
    """Return exact expectation, variance, and expected variance estimate."""
    if len(z) != len(probabilities) or not z:
        raise ValueError("nonempty equal-length family vectors required")
    if any(not math.isfinite(float(x)) for x in z):
        raise ValueError("finite contributions required")
    if any(not math.isfinite(float(p)) or p <= 0 or p > 1 for p in probabilities):
        raise ValueError("inclusion probabilities must lie in (0,1]")
    if len(z) > 12:
        raise ValueError("exact enumeration capped at 12 families")
    outcomes = []
    for bits in itertools.product((0, 1), repeat=len(z)):
        probability = math.prod(p if bit else 1 - p
                                for bit, p in zip(bits, probabilities))
        estimate = sum(bit * value / p
                       for bit, value, p in zip(bits, z, probabilities))
        variance_estimate = sum(bit * (1-p) * value**2 / p**2
                                for bit, value, p in zip(bits, z, probabilities))
        outcomes.append((probability, estimate, variance_estimate))
    expectation = sum(prob * est for prob, est, _ in outcomes)
    variance = sum(prob * (est - expectation)**2 for prob, est, _ in outcomes)
    expected_vhat = sum(prob * vhat for prob, _, vhat in outcomes)
    return expectation, variance, expected_vhat


def family_contrast(claims, denominator_candidate, denominator_baseline):
    """claims: (weight, false_label, candidate_release, baseline_release)."""
    if (not all(math.isfinite(float(d)) and float(d) > 0
                for d in (denominator_candidate, denominator_baseline))):
        raise ValueError("release denominators must be finite and positive")
    result = 0.0
    for weight, label, candidate, baseline in claims:
        if label not in (0, 1):
            raise ValueError("truth label must be resolved and binary")
        if (candidate not in (0, 1) or baseline not in (0, 1)
                or not math.isfinite(float(weight)) or weight < 0):
            raise ValueError("invalid release or weight")
        result += weight * label * (
            candidate / denominator_candidate - baseline / denominator_baseline
        )
    return result


class Protocol070ExactDesignTests(unittest.TestCase):
    def test_certainty_family(self):
        mean, var, expected_vhat = exact_design([0.2], [1.0])
        self.assertAlmostEqual(mean, 0.2)
        self.assertAlmostEqual(var, 0)
        self.assertAlmostEqual(expected_vhat, 0)

    def test_single_bernoulli_family(self):
        mean, var, expected_vhat = exact_design([0.2], [0.5])
        self.assertAlmostEqual(mean, 0.2)
        self.assertAlmostEqual(var, 0.04)
        self.assertAlmostEqual(expected_vhat, 0.04)

    def test_two_family_opposing_contrasts(self):
        mean, var, expected_vhat = exact_design([0.2, -0.1], [0.5, 0.5])
        self.assertAlmostEqual(mean, 0.1)
        self.assertAlmostEqual(var, 0.05)
        self.assertAlmostEqual(expected_vhat, 0.05)

    def test_unequal_probabilities(self):
        z, p = [0.15, -0.07, 0.04, 0.0], [0.2, 0.6, 0.9, 1.0]
        mean, var, expected_vhat = exact_design(z, p)
        expected_var = sum((1-q) * x*x/q for x, q in zip(z, p))
        self.assertAlmostEqual(mean, sum(z))
        self.assertAlmostEqual(var, expected_var)
        self.assertAlmostEqual(expected_vhat, expected_var)

    def test_within_family_cancellation(self):
        # Sum before squaring: +0.3 and -0.3 are ONE sampled family.
        mean, var, expected_vhat = exact_design([0.3 - 0.3], [0.4])
        self.assertAlmostEqual(mean, 0)
        self.assertAlmostEqual(var, 0)
        self.assertAlmostEqual(expected_vhat, 0)

    def test_reject_zero_inclusion(self):
        with self.assertRaises(ValueError):
            exact_design([0.1], [0])

    def test_reject_unresolved_label(self):
        with self.assertRaises(ValueError):
            family_contrast([(1.0, None, 1, 0)], 1.0, 1.0)

    def test_reject_zero_release_denominator(self):
        with self.assertRaises(ValueError):
            family_contrast([(1.0, 1, 1, 0)], 0.0, 1.0)

    def test_reject_nonfinite_denominators(self):
        for bad in (float("nan"), float("inf"), -float("inf")):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                family_contrast([(1.0, 1, 1, 0)], bad, 1.0)
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                family_contrast([(1.0, 1, 1, 0)], 1.0, bad)

    def test_reject_nonfinite_weights(self):
        for bad in (float("nan"), float("inf"), -float("inf")):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                family_contrast([(bad, 1, 1, 0)], 1.0, 1.0)

    def test_enumeration_cap(self):
        with self.assertRaises(ValueError):
            exact_design([0.0] * 13, [0.5] * 13)

    def test_realized_variance_one_sampled_family(self):
        p, z = 0.5, 0.2
        realized = (1 - p) * z**2 / p**2
        self.assertAlmostEqual(realized, 0.08)
        self.assertAlmostEqual(exact_design([z], [p])[2], 0.04)

    def test_family_contrast_definition(self):
        value = family_contrast([(2.0, 1, 1, 0), (1.0, 0, 1, 1)],
                                4.0, 2.0)
        self.assertAlmostEqual(value, 0.5)


if __name__ == "__main__":
    unittest.main()
