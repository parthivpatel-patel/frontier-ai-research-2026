"""Three-source, finite-grammar audit of inherited NL-to-LTL labels.

Scientific limits:
* Only a pinned 25-row MIT-licensed mutation CSV is inspected.
* The three supported source requirements are three independent original
  English strings, not fifteen independent examples.
* Counterexamples use explicitly ultimately periodic infinite traces.
* No LLM or physical model is evaluated; no novel algorithm is claimed.
* A passing witness is NOT a proof that two formulas are equivalent.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import csv
import json
import re

from src.temporal_label_audit import DATA, NUMBER, verify_upstream_snapshot


@dataclass(frozen=True)
class Lasso:
    """Infinite word: finite prefix followed by a nonempty repeating loop."""
    prefix: tuple[frozenset[str], ...]
    loop: tuple[frozenset[str], ...]

    def at(self, time: int) -> frozenset[str]:
        if time < 0 or not self.loop:
            raise ValueError("invalid time or empty loop")
        if time < len(self.prefix):
            return self.prefix[time]
        return self.loop[(time - len(self.prefix)) % len(self.loop)]

    @property
    def representative_times(self) -> range:
        # For a bounded-next-step G predicate, one loop period plus the
        # finite prefix covers every distinct triggering configuration.
        return range(len(self.prefix) + len(self.loop))


EMPTY = frozenset()
A = frozenset({"a"})
B = frozenset({"b"})
C = frozenset({"c"})
OFFSET = re.compile(
    r"Whenever a is enabled, b is enabled (one|two|three|four|five|six|seven|eight|nine) steps later\.",
    re.IGNORECASE,
)
RELATIVE = re.compile(
    r"Whenever a holds and b holds in the next step, then c holds (one|two) steps? after b\.",
    re.IGNORECASE,
)
CARDINALITY = re.compile(
    r"(one|two) of the following aps will hold at all instances: a,b,c\.",
    re.IGNORECASE,
)
GRAMMARS = (
    ("offset", OFFSET, "G(a->X(X(Xb)))", 3),
    ("relative", RELATIVE, "G(a&&Xb->XXc)", 1),
    ("cardinality", CARDINALITY, "G(a|b|c)", 1),
)


def recognize(row: dict[str, str]) -> tuple[str, int, int] | None:
    formula = re.sub(r"\s+", "", row["formula"])
    for family, pattern, expected_formula, expected_source in GRAMMARS:
        original = pattern.fullmatch(row["Original_Requirement"].strip())
        mutated = pattern.fullmatch(row["requirement"].strip())
        if original is None or mutated is None or formula != expected_formula:
            continue
        source_n = NUMBER[original.group(1).lower()]
        target_n = NUMBER[mutated.group(1).lower()]
        if source_n != expected_source:
            raise ValueError("original text is inconsistent with supported source formula")
        return family, source_n, target_n
    return None


def witness_for(family: str) -> Lasso:
    if family == "offset":
        # a at t=0, b at t=3; afterwards neither occurs.
        return Lasso((A, EMPTY, EMPTY, B), (EMPTY,))
    if family == "relative":
        # a at t=0, b at t=1, c at t=2; afterwards none occurs.
        return Lasso((A, B, C), (EMPTY,))
    if family == "cardinality":
        # Only a holds, forever. Both exact-two and at-least-two fail.
        return Lasso((), (A,))
    raise ValueError("unsupported grammar")


def holds(family: str, n: int, trace: Lasso, *, inherited_formula: bool) -> bool:
    """Evaluate supported G predicates exactly on an ultimately periodic word.

    No generic LTL solver is claimed. The inherited-formula branch implements
    the three exact source formulas; the other branch implements the strictly
    recognized English meaning. For 'one of', this uses at-least-one; we do
    not claim this resolves the source phrase's exact-vs-at-least ambiguity.
    """
    for t in trace.representative_times:
        if family == "offset":
            delay = 3 if inherited_formula else n
            if "a" in trace.at(t) and "b" not in trace.at(t + delay):
                return False
        elif family == "relative":
            delay = 1 if inherited_formula else n
            if ("a" in trace.at(t) and "b" in trace.at(t + 1)
                    and "c" not in trace.at(t + 1 + delay)):
                return False
        elif family == "cardinality":
            count = len(trace.at(t) & frozenset({"a", "b", "c"}))
            threshold = 1 if inherited_formula else n
            if count < threshold:
                return False
        else:
            raise ValueError("unsupported grammar")
    return True


def audit_independent_sources() -> dict[str, object]:
    blob = verify_upstream_snapshot()
    with DATA.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    supported: list[dict[str, object]] = []
    counterexamples: list[dict[str, object]] = []
    for i, row in enumerate(rows, 1):
        recognized = recognize(row)
        if recognized is None:
            continue
        family, source_n, target_n = recognized
        trace = witness_for(family)
        if not holds(family, source_n, trace, inherited_formula=True):
            raise AssertionError("inherited formula does not hold on its proposed witness")
        changed = not holds(family, target_n, trace, inherited_formula=False)
        supported.append({
            "row": i, "family": family, "original": row["Original_Requirement"],
            "mutated": row["requirement"], "witnessed_mismatch": changed,
        })
        if changed:
            counterexamples.append({
                "row": i, "family": family,
                "mutated": row["requirement"],
                "witness": {
                    "prefix": [sorted(s) for s in trace.prefix],
                    "repeating_loop": [sorted(s) for s in trace.loop],
                },
                "inherited_formula_true": True,
                "strict_english_false": True,
            })
    groups = sorted({r["original"] for r in supported})
    by_family = Counter(str(r["family"]) for r in supported)
    mismatch_by_family = Counter(str(r["family"]) for r in counterexamples)
    return {
        "source_rows": len(rows),
        "supported_rows": len(supported),
        "independent_original_requirements": len(groups),
        "supported_rows_by_family": dict(sorted(by_family.items())),
        "witnessed_mismatches_by_family": dict(sorted(mismatch_by_family.items())),
        "witnessed_mismatch_rows": len(counterexamples),
        "distinct_witnessed_mutated_texts": len({r["mutated"] for r in counterexamples}),
        "unsupported_rows_no_verdict": len(rows) - len(supported),
        "supported_rows_without_counterexample_no_equivalence_claim":
            len(supported) - len(counterexamples),
        "upstream_git_blob_sha1": blob,
        "source_requirements": groups,
        "counterexamples": counterexamples,
        "status": "EXPLORATORY_DATASET_CONSISTENCY_ONLY",
        "publication_ready": False,
        "limits": [
            "Only three original source requirements; repeated mutations are dependent.",
            "Strict template matching only; unsupported rows are not judged.",
            "One infinite-trace witness proves mismatch; lack of witness proves nothing.",
            "The original 'one of' phrase is potentially ambiguous; no claim of exact source equivalence.",
            "This is not an LLM benchmark, a physical simulation, or evidence of novelty.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(audit_independent_sources(), indent=2, sort_keys=True))
