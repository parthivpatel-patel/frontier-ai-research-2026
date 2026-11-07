"""Synthetic regression fixtures for Protocol 111 (not model results)."""
import unittest

from research.paired_lineage_bootstrap import Observation, paired_lineage_bootstrap


def obs(lineage, family, system, unsafe, accepted=True, intervention="base"):
    return Observation(lineage, family, intervention, system, unsafe, accepted)


class PairedBootstrapTests(unittest.TestCase):
    def run_boot(self, rows, weights=None, **kwargs):
        return paired_lineage_bootstrap(
            rows, weights or {"mechanics": 1}, ("new", "baseline"),
            replicates=100, seed=17, **kwargs
        )

    def test_identical_systems(self):
        rows = [obs(str(i), "mechanics", s, bool(i % 2))
                for i in range(6) for s in ("new", "baseline")]
        result = self.run_boot(rows)
        self.assertEqual(result["point"], 0)
        self.assertEqual(result["ci95"], (0, 0))

    def test_family_standardization(self):
        rows = [obs("a", "mechanics", "new", True),
                obs("a", "mechanics", "baseline", False),
                obs("b", "optics", "new", False),
                obs("b", "optics", "baseline", True)]
        result = self.run_boot(rows, {"mechanics": 1, "optics": 1})
        self.assertEqual(result["point"], 0)
        self.assertEqual(result["ci95"], (0, 0))

    def test_zero_acceptance_suppresses_ci(self):
        rows = [obs("a", "mechanics", "new", True, False),
                obs("a", "mechanics", "baseline", False)]
        result = self.run_boot(rows)
        self.assertIsNone(result["point"])
        self.assertIsNone(result["ci95"])
        self.assertEqual(result["undefined_replicates"], 100)

    def test_calibration_infeasible_suppresses_ci(self):
        rows = [obs("a", "mechanics", s, False)
                for s in ("new", "baseline")]
        self.assertIsNone(self.run_boot(rows, calibration_feasible=False)["ci95"])

    def test_determinism(self):
        rows = [obs(str(i), "mechanics", s, bool(i % 2))
                for i in range(5) for s in ("new", "baseline")]
        self.assertEqual(self.run_boot(rows), self.run_boot(rows))

    def test_rejects_cross_family_lineage(self):
        rows = [obs("a", "mechanics", "new", False),
                obs("a", "optics", "baseline", False)]
        with self.assertRaises(ValueError):
            self.run_boot(rows, {"mechanics": 1, "optics": 1})

    def test_rejects_duplicate_key(self):
        row = obs("a", "mechanics", "new", False)
        with self.assertRaises(ValueError):
            self.run_boot([row, row])

    def test_rejects_nonboolean(self):
        with self.assertRaises(TypeError):
            self.run_boot([obs("a", "mechanics", "new", 0)])

    def test_paired_lineage_direction(self):
        rows = [obs("a", "mechanics", "new", True),
                obs("a", "mechanics", "baseline", False),
                obs("b", "mechanics", "new", False),
                obs("b", "mechanics", "baseline", True)]
        self.assertEqual(self.run_boot(rows)["point"], 0)


if __name__ == "__main__":
    unittest.main()
