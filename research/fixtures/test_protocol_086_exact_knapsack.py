"""Protocol 086: exact, synthetic cost-aware adjudication controls.

Standard-library only. This file is a mathematical fixture, not empirical AI evidence.
No training, inference, external network calls, or random simulation.
Run only on verified zero-cost cloud infrastructure.
"""
from fractions import Fraction
from itertools import combinations, permutations
import unittest


def validate(costs, probabilities, budget):
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if not isinstance(costs, (list, tuple)) or not isinstance(probabilities, (list, tuple)):
        raise ValueError("inputs must be sequences")
    if len(costs) != len(probabilities):
        raise ValueError("length mismatch")
    if len(costs) == 0:
        raise ValueError("at least one claim required")
    for c in costs:
        if type(c) is not int or c <= 0:
            raise ValueError("costs must be positive integers, not booleans")
    for p in probabilities:
        if type(p) not in (int, Fraction) or not 0 <= p <= 1:
            raise ValueError("probabilities must be exact rational values in [0,1]")


def exact_oracle(costs, probabilities, budget):
    validate(costs, probabilities, budget)
    best_value, best_indices = Fraction(0), ()
    n = len(costs)
    for mask in range(1 << n):
        indices = tuple(i for i in range(n) if mask & (1 << i))
        if sum(costs[i] for i in indices) > budget:
            continue
        value = sum((Fraction(probabilities[i]) for i in indices), Fraction(0))
        if value > best_value or (value == best_value and indices < best_indices):
            best_value, best_indices = value, indices
    return best_value, best_indices


def ratio_greedy(costs, probabilities, budget):
    validate(costs, probabilities, budget)
    order = sorted(range(len(costs)), key=lambda i: (-Fraction(probabilities[i], costs[i]), i))
    chosen = []
    remaining = budget
    for i in order:
        if costs[i] <= remaining:
            chosen.append(i)
            remaining -= costs[i]
    return sum((Fraction(probabilities[i]) for i in chosen), Fraction(0)), tuple(chosen)


class Protocol086(unittest.TestCase):
    def test_counterexample(self):
        costs = (6, 5, 5)
        probs = (Fraction(1), Fraction(4, 5), Fraction(4, 5))
        self.assertEqual(ratio_greedy(costs, probs, 10)[0], Fraction(1))
        self.assertEqual(exact_oracle(costs, probs, 10), (Fraction(8, 5), (1, 2)))
        self.assertEqual(Fraction(8, 5) / 3, Fraction(8, 15))

    def test_equal_costs_choose_largest_probabilities(self):
        probs = (Fraction(1, 5), Fraction(3, 4), Fraction(1, 2))
        self.assertEqual(exact_oracle((2, 2, 2), probs, 4)[0], Fraction(5, 4))

    def test_zero_and_certain_success(self):
        self.assertEqual(exact_oracle((1, 1), (Fraction(0), Fraction(1)), 1)[0], Fraction(1))
        self.assertEqual(exact_oracle((1, 1), (Fraction(0), Fraction(0)), 2)[0], Fraction(0))

    def test_zero_budget(self):
        self.assertEqual(exact_oracle((1,), (Fraction(1),), 0), (Fraction(0), ()))

    def test_permutation_invariance(self):
        entries = ((6, Fraction(1)), (5, Fraction(4, 5)), (5, Fraction(4, 5)))
        for perm in set(permutations(entries)):
            costs, probs = zip(*perm)
            self.assertEqual(exact_oracle(costs, probs, 10)[0], Fraction(8, 5))

    def test_oracle_dominates_greedy_small_instances(self):
        for costs in ((1, 2, 3), (3, 2, 2), (2, 2, 2)):
            for probs in ((Fraction(0), Fraction(1, 2), Fraction(1)),
                          (Fraction(1), Fraction(1, 4), Fraction(3, 4))):
                for budget in range(8):
                    self.assertGreaterEqual(exact_oracle(costs, probs, budget)[0],
                                            ratio_greedy(costs, probs, budget)[0])

    def test_reject_invalid(self):
        cases = [
            ((True,), (Fraction(1),), 1),
            ((0,), (Fraction(1),), 1),
            ((1,), (True,), 1),
            ((1,), (Fraction(3, 2),), 1),
            ((1,), (Fraction(-1, 2),), 1),
            ((1,), (0.5,), 1),
            ((1,), (Fraction(1),), True),
            ((1,), (Fraction(1),), -1),
            ((1, 2), (Fraction(1),), 2),
            ((), (), 0),
        ]
        for costs, probs, budget in cases:
            with self.subTest(costs=costs, probs=probs, budget=budget):
                with self.assertRaises(ValueError):
                    exact_oracle(costs, probs, budget)

    def test_exhaustive_subsets_respect_budget(self):
        costs, probs, budget = (6, 5, 5), (Fraction(1), Fraction(4, 5), Fraction(4, 5)), 10
        value, indices = exact_oracle(costs, probs, budget)
        self.assertLessEqual(sum(costs[i] for i in indices), budget)
        for k in range(4):
            for subset in combinations(range(3), k):
                if sum(costs[i] for i in subset) <= budget:
                    self.assertGreaterEqual(value, sum((probs[i] for i in subset), Fraction(0)))


if __name__ == "__main__":
    unittest.main()
