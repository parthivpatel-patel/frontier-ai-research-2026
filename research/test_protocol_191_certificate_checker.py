"""Adversarial unit tests for Protocol 191 certificate checker.

Standard library only. These tests are committed as specifications until
executed on independently verified zero-cost cloud infrastructure.
Run from repository root:
python -m unittest discover -s research -p 'test_protocol_191*.py' -v
"""
import unittest

from protocol_191_certificate_checker import (
    CertificateError, check_negative, check_positive,
)


def document():
    return {
        "sources": ["s1", "s2"],
        "targets": ["t1", "t2"],
        "permitted": [["s1", "t1"], ["s1", "t2"], ["s2", "t1"], ["s2", "t2"]],
        "admissible": [["s1", "t1"], ["s2", "t2"]],
        "original": [["s1", "t1"], ["s2", "t2"]],
    }


class Protocol191Certificates(unittest.TestCase):
    def reject_positive(self, d, candidate):
        with self.assertRaises(CertificateError):
            check_positive(d, candidate)

    def reject_negative(self, d, manifest):
        with self.assertRaises(CertificateError):
            check_negative(d, manifest)

    def test_positive_crossed_matching(self):
        self.assertTrue(check_positive(document(), [["s1", "t2"], ["s2", "t1"]]))

    def test_positive_duplicate_edge(self):
        self.reject_positive(document(), [["s1", "t2"], ["s1", "t2"]])

    def test_positive_changed_margin(self):
        self.reject_positive(document(), [["s1", "t1"], ["s1", "t2"]])

    def test_positive_original_is_not_corruption(self):
        self.reject_positive(document(), document()["original"])

    def test_original_must_be_admissible(self):
        d = document()
        d["admissible"] = [["s1", "t1"]]
        self.reject_positive(d, [["s1", "t2"], ["s2", "t1"]])

    def test_empty_forbidden_universe(self):
        d = document()
        d["admissible"] = d["permitted"][:]
        self.assertTrue(check_negative(d, []))

    def test_zero_degree_forced_edge(self):
        d = {
            "sources": ["s1", "s2"], "targets": ["t1", "t2"],
            "permitted": [["s1", "t1"], ["s2", "t2"]],
            "admissible": [["s1", "t1"]],
            "original": [["s1", "t1"]],
        }
        self.assertTrue(check_negative(d, [
            {"edge": ["s2", "t2"], "reason": "zero_degree"}
        ]))

    def test_forged_zero_degree(self):
        self.reject_negative(document(), [
            {"edge": ["s1", "t2"], "reason": "zero_degree"},
            {"edge": ["s2", "t1"], "reason": "zero_degree"},
        ])

    def test_missing_manifest(self):
        self.reject_negative(document(), [])

    def test_unsupported_certificate(self):
        self.reject_negative(document(), [
            {"edge": ["s1", "t2"], "reason": "unknown_solver"},
            {"edge": ["s2", "t1"], "reason": "unknown_solver"},
        ])

    def test_fake_cut_with_no_deficiency(self):
        self.reject_negative(document(), [
            {"edge": ["s1", "t2"], "reason": "cut", "X": [], "Y": []},
            {"edge": ["s2", "t1"], "reason": "cut", "X": [], "Y": []},
        ])

    def test_wrong_stratum_in_cut(self):
        self.reject_negative(document(), [
            {"edge": ["s1", "t2"], "reason": "cut", "X": ["t1"], "Y": []},
            {"edge": ["s2", "t1"], "reason": "cut", "X": [], "Y": []},
        ])

    def test_genuine_deficient_cut(self):
        d = {
            "sources": ["s1", "s2"], "targets": ["t1", "t2"],
            "permitted": [["s1", "t1"], ["s1", "t2"], ["s2", "t2"]],
            "admissible": [["s1", "t1"], ["s2", "t2"]],
            "original": [["s1", "t1"], ["s2", "t2"]],
        }
        # Force s1->t2: residual s2->t2 has demand at t1 but no edge to t1.
        # Cut X={s2}, Y={t2}: capacity=0, required=1.
        self.assertTrue(check_negative(d, [
            {"edge": ["s1", "t2"], "reason": "cut", "X": ["s2"], "Y": ["t2"]}
        ]))

    def test_empty_original_with_forbidden_edges(self):
        d = {
            "sources": ["s1"], "targets": ["t1"],
            "permitted": [["s1", "t1"]], "admissible": [], "original": [],
        }
        self.assertTrue(check_negative(d, [
            {"edge": ["s1", "t1"], "reason": "zero_degree"}
        ]))


if __name__ == "__main__":
    unittest.main()
