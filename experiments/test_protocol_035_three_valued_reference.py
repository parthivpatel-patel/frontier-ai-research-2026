"""Independent Protocol 035 regression controls."""
import unittest
from protocol_035_three_valued_reference import (
    adjudicate, independently_valid, reference_cases)


class ThreeValuedReferenceTests(unittest.TestCase):
    def test_reference_projection_included(self):
        _, projected, boolean = reference_cases()
        self.assertLessEqual(projected, boolean)

    def test_real_counterexample_is_falsified(self):
        physical, _, boolean = reference_cases()
        status, witness = adjudicate(
            boolean, physical, lambda p: all(x < 1 for x in p), True)
        self.assertEqual(status, "falsified")
        self.assertTrue(independently_valid(witness))

    def test_spurious_abstract_failure_is_inconclusive(self):
        physical, projected, boolean = reference_cases()
        # Boolean trace (False, True, False) is abstract-only.
        self.assertIn((False, True, False), boolean - projected)
        status, witness = adjudicate(
            boolean, physical,
            lambda p: p != (False, True, False), True)
        self.assertEqual((status, witness), ("inconclusive", None))

    def test_sound_abstract_safety_can_verify_bounded_property(self):
        physical, _, boolean = reference_cases()
        status, witness = adjudicate(
            boolean, physical, lambda p: len(p) == 3, True)
        self.assertEqual((status, witness), ("verified_bounded", None))

    def test_no_soundness_no_verification(self):
        physical, _, boolean = reference_cases()
        status, _ = adjudicate(
            boolean, physical, lambda p: len(p) == 3, False)
        self.assertEqual(status, "inconclusive")

    def test_invalid_trace_not_accepted_as_physical(self):
        self.assertFalse(independently_valid((0, 2, 2)))


if __name__ == "__main__":
    unittest.main()
