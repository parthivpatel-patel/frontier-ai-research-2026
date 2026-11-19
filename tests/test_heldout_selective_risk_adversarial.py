"""Synthetic-only regression tests for input boundaries and selective-risk invariants.

These checks establish software behavior, not verifier accuracy or novelty.
"""
import unittest

from src.heldout_selective_risk_accounting import audit_fixed_decisions


def row(item, family, error, decisions):
    return {"item_id": item, "family_id": family, "error": error,
            "decisions": decisions}


class HeldoutAdversarialBoundaryTests(unittest.TestCase):
    def test_all_accepted_matches_empirical_error(self):
        rows = [row(str(i), "f" + str(i % 3), i % 4 == 0,
                    {"all": True, "none": False}) for i in range(12)]
        result = audit_fixed_decisions(rows, ("all", "none"))
        self.assertEqual(result["methods"]["all"]["accepted"], 12)
        self.assertEqual(result["methods"]["all"]["errors_accepted"], 3)
        self.assertEqual(result["methods"]["all"]["selective_risk"], 0.25)
        self.assertIsNone(result["methods"]["none"]["selective_risk"])

    def test_row_order_does_not_change_aggregate(self):
        rows = [row(str(i), "f" + str(i % 2), bool(i % 3),
                    {"a": bool(i % 2), "b": bool(i % 4)})
                for i in range(11)]
        self.assertEqual(audit_fixed_decisions(rows, ("a", "b")),
                         audit_fixed_decisions(list(reversed(rows)), ("a", "b")))

    def test_rejects_empty_and_duplicate_method_rosters(self):
        rows = [row("a", "f", False, {"a": True})]
        for methods in ((), ("a", "a"), ("",), (" ",), ["a"]):
            with self.subTest(methods=methods), self.assertRaises(ValueError):
                audit_fixed_decisions(rows, methods)

    def test_rejects_invalid_rosters_and_schemas(self):
        valid = row("a", "f", False, {"a": True})
        for rows in ([], [None], [dict(valid, extra=1)],
                     [dict(valid, item_id="")], [dict(valid, error=None)],
                     [dict(valid, decisions={"a": None})]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                audit_fixed_decisions(rows, ("a",))

    def test_rejects_duplicate_ids_even_across_families(self):
        rows = [row("same", "f1", False, {"a": True}),
                row("same", "f2", True, {"a": False})]
        with self.assertRaises(ValueError):
            audit_fixed_decisions(rows, ("a",))

    def test_invariance_to_method_order(self):
        rows = [row("x", "f1", True, {"a": True, "b": False}),
                row("y", "f2", False, {"a": False, "b": True})]
        a = audit_fixed_decisions(rows, ("a", "b"))
        b = audit_fixed_decisions(rows, ("b", "a"))
        self.assertEqual(a["methods"], b["methods"])


if __name__ == "__main__":
    unittest.main()
