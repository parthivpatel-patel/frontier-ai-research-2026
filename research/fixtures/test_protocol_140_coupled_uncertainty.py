"""Protocol 140: independent exact-rational coupled-uncertainty witness.

Synthetic mathematical regression only. No AI model evaluation or novelty claim.
Run on a verified zero-charge cloud runner, not the user's laptop.
"""
import unittest
from fractions import Fraction as Q
from itertools import product


def joint_cells(t):
    """P(V1,V2 | Y=y), ordered (00,01,10,11), both marginals 1/2."""
    if not Q(0) <= t <= Q(1, 2):
        raise ValueError("coupling outside Frechet interval")
    return (t, Q(1, 2)-t, Q(1, 2)-t, t)


def conditional_loss(y, t):
    """Accept only (1,1), otherwise abstain; false accept=2, abstain=1."""
    cells = joint_cells(t)
    losses = (Q(1), Q(1), Q(1), Q(0) if y else Q(2))
    return sum((p*l for p,l in zip(cells, losses)), Q(0))


def risk(t0, t1, prevalence=Q(1, 2)):
    if not Q(0) <= prevalence <= Q(1):
        raise ValueError("invalid prevalence")
    return (1-prevalence)*conditional_loss(0,t0)+prevalence*conditional_loss(1,t1)


class Protocol140Tests(unittest.TestCase):
    def test_cells_are_probabilities_and_have_fixed_marginals(self):
        for t in (Q(0),Q(1,8),Q(1,4),Q(3,8),Q(1,2)):
            c=joint_cells(t)
            self.assertEqual(sum(c),Q(1))
            self.assertTrue(all(x>=0 for x in c))
            self.assertEqual(c[2]+c[3],Q(1,2))
            self.assertEqual(c[1]+c[3],Q(1,2))

    def test_diagonal_feasible_set_has_constant_risk(self):
        for t in (Q(0),Q(1,8),Q(1,4),Q(3,8),Q(1,2)):
            self.assertEqual(risk(t,t),Q(1))

    def test_rectangle_maximum_is_conservative_not_attainable(self):
        corners=[risk(a,b) for a,b in product((Q(0),Q(1,2)),repeat=2)]
        self.assertEqual(max(corners),Q(5,4))
        self.assertEqual(max(risk(t,t) for t in (Q(0),Q(1,2))),Q(1))
        self.assertEqual(risk(Q(1,2),Q(0)),Q(5,4))
        self.assertNotEqual(Q(1,2),Q(0))

    def test_direct_enumeration_matches_affine_formula(self):
        for a,b in product((Q(0),Q(1,8),Q(1,4),Q(3,8),Q(1,2)),repeat=2):
            self.assertEqual(risk(a,b),Q(1)+(a-b)/2)

    def test_reject_invalid_inputs(self):
        for t in (Q(-1,8),Q(5,8)):
            with self.assertRaises(ValueError):
                joint_cells(t)
        with self.assertRaises(ValueError):
            risk(Q(0),Q(0),Q(3,2))


if __name__ == "__main__":
    unittest.main()
