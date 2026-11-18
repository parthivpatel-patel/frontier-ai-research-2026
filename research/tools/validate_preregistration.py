#!/usr/bin/env python3
"""Validate a preregistration manifest and optional separate SHA-256 attestation.

Standard library only. Does not freeze a study, attest timing, or access outcomes.
Usage: python research/tools/validate_preregistration.py MANIFEST [ATTESTATION]\n       python research/tools/validate_preregistration.py --require-attestation MANIFEST ATTESTATION
"""
import hashlib
import json
import math
import pathlib
import sys


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def validate(manifest_path, attestation_path=None, require_attestation=False):
    errors = []
    raw = pathlib.Path(manifest_path).read_bytes()
    try:
        obj = json.loads(raw, object_pairs_hook=reject_duplicate_keys,
                         parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    except (ValueError, UnicodeDecodeError) as exc:
        return ["invalid JSON: " + str(exc)]
    if not isinstance(obj, dict):
        return ["manifest must be a JSON object"]
    if "frozen_manifest_sha256" in obj:
        errors.append("self-referential frozen_manifest_sha256 field prohibited")
    if obj.get("status") != "FROZEN":
        errors.append("status must equal FROZEN (drafts cannot pass freeze validation)")
    if raw != canonical_bytes(obj):
        errors.append("manifest bytes must be canonical UTF-8 JSON (sorted keys, compact separators)")
    def walk(value, path="$"):
        if value is None:
            errors.append(path + " contains null")
        if isinstance(value, float) and not math.isfinite(value):
            errors.append(path + " contains nonfinite number")
        if isinstance(value, dict):
            for k, v in value.items():
                walk(v, path + "." + k)
        if isinstance(value, list):
            for i, v in enumerate(value):
                walk(v, path + "[" + str(i) + "]")
    walk(obj)
    for field in ("source_family_definition", "sampling_frame", "domains",
                  "candidate_policies", "baselines", "multiplicity_family",
                  "verification_budget", "exclusion_rules", "adjudication_protocol"):
        if not obj.get(field):
            errors.append("missing/empty required field: " + field)
    domains = obj.get("domains")
    if not isinstance(domains, dict) or set(domains) != {"nlp", "mathematics", "physics"}:
        errors.append("domains must be an object with exactly nlp, mathematics, physics")
    else:
        for name, domain in domains.items():
            if not isinstance(domain, dict) or not domain.get("target_population") or not domain.get("sample_size_feasibility"):
                errors.append(name + " requires target_population and sample_size_feasibility")
    for field in ("candidate_policies", "baselines"):
        items = obj.get(field)
        if not isinstance(items, list) or not items:
            errors.append(field + " must be a nonempty list")
            continue
        ids = [item.get("id") if isinstance(item, dict) else None for item in items]
        if any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != len(ids):
            errors.append(field + " requires unique nonblank string ids")
    if attestation_path is not None:
        try:
            att = json.loads(pathlib.Path(attestation_path).read_text(encoding="utf-8"),
                             object_pairs_hook=reject_duplicate_keys,
                             parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
            if not isinstance(att, dict):
                raise ValueError("attestation must be an object")
            for key in ("manifest_path", "sha256", "git_commit", "freeze_utc",
                        "canonicalization", "protocol_version"):
                if not att.get(key):
                    errors.append("attestation missing " + key)
            if att.get("sha256") != hashlib.sha256(raw).hexdigest():
                errors.append("attestation digest mismatch")
            if att.get("manifest_path") != str(manifest_path):
                errors.append("attestation manifest_path mismatch")
        except (ValueError, OSError) as exc:
            errors.append("invalid attestation: " + str(exc))
    return errors


def main(argv):
    strict = len(argv) > 1 and argv[1] == "--require-attestation"
    if strict:
        argv = [argv[0]] + argv[2:]
    if len(argv) not in (2, 3) or (strict and len(argv) != 3):
        print(__doc__.strip())
        return 2
    try:
        errors = validate(argv[1], argv[2] if len(argv) == 3 else None, require_attestation=strict)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print("FAIL:", exc)
        return 1
    for err in errors:
        print("FAIL:", err)
    if errors:
        return 1
    print("PASS: structural and digest checks only; no temporal freeze or scientific validity attested")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
