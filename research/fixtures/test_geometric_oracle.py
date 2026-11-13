"""Independent vertex-oracle tests for Protocol 050 identification bounds.

No AI inference, packages, downloads, or stochastic simulations.
Run only on verified free cloud infrastructure. This file is not evidence of
a completed test run.
"""
from fractions import Fraction as F
from itertools import product
from unittest import TestCase, main
from exact_dependence_checks import bounds_given_q, feasible_joint, posterior


def oracle(pi, s1, s2, f1, f2, q):
    """Enumerate intersections of q=pi*a+(1-pi)*b with rectangle edges.

    This is an independent geometric construction, not a copy of the
    interval-intersection implementation being tested.
    """
    a0, a1 = feasible_joint(s1, s2)
    b0, b1 = feasible_joint(f1, f2)
    candidates = set()
    for a in (a0, a1):
        b = (q - pi*a)/(1-pi)
        if b0 <= b <= b1:
            candidates.add((a,b))
    for b in (b0, b1):
        a = (q - (1-pi)*b)/pi
        if a0 <= a <= a1:
            candidates.add((a,b))
    if not candidates:
        raise ValueError("infeasible q")
    values = [posterior(pi,a,b) for a,b in candidates]
    return min(values), max(values)


class GeometricOracleChecks(TestCase):
    def test_all_small_grid_q_endpoints_and_midpoints(self):
        grid = [F(0), F(1,4), F(1,2), F(3,4), F(1)]
        for pi in (F(1,4), F(1,2), F(3,4)):
            for s1,s2,f1,f2 in product(grid, repeat=4):
                a0,a1 = feasible_joint(s1,s2)
                b0,b1 = feasible_joint(f1,f2)
                q0 = pi*a0+(1-pi)*b0
                q1 = pi*a1+(1-pi)*b1
                for q in (q0, (q0+q1)/2, q1):
                    if q == 0:
                        continue
                    self.assertEqual(
                        bounds_given_q(pi,s1,s2,f1,f2,q),
                        oracle(pi,s1,s2,f1,f2,q))
    def test_reject_outside_feasible_q(self):
        self.assertRaises(ValueError, bounds_given_q,
                          F(1,2), F(1,4), F(1,4),
                          F(1,4), F(1,4), F(3,4))


if __name__ == "__main__":
    main()
