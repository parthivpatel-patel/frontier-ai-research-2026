"""Protocol 077: deterministic adjudication-selection negative controls.

Synthetic mathematical examples only. These are NOT physics observations,
model evaluations, or empirical findings. Execute on an eligible free hosted
runner only after account-specific billing/runner safeguards are verified.
"""
from __future__ import annotations

import unittest
from fractions import Fraction


def observed_unsafe_rate(records, verifier):
    """Unsafe fraction among accepted AND independently adjudicated claims."""
    eligible = [r for r in records if r["decisions"][verifier] and r["observed"]]
    if not eligible:
        return None
    return Fraction(sum(r["unsafe"] for r in eligible), len(eligible))


def full_unsafe_rate(records, verifier):
    """Oracle-only rate; never available from incomplete real adjudication."""
    eligible = [r for r in records if r["decisions"][verifier]]
    return Fraction(sum(r["unsafe"] for r in eligible), len(eligible))


def sharp_difference_bounds(records):
    """Bounds on N^-1 sum_i (A_i-B_i)*unsafe_i.

    Missing unsafe labels share one underlying physical truth across A and B.
    No missing-at-random assumption is made. Each missing binary label can
    independently take either value; bounds are sharp for this unconstrained
    finite population.
    """
    if not records:
        raise ValueError("nonempty population required")
    lower = upper = 0
    for r in records:
        a, b = r["decisions"]
        coefficient = int(a) - int(b)
        if r["observed"]:
            contribution = coefficient * int(r["unsafe"])
            lower += contribution
            upper += contribution
        else:
            lower += min(0, coefficient)
            upper += max(0, coefficient)
    return Fraction(lower, len(records)), Fraction(upper, len(records))


def claim(a, b, unsafe, observed):
    return {"decisions": (a, b), "unsafe": unsafe, "observed": observed}


class SelectionBiasNegativeControls(unittest.TestCase):
    def test_differential_missingness_reverses_observed_order(self):
        # Each verifier accepts four claims: two safe and two unsafe.
        # The actual unsafe acceptance rate is identical at 1/2.
        # Selective adjudication reveals A's safe claims and B's unsafe ones.
        rows = [
            claim(True, False, 0, True),
            claim(True, False, 0, True),
            claim(True, False, 1, False),
            claim(True, False, 1, False),
            claim(False, True, 0, False),
            claim(False, True, 0, False),
            claim(False, True, 1, True),
            claim(False, True, 1, True),
        ]
        self.assertEqual(full_unsafe_rate(rows, 0), Fraction(1, 2))
        self.assertEqual(full_unsafe_rate(rows, 1), Fraction(1, 2))
        self.assertEqual(observed_unsafe_rate(rows, 0), 0)
        self.assertEqual(observed_unsafe_rate(rows, 1), 1)
        # Missing truth prevents signing the full-population difference.
        lo, hi = sharp_difference_bounds(rows)
        self.assertLess(lo, 0)
        # The observed data allow equality at the sharp upper endpoint,
        # but cannot establish strict superiority in either direction.
        self.assertEqual(hi, Fraction(0))

    def test_shared_unknown_truth_cancels(self):
        rows = [claim(True, True, None, False),
                claim(False, False, None, False)]
        self.assertEqual(sharp_difference_bounds(rows),
                         (Fraction(0), Fraction(0)))

    def test_unresolved_disagreement_is_not_identified(self):
        rows = [claim(True, False, None, False),
                claim(False, True, None, False)]
        self.assertEqual(sharp_difference_bounds(rows),
                         (Fraction(-1, 2), Fraction(1, 2)))

    def test_known_truth_identifies_signed_difference(self):
        rows = [claim(True, False, 1, True),
                claim(False, True, 0, True)]
        self.assertEqual(sharp_difference_bounds(rows),
                         (Fraction(1, 2), Fraction(1, 2)))

    def test_empty_population_rejected(self):
        with self.assertRaises(ValueError):
            sharp_difference_bounds([])


if __name__ == "__main__":
    unittest.main()
