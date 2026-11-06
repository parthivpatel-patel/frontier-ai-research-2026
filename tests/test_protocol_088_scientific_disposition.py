"""Constructed decision-table controls; not empirical model evaluations."""
import unittest

from research.protocol_088_scientific_disposition import (
    Applicability, Disposition, EvidenceState, classify,
)


class ScientificDispositionTests(unittest.TestCase):
    def test_full_decision_table(self):
        expected = {
            Applicability.APPLICABLE: [
                Disposition.SUPPORTED, Disposition.REFUTED,
                Disposition.UNDERDETERMINED, Disposition.CONFLICT,
                Disposition.UNDERDETERMINED,
            ],
            Applicability.INAPPLICABLE: [
                Disposition.OUTSIDE_SCOPE, Disposition.OUTSIDE_SCOPE,
                Disposition.OUTSIDE_SCOPE, Disposition.CONFLICT,
                Disposition.OUTSIDE_SCOPE,
            ],
            Applicability.UNKNOWN: [
                Disposition.UNDERDETERMINED, Disposition.UNDERDETERMINED,
                Disposition.UNDERDETERMINED, Disposition.CONFLICT,
                Disposition.UNDERDETERMINED,
            ],
        }
        states = list(EvidenceState)
        self.assertEqual(states, [
            EvidenceState.ALL_SUPPORT, EvidenceState.ALL_REFUTE,
            EvidenceState.MIXED, EvidenceState.EMPTY, EvidenceState.UNASSESSED,
        ])
        for applicability, outcomes in expected.items():
            for evidence, outcome in zip(states, outcomes):
                with self.subTest(applicability=applicability, evidence=evidence):
                    decision = classify(applicability, evidence)
                    self.assertEqual(decision.disposition, outcome)
                    self.assertTrue(decision.reason)

    def test_reject_untyped_states(self):
        with self.assertRaises(TypeError):
            classify("applicable", EvidenceState.ALL_SUPPORT)
        with self.assertRaises(TypeError):
            classify(Applicability.APPLICABLE, "all_support")

    def test_conflict_never_vacuously_supported(self):
        for applicability in Applicability:
            self.assertEqual(
                classify(applicability, EvidenceState.EMPTY).disposition,
                Disposition.CONFLICT,
            )


if __name__ == "__main__":
    unittest.main()
