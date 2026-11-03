"""Protocol 039: complete finite-horizon converse for functional abstraction.

For a total functional state map on a finite concrete graph, a failed
reachable-edge simulation condition has a projected-trace witness of length
at most |reachable concrete states| edges. This does not extend unchanged
to arbitrary relational simulation or continuous physical dynamics.

Authored regression tests; execution on a cloud runner is not asserted.
"""
import itertools
import unittest

try:
    from experiments.protocol_037_forward_simulation import check_simulation
    from experiments.test_protocol_038_differential_oracle import bounded_inclusion
except ModuleNotFoundError:
    from protocol_037_forward_simulation import check_simulation
    from test_protocol_038_differential_oracle import bounded_inclusion


def all_two_state_graphs():
    successors = ((), (0,), (1,), (0, 1))
    for left, right in itertools.product(successors, repeat=2):
        yield {0: left, 1: right}


class Protocol039ConverseTests(unittest.TestCase):
    def test_exhaustive_converse_including_deadlocks(self):
        """Simulation iff trace inclusion through two edges, for two states."""
        states = (0, 1)
        graphs = list(all_two_state_graphs())
        cases = 0
        for concrete, abstract, images, ci, ai in itertools.product(
            graphs, graphs, itertools.product(states, repeat=2), states, states
        ):
            mapping = dict(zip(states, images))
            valid = check_simulation(concrete, abstract, mapping, ci, ai)["valid"]
            oracle = bounded_inclusion(concrete, abstract, mapping, ci, ai, 2)
            self.assertEqual(valid, oracle, (concrete, abstract, mapping, ci, ai))
            cases += 1
        self.assertEqual(cases, 4096)

    def test_rejected_edge_returns_real_short_witness(self):
        concrete = {0: (1,), 1: (2,), 2: (2,)}
        abstract = {0: (1,), 1: (1,)}
        mapping = {0: 0, 1: 1, 2: 0}
        result = check_simulation(concrete, abstract, mapping, 0, 0)
        self.assertFalse(result["valid"])
        self.assertEqual(result["reason"], "missing abstract edge")
        witness = result["counterexample"]
        self.assertEqual(witness, [0, 1, 2])
        self.assertLessEqual(len(witness) - 1, len(concrete))
        self.assertFalse(bounded_inclusion(concrete, abstract, mapping, 0, 0, 2))

    def test_unreachable_bad_edge_not_a_counterexample(self):
        concrete = {0: (0,), 1: (1,)}
        abstract = {0: (0,), 1: ()}
        mapping = {0: 0, 1: 1}
        self.assertTrue(check_simulation(concrete, abstract, mapping, 0, 0)["valid"])
        self.assertTrue(bounded_inclusion(concrete, abstract, mapping, 0, 0, 2))


if __name__ == "__main__":
    unittest.main()
