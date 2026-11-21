"""Regression checks for acceptance-set diagnostics (standard library only)."""
import unittest

from research.acceptance_set_diagnostics import PairedDecision, acceptance_diagnostics


def row(i, ta, ba, te, be, family="f"):
    return PairedDecision(str(i), family, ta, ba, te, be)


class DiagnosticsTests(unittest.TestCase):
    def test_equal_coverage_different_selection(self):
        data = [row(1, True, False, 0, 0), row(2, True, False, 0, 0),
                row(3, False, True, 1, 1), row(4, False, True, 1, 1)]
        d = acceptance_diagnostics(data)
        self.assertEqual(d["temporal_coverage"], d["baseline_coverage"])
        self.assertEqual(d["temporal_selective_risk"], 0)
        self.assertEqual(d["baseline_selective_risk"], 1)
        self.assertEqual(d["full_temporal_error"], d["full_baseline_error"])
        self.assertIsNone(d["common_temporal_error"])
        self.assertEqual(sum(d[k] for k in ("both", "temporal_only", "baseline_only", "neither")), 4)

    def test_overlap_and_discordance(self):
        d = acceptance_diagnostics([row(1, True, True, 1, 0), row(2, False, False, 0, 1)])
        self.assertEqual(d["both"], 1)
        self.assertEqual(d["paired_full_discordance_t_wrong_b_right"], 1)
        self.assertEqual(d["paired_full_discordance_b_wrong_t_right"], 1)

    def test_zero_accepted_is_undefined(self):
        d = acceptance_diagnostics([row(1, False, False, 0, 0)])
        self.assertIsNone(d["temporal_selective_risk"])
        self.assertIsNone(d["baseline_selective_risk"])

    def test_duplicate_id_rejected(self):
        with self.assertRaises(ValueError):
            acceptance_diagnostics([row(1, True, True, 0, 0), row(1, False, False, 0, 0)])

    def test_invalid_bool_rejected(self):
        with self.assertRaises(TypeError):
            acceptance_diagnostics([row(1, 1, True, 0, 0)])

    def test_invalid_error_rejected(self):
        with self.assertRaises(ValueError):
            acceptance_diagnostics([row(1, True, True, True, 0)])

    def test_missing_family_rejected(self):
        with self.assertRaises(ValueError):
            acceptance_diagnostics([row(1, True, True, 0, 0, "")])

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            acceptance_diagnostics([])


if __name__ == "__main__":
    unittest.main()
