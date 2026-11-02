"""Pinned, bounded, aggregate-only VLTL-Bench prediction-string integrity audit.

Protocol 023. Run remotely on the public GitHub-hosted runner only.
External JSONL is held transiently in memory and never redistributed.
Exact token-string agreement is NOT semantic correctness or model accuracy.
"""
from __future__ import annotations

import hashlib
import json
import urllib.request

UPSTREAM_COMMIT = "383baea8210b93fe9fa7d14edd4757e5b3464e82"
UPSTREAM_ROOT = "https://raw.githubusercontent.com/Dubascudes/VLTL-Bench/"
MAX_BYTES = 1_048_576
FILES = (
    {
        "name": "navi_lifted",
        "path": "translation_eval/nl2tl/gt_lifting/navi.jsonl",
        "blob_sha": "c21575fca5e224968b56f0192b8bc0ddbaedac46",
        "bytes": 356248,
        "reference": "masked_tl",
    },
    {
        "name": "conformal_raw",
        "path": "translation_eval/nl2tl/raw_nl/conformal.jsonl",
        "blob_sha": "2e340b8b8632dd212214e583d8b964043d7f15dc",
        "bytes": 294840,
        "reference": "tl",
    },
)


def git_blob_sha(data: bytes) -> str:
    """Compute Git's SHA-1 blob object ID, including its length header."""
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def verify_pinned_bytes(data: bytes, expected_size: int, blob_sha: str) -> None:
    if type(expected_size) is not int or expected_size <= 0 or expected_size > MAX_BYTES:
        raise ValueError("invalid expected size")
    if not isinstance(data, bytes) or len(data) != expected_size:
        raise ValueError("pinned byte count mismatch")
    if not isinstance(blob_sha, str) or len(blob_sha) != 40:
        raise ValueError("invalid pinned Git blob SHA")
    if git_blob_sha(data) != blob_sha:
        raise ValueError("pinned Git blob SHA mismatch")


def _tokens(row: dict, key: str) -> list[str]:
    value = row.get(key)
    if (not isinstance(value, list) or not value or
            any(not isinstance(t, str) or not t.strip() for t in value)):
        raise ValueError(f"invalid {key} token list")
    return value


def audit_jsonl(data: bytes, reference: str) -> dict:
    """Return aggregates only; no source row, sentence, or prediction is returned."""
    if reference not in ("tl", "masked_tl"):
        raise ValueError("unsupported reference field")
    if not isinstance(data, bytes) or not data or len(data) > MAX_BYTES:
        raise ValueError("empty or oversized input")
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise ValueError("invalid UTF-8") from exc
    if not lines:
        raise ValueError("empty JSONL")
    ids: set[int] = set()
    exact = 0
    nonmatch = 0
    missing = 0
    blank = 0
    for lineno, line in enumerate(lines, 1):
        if not line.strip():
            raise ValueError(f"empty JSONL line {lineno}")
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL line {lineno}") from exc
        if not isinstance(row, dict):
            raise ValueError("JSONL record must be object")
        rid = row.get("id")
        if type(rid) is not int or rid < 0:
            raise ValueError("invalid record id")
        if rid in ids:
            raise ValueError("duplicate record id")
        ids.add(rid)
        _tokens(row, "sentence")
        _tokens(row, "tl")
        _tokens(row, "masked_tl")
        target = " ".join(_tokens(row, reference))
        if "prediction" not in row or row["prediction"] is None:
            missing += 1
            continue
        if not isinstance(row["prediction"], str):
            raise ValueError("invalid prediction type")
        prediction = " ".join(row["prediction"].split())
        if not prediction:
            blank += 1
        elif prediction == target:
            exact += 1
        else:
            nonmatch += 1
    observed = exact + nonmatch
    return {
        "status": "DESCRIPTIVE_STRING_IDENTITY_NOT_SEMANTIC_VALIDATION",
        "reference_field": reference,
        "records": len(ids),
        "unique_ids": len(ids),
        "missing_predictions": missing,
        "blank_predictions": blank,
        "nonblank_predictions": observed,
        "exact_token_string_matches": exact,
        "nonmatching_token_strings": nonmatch,
        "exact_match_fraction_among_nonblank": exact / observed if observed else None,
        "independent_source_families_verified": False,
        "model_provenance_verified": False,
        "semantic_correctness_verified": False,
        "redistribution_permission_verified": False,
        "novelty_established": False,
    }


def fetch_pinned(spec: dict) -> bytes:
    """Bound a single HTTPS fetch to a pinned commit and known path."""
    if spec not in FILES:
        raise ValueError("unregistered file")
    url = UPSTREAM_ROOT + UPSTREAM_COMMIT + "/" + spec["path"]
    req = urllib.request.Request(
        url, headers={"User-Agent": "frontier-ai-research-metadata-audit"}
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        data = response.read(MAX_BYTES + 1)
    verify_pinned_bytes(data, spec["bytes"], spec["blob_sha"])
    return data


def run_audit() -> dict:
    reports = []
    for spec in FILES:
        data = fetch_pinned(spec)
        report = audit_jsonl(data, spec["reference"])
        report["name"] = spec["name"]
        report["pinned_git_blob_sha"] = spec["blob_sha"]
        reports.append(report)
    return {
        "protocol": "023",
        "upstream_commit": UPSTREAM_COMMIT,
        "scope": "two distinct tasks; never pool their match fractions",
        "reports": reports,
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
