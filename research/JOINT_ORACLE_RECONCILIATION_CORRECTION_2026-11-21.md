# Joint oracle reconciliation correction — 2026-11-21

## Verified repository facts
A fresh default-branch directory inventory and direct file reads confirm that `research/paired_archival_oracle.py` (blob `fe1fb4378b35047e7ba7b99f6566056366dfa63e`) and `research/test_paired_archival_oracle.py` (blob `f19f8ea5258ec1c3158c4449de1f20e4e6129d00`) **do exist on main**. The earlier reconciliation note checked a different filename, `paired_archival_joint_bounds.py`, and therefore its missing-path observation did not establish missing implementation. Retain that note as a historical record but supersede its implication here.

The implementation enumerates one shared binary truth vector across both policies, uses exact rational selective-risk differences, rejects mismatched frames, and reports undefined risks. Eight authored unit tests cover identical/opposite predictions, abstention, empty missing frame, undefined risk, frame mismatch, enumeration limit, and invalid input.

## Outstanding verification
Reading source files is **not execution**. No successful CI run tied to the exact current main commit and executing these eight tests was established by this inspection. An earlier successful toy-falsification workflow is not sufficient. Before claiming validation, inspect a workflow run's head SHA, command, exit code, and test counts. Verify the applicable GitHub-hosted runner free-tier and billing restrictions before dispatching additional runs; do not assume unlimited free compute.

## Methodological caveats
The sharp interval is conditional on fixed predictions and acceptance decisions on unresolved examples; it does not identify risks when acceptance itself depends on unknown truth or when verified-case labels are uncertain. The `max_missing=16` guard permits up to 65,536 assignments and is a protective cap, not a scalability guarantee. Marginal containment is an internal consistency check, not an independent correctness proof. The result is an identification interval, not a sampling confidence interval.

## Next tests and release gate
Add independent handwritten microcase calculations, property tests for simultaneous policy swapping (sign reversal), verified-case label sensitivity, and missing-case permutation invariance. Confirm exact-head cloud CI before calling the implementation tested. No held-out model-performance or scientific novelty claim follows from these fixtures. Publication should remain methods/preregistration only pending independent data, a completed prior-art audit, and accurate AI-assistance disclosure.
