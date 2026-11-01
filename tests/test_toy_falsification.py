"""Exact mathematical and deterministic checks for the toy protocol."""
import unittest

from src.toy_falsification import (
    Case, decision_witness, evaluate, next_position, run, sample_cases,
)


class ToyFalsificationTests(unittest.TestCase):
    def test_ordinary_case_models_agree(self):
        c = Case(0.5, 0.1, -0.05)
        self.assertAlmostEqual(next_position(c, wall=True),
                               next_position(c, wall=False))

    def test_wall_reflection(self):
        c = Case(0.9, 0.2, 0.2)
        self.assertAlmostEqual(next_position(c, wall=True), 0.7)
        self.assertAlmostEqual(next_position(c, wall=False), 1.3)

    def test_decision_witness(self):
        witness = decision_witness()
        self.assertAlmostEqual(witness["selected_action"], -0.2)
        self.assertAlmostEqual(witness["oracle_action"], 0.2)
        self.assertAlmostEqual(witness["regret"], 0.04)

    def test_reproducibility(self):
        self.assertEqual(run(count=32, seed=11), run(count=32, seed=11))
        self.assertNotEqual(sample_cases("uniform", 4, 11),
                            sample_cases("uniform", 4, 12))

    def test_regime_disagreement(self):
        self.assertEqual(evaluate("ordinary", 64, 11)["fraction_disagree"], 0)
        self.assertEqual(evaluate("boundary", 64, 11)["fraction_disagree"], 1)

    def test_invalid_count_and_regime(self):
        with self.assertRaises(ValueError):
            sample_cases("uniform", 0, 11)
        with self.assertRaises(ValueError):
            sample_cases("unknown", 3, 11)


if __name__ == "__main__":
    unittest.main()
