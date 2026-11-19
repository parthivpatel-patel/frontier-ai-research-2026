"""Source-family diagnostics for fixed held-out decisions.

Descriptive only. No statistical confidence, causal, or novelty claims.
Equal-family averages differ from item-weighted pooled estimates when
families have unequal sizes. Undefined within-family risk remains None.
"""
from __future__ import annotations

from src.heldout_selective_risk_accounting import audit_fixed_decisions


def audit_by_family(rows: list[dict], methods: tuple[str, ...]) -> dict:
    """Audit pooled and per-family selective risks without tuning decisions."""
    pooled = audit_fixed_decisions(rows, methods)
    families: dict[str, list[dict]] = {}
    for row in rows:
        families.setdefault(row["family_id"], []).append(row)
    per_family = {
        family: audit_fixed_decisions(family_rows, methods)["methods"]
        for family, family_rows in sorted(families.items())
    }
    macro = {}
    for method in methods:
        coverages = [v[method]["coverage"] for v in per_family.values()]
        risks = [v[method]["selective_risk"] for v in per_family.values()]
        defined = [r for r in risks if r is not None]
        macro[method] = {
            "equal_family_coverage": sum(coverages) / len(coverages),
            "equal_family_risk_defined_only": (
                sum(defined) / len(defined) if defined else None
            ),
            "families_with_defined_risk": len(defined),
            "total_families": len(risks),
        }
    return {"pooled": pooled, "per_family": per_family, "macro": macro}
