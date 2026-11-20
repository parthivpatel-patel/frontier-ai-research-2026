"""Executable, standard-library-only checks for the paired evaluation contract.

Run on an eligible free cloud CI runner: python -m unittest tests.test_paired_contract_guardrails
No model inference, data download, or empirical result is produced.
"""
import unittest
from collections import defaultdict

POLICIES = frozenset(("C", "T", "S", "B"))
DOMAINS = frozenset(("NLP", "mathematics", "physics"))
SPLITS = frozenset(("train", "calibration", "heldout"))
LABELS = frozenset(("correct", "incorrect", "unresolved"))


def validate(rows):
    """Return all structural errors; fail closed on incomplete provenance."""
    errors = []
    seen = set()
    families = defaultdict(set)
    sources = defaultdict(set)
    answers = defaultdict(set)
    by_item = defaultdict(dict)
    for j, r in enumerate(rows):
        required = ("item_id", "problem_family_id", "source_id", "domain",
                    "split", "candidate_answer_hash", "policy_id",
                    "policy_version", "accept", "correctness",
                    "cost_usd", "input_tokens", "output_tokens",
                    "verifier_calls", "feature_available_at_decision",
                    "decision_time", "adjudication_blinded_to_policy")
        missing = [k for k in required if k not in r or r[k] is None]
        if missing:
            errors.append((j, "missing: " + ",".join(missing)))
            continue
        key = (r["item_id"], r["policy_id"])
        if key in seen:
            errors.append((j, "duplicate item-policy decision"))
        seen.add(key)
        if r["policy_id"] not in POLICIES or r["domain"] not in DOMAINS or r["split"] not in SPLITS:
            errors.append((j, "unknown policy/domain/split"))
        if r["correctness"] not in LABELS or type(r["accept"]) is not bool:
            errors.append((j, "invalid label/accept"))
        if r["adjudication_blinded_to_policy"] is not True:
            errors.append((j, "adjudication not blinded"))
        if r["feature_available_at_decision"] > r["decision_time"]:
            errors.append((j, "temporal look-ahead"))
        for k in ("cost_usd", "input_tokens", "output_tokens", "verifier_calls"):
            v = r[k]
            if type(v) not in (int, float) or v < 0 or (k == "cost_usd" and v != 0):
                errors.append((j, "invalid budget: " + k))
        families[r["problem_family_id"]].add(r["split"])
        sources[r["source_id"]].add(r["split"])
        answers[r["candidate_answer_hash"]].add(r["split"])
        previous = by_item[r["item_id"]]
        if previous:
            for k in ("domain", "split", "candidate_answer_hash", "correctness", "problem_family_id"):
                if r[k] != previous[k]:
                    errors.append((j, "inconsistent shared item: " + k))
        else:
            by_item[r["item_id"]] = r
    for label, mapping in (("family", families), ("source", sources), ("answer", answers)):
        for key, splits in mapping.items():
            if len(splits) > 1:
                errors.append((label, "cross-split leakage: " + str(key)))
    return errors


def paired_selective_error_difference(rows, first="T", second="C"):
    """Exact difference only for fully adjudicated, identical, matched-coverage pools."""
    if validate(rows):
        raise ValueError("invalid evaluation contract")
    by_policy = {p: {} for p in (first, second)}
    for r in rows:
        if r["policy_id"] in by_policy:
            by_policy[r["policy_id"]][r["item_id"]] = r
    a, b = by_policy[first], by_policy[second]
    if not a or a.keys() != b.keys():
        raise ValueError("unpaired evaluation pool")
    if any(r["correctness"] == "unresolved" for r in a.values()):
        raise ValueError("unresolved correctness; no point estimate")
    ka = sum(r["accept"] for r in a.values())
    kb = sum(r["accept"] for r in b.values())
    if ka != kb or ka == 0:
        raise ValueError("coverage unmatched or zero")
    ea = sum(r["accept"] and r["correctness"] == "incorrect" for r in a.values())
    eb = sum(r["accept"] and r["correctness"] == "incorrect" for r in b.values())
    return (ea - eb) / ka


def fixture(item, policy, accept, correctness="correct", family=None):
    return dict(item_id=item, problem_family_id=family or item,
                source_id="src_" + item, domain="physics", split="heldout",
                candidate_answer_hash="hash_" + item, policy_id=policy,
                policy_version="frozen-v1", accept=accept,
                correctness=correctness, cost_usd=0, input_tokens=1,
                output_tokens=1, verifier_calls=1,
                feature_available_at_decision=1, decision_time=2,
                adjudication_blinded_to_policy=True)


class ContractTests(unittest.TestCase):
    def test_valid_paired_identity(self):
        rows = [fixture("a", "T", True, "incorrect"),
                fixture("a", "C", False, "incorrect"),
                fixture("b", "T", False),
                fixture("b", "C", True)]
        self.assertEqual(validate(rows), [])
        self.assertEqual(paired_selective_error_difference(rows), 1.0)

    def test_detect_source_leakage(self):
        a, b = fixture("a", "T", True), fixture("b", "C", True)
        b["source_id"] = a["source_id"]
        b["split"] = "train"
        self.assertTrue(any("leakage" in msg for _, msg in validate([a, b])))

    def test_detect_lookahead_and_paid_cost(self):
        r = fixture("a", "T", True)
        r["feature_available_at_decision"] = 3
        r["cost_usd"] = 0.01
        self.assertEqual(len(validate([r])), 2)

    def test_reject_unresolved(self):
        rows = [fixture("a", "T", True, "unresolved"),
                fixture("a", "C", True, "unresolved")]
        with self.assertRaisesRegex(ValueError, "unresolved"):
            paired_selective_error_difference(rows)

    def test_reject_unmatched_coverage(self):
        rows = [fixture("a", "T", True), fixture("a", "C", False)]
        with self.assertRaisesRegex(ValueError, "coverage"):
            paired_selective_error_difference(rows)

    def test_reject_missing_policy(self):
        with self.assertRaisesRegex(ValueError, "unpaired"):
            paired_selective_error_difference([fixture("a", "T", True)])

    def test_detect_duplicate_and_label_conflict(self):
        rows = [fixture("a", "T", True),
                fixture("a", "T", True, "incorrect")]
        messages = [msg for _, msg in validate(rows)]
        self.assertTrue(any("duplicate" in m for m in messages))
        self.assertTrue(any("inconsistent" in m for m in messages))


if __name__ == "__main__":
    unittest.main()
