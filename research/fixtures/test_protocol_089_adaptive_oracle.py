"""Protocol 089: finite Bayesian adaptive adjudication oracle.
Synthetic mathematics only; no AI performance claims. Standard library only.
Execute on verified free cloud infrastructure, never on user's laptop.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
import unittest

def oracle(costs, conditional, prior, budget):
    """Return exact optimal expected successes with hidden latent state."""
    if type(budget) is not int or budget < 0:
        raise ValueError("invalid budget")
    if not isinstance(costs, (tuple, list)) or not costs or any(type(c) is not int or c <= 0 for c in costs):
        raise ValueError("invalid costs")
    if not isinstance(prior, (tuple, list)) or not prior or any(type(x) not in (int, F) or x < 0 for x in prior):
        raise ValueError("invalid prior")
    if sum(map(F, prior)) != 1:
        raise ValueError("prior must sum to one")
    if not isinstance(conditional, (tuple, list)) or len(conditional) != len(costs):
        raise ValueError("invalid conditional table")
    if any(not isinstance(row, (tuple, list)) or len(row) != len(prior) or
           any(type(p) not in (int, F) or not 0 <= p <= 1 for p in row) for row in conditional):
        raise ValueError("invalid conditional probability")
    costs = tuple(costs)
    ps = tuple(tuple(map(F, row)) for row in conditional)
    q0 = tuple(map(F, prior))
    @lru_cache(None)
    def value(remaining, b, q):
        best = F(0)
        for i in remaining:
            if costs[i] > b:
                continue
            rest = tuple(j for j in remaining if j != i)
            s = sum((q[z] * ps[i][z] for z in range(len(q))), F(0))
            expected = F(0)
            if s:
                yes = tuple(q[z] * ps[i][z] / s for z in range(len(q)))
                expected += s * (1 + value(rest, b-costs[i], yes))
            if s < 1:
                no = tuple(q[z] * (1-ps[i][z]) / (1-s) for z in range(len(q)))
                expected += (1-s) * value(rest, b-costs[i], no)
            best = max(best, expected)
        return best
    return value(tuple(range(len(costs))), budget, q0)

def static_optimum(costs, conditional, prior, budget):
    probs = [sum((F(prior[z])*F(row[z]) for z in range(len(prior))), F(0)) for row in conditional]
    return max((sum((probs[i] for i in indices), F(0))
                for k in range(len(costs)+1)
                for indices in combinations(range(len(costs)), k)
                if sum(costs[i] for i in indices) <= budget), default=F(0))

class Protocol089(unittest.TestCase):
    def test_correlated_stress(self):
        costs=(1,1,1)
        ps=((1,0),(1,0),(0,1))
        prior=(F(1,2),F(1,2))
        self.assertEqual(static_optimum(costs,ps,prior,2),F(1))
        self.assertEqual(oracle(costs,ps,prior,2),F(3,2))
    def test_independent_equals_static(self):
        for a in (F(0),F(1,2),F(1)):
            for b in (F(0),F(1,3),F(1)):
                ps=((a,a),(b,b),(F(3,4),F(3,4)))
                for costs in ((1,1,1),(2,1,2)):
                    for budget in range(5):
                        self.assertEqual(oracle(costs,ps,(F(1,4),F(3,4)),budget),
                                         static_optimum(costs,ps,(F(1,4),F(3,4)),budget))
    def test_latent_relabeling(self):
        ps=((1,0),(1,0),(0,1))
        self.assertEqual(oracle((1,1,1),ps,(F(1,3),F(2,3)),2),
                         oracle((1,1,1),tuple(tuple(reversed(x)) for x in ps),
                                (F(2,3),F(1,3)),2))
    def test_zero_probability_branches(self):
        self.assertEqual(oracle((1,1),((1,1),(0,0)),(F(1,2),F(1,2)),2),F(1))
    def test_validation(self):
        cases=[((0,),((1,),),(1,),1),((1,),((F(3,2),),),(1,),1),
               ((1,),((1,),),(F(1,2),),1),((1,),((1,),),(1,),True),
               ((1,),((True,),),(1,),1)]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                oracle(*args)

if __name__ == "__main__":
    unittest.main()
