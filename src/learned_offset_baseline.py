"""Tiny supervised NLP sanity check with an external held-out template.

Training: 45 explicitly synthetic English examples (5 independently authored
templates x 9 offset labels). Test: only the strictly adjudicated five
mutations of ONE external source instruction, never used for training.

This is NOT an LLM, a physics experiment, a novel method, or a statistically
independent evaluation of five human instructions. It is a contamination-aware
engineering feasibility check for a real learned (multinomial NB) baseline.
"""
from __future__ import annotations

from collections import Counter
import csv
import json
import math
import re

from src.temporal_label_audit import (
    DATA, NUMBER, audit_snapshot, number_of_steps, verify_upstream_snapshot,
)

# Original synthetic training templates, not copied from the external dataset.
TRAIN_TEMPLATES = (
    "After {n} ticks, indicator b must activate following event a.",
    "If event a occurs, require event b {n} discrete intervals afterward.",
    "Following event a, ensure b holds exactly {n} time units later.",
    "When event a fires, b becomes active {n} ticks afterward.",
    "For each a event, the system requires b at offset {n}.",
)
TOKENS = re.compile(r"[a-z]+")
NUMBERS = frozenset(NUMBER)


def tokenize(text: str, mask_numbers: bool = False) -> list[str]:
    tokens = TOKENS.findall(text.lower())
    return ["__number__" if mask_numbers and token in NUMBERS else token
            for token in tokens]


def training_examples() -> list[tuple[str, int]]:
    return [(template.format(n=word), value)
            for template in TRAIN_TEMPLATES
            for word, value in NUMBER.items()]


class MultinomialNB:
    """Actual fitted count-based probabilistic classifier; stdlib only."""

    def __init__(self, mask_numbers: bool = False):
        self.mask_numbers = mask_numbers
        self.counts: dict[int, Counter[str]] = {}
        self.totals: dict[int, int] = {}
        self.priors: Counter[int] = Counter()
        self.vocab: set[str] = set()

    def fit(self, examples: list[tuple[str, int]]) -> "MultinomialNB":
        if not examples:
            raise ValueError("empty training set")
        self.counts = {}
        self.priors = Counter()
        self.vocab = set()
        for text, label in examples:
            if label not in NUMBER.values():
                raise ValueError("unsupported label")
            self.priors[label] += 1
            bag = Counter(tokenize(text, self.mask_numbers))
            self.counts.setdefault(label, Counter()).update(bag)
            self.vocab.update(bag)
        self.totals = {label: sum(bag.values())
                       for label, bag in self.counts.items()}
        return self

    def predict(self, text: str) -> int:
        if not self.counts:
            raise ValueError("model not fitted")
        bag = Counter(tokenize(text, self.mask_numbers))
        size = len(self.vocab) + 1
        n = sum(self.priors.values())
        scores = {}
        for label, counts in self.counts.items():
            score = math.log(self.priors[label] / n)
            denominator = self.totals[label] + size
            for token, occurrences in bag.items():
                score += occurrences * math.log(
                    (counts.get(token, 0) + 1) / denominator)
            scores[label] = score
        return min(scores, key=lambda label: (-scores[label], label))


def held_out_rows() -> list[tuple[str, int, str]]:
    verify_upstream_snapshot()
    with DATA.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    accepted = []
    for row in rows:
        target = number_of_steps(row["requirement"])
        original = number_of_steps(row["Original_Requirement"])
        normalized = re.sub(r"\s+", "", row["formula"])
        if target is not None and original == 3 and normalized == "G(a->X(X(Xb)))":
            accepted.append((row["requirement"], target, row["Original_Requirement"]))
    return accepted


def run_exploratory_baseline() -> dict[str, object]:
    audited = audit_snapshot()
    rows = held_out_rows()
    assert len(rows) == audited["strict_template_rows"] == 5
    assert len({source for _, _, source in rows}) == 1
    train = training_examples()
    train_texts = {text.lower() for text, _ in train}
    if any(text.lower() in train_texts for text, _, _ in rows):
        raise AssertionError("external text overlaps synthetic training")
    fitted = MultinomialNB().fit(train)
    masked = MultinomialNB(mask_numbers=True).fit(train)
    predictions = [fitted.predict(text) for text, _, _ in rows]
    masked_predictions = [masked.predict(text) for text, _, _ in rows]
    truths = [target for _, target, _ in rows]
    return {
        "training_examples": len(train),
        "training_provenance": "synthetic, five authored paraphrase templates; not external training",
        "held_out_external_rows": len(rows),
        "independent_external_source_instructions": 1,
        "external_labels": truths,
        "learned_predictions": predictions,
        "learned_correct_rows": sum(a == b for a, b in zip(predictions, truths)),
        "masked_predictions": masked_predictions,
        "masked_correct_rows": sum(a == b for a, b in zip(masked_predictions, truths)),
        "inherited_formula_offset": 3,
        "inherited_label_mismatches": sum(x != 3 for x in truths),
        "evaluation_status": "EXPLORATORY_ONLY_INSUFFICIENT_INDEPENDENT_SOURCES",
        "publication_ready": False,
        "claim_limits": [
            "One independent external source instruction; five correlated mutations.",
            "The task is number-word classification, not NL-to-LTL generation or physical reasoning.",
            "The numeric parser defines labels only on a predeclared strict template.",
            "Synthetic training data and exact external template must not be called broad generalization.",
            "The inherited formula is an annotation baseline, not a competing trained model.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_exploratory_baseline(), indent=2, sort_keys=True))
