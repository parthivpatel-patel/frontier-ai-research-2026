"""Exact witnesses, identifiability limits, and negative controls."""
import unittest
from dataclasses import replace

from src.exact_domain_audit import Q
from src.physical_probe_suite import make_suite
from src.intervention_identifiability import (
    Intervention, choose_cheapest_separating_intervention,
    demonstration, observational_equivalence_classes,
    separating_witness, trajectory_output,
)


class InterventionIdentifiabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cases = {case.case_id: case for case in make_suite()}
        cls.restricted = (
            Intervention("reflecting_restricted", "reflecting",
                         cases["reflecting_restricted"].domain, Q(1)),
            Intervention("damped_restricted", "damped",
                         cases["damped_restricted"].domain, Q(1)),
        )
        cls.wide = (
            Intervention("reflecting_wide", "reflecting",
                         cases["reflecting_drift"].domain, Q(2)),
            Intervention("damped_wide", "damped",
                         cases["damped_drift"].domain, Q(3)),
        )

    def test_restricted_domains_cannot_separate_thresholds(self):
        for option in self.restricted:
            self.assertIsNone(separating_witness(option, Q("4/5"), Q("9/10")))
        result = choose_cheapest_separating_intervention(
            self.restricted, Q("4/5"), Q("9/10"))
        self.assertEqual(result["status"], "indistinguishable_under_supplied_menu")

    def test_both_wide_families_have_exact_witnesses(self):
        for option in self.wide:
            witness = separating_witness(option, Q("4/5"), Q("9/10"))
            self.assertIsNotNone(witness)
            y = trajectory_output(option, witness)
            self.assertTrue(Q("4/5") < y <= Q("9/10"))

    def test_cheapest_wide_intervention_is_selected(self):
        result = choose_cheapest_separating_intervention(
            self.restricted + self.wide, Q("4/5"), Q("9/10"))
        self.assertEqual(result["status"], "physically_distinguishable")
        self.assertEqual(result["selected"], "reflecting_wide")
        self.assertEqual(result["hypothetical_cost"], "2")
        self.assertEqual(result["separating_options"], 2)
        self.assertNotEqual(result["first_predicate"], result["second_predicate"])

    def test_equal_costs_break_ties_by_label(self):
        options = (replace(self.wide[0], label="z", cost=Q(2)),
                   replace(self.wide[1], label="a", cost=Q(2)))
        result = choose_cheapest_separating_intervention(
            options, Q("4/5"), Q("9/10"))
        self.assertEqual(result["selected"], "a")

    def test_boundary_at_reachable_maximum_is_equivalent(self):
        for option in self.restricted:
            self.assertIsNone(separating_witness(option, Q("3/4"), Q("4/5")))
            self.assertIsNotNone(separating_witness(option, Q("1/2"), Q("3/4")))

    def test_observational_equivalence_classes(self):
        groups = observational_equivalence_classes(
            self.restricted, (Q("3/5"), Q("4/5"), Q("9/10")))
        self.assertEqual(groups, ((Q("3/5"),), (Q("4/5"), Q("9/10"))))

    def test_same_threshold_never_has_separating_witness(self):
        for option in self.restricted + self.wide:
            self.assertIsNone(separating_witness(option, Q("4/5"), Q("4/5")))

    def test_empty_menu_does_not_claim_global_equivalence(self):
        result = choose_cheapest_separating_intervention(
            (), Q("4/5"), Q("9/10"))
        self.assertEqual(result["menu_size"], 0)
        self.assertIn("menu", result["status"])

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            replace(self.wide[0], cost=Q(-1))
        with self.assertRaises(TypeError):
            replace(self.wide[0], family="damped")
        with self.assertRaises(ValueError):
            choose_cheapest_separating_intervention(
                (self.wide[0], self.wide[0]), Q(0), Q(1))
        with self.assertRaises(TypeError):
            separating_witness(self.wide[0], 0.8, Q("9/10"))
        with self.assertRaises(ValueError):
            observational_equivalence_classes(
                self.wide, (Q("4/5"), Q("4/5")))
        with self.assertRaises(ValueError):
            trajectory_output(self.wide[0], (Q(0), Q(0), Q(0)))

    def test_demo_separates_physics_without_identifying_intent(self):
        result = demonstration()
        self.assertEqual(result["restricted_only"]["separating_options"], 0)
        self.assertEqual(result["full_menu"]["separating_options"], 2)
        self.assertIn("does not identify",
                      result["full_menu"]["intent_caveat"])


if __name__ == "__main__":
    unittest.main()
