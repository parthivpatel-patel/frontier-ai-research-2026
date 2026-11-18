"""Protocol 152: deterministic finite-family source-cluster bound checks.

This checks arithmetic and invariants only, not statistical coverage or model accuracy.
No third-party packages, inference, network, or dataset downloads.
"""
import math
import unittest


def radius(n, k, alpha=0.05, bound=2.0):
    if isinstance(n, bool) or isinstance(k, bool) or not isinstance(n, int) or not isinstance(k, int) or n < 1 or k < 1:
        raise ValueError("n and k must be positive integers")
    if not (math.isfinite(alpha) and 0 < alpha < 1):
        raise ValueError("alpha must lie strictly between zero and one")
    if not (math.isfinite(bound) and bound > 0):
        raise ValueError("bound must be finite and positive")
    return bound * math.sqrt(math.log(k / alpha) / (2 * n))


def upper_certificate(cluster_losses, k, alpha=0.05, bound=2.0):
    if not cluster_losses:
        raise ValueError("at least one source cluster is required")
    if any(not math.isfinite(x) or x < 0 or x > bound for x in cluster_losses):
        raise ValueError("loss outside prespecified range")
    mean = sum(cluster_losses) / len(cluster_losses)
    return min(bound, mean + radius(len(cluster_losses), k, alpha, bound))


class Protocol152Tests(unittest.TestCase):
    def test_single_policy_equivalence(self):
        self.assertAlmostEqual(radius(100, 1), 2 * math.sqrt(math.log(20) / 200))

    def test_family_size_monotonicity(self):
        self.assertLess(radius(100, 1), radius(100, 10))
        self.assertLess(radius(100, 10), radius(100, 100))

    def test_source_count_monotonicity(self):
        self.assertGreater(radius(20, 5), radius(100, 5))

    def test_bound_is_capped_and_can_be_vacuous(self):
        self.assertEqual(upper_certificate([2.0] * 10, 10), 2.0)
        self.assertEqual(upper_certificate([0.0], 100000), 2.0)

    def test_cluster_not_prompt_count(self):
        clusters = [0.0, 2.0, 0.0, 2.0]
        # Each source's prompt-level observations may be repeated without
        # changing the pre-aggregated source-level certificate.
        repeated_prompts = [[x] * 100 for x in clusters]
        aggregated = [sum(row) / len(row) for row in repeated_prompts]
        self.assertEqual(upper_certificate(clusters, 2), upper_certificate(aggregated, 2))

    def test_invalid_parameters(self):
        for n, k in [(0, 1), (1, 0), (-1, 1), (1, -1), (1.5, 2), (True, 2)]:
            with self.subTest(n=n, k=k), self.assertRaises(ValueError):
                radius(n, k)
        for alpha in [0, 1, -0.1, float("nan")]:
            with self.subTest(alpha=alpha), self.assertRaises(ValueError):
                radius(10, 2, alpha)
        with self.assertRaises(ValueError):
            upper_certificate([2.1], 2)
        with self.assertRaises(ValueError):
            upper_certificate([], 2)


if __name__ == "__main__":
    unittest.main()
