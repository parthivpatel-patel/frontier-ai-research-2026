"""Protocol 041: reachable-state simulation versus observable finite traces.

Constructed, standard-library-only regression controls. No empirical claims.
Run in a free cloud runner with:
    python -m unittest discover -s experiments -p 'test_protocol_041*.py' -v
"""
import unittest
from collections import deque
from itertools import product


def reachable(edges, initial):
    """Reachable concrete states, including the initial state."""
    seen = {initial}
    pending = deque([initial])
    while pending:
        for nxt in edges[pending.popleft()]:
            if nxt not in seen:
                seen.add(nxt)
                pending.append(nxt)
    return seen


def reachable_simulation(concrete, abstract, initial, mapping):
    """Check initial membership and all reachable concrete transitions.

    This is a sufficient condition for preservation of all finite projected
    state traces, provided both graphs are total on their listed states and
    mapping is a total function on the reachable concrete states.
    """
    if initial not in concrete:
        return False
    if set(concrete) != {x for x in concrete}:
        return False
    if any(n not in concrete for successors in concrete.values() for n in successors):
        return False
    if any(n not in abstract for successors in abstract.values() for n in successors):
        return False
    if not all(concrete.values()) or not all(abstract.values()):
        return False  # Explicit infinite-stuttering/deadlock convention required.
    states = reachable(concrete, initial)
    if any(s not in mapping or mapping[s] not in abstract for s in states):
        return False
    for s in states:
        for t in concrete[s]:
            if mapping[t] not in abstract[mapping[s]]:
                return False
    return True


def finite_paths(edges, start, horizon):
    paths = {(start,)}
    for _ in range(horizon):
        paths = {p + (n,) for p in paths for n in edges[p[-1]]}
    return paths


def projected_inclusion(concrete, abstract, initial, mapping, horizon):
    if initial not in concrete or initial not in mapping:
        return False
    projected = {tuple(mapping[x] for x in p)
                 for p in finite_paths(concrete, initial, horizon)}
    return projected <= finite_paths(abstract, mapping[initial], horizon)


class Protocol041Controls(unittest.TestCase):
    def test_unreachable_bad_edge_is_not_a_counterexample(self):
        concrete = {0: (0,), 1: (0,)}
        abstract = {"a": ("a",), "b": ("b",)}
        mapping = {0: "a", 1: "b"}
        self.assertTrue(reachable_simulation(concrete, abstract, 0, mapping))
        for horizon in range(5):
            self.assertTrue(projected_inclusion(
                concrete, abstract, 0, mapping, horizon))

    def test_reachable_bad_edge_has_short_witness(self):
        concrete = {0: (1,), 1: (1,)}
        abstract = {"a": ("a",), "b": ("b",)}
        mapping = {0: "a", 1: "b"}
        self.assertFalse(reachable_simulation(concrete, abstract, 0, mapping))
        self.assertTrue(projected_inclusion(concrete, abstract, 0, mapping, 0))
        self.assertFalse(projected_inclusion(concrete, abstract, 0, mapping, 1))

    def test_observational_collapse_does_not_imply_state_identity(self):
        concrete = {0: (1,), 1: (0,)}
        abstract = {"same": ("same",)}
        mapping = {0: "same", 1: "same"}
        self.assertTrue(reachable_simulation(concrete, abstract, 0, mapping))
        self.assertTrue(projected_inclusion(concrete, abstract, 0, mapping, 8))

    def test_reject_missing_mapping_and_dangling_transition(self):
        self.assertFalse(reachable_simulation(
            {0: (1,), 1: (1,)}, {"a": ("a",)}, 0, {0: "a"}))
        self.assertFalse(reachable_simulation(
            {0: (2,)}, {"a": ("a",)}, 0, {0: "a"}))

    def test_deadlocks_are_explicitly_out_of_scope(self):
        self.assertFalse(reachable_simulation(
            {0: ()}, {"a": ("a",)}, 0, {0: "a"}))

    def test_exhaustive_small_total_graphs_soundness_direction(self):
        # 2 concrete and 2 abstract states; each successor set nonempty.
        successors = [(0,), (1,), (0, 1)]
        checked = 0
        for c0, c1, a0, a1, m0, m1 in product(
                successors, successors, successors, successors,
                (0, 1), (0, 1)):
            concrete = {0: c0, 1: c1}
            abstract = {0: a0, 1: a1}
            mapping = {0: m0, 1: m1}
            if reachable_simulation(concrete, abstract, 0, mapping):
                for horizon in range(5):
                    self.assertTrue(projected_inclusion(
                        concrete, abstract, 0, mapping, horizon))
            checked += 1
        self.assertEqual(checked, 324)


if __name__ == "__main__":
    unittest.main()
