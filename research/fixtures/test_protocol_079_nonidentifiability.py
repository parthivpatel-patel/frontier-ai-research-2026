"""Protocol 079: exact nonidentifiability witness for unresolved released claims.

Dependency-free, deterministic tests. Mathematical verification only, not AI evidence.
Run on a verified free cloud runner; no local execution is requested.
"""
import itertools
import unittest


def released_risk_bounds(records, *, census):
    """Return sharp logical bounds for binary false-release fraction in a census.

    Each record: (released: bool, resolved: bool, false: bool | None).
    Non-released claims do not enter the released-claim estimand.
    """
    if type(census) is not bool or not census:
        raise ValueError("sample-only records cannot establish census bounds")
    if not isinstance(records, (tuple, list)):
        raise TypeError("records must be a sequence")
    for record in records:
        if not isinstance(record, (tuple, list)) or len(record) != 3:
            raise ValueError("each record must contain exactly three fields")
        released_flag, resolved, truth = record
        if type(released_flag) is not bool or type(resolved) is not bool:
            raise ValueError("release and resolution must be booleans")
        if resolved and type(truth) is not bool:
            raise ValueError("resolved label must be boolean")
        if not resolved and truth is not None:
            raise ValueError("unresolved label must not masquerade as observed")
    released = [r for r in records if r[0]]
    if not released:
        raise ValueError("false-release fraction undefined with no releases")
    false_known = 0
    unresolved = 0
    for released_flag, resolved, truth in records:
        if released_flag:
            false_known += int(resolved and truth is True)
            unresolved += int(not resolved)
    k = len(released)
    return false_known / k, (false_known + unresolved) / k


def observed_record(latent_completion):
    """Identical observation for any completion of the two missing labels."""
    if len(latent_completion) != 2 or any(type(v) is not bool for v in latent_completion):
        raise ValueError("two latent boolean labels required")
    return ((True, True, True), (True, True, False),
            (True, False, None), (True, False, None))


class Protocol079ExactWitness(unittest.TestCase):
    def test_all_completions(self):
        risks = sorted((1 + sum(bits)) / 4 for bits in itertools.product((False, True), repeat=2))
        self.assertEqual(risks, [0.25, 0.5, 0.5, 0.75])

    def test_observational_equivalence(self):
        self.assertEqual(observed_record((False, False)), observed_record((True, True)))
        self.assertNotEqual((1 + sum((False, False))) / 4,
                            (1 + sum((True, True))) / 4)

    def test_sharp_bounds(self):
        self.assertEqual(released_risk_bounds(observed_record((False, False)), census=True),
                         (0.25, 0.75))

    def test_complete_labels_collapse(self):
        records = [(True, True, True), (True, True, False),
                   (True, True, True), (True, True, False)]
        self.assertEqual(released_risk_bounds(records, census=True), (0.5, 0.5))

    def test_no_releases_undefined(self):
        with self.assertRaises(ValueError):
            released_risk_bounds([(False, True, False)], census=True)

    def test_unresolved_cannot_be_falsely_observed(self):
        with self.assertRaises(ValueError):
            released_risk_bounds([(True, False, False)], census=True)

    def test_sample_only_rejected(self):
        with self.assertRaises(ValueError):
            released_risk_bounds(observed_record((False, False)), census=False)

    def test_adversarial_record_shapes_rejected(self):
        malformed = [[], [()], [(True,)], [(1, True, True)],
                     [(True, 1, True)], [(False, True)],
                     [(False, True, 1)], [(False, False, False)],
                     [(True, True, True), ()], [None]]
        for records in malformed:
            with self.subTest(records=records):
                with self.assertRaises(ValueError):
                    released_risk_bounds(records, census=True)

    def test_valid_nonreleased_unresolved_record(self):
        self.assertEqual(released_risk_bounds(
            [(False, False, None), (True, True, True)], census=True), (1.0, 1.0))

    def test_strict_census_flag(self):
        with self.assertRaises(ValueError):
            released_risk_bounds([(True, True, True)], census=0)

    def test_invalid_resolved_label_rejected(self):
        with self.assertRaises(ValueError):
            released_risk_bounds([(True, True, None)], census=True)


if __name__ == "__main__":
    unittest.main()
