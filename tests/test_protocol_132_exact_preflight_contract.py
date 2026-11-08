"""Protocol 132: exact-oracle contract checks against analytic preflight.

These tests are intentionally small and deterministic. They do not validate
bootstrap confidence interval coverage or physics model performance.
"""
import unittest
from fractions import Fraction

from research.analytic_preflight import analytic_preflight
from research.protocol_131_exact_oracle import exact_oracle


def paired_rows(accepted, contrasts):
    rows = []
    for i, (a, delta) in enumerate(zip(accepted, contrasts)):
        # Accepted differences -1, 0, +1 can be represented by paired
        # binary unsafe outcomes. Nonaccepted units abstain on both systems.
        if a:
            unsafe_a, unsafe_b = (delta == 1), (delta == -1)
        else:
            unsafe_a = unsafe_b = None
        for system, unsafe in (("A", unsafe_a), ("B", unsafe_b)):
            rows.append({
                "physics_family": "mechanics",
                "lineage_id": f"lineage_{i}",
                "intervention_id": f"item_{i}",
                "system_id": system,
                "accepted": a,
                "response_unsafe": unsafe,
            })
    return rows


class ExactPreflightContractTests(unittest.TestCase):
    def test_reference_cases_match_preflight(self):
        cases = [
            ((True, False), (1, None)),
            ((True, True), (-1, 1)),
            ((True, True, False), (-1, 1, None)),
        ]
        for accepted, contrasts in cases:
            with self.subTest(accepted=accepted, contrasts=contrasts):
                oracle = exact_oracle(accepted, contrasts)
                preflight = analytic_preflight(
                    paired_rows(accepted, contrasts), {"mechanics": 1.0},
                    max_undefined_fraction=1.0,
                )
                self.assertAlmostEqual(
                    preflight["conditional_undefined_probability"],
                    float(oracle["undefined_probability"]),
                    places=14,
                )
                self.assertEqual(
                    preflight["original_defined"],
                    oracle["defined_outcomes"] > 0,
                )

    def test_all_abstain_is_ineligible(self):
        accepted = (False, False)
        oracle = exact_oracle(accepted, (None, None))
        gate = analytic_preflight(
            paired_rows(accepted, (None, None)), {"mechanics": 1.0},
            max_undefined_fraction=1.0,
        )
        self.assertEqual(oracle["undefined_probability"], Fraction(1))
        self.assertFalse(gate["original_defined"])
        self.assertFalse(gate["interval_eligible"])

    def test_threshold_boundary(self):
        rows = paired_rows((True, False), (1, None))
        at_boundary = analytic_preflight(
            rows, {"mechanics": 1.0}, max_undefined_fraction=0.25)
        below_boundary = analytic_preflight(
            rows, {"mechanics": 1.0}, max_undefined_fraction=0.249)
        self.assertTrue(at_boundary["interval_eligible"])
        self.assertFalse(below_boundary["interval_eligible"])


if __name__ == "__main__":
    unittest.main()
