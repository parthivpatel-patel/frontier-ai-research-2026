"""Protocol 131: independent finite-resampling oracle.

Pure standard-library enumeration. This is a mathematical reference, not a
population coverage experiment or evidence of physics-model performance.
"""
from collections import Counter
from fractions import Fraction
from itertools import product


def exact_oracle(accepted, contrasts):
    """Enumerate ordered size-n lineage resamples, with replacement.

    accepted[i] is bool; contrasts[i] is an integer for accepted units and
    None otherwise. The statistic is the mean contrast among accepted draws.
    Each lineage has equal selection probability. No production bootstrap
    functions are imported.
    """
    if not accepted or len(accepted) != len(contrasts):
        raise ValueError("nonempty equal-length arrays required")
    if any(type(a) is not bool for a in accepted):
        raise ValueError("acceptance must be boolean")
    if any((type(y) is not int) if a else (y is not None)
           for a, y in zip(accepted, contrasts)):
        raise ValueError("invalid contrasts")
    n = len(accepted)
    counts = Counter()
    for indices in product(range(n), repeat=n):
        ys = [contrasts[i] for i in indices if accepted[i]]
        statistic = Fraction(sum(ys), len(ys)) if ys else None
        counts[statistic] += 1
    total = n ** n
    undefined = Fraction(counts[None], total)
    defined = total - counts[None]
    pmf = {str(value): Fraction(count, defined)
           for value, count in counts.items() if value is not None} if defined else {}
    cdf = {}
    cumulative = Fraction(0)
    for value in sorted(v for v in counts if v is not None):
        cumulative += Fraction(counts[value], defined)
        cdf[str(value)] = cumulative
    return {"total_outcomes": total, "undefined_probability": undefined,
            "defined_outcomes": defined, "conditional_pmf": pmf,
            "conditional_cdf": cdf}


def reference_cases():
    return {
        "one_accepting": exact_oracle((True, False), (1, None)),
        "opposing": exact_oracle((True, True), (-1, 1)),
        "three_lineages": exact_oracle((True, True, False), (-1, 1, None)),
    }
