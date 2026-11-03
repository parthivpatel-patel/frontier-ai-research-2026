"""Protocol 031: independent exact-arithmetic audit of constructed physical traces.

No model inference, numerical approximation, or external dependencies.
This module does not establish novelty or empirical AI performance.
"""
from __future__ import annotations

from fractions import Fraction
import json


def audit_trace(record: dict) -> dict:
    """Check a trajectory without trusting its recorded predicate labels."""
    states = record["states"]
    if not states:
        raise ValueError("empty trajectory")
    dt = Fraction(record.get("dt", "1"))
    if dt <= 0:
        raise ValueError("nonpositive timestep")
    checked = []
    for index, state in enumerate(states):
        x = Fraction(str(state["x"]))
        v = Fraction(str(state["v"]))
        actual = {"P": x >= 0, "Q": x >= 1, "R": v >= 0}
        declared = state.get("predicates")
        if declared is not None:
            if set(declared) != set(actual) or any(type(declared[k]) is not bool for k in actual):
                raise ValueError("invalid predicate schema")
            if declared != actual:
                raise ValueError(f"predicate mismatch at state {index}")
        if index:
            prev = checked[-1]
            if x != prev["x"] + prev["v"] * dt or v != prev["v"]:
                raise ValueError(f"invalid physical transition at state {index}")
        checked.append({"x": x, "v": v, **actual})
    implication_violations = sum(s["Q"] and not s["P"] for s in checked)
    alias_counterexamples = sum(s["P"] != s["Q"] for s in checked)
    return {
        "valid": True,
        "states_checked": len(checked),
        "implication_violations": implication_violations,
        "false_alias_counterexamples": alias_counterexamples,
        "finite_trace_only": True,
    }


def constructed_grid() -> dict:
    """Exhaustively audit the preregistered 5 x 3 x 4 grid."""
    cases = 0
    false_alias_cases = 0
    for x0 in range(-2, 3):
        for v0 in (-1, 0, 1):
            for horizon in range(1, 5):
                states = [{"x": str(x0 + t * v0), "v": str(v0)}
                          for t in range(horizon + 1)]
                result = audit_trace({"dt": "1", "states": states})
                assert result["implication_violations"] == 0
                cases += 1
                false_alias_cases += result["false_alias_counterexamples"] > 0
    return {"constructed_cases": cases,
            "cases_with_P_not_equal_Q": false_alias_cases,
            "claim": "constructed finite-trace arithmetic check only"}


if __name__ == "__main__":
    print(json.dumps(constructed_grid(), sort_keys=True))
