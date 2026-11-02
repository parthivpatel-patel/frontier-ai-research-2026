"""Bounded, read-only schema audit of externally hosted QSTRBench records.

No model inference, no raw record publication, no evaluation score claims.
Run in GitHub Actions, not on the user's laptop. Python standard library only.
"""
from __future__ import annotations

import hashlib
import io
import json
import lzma
from collections import Counter
from urllib.request import Request, urlopen

UPSTREAM = "RobBlackwell/QSTRBench"
COMMIT = "7da82bae3b1300e8f7fba8f448adca551e0a1f9a"
FILES = {
    "questions": (
        "data/raw/QSTRBench/questions.jsonl.xz",
        "d1a85e4b821ba67e18b267d0f012845ed3c38b22",
        31564,
    ),
    "openai_gpt5": (
        "data/raw/QSTRBench/openai-gpt-5/answers.jsonl.xz",
        "79ae331232af66ad936da12155c7539a6b7a02fb",
        364448,
    ),
    "claude_sonnet4": (
        "data/raw/QSTRBench/claude-sonnet-4-20250514/answers.jsonl.xz",
        "2f17d23ba659caaf9b70773cfc89b0d16d34642f",
        402552,
    ),
}
MAX_COMPRESSED = 1_000_000
MAX_DECOMPRESSED = 256_000_000
MAX_LINE = 1_000_000
MAX_ROWS = 100_000


def git_blob_sha(blob: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(blob)).encode() + b"\0" + blob).hexdigest()


def iter_records(blob: bytes, expected_sha: str, expected_size: int):
    """Stream bounded JSONL objects without retaining external model responses."""
    if len(blob) != expected_size or len(blob) > MAX_COMPRESSED:
        raise ValueError("Compressed input size mismatch or exceeded bound")
    if git_blob_sha(blob) != expected_sha:
        raise ValueError("Upstream Git blob SHA mismatch")
    count = 0
    total = 0
    try:
        with lzma.LZMAFile(io.BytesIO(blob)) as stream:
            while True:
                line = stream.readline(MAX_LINE + 1)
                if not line:
                    break
                total += len(line)
                if total > MAX_DECOMPRESSED:
                    raise ValueError("Decompressed input exceeded bound")
                if len(line) > MAX_LINE:
                    raise ValueError("JSONL line exceeded bound")
                if not line.strip():
                    continue
                if count >= MAX_ROWS:
                    raise ValueError("Too many records")
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError("Expected JSON objects, not scalar/array rows")
                count += 1
                yield row
    except lzma.LZMAError as exc:
        raise ValueError("Invalid xz data") from exc
    if not count:
        raise ValueError("No records found")


def unpack_records(blob: bytes, expected_sha: str, expected_size: int) -> list[dict]:
    """Test helper only; cloud audit uses the streaming iterator."""
    return list(iter_records(blob, expected_sha, expected_size))


def schema_summary(rows) -> dict:
    count = 0
    fields = Counter()
    types: dict[str, Counter] = {}
    identifiers = Counter()
    repeats = Counter()
    nested_fields: dict[str, Counter] = {}
    for row in rows:
        count += 1
        for key, value in row.items():
            fields[key] += 1
            types.setdefault(key, Counter())[type(value).__name__] += 1
            if key in ("request", "response") and isinstance(value, dict):
                nested_fields.setdefault(key, Counter()).update(value.keys())
        identifier = row.get("id", row.get("ID"))
        if identifier is not None:
            identifiers[str(identifier)] += 1
        if "repeat" in row:
            repeats[str(row["repeat"])] += 1
    return {
        "rows": count,
        "fields_present": dict(sorted(fields.items())),
        "field_types": {k: dict(sorted(v.items())) for k, v in sorted(types.items())},
        "nested_fields_present": {k: dict(sorted(v.items())) for k, v in sorted(nested_fields.items())},
        "unique_identifier_values": len(identifiers),
        "identifier_values_with_repeats": sum(n > 1 for n in identifiers.values()),
        "repeat_field_distribution": dict(sorted(repeats.items())),
        "interpretation": "Schema only; no model accuracy, semantics, or authorship established",
    }


def audit() -> dict:
    result = {
        "upstream": f"https://github.com/{UPSTREAM}/tree/{COMMIT}",
        "upstream_commit": COMMIT,
        "rights": "Upstream claims CC BY 4.0 for its dataset; third-party materials differ",
        "task": "QSTR, not NL-to-LTL translation",
        "files": {},
    }
    for name, (path, sha, size) in FILES.items():
        url = f"https://raw.githubusercontent.com/{UPSTREAM}/{COMMIT}/{path}"
        request = Request(url, headers={"User-Agent": "frontier-ai-research-read-only-schema-audit"})
        with urlopen(request, timeout=20) as response:
            blob = response.read(MAX_COMPRESSED + 1)
        rows = iter_records(blob, sha, size)
        result["files"][name] = {
            "source_path": path,
            "git_blob_sha1": sha,
            "compressed_bytes": size,
            **schema_summary(rows),
        }
    return result


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
