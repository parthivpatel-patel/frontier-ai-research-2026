"""Protocol 146: standalone exact-rational identifiability witnesses.

Specification tests only. Run on verified zero-charge cloud infrastructure.
No third-party packages or model inference required.
"""
import unittest
from fractions import Fraction as F
from itertools import product


def joint_distribution(p, t0, t1):
    """Return eight P(Y=y,V1=a,V2=b) values, independently normalized."""
    if not F(0) <= p <= F(1):
        raise ValueError("prevalence outside [0,1]")
    if not all(F(0) <= t <= F(1, 2) for t in (t0, t1)):
        raise ValueError("conditional dependence outside [0,1/2]")
    out = {}
    for y, a, b in product((0, 1), repeat=3):
        prior = p if y else 1 - p
        t = t1 if y else t0
        out[y, a, b] = prior * (t if a == b else F(1, 2) - t)
    assert sum(out.values()) == 1
    return out


def unlabeled_pairs(joint):
    return {(a, b): sum(joint[y, a, b] for y in (0, 1))
            for a, b in product((0, 1), repeat=2)}


def enumerated_loss(joint):
    """Accept 11: loss 2 if false, 0 if true; otherwise abstain at loss 1."""
    return sum(mass * ((2 if y == 0 else 0) if a == b == 1 else 1)
               for (y, a, b), mass in joint.items())


class Protocol146Tests(unittest.TestCase):
    def test_indistinguishable_unlabeled_pairs(self):
        a = joint_distribution(F(1, 2), F(0), F(1, 2))
        b = joint_distribution(F(1, 2), F(1, 2), F(0))
        self.assertEqual(unlabeled_pairs(a), unlabeled_pairs(b))
        self.assertEqual(unlabeled_pairs(a),
                         {(0, 0): F(1, 4), (0, 1): F(1, 4),
                          (1, 0): F(1, 4), (1, 1): F(1, 4)})
        self.assertNotEqual(a, b)

    def test_distinct_losses_under_identical_observations(self):
        a = joint_distribution(F(1, 2), F(0), F(1, 2))
        b = joint_distribution(F(1, 2), F(1, 2), F(0))
        self.assertEqual(enumerated_loss(a), F(3, 4))
        self.assertEqual(enumerated_loss(b), F(5, 4))
        self.assertEqual(enumerated_loss(b) - enumerated_loss(a), F(1, 2))

    def test_rectangular_and_coupled_maxima(self):
        ps = (F(1, 4), F(3, 4))
        ts = (F(0), F(1, 2))
        rectangular = [enumerated_loss(joint_distribution(p, a, b))
                       for p, a, b in product(ps, ts, ts)]
        coupled = [enumerated_loss(joint_distribution(p, t, t))
                   for p, t in product(ps, ts)]
        self.assertEqual(max(rectangular), F(11, 8))
        self.assertEqual(max(coupled), F(5, 4))
        self.assertEqual(max(rectangular) - max(coupled), F(1, 8))

    def test_conditional_verifier_marginals(self):
        for p, t0, t1 in product((F(1, 4), F(1, 2), F(3, 4)),
                                  (F(0), F(1, 4), F(1, 2)),
                                  (F(0), F(1, 4), F(1, 2))):
            j = joint_distribution(p, t0, t1)
            for y in (0, 1):
                prior = p if y else 1-p
                for index in (1, 2):
                    self.assertEqual(
                        sum(v for state, v in j.items()
                            if state[0] == y and state[index] == 1),
                        prior / 2)

    def test_invalid_parameters(self):
        for args in ((F(-1, 8), F(0), F(0)),
                     (F(9, 8), F(0), F(0)),
                     (F(1, 2), F(-1, 8), F(0)),
                     (F(1, 2), F(0), F(5, 8))):
            with self.assertRaises(ValueError):
                joint_distribution(*args)


if __name__ == "__main__":
    unittest.main()
