"""Protocol 054: regression controls for the paired source-cluster bootstrap.

Run only on a verified no-charge cloud runner. Synthetic fixtures are unit tests,
not empirical scientific evidence. Standard-library unittest, no model inference.
"""
import importlib.util
import pathlib
import unittest

MODULE = pathlib.Path(__file__).resolve().parents[1] / "research" / "paired_cluster_bootstrap.py"
spec = importlib.util.spec_from_file_location("paired_cluster_bootstrap", MODULE)
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


def record(i, source, truth, baseline, certificate):
    return {"id": str(i), "source_id": source, "truth": truth,
            "baseline_accept": baseline, "certificate_accept": certificate}


class BootstrapContractTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            record(1, "source_a", 1, True, False),
            record(2, "source_a", 0, True, True),
            record(3, "source_b", 1, True, False),
            record(4, "source_b", 0, False, True),
            record(5, "source_c", None, False, False),
            record(6, "source_c", 0, True, True),
        ]

    def test_paired_point_estimates(self):
        p = bootstrap.metrics(self.rows)
        self.assertAlmostEqual(p["baseline"]["coverage"], 4 / 6)
        self.assertAlmostEqual(p["certificate"]["coverage"], 3 / 6)
        self.assertAlmostEqual(p["baseline"]["unsafe_acceptance_known"], 2 / 5)
        self.assertEqual(p["certificate"]["unsafe_acceptance_known"], 0)

    def test_unknown_not_counted_as_safe(self):
        p = bootstrap.metrics(self.rows)
        self.assertEqual(p["n_unknown"], 1)
        self.assertEqual(p["n_known"], 5)

    def test_empty_acceptance_has_undefined_conditional_risk(self):
        rows = [record(1, "a", 1, False, False), record(2, "b", 0, True, False)]
        p = bootstrap.metrics(rows)
        self.assertIsNone(p["certificate"]["conditional_unsafe_known"])
        self.assertEqual(p["certificate"]["coverage"], 0)

    def test_all_unknown_truth_has_undefined_risk(self):
        rows = [record(1, "a", None, True, False), record(2, "b", None, False, True)]
        p = bootstrap.metrics(rows)
        self.assertIsNone(p["baseline"]["unsafe_acceptance_known"])
        self.assertIsNone(p["certificate"]["unsafe_acceptance_known"])

    def test_repeatable_seed(self):
        a = bootstrap.evaluate(self.rows, replicates=100, seed=7)
        b = bootstrap.evaluate(self.rows, replicates=100, seed=7)
        self.assertEqual(a, b)
        self.assertEqual(a["clusters"], 3)

    def test_identical_methods_zero_paired_difference(self):
        rows = [dict(r, certificate_accept=r["baseline_accept"]) for r in self.rows]
        result = bootstrap.evaluate(rows, replicates=100, seed=11)
        for key in ("coverage", "known_label_coverage", "unsafe_acceptance_known"):
            self.assertEqual(result["point"]["difference_certificate_minus_baseline"][key], 0)
            interval = result["intervals"][key]
            if interval["lower"] is not None:
                self.assertEqual(interval["lower"], 0)
                self.assertEqual(interval["upper"], 0)

    def test_reject_duplicate_ids_and_single_cluster(self):
        with self.assertRaises(ValueError):
            bootstrap.validate([self.rows[0], dict(self.rows[1], id="1")])
        with self.assertRaises(ValueError):
            bootstrap.validate(self.rows[:2])

    def test_reject_bool_truth_and_invalid_replicates(self):
        with self.assertRaises(ValueError):
            bootstrap.validate([dict(self.rows[0], truth=True), *self.rows[1:]])
        with self.assertRaises(ValueError):
            bootstrap.evaluate(self.rows, replicates=True)
        with self.assertRaises(ValueError):
            bootstrap.evaluate(self.rows, replicates=99)


if __name__ == "__main__":
    unittest.main()
