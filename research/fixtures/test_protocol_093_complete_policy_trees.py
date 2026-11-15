"""Protocol 093: independent complete contingent-policy enumeration.
Standard-library-only, exact arithmetic. Not executed at publication.
Run only on verified zero-cost cloud compute, never on the user's laptop.
Unlike Protocols 089/090, this enumerates and scores full trees; no Bellman max.
"""
from fractions import Fraction as F
from itertools import product
import unittest

STOP = ("stop",)

class Intractable(Exception):
    pass

def certify(costs, budget, worlds, cap=100000):
    """Return (best_value, best_tree, tree_count); worlds maps bit tuples to masses."""
    if type(budget) is not int or budget < 0 or type(cap) is not int or cap < 1:
        raise ValueError("invalid budget/cap")
    if not isinstance(costs, (tuple, list)) or not costs or any(
            type(c) is not int or c <= 0 for c in costs):
        raise ValueError("invalid costs")
    n = len(costs)
    if not isinstance(worlds, dict) or set(worlds) != set(product((0, 1), repeat=n)):
        raise ValueError("must supply every possible world")
    if any(type(p) not in (int, F) or p < 0 for p in worlds.values()) or sum(
            map(F, worlds.values()), F(0)) != 1:
        raise ValueError("invalid probability mass")
    count = [0]
    def trees(remaining, b):
        count[0] += 1
        if count[0] > cap:
            raise Intractable("tree generation cap exceeded")
        yield STOP
        for i in remaining:
            if costs[i] > b:
                continue
            rest = tuple(j for j in remaining if j != i)
            # Materialize each continuation set, then use the structural product.
            left = tuple(trees(rest, b-costs[i]))
            right = tuple(trees(rest, b-costs[i]))
            for no, yes in product(left, right):
                count[0] += 1
                if count[0] > cap:
                    raise Intractable("tree generation cap exceeded")
                yield (i, no, yes)
    def reward(tree, world):
        total = 0
        while tree != STOP:
            i, no, yes = tree
            total += world[i]
            tree = yes if world[i] else no
        return total
    best, witness, ntrees = F(-1), None, 0
    for tree in trees(tuple(range(n)), budget):
        ntrees += 1
        score = sum((F(mass)*reward(tree, world) for world, mass in worlds.items()), F(0))
        if score > best:
            best, witness = score, tree
    return best, witness, ntrees

def latent_worlds(conditional, prior):
    """Convert conditionally independent binary outcomes to a joint table."""
    n = len(conditional)
    return {x: sum((F(prior[z]) * product_prob(x, conditional, z)
                    for z in range(len(prior))), F(0))
            for x in product((0, 1), repeat=n)}

def product_prob(x, conditional, z):
    out = F(1)
    for i, bit in enumerate(x):
        p = F(conditional[i][z])
        out *= p if bit else 1-p
    return out

class Protocol093(unittest.TestCase):
    def test_correlated_policy_witness(self):
        worlds = latent_worlds(((1,0),(1,0),(0,1)), (F(1,2), F(1,2)))
        best, tree, count = certify((1,1,1), 2, worlds)
        self.assertEqual(best, F(3,2))
        self.assertIsNotNone(tree)
        self.assertGreater(count, 1)

    def test_independent_and_budget(self):
        worlds = latent_worlds(((F(1,4),F(1,4)),(F(3,4),F(3,4))),
                               (F(1,2),F(1,2)))
        self.assertEqual(certify((1,1),1,worlds)[0], F(3,4))
        self.assertEqual(certify((1,1),2,worlds)[0], F(1))
        self.assertEqual(certify((2,2),1,worlds)[0], F(0))

    def test_asymmetric_mutation_guard(self):
        worlds = {(0,): F(3,4), (1,): F(1,4)}
        self.assertEqual(certify((1,),1,worlds)[0], F(1,4))

    def test_cap_is_explicit(self):
        worlds = {(0,): F(1,2), (1,): F(1,2)}
        with self.assertRaises(Intractable):
            certify((1,),1,worlds,cap=1)

    def test_bad_mass(self):
        with self.assertRaises(ValueError):
            certify((1,),1,{(0,):F(1,4),(1,):F(1,4)})

if __name__ == "__main__":
    unittest.main()
