"""Protocol 029 exhaustive bounded differential check (standard library only).

Grammar: depth-zero atoms p0,p1,true,false; depth-one unary ! X F G;
depth-one binary &, |, ->, U. Each AST is evaluated on every 1..3-state
lasso, every loop entry, every valuation of two propositions. Deterministic.
"""
import json
import os
import time

from src.assumption_lasso_witness import _truth, parse
from src.independent_lasso_oracle import satisfaction


def main():
    atoms = ["prop_0", "prop_1", "true", "false"]
    expressions = list(atoms)
    for op in ("!", "X ", "F ", "G "):
        expressions.extend(op + "(" + a + ")" for a in atoms)
    for op in ("&", "|", "->", "U"):
        expressions.extend("(" + a + " " + op + " " + b + ")" for a in atoms for b in atoms)
    checked = 0
    started = time.monotonic()
    for expression in expressions:
        ast = parse(expression)
        for n in range(1, 4):
            for loop in range(n):
                for assignment in range(1 << (2 * n)):
                    labels = tuple(
                        frozenset(p for j, p in enumerate(("prop_0", "prop_1"))
                                  if assignment & (1 << (2 * i + j)))
                        for i in range(n)
                    )
                    masks = {
                        p: sum((1 << i) for i in range(n) if p in labels[i])
                        for p in ("prop_0", "prop_1")
                    }
                    expected = satisfaction(ast, labels, loop)
                    actual_mask = _truth(ast, masks, n, loop)
                    actual = frozenset(i for i in range(n) if actual_mask & (1 << i))
                    checked += 1
                    if actual != expected:
                        raise AssertionError(json.dumps({
                            "expression": expression, "n": n, "loop": loop,
                            "labels": [sorted(s) for s in labels],
                            "oracle": sorted(expected), "existing": sorted(actual)
                        }, sort_keys=True))
    report = {
        "protocol": "029", "grammar_depth": 1,
        "formulas": len(expressions), "comparisons": checked,
        "max_states": 3, "propositions": 2,
        "status": "pass", "elapsed_seconds": round(time.monotonic() - started, 6),
        "commit": os.environ.get("GITHUB_SHA", "unverified_local")
    }
    print(json.dumps(report, sort_keys=True))
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write("### Independent LTL oracle cross-check\\n\\n`" + json.dumps(report) + "`\\n")


if __name__ == "__main__":
    main()
