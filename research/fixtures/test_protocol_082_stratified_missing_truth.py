"""Protocol 082: exact stratified missing-truth bounds (synthetic only).

Dependency-free unittest fixture. No model evaluation, no empirical claim.
Run on an independently verified zero-cost standard public GitHub runner.
"""
import itertools
import unittest
from fractions import Fraction

DOMAINS = ("nlp", "mathematics", "physics")


def bounds(records):
    """Return sharp released-claim census bounds and domain-specific bounds.

    Each record: {id: nonempty str, domain: one of DOMAINS,
                  released: exact bool, false: exact bool or None,
                  family: nonempty str}.
    None means unresolved; false=True means adjudicated false.
    """
    if not isinstance(records, (list, tuple)):
        raise ValueError("records must be a sequence")
    seen = set()
    counts = {d: [0, 0, 0] for d in DOMAINS}  # K,F,U
    for r in records:
        if not isinstance(r, dict) or set(r) != {"id", "domain", "released", "false", "family"}:
            raise ValueError("invalid record structure")
        if not isinstance(r["id"], str) or not r["id"].strip() or r["id"] in seen:
            raise ValueError("invalid or duplicate claim id")
        seen.add(r["id"])
        if r["domain"] not in DOMAINS:
            raise ValueError("invalid domain")
        if not isinstance(r["family"], str) or not r["family"].strip():
            raise ValueError("invalid provenance family")
        if type(r["released"]) is not bool:
            raise ValueError("released must be boolean")
        if r["false"] is not None and type(r["false"]) is not bool:
            raise ValueError("false must be boolean or unresolved")
        if not r["released"]:
            continue
        c = counts[r["domain"]]
        c[0] += 1
        if r["false"] is None:
            c[2] += 1
        elif r["false"]:
            c[1] += 1
    k = sum(c[0] for c in counts.values())
    if not k:
        raise ValueError("no released claims")
    f = sum(c[1] for c in counts.values())
    u = sum(c[2] for c in counts.values())
    domain_bounds = {
        d: None if c[0] == 0 else (Fraction(c[1], c[0]), Fraction(c[1] + c[2], c[0]))
        for d, c in counts.items()
    }
    return (Fraction(f, k), Fraction(f + u, k)), domain_bounds


def rec(identifier, domain, false, released=True, family="source-1"):
    return {"id": identifier, "domain": domain, "released": released,
            "false": false, "family": family}


class Protocol082Tests(unittest.TestCase):
    def setUp(self):
        self.witness = [
            rec("n1", "nlp", True), rec("n2", "nlp", False),
            rec("m1", "mathematics", None), rec("m2", "mathematics", None),
            rec("p1", "physics", True), rec("p2", "physics", None),
        ]

    def test_exact_witness(self):
        pooled, domains = bounds(self.witness)
        self.assertEqual(pooled, (Fraction(1, 3), Fraction(5, 6)))
        self.assertEqual(domains["nlp"], (Fraction(1, 2), Fraction(1, 2)))
        self.assertEqual(domains["mathematics"], (Fraction(0), Fraction(1)))
        self.assertEqual(domains["physics"], (Fraction(1, 2), Fraction(1)))

    def test_all_eight_completions_and_sharpness(self):
        outcomes = []
        for bits in itertools.product((False, True), repeat=3):
            completed = [dict(r) for r in self.witness]
            unresolved = [r for r in completed if r["false"] is None]
            for r, bit in zip(unresolved, bits):
                r["false"] = bit
            outcomes.append(bounds(completed)[0][0])
        self.assertEqual(len(outcomes), 8)
        self.assertEqual(min(outcomes), Fraction(1, 3))
        self.assertEqual(max(outcomes), Fraction(5, 6))

    def test_partition_invariance(self):
        original = bounds(self.witness)[0]
        for assignments in itertools.product(DOMAINS, repeat=len(self.witness)):
            changed = [dict(r, domain=d) for r, d in zip(self.witness, assignments)]
            self.assertEqual(bounds(changed)[0], original)

    def test_unresolved_can_increase_width(self):
        old = bounds([rec("a", "nlp", False)])[0]
        new = bounds([rec("a", "nlp", False), rec("b", "physics", None)])[0]
        self.assertGreater(new[1] - new[0], old[1] - old[0])

    def test_empty_domain_is_undefined(self):
        self.assertIsNone(bounds([rec("a", "nlp", True)])[1]["physics"])

    def test_unreleased_excluded(self):
        self.assertEqual(bounds([rec("a", "nlp", True), rec("b", "physics", None, False)])[0],
                         (Fraction(1), Fraction(1)))

    def test_invalid_records_rejected(self):
        invalid = [
            [rec("a", "nlp", True), rec("a", "physics", None)],
            [rec("a", "unknown", None)],
            [rec("a", "nlp", 1)],
            [rec("a", "nlp", None, released=1)],
            [rec("a", "nlp", None, family="")],
            [rec("", "nlp", None)],
            [rec("a", "nlp", False, released=False)],
            [{"id": "a", "domain": "nlp"}],
        ]
        for case in invalid:
            with self.subTest(case=case), self.assertRaises(ValueError):
                bounds(case)

    def test_provenance_grouping_does_not_change_claim_bounds(self):
        alternative = [dict(r, family="shared") for r in self.witness]
        self.assertEqual(bounds(alternative)[0], bounds(self.witness)[0])
        # This is not a variance test; dependence affects inference, not census counts.


if __name__ == "__main__":
    unittest.main()
