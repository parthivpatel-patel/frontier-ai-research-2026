"""Protocol 107 arithmetic fixtures; run with python -m unittest discover -s research."""
import unittest
from estimand_counts import Cell, summarize


class EstimandFixtureTests(unittest.TestCase):
    def test_fixture_a_negative_control(self):
        w = {"mechanics": .5, "circuits": .5}
        a = summarize({"mechanics": Cell(9, 1), "circuits": Cell(72, 8)}, w)
        b = summarize({"mechanics": Cell(72, 8), "circuits": Cell(9, 1)}, w)
        for result in (a, b):
            self.assertAlmostEqual(result["pooled_unsafe_risk"], .1)
            self.assertAlmostEqual(result["standardized_unsafe_risk"], .1)
            self.assertEqual(result["accepted_total"], 90)

    def test_fixture_b_undefined(self):
        w = {"mechanics": .5, "circuits": .5}
        a = summarize({"mechanics": Cell(0, 0), "circuits": Cell(2, 0)}, w)
        b = summarize({"mechanics": Cell(2, 1), "circuits": Cell(2, 0)}, w)
        self.assertIsNone(a["standardized_unsafe_risk"])
        self.assertEqual(a["pooled_unsafe_risk"], 0)
        self.assertAlmostEqual(b["standardized_unsafe_risk"], 1 / 6)
        self.assertAlmostEqual(b["pooled_unsafe_risk"], 1 / 5)

    def test_fixture_c_unequal_weights(self):
        w = {"mechanics": .75, "circuits": .25}
        a = summarize({"mechanics": Cell(9, 1), "circuits": Cell(7, 3)}, w)
        b = summarize({"mechanics": Cell(8, 2), "circuits": Cell(6, 4)}, w)
        self.assertAlmostEqual(a["standardized_unsafe_risk"], .15)
        self.assertAlmostEqual(b["standardized_unsafe_risk"], .25)

    def test_zero_total_undefined(self):
        r = summarize({"f": Cell(0, 0)}, {"f": 1})
        self.assertIsNone(r["pooled_unsafe_risk"])
        self.assertIsNone(r["standardized_unsafe_risk"])

    def test_invalid_counts(self):
        for value in (True, 1.0, -1, "1"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    Cell(value, 0)

    def test_invalid_weights(self):
        for value in (True, -0.1, float("nan"), float("inf"), "1"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    summarize({"f": Cell(1, 0)}, {"f": value})

    def test_family_mismatch(self):
        with self.assertRaises(ValueError):
            summarize({"f": Cell(1, 0)}, {"g": 1.0})

    def test_zero_weight_family_can_be_undefined(self):
        r = summarize({"f": Cell(0, 0), "g": Cell(1, 1)}, {"f": 0, "g": 1})
        self.assertAlmostEqual(r["standardized_unsafe_risk"], .5)

    def test_weight_sum(self):
        with self.assertRaises(ValueError):
            summarize({"f": Cell(1, 0)}, {"f": .9})


if __name__ == "__main__":
    unittest.main()
