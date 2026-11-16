"""Protocol 110: negative controls for cross-oracle comparison assertions.

Standard-library-only; intentionally tiny one-claim cases. These tests verify
that Protocol 107's comparator REJECTS injected disagreement, not that the
underlying independent implementations are correct. Execute only on an
approved zero-cost cloud runner. No laptop execution is required.
"""
import unittest
from fractions import Fraction
from unittest.mock import patch

import test_protocol_107_cross_oracle as cross


class CrossOracleNegativeControls(unittest.TestCase):
    def setUp(self):
        self.case = cross.CrossOracleTests()
        self.worlds = cross.full_table(1, (1, 1))

    def test_bellman_value_mutation_is_rejected(self):
        # A deliberately wrong optimum must fail the equality assertion.
        with patch.object(cross, "optimal_value", return_value=Fraction(-1)):
            with self.assertRaises(AssertionError):
                self.case.compare((1,), 1, self.worlds)

    def test_witness_score_mutation_is_rejected(self):
        # A wrong independent witness score must not be accepted as optimal.
        with patch.object(cross, "score_witness", return_value=Fraction(-1)):
            with self.assertRaises(AssertionError):
                self.case.compare((1,), 1, self.worlds)

    def test_empty_enumerator_count_is_rejected(self):
        # Keep actual Bellman and witness scorer; mutate count alone.
        real_certify = cross.certify
        def zero_count(*args, **kwargs):
            value, witness, _ = real_certify(*args, **kwargs)
            return value, witness, 0
        with patch.object(cross, "certify", side_effect=zero_count):
            with self.assertRaises(AssertionError):
                self.case.compare((1,), 1, self.worlds)


if __name__ == "__main__":
    unittest.main()
