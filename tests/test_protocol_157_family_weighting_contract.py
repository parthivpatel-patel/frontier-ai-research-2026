"""Protocol 157: deterministic checks for family weighting and abstention.

Standard-library-only arithmetic fixtures. These are NOT model evaluations.
"""
import unittest


def summarize(records):
    """Return unconditional yield and selective accuracy by case and family."""
    if not records:
        raise ValueError("at least one case required")
    groups = {}
    for family, returned, correct in records:
        if not family or not isinstance(returned, bool) or not isinstance(correct, bool):
            raise ValueError("invalid record")
        if correct and not returned:
            raise ValueError("a non-returned answer cannot be correct")
        groups.setdefault(family, []).append((returned, correct))
    n = len(records)
    case_yield = sum(correct for _, _, correct in records) / n
    family_yield = sum(
        sum(correct for _, correct in values) / len(values)
        for values in groups.values()
    ) / len(groups)
    returned_count = sum(returned for _, returned, _ in records)
    conditional_accuracy = (
        sum(correct for _, _, correct in records) / returned_count
        if returned_count else None
    )
    return case_yield, family_yield, conditional_accuracy


class FamilyWeightingContract(unittest.TestCase):
    def test_unequal_family_counterexample(self):
        x = [("A", True, True)] * 100 + [("B", True, False)]
        y = [("A", True, False)] * 100 + [("B", True, True)]
        sx, sy = summarize(x), summarize(y)
        self.assertEqual(sx[0], 100 / 101)
        self.assertEqual(sy[0], 1 / 101)
        self.assertEqual(sx[1], 0.5)
        self.assertEqual(sy[1], 0.5)

    def test_zero_return_has_defined_unconditional_yield(self):
        result = summarize([("mechanics", False, False), ("optics", False, False)])
        self.assertEqual(result[:2], (0.0, 0.0))
        self.assertIsNone(result[2])

    def test_selective_accuracy_differs_from_unconditional_yield(self):
        result = summarize([
            ("mechanics", True, True),
            ("mechanics", False, False),
            ("optics", True, False),
        ])
        self.assertEqual(result[0], 1 / 3)
        self.assertEqual(result[1], 1 / 4)
        self.assertEqual(result[2], 1 / 2)

    def test_invalid_nonreturn_correctness_rejected(self):
        with self.assertRaises(ValueError):
            summarize([("mechanics", False, True)])

    def test_empty_manifest_rejected(self):
        with self.assertRaises(ValueError):
            summarize([])


if __name__ == "__main__":
    unittest.main()
