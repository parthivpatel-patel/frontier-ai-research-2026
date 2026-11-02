"""Pinned, metadata-only access audit for SecDev 2026 NL2FutureLTL input.

Protocol 021. No model inference, scoring, physical assumptions, independent
adjudication, or redistribution of the upstream data. Standard library only.
"""
from __future__ import annotations

from collections import defaultdict
import csv
import hashlib
import io
import json
import re
from urllib.request import Request, urlopen

REPO = "ochowdhu/NL2LTL-SecDev26"
COMMIT = "35b2b28069531f3ca5cea938182f652bacd4922a"
PATH = "input_data/nl2ltl_finalized.csv"
BLOB_SHA1 = "9a0939aad2ecce0a20094f29e7cc87dd2e88d731"
URL = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/{PATH}"
MAX_BYTES = 60_000
MAX_ROWS = 10_000
HEADER = ("Natural Language", "Ground Truth", "Atomic Proposition")


def git_blob_sha1(raw: bytes) -> str:
    """Git object ID of a byte-exact blob; provenance check, not a MAC."""
    if not isinstance(raw, bytes):
        raise ValueError("source must be bytes")
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def normalized_nl(value: str) -> str:
    """Only case and whitespace normalization; NOT semantic equivalence."""
    return " ".join(value.casefold().split())


def normalized_formula(value: str) -> str:
    """Whitespace-only lexical grouping; NOT an LTL equivalence checker."""
    return re.sub(r"\s+", "", value)


def audit_csv_bytes(raw: bytes, *, expected_blob_sha: str) -> dict:
    """Audit a pinned CSV, returning counts only, never original rows.

    Synthetic tests may pass their own known blob hash. The production entry
    point always passes the frozen upstream blob hash from Protocol 021.
    """
    if not isinstance(raw, bytes) or not 1 <= len(raw) <= MAX_BYTES:
        raise ValueError("invalid or oversized source bytes")
    if (not isinstance(expected_blob_sha, str)
            or re.fullmatch(r"[0-9a-f]{40}", expected_blob_sha) is None):
        raise ValueError("invalid expected Git blob SHA-1")
    digest = git_blob_sha1(raw)
    if digest != expected_blob_sha:
        raise ValueError("source bytes differ from the pinned Git blob")
    try:
        decoded = raw.decode("utf-8-sig", errors="strict")
        reader = csv.reader(io.StringIO(decoded, newline=""), strict=True)
        if tuple(next(reader, ())) != HEADER:
            raise ValueError("unexpected CSV schema")
        n = 0
        nl_counts: dict[str, int] = defaultdict(int)
        formula_counts: dict[str, int] = defaultdict(int)
        pair_counts: dict[tuple[str, str], int] = defaultdict(int)
        formulas_by_nl: dict[str, set[str]] = defaultdict(set)
        nl_by_formula: dict[str, set[str]] = defaultdict(set)
        for row in reader:
            n += 1
            if n > MAX_ROWS:
                raise ValueError("row limit exceeded")
            if len(row) != len(HEADER):
                raise ValueError("malformed CSV row")
            nl, formula, ap = row
            if not nl.strip() or not formula.strip():
                raise ValueError("empty NL or ground-truth formula")
            if len(nl) > 10_000 or len(formula) > 10_000 or len(ap) > 10_000:
                raise ValueError("oversized cell")
            source = normalized_nl(nl)
            target = normalized_formula(formula)
            nl_counts[source] += 1
            formula_counts[target] += 1
            pair_counts[(source, target)] += 1
            formulas_by_nl[source].add(target)
            nl_by_formula[target].add(source)
    except (UnicodeError, csv.Error) as exc:
        raise ValueError("invalid UTF-8 or malformed CSV") from exc
    if n == 0:
        raise ValueError("empty CSV")
    return {
        "status": "PINNED_INPUT_SCHEMA_AND_LEXICAL_COUNTS_ONLY",
        "git_blob_sha1_verified": digest,
        "input_rows": n,
        "distinct_normalized_nl_strings": len(nl_counts),
        "distinct_whitespace_normalized_formula_strings": len(formula_counts),
        "distinct_nl_formula_pairs": len(pair_counts),
        "duplicate_nl_formula_pair_occurrences": sum(v - 1 for v in pair_counts.values()),
        "normalized_nl_strings_with_multiple_lexical_formulas":
            sum(len(v) > 1 for v in formulas_by_nl.values()),
        "lexical_formulas_with_multiple_normalized_nl_strings":
            sum(len(v) > 1 for v in nl_by_formula.values()),
        "nl_strings_repeated_across_rows": sum(v > 1 for v in nl_counts.values()),
        "source_family_independence_verified": False,
        "independent_human_intent_adjudications": 0,
        "authenticated_nl2futureltl_model_predictions": 0,
        "semantic_mismatch_claims": 0,
        "novelty_established": False,
        "limits": (
            "Lexical duplicates and one-to-many mappings are annotation-review "
            "candidates, not semantic errors. Distinct strings are not independent "
            "requirements. The source's README/license terms conflict; do not "
            "redistribute or adapt upstream dataset without rights review."
        ),
    }


def audit_pinned() -> dict:
    """Read <=60 KB from one pinned public URL; fail closed on any error."""
    request = Request(URL, headers={"User-Agent": "frontier-research-pinned-audit/1.0"})
    with urlopen(request, timeout=15) as response:
        raw = response.read(MAX_BYTES + 1)
    result = audit_csv_bytes(raw, expected_blob_sha=BLOB_SHA1)
    return {
        "protocol": "021_secdev26_source_eligibility",
        "source_repository": REPO,
        "source_commit": COMMIT,
        "source_path": PATH,
        "external_data_redistributed": False,
        **result,
    }


if __name__ == "__main__":
    print(json.dumps(audit_pinned(), indent=2, sort_keys=True))
