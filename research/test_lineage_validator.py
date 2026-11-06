"""Synthetic regression tests for Protocol 098 lineage validation."""
import copy
import unittest
from research.lineage_validator import validate_lineages


def example(**changes):
    row = dict(scenario_id="scenario-1", source_id="source-1",
               family="mechanics", assumptions={"drag": "negligible"},
               claim="Horizontal velocity is constant",
               intervention_id="base", adjudicator="independent-reviewer-1",
               label="supported", split="train")
    row.update(changes)
    return row


class LineageValidationTests(unittest.TestCase):
    def assert_rejected(self, records):
        with self.assertRaises(ValueError):
            validate_lineages(records)

    def test_valid_synthetic_record(self):
        self.assertEqual(validate_lineages([example()]), 1)

    def test_duplicate_identifier(self):
        self.assert_rejected([example(), example()])

    def test_cross_split_scenario(self):
        self.assert_rejected([example(), example(intervention_id="changed",
                                               split="test")])

    def test_cross_split_source(self):
        self.assert_rejected([example(), example(scenario_id="scenario-2",
                                               intervention_id="changed",
                                               split="test")])

    def test_conflicting_truth(self):
        self.assert_rejected([example(), example(intervention_id="paraphrase",
                                               label="refuted")])

    def test_missing_provenance(self):
        self.assert_rejected([example(adjudicator=None)])

    def test_unresolved_allowed(self):
        self.assertEqual(validate_lineages([example(label=None,
                                                   adjudicator=None)]), 1)

    def test_different_assumptions_allow_different_verdicts(self):
        self.assertEqual(validate_lineages([
            example(),
            example(intervention_id="drag", assumptions={"drag": "significant"},
                    label="refuted")]), 2)

    def test_missing_field(self):
        row = example()
        del row["source_id"]
        self.assert_rejected([row])

    def test_noncanonical_assumptions(self):
        self.assert_rejected([example(assumptions={"bad": {1, 2}})])

    def test_unknown_split(self):
        self.assert_rejected([example(split="evaluation")])

    def test_input_not_list(self):
        self.assert_rejected({"records": [example()]})


if __name__ == "__main__":
    unittest.main()
