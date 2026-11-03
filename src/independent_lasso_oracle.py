"""Independent set-based LTL semantics on explicit finite lasso graphs.

Protocol 029. Does not import or invoke the existing bitmask evaluator.
Input AST convention is documented here to permit differential testing.
This implementation is not an independent parser or proof of full LTL correctness.
"""
from __future__ import annotations


def satisfaction(ast: tuple, states: tuple[frozenset[str], ...], loop_start: int) -> frozenset[int]:
    """Return states satisfying an LTL AST on the infinite lasso.

    The last state transitions to loop_start; all other states transition to i+1.
    Operators: atom, true, false, not, and, or, next, finally, always, until.
    Implication is represented by (or, (not, antecedent), consequent).
    """
    n = len(states)
    if not n or not 0 <= loop_start < n:
        raise ValueError("invalid lasso")
    universe = frozenset(range(n))

    def pre(target: frozenset[int]) -> frozenset[int]:
        return frozenset(i for i in range(n) if (i + 1 if i + 1 < n else loop_start) in target)

    def least(left: frozenset[int], right: frozenset[int]) -> frozenset[int]:
        current = right
        while True:
            updated = right | (left & pre(current))
            if updated == current:
                return current
            current = updated

    def evaluate(node: tuple) -> frozenset[int]:
        op = node[0]
        if op == "atom":
            return frozenset(i for i, labels in enumerate(states) if node[1] in labels)
        if op == "true":
            return universe
        if op == "false":
            return frozenset()
        if op == "not":
            return universe - evaluate(node[1])
        if op == "and":
            return evaluate(node[1]) & evaluate(node[2])
        if op == "or":
            return evaluate(node[1]) | evaluate(node[2])
        if op == "next":
            return pre(evaluate(node[1]))
        if op == "finally":
            return least(universe, evaluate(node[1]))
        if op == "until":
            return least(evaluate(node[1]), evaluate(node[2]))
        if op == "always":
            # Greatest fixed point Z = phi AND X Z, initialized at all states.
            phi = evaluate(node[1])
            current = universe
            while True:
                updated = phi & pre(current)
                if updated == current:
                    return current
                current = updated
        raise ValueError(f"unsupported AST operator: {op!r}")

    return evaluate(ast)
