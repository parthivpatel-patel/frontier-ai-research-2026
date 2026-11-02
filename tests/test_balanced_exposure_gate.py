"""Protocol 020 equal-exposure gate: all examples are synthetic."""
import math
import unittest

from src.balanced_exposure_gate import (
    any_failure_probability, balanced_exposure_audit,
)
from src.paired_unsafe_acceptance import paired_unsafe_acceptance_audit


def record(method, source, trial, accepted=True, incorrect=False):
    return {"method_id": method, "source_id": source, "trial_id": trial,
            "accepted": accepted, "incorrect": incorrect if accepted else None}


def fixture():
    return [record(m, s, t, incorrect=(t == "r2"))
            for s in ("s1", "s2") for m in ("A", "B")
            for t in ("r1", "r2")]


def audit(rows, sources=("s1", "s2"), trials=("r1", "r2"), **kw):
    return balanced_exposure_audit(
        rows, method_ids=("A", "B"), source_ids=sources,
        trial_ids=trials, min_coverage=kw.get("min_coverage", .5),
        max_coverage_gap=kw.get("max_coverage_gap", .1),
    )


class AnyFailureProbabilityTests(unittest.TestCase):
    def test_one_and_five_trials(self):
        self.assertAlmostEqual(any_failure_probability(.1, 1), .1)
        self.assertAlmostEqual(any_failure_probability(.1, 5), .40951)

    def test_boundaries_and_monotonicity(self):
        self.assertEqual(any_failure_probability(0, 100), 0)
        self.assertEqual(any_failure_probability(1, 100), 1)
        self.assertLess(any_failure_probability(.2, 1),
                        any_failure_probability(.2, 5))

    def test_reject_invalid_probability_and_trial_budget(self):
        for p in (-.1, 1.1, math.nan, math.inf, True, "0.2"):
            with self.assertRaises(ValueError):
                any_failure_probability(p, 2)
        for k in (0, -1, 1.5, True, 10001):
            with self.assertRaises(ValueError):
                any_failure_probability(.2, k)


