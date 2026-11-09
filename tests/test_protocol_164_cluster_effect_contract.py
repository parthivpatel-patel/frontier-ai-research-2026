"""Protocol 164: descriptive cluster-weighted paired oracle.

No statistical significance is inferred. Standard-library-only fixtures.
Execution is reserved for verified free cloud CI.
"""
import unittest


def cluster_effect(a, b, clusters, families):
    """Return descriptive paired yields weighted by source cluster and family.

    Each system maps observation IDs to (answered, correct) booleans.
    Cluster and family manifests map each observation ID to nonempty strings.
    All observations in one source cluster must have the same family.
    """
    if not all(isinstance(x, dict) for x in (a, b, clusters, families)):
        raise ValueError("all inputs must be dictionaries")
    ids = set(a)
    if not ids or any(set(x) != ids for x in (b, clusters, families)):
        raise ValueError("nonempty identical observation IDs required")
    grouped = {}
    family_for_cluster = {}
    for key in ids:
        for record in (a[key], b[key]):
            if (not isinstance(record, tuple) or len(record) != 2
                    or any(type(v) is not bool for v in record)):
                raise ValueError("records must be two booleans")
            if record[1] and not record[0]:
                raise ValueError("unanswered observation cannot be correct")
        cluster, family = clusters[key], families[key]
        if not isinstance(cluster, str) or not cluster.strip():
            raise ValueError("cluster IDs must be nonempty strings")
        if not isinstance(family, str) or not family.strip():
            raise ValueError("family IDs must be nonempty strings")
        if cluster in family_for_cluster and family_for_cluster[cluster] != family:
            raise ValueError("cluster spans multiple families")
        family_for_cluster[cluster] = family
        delta = int(all(a[key])) - int(all(b[key]))
        grouped.setdefault(cluster, []).append(delta)
    means = {g: sum(ds) / len(ds) for g, ds in grouped.items()}
    by_family = {}
    for g, value in means.items():
        by_family.setdefault(family_for_cluster[g], []).append(value)
    family_means = {f: sum(v) / len(v) for f, v in by_family.items()}
    return {
        "n_observations": len(ids),
        "n_clusters": len(grouped),
        "n_families": len(by_family),
        "case_weighted_delta": sum(sum(v) for v in grouped.values()) / len(ids),
        "cluster_weighted_delta": sum(means.values()) / len(means),
        "equal_family_delta": sum(family_means.values()) / len(family_means),
        "p_value": None,
        "confidence_interval": None,
        "inference_status": "descriptive_only",
    }


class ClusterEffectContract(unittest.TestCase):
    def test_paraphrase_duplication_does_not_change_cluster_effect(self):
        a = {"x": (True, True), "y": (True, False)}
        b = {"x": (True, False), "y": (True, True)}
        r1 = cluster_effect(a, b, {"x": "one", "y": "two"},
                            {"x": "physics", "y": "physics"})
        a["x2"] = a["x"]
        b["x2"] = b["x"]
        r2 = cluster_effect(a, b, {"x": "one", "x2": "one", "y": "two"},
                            {"x": "physics", "x2": "physics", "y": "physics"})
        self.assertEqual(r1["cluster_weighted_delta"], r2["cluster_weighted_delta"])
        self.assertNotEqual(r1["case_weighted_delta"], r2["case_weighted_delta"])

    def test_unequal_family_counts(self):
        ids = ["a", "b", "c"]
        a = {k: (True, True) for k in ids}
        b = {"a": (True, False), "b": (True, False), "c": (True, True)}
        r = cluster_effect(a, b, {k: k for k in ids},
                           {"a": "f1", "b": "f1", "c": "f2"})
        self.assertAlmostEqual(r["cluster_weighted_delta"], 2 / 3)
        self.assertAlmostEqual(r["equal_family_delta"], 0.5)
        self.assertIsNone(r["p_value"])

    def test_reject_cross_family_cluster(self):
        a = {"a": (True, True), "b": (True, True)}
        with self.assertRaises(ValueError):
            cluster_effect(a, a, {"a": "same", "b": "same"},
                           {"a": "f1", "b": "f2"})

    def test_reject_missing_and_invalid_records(self):
        with self.assertRaises(ValueError):
            cluster_effect({}, {}, {}, {})
        with self.assertRaises(ValueError):
            cluster_effect({"a": (False, True)}, {"a": (True, True)},
                           {"a": "c"}, {"a": "f"})
        with self.assertRaises(ValueError):
            cluster_effect({"a": (True, True)}, {}, {"a": "c"}, {"a": "f"})


if __name__ == "__main__":
    unittest.main()
