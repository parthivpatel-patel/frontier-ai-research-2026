"""Protocol 108 calibration selector regression tests (authored, not yet executed)."""
import unittest
from calibration_coverage import CalibrationRow, calibrate, apply_frozen_threshold


def row(i, family, score):
    return CalibrationRow(str(i), family, score)


class CalibrationTests(unittest.TestCase):
    def test_exact_target(self):
        result = calibrate([row(1,"m",.9),row(2,"m",.8),row(3,"m",.1),row(4,"m",0)], {"m":.5}, 0)
        self.assertEqual(result["m"].accepted, 2)
        self.assertTrue(result["m"].within_tolerance)

    def test_ties_not_split(self):
        result = calibrate([row(1,"m",.9),row(2,"m",.9),row(3,"m",.1)], {"m":1/3}, 0)
        self.assertEqual(result["m"].accepted, 2)
        self.assertFalse(result["m"].within_tolerance)

    def test_nearest_tie_prefers_fewer(self):
        result = calibrate([row(1,"m",.9),row(2,"m",.1)], {"m":.25}, .25)
        self.assertEqual(result["m"].accepted, 0)

    def test_zero_acceptance(self):
        result = calibrate([row(1,"m",.9)], {"m":0}, 0)
        self.assertEqual(result["m"].accepted, 0)
        self.assertFalse(apply_frozen_threshold([row(2,"m",.9)], result)["2"])

    def test_frozen_application(self):
        selection = calibrate([row(1,"m",.9),row(2,"m",.5)], {"m":.5}, 0)
        outcomes = apply_frozen_threshold([row(3,"m",.7),row(4,"m",.1)], selection)
        self.assertEqual(outcomes, {"3":False,"4":False})

    def test_multiple_families(self):
        result = calibrate([row(1,"m",.9),row(2,"c",.8)], {"m":1,"c":0}, 0)
        self.assertEqual((result["m"].accepted,result["c"].accepted),(1,0))

    def test_invalid_score(self):
        for x in (True,float("nan"),float("inf"),"0.5"):
            with self.assertRaises(ValueError):
                row(1,"m",x)

    def test_invalid_target_and_tolerance(self):
        for x in (True,-.1,1.1,float("nan")):
            with self.assertRaises(ValueError):
                calibrate([row(1,"m",.5)], {"m":x}, 0)
            with self.assertRaises(ValueError):
                calibrate([row(1,"m",.5)], {"m":.5}, x)

    def test_duplicate_ids(self):
        with self.assertRaises(ValueError):
            calibrate([row(1,"m",.5),row(1,"m",.2)], {"m":.5}, 0)

    def test_missing_family(self):
        with self.assertRaises(ValueError):
            calibrate([row(1,"m",.5)], {"m":.5,"c":.5}, 0)

    def test_unknown_heldout_family(self):
        s = calibrate([row(1,"m",.5)], {"m":1}, 0)
        with self.assertRaises(ValueError):
            apply_frozen_threshold([row(2,"c",.4)], s)


if __name__ == "__main__":
    unittest.main()
