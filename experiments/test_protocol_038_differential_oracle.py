"""Protocol 038: independent bounded trace oracle for Protocol 037.

The oracle is intentionally separate from the forward-simulation algorithm.
These tests are authored, not evidence of successful cloud execution.
"""
import itertools
import unittest

try:
    from experiments.protocol_037_forward_simulation import check_simulation
except ModuleNotFoundError:
    from protocol_037_forward_simulation import check_simulation


def traces(graph, initial, edges):
    """Enumerate exact state sequences with a specified number of edges."""
    paths = [(initial,)]
    for _ in range(edges):
        paths = [path + (nxt,) for path in paths for nxt in graph[path[-1]]]
    return set(paths)


def bounded_inclusion(concrete, abstract, mapping, ci, ai, horizon):
    """Independent exhaustive reference: projected concrete traces are abstract traces."""
    for k in range(horizon + 1):
        abstract_paths = traces(abstract, ai, k)
        for path in traces(concrete, ci, k):
            if tuple(mapping[s] for s in path) not in abstract_paths:
                return False
    return True


class DifferentialOracleTests(unittest.TestCase):
    def test_exhaustive_two_state_graphs_simulation_implies_bounded_inclusion(self):
        """All 2-state graphs with nonempty successor sets, all total maps, horizon 4."""
        states = (0, 1)
        successor_sets = ((0,), (1,), (0, 1))
        graphs = [
            {0: a, 1: b}
            for a, b in itertools.product(successor_sets, repeat=2)
        ]
        checked = 0
        for c, a, images, ci, ai in itertools.product(
            graphs, graphs, itertools.product(states, repeat=2), states, states
        ):
            mapping = dict(zip(states, images))
            result = check_simulation(c, a, mapping, ci, ai)
            if result["valid"]:
                self.assertTrue(bounded_inclusion(c, a, mapping, ci, ai, 4))
            checked += 1
        self.assertEqual(checked, 1296)

    def test_failed_simulation_does_not_imply_trace_inclusion_failure(self):
        """An invalid certificate need not refute trace inclusion under other relations.

        Here the functional mapping is fixed, so a reachable missing abstract
        edge is a genuine projected-trace counterexample; the broader warning
        concerns *alternative* abstraction relations and nonfunctional simulation.
        """
        c = {0: (1,), 1: (1,)}
        a = {0: (0,), 1: (1,)}
        m = {0: 0, 1: 1}
        self.assertFalse(check_simulation(c, a, m, 0, 0)["valid"])
        self.assertFalse(bounded_inclusion(c, a, m, 0, 0, 2))

    def test_initial_mismatch_detected_by_zero_length_trace(self):
        c = {0: (0,), 1: (1,)}
        a = {0: (0,), 1: (1,)}
        m = {0: 0, 1: 1}
        self.assertFalse(bounded_inclusion(c, a, m, 0, 1, 0))


if __name__ == "__main__":
    unittest.main()
