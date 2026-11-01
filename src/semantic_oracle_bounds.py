"""Exact, deterministic audit of ambiguity in a supplied semantic oracle.

This is a diagnostic baseline, not a novel estimator, learned language parser,
or a conformal/generalization guarantee. Candidate intended meanings are
supplied by the experiment designer, not inferred from natural language.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from src.exact_domain_audit import Domain, threshold_disagreement


@dataclass(frozen=True)
class OracleCase:
    """A candidate formalization and a nonempty set of plausible references."""

    domain: Domain
    candidate_upper: Fraction
    reference_uppers: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if not self.reference_uppers:
            raise ValueError("reference set must be nonempty")
        if not isinstance(self.candidate_upper, Fraction):
            raise TypeError("candidate_upper must be an exact Fraction")
        if any(not isinstance(x, Fraction) for x in self.reference_uppers):
            raise TypeError("reference_uppers must contain exact Fractions")

    def possible_errors(self) -> frozenset[int]:
        """0 = equivalent, 1 = mismatch on at least one state in the box."""
        return frozenset(
            int(threshold_disagreement(self.domain, self.candidate_upper, ref))
            for ref in self.reference_uppers
        )


def sample_error_bounds(cases: Iterable[OracleCase]) -> dict[str, object]:
    """Exact bounds over the supplied cases and their reference candidate sets.

    These are bounds on the observed finite sample, not distribution-free
    guarantees for new instructions or real-world systems. The maximum remains
    conservative if references are constrained jointly across cases.
    """
    selected = tuple(cases)
    if not selected:
        raise ValueError("at least one accepted case is required")
    sets = tuple(case.possible_errors() for case in selected)
    n = len(sets)
    certain = sum(errors == frozenset({1}) for errors in sets)
    possible = sum(1 in errors for errors in sets)
    return {
        "accepted_cases": n,
        "certain_errors": certain,
        "possible_errors": possible,
        "ambiguous_cases": sum(errors == frozenset({0, 1}) for errors in sets),
        "lower_error_rate": Fraction(certain, n),
        "upper_error_rate": Fraction(possible, n),
        "guarantee_scope": "Finite sample and supplied semantic candidates only",
    }


def sample_risk_decision(cases: Iterable[OracleCase], maximum_error_rate: Fraction) -> str:
    """Three-way diagnostic; not a statistical deployment certificate."""
    if not isinstance(maximum_error_rate, Fraction) or not 0 <= maximum_error_rate <= 1:
        raise ValueError("maximum_error_rate must be an exact Fraction in [0,1]")
    bounds = sample_error_bounds(cases)
    lower = bounds["lower_error_rate"]
    upper = bounds["upper_error_rate"]
    if upper <= maximum_error_rate:
        return "passes_for_every_supplied_interpretation"
    if lower > maximum_error_rate:
        return "fails_for_every_supplied_interpretation"
    return "depends_on_unresolved_interpretation"


def joint_error_bounds(accepted_cases: Iterable[OracleCase],
                       total_instructions: int) -> dict[str, object]:
    """Finite-sample accepted-error bounds with ALL instructions in denominator.

    Matches the *definition* of joint risk in selective prediction, not its
    population-level conformal guarantee. Rejected instructions count zero.
    """
    accepted = tuple(accepted_cases)
    if (isinstance(total_instructions, bool)
            or not isinstance(total_instructions, int)
            or total_instructions < 1
            or len(accepted) > total_instructions):
        raise ValueError("total_instructions must be >=1 and >= accepted count")
    error_sets = tuple(case.possible_errors() for case in accepted)
    return {
        "total_instructions": total_instructions,
        "accepted_cases": len(accepted),
        "lower_joint_error_rate": Fraction(sum(s == frozenset({1}) for s in error_sets),
                                           total_instructions),
        "upper_joint_error_rate": Fraction(sum(1 in s for s in error_sets),
                                           total_instructions),
        "guarantee_scope": "Finite sample and supplied semantic candidates only",
    }
