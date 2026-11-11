"""Protocol 191: independently check fixed-margin provenance certificates.

Pure standard-library verifier. Not an adjudicator, solver, or executed test.
Inputs are explicit registered vertices and edges; no implicit coercions.
"""
from collections import Counter


class CertificateError(ValueError):
    pass


def _identifiers(values, name):
    if not isinstance(values, list) or any(type(x) is not str or not x for x in values):
        raise CertificateError(f"{name}: expected nonempty string identifiers")
    if len(values) != len(set(values)):
        raise CertificateError(f"{name}: duplicate identifiers")
    return set(values)


def _edges(values, sources, targets, name):
    if not isinstance(values, list):
        raise CertificateError(f"{name}: expected edge list")
    result = set()
    for edge in values:
        if (not isinstance(edge, list) or len(edge) != 2
                or type(edge[0]) is not str or type(edge[1]) is not str
                or edge[0] not in sources or edge[1] not in targets):
            raise CertificateError(f"{name}: invalid edge")
        pair = tuple(edge)
        if pair in result:
            raise CertificateError(f"{name}: duplicate edge")
        result.add(pair)
    return result


def _setup(document):
    if not isinstance(document, dict):
        raise CertificateError("document must be an object")
    s = _identifiers(document.get("sources"), "sources")
    t = _identifiers(document.get("targets"), "targets")
    if s & t:
        raise CertificateError("source and target namespaces overlap")
    u = _edges(document.get("permitted"), s, t, "permitted")
    a = _edges(document.get("admissible"), s, t, "admissible")
    e0 = _edges(document.get("original"), s, t, "original")
    if not a <= u or not e0 <= a:
        raise CertificateError("admissible/permitted/original inclusion failure")
    ds = Counter(x for x, _ in e0)
    dt = Counter(y for _, y in e0)
    return s, t, u, a, e0, ds, dt


def check_positive(document, candidate):
    """Check a positive witness; does not establish semantic correctness."""
    s, t, u, a, e0, ds, dt = _setup(document)
    e1 = _edges(candidate, s, t, "candidate")
    if not e1 <= u or e1 == e0 or not (e1 - a):
        raise CertificateError("not a different, semantically inadmissible permitted graph")
    if Counter(x for x, _ in e1) != ds or Counter(y for _, y in e1) != dt:
        raise CertificateError("degree margins changed")
    return True


def check_negative(document, manifest):
    """Check complete forced-edge exclusions using zero degree or deficient cuts.

    Manifest is a list of {edge:[s,t], reason:'zero_degree'} or
    {edge:[s,t], reason:'cut', X:[source ids], Y:[target ids]}.
    This checks certificates, not the accuracy of independent semantic labels.
    """
    s, t, u, a, e0, ds, dt = _setup(document)
    if not isinstance(manifest, list):
        raise CertificateError("manifest must be a list")
    forbidden = sorted(u - a)
    if len(manifest) != len(forbidden):
        raise CertificateError("incomplete or duplicated manifest")
    for expected, entry in zip(forbidden, manifest):
        if not isinstance(entry, dict) or entry.get("edge") != list(expected):
            raise CertificateError("manifest must enumerate forbidden edges in sorted order")
        left, right = expected
        reason = entry.get("reason")
        if reason == "zero_degree":
            if set(entry) != {"edge", "reason"} or (ds[left] > 0 and dt[right] > 0):
                raise CertificateError("invalid zero-degree exclusion")
            continue
        if reason != "cut" or set(entry) != {"edge", "reason", "X", "Y"}:
            raise CertificateError("unsupported certificate")
        if ds[left] == 0 or dt[right] == 0:
            raise CertificateError("use zero-degree certificate")
        x = _identifiers(entry["X"], "X")
        y = _identifiers(entry["Y"], "Y")
        if not x <= s or not y <= t:
            raise CertificateError("cut includes wrong-stratum vertex")
        residual_s = ds.copy()
        residual_t = dt.copy()
        residual_s[left] -= 1
        residual_t[right] -= 1
        required = len(e0) - 1
        capacity = (sum(residual_s[v] for v in s - x)
                    + sum(1 for p, q in u - {expected} if p in x and q not in y)
                    + sum(residual_t[v] for v in y))
        if capacity >= required:
            raise CertificateError("cut is not deficient")
    return True
