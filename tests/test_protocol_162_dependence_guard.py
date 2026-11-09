"""Protocol 162: explicit dependence guard for paired inference.

Fixture-level contract only. No model inference, training, or downloads.
Run solely in verified zero-cost cloud CI.
"""
import unittest
from tests.test_protocol_159_paired_discordance_contract import paired_oracle


def paired_report_with_groups(a, b, groups):
    """Report paired outcomes; suppress independent-pair p when groups repeat.

    groups maps every original-problem ID to a stable independent sampling-unit ID.
    Unique groups are a necessary but not sufficient independence assumption.
    """
    if not isinstance(groups, dict) or set(groups) != set(a):
        raise ValueError("group manifest must match original-problem IDs")
    for group in groups.values():
        if type(group) not in (str, int) or group == "":
            raise ValueError("group IDs must be nonempty strings or integers")
    result = paired_oracle(a, b)
    unique = len(set(groups.values()))
    result["n_independent_units_declared"] = unique
    result["independence_assumption_verified"] = False
    result["p_independent_pairs"] = (
        result["p_independent_pairs"] if unique == result["n"] else None
    )
    result["p_suppression_reason"] = (
        None if unique == result["n"] else "repeated sampling-unit IDs"
    )
    return result


class DependenceGuard(unittest.TestCase):
    def test_repeated_paraphrases_suppress_p_but_keep_effect(self):
        a = {"a1": (True, True), "a2": (True, True),
             "b1": (True, False), "b2": (True, False)}
        b = {"a1": (True, False), "a2": (True, False),
             "b1": (True, True), "b2": (True, True)}
        r = paired_report_with_groups(a, b, {"a1": "a", "a2": "a",
                                               "b1": "b", "b2": "b"})
        self.assertIsNone(r["p_independent_pairs"])
        self.assertEqual(r["n_independent_units_declared"], 2)
        self.assertEqual(r["delta_yield"], 0)
        self.assertEqual(r["n10"], 2)

    def test_unique_units_preserve_conditional_p(self):
        a = {i: (True, True) for i in range(6)}
        b = {i: (True, False) for i in range(6)}
        r = paired_report_with_groups(a, b, {i: i for i in range(6)})
        self.assertAlmostEqual(r["p_independent_pairs"], 0.03125, places=12)
        self.assertFalse(r["independence_assumption_verified"])

    def test_reject_missing_group(self):
        with self.assertRaises(ValueError):
            paired_report_with_groups({"a": (True, True)},
                                      {"a": (True, False)}, {})

    def test_reject_invalid_group(self):
        for group in ("", None, True, []):
            with self.subTest(group=group), self.assertRaises(ValueError):
                paired_report_with_groups({"a": (True, True)},
                                          {"a": (True, False)}, {"a": group})


if __name__ == "__main__":
    unittest.main()
