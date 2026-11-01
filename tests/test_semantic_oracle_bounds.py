"""Unit tests for finite-sample semantic-oracle ambiguity diagnostics."""
import unittest
from fractions import Fraction

from src.exact_domain_audit import Domain, Interval, Q
from src.semantic_oracle_bounds import OracleCase, sample_error_bounds, sample_risk_decision


def domain():
    # Exactly covers next positions in [1/2,1], with no bounce.
    return Domain(Interval(Q('0.5'), Q('0.5')),
                  Interval(Q('0'), Q('0')),
                  Interval(Q('0'), Q('0.5')))


class OracleAmbiguityTests(unittest.TestCase):
    def test_equivalent_reference(self):
        case = OracleCase(domain(), Q('0.8'), (Q('0.8'),))
        self.assertEqual(case.possible_errors(), frozenset({0}))

    def test_certain_mismatch(self):
        case = OracleCase(domain(), Q('1'), (Q('0.8'), Q('0.9')))
        self.assertEqual(case.possible_errors(), frozenset({1}))

    def test_ambiguous_reference(self):
        case = OracleCase(domain(), Q('0.8'), (Q('0.8'), Q('0.9')))
        self.assertEqual(case.possible_errors(), frozenset({0, 1}))

    def test_finite_sample_bounds(self):
        cases = (
            OracleCase(domain(), Q('0.8'), (Q('0.8'),)),
            OracleCase(domain(), Q('0.8'), (Q('0.8'), Q('0.9'))),
            OracleCase(domain(), Q('1'), (Q('0.8'), Q('0.9'))),
        )
        result = sample_error_bounds(cases)
        self.assertEqual(result['certain_errors'], 1)
        self.assertEqual(result['possible_errors'], 2)
        self.assertEqual(result['ambiguous_cases'], 1)
        self.assertEqual(result['lower_error_rate'], Fraction(1, 3))
        self.assertEqual(result['upper_error_rate'], Fraction(2, 3))
        self.assertEqual(sample_risk_decision(cases, Fraction(1, 2)),
                         'depends_on_unresolved_interpretation')
        self.assertEqual(sample_risk_decision(cases, Fraction(2, 3)),
                         'passes_for_every_supplied_interpretation')
        self.assertEqual(sample_risk_decision(cases, Fraction(1, 4)),
                         'fails_for_every_supplied_interpretation')

    def test_reject_empty_reference(self):
        with self.assertRaises(ValueError):
            OracleCase(domain(), Q('0.8'), ())

    def test_reject_empty_sample(self):
        with self.assertRaises(ValueError):
            sample_error_bounds([])

    def test_reject_invalid_risk_target(self):
        case = OracleCase(domain(), Q('0.8'), (Q('0.8'),))
        with self.assertRaises(ValueError):
            sample_risk_decision((case,), Fraction(3, 2))

    def test_threshold_endpoint_semantics(self):
        # Candidate <= 1 is true everywhere; <= 1/2 differs above 1/2.
        case = OracleCase(domain(), Q('1'), (Q('0.5'),))
        self.assertEqual(case.possible_errors(), frozenset({1}))


if __name__ == '__main__':
    unittest.main()
