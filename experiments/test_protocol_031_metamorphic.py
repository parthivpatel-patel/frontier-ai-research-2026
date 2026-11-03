"""Protocol 031 metamorphic tests: independently constructed rational traces.

These tests are intended for eligible zero-cost cloud execution only.
They do not constitute observed results until a cloud run is verified.
"""
from fractions import Fraction
import unittest

from protocol_031_independent_arithmetic_audit import audit_trace


def make_trace(x0, v, dt, steps):
    """Construct a trace by exact rational recurrence, not floating-point math."""
    x0, v, dt = map(Fraction, (x0, v, dt))
    states = []
    for t in range(steps + 1):
        states.append({"x": str(x0 + t * v * dt), "v": str(v)})
    return {"dt": str(dt), "states": states}


class MetamorphicPhysicsAudit(unittest.TestCase):
    def test_fractional_timesteps_and_boundaries(self):
        for dt in ("1/2", "2/3", "3/4"):
            for x0 in ("-1", "0", "1/2", "1"):
                for v in ("-1", "0", "1"):
                    with self.subTest(dt=dt, x0=x0, v=v):
                        result = audit_trace(make_trace(x0, v, dt, 4))
                        self.assertEqual(result["implication_violations"], 0)
                        self.assertEqual(result["states_checked"], 5)

    def test_position_translation_preserves_dynamics(self):
        source = make_trace("-1/2", "2/3", "3/4", 4)
        shifted = {
            "dt": source["dt"],
            "states": [
                {"x": str(Fraction(s["x"]) + Fraction(3, 2)), "v": s["v"]}
                for s in source["states"]
            ],
        }
        self.assertTrue(audit_trace(source)["valid"])
        self.assertTrue(audit_trace(shifted)["valid"])

    def test_velocity_time_rescaling_preserves_positions(self):
        source = make_trace("-1/2", "2/3", "3/4", 4)
        rescaled = {
            "dt": str(Fraction(source["dt"]) / 2),
            "states": [
                {"x": s["x"], "v": str(Fraction(s["v"]) * 2)}
                for s in source["states"]
            ],
        }
        self.assertTrue(audit_trace(rescaled)["valid"])
        self.assertEqual(
            [s["x"] for s in source["states"]],
            [s["x"] for s in rescaled["states"]],
        )

    def test_corrupted_fractional_transition_rejected(self):
        trace = make_trace("0", "1/3", "1/2", 3)
        trace["states"][2]["x"] = "1/2"
        with self.assertRaisesRegex(ValueError, "invalid physical transition"):
            audit_trace(trace)

    def test_physical_implication_is_not_identity(self):
        trace = make_trace("1/2", "0", "1/2", 2)
        result = audit_trace(trace)
        self.assertEqual(result["implication_violations"], 0)
        self.assertEqual(result["false_alias_counterexamples"], 3)


if __name__ == "__main__":
    unittest.main()
