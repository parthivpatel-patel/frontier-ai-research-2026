"""Protocol 131 independent oracle regression tests; not yet cloud-executed."""
import unittest
from fractions import Fraction

from research.protocol_131_exact_oracle import exact_oracle, reference_cases


class ExactOracleTests(unittest.TestCase):
    def test_first_case(self):
        result = reference_cases()["one_accepting"]
        self.assertEqual(result["total_outcomes"], 4)
        self.assertEqual(result["undefined_probability"], Fraction(1, 4))
        self.assertEqual(result["conditional_pmf"], {"1": Fraction(1)})

    def test_second_case(self):
        result = reference_cases()["opposing"]
        self.assertEqual(result["undefined_probability"], 0)
        self.assertEqual(result["conditional_pmf"],
                         {"-1": Fraction(1, 4), "0": Fraction(1, 2),
                          "1": Fraction(1, 4)})

    def test_third_case(self):
        result = reference_cases()["three_lineages"]
        self.assertEqual(result["total_outcomes"], 27)
        self.assertEqual(result["defined_outcomes"], 26)
        self.assertEqual(result["undefined_probability"], Fraction(1, 27))

    def test_normalized_and_monotone(self):
        for result in reference_cases().values():
            self.assertEqual(sum(result["conditional_pmf"].values()), 1)
            values = list(result["conditional_cdf"].values())
            self.assertEqual(values[-1], 1)
            self.assertEqual(values, sorted(values))

    def test_all_unaccepted(self):
        result = exact_oracle((False, False), (None, None))
        self.assertEqual(result["undefined_probability"], 1)
        self.assertEqual(result["conditional_pmf"], {})

    def test_validation(self):
        for accepted, outcomes in [((), ()), ((True,), (None,)),
                                   ((1,), (1,)), ((False,), (0,))]:
            with self.subTest(accepted=accepted, outcomes=outcomes):
                with self.assertRaises(ValueError):
                    exact_oracle(accepted, outcomes)


if __name__ == "__main__":
    unittest.main()
