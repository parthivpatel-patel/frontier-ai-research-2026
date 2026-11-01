"""Exact-arithmetic positive and negative controls; no model-performance claim."""
import unittest
from src.exact_domain_audit import (
    Domain, Interval, Q, audit_scope, counterexample,
    exact_reachable, reflect, threshold_disagreement,
)

def I(a, b):
    return Interval(Q(a), Q(b))

def D(a0, a1, v0, v1, u0, u1):
    return Domain(I(a0, a1), I(v0, v1), I(u0, u1))

class ExactDomainAuditTests(unittest.TestCase):
    def setUp(self):
        self.certified = D('0.9', '0.9', '0.2', '0.2', '0.2', '0.2')
        self.expanded = D('0.9', '0.9', '0.2', '0.2', '-0.2', '0.2')

    def test_exact_reachability_crosses_reflection_kink(self):
        self.assertEqual(exact_reachable(self.expanded), I('0.7', '1'))
        self.assertEqual(exact_reachable(self.certified), I('0.7', '0.7'))

    def test_scope_leak_has_constructive_counterexample(self):
        result = audit_scope(self.certified, self.expanded, Q('0.8'))
        self.assertEqual(result['status'], 'asserted_claim_falsified')
        self.assertTrue(result['certificate_valid_on_certified_domain'])
        self.assertFalse(result['asserted_domain_subset_of_certified'])
        witness = tuple(Q(x) for x in result['counterexample'])
        self.assertEqual(reflect(sum(witness, Q(0))), Q(1))
        self.assertTrue(self.expanded.position.low <= witness[0] <= self.expanded.position.high)
        self.assertTrue(self.expanded.velocity.low <= witness[1] <= self.expanded.velocity.high)
        self.assertTrue(self.expanded.impulse.low <= witness[2] <= self.expanded.impulse.high)

    def test_unsupported_scope_does_not_mean_false(self):
        enlarged = D('0.9', '0.9', '0.2', '0.2', '0.1', '0.2')
        result = audit_scope(self.certified, enlarged, Q(1))
        self.assertEqual(result['status'], 'asserted_claim_true_but_scope_unsupported')
        self.assertIsNone(result['counterexample'])

    def test_valid_certificate_and_subset(self):
        result = audit_scope(self.expanded, self.certified, Q(1))
        self.assertEqual(result['status'], 'supported_on_asserted_scope')
        self.assertTrue(result['asserted_domain_subset_of_certified'])

    def test_invalid_certificate_is_distinct(self):
        result = audit_scope(self.expanded, self.certified, Q('0.8'))
        self.assertEqual(result['status'], 'invalid_certificate')
        self.assertTrue(result['asserted_claim_true_for_this_toy_dynamics'])

    def test_threshold_semantics_and_negative_control(self):
        self.assertTrue(threshold_disagreement(self.expanded, Q('0.8'), Q(1)))
        self.assertFalse(threshold_disagreement(self.expanded, Q(1), Q(1)))
        self.assertFalse(threshold_disagreement(self.certified, Q('0.8'), Q(1)))

    def test_exact_endpoint_semantics(self):
        singleton = D('0.9', '0.9', '0.2', '0.2', '-0.1', '-0.1')
        self.assertEqual(exact_reachable(singleton), I(1, 1))
        self.assertTrue(threshold_disagreement(singleton, Q('0.8'), Q(1)))
        self.assertFalse(threshold_disagreement(singleton, Q(1), Q(2)))
        self.assertIsNone(counterexample(singleton, Q(1)))

    def test_reject_unsupported_physical_domain(self):
        with self.assertRaises(ValueError):
            D('0.9', '1.1', '0', '0', '0', '0')
        with self.assertRaises(ValueError):
            D('0.9', '0.9', '2', '2', '0', '0')
        with self.assertRaises(ValueError):
            I('0.3', '0.2')
        with self.assertRaises(TypeError):
            Interval(0.2, 0.3)

if __name__ == '__main__':
    unittest.main()
