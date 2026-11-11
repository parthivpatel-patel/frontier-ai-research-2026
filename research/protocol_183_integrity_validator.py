"""Protocol 183 artifact-level integrity gate. Standard library only.

This gate checks paired intervention delivery; it does not measure model accuracy.
Input is an audit JSON document with `assignment` and `pairs`.
Each pair has `correct` and `matched_shuffle` arms with explicit model-visible
`invariant` (structured object) and `links` (list of structured link objects).
`full_input_utf8` must be the actual transmitted text, and must equal the
canonical JSON encoding of {"invariant": ..., "links": ...}. This intentionally
supports only canonical-JSON verifier inputs; other transports must fail closed.
"""
import hashlib
import json
import re
import sys

HEX = re.compile(r"^[0-9a-f]{64}$")
CONDITIONS = ("correct", "matched_shuffle")
ALLOWED_LINK_KEYS = {"source", "target", "type", "scope"}
LEAKAGE_KEYS = {"gold_answer", "gold_label", "condition", "provenance_condition", "verdict"}


def reject_nested_leakage(value):
    """Reject prohibited field names at any depth in model-visible invariant data.

    This is a syntactic safeguard, not a semantic leakage detector: answers
    embedded in ordinary prose remain a separately audited risk.
    """
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise ValueError("non-string invariant key")
            if key.casefold() in LEAKAGE_KEYS:
                raise ValueError("potential nested answer/condition leakage")
            reject_nested_leakage(child)
    elif isinstance(value, list):
        for child in value:
            reject_nested_leakage(child)



def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def strict_json(raw):
    def no_duplicates(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError("duplicate JSON key: " + key)
            obj[key] = value
        return obj
    def no_constants(value):
        raise ValueError("nonfinite JSON constant: " + value)
    return json.loads(raw, object_pairs_hook=no_duplicates,
                      parse_constant=no_constants)


def require_hash(value, name):
    if not isinstance(value, str) or not HEX.fullmatch(value):
        raise ValueError("invalid " + name)


def validate(document):
    if not isinstance(document, dict) or document.get("schema_version") != "183.1":
        raise ValueError("unsupported schema")
    assignment = document.get("assignment")
    pairs = document.get("pairs")
    if not isinstance(assignment, dict) or not isinstance(pairs, list) or not pairs:
        raise ValueError("missing assignment or pairs")
    seen = set()
    for pair in pairs:
        if not isinstance(pair, dict):
            raise ValueError("pair must be an object")
        key = pair.get("item_key")
        if not isinstance(key, str) or not key.strip() or key in seen:
            raise ValueError("duplicate or invalid item key")
        seen.add(key)
        if assignment.get(key) != list(CONDITIONS):
            raise ValueError("assignment manifest mismatch")
        arms = pair.get("arms")
        if not isinstance(arms, dict) or set(arms) != set(CONDITIONS):
            raise ValueError("missing intervention arm")
        skeletons, payloads, fulls = [], [], []
        for condition in CONDITIONS:
            arm = arms[condition]
            if not isinstance(arm, dict):
                raise ValueError("invalid arm")
            invariant, links = arm.get("invariant"), arm.get("links")
            if not isinstance(invariant, dict) or not isinstance(links, list) or not links:
                raise ValueError("invalid invariant or links")
            reject_nested_leakage(invariant)
            allowed_targets = invariant.get("allowed_target_ids")
            if not isinstance(allowed_targets, list) or not allowed_targets:
                raise ValueError("missing allowed target universe")
            allowed_sources = invariant.get("allowed_source_ids")
            def valid_universe(ids):
                return (isinstance(ids, list) and bool(ids)
                        and all(isinstance(x, str) and bool(x.strip()) for x in ids)
                        and len(set(ids)) == len(ids))
            if not valid_universe(allowed_sources) or not valid_universe(allowed_targets):
                raise ValueError("invalid source or target universe")
            if set(allowed_sources) & set(allowed_targets):
                raise ValueError("ambiguous source/target namespace collision")
            for link in links:
                if not isinstance(link, dict) or set(link) != ALLOWED_LINK_KEYS:
                    raise ValueError("invalid link fields")
                if not all(isinstance(link[k], str) and link[k] for k in ALLOWED_LINK_KEYS):
                    raise ValueError("empty link attribute")
                if link["target"] not in allowed_targets or link["source"] not in allowed_sources or link["source"] == link["target"]:
                    raise ValueError("inadmissible target")
            transmitted = arm.get("full_input_utf8")
            if not isinstance(transmitted, str):
                raise ValueError("missing transmitted artifact")
            full_bytes = transmitted.encode("utf-8")
            if full_bytes != canonical({"invariant": invariant, "links": links}):
                raise ValueError("transmitted bytes differ from canonical artifact")
            for field, data in (("invariant_prompt_sha256", canonical(invariant)),
                                ("intervention_payload_sha256", canonical(links)),
                                ("full_input_sha256", full_bytes),
                                ("blinded_input_artifact_sha256", full_bytes)):
                require_hash(arm.get(field), field)
                if arm[field] != digest(data):
                    raise ValueError("hash mismatch: " + field)
            skeletons.append(canonical(invariant))
            payloads.append(canonical(links))
            fulls.append(full_bytes)
        if skeletons[0] != skeletons[1]:
            raise ValueError("non-provenance content differs")
        if payloads[0] == payloads[1] or fulls[0] == fulls[1]:
            raise ValueError("intervention not delivered")
        correct, shuffled = (arms[c]["links"] for c in CONDITIONS)
        def signatures(links):
            return sorted((x["source"], x["type"], x["scope"]) for x in links)
        if signatures(correct) != signatures(shuffled):
            raise ValueError("link type/scope/source mismatch")
        # A shuffle must not change target degree within link type/scope strata.
        def target_strata(links):
            strata = {}
            for link in links:
                stratum = (link["type"], link["scope"])
                strata.setdefault(stratum, []).append(link["target"])
            return {key: sorted(values) for key, values in strata.items()}
        if target_strata(correct) != target_strata(shuffled):
            raise ValueError("target multiset differs within type/scope stratum")
        def unique_edges(links):
            return {(x["source"], x["target"], x["type"], x["scope"])
                    for x in links}
        if len(unique_edges(correct)) != len(correct) or len(unique_edges(shuffled)) != len(shuffled):
            raise ValueError("duplicate provenance link")
        # Reordering JSON list entries is not a changed provenance graph.
        if unique_edges(correct) == unique_edges(shuffled):
            raise ValueError("shuffle changes ordering only, not provenance edges")
    if set(assignment) != seen:
        raise ValueError("unregistered assignment or attrition")
    return {"accepted_pairs": len(pairs), "status": "structural_gate_only"}


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python protocol_183_integrity_validator.py audit.json")
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as handle:
            result = validate(strict_json(handle.read()))
        print(json.dumps(result, sort_keys=True))
    except (ValueError, TypeError, KeyError) as exc:
        print("REJECTED: " + str(exc), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
