"""Protocol 134: independent adversarial risk oracle for heterogeneous verification.

Synthetic exact-rational fixtures, not empirical AI observations.
Run only on verified no-charge cloud compute; never on the user's laptop.
"""
import unittest
from fractions import Fraction as F
from itertools import product
try:
    from test_protocol_132_heterogeneous_sequential import risk, corners, POLICIES, bounds
except ImportError:
    from research.fixtures.test_protocol_132_heterogeneous_sequential import risk, corners, POLICIES, bounds

A1,B1,A0,B0=F(3,4),F(2,3),F(1,3),F(1,4)
PRIOR,FEE,FA,FR,ABST=F(2,5),F(1,20),F(3),F(1),F(2,5)

def independent_risk(policy, q_true, q_false):
    total=F(0)
    for truth,prior,p_first,p_second,q in (
        (1,PRIOR,A1,B1,q_true),(0,1-PRIOR,A0,B0,q_false)):
        joint={(0,0):q,(0,1):p_first-q,
               (1,0):p_second-q,(1,1):1-p_first-p_second+q}
        for (first,second),conditional_mass in joint.items():
            choice=policy[first]
            if choice in (0,1,2):
                action=choice
                acquisition=F(0)
            else:
                offset=choice-3
                action=(offset//3,offset%3)[second]
                acquisition=FEE
            error=ABST if action==2 else (
                F(0) if action==truth else (FA if action==1 else FR))
            total+=prior*conditional_mass*(error+acquisition)
    return total

class Protocol134Tests(unittest.TestCase):
    def test_independent_oracle_all_policies_and_grid(self):
        lo1,hi1=bounds(A1,B1)
        lo0,hi0=bounds(A0,B0)
        weights=(F(0),F(1,4),F(1,2),F(3,4),F(1))
        for w1,w0 in product(weights,repeat=2):
            q1=lo1+(hi1-lo1)*w1
            q0=lo0+(hi0-lo0)*w0
            for policy in POLICIES:
                self.assertEqual(
                    risk(policy,(q1,q0)),
                    independent_risk(policy,q1,q0))

    def test_all_corners_bound_independent_interior_grid(self):
        lo1,hi1=bounds(A1,B1)
        lo0,hi0=bounds(A0,B0)
        weights=(F(0),F(1,4),F(1,2),F(3,4),F(1))
        for policy in POLICIES:
            corner_worst=max(independent_risk(policy,*c) for c in
                             product((lo1,hi1),(lo0,hi0)))
            for w1,w0 in product(weights,repeat=2):
                self.assertLessEqual(
                    independent_risk(policy,
                        lo1+(hi1-lo1)*w1,lo0+(hi0-lo0)*w0),
                    corner_worst)

    def test_off_diagonal_corners_explicit(self):
        cc=set(corners(A1,B1,A0,B0))
        self.assertEqual(cc,set(product(bounds(A1,B1),bounds(A0,B0))))
        self.assertIn((bounds(A1,B1)[0],bounds(A0,B0)[1]),cc)
        self.assertIn((bounds(A1,B1)[1],bounds(A0,B0)[0]),cc)

if __name__=="__main__":
    unittest.main()
