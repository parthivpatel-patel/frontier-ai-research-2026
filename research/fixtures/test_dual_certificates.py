"""Exact-rational independent dual and primal certificates for Protocol 054.

Not an empirical AI benchmark. Run only on account-verified free cloud infrastructure.
"""
from fractions import Fraction as F
import unittest


def dual_value(L, U, a, b, c):
    vals = (L, U, a, b, c)
    if not all(isinstance(v, F) for v in vals):
        raise TypeError("Use exact fractions")
    if not (F(0) <= L <= U <= F(1) and a > 0 and b > 0 and c >= 0):
        raise ValueError("Invalid interval or costs")
    candidates = {L, U}
    candidates.update(p for p in (a / (a + b), 1 - c / a, c / b)
                      if L <= p <= U)
    scores = {p: min(a * (1 - p), b * p, c) for p in candidates}
    optimum = max(scores.values())
    return optimum, tuple(sorted(p for p, v in scores.items() if v == optimum))


def endpoint_risks(L, U, a, b, c, q):
    if len(q) != 3 or any(not isinstance(x, F) for x in q):
        raise TypeError("Policy must be three exact fractions")
    if any(x < 0 for x in q) or sum(q) != 1:
        raise ValueError("Policy must lie in the simplex")
    return tuple(q[0] * a * (1 - p) + q[1] * b * p + q[2] * c
                 for p in (L, U))


def certify(L, U, a, b, c, q):
    value, witnesses = dual_value(L, U, a, b, c)
    risks = endpoint_risks(L, U, a, b, c, q)
    return max(risks) == value, value, witnesses, risks


class DualCertificateTests(unittest.TestCase):
    def test_randomized_gap(self):
        args = (F(3, 4), F(1), F(4), F(1), F(2))
        self.assertEqual(dual_value(*args)[0], F(4, 5))
        self.assertEqual(certify(*args, (F(1, 5), F(4, 5), F(0))),
                         (True, F(4, 5), (F(4, 5),),
                          (F(4, 5), F(4, 5))))
        self.assertFalse(certify(*args, (F(1), F(0), F(0)))[0])

    def test_abstention_and_boundaries(self):
        self.assertTrue(certify(F(3, 4), F(1), F(4), F(1), F(1, 5),
                                (F(0), F(0), F(1)))[0])
        self.assertTrue(certify(F(0), F(1), F(1), F(1), F(1),
                                (F(1, 2), F(1, 2), F(0)))[0])
        self.assertTrue(certify(F(1), F(1), F(1), F(1), F(1),
                                (F(1), F(0), F(0)))[0])
        self.assertTrue(certify(F(0), F(1), F(1), F(1), F(0),
                                (F(0), F(0), F(1)))[0])

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            dual_value(F(3, 4), F(1, 2), F(1), F(1), F(1))
        with self.assertRaises(ValueError):
            dual_value(F(0), F(1), F(0), F(1), F(1))
        with self.assertRaises(ValueError):
            endpoint_risks(F(0), F(1), F(1), F(1), F(1),
                           (F(1, 2), F(1, 2), F(1, 2)))
        with self.assertRaises(TypeError):
            dual_value(0.0, F(1), F(1), F(1), F(1))

    def test_dual_lower_bound_on_rational_grid(self):
        grid = [F(i, 4) for i in range(5)]
        policies = [(F(i, 4), F(j, 4), F(4-i-j, 4))
                    for i in range(5) for j in range(5-i)]
        for L in grid:
            for U in grid:
                if U < L:
                    continue
                for c in (F(0), F(1, 4), F(1), F(2)):
                    args = (L, U, F(1), F(2), c)
                    lower, _ = dual_value(*args)
                    for q in policies:
                        self.assertGreaterEqual(max(endpoint_risks(*args, q)), lower)


if __name__ == "__main__":
    unittest.main()
