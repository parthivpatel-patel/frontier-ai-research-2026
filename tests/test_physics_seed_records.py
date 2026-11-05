"""Protocol 083: constructed physics controls, NOT independent adjudication.

Run on an eligible free cloud runner: python -m unittest discover -s tests -p 'test_physics_seed_records.py'
No dependencies, model calls, downloads, or laptop execution required.
"""
import hashlib
import json
import unittest
from decimal import Decimal

# Canonical decimal strings avoid binary floating point ambiguity.
# All candidate labels are *author-constructed*, not empirical ground truth.
RECORDS = (
    ("N1a", "N1", "newton", ("6", "2"), "3", "supported"),
    ("N1b", "N1", "newton", ("6", "2"), "4", "contradicted"),
    ("K1a", "K1", "kinematics", ("1", "2", "3"), "7", "supported"),
    ("K1b", "K1", "kinematics", ("1", "0", "3"), "7", "contradicted"),
    ("E1a", "E1", "kinetic_energy", ("4", "3"), "18", "supported"),
    ("E1b", "E1", "kinetic_energy", ("4", "6"), "18", "contradicted"),
    ("C1a", "C1", "ohmic_circuit", ("12", "4"), "3", "supported"),
    ("C1b", "C1", "ohmic_circuit", ("8", "4"), "3", "contradicted"),
)

def predicted_value(domain, parameters):
    p = tuple(map(Decimal, parameters))
    if domain == "newton":
        return p[0] / p[1]
    if domain == "kinematics":
        return p[0] + p[1] * p[2]
    if domain == "kinetic_energy":
        return p[0] * p[1] ** 2 / Decimal(2)
    if domain == "ohmic_circuit":
        return p[0] / p[1]
    raise ValueError("unknown physics domain")

def canonical_record(row):
    identifier, pair, domain, parameters, asserted, label = row
    record = {
        "record_id": identifier,
        "pair_id": pair,
        "domain": domain,
        "parameters_decimal_si": list(parameters),
        "asserted_decimal_si": asserted,
        "candidate_label": label,
        "adjudicated_label": None,
        "adjudicator_id": None,
        "source_reference": None,
        "status": "constructed_unadjudicated",
    }
    encoded = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return record, hashlib.sha256(encoded).hexdigest()

class PhysicsSeedControls(unittest.TestCase):
    def test_all_eight_candidates_match_independent_arithmetic(self):
        for row in RECORDS:
            with self.subTest(record=row[0]):
                computed = predicted_value(row[2], row[3])
                label = "supported" if computed == Decimal(row[4]) else "contradicted"
                self.assertEqual(label, row[5])

    def test_pair_balance_and_unique_identifiers(self):
        self.assertEqual(len({r[0] for r in RECORDS}), 8)
        for pair in ("N1", "K1", "E1", "C1"):
            self.assertEqual({r[5] for r in RECORDS if r[1] == pair},
                             {"supported", "contradicted"})

    def test_unadjudicated_records_cannot_become_ground_truth(self):
        for row in RECORDS:
            record, digest = canonical_record(row)
            self.assertIsNone(record["adjudicated_label"])
            self.assertIsNone(record["adjudicator_id"])
            self.assertEqual(record["status"], "constructed_unadjudicated")
            self.assertEqual(len(digest), 64)
            self.assertEqual(digest, canonical_record(row)[1])

    def test_hash_changes_with_claim(self):
        original = RECORDS[0]
        altered = original[:4] + ("4",) + original[5:]
        self.assertNotEqual(canonical_record(original)[1], canonical_record(altered)[1])

    def test_unknown_domain_rejected(self):
        with self.assertRaises(ValueError):
            predicted_value("unknown", ("1", "2"))

if __name__ == "__main__":
    unittest.main()
