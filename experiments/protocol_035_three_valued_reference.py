"""Protocol 035: bounded three-valued safety adjudication.

Constructed standard-library reference, not an empirical AI result.
Run from repository root: python -m unittest discover -s experiments -p 'test_protocol_035*.py'
"""
from itertools import product

EDGES = {0: (0, 1), 1: (1, 2), 2: (2,)}


def enumerate_traces(edges, start, steps):
    traces = {(start,)}
    for _ in range(steps):
        traces = {trace + (successor,) for trace in traces
                  for successor in edges[trace[-1]]}
    return traces


def independently_valid(trace):
    return bool(trace) and trace[0] == 0 and all(
        b in EDGES[a] for a, b in zip(trace, trace[1:]))


def adjudicate(abstract_traces, physical_traces, property_holds,
               soundness_established):
    """Return (status, witness) for a universal finite-trace property.

    Abstract safety alone is insufficient if trace inclusion is unproven.
    A physical counterexample is sufficient to falsify even without
    abstraction soundness. Spurious abstract violations are inconclusive.
    """
    for trace in sorted(physical_traces):
        if independently_valid(trace) and not property_holds(trace):
            return "falsified", trace
    if soundness_established and all(property_holds(t) for t in abstract_traces):
        return "verified_bounded", None
    return "inconclusive", None


def reference_cases():
    physical = enumerate_traces(EDGES, 0, 2)
    projected = {tuple(x >= 1 for x in trace) for trace in physical}
    boolean = enumerate_traces({False: (False, True),
                                True: (False, True)}, False, 2)
    return physical, projected, boolean
