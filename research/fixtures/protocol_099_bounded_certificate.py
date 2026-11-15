"""Protocol 099: structural admission and independent policy-witness checks.

Standard-library only. Run only on verified zero-cost cloud infrastructure.
Structural limits do not replace OS-enforced memory and wall-time limits.
"""
from fractions import Fraction
from protocol_098_structural_preflight import admit
from test_protocol_093_complete_policy_trees import certify, STOP


def bounded_certify(costs, budget, worlds, *, max_trees=10000,
                    max_generator_events=1000000, max_claims=6,
                    max_worlds=64, max_budget=12, max_cost=12):
    """Admit by complete-policy count, then separately cap generator events.

    The two caps measure different quantities. An Intractable refusal from
    the generator is not evidence of a structural-count disagreement.
    """
    if type(max_generator_events) is not int or max_generator_events < 1:
        raise ValueError("invalid generator-event cap")
    predicted = admit(costs, budget, worlds, max_claims=max_claims,
                      max_trees=max_trees, max_worlds=max_worlds,
                      max_budget=max_budget, max_cost=max_cost)
    value, witness, actual = certify(
        costs, budget, worlds, cap=max_generator_events)
    if actual != predicted:
        raise AssertionError("complete-policy count disagrees with enumerator")
    if score_witness(witness, costs, budget, worlds) != value:
        raise AssertionError("independent witness score disagrees")
    return value, witness, actual


def score_witness(tree, costs, budget, worlds):
    """Non-optimizing legality and exact expected-reward check."""
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
