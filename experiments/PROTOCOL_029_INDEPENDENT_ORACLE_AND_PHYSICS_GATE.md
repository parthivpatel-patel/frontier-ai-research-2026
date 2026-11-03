# Protocol 029 — Independent semantic oracle and physics grounding gate

Date: 2026-11-03. Status: preregistered audit; no new empirical result.

## Audit of Protocol 028

The constructed one-state lasso uses `G prop_0` versus `G prop_1`, with `prop_0=true` and `prop_1=false`. Its disagreement follows immediately from Boolean semantics. This is a software demonstration, **not** an AI-generated specification error, physics result, novel theorem, or external benchmark.

The current exporter calls `find_counterexample` and then `_truth` from the same `src.assumption_lasso_witness` module. The second call verifies the selected valuation, but it is **not an independent semantic oracle**. Shared evaluator defects could pass both checks. The existing SVG also renders a hand-authored state diagram from a known fixture rather than discovering and exporting a witness valuation. These limitations must appear in figure captions.

## Preregistered independent verification

1. Implement a second, separately coded LTL satisfaction oracle on explicit finite lasso graphs, using sets of satisfying states and monotone least/greatest fixed points. Do not call `_truth`, `find_counterexample`, or their private helpers from this oracle.
2. Exhaustively compare the two implementations on syntactically valid formulas from a documented grammar, every lasso of 1–3 states, every loop entry, and every Boolean valuation for at most two propositions. Record grammar, seed (if sampled), cases, runtime, and source commit.
3. Independently verify the semantics of `X`, `F`, `G`, `U`, negation, conjunction, disjunction, and implication, including eventualities that never occur on a cycle. A disagreement is a blocking failure: preserve the smallest reproducible counterexample and do not publish an accuracy claim.
4. Extend the witness API to optionally emit the actual valuation, loop start, formula satisfaction values, and bounds for **constructed fixtures only**. Preserve the current privacy-safe API for external text. Render figure geometry from the returned witness record rather than manually duplicating a known example.
5. Make GitHub Actions archive the JSON, SVG, provenance manifest, test logs, and the oracle cross-check report. Verify a successful run and artifact IDs before describing outputs as cloud-verified.

## Physics-grounding requirement

The proposition-identity assumption is currently imposed syntactically. It is not evidence of physical equivalence. Before calling a study physics-grounded, define a physical dynamical system, measurement map from state to propositions, noise/uncertainty model, and an independently testable source of equivalence constraints. Prefer a transparent synthetic dynamical system initially, with explicit labeling; do not imply validation on real instruments or robots.

Compare at least three conditions: no identity constraints, correct physically derived constraints, and intentionally wrong constraints. Evaluate witness validity, false equivalence claims, coverage, runtime, and abstention. Include a negative control where incorrect constraints conceal a genuine disagreement. A method that improves apparent agreement only by suppressing valid witnesses is falsified as a reliability improvement.

## Closest prior-art families requiring explicit comparison

Classical LTL model checking and automata-theoretic verification; bounded model checking and lasso witnesses; abstraction and counterexample-guided abstraction refinement; runtime verification and temporal logic robustness; natural-language-to-temporal-logic translation; neuro-symbolic constraint checking; specification mining and formal methods for learned systems. A novel claim cannot rest on using bounded lasso search, proposition aliasing, or plotting a witness. Search and cite primary publications before claiming differentiation.

## Decision gates

**Gate A:** independent oracle cross-check passes and original cloud artifacts are retrievable.

**Gate B:** proposition constraints are derived from an explicit model and tested against incorrect-constraint controls.

**Gate C:** external, legally reusable evaluation set with documented provenance and no leakage; strong baselines; preregistered metrics; uncertainty intervals; ablations.

**Gate D:** closest-prior-art audit supports a precisely delimited claim, and negative results are reported. If any gate fails, release a technical report or replication note rather than asserting a novel paper.

## Resource policy

Only standard-library Python and bounded CPU experiments on a verified free GitHub Actions allowance; no laptop execution, paid inference, cloud billing changes, or large downloads. Check repository/account Actions quota and billing settings before expanding compute. Do not assume public-repository runner access means unlimited free compute.

Publication target November 22, 2026 is aspirational and subordinate to evidence. Disclose AI assistance and tool provenance in accordance with venue policies.
