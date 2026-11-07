"""Synthetic checks for Protocol 122; execution in cloud CI is still required."""
import unittest

from research.preflight_gated_bootstrap import preflight_gated_bootstrap


def make_rows(accepting):
    rows = []
    for lineage, accepted in enumerate(accepting):
        for system, unsafe in (("A", True), ("B", False)):
            rows.append(dict(physics_family="mechanics", lineage_id=str(lineage),
                             intervention_id="trial", system_id=system,
                             accepted=accepted,
                             response_unsafe=unsafe if accepted else None))
    return rows


class PreflightGatedBootstrapTests(unittest.TestCase):
    def test_all_accepting_has_defined_interval(self):
        result = preflight_gated_bootstrap(make_rows([True] * 4),
                                           {"mechanics": 1}, replicates=20)
        self.assertTrue(result["analytic_preflight"]["interval_eligible"])
        self.assertEqual(result["ci95"], (1.0, 1.0))

    def test_rare_acceptance_suppresses_interval_independent_of_seed(self):
        rows = make_rows([True, False, False, False])
        for seed in range(6):
            result = preflight_gated_bootstrap(
                rows, {"mechanics": 1}, seed=seed, replicates=10)
            self.assertFalse(result["analytic_preflight"]["interval_eligible"])
            self.assertIsNone(result["ci95"])

    def test_zero_acceptance_has_no_point_or_interval(self):
        result = preflight_gated_bootstrap(make_rows([False] * 3),
                                           {"mechanics": 1}, replicates=10)
        self.assertIsNone(result["point"])
        self.assertIsNone(result["ci95"])

    def test_input_order_invariance(self):
        rows = make_rows([True, True, False, True])
        a = preflight_gated_bootstrap(rows, {"mechanics": 1}, replicates=30)
        b = preflight_gated_bootstrap(list(reversed(rows)),
                                      {"mechanics": 1}, replicates=30)
        self.assertEqual(a, b)

    def test_rejects_missing_counterpart(self):
        with self.assertRaises(ValueError):
            preflight_gated_bootstrap(make_rows([True, True])[:-1],
                                       {"mechanics": 1}, replicates=5)

    def test_rejects_invalid_abstention(self):
        rows = make_rows([True, False])
        rows[-1]["response_unsafe"] = False
        with self.assertRaises(ValueError):
            preflight_gated_bootstrap(rows, {"mechanics": 1}, replicates=5)


if __name__ == "__main__":
    unittest.main()
