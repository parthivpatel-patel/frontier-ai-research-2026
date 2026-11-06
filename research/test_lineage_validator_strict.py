"""Protocol 101 synthetic tests. No empirical physics claims."""
import unittest
from research.lineage_validator_strict import validate_strict_lineages


def row(**changes):
    item = dict(scenario_id="s1", source_id="src1", family="mechanics",
                assumptions={"drag": False}, claim="velocity constant",
                intervention_id="base", adjudicator="reviewer1",
                label="supported", split="train")
    item.update(changes)
    return item


class StrictLineageTests(unittest.TestCase):
    def rejects(self, records):
        with self.assertRaises(ValueError):
            validate_strict_lineages(records)

    def test_valid(self):
        self.assertEqual(validate_strict_lineages([row()]), 1)

    def test_unhashable_label(self):
        self.rejects([row(label=[])])

    def test_dictionary_label(self):
        self.rejects([row(label={})])

    def test_nonstring_assumption_key(self):
        self.rejects([row(assumptions={1: "yes"})])

    def test_nested_nonstring_key(self):
        self.rejects([row(assumptions={"nested": {False: 1}})])

    def test_nan(self):
        self.rejects([row(assumptions={"x": float("nan")})])

    def test_tuple(self):
        self.rejects([row(assumptions={"x": (1, 2)})])

    def test_leading_space(self):
        self.rejects([row(scenario_id=" s1")])

    def test_trailing_space(self):
        self.rejects([row(source_id="src1 ")])

    def test_family_leakage(self):
        self.rejects([row(source_family_id="familyA"),
                      row(scenario_id="s2", source_id="src2",
                          source_family_id="familyA", split="test")])

    def test_paraphrase_conflict(self):
        self.rejects([row(proposition_id="p1"),
                      row(intervention_id="paraphrase", claim="speed unchanged",
                          proposition_id="p1", label="refuted")])

    def test_distinct_intervention(self):
        self.assertEqual(validate_strict_lineages([
            row(proposition_id="p1"),
            row(intervention_id="drag", proposition_id="p1",
                assumptions={"drag": True}, label="refuted")]), 2)

    def test_unresolved(self):
        self.assertEqual(validate_strict_lineages([
            row(label=None, adjudicator=None)]), 1)

    def test_duplicate(self):
        self.rejects([row(), row()])

    def test_nonstring_optional_id(self):
        self.rejects([row(proposition_id=3)])

    def test_cross_split_scenario(self):
        self.rejects([row(), row(intervention_id="changed", split="test")])


if __name__ == "__main__":
    unittest.main()
