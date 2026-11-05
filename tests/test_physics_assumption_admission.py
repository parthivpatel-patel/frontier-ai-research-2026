"""Protocol 084: assumption-admission negative controls for constructed physics seeds.

This module is a proposed validation layer, not an independently adjudicated
physics benchmark. Execute only on a verified zero-cost hosted runner:
python -m unittest discover -s tests -p 'test_physics_assumption_admission.py'
"""
import unittest
from decimal import Decimal, InvalidOperation
from test_physics_seed_records import RECORDS, predicted_value

ARITY = {"newton": 2, "kinematics": 3, "kinetic_energy": 2, "ohmic_circuit": 2}

def admitted_prediction(domain, parameters, assumptions):
    """Return an arithmetic consequence only when explicitly scoped premises hold.

    This intentionally does not infer physical assumptions from numeric inputs.
    It is a reference admission gate for negative controls, not a general solver.
    """
    if domain not in ARITY:
        raise ValueError("unsupported domain")
    if len(parameters) != ARITY[domain]:
        raise ValueError("wrong parameter count")
    if not isinstance(assumptions, dict) or assumptions.get("model_valid") is not True:
        raise ValueError("model applicability not certified")
    try:
        p = tuple(Decimal(x) for x in parameters)
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("invalid numerical parameter") from None
    if any(not x.is_finite() for x in p):
        raise ValueError("nonfinite parameter")
    if domain == "newton" and p[1] <= 0:
        raise ValueError("mass must be positive")
    if domain == "kinetic_energy" and p[0] <= 0:
        raise ValueError("mass must be positive")
    if domain == "ohmic_circuit" and p[1] <= 0:
        raise ValueError("resistance must be positive")
    if domain == "kinematics" and p[2] < 0:
        raise ValueError("time interval must be nonnegative")
    return predicted_value(domain, parameters)

class AssumptionAdmissionControls(unittest.TestCase):
    def test_existing_candidates_require_explicit_applicability(self):
        for row in RECORDS:
            with self.subTest(record=row[0]):
                self.assertEqual(admitted_prediction(row[2], row[3], {"model_valid": True}),
                                 predicted_value(row[2], row[3]))

    def test_missing_or_false_applicability_rejected(self):
        for premise in ({}, {"model_valid": False}, {"model_valid": "true"}, None):
            with self.subTest(premise=premise):
                with self.assertRaises(ValueError):
                    admitted_prediction("newton", ("6", "2"), premise)

    def test_undefined_and_nonphysical_inputs_rejected(self):
        cases = (
            ("newton", ("6", "0")),
            ("newton", ("6", "-2")),
            ("kinetic_energy", ("-4", "3")),
            ("ohmic_circuit", ("12", "0")),
            ("ohmic_circuit", ("12", "-4")),
            ("kinematics", ("1", "2", "-3")),
            ("newton", ("NaN", "2")),
            ("newton", ("Infinity", "2")),
            ("newton", ("6",)),
            ("newton", ("6", "2", "3")),
        )
        for domain, params in cases:
            with self.subTest(domain=domain, params=params):
                with self.assertRaises(ValueError):
                    admitted_prediction(domain, params, {"model_valid": True})

    def test_assumption_failure_is_not_false_claim_label(self):
        # A failed applicability gate yields no truth label. This is not a
        # proof that any asserted value is physically false.
        with self.assertRaisesRegex(ValueError, "applicability"):
            admitted_prediction("ohmic_circuit", ("12", "4"), {"model_valid": False})

    def test_unsupported_domain_rejected_before_arithmetic(self):
        with self.assertRaises(ValueError):
            admitted_prediction("quantum", ("1", "2"), {"model_valid": True})

if __name__ == "__main__":
    unittest.main()
