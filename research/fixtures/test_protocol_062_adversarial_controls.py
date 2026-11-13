"""Adversarial, standard-library-only checks for Protocol 062.

Not an experiment, not an authorization to run cloud jobs. Execute only after
account-specific zero-cost cloud eligibility and billing exposure are verified.
"""
import unittest

def validate_audit_budget(value, alternative_identification=None):
    """Return a blocker unless labels are identifiable with a positive budget."""
    if type(value) is not int or value < 1:
        if alternative_identification is not None:
            # A mere assertion of alternative identification is not proof.
            return "alternative identification requires independently reviewed evidence"
        return "audit_budget must be a positive integer"
    return None

def verify_disjoint_families(calibration, test):
    """Use actual family IDs, not a declaration of disjointness."""
    if not isinstance(calibration, (list, tuple, set)) or not isinstance(test, (list, tuple, set)):
        return "family partitions must be explicit collections"
    if not calibration or not test:
        return "both partitions must contain families"
    if any(type(x) is not str or not x.strip() for x in list(calibration) + list(test)):
        return "family IDs must be nonempty strings"
    if set(calibration) & set(test):
        return "calibration and test share provenance families"
    return None

def validate_coverage(target, tolerance):
    """Absolute tolerance must define a nonempty feasible interval in [0,1]."""
    if any(type(v) not in (int, float) for v in (target, tolerance)):
        return "coverage values must be numeric"
    if not (0 < target <= 1 and 0 <= tolerance < 1):
        return "invalid target or absolute tolerance"
    if target - tolerance < 0 or target + tolerance > 1:
        return "absolute coverage interval exceeds [0,1]"
    return None

class AdversarialManifestControls(unittest.TestCase):
    def test_zero_budget_rejected(self):
        for value in (0, -1, True, 0.5, None):
            with self.subTest(value=value):
                self.assertIsNotNone(validate_audit_budget(value))
        self.assertIsNone(validate_audit_budget(1))

    def test_claimed_disjointness_cannot_hide_overlap(self):
        self.assertIsNotNone(verify_disjoint_families(["family-a", "family-b"], ["family-b"]))
        self.assertIsNone(verify_disjoint_families(["family-a"], ["family-b"]))
        self.assertIsNotNone(verify_disjoint_families([], ["family-b"]))

    def test_coverage_interval_is_feasible(self):
        self.assertIsNotNone(validate_coverage(0.95, 0.10))
        self.assertIsNone(validate_coverage(0.8, 0.05))
        self.assertIsNotNone(validate_coverage(True, 0.05))

    def test_alternative_identification_is_not_self_attesting(self):
        self.assertIsNotNone(validate_audit_budget(0, alternative_identification="verified"))

if __name__ == "__main__":
    unittest.main()
