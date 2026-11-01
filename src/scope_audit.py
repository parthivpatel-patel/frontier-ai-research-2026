"""Finite semantic and scope audit fixtures; not a novel algorithm or LLM result."""
from __future__ import annotations
from dataclasses import dataclass
from src.toy_falsification import Case, next_position

@dataclass(frozen=True)
class ThresholdClaim:
    upper: float
    def holds(self, position: float) -> bool:
        return position <= self.upper + 1e-12

def reference(case: Case) -> float:
    return next_position(case, wall=True)

def model_discrepancy(case: Case, *, candidate_has_wall: bool) -> bool:
    return abs(reference(case) - next_position(case, wall=candidate_has_wall)) > 1e-10

def formalization_mismatch(cases: tuple[Case, ...], intended: ThresholdClaim,
                           encoded: ThresholdClaim) -> bool:
    """A finite witness of mismatch, not proof of global equivalence."""
    return any(intended.holds(reference(c)) != encoded.holds(reference(c))
               for c in cases)

def scope_audit(certified: tuple[Case, ...], asserted: tuple[Case, ...],
                claim: ThresholdClaim) -> dict:
    """Finite check, not a global certificate."""
    valid = all(claim.holds(reference(c)) for c in certified)
    uncovered = set(asserted) - set(certified)
    violations = [c for c in uncovered if not claim.holds(reference(c))]
    return {
        "certificate_valid_on_checked_scope": valid,
        "asserted_scope_fully_checked": not uncovered,
        "unsupported_scope_expansion": bool(uncovered),
        "observed_counterexample_outside_scope": bool(violations),
        "uncovered_count": len(uncovered),
        "outside_counterexample_count": len(violations),
        "note": "Finite fixtures only; no theorem, LLM result, or global proof.",
    }

def example_fixtures() -> dict:
    """Hand-constructed witnesses, not performance estimates."""
    right_impact = Case(0.9, 0.2, 0.2)
    no_impact = Case(0.9, 0.2, -0.2)
    intended = ThresholdClaim(0.8)
    encoded = ThresholdClaim(1.0)
    return {
        "model_error_witness": model_discrepancy(right_impact, candidate_has_wall=False),
        "equivalent_model_negative_control": model_discrepancy(right_impact, candidate_has_wall=True),
        "formalization_mismatch_witness": formalization_mismatch((right_impact, no_impact), intended, encoded),
        "matching_formalization_negative_control": formalization_mismatch((right_impact, no_impact), intended, intended),
        "scope": scope_audit((right_impact,), (right_impact, no_impact), intended),
    }
