"""Exact lasso checks under two explicitly bounded discrete actuator models.

This is classical finite-transition-system reasoning, not a new algorithm,
a real robot experiment, or an NLP/LLM evaluation.  A bounded search failure
is NEVER treated as a proof of equivalence for a nondeterministic model.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import product
import csv
import json

from src.independent_source_audit import Lasso, holds, recognize
from src.temporal_label_audit import DATA, verify_upstream_snapshot

LABELS = (frozenset({"a"}), frozenset(), frozenset({"b"}))


@dataclass(frozen=True)
class Actuator:
    name: str
    edges: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        if len(self.edges) != 3 or any(not row or any(
                target not in (0, 1, 2) for target in row) for row in self.edges):
            raise ValueError("expected three nonempty transition rows")

    @property
    def deterministic(self) -> bool:
        return all(len(row) == 1 for row in self.edges)


FLEXIBLE = Actuator("bounded_step_control", ((0, 1), (0, 1, 2), (1, 2)))
FIXED = Actuator("fixed_positive_step", ((1,), (2,), (2,)))


@dataclass(frozen=True)
class StateLasso:
    prefix: tuple[int, ...]
    loop: tuple[int, ...]

    def propositions(self) -> Lasso:
        return Lasso(tuple(LABELS[x] for x in self.prefix),
                     tuple(LABELS[x] for x in self.loop))

    def valid(self, model: Actuator) -> bool:
        if not self.loop:
            return False
        states = self.prefix + self.loop
        if not states or states[0] != 0 or any(x not in (0, 1, 2) for x in states):
            return False
        return (all(y in model.edges[x] for x, y in zip(states, states[1:]))
                and self.loop[0] in model.edges[states[-1]])

    def encoded(self) -> dict[str, list[int]]:
        return {"prefix": list(self.prefix), "loop": list(self.loop)}


def unique_fixed_trace() -> StateLasso:
    """Complete infinite trace of FIXED from initial x=0."""
    return StateLasso((0, 1), (2,))


def candidates(model: Actuator, max_states: int = 9,
               max_loop: int = 3):
    """Finite, explicitly bounded enumeration; not complete model checking."""
    if max_states < 1 or max_loop < 1:
        raise ValueError("positive bounds required")
    for total in range(1, max_states + 1):
        for loop_length in range(1, min(total, max_loop) + 1):
            prefix_length = total - loop_length
            for suffix in product((0, 1, 2), repeat=total - 1):
                states = (0,) + suffix
                witness = StateLasso(states[:prefix_length],
                                     states[prefix_length:])
                if witness.valid(model):
                    yield witness


@lru_cache(maxsize=None)
def find_witness(model: Actuator, target_offset: int,
                 source_true: bool, max_states: int = 9,
                 max_loop: int = 3) -> StateLasso | None:
    """Find an infinite admissible lasso separating two offset predicates.

    If none is found, only FIXED's unique-trace check is exhaustive.
    For FLEXIBLE, None means NOT FOUND WITHIN BOUND, never equivalence.
    """
    if target_offset not in (1, 2, 4, 6):
        raise ValueError("only pinned external changed offsets supported")
    words = ((unique_fixed_trace(),) if model == FIXED
             else candidates(model, max_states, max_loop))
    for witness in words:
        if not witness.valid(model):
            raise AssertionError("internal witness violates dynamics")
        trace = witness.propositions()
        inherited = holds("offset", 3, trace, inherited_formula=True)
        changed = holds("offset", target_offset, trace, inherited_formula=False)
        if inherited == source_true and changed != source_true:
            return witness
    return None


def changed_offsets() -> tuple[int, ...]:
    """Deduplicate mutation rows by changed semantic offset."""
    verify_upstream_snapshot()
    offsets: set[int] = set()
    with DATA.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            result = recognize(row)
            if result is not None and result[0] == "offset" and result[2] != 3:
                offsets.add(result[2])
    if offsets != {1, 2, 4, 6}:
        raise AssertionError("pinned external offset family changed")
    return tuple(sorted(offsets))


def audit() -> dict[str, object]:
    comparisons = []
    for model in (FLEXIBLE, FIXED):
        for n in changed_offsets():
            forward = find_witness(model, n, True)
            reverse = find_witness(model, n, False)
            comparisons.append({
                "model": model.name, "changed_offset": n,
                "inherited_true_changed_false": (
                    forward.encoded() if forward else None),
                "inherited_false_changed_true": (
                    reverse.encoded() if reverse else None),
                "absence_interpretation": (
                    "EXHAUSTIVE_UNIQUE_TRACE" if model.deterministic
                    else "BOUNDED_SEARCH_ONLY_NO_EQUIVALENCE_PROOF"),
            })
    return {
        "external_originals_in_this_experiment": 1,
        "distinct_changed_offsets": list(changed_offsets()),
        "models": {
            "bounded_step_control": "x(0)=0; x in {0,1,2}; |x(t+1)-x(t)|<=1",
            "fixed_positive_step": "x(0)=0; x(t+1)=min(2,x(t)+1)",
            "atoms": "a iff x=0; b iff x=2; x=1 has neither",
        },
        "comparisons": comparisons,
        "status": "TOY_DYNAMICS_FILTER_NOT_MODEL_PERFORMANCE",
        "publication_ready": False,
        "limits": [
            "One external original and four distinct mutations, not four independent tasks.",
            "Only finite-state, discrete, constructed dynamics; no measured physical data.",
            "Flexible model search is bounded: missing witness is not equivalence.",
            "Fixed model is exhaustive because its unique infinite trace is known.",
            "No actual NL-to-LTL model predictions or new theoretical guarantee.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
