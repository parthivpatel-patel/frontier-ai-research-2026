"""Protocol 113: exact single-test Bayesian decision value (standard library only).

Analytical fixture calculator, not an empirical verifier. No external dependencies.
Run only on verified no-charge cloud infrastructure with external resource limits.
"""
from fractions import Fraction


def _prob(x):
    if isinstance(x, (bool, float)):
        raise ValueError("probabilities must be exact, not float or bool")
    try:
        p = Fraction(x)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid rational probability") from exc
    if not 0 <= p <= 1:
        raise ValueError("probability outside [0,1]")
    return p


def _loss(x):
    if isinstance(x, (bool, float)):
        raise ValueError("loss must be exact, not float or bool")
    try:
        v = Fraction(x)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid loss") from exc
    if v < 0:
        raise ValueError("loss must be nonnegative")
    return v


def decision_loss(p, false_accept=1, false_reject=1, abstain=Fraction(1, 4)):
    """Bayes risk for ACCEPT, REJECT, ABSTAIN, with p=P(true)."""
    p = _prob(p)
    fa, fr, ab = map(_loss, (false_accept, false_reject, abstain))
    return min((1-p)*fa, p*fr, ab)


def evaluate(prior, sensitivity, specificity, cost=0, *,
             false_accept=1, false_reject=1, abstain=Fraction(1, 4)):
    """Exact expected Bayes-risk reduction for one binary noisy observation.

    Return prior risk, posterior risks and probabilities for possible outcomes,
    gross/net value, and whether purchasing the test strictly improves risk.
    Zero-mass observations are omitted rather than conditioned upon.
    """
    p, se, sp = map(_prob, (prior, sensitivity, specificity))
    c = _loss(cost)
    fa, fr, ab = map(_loss, (false_accept, false_reject, abstain))
    base = decision_loss(p, fa, fr, ab)
    observations = {}
    for label, like_true, like_false in (
        ("positive", se, 1-sp), ("negative", 1-se, sp)
    ):
        joint_true = p * like_true
        joint_false = (1-p) * like_false
        mass = joint_true + joint_false
        if mass == 0:
            continue
        posterior = joint_true / mass
        observations[label] = {
            "probability": mass,
            "posterior_true": posterior,
            "risk": decision_loss(posterior, fa, fr, ab),
        }
    assert sum((v["probability"] for v in observations.values()), Fraction(0)) == 1
    expected = sum((v["probability"] * v["risk"] for v in observations.values()), Fraction(0))
    gross = base - expected
    net = gross - c
    return {"prior_risk": base, "observations": observations,
            "posterior_risk": expected, "gross_value": gross,
            "net_value": net, "buy_test": net > 0}
