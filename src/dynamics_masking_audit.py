"""Audit when stronger physical assumptions hide temporal-formula disagreement.

This is a classical finite-state diagnostic, not a new model checker or
a measure of natural-language correctness. All claims are restricted to the
declared three-state transition systems and infinite-trace LTL.
"""
from __future__ import annotations

from collections import deque
import json

from src.admissible_lasso_audit import Actuator, FLEXIBLE, FIXED
from src.exhaustive_offset_audit import (
    SearchBudgetExceeded, _bad_at_next, _find_cycle, exact_witness,
)


def is_restriction(broad: Actuator, restricted: Actuator) -> bool:
    """Both models have the same initial state and proposition interpretation."""
    return all(set(narrow).issubset(set(wide))
               for wide, narrow in zip(broad.edges, restricted.edges))


def satisfiable_on_model(model: Actuator, offset: int, *,
                         max_nodes: int = 100_000) -> bool:
    """Existence of an infinite admissible trace satisfying G(a -> X^k b).

    Exact via reachable safe-product cycle. False means unrealizable on this
    particular transition system, not universally logically inconsistent.
    Budget exhaustion raises; it is never interpreted as unsatisfiability.
    """
    if isinstance(offset, bool) or not isinstance(offset, int) or not 1 <= offset <= 6:
        raise ValueError("offset must be an integer in [1,6]")
    if isinstance(max_nodes, bool) or not isinstance(max_nodes, int) or max_nodes < 1:
        raise ValueError("max_nodes must be a positive integer")
    start = ((0,), True)
    seen = {start}
    queue = deque([start])
    graph = {}
    while queue:
        vertex = queue.popleft()
        history = vertex[0]
        next_vertices = []
        for state in model.edges[history[-1]]:
            if _bad_at_next(history, state, offset):
                continue
            successor = ((history + (state,))[-(offset + 1):], True)
            next_vertices.append(successor)
            if successor not in seen:
                if len(seen) >= max_nodes:
                    raise SearchBudgetExceeded("incomplete satisfiability search")
                seen.add(successor)
                queue.append(successor)
        graph[vertex] = tuple(next_vertices)
    return _find_cycle(graph) is not None


def compare_models(broad: Actuator, restricted: Actuator,
                   offsets: tuple[int, ...] = (1, 2, 4, 6)) -> dict[str, object]:
    """Compare witness existence under nested physical dynamics.

    A separating trace under restricted dynamics must also be allowed by the
    broad model. The converse need not hold. Disappearance is NOT evidence
    that the two English requirements have the same intended meaning.
    """
    if not is_restriction(broad, restricted):
        raise ValueError("physical models are not nested under edge inclusion")
    if not offsets or len(set(offsets)) != len(offsets) or any(
        isinstance(n, bool) or not isinstance(n, int)
        or n not in (1, 2, 4, 6) for n in offsets
    ):
        raise ValueError("offsets must be distinct members of {1,2,4,6}")
    comparisons = []
    for n in offsets:
        satisfiable = {
            "source_broad": satisfiable_on_model(broad, 3),
            "changed_broad": satisfiable_on_model(broad, n),
            "source_restricted": satisfiable_on_model(restricted, 3),
            "changed_restricted": satisfiable_on_model(restricted, n),
        }
        for direction, required, violated in (
            ("source_true_changed_false", 3, n),
            ("changed_true_source_false", n, 3),
        ):
            wide = exact_witness(broad, required, violated).witness
            narrow = exact_witness(restricted, required, violated).witness
            if narrow is not None and (wide is None or not narrow.valid(broad)):
                raise AssertionError("violated monotonicity under model restriction")
            comparisons.append({
                "changed_offset": n,
                "direction": direction,
                "broad_witness_exists": wide is not None,
                "restricted_witness_exists": narrow is not None,
                "masked_by_restriction": wide is not None and narrow is None,
                "required_formula_unrealizable_on_broad": not satisfiable[
                    "source_broad" if required == 3 else "changed_broad"],
                "required_formula_unrealizable_on_restricted": not satisfiable[
                    "source_restricted" if required == 3 else "changed_restricted"],
            })
    return {
        "status": "EXACT_TOY_DYNAMICS_MASKING_AUDIT",
        "broad_model": broad.name,
        "restricted_model": restricted.name,
        "nested_dynamics": True,
        "comparisons": comparisons,
        "masked_directions": sum(x["masked_by_restriction"] for x in comparisons),
        "source_requirements": 1,
        "independent_model_predictions": 0,
        "publication_ready": False,
        "interpretation": (
            "Missing separating witnesses after restricting physical behavior "
            "can mask formal differences; it never proves language faithfulness."
        ),
    }


def audit() -> dict[str, object]:
    return compare_models(FLEXIBLE, FIXED)


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
