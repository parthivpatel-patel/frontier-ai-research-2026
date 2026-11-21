"""Paired selective-risk decomposition and family-cluster sensitivity checks.

Pure Python standard-library code. Synthetic unit tests are NOT model evidence.
This module deliberately does not produce confirmatory p-values or CIs.
"""
import math
import unittest
from collections import defaultdict


def paired_disagreement(rows, a="temporal", b="baseline"):
    """At identical held-out item sets and equal accepted counts, decompose risk.

    Returns the exact error-rate difference (a minus b), based only on
    discordantly accepted items. This is descriptive, not causal attribution.
    """
    if not rows:
        raise ValueError("empty paired evaluation")
    if not isinstance(a, str) or not isinstance(b, str) or not a or not b or a == b:
        raise ValueError("two distinct verifier decision columns required")
    seen = set()
    n_a = n_b = 0
    only_a_errors = only_b_errors = 0
    only_a = only_b = 0
    family = defaultdict(int)
    for r in rows:
        item = r.get("item_id")
        if not isinstance(item, str) or not item or item in seen:
            raise ValueError("missing or duplicate item_id")
        seen.add(item)
        if r.get("split") != "heldout" or r.get("correctness") not in ("correct", "incorrect"):
            raise ValueError("held-out independent correctness required")
        if not isinstance(r.get("problem_family_id"), str) or not r["problem_family_id"]:
            raise ValueError("valid problem_family_id required")
        x, y = r.get(a), r.get(b)
        if type(x) is not bool or type(y) is not bool:
            raise ValueError("paired acceptance decisions must be boolean")
        n_a += x
        n_b += y
        if x and not y:
            only_a += 1
            only_a_errors += r["correctness"] == "incorrect"
            family[r["problem_family_id"]] += 1
        elif y and not x:
            only_b += 1
            only_b_errors += r["correctness"] == "incorrect"
            family[r["problem_family_id"]] += 1
    if n_a != n_b:
        raise ValueError("equal acceptance coverage required for exact identity")
    return {
        "n": len(rows),
        "accepted_each": n_a,
        "only_a": only_a,
        "only_b": only_b,
        "discordant_families": len(family),
        "risk_difference": ((only_a_errors - only_b_errors) / n_a if n_a else None),
        "only_a_errors": only_a_errors,
        "only_b_errors": only_b_errors,
    }


def family_leave_one_out(rows, a="temporal", b="baseline"):
    """Descriptive sensitivity only: recompute after dropping each source family.

    Dropping a family may break equal coverage; such subsets are reported as
    non-comparable, rather than silently recalibrating thresholds on held-out.
    """
    paired_disagreement(rows, a, b)
    families = sorted({r["problem_family_id"] for r in rows})
    out = {}
    for family in families:
        subset = [r for r in rows if r["problem_family_id"] != family]
        if not subset:
            out[family] = {"status": "empty", "risk_difference": None}
            continue
        try:
            d = paired_disagreement(subset, a, b)
            out[family] = {"status": "comparable", "risk_difference": d["risk_difference"]}
        except ValueError as exc:
            if "equal acceptance coverage" not in str(exc):
                raise
            out[family] = {"status": "unequal_coverage", "risk_difference": None}
    return out


class PairedDisagreementTests(unittest.TestCase):
    def row(self, item, family, correct, temporal, baseline):
        return dict(item_id=item, problem_family_id=family, split="heldout",
                    correctness=correct, temporal=temporal, baseline=baseline)

    def test_exact_discordance_identity(self):
        rows = [self.row("1", "f1", "incorrect", True, False),
                self.row("2", "f2", "correct", False, True),
                self.row("3", "f3", "incorrect", True, True)]
        result = paired_disagreement(rows)
        self.assertEqual(result["accepted_each"], 2)
        self.assertEqual(result["risk_difference"], 0.5)
        self.assertEqual((result["only_a"], result["only_b"]), (1, 1))

    def test_common_accepted_errors_cancel(self):
        rows = [self.row("1", "f1", "incorrect", True, True),
                self.row("2", "f2", "correct", False, False)]
        self.assertEqual(paired_disagreement(rows)["risk_difference"], 0.0)

    def test_zero_coverage_undefined(self):
        self.assertIsNone(paired_disagreement([self.row("1", "f1", "correct", False, False)])["risk_difference"])

    def test_reject_unequal_coverage(self):
        with self.assertRaisesRegex(ValueError, "equal acceptance"):
            paired_disagreement([self.row("1", "f1", "correct", True, False)])

    def test_reject_duplicate_id(self):
        row = self.row("1", "f1", "correct", True, True)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            paired_disagreement([row, row])

    def test_reject_integer_decision(self):
        with self.assertRaisesRegex(ValueError, "boolean"):
            paired_disagreement([self.row("1", "f1", "correct", 1, True)])

    def test_reject_same_verifier_column(self):
        with self.assertRaisesRegex(ValueError, "distinct verifier"):
            paired_disagreement([self.row("1", "f1", "correct", True, False)], a="temporal", b="temporal")

    def test_reject_mixed_family_types_with_value_error(self):
        rows = [self.row("1", "f1", "correct", True, True),
                self.row("2", 3, "correct", True, True)]
        with self.assertRaisesRegex(ValueError, "problem_family_id"):
            family_leave_one_out(rows)

    def test_leave_one_family_out_unequal_coverage(self):
        rows = [self.row("1", "f1", "incorrect", True, False),
                self.row("2", "f2", "correct", False, True)]
        out = family_leave_one_out(rows)
        self.assertEqual(out["f1"]["status"], "unequal_coverage")
        self.assertEqual(out["f2"]["status"], "unequal_coverage")

    def test_leave_one_family_out_comparable(self):
        rows = [self.row("1", "f1", "incorrect", True, False),
                self.row("2", "f1", "correct", False, True),
                self.row("3", "f2", "correct", True, True)]
        self.assertEqual(family_leave_one_out(rows)["f2"]["status"], "comparable")


if __name__ == "__main__":
    unittest.main()
