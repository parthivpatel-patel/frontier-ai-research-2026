"""Protocol 095: independent witness validator for Protocol 093.
No optimizer is imported or reused. Standard library only.
Execution is deferred until a verified free cloud runner is available.
"""
from fractions import Fraction
from itertools import product
import unittest

STOP = ("stop",)

def validate_witness(costs, budget, worlds, witness, claimed_value):
    """Validate paths, affordability and expected reward without calling certify."""
    if type(budget) is not int or budget < 0:
        raise ValueError("invalid budget")
    if not isinstance(costs, (tuple, list)) or not costs or any(type(c) is not int or c <= 0 for c in costs):
        raise ValueError("invalid costs")
    if not isinstance(worlds, dict) or set(worlds) != set(product((0, 1), repeat=len(costs))):
        raise ValueError("incomplete joint table")
    if any(type(p) not in (int, Fraction) or p < 0 for p in worlds.values()):
        raise ValueError("invalid masses")
    if sum(map(Fraction, worlds.values()), Fraction(0)) != 1:
        raise ValueError("unnormalized masses")
    if type(claimed_value) not in (int, Fraction):
        raise ValueError("invalid claimed value")

    def check(node, seen, remaining):
        if node == STOP:
            return
        if not isinstance(node, tuple) or len(node) != 3:
            raise ValueError("malformed tree")
        i, no, yes = node
        if type(i) is not int or i < 0 or i >= len(costs) or i in seen:
            raise ValueError("repeated or invalid claim")
        if costs[i] > remaining:
            raise ValueError("unaffordable action")
        check(no, seen | {i}, remaining - costs[i])
        check(yes, seen | {i}, remaining - costs[i])

    check(witness, set(), budget)
    expected = Fraction(0)
    for world, mass in worlds.items():
        node, reward = witness, 0
        while node != STOP:
            i, no, yes = node
            reward += world[i]
            node = yes if world[i] == 1 else no
        expected += Fraction(mass) * reward
    if expected != Fraction(claimed_value):
        raise AssertionError("witness score differs from claimed value")
    return expected

class Protocol095(unittest.TestCase):
    def setUp(self):
        self.worlds = {(0,0): Fraction(1,2), (0,1): Fraction(0),
                       (1,0): Fraction(0), (1,1): Fraction(1,2)}

    def test_valid_contingent_witness(self):
        tree = (0, (1, STOP, STOP), (1, STOP, STOP))
        self.assertEqual(validate_witness((1,1), 2, self.worlds, tree, Fraction(1)), 1)

    def test_repeated_action_rejected(self):
        with self.assertRaises(ValueError):
            validate_witness((1,1), 2, self.worlds, (0, (0,STOP,STOP),STOP), 0)

    def test_unaffordable_branch_rejected(self):
        with self.assertRaises(ValueError):
            validate_witness((2,1), 2, self.worlds, (0,(1,STOP,STOP),STOP), 0)

    def test_wrong_claimed_score_rejected(self):
        with self.assertRaises(AssertionError):
            validate_witness((1,1), 2, self.worlds, (0,STOP,STOP), Fraction(3,4))

    def test_malformed_branch_rejected(self):
        with self.assertRaises(ValueError):
            validate_witness((1,1), 2, self.worlds, (0,STOP,("stop",0)), 0)

    def test_missing_world_rejected(self):
        with self.assertRaises(ValueError):
            validate_witness((1,), 1, {(1,): Fraction(1)}, (0,STOP,STOP), 1)

    def test_boolean_index_rejected(self):
        with self.assertRaises(ValueError):
            validate_witness((1,1), 1, self.worlds, (True,STOP,STOP), 0)

if __name__ == "__main__":
    unittest.main()
