"""Pinned, aggregate-only structural audit of historical NL2MTL outputs.

No model inference, no text redistribution, no accuracy claims. Network access is
used only in the explicit CLI, on the public GitHub Actions runner.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from urllib.request import urlopen

UPSTREAM_COMMIT = "c8cd92f7f46da57848cf9f6af494219f8683d1b3"
SOURCES = ("article_78", "article_80", "cara_pump_requirements", "harvesting_process")
# Git blob IDs from the upstream repository's immutable tree, inspected 2026-11-02.
SHAS = (
    ("85f482d17dbedcabe0915d014728b4ac655401f3", "ca282dccb9199653019b16d1a54758e166c02568", "4fac4446d4d45c2b755a5f0632bb30e8e7159893", "a3112b689cc8be67cd776e71ab3cff18697c3ec8"),
    ("489f6bba7cf3ae52263b1f1c9fc8f345c25dbc9e", "e386f28e9ddc74d7bbe358ed7daf343bbe101e6d", "a06c7141d525c2cc73603692d54a877d8ab272af", "9c547ce5697e0e0ba8a32fc1d569743a91f06e71"),
    ("4ab9972e9be8f6412e793d25152b4b3de20b1cb2", "10ebf7e5992672d8ac59baaa1ac2b4466ef8208f", "ff81bdfbf6dd1caa3f667cbdfa3def3ee5f22de7", "7b69db7c56db357025a02ad346227171c20d7771"),
    ("e58ffbbfa32743bda872237f6d20f75a6d83eaa2", "0b26da6ac85c24c79039e3a24aa91b32f5ba0c45", "08a188aa3c953ece8011ba1d4a9fdd9ff78fbe1a", "d06bac9d10f9a5eb3636924717d38eeca143ff7c"),
    ("f27e3c5412b86e75c15297b8c729ae6785ac8315", "d9adf6b4f5688c0634cb83a63c1ff7034b6b9196", "1beefb21d55e5158a71498df46a21d56259755cf", "30ce2a152b7da8b72ff279482c3228f4112b91bb"),
)
# Note: the SHA table is validated by tests and by the remote blob digest;
# no partially verified aggregate may be emitted.
MAX_BYTES = 20_000


def manifest() -> dict[str, str]:
    return {
        f"data/test_{run}/output/{source}.json": SHAS[run - 1][index]
        for run in range(1, 6)
        for index, source in enumerate(SOURCES)
    }


def verify_blob(data: bytes, expected_sha: str) -> dict:
    if len(data) > MAX_BYTES:
        raise ValueError("external file exceeds the pinned size limit")
    actual = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + bytes([0]) + data).hexdigest()
    if actual != expected_sha:
        raise ValueError("upstream blob SHA mismatch")
    decoded = json.loads(data.decode("utf-8"))
    if not isinstance(decoded, dict):
        raise ValueError("expected a JSON object")
    return decoded


def fetch_pinned() -> dict[str, dict]:
    result = {}
    for path, sha in manifest().items():
        url = (
            "https://raw.githubusercontent.com/marisol-barrientos/nl2mtl/"
            + UPSTREAM_COMMIT + "/" + path
        )
        with urlopen(url, timeout=10) as response:
            data = response.read(MAX_BYTES + 1)
        result[path] = verify_blob(data, sha)
    return result


def nonempty(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return value is not None and value is not False


def audit(records: dict[str, dict]) -> dict:
    if set(records) != set(manifest()):
        raise ValueError("incomplete or unexpected source-file set")
    by_source = {source: [] for source in SOURCES}
    totals = Counter()
    ambiguity_types = Counter()
    assumption_types = Counter()
    for path in manifest():
        record = records[path]
        if not isinstance(record, dict):
            raise ValueError("invalid output object")
        expressions = record.get("MTL_expressions")
        dependencies = record.get("dependency_sequence")
        nonformalized = record.get("non_formalized_parts")
        if not all(isinstance(x, list) for x in (expressions, dependencies, nonformalized)):
            raise ValueError("missing or non-list structural field")
        source = path.rsplit("/", 1)[1].removesuffix(".json")
        by_source[source].append(len(expressions))
        totals["expression_records"] += len(expressions)
        totals["dependency_edges"] += len(dependencies)
        totals["nonformalized_parts"] += len(nonformalized)
        ids = []
        for expression in expressions:
            if not isinstance(expression, dict):
                raise ValueError("invalid expression record")
            eid = expression.get("id")
            formula = expression.get("MTL_expression")
            props = expression.get("propositions")
            if not isinstance(eid, str) or not isinstance(formula, str) or not isinstance(props, list):
                raise ValueError("malformed expression fields")
            ids.append(eid)
            totals["empty_formulas"] += int(not formula.strip())
            totals["expressions_with_propositions"] += int(bool(props))
            totals["proposition_records"] += len(props)
            for prop in props:
                if not isinstance(prop, dict):
                    raise ValueError("malformed proposition")
                for field, counter, metric in (
                    ("ambiguities", ambiguity_types, "propositions_with_nonempty_ambiguities"),
                    ("assumptions", assumption_types, "propositions_with_nonempty_assumptions"),
                ):
                    value = prop.get(field)
                    counter[type(value).__name__] += 1
                    totals[metric] += int(nonempty(value))
        totals["duplicate_expression_ids"] += len(ids) - len(set(ids))
        for edge in dependencies:
            if not isinstance(edge, dict):
                raise ValueError("malformed dependency")
            for field in ("preceding_id", "following_id"):
                ref = edge.get(field)
                if not isinstance(ref, str):
                    raise ValueError("malformed dependency reference")
                totals["unresolved_local_dependency_endpoints"] += int(ref not in ids)
    return {
        "audit": "pinned_external_schema_only",
        "upstream_commit": UPSTREAM_COMMIT,
        "files_verified": len(records),
        "source_documents": len(SOURCES),
        "runs_per_document": 5,
        "per_source_expression_counts": {
            source: {"runs": counts, "min": min(counts), "max": max(counts),
                     "mean": sum(counts) / len(counts)}
            for source, counts in by_source.items()
        },
        "sources_with_variable_expression_counts": sum(
            len(set(counts)) > 1 for counts in by_source.values()
        ),
        "totals": dict(sorted(totals.items())),
        "ambiguity_field_json_types": dict(sorted(ambiguity_types.items())),
        "assumption_field_json_types": dict(sorted(assumption_types.items())),
        "limitations": (
            "Four source documents, repeated outputs, no independent intent labels; "
            "no cross-run formula alignment or model correctness inference."
        ),
    }


def main() -> None:
    print(json.dumps(audit(fetch_pinned()), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
