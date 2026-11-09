"""Protocol 159: deterministic paired-discordance oracle, no model inference.

Run in verified zero-cost cloud CI: python -m unittest tests.test_protocol_159_paired_discordance_contract
"""
import math
import unittest


def paired_oracle(a, b):
    """Return paired unconditional-correctness and selection accounting.

    Inputs are mappings from immutable original-problem IDs to
    (returned: bool, correct: bool | None) tuples. For abstentions,
    correct must be None. This is a fixture oracle, not a production metric.
    """
    if not isinstance(a, dict) or not isinstance(b, dict):
        raise ValueError("manifests must be mappings")
    if set(a) != set(b):
        raise ValueError("unpaired original-problem IDs")
    if not a:
        raise ValueError("empty paired sample")

    def validate(record):
        if not isinstance(record, tuple) or len(record) != 2:
            raise ValueError("invalid record")
        returned, correct = record
        if type(returned) is not bool:
            raise ValueError("returned must be bool")
        if returned:
            if type(correct) is not bool:
                raise ValueError("correct must be bool for returned answer")
        elif correct is not None:
            raise ValueError("abstention must not carry correctness")
        return returned, (returned and correct)

    counts = {"n11": 0, "n10": 0, "n01": 0, "n00": 0}
    selection = {"both": 0, "a_only": 0, "b_only": 0, "neither": 0}
    for key in a:
        ar, ay = validate(a[key])
        br, by = validate(b[key])
        counts["n" + str(int(ay)) + str(int(by))] += 1
        selection["both" if ar and br else "a_only" if ar else "b_only" if br else "neither"] += 1
    n = len(a)
    n10, n01 = counts["n10"], counts["n01"]
    discordant = n10 + n01
    # Exact two-sided conditional binomial test, valid for independent pairs.
    p = min(1.0, 2.0 * sum(math.comb(discordant, k) for k in range(min(n10, n01) + 1)) / (2 ** discordant))
    return {"n": n, **counts, **selection, "delta_yield": (n10 - n01) / n,
            "p_independent_pairs": p}


class PairedDiscordanceContract(unittest.TestCase):
    def test_disjoint_selection_equal_coverage(self):
        a = {i: (i < 2, True if i < 2 else None) for i in range(4)}
        b = {i: (i >= 2, True if i >= 2 else None) for i in range(4)}
        r = paired_oracle(a, b)
        self.assertEqual((r["both"], r["a_only"], r["b_only"]), (0, 2, 2))
        self.assertEqual(r["delta_yield"], 0)
        self.assertEqual(r["p_independent_pairs"], 1)

    def test_complete_abstention(self):
        x = {"p": (False, None), "q": (False, None)}
        r = paired_oracle(x, x)
        self.assertEqual(r["n00"], 2)
        self.assertEqual(r["neither"], 2)
        self.assertEqual(r["p_independent_pairs"], 1)

    def test_all_discordant_one_direction(self):
        a = {i: (True, True) for i in range(6)}
        b = {i: (True, False) for i in range(6)}
        r = paired_oracle(a, b)
        self.assertEqual(r["n10"], 6)
        self.assertEqual(r["delta_yield"], 1)
        self.assertEqual(r["p_independent_pairs"], 0.03125)

    def test_identical_outputs(self):
        x = {"p": (True, False), "q": (True, True), "r": (False, None)}
        r = paired_oracle(x, x)
        self.assertEqual((r["n11"], r["n00"], r["n10"], r["n01"]), (1, 2, 0, 0))

    def test_reject_unpaired_and_malformed(self):
        with self.assertRaises(ValueError):
            paired_oracle({"a": (True, True)}, {"b": (True, True)})
        for bad in [(False, True), (False, False), (True, None), (1, True), (True, 1)]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                paired_oracle({"a": bad}, {"a": (True, True)})
        with self.assertRaises(ValueError):
            paired_oracle({}, {})


if __name__ == "__main__":
    unittest.main()
