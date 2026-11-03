"""Protocol 034: exhaustive finite-state abstraction controls.

Standard-library-only reference implementation. This is a constructed
model-checking regression, not evidence of a new AI method.
"""
from itertools import product
import json
import unittest

# Concrete states: position 0, 1, 2. Physically permitted transitions.
CONCRETE = {0: (0, 1), 1: (1, 2), 2: (2,)}
# Predicate P = position >= 1. The abstract model intentionally forgets
# the position and admits all Boolean successor pairs.
def predicate(x):
    return x >= 1


def paths(edges, initial, transitions):
    current = [(initial,)]
    for _ in range(transitions):
        current = [path + (nxt,) for path in current for nxt in edges[path[-1]]]
    return set(current)


def validate_concrete(path):
    return bool(path) and path[0] == 0 and all(
        nxt in CONCRETE[prev] for prev, nxt in zip(path, path[1:])
    )


def experiment():
    horizon = 2
    physical = paths(CONCRETE, 0, horizon)
    abstract_edges = {False: (False, True), True: (False, True)}
    abstract = paths(abstract_edges, False, horizon)
    projected = {tuple(predicate(x) for x in path) for path in physical}
    assert projected <= abstract, "sound overapproximation violated"
    spurious = abstract - projected
    assert spurious, "missing spurious path control"
    # Incorrect constraint: forbid visiting position 1. This removes a
    # reachable witness of P, so a universal claim 'always not P' becomes
    # falsely safe if checked only against the constrained traces.
    bad_subset = {p for p in physical if all(x != 1 for x in p)}
    witness = next(p for p in sorted(physical) if 1 in p)
    assert validate_concrete(witness)
    assert all(1 not in p for p in bad_subset)
    return {
        "horizon_transitions": horizon,
        "concrete_paths": len(physical),
        "abstract_paths": len(abstract),
        "projected_paths": len(projected),
        "spurious_abstract_paths": len(spurious),
        "unsound_remaining_paths": len(bad_subset),
        "excluded_valid_witness": list(witness),
        "claim": "constructed bounded finite-state regression only",
    }


class Protocol034Controls(unittest.TestCase):
    def test_all_concrete_paths_valid(self):
        self.assertTrue(all(validate_concrete(p) for p in paths(CONCRETE, 0, 2)))

    def test_sound_projection_included(self):
        concrete = paths(CONCRETE, 0, 2)
        abstract = paths({False: (False, True), True: (False, True)}, False, 2)
        self.assertTrue({tuple(map(predicate, p)) for p in concrete} <= abstract)

    def test_spurious_abstract_trace(self):
        concrete = paths(CONCRETE, 0, 2)
        projected = {tuple(map(predicate, p)) for p in concrete}
        self.assertNotIn((False, True, False), projected)

    def test_unsound_constraint_hides_real_witness(self):
        physical = paths(CONCRETE, 0, 2)
        witness = (0, 1, 2)
        self.assertIn(witness, physical)
        restricted = {p for p in physical if 1 not in p}
        self.assertNotIn(witness, restricted)
        self.assertTrue(validate_concrete(witness))

    def test_summary_is_constructed(self):
        self.assertEqual(experiment()["claim"], "constructed bounded finite-state regression only")


if __name__ == "__main__":
    print(json.dumps(experiment(), sort_keys=True))
    unittest.main()
