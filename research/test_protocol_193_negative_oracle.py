"""Protocol 193: independent exhaustive oracle for negative certificates.

Specification only: execution must occur on verified zero-cost cloud CI.
For all 2x2 simple permitted graphs and all admissible supersets of each
original, independently enumerate feasible fixed-margin assignments.
For ineligible cases, search all source/target cuts for each forbidden edge.
For eligible cases, confirm no complete valid negative manifest is accepted.
"""
import itertools
import unittest

from protocol_191_certificate_checker import CertificateError, check_negative
from test_protocol_192_exhaustive_oracle import enumerate_feasible


def find_certificate(doc, edge):
    source, target = edge
    original = [tuple(e) for e in doc["original"]]
    ds = sum(s == source for s, _ in original)
    dt = sum(t == target for _, t in original)
    if ds == 0 or dt == 0:
        return {"edge": list(edge), "reason": "zero_degree"}
    permitted = set(map(tuple, doc["permitted"]))
    for mask_s in range(1 << len(doc["sources"])):
        x = [v for i, v in enumerate(doc["sources"]) if mask_s & (1 << i)]
        for mask_t in range(1 << len(doc["targets"])):
            y = [v for i, v in enumerate(doc["targets"]) if mask_t & (1 << i)]
            residual_s = {v: sum(a == v for a, _ in original) - (v == source)
                          for v in doc["sources"]}
            residual_t = {v: sum(b == v for _, b in original) - (v == target)
                          for v in doc["targets"]}
            capacity = (sum(residual_s[v] for v in doc["sources"] if v not in x)
                        + sum(a in x and b not in y for a, b in permitted - {edge})
                        + sum(residual_t[v] for v in y))
            if capacity < len(original) - 1:
                return {"edge": list(edge), "reason": "cut", "X": x, "Y": y}
    return None


class Protocol193NegativeOracle(unittest.TestCase):
    def test_complete_two_by_two_universe(self):
        sources, targets = ["s1", "s2"], ["t1", "t2"]
        universe = [[s, t] for s in sources for t in targets]
        eligible_count = ineligible_count = 0
        for permitted_mask in range(1 << 4):
            permitted = [e for i, e in enumerate(universe) if permitted_mask & (1 << i)]
            for original_mask in range(1 << len(permitted)):
                original = [e for i, e in enumerate(permitted) if original_mask & (1 << i)]
                doc = dict(sources=sources, targets=targets, permitted=permitted,
                           admissible=permitted, original=original)
                feasible = list(enumerate_feasible(doc))
                for admissible_mask in range(1 << len(permitted)):
                    admissible = [e for i, e in enumerate(permitted)
                                  if admissible_mask & (1 << i)]
                    if not set(map(tuple, original)) <= set(map(tuple, admissible)):
                        continue
                    doc["admissible"] = admissible
                    forbidden = sorted(set(map(tuple, permitted)) - set(map(tuple, admissible)))
                    eligible = any(set(map(tuple, graph)) & set(forbidden) for graph in feasible)
                    certificates = [find_certificate(doc, edge) for edge in forbidden]
                    if eligible:
                        eligible_count += 1
                        self.assertIn(None, certificates)
                    else:
                        ineligible_count += 1
                        self.assertNotIn(None, certificates)
                        self.assertTrue(check_negative(doc, certificates))
        self.assertGreater(eligible_count, 0)
        self.assertGreater(ineligible_count, 0)


if __name__ == "__main__":
    unittest.main()
