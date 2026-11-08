"""Protocol 143: standard-library regression for independent-family preflight.

Designed for cloud CI; authoring this file does not constitute execution.
"""
import unittest
from fractions import Fraction
from itertools import product

from research.analytic_preflight import analytic_preflight
from research.common_acceptance_bootstrap import common_acceptance_bootstrap


def rows_for(family_flags):
    rows = []
    for family, flags in family_flags.items():
        for i, accepted in enumerate(flags):
            for system in ("A", "B"):
                rows.append({
                    "physics_family": family,
                    "lineage_id": f"{family}-{i}",
                    "intervention_id": "intervention-0",
                    "system_id": system,
                    "accepted": accepted,
                    "response_unsafe": False if accepted else None,
                })
    return rows


def exact_independent_failure(family_flags):
    """Independent exhaustive reference, intentionally not using preflight."""
    defined = Fraction(1)
    for flags in family_flags.values():
        n = len(flags)
        valid = sum(
            any(flags[index] for index in indices)
            for indices in product(range(n), repeat=n)
        )
        defined *= Fraction(valid, n ** n)
    return 1 - defined


class ProductionContractTests(unittest.TestCase):
    def test_preflight_against_independent_enumeration(self):
        for families in (
            {"mechanics": (True, False)},
            {"mechanics": (True, False), "optics": (True, True, False)},
            {"mechanics": (True, True), "optics": (True, False)},
            {"mechanics": (False, False), "optics": (True, True)},
        ):
            with self.subTest(families=families):
                result = analytic_preflight(
                    rows_for(families), {family: 1 for family in families},
                    max_undefined_fraction=1,
                )
                expected = exact_independent_failure(families)
                self.assertAlmostEqual(
                    result["conditional_undefined_probability"], float(expected),
                    places=12,
                )
                self.assertEqual(
                    result["original_defined"],
                    all(any(flags) for flags in families.values()),
                )

    def test_empirical_counts_account_for_all_replicates(self):
        families = {"mechanics": (True, False), "optics": (True, True, False)}
        sample = common_acceptance_bootstrap(
            rows_for(families), {family: 1 for family in families},
            seed=17, replicates=101, max_undefined_fraction=1,
        )
        self.assertEqual(
            sample["defined_replicates"] + sample["undefined_replicates"], 101
        )
        self.assertAlmostEqual(
            sample["undefined_fraction"], sample["undefined_replicates"] / 101
        )

    def test_zero_weight_family_excluded(self):
        families = {"mechanics": (True, False), "optics": (False, False)}
        result = analytic_preflight(
            rows_for(families), {"mechanics": 1, "optics": 0},
            max_undefined_fraction=1,
        )
        self.assertAlmostEqual(result["conditional_undefined_probability"], 0.25)
        self.assertTrue(result["original_defined"])


if __name__ == "__main__":
    unittest.main()
