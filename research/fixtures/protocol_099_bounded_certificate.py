"""Protocol 099: fail-closed admission wrapper for Protocol 093.

Standard-library-only. Do not run on the user's laptop. This wrapper is
not a process-level CPU, memory, or wall-time sandbox.
"""
from fractions import Fraction
from protocol_098_structural_preflight import admit, PreflightRefusal
from test_protocol_093_complete_policy_trees import certify, STOP


def bounded_certify(costs, budget, worlds, *, max_trees=10000,
                    max_claims=6, max_worlds=64, max_budget=12,
                    max_cost=12):
    """Validate and count *before* constructing contingent policy trees.

    Returns the original oracle's (optimal value, witness, generated count).
    An admitted call must still run in a separately resource-limited process.
    """
    predicted = admit(costs, budget, worlds, max_claims=max_claims,
                      max_trees=max_trees, max_worlds=max_worlds,
                      max_budget=max_budget, max_cost=max_cost)
    # The original cap counts generator activity, not just complete policies.
    # Keep it as a second, potentially stricter safety stop; do not equate it
    # to the structural count.
    value, witness, actual = certify(costs, budget, worlds, cap=max_trees)
    if actual != predicted:
        raise AssertionError("structural count disagrees with enumerator")
    return value, witness, actual


def score_witness(tree, costs, budget, worlds):
    """Independent, non-optimizing legality and exact-reward check."""
    n = len(costs)
    def walk(node, remaining, balance):
        if node == STOP:
            return
        if not isinstance(node, tuple) or len(node) != 3:
            raise ValueError("invalid policy node")
        i, no, yes = node
        if type(i) is not int or i not in remaining or costs[i] > balance:
            raise ValueError("illegal verification action")
        rest = remaining - {i}
        walk(no, rest, balance - costs[i])
        walk(yes, rest, balance - costs[i])
    walk(tree, set(range(n)), budget)
    total = Fraction(0)
    for world, mass in worlds.items():
        node, reward = tree, 0
        while node != STOP:
            i, no, yes = node
            reward += world[i]
            node = yes if world[i] else no
        total += Fraction(mass) * reward
    return total
