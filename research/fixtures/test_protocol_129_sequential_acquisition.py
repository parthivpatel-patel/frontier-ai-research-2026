"""Protocol 129: independent exact-rational sequential acquisition oracle.

Standard-library-only fixture. Synthetic stipulated conditional distributions,
NOT empirical AI results. Execute only on verified zero-charge remote compute.
"""
from fractions import Fraction as F
from itertools import product
import unittest

ACTIONS = (0, 1, 2)  # reject, accept, abstain
# For each Y1 outcome, stop with action 0..2 or acquire and
# choose a terminal action for each Y2 outcome (3..11).
CHOICES = tuple(range(12))
POLICIES = tuple(product(CHOICES, repeat=2))


def corners(sensitivity=F(4, 5), specificity=F(4, 5)):
    """Four Fréchet corners with identical marginals for both verifiers."""
    p1, p0 = sensitivity, 1 - specificity
    def endpoints(p):
        return (max(F(0), 2 * p - 1), p)
    return tuple((u, v) for u in endpoints(p1) for v in endpoints(p0))


def joint(p, both_positive):
    """Joint probabilities ordered (++,+-,-+,--)."""
    return (both_positive, p - both_positive, p - both_positive,
            1 - 2 * p + both_positive)


def action(choice, second):
    if choice < 3:
        return choice
    return (choice - 3) // 3 if second == 0 else (choice - 3) % 3


def acquired(choice):
    return choice >= 3


def loss(action_id, truth, false_accept=F(1), false_reject=F(1),
         abstain=F(1, 4)):
    if action_id == 2:
        return abstain
    if action_id == truth:
        return F(0)
    return false_accept if action_id == 1 else false_reject


def risk(policy, coupling, prior=F(1, 2), fee=F(0),
         false_accept=F(1), false_reject=F(1), abstain=F(1, 4),
         sensitivity=F(4, 5), specificity=F(4, 5)):
    total = F(0)
    for truth, weight, positive, both in (
        (1, prior, sensitivity, coupling[0]),
        (0, 1 - prior, 1 - specificity, coupling[1]),
    ):
        for (first, second), probability in zip(
            ((0, 0), (0, 1), (1, 0), (1, 1)), joint(positive, both)
        ):
            choice = policy[first]
            total += weight * probability * (
                loss(action(choice, second), truth,
                     false_accept, false_reject, abstain)
                + (fee if acquired(choice) else 0)
            )
    return total


def minimax(policies, **kwargs):
    feasible = corners(kwargs.get('sensitivity', F(4, 5)),
                       kwargs.get('specificity', F(4, 5)))
    return min(max(risk(policy, c, **kwargs) for c in feasible)
               for policy in policies)


NEVER = tuple(p for p in POLICIES if all(x < 3 for x in p))
ALWAYS = tuple(p for p in POLICIES if all(x >= 3 for x in p))
CONDITIONAL = tuple(p for p in POLICIES if (p[0] >= 3) != (p[1] >= 3))


class Protocol129Tests(unittest.TestCase):
    def test_nondefault_marginals_are_consistent(self):
        sensitivity, specificity = F(3, 4), F(2, 3)
        for c in corners(sensitivity, specificity):
            self.assertEqual(sum(joint(sensitivity, c[0])), 1)
            self.assertEqual(sum(joint(1-specificity, c[1])), 1)
            self.assertTrue(all(x >= 0 for x in joint(sensitivity, c[0])))
            self.assertTrue(all(x >= 0 for x in joint(1-specificity, c[1])))
            # An always-reject policy incurs loss exactly equal to prior
            # times false-reject cost, regardless of verifier marginals.
            self.assertEqual(risk((0, 0), c, prior=F(2, 5),
                                  sensitivity=sensitivity,
                                  specificity=specificity), F(2, 5))
        self.assertEqual(minimax(NEVER, sensitivity=sensitivity,
                                 specificity=specificity),
                         minimax(NEVER))

    def test_policy_partition(self):
        self.assertEqual((len(POLICIES), len(NEVER), len(ALWAYS),
                          len(CONDITIONAL)), (144, 9, 81, 54))
        self.assertEqual(len(set(POLICIES)), 144)

    def test_joint_marginals(self):
        for both, positive in ((u, F(4, 5)) for u, _ in corners()):
            cells = joint(positive, both)
            self.assertEqual(sum(cells), 1)
            self.assertEqual(cells[0] + cells[1], positive)
            self.assertEqual(cells[0] + cells[2], positive)
            self.assertTrue(all(x >= 0 for x in cells))

    def test_embedding_and_zero_cost(self):
        for prior in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
            for fee in (F(0), F(1, 20), F(1, 4), F(1)):
                args = dict(prior=prior, fee=fee)
                seq = minimax(POLICIES, **args)
                no = minimax(NEVER, **args)
                yes = minimax(ALWAYS, **args)
                self.assertLessEqual(seq, min(no, yes))
                if fee == 0:
                    self.assertEqual(seq, yes)

    def test_fee_never_paid_when_stopping(self):
        for policy in NEVER:
            self.assertEqual(risk(policy, corners()[0], fee=F(10)),
                             risk(policy, corners()[0], fee=F(0)))

    def test_asymmetric_loss_embedding(self):
        args = dict(prior=F(2, 5), fee=F(1, 20),
                    false_accept=F(3), false_reject=F(1),
                    abstain=F(2, 5))
        self.assertLessEqual(minimax(POLICIES, **args),
                             min(minimax(NEVER, **args),
                                 minimax(ALWAYS, **args)))


if __name__ == "__main__":
    unittest.main()
