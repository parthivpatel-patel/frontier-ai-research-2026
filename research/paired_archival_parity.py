"""Exact sharp paired selective-risk bounds under authenticated XOR constraints.

Constraints are supplied by the caller and MUST have independent provenance.
This code does not validate scientific provenance or establish novel mathematics.
"""
from collections import deque
from fractions import Fraction

from research.archival_bounds import paired_difference
from research.paired_archival_oracle import MissingCase


def sharp_paired_difference_parity(a, b, missing, constraints=()):
    """Optimize fixed-denominator paired error difference over parity components.

    Each (i, j, parity) asserts truth[i] XOR truth[j] == parity.
    Contradictions raise ValueError. Endpoints are identification bounds,
    not statistical confidence intervals. Arithmetic uses exact fractions.
    """
    missing = tuple(missing)
    if a.n != b.n or a.m != b.m or len(missing) != a.m:
        raise ValueError("Verified and unresolved sampling frames must agree")
    if any(not isinstance(c, MissingCase) for c in missing):
        raise TypeError("Missing cases must be MissingCase instances")
    m = len(missing)
    graph = [[] for _ in range(m)]
    for edge in constraints:
        if not isinstance(edge, (tuple, list)) or len(edge) != 3:
            raise ValueError("Each constraint must be (i, j, parity)")
        i, j, d = edge
        if any(type(v) is not int for v in (i, j, d)) or not (0 <= i < m and 0 <= j < m and d in (0, 1)):
            raise ValueError("Invalid parity constraint")
        graph[i].append((j, d))
        graph[j].append((i, d))
    components = []
    parity = [None] * m
    for root in range(m):
        if parity[root] is not None:
            continue
        parity[root] = 0
        queue = deque([root])
        group = []
        while queue:
            i = queue.popleft()
            group.append(i)
            for j, d in graph[i]:
                expected = parity[i] ^ d
                if parity[j] is None:
                    parity[j] = expected
                    queue.append(j)
                elif parity[j] != expected:
                    raise ValueError("Infeasible parity constraints")
        components.append(group)
    ka = a.accepted + sum(c.accept_a for c in missing)
    kb = b.accepted + sum(c.accept_b for c in missing)
    conservative = paired_difference(a, b)
    assignments = 2 ** len(components)
    if ka == 0 or kb == 0:
        return {"sharp": None, "conservative": conservative,
                "defined_assignments": 0, "undefined_assignments": assignments}
    base = Fraction(a.errors, ka) - Fraction(b.errors, kb)
    lo = hi = base
    for group in components:
        values = []
        for z in (0, 1):
            contribution = Fraction(0)
            for i in group:
                c = missing[i]
                truth = z ^ parity[i]
                if c.accept_a:
                    contribution += Fraction(int(c.predict_a != truth), ka)
                if c.accept_b:
                    contribution -= Fraction(int(c.predict_b != truth), kb)
            values.append(contribution)
        lo += min(values)
        hi += max(values)
    if conservative is not None and not (conservative[0] <= lo <= hi <= conservative[1]):
        raise AssertionError("Constrained bounds escaped conservative envelope")
    return {"sharp": (lo, hi), "conservative": conservative,
            "defined_assignments": assignments, "undefined_assignments": 0}
