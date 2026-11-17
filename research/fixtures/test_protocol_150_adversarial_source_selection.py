"""Protocol 150: adversarial source-selection witnesses.

These are deterministic synthetic regression tests, not experimental evidence.
A source-cluster Hoeffding certificate needs iid representative clusters;
grouping duplicates alone does not establish representativeness.
"""
import math
import unittest
from fractions import Fraction


def observed_cluster_risk(source_losses, observed_ids):
    """Equal-source risk among selected source IDs, with no prompt-count inflation."""
    if not observed_ids:
        raise ValueError("empty observed sample")
    if len(set(observed_ids)) != len(observed_ids):
        raise ValueError("duplicate source ID")
    if any(s not in source_losses for s in observed_ids):
        raise ValueError("unknown source")
    if any(not 0 <= x <= 2 for x in source_losses.values()):
        raise ValueError("loss outside [0,2]")
    return sum((Fraction(source_losses[s]) for s in observed_ids), Fraction(0)) / len(observed_ids)


def finite_population_risk(source_losses):
    return observed_cluster_risk(source_losses, list(source_losses))


def nominal_upper_bound(mean, g, delta=0.05):
    if not 0 <= mean <= 2 or g <= 0 or not 0 < delta < 1:
        raise ValueError("invalid certificate input")
    return min(2, float(mean) + 2 * math.sqrt(math.log(1 / delta) / (2 * g)))


class AdversarialSourceSelectionTests(unittest.TestCase):
    def setUp(self):
        # 100 low-loss and 100 high-loss sources. Selection is deliberately biased.
        self.population = {f"low-{i}": 0 for i in range(100)}
        self.population.update({f"high-{i}": 2 for i in range(100)})

    def test_true_population_risk(self):
        self.assertEqual(finite_population_risk(self.population), Fraction(1))

    def test_source_disjointness_does_not_imply_representativeness(self):
        selected = [f"low-{i}" for i in range(100)]
        self.assertEqual(len(set(selected)), 100)
        self.assertEqual(observed_cluster_risk(self.population, selected), 0)
        self.assertGreater(finite_population_risk(self.population),
                           nominal_upper_bound(0, 100))

    def test_opposite_selection_reverses_apparent_risk(self):
        low = [f"low-{i}" for i in range(100)]
        high = [f"high-{i}" for i in range(100)]
        self.assertEqual(observed_cluster_risk(self.population, low), 0)
        self.assertEqual(observed_cluster_risk(self.population, high), 2)

    def test_duplicate_source_ids_rejected(self):
        with self.assertRaises(ValueError):
            observed_cluster_risk(self.population, ["low-0", "low-0"])

    def test_unknown_source_rejected(self):
        with self.assertRaises(ValueError):
            observed_cluster_risk(self.population, ["missing"])

    def test_invalid_loss_rejected(self):
        with self.assertRaises(ValueError):
            observed_cluster_risk({"a": 3}, ["a"])


if __name__ == "__main__":
    unittest.main()
