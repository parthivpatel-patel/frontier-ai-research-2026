"""Protocol 051 negative controls: observation semantics and transport failure.

Exact rational mathematical fixtures. No model calls, network, or dependencies.
Execute only after the repository's zero-cost cloud gate is verified.
"""
from fractions import Fraction as F
from unittest import TestCase, main

def joint_table(pi, a, b, s1, s2, f1, f2):
    """Return unconditional (++,+-,-+,--) probabilities for two binary verifiers."""
    def conditional(joint, m1, m2):
        cells = (joint, m1-joint, m2-joint, 1-m1-m2+joint)
        if min(cells) < 0 or sum(cells) != 1:
            raise ValueError("infeasible conditional distribution")
        return cells
    if not 0 <= pi <= 1:
        raise ValueError("invalid prevalence")
    pos, neg = conditional(a, s1, s2), conditional(b, f1, f2)
    return tuple(pi*x+(1-pi)*y for x,y in zip(pos,neg))

def posterior_positive(pi,a,b):
    q=pi*a+(1-pi)*b
    if not q:
        raise ValueError("zero joint-positive mass")
    return pi*a/q

class NegativeControls(TestCase):
    def test_joint_positive_not_total_agreement(self):
        # Both populations have P(++)=1/4, but total agreement differs.
        first=joint_table(F(1,2),F(1,4),F(1,4),F(1,2),F(1,2),F(1,2),F(1,2))
        second=joint_table(F(1,2),F(1,4),F(1,4),F(3,4),F(3,4),F(3,4),F(3,4))
        self.assertEqual(first[0],second[0])
        self.assertNotEqual(first[0]+first[3],second[0]+second[3])
        self.assertEqual(sum(first),1)
        self.assertEqual(sum(second),1)

    def test_same_unlabeled_joint_table_different_truth_posterior(self):
        # Y can have different associations with the same observable V1,V2.
        # Marginal verifier error rates are NOT held fixed across worlds:
        # this is a negative control for unlabeled transport, not Protocol 050.
        pi=F(1,2)
        world_a=joint_table(pi,F(3,5),F(2,25),F(4,5),F(4,5),F(1,5),F(1,5))
        world_b=joint_table(pi,F(17,25),F(0),F(4,5),F(4,5),F(1,5),F(1,5))
        self.assertEqual(world_a,world_b)
        self.assertEqual(world_a,(F(17,50),F(4,25),F(4,25),F(17,50)))
        self.assertEqual(posterior_positive(pi,F(3,5),F(2,25)),F(15,17))
        self.assertEqual(posterior_positive(pi,F(17,25),F(0)),1)

    def test_infeasible_conditional_rejected(self):
        with self.assertRaises(ValueError):
            joint_table(F(1,2),F(0),F(0),F(4,5),F(4,5),F(1,5),F(1,5))

if __name__=="__main__":
    main()
