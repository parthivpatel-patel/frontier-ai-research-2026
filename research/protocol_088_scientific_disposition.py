"""Protocol 088: conservative disposition of externally adjudicated scientific claims.

This is a decision-layer reference, NOT a physics solver or independent adjudicator.
Inputs describe evidence status supplied by a separate, audited adjudication process.
"""
from dataclasses import dataclass
from enum import Enum


class Disposition(str, Enum):
    SUPPORTED = "supported"
    REFUTED = "refuted"
    UNDERDETERMINED = "underdetermined"
    OUTSIDE_SCOPE = "outside_scope"
    CONFLICT = "conflict"


class Applicability(str, Enum):
    APPLICABLE = "applicable"
    INAPPLICABLE = "inapplicable"
    UNKNOWN = "unknown"


class EvidenceState(str, Enum):
    ALL_SUPPORT = "all_support"
    ALL_REFUTE = "all_refute"
    MIXED = "mixed"
    EMPTY = "empty"
    UNASSESSED = "unassessed"


@dataclass(frozen=True)
class Decision:
    disposition: Disposition
    reason: str


def classify(applicability: Applicability, evidence: EvidenceState) -> Decision:
    """Apply a fixed priority: contradictory evidence, scope, then entailment.

    EMPTY means admitted constraints have no jointly feasible world, not merely
    that no observations were collected. UNASSESSED means truth was not checked.
    """
    if not isinstance(applicability, Applicability) or not isinstance(evidence, EvidenceState):
        raise TypeError("typed applicability and evidence state required")
    if evidence is EvidenceState.EMPTY:
        return Decision(Disposition.CONFLICT, "inconsistent_admitted_evidence")
    if applicability is Applicability.INAPPLICABLE:
        return Decision(Disposition.OUTSIDE_SCOPE, "declared_model_inapplicable")
    if applicability is Applicability.UNKNOWN:
        return Decision(Disposition.UNDERDETERMINED, "model_applicability_unresolved")
    if evidence is EvidenceState.UNASSESSED:
        return Decision(Disposition.UNDERDETERMINED, "truth_not_adjudicated")
    return {
        EvidenceState.ALL_SUPPORT: Decision(Disposition.SUPPORTED, "entailed_under_admitted_evidence"),
        EvidenceState.ALL_REFUTE: Decision(Disposition.REFUTED, "negation_entailed_under_admitted_evidence"),
        EvidenceState.MIXED: Decision(Disposition.UNDERDETERMINED, "both_truth_values_feasible"),
    }[evidence]
