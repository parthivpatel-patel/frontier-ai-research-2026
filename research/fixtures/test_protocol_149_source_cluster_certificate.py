"""Protocol 149: exact source-cluster certification regression witnesses.

Standard library only. This is a test specification, not evidence of execution.
The certificate requires iid independent source clusters and a frozen policy.
"""
import math
import unittest
from fractions import Fraction


def cluster_means(rows):
    """rows: (source_id, bounded_loss) pairs; each source is equally weighted."""
    grouped = {}
    for source, loss in rows:
        if not 0 <= loss <= 2:
            raise ValueError("loss must be in [0,2]")
        grouped.setdefault(source, []).append(Fraction(loss))
    if not grouped:
        raise ValueError("at least one source is required")
    return {source: sum(values, Fraction(0)) / len(values)
            for source, values in grouped.items()}


def upper_certificate(rows, delta=0.05):
    if not 0 < delta < 1:
        raise ValueError("delta must be between 0 and 1")
    means = cluster_means(rows)
    g = len(means)
    risk = float(sum(means.values(), Fraction(0)) / g)
    radius = 2 * math.sqrt(math.log(1 / delta) / (2 * g))
    return risk, radius, min(2.0, risk + radius), g


class SourceClusterCertificateTests(unittest.TestCase):
    def test_duplicate_rows_do_not_increase_independent_count(self):
        base = [("a", 0), ("b", 2), ("c", 1)]
        duplicate = [(source, loss) for source, loss in base for _ in range(100)]
        self.assertEqual(upper_certificate(base), upper_certificate(duplicate))

    def test_prompt_weighting_differs_from_equal_source_weighting(self):
        rows = [("a", 0)] * 100 + [("b", 2)]
        mean, _, _, g = upper_certificate(rows)
        self.assertEqual(g, 2)
        self.assertEqual(mean, 1.0)
        self.assertNotEqual(mean, sum(x for _, x in rows) / len(rows))

    def test_within_source_dependence_not_independent_samples(self):
        rows = [("one", 2)] * 500 + [("two", 0)] * 500
        mean, radius, _, g = upper_certificate(rows)
        self.assertEqual((mean, g), (1.0, 2))
        self.assertAlmostEqual(radius, 2 * math.sqrt(math.log(20) / 4))

    def test_radius_monotonically_shrinks_with_sources(self):
        radii = [upper_certificate([(str(i), 1) for i in range(g)])[1]
                 for g in (20, 100, 1000)]
        self.assertGreater(radii[0], radii[1])
        self.assertGreater(radii[1], radii[2])

    def test_invalid_inputs(self):
        for rows, delta in (([], .05), ([("a", -1)], .05),
                            ([("a", 3)], .05), ([("a", 1)], 0),
                            ([("a", 1)], 1)):
            with self.assertRaises(ValueError):
                upper_certificate(rows, delta)


if __name__ == "__main__":
    unittest.main()
