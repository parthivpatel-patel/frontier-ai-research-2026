"""Claim-level consistency oracle for the synthetic Protocol 095 reversal.

All claims, labels and acceptance decisions here are synthetic. This is not
physics adjudication, model inference, or evidence of empirical performance.
Run: python -m unittest discover -s tests -p 'test_protocol_097_claim_level.py'
"""
from fractions import Fraction
import unittest

from test_protocol_096_simpson_fixture import compare_families


def aggregate_claims(claims):
    """Require one unique claim ID and one shared binary truth per claim."""
    if not isinstance(claims, (list, tuple)) or not claims:
        raise ValueError("nonempty claim records required")
    seen = set()
    counts = {}
    for record in claims:
        if not isinstance(record, dict) or set(record) != {
            "id", "family", "unsafe", "accept_a", "accept_b"
        }:
            raise ValueError("invalid claim record schema")
        cid, family = record["id"], record["family"]
        if type(cid) is not str or not cid or cid in seen:
            raise ValueError("duplicate or invalid claim ID")
        if type(family) is not str or not family:
            raise ValueError("invalid family")
        for key in ("unsafe", "accept_a", "accept_b"):
            if type(record[key]) is not bool:
                raise ValueError("truth and decisions must be booleans")
        seen.add(cid)
        if family not in counts:
            counts[family] = [0, 0, 0, 0, 0]
        row = counts[family]
        a, b, unsafe = record["accept_a"], record["accept_b"], record["unsafe"]
        for index, increment in enumerate((1, int(a), int(a and unsafe),
                                           int(b), int(b and unsafe))):
            row[index] += increment
    return {family: tuple(row) for family, row in counts.items()}


def synthetic_reversal_claims():
    """Disjoint acceptance sets within each family; shared truth per ID."""
    records = []
    for family in ("mechanics", "circuits"):
        for i in range(100):
            a = i < (90 if family == "mechanics" else 10)
            b = not a
            unsafe = (a and i < 9) or (
                b and family == "circuits" and i < 82
            )
            records.append({"id": f"{family}-{i:03d}", "family": family,
                            "unsafe": bool(unsafe),
                            "accept_a": a, "accept_b": b})
    return records


class Protocol097ClaimLevel(unittest.TestCase):
    def test_claim_level_reproduces_aggregate_reversal(self):
        rows = aggregate_claims(synthetic_reversal_claims())
        self.assertEqual(rows, {
            "mechanics": (100, 90, 9, 10, 0),
            "circuits": (100, 10, 9, 90, 72),
        })
        weights = {k: Fraction(1, 2) for k in rows}
        result = compare_families(rows, weights)
        self.assertEqual(result["pooled_difference"], Fraction(-27, 50))
        self.assertEqual(result["standardized_difference"], Fraction(1, 10))

    def test_duplicate_claim_rejected(self):
        records = synthetic_reversal_claims()
        with self.assertRaises(ValueError):
            aggregate_claims(records + [dict(records[0])])

    def test_conflicting_truth_same_id_rejected(self):
        records = synthetic_reversal_claims()
        altered = dict(records[0])
        altered["unsafe"] = not altered["unsafe"]
        with self.assertRaises(ValueError):
            aggregate_claims(records + [altered])

    def test_missing_truth_rejected(self):
        records = synthetic_reversal_claims()
        records[0] = {**records[0], "unsafe": None}
        with self.assertRaises(ValueError):
            aggregate_claims(records)

    def test_family_and_decision_types_rejected(self):
        records = synthetic_reversal_claims()
        records[0] = {**records[0], "accept_a": 1}
        with self.assertRaises(ValueError):
            aggregate_claims(records)

    def test_schema_rejected(self):
        records = synthetic_reversal_claims()
        del records[0]["family"]
        with self.assertRaises(ValueError):
            aggregate_claims(records)


if __name__ == "__main__":
    unittest.main()
