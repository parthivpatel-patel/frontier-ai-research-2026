"""Protocol 192: bounded exhaustive oracle for Protocol 191 positive certificates.

This is a deterministic test specification, not a record of executed results.
It uses only the Python standard library and deliberately caps graph size.
Run on independently verified zero-cost cloud CI, never on the user's laptop.
"""
import itertools
import unittest

from protocol_191_certificate_checker import CertificateError, check_positive, check_negative


def enumerate_feasible(document):
    """Enumerate all simple permitted graphs with original degree margins."""
    allowed = [tuple(edge) for edge in document["permitted"]]
    original = [tuple(edge) for edge in document["original"]]
    source_degrees = {s: sum(a == s for a, _ in original) for s in document["sources"]}
    target_degrees = {t: sum(b == t for _, b in original) for t in document["targets"]}
    for subset in itertools.combinations(allowed, len(original)):
        if (all(sum(a == s for a, _ in subset) == d for s, d in source_degrees.items())
                and all(sum(b == t for _, b in subset) == d for t, d in target_degrees.items())):
            yield [list(edge) for edge in subset]


class Protocol192ExhaustiveOracle(unittest.TestCase):
    def test_small_graph_positive_soundness_and_completeness(self):
        # All 2x2 permitted universes, nonempty admissible supersets,
        # and each feasible original. No random seeds or external dependencies.
        sources, targets = ["s1", "s2"], ["t1", "t2"]
        universe = [[s, t] for s in sources for t in targets]
        checked = 0
        for permitted_mask in range(1 << len(universe)):
            permitted = [edge for i, edge in enumerate(universe)
                         if permitted_mask & (1 << i)]
            for original_mask in range(1 << len(permitted)):
                original = [edge for i, edge in enumerate(permitted)
                            if original_mask & (1 << i)]
                doc = dict(sources=sources, targets=targets, permitted=permitted,
                           admissible=permitted, original=original)
                feasible = list(enumerate_feasible(doc))
                if original not in feasible:
                    continue
                for admissible_mask in range(1 << len(permitted)):
                    admissible = [edge for i, edge in enumerate(permitted)
                                  if admissible_mask & (1 << i)]
                    if not all(edge in admissible for edge in original):
                        continue
                    doc["admissible"] = admissible
                    forbidden = set(map(tuple, permitted)) - set(map(tuple, admissible))
                    eligible = [graph for graph in feasible
                                if set(map(tuple, graph)) & forbidden]
                    for graph in feasible:
                        expected = bool(set(map(tuple, graph)) & forbidden)
                        if expected:
                            self.assertTrue(check_positive(doc, graph))
                        else:
                            with self.assertRaises(CertificateError):
                                check_positive(doc, graph)
                    if not eligible and not forbidden:
                        self.assertTrue(check_negative(doc, []))
                    checked += 1
        self.assertGreater(checked, 0)

    def test_negative_certificate_rejects_forged_claim_on_crossed_matching(self):
        doc = dict(sources=["s1", "s2"], targets=["t1", "t2"],
                   permitted=[["s1", "t1"], ["s1", "t2"],
                              ["s2", "t1"], ["s2", "t2"]],
                   admissible=[["s1", "t1"], ["s2", "t2"]],
                   original=[["s1", "t1"], ["s2", "t2"]])
        # Every alleged cut here must fail because the crossed matching exists.
        for xmask in range(4):
            for ymask in range(4):
                x = [s for i, s in enumerate(doc["sources"]) if xmask & (1 << i)]
                y = [t for i, t in enumerate(doc["targets"]) if ymask & (1 << i)]
                manifest = [
                    dict(edge=["s1", "t2"], reason="cut", X=x, Y=y),
                    dict(edge=["s2", "t1"], reason="cut", X=x, Y=y),
                ]
                with self.assertRaises(CertificateError):
                    check_negative(doc, manifest)


if __name__ == "__main__":
    unittest.main()
