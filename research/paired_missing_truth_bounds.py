"""Sharp paired unsafe-acceptance bounds with missing physical truth.

This module is dependency-free. It does not infer missing truth or establish
physical validity. Each row represents the SAME claim for two verifiers.
"""
from __future__ import annotations

from typing import Iterable, Mapping


def paired_unsafe_difference_bounds(rows: Iterable[Mapping[str, object]]) -> dict[str, float | int]:
    """Bound (unsafe accepted by A - unsafe accepted by B)/N.

    accepted_a/accepted_b must be bool; unsafe must be bool or None.
    Unknown truth is shared across verifiers for each claim. For unknown
    records, the contribution (a-b)*unsafe ranges over {0, a-b}.
    Bounds are sharp absent cross-record restrictions on missing truth.
    """
    lo = hi = 0
    n = unknown = 0
    for row in rows:
        a = row["accepted_a"]
        b = row["accepted_b"]
        y = row["unsafe"]
        if type(a) is not bool or type(b) is not bool:
            raise ValueError("accepted_a and accepted_b must be booleans")
        if y is not None and type(y) is not bool:
            raise ValueError("unsafe must be boolean or None")
        n += 1
        coefficient = int(a) - int(b)
        if y is None:
            unknown += 1
            lo += min(0, coefficient)
            hi += max(0, coefficient)
        else:
            lo += coefficient * int(y)
            hi += coefficient * int(y)
    if not n:
        raise ValueError("at least one paired claim is required")
    return {
        "n": n, "unknown_truth": unknown,
        "lower": lo / n, "upper": hi / n,
    }


if __name__ == "__main__":
    import unittest

    class SharpBoundsTests(unittest.TestCase):
        def test_shared_unknown_both_accept_cancels(self):
            result = paired_unsafe_difference_bounds([
                {"accepted_a": True, "accepted_b": True, "unsafe": None}
            ])
            self.assertEqual((result["lower"], result["upper"]), (0, 0))

        def test_unknown_disagreement(self):
            result = paired_unsafe_difference_bounds([
                {"accepted_a": True, "accepted_b": False, "unsafe": None},
                {"accepted_a": False, "accepted_b": True, "unsafe": None},
            ])
            self.assertEqual((result["lower"], result["upper"]), (-0.5, 0.5))

        def test_known_truth_and_unknown(self):
            result = paired_unsafe_difference_bounds([
                {"accepted_a": True, "accepted_b": False, "unsafe": True},
                {"accepted_a": False, "accepted_b": True, "unsafe": False},
                {"accepted_a": False, "accepted_b": True, "unsafe": None},
            ])
            self.assertAlmostEqual(result["lower"], 0)
            self.assertAlmostEqual(result["upper"], 1 / 3)

        def test_no_records(self):
            with self.assertRaises(ValueError):
                paired_unsafe_difference_bounds([])

        def test_reject_nonboolean(self):
            with self.assertRaises(ValueError):
                paired_unsafe_difference_bounds([
                    {"accepted_a": 1, "accepted_b": False, "unsafe": None}
                ])

        def test_reject_nonboolean_truth(self):
            with self.assertRaises(ValueError):
                paired_unsafe_difference_bounds([
                    {"accepted_a": True, "accepted_b": False, "unsafe": 1}
                ])

    unittest.main()
