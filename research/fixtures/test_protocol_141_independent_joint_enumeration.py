"""Protocol 141: independent joint-state enumeration and prevalence stress test.

Synthetic exact-rational regression. No model inference or empirical claims.
Execute only on an account-verified zero-charge cloud runner.
"""
import unittest
from fractions import Fraction as F
from itertools import product

STATES = tuple(product((0, 1), repeat=3))  # (truth, verifier1, verifier2)

def independent_enumeration(t0, t1, prevalence):
    """Construct P(Y,V1,V2) directly, without importing Protocol 140 risk."""
    if not F(0) <= prevalence <= F(1):
        raise ValueError("prevalence")
    if any(not F(0) <= t <= F(1,2) for t in (t0,t1)):
        raise ValueError("coupling")
    total = F(0)
    mass = F(0)
    for y,v1,v2 in STATES:
        py = prevalence if y else (1-prevalence)
        t = t1 if y else t0
        pv = t if v1 == v2 else F(1,2)-t
        joint = py*pv
        mass += joint
        accept = (v1 == 1 and v2 == 1)
        loss = (F(0) if y else F(2)) if accept else F(1)
        total += joint*loss
    assert mass == 1
    return total

class Protocol141Tests(unittest.TestCase):
    def test_independent_enumeration_on_grid(self):
        from test_protocol_140_coupled_uncertainty import risk
        grid = [F(0), F(1,8), F(1,4), F(3,8), F(1,2)]
        for p,a,b in product((F(0),F(1,4),F(1,2),F(3,4),F(1)),grid,grid):
            self.assertEqual(independent_enumeration(a,b,p), risk(a,b,p))

    def test_prevalence_breaks_constant_diagonal_risk(self):
        # R(t,t;p)=1+(1-2p)t; only constant at p=1/2.
        for p in (F(1,4),F(3,4)):
            self.assertNotEqual(independent_enumeration(F(0),F(0),p),
                                independent_enumeration(F(1,2),F(1,2),p))
        self.assertEqual(independent_enumeration(F(1,2),F(1,2),F(1,4)),F(5,4))
        self.assertEqual(independent_enumeration(F(1,2),F(1,2),F(3,4)),F(3,4))

    def test_joint_prevalence_coupling_extremes(self):
        # p in [1/4,3/4], t0=t1=t in [0,1/2].
        # Maximum = 5/4, minimum = 3/4, both attainable.
        values=[independent_enumeration(t,t,p)
                for t,p in product((F(0),F(1,2)),(F(1,4),F(3,4)))]
        self.assertEqual(max(values),F(5,4))
        self.assertEqual(min(values),F(3,4))

    def test_invalid_joint_parameters(self):
        for a,b,p in ((F(-1,8),F(0),F(1,2)),
                      (F(0),F(5,8),F(1,2)),
                      (F(0),F(0),F(-1,8))):
            with self.assertRaises(ValueError):
                independent_enumeration(a,b,p)

if __name__ == "__main__":
    unittest.main()
