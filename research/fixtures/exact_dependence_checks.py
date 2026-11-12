"""Exact-rational synthetic checks for Protocols 048–050.

Mathematical fixtures only. No AI model calls, downloads, or experimental claims.
Run on a verified free cloud runner only; do not execute on the user's laptop.
"""
from fractions import Fraction as F
from unittest import TestCase, main


def feasible_joint(m1, m2):
    """Fréchet interval for P(V1=1,V2=1) given Bernoulli marginals."""
    return max(F(0), m1 + m2 - 1), min(m1, m2)


def posterior(pi, a, b):
    """P(Y=1 | V1=V2=1), undefined if the event has zero probability."""
    q = pi * a + (1 - pi) * b
    if q == 0:
        raise ValueError("zero-probability conditioning event")
    return pi * a / q


def bounds_given_q(pi, s1, s2, f1, f2, q):
    """Sharp interval for P(Y=1|++) at fixed prevalence and observed q.

    All inputs must be exact rational probabilities. Requires 0<pi<1, q>0.
    """
    vals = (pi, s1, s2, f1, f2, q)
    if any(not F(0) <= x <= F(1) for x in vals):
        raise ValueError("probability outside [0,1]")
    if not F(0) < pi < F(1) or q <= 0:
        raise ValueError("requires interior prevalence and positive q")
    alo, ahi = feasible_joint(s1, s2)
    blo, bhi = feasible_joint(f1, f2)
    # q = pi*a + (1-pi)*b. Enforce both joint Fréchet intervals.
    lower_a = max(alo, (q - (1 - pi) * bhi) / pi)
    upper_a = min(ahi, (q - (1 - pi) * blo) / pi)
    if lower_a > upper_a:
        raise ValueError("incompatible observed agreement and marginals")
    return pi * lower_a / q, pi * upper_a / q


class ExactSyntheticChecks(TestCase):
    def test_worlds_and_sharp_interval(self):
        pi, q = F(1, 2), F(17, 50)
        a1, b1 = F(3, 5), F(2, 25)
        a2, b2 = F(17, 25), F(0)
        self.assertEqual(pi * a1 + (1 - pi) * b1, q)
        self.assertEqual(pi * a2 + (1 - pi) * b2, q)
        self.assertEqual(posterior(pi, a1, b1), F(15, 17))
        self.assertEqual(posterior(pi, a2, b2), F(1))
        self.assertEqual(bounds_given_q(pi, F(4, 5), F(4, 5),
                                        F(1, 5), F(1, 5), q),
                         (F(15, 17), F(1)))

    def test_independence_not_identified(self):
        pi = F(1, 2)
        a, b = F(16, 25), F(1, 25)
        self.assertEqual(posterior(pi, a, b), F(16, 17))
        self.assertEqual(posterior(pi, F(4, 5), F(1, 5)), F(4, 5))

    def test_infeasible_observation_rejected(self):
        with self.assertRaises(ValueError):
            bounds_given_q(F(1, 2), F(4, 5), F(4, 5),
                           F(1, 5), F(1, 5), F(1, 20))

    def test_zero_conditioning_event_rejected(self):
        with self.assertRaises(ValueError):
            posterior(F(1, 2), F(0), F(0))

    def test_label_shift_formula(self):
        a, b, pi = F(3, 5), F(1, 10), F(2, 5)
        q = pi * a + (1 - pi) * b
        self.assertEqual((q - b) / (a - b), pi)


if __name__ == "__main__":
    main()
