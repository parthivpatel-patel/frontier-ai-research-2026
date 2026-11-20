"""Frozen-threshold cross-domain transfer: deterministic, descriptive checks only.

No empirical data, model calls, p-values, or confirmatory inference are produced.
Run with: python -m unittest tests.test_frozen_threshold_transfer
"""
import math
import unittest
from collections import defaultdict


def _finite_score(value):
    return type(value) in (int, float) and math.isfinite(value)


def freeze_threshold(calibration_rows, policy, target_coverage=0.5):
    """Select threshold from calibration only, with deterministic item-ID tie breaks.

    Returns (threshold, accepted_tie_ids). This permits exact calibration
    coverage but is not a deployable rule for unseen tied item IDs. For
    confirmatory deployment, use the conservative strict threshold instead.
    """
    if not 0 < target_coverage <= 1:
        raise ValueError("target coverage must lie in (0,1]")
    rows = [r for r in calibration_rows if r.get("policy_id") == policy]
    if not rows or any(r.get("split") != "calibration" for r in rows):
        raise ValueError("missing or non-calibration scores")
    if len({r.get("item_id") for r in rows}) != len(rows):
        raise ValueError("duplicate calibration items")
    if any(not _finite_score(r.get("score")) for r in rows):
        raise ValueError("invalid calibration score")
    ranked = sorted(rows, key=lambda r: (-r["score"], str(r["item_id"])))
    k = max(1, math.ceil(len(ranked) * target_coverage))
    cutoff = ranked[k - 1]["score"]
    tie_ids = frozenset(str(r["item_id"]) for r in ranked[:k] if r["score"] == cutoff)
    return cutoff, tie_ids


def frozen_decisions(heldout_rows, cutoff, tie_policy="reject"):
    """Apply frozen score cutoff; ties reject unless predeclared accept-all.

    Never use calibration item-ID tie selections on held-out items: that would
    imply a data-dependent or undeployable selection rule.
    """
    if not _finite_score(cutoff) or tie_policy not in ("reject", "accept"):
        raise ValueError("invalid frozen cutoff or tie policy")
    if any(r.get("split") != "heldout" or not _finite_score(r.get("score")) for r in heldout_rows):
        raise ValueError("held-out scores required")
    return {r["item_id"]: r["score"] > cutoff or
            (tie_policy == "accept" and r["score"] == cutoff)
            for r in heldout_rows}


def descriptive_domain_metrics(rows, decisions):
    """Return coverage/risk by domain; refuse unresolved correctness."""
    if not rows:
        raise ValueError("empty evaluation")
    groups = defaultdict(list)
    seen = set()
    for r in rows:
        item = r.get("item_id")
        if item in seen or item not in decisions:
            raise ValueError("duplicate or missing held-out decision")
        seen.add(item)
        if r.get("split") != "heldout" or r.get("correctness") not in ("correct", "incorrect"):
            raise ValueError("unresolved correctness or wrong split")
        if r.get("domain") not in ("NLP", "mathematics", "physics"):
            raise ValueError("unknown domain")
        groups[r["domain"]].append(r)
    if set(decisions) != seen:
        raise ValueError("extra held-out decisions")
    result = {}
    for domain, group in groups.items():
        accepted = [r for r in group if decisions[r["item_id"]]]
        result[domain] = {
            "n": len(group),
            "accepted": len(accepted),
            "coverage": len(accepted) / len(group),
            "selective_risk": (
                sum(r["correctness"] == "incorrect" for r in accepted) / len(accepted)
                if accepted else None
            ),
            "source_families": len({r["problem_family_id"] for r in group}),
        }
    return result


def assert_family_disjoint(calibration_rows, heldout_rows):
    """Reject source, problem-family and answer-hash leakage across splits."""
    for key in ("problem_family_id", "source_id", "candidate_answer_hash"):
        left = {r[key] for r in calibration_rows}
        right = {r[key] for r in heldout_rows}
        if left & right:
            raise ValueError("cross-split leakage: " + key)


class FrozenTransferTests(unittest.TestCase):
    def test_calibration_only_threshold(self):
        cal = [dict(item_id=str(i), policy_id="T", split="calibration", score=i)
               for i in range(4)]
        cutoff, ties = freeze_threshold(cal, "T")
        self.assertEqual(cutoff, 2)
        self.assertEqual(ties, frozenset(("2",)))

    def test_reject_heldout_in_calibration(self):
        with self.assertRaisesRegex(ValueError, "non-calibration"):
            freeze_threshold([dict(item_id="x", policy_id="T",
                                   split="heldout", score=0.9)], "T")

    def test_tie_policy_does_not_use_heldout_ids(self):
        held = [dict(item_id="unseen", split="heldout", score=0.5)]
        self.assertEqual(frozen_decisions(held, 0.5), {"unseen": False})
        self.assertEqual(frozen_decisions(held, 0.5, "accept"), {"unseen": True})

    def test_reject_nonfinite_scores(self):
        with self.assertRaisesRegex(ValueError, "invalid calibration score"):
            freeze_threshold([dict(item_id="a", policy_id="T",
                                   split="calibration", score=float("nan"))], "T")

    def test_zero_accepted_is_undefined_not_zero_risk(self):
        rows = [dict(item_id="a", split="heldout", domain="physics",
                     correctness="incorrect", problem_family_id="f1")]
        metric = descriptive_domain_metrics(rows, {"a": False})["physics"]
        self.assertEqual(metric["coverage"], 0)
        self.assertIsNone(metric["selective_risk"])

    def test_reject_unresolved_correctness(self):
        rows = [dict(item_id="a", split="heldout", domain="NLP",
                     correctness="unresolved", problem_family_id="f1")]
        with self.assertRaisesRegex(ValueError, "unresolved"):
            descriptive_domain_metrics(rows, {"a": True})

    def test_family_and_answer_leakage(self):
        base = dict(problem_family_id="f", source_id="s", candidate_answer_hash="h")
        with self.assertRaisesRegex(ValueError, "leakage"):
            assert_family_disjoint([base], [dict(base, source_id="s2")])

    def test_metrics_are_descriptive_only(self):
        rows = [dict(item_id="a", split="heldout", domain="mathematics",
                     correctness="incorrect", problem_family_id="f1"),
                dict(item_id="b", split="heldout", domain="mathematics",
                     correctness="correct", problem_family_id="f2")]
        m = descriptive_domain_metrics(rows, {"a": True, "b": False})["mathematics"]
        self.assertEqual((m["coverage"], m["selective_risk"], m["source_families"]),
                         (0.5, 1.0, 2))


if __name__ == "__main__":
    unittest.main()
