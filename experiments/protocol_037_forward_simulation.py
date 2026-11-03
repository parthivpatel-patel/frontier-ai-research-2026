"""Protocol 037: finite-state forward-simulation certificate checker.

A local, inductive sufficient condition for unbounded trace inclusion.
This is classical simulation checking, not a new formal-methods result.
No AI/model calls, dependencies, or physical-system generalization.
"""
import unittest
from collections import deque


def check_simulation(concrete, abstract, mapping, concrete_initial, abstract_initial):
    """Check total functional abstraction on reachable concrete states.

    If initial states correspond and every concrete edge projects to an
    abstract edge, all finite concrete traces project to abstract traces,
    by induction on trace length. Only the supplied finite graphs are covered.
    """
    if not isinstance(concrete, dict) or not concrete:
        raise ValueError("empty concrete graph")
    if not isinstance(abstract, dict) or not abstract:
        raise ValueError("empty abstract graph")
    if concrete_initial not in concrete or abstract_initial not in abstract:
        raise ValueError("missing initial state")
    if set(mapping) != set(concrete):
        raise ValueError("mapping must cover all concrete states")
    if any(value not in abstract for value in mapping.values()):
        raise ValueError("mapping points outside abstract graph")
    for graph in (concrete, abstract):
        for state, targets in graph.items():
            if not isinstance(targets, (tuple, list, set, frozenset)):
                raise ValueError("successors must be a finite collection")
            if any(target not in graph for target in targets):
                raise ValueError("edge targets missing state")
    if mapping[concrete_initial] != abstract_initial:
        return {"valid": False, "reason": "initial mismatch",
                "counterexample": [concrete_initial], "checked_states": 0}
    seen = {concrete_initial}
    paths = {concrete_initial: (concrete_initial,)}
    queue = deque([concrete_initial])
    while queue:
        state = queue.popleft()
        for target in concrete[state]:
            if mapping[target] not in abstract[mapping[state]]:
                return {"valid": False, "reason": "missing abstract edge",
                        "counterexample": list(paths[state] + (target,)),
                        "checked_states": len(seen)}
            if target not in seen:
                seen.add(target)
                paths[target] = paths[state] + (target,)
                queue.append(target)
    return {"valid": True, "reason": "forward simulation on reachable states",
            "counterexample": None, "checked_states": len(seen)}


class SimulationTests(unittest.TestCase):
    def setUp(self):
        self.c = {0: (0, 1), 1: (1, 2), 2: (2,)}
        self.a = {False: (False, True), True: (True,)}
        self.m = {0: False, 1: True, 2: True}

    def test_valid_inductive_certificate(self):
        self.assertTrue(check_simulation(self.c, self.a, self.m, 0, False)["valid"])

    def test_missing_transition_yields_concrete_witness(self):
        a = {False: (False,), True: (True,)}
        result = check_simulation(self.c, a, self.m, 0, False)
        self.assertFalse(result["valid"])
        self.assertEqual(result["counterexample"], [0, 1])

    def test_initial_mismatch(self):
        self.assertEqual(check_simulation(self.c, self.a, self.m, 0, True)
                         ["reason"], "initial mismatch")

    def test_unreachable_missing_edge_does_not_invalidate(self):
        c = {0: (0,), 1: (0,)}
        m = {0: False, 1: True}
        a = {False: (False,), True: (True,)}
        self.assertTrue(check_simulation(c, a, m, 0, False)["valid"])

    def test_incomplete_mapping_rejected(self):
        with self.assertRaises(ValueError):
            check_simulation(self.c, self.a, {0: False}, 0, False)

    def test_dangling_transition_rejected(self):
        with self.assertRaises(ValueError):
            check_simulation({0: (3,)}, self.a, {0: False}, 0, False)

    def test_empty_graph_rejected(self):
        with self.assertRaises(ValueError):
            check_simulation({}, self.a, {}, 0, False)


if __name__ == "__main__":
    unittest.main()
