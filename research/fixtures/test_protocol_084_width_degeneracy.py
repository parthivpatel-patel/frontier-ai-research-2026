"""Protocol 084: exact fixed-census width-degeneracy regression tests.

Synthetic algebra only. No model inference or empirical AI claims.
Execute only on a confirmed zero-cost standard public cloud runner.
"""
import itertools
import unittest
from fractions import Fraction


def sharp_bounds(labels):
    """True = adjudicated false, False = adjudicated true, None = unresolved."""
    if not isinstance(labels, (tuple, list)) or not labels:
        raise ValueError("nonempty fixed census required")
    if any(x is not None and type(x) is not bool for x in labels):
        raise ValueError("labels must be exact booleans or None")
    k = len(labels)
    f = sum(x is True for x in labels)
    u = sum(x is None for x in labels)
    return Fraction(f, k), Fraction(f + u, k)


def width(labels):
    lo, hi = sharp_bounds(labels)
    return hi - lo


def resolve(labels, index, truth_is_false):
    if type(index) is not int or not 0 <= index < len(labels):
        raise ValueError("invalid index")
    if labels[index] is not None:
        raise ValueError("already resolved")
    if type(truth_is_false) is not bool:
        raise ValueError("outcome must be boolean")
    result = list(labels)
    result[index] = truth_is_false
    return tuple(result)


def weighted_width(domains, weights):
    """Predeclared domain rates; no empty domains and weights sum to one."""
    if not isinstance(domains, dict) or not domains:
        raise ValueError("nonempty domains required")
    if set(domains) != set(weights):
        raise ValueError("weights must match domains")
    if any(type(w) is not Fraction or w <= 0 for w in weights.values()):
        raise ValueError("strictly positive Fraction weights required")
    if sum(weights.values(), Fraction(0)) != 1:
        raise ValueError("weights must sum to one")
    return sum((weights[d] * width(labels) for d, labels in domains.items()), Fraction(0))


class Protocol084Tests(unittest.TestCase):
    def test_exhaustive_one_step_for_all_small_censuses(self):
        for k in range(1, 7):
            for labels in itertools.product((False, True, None), repeat=k):
                before = width(labels)
                for i, label in enumerate(labels):
                    if label is None:
                        for outcome in (False, True):
                            after = width(resolve(labels, i, outcome))
                            self.assertEqual(before - after, Fraction(1, k))

    def test_policy_order_invariance_at_equal_success_count(self):
        initial = (True, None, False, None, None, True)
        for b in range(4):
            for indices in itertools.permutations((1, 3, 4), b):
                for outcomes in itertools.product((False, True), repeat=b):
                    state = initial
                    for i, outcome in zip(indices, outcomes):
                        state = resolve(state, i, outcome)
                    self.assertEqual(width(state), Fraction(3 - b, 6))

    def test_weighted_domain_counterexample(self):
        domains = {"nlp": (None, None), "physics": (None, None, None, None)}
        weights = {"nlp": Fraction(3, 4), "physics": Fraction(1, 4)}
        baseline = weighted_width(domains, weights)
        nlp = dict(domains, nlp=(False, None))
        physics = dict(domains, physics=(False, None, None, None))
        self.assertEqual(baseline - weighted_width(nlp, weights), Fraction(3, 8))
        self.assertEqual(baseline - weighted_width(physics, weights), Fraction(1, 16))
        # The difference follows predeclared weights, not learned verification.

    def test_unresolved_truth_changes_endpoint_not_width(self):
        initial = (True, None, False)
        low = sharp_bounds(resolve(initial, 1, False))
        high = sharp_bounds(resolve(initial, 1, True))
        self.assertEqual(low, (Fraction(1, 3), Fraction(1, 3)))
        self.assertEqual(high, (Fraction(2, 3), Fraction(2, 3)))

    def test_invalid_inputs_fail_closed(self):
        for labels in ((), [], (1,), ("false",), (None, 0)):
            with self.subTest(labels=labels), self.assertRaises(ValueError):
                sharp_bounds(labels)
        for index, outcome in ((0, True), (1, 1), (True, False), (4, False)):
            with self.subTest(index=index, outcome=outcome), self.assertRaises(ValueError):
                resolve((True, None), index, outcome)
        with self.assertRaises(ValueError):
            weighted_width({"nlp": (None,)}, {"nlp": Fraction(1, 2)})


if __name__ == "__main__":
    unittest.main()
