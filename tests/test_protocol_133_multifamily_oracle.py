"""Protocol 133 independent multifamily exact preflight checks."""
import unittest
from fractions import Fraction
from research.analytic_preflight import analytic_preflight
from research.protocol_133_multifamily_oracle import exact_multifamily_undefined


def rows(family, flags):
    result = []
    for index, accepted in enumerate(flags):
        for system in ("A", "B"):
            result.append({
                "physics_family": family,
                "lineage_id": f"{family}_lineage_{index}",
                "intervention_id": f"{family}_item_{index}",
                "system_id": system,
                "accepted": accepted,
                "response_unsafe": False if accepted else None,
            })
    return result


class MultiFamilyOracleTests(unittest.TestCase):
    def test_two_families_exact_union(self):
        flags = {"mechanics": (True, False), "optics": (True, True, False)}
        expected = exact_multifamily_undefined(((1, flags["mechanics"]), (1, flags["optics"])))
        self.assertEqual(expected, Fraction(5, 18))
        population = sum((rows(f, a) for f, a in flags.items()), [])
        actual = analytic_preflight(population, {"mechanics": 1, "optics": 1},
                                    max_undefined_fraction=1)
        self.assertAlmostEqual(actual["conditional_undefined_probability"], float(expected), places=14)

    def test_zero_weight_family_excluded(self):
        flags = {"mechanics": (True, False), "optics": (False, False)}
        expected = exact_multifamily_undefined(((1, flags["mechanics"]), (0, flags["optics"])))
        self.assertEqual(expected, Fraction(1, 4))
        population = sum((rows(f, a) for f, a in flags.items()), [])
        actual = analytic_preflight(population, {"mechanics": 1, "optics": 0},
                                    max_undefined_fraction=1)
        self.assertAlmostEqual(actual["conditional_undefined_probability"], float(expected), places=14)
        self.assertTrue(actual["original_defined"])

    def test_all_abstain_family(self):
        flags = {"mechanics": (True, True), "optics": (False, False)}
        expected = exact_multifamily_undefined(((1, flags["mechanics"]), (1, flags["optics"])))
        self.assertEqual(expected, Fraction(1))
        population = sum((rows(f, a) for f, a in flags.items()), [])
        actual = analytic_preflight(population, {"mechanics": 1, "optics": 1},
                                    max_undefined_fraction=1)
        self.assertFalse(actual["original_defined"])
        self.assertFalse(actual["interval_eligible"])

    def test_invalid_oracle_inputs(self):
        for case in ((), ((0, (True, False)),), ((1, (True,)),),
                     ((1, (1, False)),), ((-1, (True, False)),)):
            with self.subTest(case=case), self.assertRaises(ValueError):
                exact_multifamily_undefined(case)


if __name__ == "__main__":
    unittest.main()
