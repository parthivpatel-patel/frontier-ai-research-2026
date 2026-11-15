"""Protocol 090: independent possible-world policy enumeration for Protocol 089.
Synthetic exact arithmetic; no model evaluation. Execute only on verified free cloud.
"""
from fractions import Fraction as F
from itertools import product, permutations
from functools import lru_cache
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("protocol089", Path(__file__).with_name("test_protocol_089_adaptive_oracle.py"))
p089 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p089)

def enumerate_worlds(conditional, prior):
    """Return exact joint probabilities of all binary adjudication outcomes."""
    n = len(conditional)
    worlds = {}
    for bits in product((0, 1), repeat=n):
        mass = F(0)
        for z, weight in enumerate(prior):
            term = F(weight)
            for i, bit in enumerate(bits):
                probability = F(conditional[i][z])
                term *= probability if bit else 1-probability
            mass += term
        if mass:
            worlds[bits] = mass
    assert sum(worlds.values(), F(0)) == 1
    return worlds

def exhaustive_policy_value(costs, conditional, prior, budget):
    """Enumerate first actions and outcome-contingent continuations on joint worlds.

    Does not call Protocol 089's posterior update or Bellman implementation.
    Each observation filters the possible-world distribution directly.
    """
    worlds = enumerate_worlds(conditional, prior)
    n = len(costs)
    @lru_cache(None)
    def solve(remaining, funds, history):
        compatible = {bits: mass for bits, mass in worlds.items()
                      if all(bits[i] == outcome for i, outcome in history)}
        total = sum(compatible.values(), F(0))
        if not total:
            return F(0)
        best = F(0)  # stopping is always permitted
        for i in remaining:
            if costs[i] > funds:
                continue
            future = tuple(j for j in remaining if j != i)
            value = F(0)
            for outcome in (0, 1):
                branch_mass = sum((mass for bits, mass in compatible.items()
                                   if bits[i] == outcome), F(0))
                if branch_mass:
                    next_history = tuple(sorted(history + ((i, outcome),)))
                    value += branch_mass / total * (
                        F(outcome) + solve(future, funds-costs[i], next_history))
            best = max(best, value)
        return best
    return solve(tuple(range(n)), budget, ())

class Protocol090(unittest.TestCase):
    def test_correlated_world_enumeration(self):
        costs=(1,1,1)
        conditional=((1,0),(1,0),(0,1))
        prior=(F(1,2),F(1,2))
        self.assertEqual(exhaustive_policy_value(costs,conditional,prior,2),F(3,2))
        self.assertEqual(exhaustive_policy_value(costs,conditional,prior,2),
                         p089.oracle(costs,conditional,prior,2))

    def test_exhaustive_small_rational_grid(self):
        values=(F(0),F(1,2),F(1))
        # 3 claims, two latent states; exact 729 conditional tables
        for flat in product(values, repeat=6):
            conditional=tuple(tuple(flat[2*i:2*i+2]) for i in range(3))
            for costs,budget in (((1,1,1),2),((1,2,1),2)):
                expected=exhaustive_policy_value(costs,conditional,(F(1,3),F(2,3)),budget)
                actual=p089.oracle(costs,conditional,(F(1,3),F(2,3)),budget)
                self.assertEqual(actual,expected)

    def test_permutation_invariance(self):
        costs=(1,2,1)
        conditional=((F(1,4),F(3,4)),(1,0),(0,1))
        prior=(F(1,3),F(2,3))
        expected=exhaustive_policy_value(costs,conditional,prior,3)
        for order in permutations(range(3)):
            reordered_costs=tuple(costs[i] for i in order)
            reordered_probs=tuple(conditional[i] for i in order)
            self.assertEqual(exhaustive_policy_value(reordered_costs,reordered_probs,prior,3),expected)
            self.assertEqual(p089.oracle(reordered_costs,reordered_probs,prior,3),expected)

    def test_independent_control(self):
        costs=(2,1,1)
        conditional=((F(1,2),F(1,2)),(F(2,3),F(2,3)),(F(1,4),F(1,4)))
        prior=(F(1,4),F(3,4))
        expected=p089.static_optimum(costs,conditional,prior,2)
        self.assertEqual(exhaustive_policy_value(costs,conditional,prior,2),expected)

    def test_zero_mass_worlds(self):
        conditional=((1,0),(1,0))
        worlds=enumerate_worlds(conditional,(F(1,2),F(1,2)))
        self.assertEqual(len(worlds),2)
        self.assertEqual(exhaustive_policy_value((1,1),conditional,(F(1,2),F(1,2)),2),F(1))

if __name__ == "__main__":
    unittest.main()
