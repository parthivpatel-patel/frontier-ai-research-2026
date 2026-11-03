"""Protocol 036: independently check a finite predicate-abstraction certificate.

Constructed, bounded graph only. Exhaustive enumeration is a reference oracle,
not a scalable proof procedure or a novel formal-verification algorithm.
"""
from itertools import product
import json
import unittest

CONCRETE = {0: (0, 1), 1: (1, 2), 2: (2,)}
ABSTRACT = {False: (False, True), True: (False, True)}
INITIAL = 0
HORIZON = 2


def enumerate_traces(graph, initial, steps):
    if steps < 0:
        raise ValueError("negative horizon")
    frontier = {(initial,)}
    for _ in range(steps):
        frontier = {trace + (successor,)
                    for trace in frontier
                    for successor in graph[trace[-1]]}
    return frontier


def check_certificate(concrete, abstract, mapping, initial, horizon):
    """Independently establish bounded trace inclusion by enumeration.

    Reject incomplete mappings, malformed graphs and non-Boolean abstract
    states. This establishes inclusion for the supplied finite graphs only.
    """
    if type(horizon) is not int or horizon < 0:
        raise ValueError("invalid horizon")
    if not concrete or not abstract or initial not in concrete:
        raise ValueError("invalid initial state or graph")
    states = set(concrete)
    if set(mapping) != states or set(abstract) != {False, True}:
        raise ValueError("incomplete mapping or abstract graph")
    if any(type(value) is not bool for value in mapping.values()):
        raise ValueError("non-Boolean predicate")
    for graph in (concrete, abstract):
        if any(not isinstance(successors, (tuple, list, set)) or
               any(target not in graph for target in successors)
               for successors in graph.values()):
            raise ValueError("malformed transition graph")
    physical = enumerate_traces(concrete, initial, horizon)
    abstraction = enumerate_traces(abstract, mapping[initial], horizon)
    projected = {tuple(mapping[state] for state in trace) for trace in physical}
    missing = sorted(projected - abstraction)
    return {
        "certificate_valid": not missing,
        "horizon_transitions": horizon,
        "physical_trace_count": len(physical),
        "projected_trace_count": len(projected),
        "abstract_trace_count": len(abstraction),
        "missing_projected_traces": [list(t) for t in missing],
        "scope": "exhaustive bounded trace inclusion for supplied finite graphs",
    }


class CertificateTests(unittest.TestCase):
    def setUp(self):
        self.mapping = {state: state >= 1 for state in CONCRETE}

    def test_sound_abstraction(self):
        self.assertTrue(check_certificate(CONCRETE, ABSTRACT, self.mapping,
                                          INITIAL, HORIZON)["certificate_valid"])

    def test_unsound_abstract_transition_rejected(self):
        restricted = {False: (False,), True: (True,)}
        result = check_certificate(CONCRETE, restricted, self.mapping, 0, 2)
        self.assertFalse(result["certificate_valid"])
        self.assertTrue(result["missing_projected_traces"])

    def test_incomplete_mapping_rejected(self):
        with self.assertRaises(ValueError):
            check_certificate(CONCRETE, ABSTRACT, {0: False}, 0, 2)

    def test_bad_transition_rejected(self):
        with self.assertRaises(ValueError):
            check_certificate({0: (9,)}, ABSTRACT, {0: False}, 0, 2)

    def test_zero_horizon(self):
        self.assertTrue(check_certificate(CONCRETE, ABSTRACT, self.mapping,
                                          0, 0)["certificate_valid"])

    def test_negative_horizon_rejected(self):
        with self.assertRaises(ValueError):
            check_certificate(CONCRETE, ABSTRACT, self.mapping, 0, -1)


if __name__ == "__main__":
    unittest.main()