class BalancedExposureTests(unittest.TestCase):
    def test_complete_balanced_roster(self):
        result = audit(fixture())
        self.assertTrue(result["equal_exposure_roster_verified"])
        self.assertEqual(result["total_recorded_attempts"], 8)
        self.assertEqual(result["n_eligible_sources"], 2)
        self.assertEqual(result["trial_budget_per_source_per_method"], 2)
        self.assertEqual(result["source_level_paired_audit"]["paired_table"]["both_unsafe"], 2)
        self.assertEqual(result["source_level_paired_audit"]["exact_mcnemar"]["two_sided_p"], 1)

    def test_attempt_and_source_denominators_are_distinct(self):
        result = audit(fixture())
        a = result["per_method_attempt_counts"]["A"]
        self.assertEqual(a["accepted_attempts"], 4)
        self.assertEqual(a["unsafe_accepted_attempts"], 2)
        self.assertEqual(a["conditional_attempt_failure_fraction"], .5)
        self.assertEqual(result["source_level_paired_audit"]["methods"]["A"]["unsafe_acceptance_per_eligible"], 1)

    def test_unbalanced_exposure_is_rejected(self):
        rows = [r for r in fixture()
                if not (r["method_id"] == "B" and r["trial_id"] == "r2")]
        with self.assertRaisesRegex(ValueError, "incomplete"):
            audit(rows)

    def test_unbalanced_exposure_can_fake_source_difference_in_legacy_audit(self):
        rows = [record("A", "s1", "r1"), record("A", "s1", "r2", incorrect=True),
                record("B", "s1", "r1")]
        old = paired_unsafe_acceptance_audit(
            [{k: v for k, v in r.items() if k != "trial_id"} for r in rows],
            method_ids=("A", "B"), min_coverage=1, max_coverage_gap=0)
        self.assertEqual(old["paired_table"]["A_only_unsafe"], 1)
        with self.assertRaisesRegex(ValueError, "incomplete"):
            audit(rows, sources=("s1",))

    def test_duplicate_slot_rejected_even_if_count_matches(self):
        rows = fixture()
        rows[-1] = dict(rows[0])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            audit(rows)

    def test_unknown_source_and_trial_rejected(self):
        for field, value in (("source_id", "unknown"), ("trial_id", "r3"),
                             ("method_id", "C")):
            rows = fixture()
            rows[0] = {**rows[0], field: value}
            with self.assertRaisesRegex(ValueError, "outside"):
                audit(rows)

    def test_wrong_rosters_rejected(self):
        for sources, trials in ((("s1",), ("r1", "r2")),
                                (("s1", "s2"), ("r1",)),
                                (("s1", "s2"), ("r1", "r2", "r3"))):
            with self.assertRaises(ValueError):
                audit(fixture(), sources=sources, trials=trials)

    def test_invalid_roster_ids_rejected(self):
        for sources in ((), ("s1", "s1"), ("s1", " "), ["s1", "s2"]):
            with self.assertRaises(ValueError):
                audit(fixture(), sources=sources)
        for trials in ((), ("r1", "r1"), ("r1", " "), tuple(map(str, range(33)))):
            with self.assertRaises(ValueError):
                audit(fixture(), trials=trials)

    def test_invalid_method_roster_rejected(self):
        for ids in (("A",), ("A", "A"), ["A", "B"], ("A", "B", "C")):
            with self.assertRaises(ValueError):
                balanced_exposure_audit(
                    fixture(), method_ids=ids, source_ids=("s1", "s2"),
                    trial_ids=("r1", "r2"), min_coverage=.5,
                    max_coverage_gap=.1)

    def test_missing_correctness_label_rejected(self):
        rows = fixture()
        rows[0] = {**rows[0], "incorrect": None}
        with self.assertRaisesRegex(ValueError, "adjudicated"):
            audit(rows)

    def test_abstention_requires_null_label(self):
        rows = fixture()
        rows[0] = {**rows[0], "accepted": False, "incorrect": False}
        with self.assertRaisesRegex(ValueError, "abstained"):
            audit(rows)

    def test_invalid_schema_and_flags_rejected(self):
        for field, value in (("accepted", 1), ("incorrect", "false")):
            rows = fixture()
            rows[0] = {**rows[0], field: value}
            with self.assertRaises(ValueError):
                audit(rows)
        rows = fixture()
        rows[0] = {**rows[0], "extra": 1}
        with self.assertRaisesRegex(ValueError, "schema"):
            audit(rows)

    def test_abstain_all_coverage_gate_fails(self):
        rows = [record(m, s, t, accepted=(m == "A"))
                for m in ("A", "B") for s in ("s1", "s2")
                for t in ("r1", "r2")]
        result = audit(rows)
        self.assertFalse(result["source_level_paired_audit"]["descriptive_coverage_gate_passed"])
        self.assertIsNone(result["per_method_attempt_counts"]["B"]["conditional_attempt_failure_fraction"])

    def test_swap_methods_changes_difference_sign(self):
        rows = fixture()
        rows[0] = {**rows[0], "incorrect": False}
        x = audit(rows)
        y = audit([{**r, "method_id": "B" if r["method_id"] == "A" else "A"}
                   for r in rows])
        self.assertEqual(
            x["source_level_paired_audit"]["difference_unsafe_acceptance_A_minus_B"],
            -y["source_level_paired_audit"]["difference_unsafe_acceptance_A_minus_B"])
        self.assertEqual(
            x["source_level_paired_audit"]["exact_mcnemar"]["two_sided_p"],
            y["source_level_paired_audit"]["exact_mcnemar"]["two_sided_p"])

    def test_empty_and_extra_rows_rejected(self):
        with self.assertRaises(ValueError):
            audit([])
        with self.assertRaisesRegex(ValueError, "extra"):
            audit(fixture() + [fixture()[0]])

    def test_disclaimers_preserved(self):
        result = audit(fixture())
        self.assertEqual(result["data_provenance"], "caller_supplied_unverified")
        self.assertIn("not prove identical generation", result["limits"])
        self.assertEqual(result["source_level_paired_audit"]["analysis"],
                         "paired_source_level_descriptive_only")


if __name__ == "__main__":
    unittest.main()
