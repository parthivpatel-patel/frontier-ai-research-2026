"""Pre-registered paired parser sensitivity audit of pinned QSTRBench responses.

Exploratory benchmark replication, not a model comparison or semantic oracle.
Run on standard free public GitHub Actions runner; output aggregates only.
See experiments/PROTOCOL_012_PARSER_SENSITIVITY_PREREGISTRATION.md.
"""
from __future__ import annotations

import json
import re
from collections import Counter

from src.qstr_scoring_replication import (
    clean_answer, fetch_pinned, parse_answers, question_index,
)

ANSWER_MARKER = re.compile(r"answer:", re.IGNORECASE)
COMPACT_INEQUALITY = re.compile(
    r"(?<![A-Za-z0-9_])([A-Za-z][A-Za-z0-9_]*)!=([A-Za-z][A-Za-z0-9_]*)(?![A-Za-z0-9_])"
)
UPSTREAM_EDGE_CLEANUP = re.compile(
    r"^[^a-zA-Z0-9<>=]+|[^a-zA-Z0-9<>=\\)]+$"
)


def clean_first_marker(text: str) -> str:
    """Only change last-answer-marker choice to first; preserve all other rules."""
    matches = list(ANSWER_MARKER.finditer(text))
    if not matches:
        return clean_answer(text)
    after = text[matches[0].end():]
    lines = [line.strip() for line in after.splitlines()]
    selected = next((line for line in lines if line), "")
    return UPSTREAM_EDGE_CLEANUP.sub("", selected)


def compact_inequality_fix(cleaned: str) -> str:
    """Only insert spaces around an isolated compact ASCII identifier != pair."""
    return COMPACT_INEQUALITY.sub(r"\\1 != \\2", cleaned)


def paired_sensitivity(rows, questions, expected_repeats) -> dict:
    """Fail closed on joins and report only paired aggregate counts."""
    expected = {
        (identifier, repeat)
        for identifier in questions
        for repeat in expected_repeats
    }
    observed = set()
    totals = Counter()
    changed_question_ids = {"compact": set(), "first_marker": set()}
    flipped_question_ids = {"compact": set(), "first_marker": set()}
    for row in rows:
        identifier = str(row["id"])
        repeat = row["repeat"]
        if identifier not in questions:
            raise ValueError("Model answer without matching question")
        if type(repeat) is not int or repeat not in expected_repeats:
            raise ValueError("Unexpected repeat")
        key = (identifier, repeat)
        if key in observed:
            raise ValueError("Duplicate model answer")
        observed.add(key)
        answer = row["answer"]
        if not isinstance(answer, str):
            raise ValueError("Expected text model answer")
        reference = questions[identifier][0]
        cleaned = clean_answer(answer)
        original_list = parse_answers(cleaned)
        legacy = frozenset(original_list)
        marker_count = len(ANSWER_MARKER.findall(answer))
        totals["rows"] += 1
        totals["legacy_correct"] += legacy == reference
        totals["no_answer_marker"] += marker_count == 0
        totals["multiple_answer_markers"] += marker_count > 1
        totals["compact_candidate"] += bool(COMPACT_INEQUALITY.search(cleaned))
        totals["legacy_empty"] += not legacy
        totals["legacy_duplicate_relations"] += len(original_list) != len(legacy)

        variants = {
            "compact": frozenset(parse_answers(compact_inequality_fix(cleaned))),
            "first_marker": frozenset(parse_answers(clean_first_marker(answer))),
        }
        for name, variant in variants.items():
            new_correct = variant == reference
            old_correct = legacy == reference
            totals[name + "_correct"] += new_correct
            if variant != legacy:
                totals[name + "_parsed_changed"] += 1
                changed_question_ids[name].add(identifier)
            if new_correct != old_correct:
                totals[name + "_score_flipped"] += 1
                flipped_question_ids[name].add(identifier)
                totals[name + ("_gained" if new_correct else "_lost")] += 1

    if observed != expected:
        raise ValueError("Missing question/repeat rows")
    summary = {
        "rows": totals["rows"],
        "unique_questions": len(questions),
        "legacy_correct": totals["legacy_correct"],
        "no_answer_marker": totals["no_answer_marker"],
        "multiple_answer_markers": totals["multiple_answer_markers"],
        "compact_candidate": totals["compact_candidate"],
        "legacy_empty": totals["legacy_empty"],
        "legacy_duplicate_relations": totals["legacy_duplicate_relations"],
        "interventions": {},
    }
    for name in ("compact", "first_marker"):
        summary["interventions"][name] = {
            "correct": totals[name + "_correct"],
            "parsed_changed_rows": totals[name + "_parsed_changed"],
            "parsed_changed_question_ids": len(changed_question_ids[name]),
            "gained_correct": totals[name + "_gained"],
            "lost_correct": totals[name + "_lost"],
            "score_flipped_rows": totals[name + "_score_flipped"],
            "score_flipped_question_ids": len(flipped_question_ids[name]),
        }
    return summary


def audit() -> dict:
    questions = question_index(fetch_pinned("questions"))
    return {
        "task": "QSTR recorded-output parser sensitivity; not NL-to-formal",
        "registration": "experiments/PROTOCOL_012_PARSER_SENSITIVITY_PREREGISTRATION.md",
        "interpretation": "Syntactic scorer sensitivity only; no semantic correctness adjudication",
        "provenance": "Upstream-attributed stored outputs; no new model inference",
        "models": {
            "openai_gpt5": paired_sensitivity(
                fetch_pinned("openai_gpt5"), questions, (0, 1, 2)
            ),
            "claude_sonnet4": paired_sensitivity(
                fetch_pinned("claude_sonnet4"), questions, (0,)
            ),
        },
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
