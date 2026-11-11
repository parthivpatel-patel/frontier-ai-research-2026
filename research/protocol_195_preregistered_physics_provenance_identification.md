# Protocol 195 — Preregistered physics-provenance intervention and identification plan

Date: 2026-11-11. Status: design-only; no data, labels, model runs, or findings.

## Why this protocol is necessary

Protocols 190–194 address a **combinatorial eligibility** question conditional on an admissibility relation A. They do not show that a language model distinguishes genuine scientific support from graph formatting, unfamiliar edges, token distribution, or answer-position cues. The experimental contribution must be evaluated separately from established max-flow and graph-switching methods.

## Units, outcomes, and estimands

A unit is a frozen (physics problem, derivation, citation/provenance graph, prompt template, model version, decoding configuration) tuple. A qualified human physics adjudicator must independently label each permitted edge before seeing model outcomes. Preserve source passages, equations, assumptions, units, and the reason for each admissible/inadmissible judgment.

For each eligible unit i, construct a matched pair: Z=0 original correct provenance and Z=1 degree-preserving graph with at least one adjudicated invalid edge. Preserve every visible statement and numerical value; change only the designated provenance links. If tokenization or serialization length changes, record it and create a matched presentation control.

Primary outcome Y_i(z): binary model judgment that the **specified support relation** is valid, scored against the independently fixed answer key. Secondary outcomes: final physics-answer accuracy, calibrated confidence if supported, refusal/abstention, and citation-edge localization. Do not substitute a model-generated explanation for independent correctness.

Define paired intention-to-treat contrast Δ = E[Y_i(1)-Y_i(0) | eligible, sampled by preregistered rule]. This is an effect of the *entire graph intervention*, not by itself an effect of recognizing provenance truth. State the eligible-population restriction. Fix sampling and seed before model queries; never select units using model responses.

## Negative and positive controls

1. **Presentation sham:** serialize an unchanged graph with a matched nonsemantic formatting perturbation. If the sham effect approaches the graph effect, do not claim provenance-specific sensitivity.
2. **Semantically valid reassignment:** use a structurally changed graph whose edges are all independently admissible, when feasible. The expected invalidity judgment must not be triggered solely by rearrangement.
3. **Unsupported but visually plausible citation:** keep the same citation style, edge count, and degree margins while using independently invalid support.
4. **Physics-content sanity control:** ask a separately blinded evaluator to solve/check the physics without provenance. Discard or flag ambiguous underlying physics; do not infer invalidity from model disagreement.
5. **Answer-position/order counterbalance:** swap ordering and source identifiers with deterministic permutations, retaining the exact adjudicated relation.
6. **Null/no-evidence baseline:** assess whether the model defaults to accepting citations without reading support.

The primary comparison and control-family thresholds must be registered before observing responses. If controls fail, report the graph-intervention effect descriptively and reject the stronger mechanistic interpretation.

## Analysis and falsification

- Pair outcomes by problem, not by query as an independent observation. Report paired discordances, effect estimate and confidence interval; cluster or hierarchically resample by source problem if multiple templates/graphs share content.
- Preregister one primary model and one primary prompt/temperature; other models are external-validity replications, not extra chances to discover a positive result.
- Report all attempted problems, infeasible interventions, adjudicator disagreements, invalid inputs, model refusals, and API failures. Separate local two-switch eligibility from global fixed-margin eligibility.
- Explicit falsification: no reliable difference from sham; valid-reassignment control also flagged invalid; effects disappear under identifier permutation; independent adjudicators cannot agree on labels; physics answer key is unstable; apparent effects only emerge after selective exclusions; or paired uncertainty includes substantively negligible effects.
- No p-value, confidence interval, performance result, or novelty claim is currently available. A null result is publishable as a methodological limitation if faithfully reported.

## Prior-art overlap to resolve before novelty claims

Compare full texts and evaluation protocols of Turpin et al. (2023, unfaithful chain-of-thought explanations), Lightman et al. (2023, process supervision), Gao et al. (2023, citation evaluation), and subsequent work on attribution, counterfactual faithfulness, graph perturbation, and physics reasoning. Build a claim-by-claim matrix: existing intervention type, causal unit, semantic oracle, controls, physics domain, and mathematical certification. A new combination of familiar techniques is not automatically a novel contribution.

## Cloud and cost gate

No workflow may be dispatched merely because GitHub Actions offers a published free allowance. Before running, verify **current** GitHub-hosted runner entitlement, minutes/storage remaining for this specific repository/account, billing configuration and spending limits, public-repository eligibility, runner availability, and any required card/verification. Record a timestamped evidence receipt. If any check is unavailable, execution is BLOCKED. Avoid third-party inference APIs until their current free tier, quotas, card requirements, and data-use terms are independently checked. Do not use the user's laptop for compute. No paid fallback, auto-upgrade, or unbounded workflow.

Once verified, first run the existing standard-library Protocol 191–194 tests on a bounded CPU-only GitHub-hosted runner, using a timeout, no secrets, read-only permissions, and no external downloads. Only after regression success and physics-label audit should any model experiment be considered.

## Deliverable gates for November 22

A research manuscript may be publicly released as a **methods/protocol/preliminary negative-result** paper if it clearly states what was actually executed. An empirical causal or model-performance paper requires verified execution logs, independently adjudicated examples, preregistered outcomes, and complete analysis. Do not represent protocol text or unexecuted tests as experimental findings.

No compute or cloud job was started in preparing this protocol; no spending incurred. Scientific novelty remains unproven.
