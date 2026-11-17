"""Protocol 132: heterogeneous two-verifier exact-rational falsification fixture.

Synthetic stipulated probabilities only; not empirical AI observations.
Standard library only. Execute on verified zero-charge cloud compute, never laptop.
"""
from fractions import Fraction as Q
from itertools import product
import unittest

CHOICES = tuple(range(12))
POLICIES = tuple(product(CHOICES, repeat=2))
NEVER = tuple(p for p in POLICIES if max(p) < 3)
ALWAYS = tuple(p for p in POLICIES if min(p) >= 3)

def bounds(a, b):
    return max(Q(0), a+b-1), min(a,b)

def table(a, b, q):
    if not bounds(a,b)[0] <= q <= bounds(a,b)[1]:
        raise ValueError("infeasible coupling")
    return (q, a-q, b-q, 1-a-b+q)

def corners(a1,b1,a0,b0):
    return tuple(product(bounds(a1,b1), bounds(a0,b0)))

def decision(choice, y2):
    if choice < 3:
        return choice
    return (choice-3)//3 if y2 == 0 else (choice-3)%3

def loss(act, truth, fa, fr, abst):
    if act == 2:
        return abst
    if act == truth:
        return Q(0)
    return fa if act == 1 else fr

def risk(policy, coupling, a1=Q(3,4), b1=Q(2,3),
         a0=Q(1,3), b0=Q(1,4), prior=Q(2,5), fee=Q(1,20),
         fa=Q(3), fr=Q(1), abst=Q(2,5)):
    result = Q(0)
    for truth, weight, a,b,q in ((1,prior,a1,b1,coupling[0]),
                                  (0,1-prior,a0,b0,coupling[1])):
        cells = table(a,b,q)
        # Outcome order ++, +-, -+, -- ; 0 denotes positive signal.
        for (y1,y2), mass in zip(((0,0),(0,1),(1,0),(1,1)),cells):
            c = policy[y1]
            result += weight*mass*(loss(decision(c,y2),truth,fa,fr,abst)
                                   +(fee if c >= 3 else 0))
    return result

def minimax(policies, **kw):
    cc = corners(kw.get("a1",Q(3,4)),kw.get("b1",Q(2,3)),
                 kw.get("a0",Q(1,3)),kw.get("b0",Q(1,4)))
    return min(max(risk(p,c,**kw) for c in cc) for p in policies)

class Protocol132Tests(unittest.TestCase):
    def test_marginals_and_sharp_endpoints(self):
        for a,b in ((Q(3,4),Q(2,3)),(Q(1,3),Q(1,4))):
            for q in bounds(a,b):
                x = table(a,b,q)
                self.assertEqual(sum(x),1)
                self.assertEqual(x[0]+x[1],a)
                self.assertEqual(x[0]+x[2],b)
                self.assertTrue(all(v >= 0 for v in x))
            with self.assertRaises(ValueError):
                table(a,b,bounds(a,b)[0]-Q(1,100))

    def test_symmetric_reduction_to_129(self):
        # Independent implementation of table/risk; 129 imported only as comparator.
        try:
            from test_protocol_129_sequential_acquisition import risk as oldrisk, corners as oldcorners
        except ImportError:
            from research.fixtures.test_protocol_129_sequential_acquisition import risk as oldrisk, corners as oldcorners
        for sensitivity,specificity in ((Q(4,5),Q(4,5)),(Q(3,4),Q(2,3))):
            for c in oldcorners(sensitivity,specificity):
                for p in POLICIES:
                    kw=dict(a1=sensitivity,b1=sensitivity,
                            a0=1-specificity,b0=1-specificity,
                            prior=Q(1,2),fee=Q(1,20),
                            fa=Q(1),fr=Q(1),abst=Q(1,4))
                    self.assertEqual(risk(p,c,**kw),
                        oldrisk(p,c,prior=Q(1,2),fee=Q(1,20),
                                sensitivity=sensitivity,specificity=specificity))

    def test_acquisition_fee_and_no_peeking(self):
        p=(0,3) # stop on first positive; acquire on first negative
        q=corners(Q(3,4),Q(2,3),Q(1,3),Q(1,4))
        fee=Q(7,20)
        for c in q:
            self.assertEqual(risk(p,c,fee=fee)-risk(p,c,fee=0),
                             fee*(Q(2,5)*(1-Q(3,4))+Q(3,5)*(1-Q(1,3))))
        # Stop-only policies are invariant to second verifier and coupling.
        for p in NEVER:
            vals=[risk(p,c,b1=Q(2,3),b0=Q(1,4)) for c in q]
            self.assertEqual(len(set(vals)),1)

    def test_nesting_zero_fee_and_cost_monotonicity(self):
        for fee in (Q(0),Q(1,20),Q(1,4)):
            kw=dict(fee=fee)
            s=minimax(POLICIES,**kw)
            self.assertLessEqual(s,min(minimax(NEVER,**kw),minimax(ALWAYS,**kw)))
            if fee==0:
                self.assertEqual(s,minimax(ALWAYS,**kw))
        self.assertLessEqual(minimax(POLICIES,fee=Q(0)),
                             minimax(POLICIES,fee=Q(1,4)))

    def test_corners_dominate_interior(self):
        kw=dict()
        cc=corners(Q(3,4),Q(2,3),Q(1,3),Q(1,4))
        for p in POLICIES:
            worst=max(risk(p,c,**kw) for c in cc)
            for w in (Q(1,4),Q(1,2),Q(3,4)):
                interior=tuple((1-w)*lo+w*hi for lo,hi in
                    (bounds(Q(3,4),Q(2,3)),bounds(Q(1,3),Q(1,4))))
                self.assertLessEqual(risk(p,interior,**kw),worst)

if __name__=="__main__":
    unittest.main()
