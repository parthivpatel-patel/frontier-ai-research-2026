"""Protocol 031: exact finite physical traces and independently checkable JSON.

Constructed one-dimensional constant-velocity dynamics; NOT observed physics or
evidence of scientific novelty. Standard library only. No model inference.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path


def trace(x0: int, v0: int, transitions: int) -> list[dict]:
    if transitions not in range(1, 5) or x0 not in range(-2, 3) or v0 not in (-1, 0, 1):
        raise ValueError("outside preregistered bounds")
    x, v = Fraction(x0), Fraction(v0)
    states = []
    for t in range(transitions + 1):
        states.append({"t": t, "x_m": str(x), "v_m_per_s": str(v),
                       "P": x >= 0, "Q": x >= 1, "R": v >= 0})
        x += v  # dt = 1 second
    return states


def independently_validate(states: list[dict]) -> None:
    for i, s in enumerate(states):
        x, v = Fraction(s["x_m"]), Fraction(s["v_m_per_s"])
        if s["t"] != i or (s["P"], s["Q"], s["R"]) != (x >= 0, x >= 1, v >= 0):
            raise AssertionError("invalid state or proposition")
        if i:
            prev = states[i - 1]
            if x != Fraction(prev["x_m"]) + Fraction(prev["v_m_per_s"]) or v != Fraction(prev["v_m_per_s"]):
                raise AssertionError("invalid physical transition")


def experiment() -> dict:
    records = []
    for horizon in range(1, 5):
        for x0 in range(-2, 3):
            for v0 in (-1, 0, 1):
                states = trace(x0, v0, horizon)
                independently_validate(states)
                # Correct implication Q=>P must always hold; false alias P==Q
                # can suppress a real physically realizable distinction.
                if any(s["Q"] and not s["P"] for s in states):
                    raise AssertionError("physical implication violated")
                records.append({"x0_m": x0, "v0_m_per_s": v0,
                                "transitions": horizon, "states": states,
                                "false_alias_violated": any(s["P"] != s["Q"] for s in states)})
    witness = next(r for r in records if r["x0_m"] == 0 and r["v0_m_per_s"] == 0 and r["transitions"] == 1)
    assert witness["false_alias_violated"]
    return {"protocol": "031", "status": "constructed_finite_trace_enumeration",
            "semantics": "finite states t=0..horizon inclusive; statewise predicates; no infinite LTL claims",
            "units": {"x": "m", "v": "m/s", "dt": "1 s"},
            "traces": len(records),
            "correct_implication_violations": 0,
            "false_alias_violation_traces": sum(r["false_alias_violated"] for r in records),
            "illustrative_witness": witness,
            "all_traces": records}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = experiment()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Constructed traces: {result['traces']}; output: {args.output}")


if __name__ == "__main__":
    main()
