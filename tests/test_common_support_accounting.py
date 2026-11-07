"""Synthetic acceptance-accounting regression tests; no empirical claims."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "common_support_accounting",
    Path(__file__).resolve().parents[1] / "research" / "common_support_accounting.py",
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
summarize = module.summarize


def pair(key, a, b, ua=None, ub=None):
    return [
        dict(intervention_key=key, system="A", accepted=a, unsafe=ua),
        dict(intervention_key=key, system="B", accepted=b, unsafe=ub),
    ]


class CommonSupportAccountingTests(unittest.TestCase):
    def test_identical(self):
        x = summarize(pair("p", True, True, False, False))
        self.assertEqual(x["common_support_difference"], 0)

    def test_disjoint(self):
        x = summarize(pair("p", True, False, False) + pair("q", False, True, ub=True))
        self.assertIsNone(x["common_support_difference"])
        self.assertEqual(x["acceptance_cells"]["11"], 0)

    def test_zero_acceptance_is_undefined(self):
        x = summarize(pair("p", False, True, ub=True))
        self.assertIsNone(x["selective_risk"]["A"])

    def test_common_support_excludes_single_acceptance(self):
        x = summarize(pair("p", True, True, True, False) + pair("q", True, False, False))
        self.assertEqual(x["common_support_difference"], 1)
        self.assertEqual(x["selective_risk"]["A"], 0.5)

    def test_equal_coverage_not_equal_overlap(self):
        x = summarize(pair("p", True, False, False) + pair("q", False, True, ub=False))
        self.assertEqual(x["coverage"]["A"], x["coverage"]["B"])
        self.assertEqual(x["common_support_coverage"], 0)

    def test_missing_counterpart_rejected(self):
        with self.assertRaises(ValueError):
            summarize([dict(intervention_key="p", system="A", accepted=False, unsafe=None)])

    def test_row_order_invariance(self):
        rows = pair("p", True, True, False, True) + pair("q", False, False)
        self.assertEqual(summarize(rows), summarize(list(reversed(rows))))

    def test_duplicate_rejected(self):
        rows = pair("p", False, False)
        with self.assertRaises(ValueError):
            summarize(rows + [rows[0]])

    def test_abstention_label_rejected(self):
        with self.assertRaises(ValueError):
            summarize(pair("p", False, False, True))

    def test_accepted_without_label_rejected(self):
        with self.assertRaises(ValueError):
            summarize(pair("p", True, False))

    def test_empty_population_rejected(self):
        with self.assertRaises(ValueError):
            summarize([])


if __name__ == "__main__":
    unittest.main()
