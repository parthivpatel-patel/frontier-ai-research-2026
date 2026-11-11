"""Protocol 194: independent boundary and metamorphic tests for certificate claims.

These tests are NOT evidence of physics-label validity or model performance.
Execution is deliberately deferred until verified zero-charge cloud CI is available.
"""
import copy
import itertools
import unittest

from protocol_191_certificate_checker import CertificateError, check_positive, check_negative
from test_protocol_192_exhaustive_oracle import enumerate_feasible
from test_protocol_193_negative_oracle import find_certificate


class Protocol194Boundary(unittest.TestCase):
    def test_three_by_three_permutation_invariance(self):
        sources = ["s1", "s2", "s3"]
        targets = ["t1", "t2", "t3"]
        permitted = [[s, t] for s in sources for t in targets]
        original = [["s1", "t1"], ["s2", "t2"], ["s3", "t3"]]
        admissible = original[:]
        doc = dict(sources=sources, targets=targets, permitted=permitted,
                   original=original, admissible=admissible)
        feasible = list(enumerate_feasible(doc))
        self.assertEqual(len(feasible), 6)  # Six perfect matchings.
        for graph in feasible:
            if graph == original:
                with self.assertRaises(CertificateError):
                    check_positive(doc, graph)
            else:
                self.assertTrue(check_positive(doc, graph))
        # Renaming vertices must not change the outcome.
        renamed = copy.deepcopy(doc)
        remap = {**{s: "source_" + s for s in sources},
                 **{t: "target_" + t for t in targets}}
        renamed["sources"] = [remap[x] for x in sources]
        renamed["targets"] = [remap[x] for x in targets]
        for field in ("permitted", "original", "admissible"):
            renamed[field] = [[remap[a], remap[b]] for a, b in doc[field]]
        for graph in feasible:
            transformed = [[remap[a], remap[b]] for a, b in graph]
            if graph == original:
                with self.assertRaises(CertificateError):
                    check_positive(renamed, transformed)
            else:
                self.assertTrue(check_positive(renamed, transformed))

    def test_three_by_three_unique_matching_negative(self):
        # A triangular permitted graph with a unique perfect matching.
        doc = dict(sources=["s1", "s2", "s3"], targets=["t1", "t2", "t3"],
                   permitted=[["s1", "t1"], ["s1", "t2"], ["s1", "t3"],
                              ["s2", "t2"], ["s2", "t3"], ["s3", "t3"]],
                   original=[["s1", "t1"], ["s2", "t2"], ["s3", "t3"]],
                   admissible=[["s1", "t1"], ["s2", "t2"], ["s3", "t3"]])
        self.assertEqual(len(list(enumerate_feasible(doc))), 1)
        forbidden = sorted(set(map(tuple, doc["permitted"])) -
                           set(map(tuple, doc["admissible"])))
        manifest = [find_certificate(doc, edge) for edge in forbidden]
        self.assertNotIn(None, manifest)
        self.assertTrue(check_negative(doc, manifest))

    def test_nonexistent_semantic_corruption_is_not_positive(self):
        doc = dict(sources=["s1", "s2"], targets=["t1", "t2"],
                   permitted=[["s1", "t1"], ["s1", "t2"], ["s2", "t1"], ["s2", "t2"]],
                   original=[["s1", "t1"], ["s2", "t2"]],
                   admissible=[["s1", "t1"], ["s1", "t2"], ["s2", "t1"], ["s2", "t2"]])
        crossed = [["s1", "t2"], ["s2", "t1"]]
        with self.assertRaises(CertificateError):
            check_positive(doc, crossed)
        self.assertTrue(check_negative(doc, []))

    def test_false_manifest_rejected_even_with_real_cut_elsewhere(self):
        doc = dict(sources=["s1", "s2"], targets=["t1", "t2"],
                   permitted=[["s1", "t1"], ["s1", "t2"], ["s2", "t1"], ["s2", "t2"]],
                   original=[["s1", "t1"], ["s2", "t2"]],
                   admissible=[["s1", "t1"], ["s2", "t2"]])
        forbidden = sorted(set(map(tuple, doc["permitted"])) -
                           set(map(tuple, doc["admissible"])))
        self.assertTrue(all(find_certificate(doc, edge) is None for edge in forbidden))
        with self.assertRaises(CertificateError):
            check_negative(doc, [
                dict(edge=list(edge), reason="cut", X=[], Y=[])
                for edge in forbidden
            ])


if __name__ == "__main__":
    unittest.main()
