"""Synthetic deterministic checks; execution requires verified free cloud CI."""
import unittest
from research.denominator_failure_diagnostic import denominator_failure_probability


def rows(family, acceptance):
    result = []
    for idx, joint in enumerate(acceptance):
        for system in ("A", "B"):
            result.append(dict(physics_family=family, lineage_id=f"L{idx}",
                               intervention_id="I", system_id=system,
                               accepted=joint))
    return result


class DenominatorFailureTests(unittest.TestCase):
    def test_two_families(self):
        data = rows("mechanics", [True, False]) + rows("optics", [True, False])
        r = denominator_failure_probability(data, {"mechanics": 1, "optics": 1})
        self.assertAlmostEqual(r["conditional_undefined_probability"], .4375)

    def test_all_accept(self):
        self.assertEqual(denominator_failure_probability(
            rows("f", [True, True]), {"f": 1}
        )["conditional_undefined_probability"], 0)

    def test_none_accept(self):
        self.assertEqual(denominator_failure_probability(
            rows("f", [False, False]), {"f": 1}
        )["conditional_undefined_probability"], 1)

    def test_zero_weight_family_excluded(self):
        data = rows("f", [True, True]) + rows("g", [False, False])
        self.assertEqual(denominator_failure_probability(
            data, {"f": 1, "g": 0}
        )["conditional_undefined_probability"], 0)

    def test_order_invariance(self):
        data = rows("f", [True, False, False])
        self.assertEqual(denominator_failure_probability(data, {"f": 1}),
                         denominator_failure_probability(data[::-1], {"f": 1}))

    def test_missing_counterpart_rejected(self):
        with self.assertRaises(ValueError):
            denominator_failure_probability(rows("f", [True, False])[:-1], {"f": 1})

    def test_duplicate_rejected(self):
        data = rows("f", [True, False])
        with self.assertRaises(ValueError):
            denominator_failure_probability(data + [data[0]], {"f": 1})

    def test_multiple_interventions_same_lineage(self):
        data = rows("f", [False, False])
        for system in ("A", "B"):
            data.append(dict(physics_family="f", lineage_id="L0",
                             intervention_id="I2", system_id=system, accepted=True))
        self.assertAlmostEqual(denominator_failure_probability(
            data, {"f": 1})["conditional_undefined_probability"], .25)


if __name__ == "__main__":
    unittest.main()
