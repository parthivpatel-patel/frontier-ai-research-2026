"""Replicate QSTRBench's published strict set-equality scorer on pinned records.

Run only on a free public GitHub-hosted runner. Aggregate results only:
never print or commit source prompts, answers, or individual model responses.
This is a replication of upstream bin/process.py, not a novel method.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from urllib.request import Request, urlopen

from src.qstr_schema_audit import (
    COMMIT, FILES, MAX_COMPRESSED, UPSTREAM, iter_records,
)


def clean_answer(text: str) -> str:
    """Mirror QSTRBench bin/process.py clean_answer."""
    if not isinstance(text, str):
        raise ValueError("Expected text answer")
    matches = list(re.finditer(r"answer:", text, re.IGNORECASE))
    if matches:
        after = text[matches[-1].end():]
        lines = [line.strip() for line in after.splitlines()]
        result = next((line for line in lines if line), "")
    else:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        result = lines[-1] if lines else ""
    return re.sub(r"^[^a-zA-Z0-9<>=]+|[^a-zA-Z0-9<>=\)]+$", "", result)


def extract_relation(value: str) -> str:
    value = value.strip()
    stripped = value.rstrip(")];,")
    match = re.match(r"^\s*\S+\s*([<>]=?|!=|==|=)\s*\S+\s*$", stripped)
    if match:
        return "=" if match.group(1) == "==" else match.group(1)
    tokens = value.split()
    if len(tokens) == 3:
        return tokens[1]
    return value


def parse_answers(text: str) -> list[str]:
    """Mirror QSTRBench bin/process.py parse_answers (including its limitations)."""
    text = re.sub(r"\([^)]*\)", "", text)
    parts = [p.strip() for p in re.split(r"[;,]", text) if p.strip()]
    return [extract_relation(re.sub(r"\*{2,}", "", p)) for p in parts]


def reference_set(value) -> frozenset[str]:
    if value is None:
        return frozenset()
    values = value if isinstance(value, list) else [value]
    if any(not isinstance(v, str) for v in values):
        raise ValueError("Reference relation must be text")
    return frozenset(values)


def question_index(rows) -> dict[str, tuple[frozenset[str], str, str]]:
    result = {}
    for row in rows:
        identifier = str(row["ID"])
        if identifier in result:
            raise ValueError("Duplicate question identifier")
        result[identifier] = (
            reference_set(row["ANSWER"]),
            str(row["TYPE"]),
            str(row["CALCULUS"]),
        )
    if not result:
        raise ValueError("No questions")
    return result


def score_rows(rows, questions, expected_repeats) -> dict:
    """Fail closed on missing/duplicate joins and report only aggregate metrics."""
    counts = Counter()
    correct = Counter()
    by_type = defaultdict(Counter)
    by_calculus = defaultdict(Counter)
    by_repeat = defaultdict(Counter)
    observed = set()
    parsed_by_id = defaultdict(set)
    correct_by_id = defaultdict(list)
    for row in rows:
        identifier = str(row["id"])
        repeat = row["repeat"]
        if not isinstance(repeat, int) or repeat not in expected_repeats:
            raise ValueError("Unexpected repeat")
        key = (identifier, repeat)
        if key in observed:
            raise ValueError("Duplicate model answer for question/repeat")
        if identifier not in questions:
            raise ValueError("Model answer without matching question")
        observed.add(key)
        truth, kind, calculus = questions[identifier]
        prediction = frozenset(parse_answers(clean_answer(row["answer"])))
        is_correct = prediction == truth
        counts["rows"] += 1
        counts["empty_parsed_answers"] += not prediction
        correct["correct"] += is_correct
        by_type[kind]["rows"] += 1
        by_type[kind]["correct"] += is_correct
        by_calculus[calculus]["rows"] += 1
        by_calculus[calculus]["correct"] += is_correct
        by_repeat[str(repeat)]["rows"] += 1
        by_repeat[str(repeat)]["correct"] += is_correct
        parsed_by_id[identifier].add(prediction)
        correct_by_id[identifier].append(is_correct)

    expected = {(identifier, repeat) for identifier in questions for repeat in expected_repeats}
    if observed != expected:
        raise ValueError("Missing question/repeat rows")
    if len(parsed_by_id) != len(questions):
        raise ValueError("Question coverage mismatch")
    return {
        "rows": counts["rows"],
        "questions": len(questions),
        "strict_correct": correct["correct"],
        "strict_accuracy": round(correct["correct"] / counts["rows"], 6),
        "empty_parsed_answers": counts["empty_parsed_answers"],
        "by_type": {k: dict(v) for k, v in sorted(by_type.items())},
        "by_calculus": {k: dict(v) for k, v in sorted(by_calculus.items())},
        "by_repeat": {k: dict(v) for k, v in sorted(by_repeat.items())},
        "question_level": {
            "distinct_parsed_predictions_across_repeats": sum(
                len(predictions) > 1 for predictions in parsed_by_id.values()
            ),
            "all_repeats_correct": sum(all(values) for values in correct_by_id.values()),
            "any_repeat_correct": sum(any(values) for values in correct_by_id.values()),
        },
    }


def fetch_pinned(name):
    path, sha, size = FILES[name]
    url = f"https://raw.githubusercontent.com/{UPSTREAM}/{COMMIT}/{path}"
    request = Request(url, headers={"User-Agent": "frontier-ai-research-pinned-scoring-replication"})
    with urlopen(request, timeout=20) as response:
        blob = response.read(MAX_COMPRESSED + 1)
    return iter_records(blob, sha, size)


def audit():
    questions = question_index(fetch_pinned("questions"))
    return {
        "task": "QSTR qualitative relation reasoning; not NL-to-LTL",
        "source": f"https://github.com/{UPSTREAM}/tree/{COMMIT}",
        "scoring_source": f"https://github.com/{UPSTREAM}/blob/{COMMIT}/bin/process.py",
        "scoring": "Upstream clean_answer + parse_answers + exact set equality",
        "provenance": "Upstream-attributed model outputs; not independently authenticated",
        "uncertainty": "Repeats of one question are not independent source questions",
        "models": {
            "openai_gpt5": score_rows(fetch_pinned("openai_gpt5"), questions, (0, 1, 2)),
            "claude_sonnet4": score_rows(fetch_pinned("claude_sonnet4"), questions, (0,)),
        },
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
