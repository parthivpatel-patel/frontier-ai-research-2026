"""Complete finite-state model check for two bounded-next temporal requirements.

The classical product-state construction proves existence/nonexistence of an
infinite admissible witness for G(a -> X^k b) versus G(a -> X^m b), for a
finite 3-state actuator. This is not a new verification algorithm.

The monitored product stores the last max(k,m)+1 states, tracks whether the
formula to be violated has failed, and discards any path violating the formula
to be preserved. An infinite separating trace exists iff the reachable safe
product graph has a directed cycle after the desired violation. This is exact,
not bounded lasso enumeration. Resource-budget exhaustion raises explicitly.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import json

from src.admissible_lasso_audit import Actuator, FIXED, FLEXIBLE, StateLasso, changed_offsets
from src.independent_source_audit import holds


class SearchBudgetExceeded(RuntimeError):
    """An incomplete search must never be confused with equivalence."""


ProductState = tuple[tuple[int, ...], bool]


@dataclass(frozen=True)
class ExactResult:
    witness: StateLasso | None
    reachable_product_states: int
    complete: bool = True

    def encoded(self) -> dict[str, object]:
        return {
            "witness": self.witness.encoded() if self.witness else None,
            "reachable_product_states": self.reachable_product_states,
            "complete": self.complete,
            "interpretation": (
                "EXACT_NON_EQUIVALENCE" if self.witness
                else "EXACT_NO_SEPARATING_TRACE_ON_THIS_FINITE_MODEL"
            ),
        }


def _bad_at_next(history: tuple[int, ...], next_state: int, offset: int) -> bool:
    # At the new time t+1, the triggering state is x[t+1-offset].
    return (len(history) >= offset and history[-offset] == 0
            and next_state != 2)


def _find_cycle(graph: dict[ProductState, tuple[ProductState, ...]]
                ) -> tuple[ProductState, list[ProductState]] | None:
    """Find a cycle after target failure, using iterative DFS (no recursion)."""
    color: dict[ProductState, int] = {}
    for root in graph:
        if not root[1] or root in color:
            continue
        color[root] = 1
        active: list[ProductState] = [root]
        positions = {root: 0}
        frames = [(root, iter(graph[root]))]
        while frames:
            current, successors = frames[-1]
            try:
                successor = next(successors)
            except StopIteration:
                color[current] = 2
                del positions[current]
                active.pop()
                frames.pop()
                continue
            if not successor[1]:
                continue
            if successor not in color:
                color[successor] = 1
                positions[successor] = len(active)
                active.append(successor)
                frames.append((successor, iter(graph[successor])))
            elif color[successor] == 1:
                return successor, active[positions[successor]:]
    return None


def exact_witness(model: Actuator, required_offset: int,
                  violated_offset: int, *, max_nodes: int = 100_000) -> ExactResult:
    """Complete check for G(a -> X^required b) AND NOT G(a -> X^violated b).

    None means no such infinite trace on the declared finite transition
    system. It does not establish natural-language meaning, correctness on
    other dynamics, or equivalence on unrestricted words.
    """
    if (not isinstance(required_offset, int) or isinstance(required_offset, bool)
            or not isinstance(violated_offset, int) or isinstance(violated_offset, bool)
            or not 1 <= required_offset <= 6 or not 1 <= violated_offset <= 6
            or required_offset == violated_offset):
        raise ValueError("two distinct integer offsets between 1 and 6 required")
    if not isinstance(max_nodes, int) or max_nodes < 1:
        raise ValueError("max_nodes must be a positive integer")
    max_history = max(required_offset, violated_offset) + 1
    start: ProductState = ((0,), False)
    parents: dict[ProductState, ProductState | None] = {start: None}
    graph: dict[ProductState, tuple[ProductState, ...]] = {}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        history, target_bad = current
        next_vertices = []
        for physical_next in model.edges[history[-1]]:
            if _bad_at_next(history, physical_next, required_offset):
                continue
            target_bad_next = target_bad or _bad_at_next(
                history, physical_next, violated_offset)
            next_history = (history + (physical_next,))[-max_history:]
            successor = (next_history, target_bad_next)
            next_vertices.append(successor)
            if successor not in parents:
                if len(parents) >= max_nodes:
                    raise SearchBudgetExceeded(
                        f"incomplete product search: max_nodes={max_nodes}")
                parents[successor] = current
                queue.append(successor)
        graph[current] = tuple(next_vertices)

    cycle = _find_cycle(graph)
    if cycle is None:
        return ExactResult(None, len(parents))
    cycle_start, cycle_vertices = cycle
    path = []
    cursor: ProductState | None = cycle_start
    while cursor is not None:
        path.append(cursor)
        cursor = parents[cursor]
    path.reverse()
    witness = StateLasso(
        tuple(vertex[0][-1] for vertex in path[:-1]),
        tuple(vertex[0][-1] for vertex in cycle_vertices),
    )
    if not witness.valid(model):
        raise AssertionError("internal cycle violates the physical transition system")
    trace = witness.propositions()
    if (not holds("offset", required_offset, trace, inherited_formula=False)
            or holds("offset", violated_offset, trace, inherited_formula=False)):
        raise AssertionError("internal product-state witness fails independent LTL check")
    return ExactResult(witness, len(parents))


def audit() -> dict[str, object]:
    rows = []
    for model in (FLEXIBLE, FIXED):
        for offset in changed_offsets():
            forward = exact_witness(model, 3, offset)
            reverse = exact_witness(model, offset, 3)
            rows.append({
                "model": model.name, "changed_offset": offset,
                "inherited_true_changed_false": forward.encoded(),
                "inherited_false_changed_true": reverse.encoded(),
            })
    return {
        "status": "CLASSICAL_EXACT_FINITE_STATE_TOY_AUDIT",
        "external_originals": 1,
        "independent_model_predictions": 0,
        "method": "reachable product graph + reachable accepting cycle",
        "all_checks_complete": True,
        "comparisons": rows,
        "publication_ready": False,
        "limits": [
            "This is exact only for the two declared three-state transition systems.",
            "The source contains one original instruction, not four independent tasks.",
            "No human-intent oracle or measured model performance is established.",
            "This is classical finite-state safety model checking, not a new theorem.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True, indent=2))
