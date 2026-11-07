"""Synthetic regression checks for Protocol 117 common-acceptance estimator."""
import unittest

from research.common_acceptance_bootstrap import common_acceptance_bootstrap


def row(family, lineage, intervention, system, accepted, unsafe):
    return dict(physics_family=family, lineage_id=lineage,
                intervention_id=intervention, system_id=system,
                accepted=accepted, response_unsafe=unsafe)


def sample():
    return [
        row("mechanics", "l1", "i1", "A", True, True),
        row("mechanics", "l1", "i1", "B", True, False),
        row("mechanics", "l2", "i2", "A", True, False),
        row("mechanics", "l2", "i2", "B", True, False),
    ]


class BootstrapTests(unittest.TestCase):
    def run_estimator(self, records=None, **kwargs):
        return common_acceptance_bootstrap(
            sample() if records is None else records,
            {"mechanics": 1}, replicates=80, seed=17, **kwargs
        )

    def test_point_is_joint_acceptance_difference(self):
        self.assertEqual(self.run_estimator()["point"], 0.5)

    def test_input_order_invariant(self):
        self.assertEqual(self.run_estimator(), self.run_estimator(list(reversed(sample()))))

    def test_missing_counterpart_rejected(self):
        with self.assertRaises(ValueError):
            self.run_estimator(sample()[:-1])

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            self.run_estimator(sample() + [sample()[0]])

    def test_abstentions_produce_undefined_not_zero(self):
        records = [dict(r, accepted=False, response_unsafe=None) for r in sample()]
        result = self.run_estimator(records)
        self.assertIsNone(result["point"])
        self.assertIsNone(result["ci95"])
        self.assertEqual(result["undefined_replicates"], 80)

    def test_invalid_abstention_rejected(self):
        records = sample()
        records[0] = dict(records[0], accepted=False)
        with self.assertRaises(ValueError):
            self.run_estimator(records)

    def test_family_scoped_lineage_identifiers(self):
        records = sample() + [
            row("optics", "l1", "i1", "A", True, False),
            row("optics", "l1", "i1", "B", True, True),
            row("optics", "l2", "i2", "A", True, False),
            row("optics", "l2", "i2", "B", True, True),
        ]
        result = common_acceptance_bootstrap(
            records, {"mechanics": 1, "optics": 1}, replicates=80)
        self.assertAlmostEqual(result["point"], -0.25)

    def test_insufficient_lineages_rejected(self):
        with self.assertRaises(ValueError):
            self.run_estimator(sample()[:2])

    def test_undefined_draws_suppress_interval(self):
        records = sample()
        for index in (2, 3):
            records[index] = dict(records[index], accepted=False, response_unsafe=None)
        result = self.run_estimator(records, max_undefined_fraction=0)
        self.assertIsNotNone(result["point"])
        self.assertGreater(result["undefined_replicates"], 0)
        self.assertIsNone(result["ci95"])


if __name__ == "__main__":
    unittest.main()
