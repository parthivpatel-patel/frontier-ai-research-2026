"""Protocol 153: regression checks for preflight reporting; not yet executed."""
import unittest
from research.analytic_preflight import analytic_preflight
from research.common_acceptance_bootstrap import common_acceptance_bootstrap
from research.preflight_gated_bootstrap import preflight_gated_bootstrap

def rows(flags):
    return [{"physics_family": f, "lineage_id": f"{f}-{i}",
             "intervention_id": "i0", "system_id": s, "accepted": a,
             "response_unsafe": False if a else None}
            for f, values in flags.items() for i, a in enumerate(values)
            for s in ("A", "B")]

class PreflightReportingContract(unittest.TestCase):
    def test_point_defined_equivalence(self):
        for flags in ({"mechanics": (True, False)},
                      {"mechanics": (False, False)},
                      {"mechanics": (True, False), "optics": (False, False)},
                      {"mechanics": (True, True), "optics": (False, True)}):
            with self.subTest(flags=flags):
                w = {f: 1 for f in flags}
                p = analytic_preflight(rows(flags), w, max_undefined_fraction=1)
                b = common_acceptance_bootstrap(rows(flags), w, seed=3,
                                                replicates=7, max_undefined_fraction=1)
                self.assertEqual(p["original_defined"], b["point"] is not None)

    def test_ineligible_gate_preserves_draw_accounting(self):
        result = preflight_gated_bootstrap(
            rows({"mechanics": (True, False)}), {"mechanics": 1},
            seed=11, replicates=23, max_undefined_fraction=0)
        self.assertTrue(result["analytic_preflight"]["original_defined"])
        self.assertFalse(result["analytic_preflight"]["interval_eligible"])
        self.assertIsNotNone(result["point"])
        self.assertIsNone(result["ci95"])
        self.assertEqual(result["defined_replicates"] +
                         result["undefined_replicates"], 23)

    def test_zero_weight_family_ignored(self):
        sample = rows({"mechanics": (True, False), "optics": (False, False)})
        weights = {"mechanics": 1, "optics": 0}
        p = analytic_preflight(sample, weights, max_undefined_fraction=1)
        b = common_acceptance_bootstrap(sample, weights, seed=5,
                                        replicates=9, max_undefined_fraction=1)
        self.assertTrue(p["original_defined"])
        self.assertIsNotNone(b["point"])
        self.assertEqual([d["physics_family"] for d in p["families"]], ["mechanics"])

    def test_invalid_pair_raises_not_abstains(self):
        sample = rows({"mechanics": (True, True)})
        sample.pop()
        with self.assertRaises(ValueError):
            preflight_gated_bootstrap(sample, {"mechanics": 1}, replicates=5)

if __name__ == "__main__":
    unittest.main()
