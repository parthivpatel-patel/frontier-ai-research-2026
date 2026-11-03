"""Protocol 030: falsify overconfident proposition-identity assumptions.

Constructed examples only. No physical dataset or AI-model outputs are used.
This is a deterministic cloud-executable negative control, not evidence of novelty.
"""
import json
from src.assumption_lasso_witness import find_counterexample, parse
from src.independent_lasso_oracle import satisfaction


def main():
    left, right = "G prop_0", "G prop_1"
    unconstrained = find_counterexample(left, right, max_states=3, max_propositions=2)
    constrained = find_counterexample(
        left, right, max_states=3, max_propositions=2,
        equalities=(("prop_0", "prop_1"),),
    )
    # Independently inspect a one-state infinite lasso where p0 is true and p1 false.
    trace = (frozenset({"prop_0"}),)
    left_holds = 0 in satisfaction(parse(left), trace, 0)
    right_holds = 0 in satisfaction(parse(right), trace, 0)
    assert left_holds and not right_holds, "independent oracle did not confirm disagreement"
    assert unconstrained["status"] == "witness", unconstrained
    assert constrained["status"] == "no_witness_within_bound", constrained
    report = {
        "protocol": "030", "kind": "constructed_negative_control",
        "formula_left": left, "formula_right": right,
        "unconstrained": unconstrained, "assumed_equal": constrained,
        "independent_one_state_oracle": {
            "labels": [["prop_0"]], "loop_start": 0,
            "left_holds": left_holds, "right_holds": right_holds,
        },
        "interpretation": (
            "An incorrect identity assumption can conceal a genuine logical "
            "counterexample. Absence within a finite bound is not a proof "
            "of unrestricted equivalence."
        ),
    }
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
