"""Protocol 031 adversarial regression checks (constructed data only).

Run on an eligible free cloud runner; never on the user's laptop.
No experimental outcome is claimed until a cloud execution is verified.
"""
from __future__ import annotations

import copy
import unittest

from protocol_031_independent_arithmetic_audit import audit_trace, constructed_grid


def valid_record():
    return {
        "dt": "1/2",
        "states": [
            {"x": "0", "v": "2", "predicates": {"P": True, "Q": False, "R": True}},
            {"x": "1", "v": "2", "predicates": {"P": True, "Q": True, "R": True}},
            {"x": "2", "v": "2", "predicates": {"P": True, "Q": True, "R": True}},
        ],
    }


class TestIndependentPhysicsAudit(unittest.TestCase):
    def test_exact_rational_transition_and_false_alias(self):
        outcome = audit_trace(valid_record())
        self.assertEqual(outcome["states_checked"], 3)
        self.assertEqual(outcome["implication_violations"], 0)
        self.assertEqual(outcome["false_alias_counterexamples"], 1)

    def test_grid_size_is_design_not_measurement(self):
        result = constructed_grid()
        self.assertEqual(result["constructed_cases"], 60)
        self.assertGreater(result["cases_with_P_not_equal_Q"], 0)

    def test_corrupt_position_rejected(self):
        record = valid_record()
        record["states"][1]["x"] = "3/2"
        with self.assertRaises(ValueError):
            audit_trace(record)

    def test_corrupt_velocity_rejected(self):
        record = valid_record()
        record["states"][1]["v"] = "3"
        with self.assertRaises(ValueError):
            audit_trace(record)

    def test_false_predicate_rejected(self):
        record = valid_record()
        record["states"][0]["predicates"]["Q"] = True
        with self.assertRaises(ValueError):
            audit_trace(record)

    def test_nonboolean_predicate_rejected(self):
        record = valid_record()
        record["states"][0]["predicates"]["P"] = 1
        with self.assertRaises(ValueError):
            audit_trace(record)

    def test_nonpositive_dt_rejected(self):
        for dt in ("0", "-1/2"):
            with self.subTest(dt=dt):
                record = valid_record()
                record["dt"] = dt
                with self.assertRaises(ValueError):
                    audit_trace(record)

    def test_empty_trace_rejected(self):
        with self.assertRaises(ValueError):
            audit_trace({"states": []})

    def test_threshold_boundary(self):
        record = {"states": [
            {"x": "-1", "v": "1"},
            {"x": "0", "v": "1"},
            {"x": "1", "v": "1"},
        ]}
        result = audit_trace(record)
        self.assertEqual(result["false_alias_counterexamples"], 1)
        self.assertEqual(result["implication_violations"], 0)


if __name__ == "__main__":
    unittest.main()
