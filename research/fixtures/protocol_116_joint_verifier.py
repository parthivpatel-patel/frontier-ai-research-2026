"""Protocol 116: exact two-verifier joint likelihood and decision value.

Analytical reference fixture. Standard library only. No empirical measurements.
Do not execute except in verified no-charge cloud with resource limits.
"""
from fractions import Fraction
from itertools import product

OUTCOMES = ("++", "+-", "-+", "--")


def exact_probability(value):
    if isinstance(value, (float, bool)):
        raise ValueError("exact rational required")
    try:
        result = Fraction(value)
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        raise ValueError("invalid rational") from exc
    if not 0 <= result <= 1:
        raise ValueError("outside probability interval")
    return result


def joint_model(rows):
    """rows[truth] maps each of four outcomes to P(outcome | truth)."""
    if set(rows) != {True, False}:
        raise ValueError("two truth states required")
    normalized = {}
    for truth in (True, False):
        row = rows[truth]
        if set(row) != set(OUTCOMES):
            raise ValueError("all four joint outcomes required")
        normalized[truth] = {key: exact_probability(row[key]) for key in OUTCOMES}
        if sum(normalized[truth].values(), Fraction(0)) != 1:
            raise ValueError("conditional joint distribution not normalized")
    return normalized


def independent_model(sensitivity, specificity):
    se, sp = exact_probability(sensitivity), exact_probability(specificity)
    rows = {}
    for truth in (True, False):
        positive = se if truth else 1-sp
        rows[truth] = {a+b: (positive if a == "+" else 1-positive) *
                             (positive if b == "+" else 1-positive)
                       for a, b in product("+-", repeat=2)}
    return joint_model(rows)


def duplicate_model(sensitivity, specificity):
    se, sp = exact_probability(sensitivity), exact_probability(specificity)
    return joint_model({
        True: {"++": se, "+-": 0, "-+": 0, "--": 1-se},
        False: {"++": 1-sp, "+-": 0, "-+": 0, "--": sp},
    })


def posterior(prior, model, observed):
    p = exact_probability(prior)
    if observed not in OUTCOMES:
        raise ValueError("invalid outcome")
    row = joint_model(model)
    a, b = p * row[True][observed], (1-p) * row[False][observed]
    if a+b == 0:
        return None
    return a/(a+b)


def marginals(model, truth, verifier_index):
    if verifier_index not in (0, 1):
        raise ValueError("verifier index must be 0 or 1")
    row = joint_model(model)[truth]
    return sum((value for outcome, value in row.items()
                if outcome[verifier_index] == "+"), Fraction(0))


def bayes_risk(p, false_accept=1, false_reject=1, abstain=Fraction(1, 4)):
    p = exact_probability(p)
    costs = [Fraction(x) for x in (false_accept, false_reject, abstain)]
    if any(isinstance(x, (bool, float)) for x in (false_accept, false_reject, abstain)):
        raise ValueError("exact losses required")
    if any(x < 0 for x in costs):
        raise ValueError("negative loss")
    return min((1-p)*costs[0], p*costs[1], costs[2])


def expected_risk(prior, model):
    p = exact_probability(prior)
    rows = joint_model(model)
    total = Fraction(0)
    for outcome in OUTCOMES:
        true_mass = p*rows[True][outcome]
        false_mass = (1-p)*rows[False][outcome]
        mass = true_mass+false_mass
        if mass:
            total += mass*bayes_risk(true_mass/mass)
    return total


def first_only_risk(prior, model):
    p = exact_probability(prior)
    rows = joint_model(model)
    total = Fraction(0)
    for first in "+-":
        a = p*sum(rows[True][o] for o in OUTCOMES if o[0] == first)
        b = (1-p)*sum(rows[False][o] for o in OUTCOMES if o[0] == first)
        if a+b:
            total += (a+b)*bayes_risk(a/(a+b))
    return total
