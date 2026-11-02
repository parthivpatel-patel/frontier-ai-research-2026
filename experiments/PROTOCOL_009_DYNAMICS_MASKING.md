# Protocol 009 — Dynamics masking, unrealizability, and model-data stop gates

Date: 2026-11-02. Status: **exploratory mathematical diagnostic only**. Not a novel theorem or a model benchmark.

## Core methodological question

Can narrowing the physical transition relation make two formally different specifications appear equivalent **on the allowed traces**, even though they are not equivalent on a less restrictive model? Yes, by set inclusion. This is an established consequence of model checking, not a novel research result.

Let T(M) be the set of infinite traces starting at state 0 and respecting the edges of finite model M. If E(M_strict) is a subset of E(M_broad), then T(M_strict) is a subset of T(M_broad). For formulas P and Q, define W_M(P,Q) = {t in T(M): t satisfies P and violates Q}. Therefore W_strict(P,Q) is a subset of W_broad(P,Q). **A witness can disappear under stronger dynamics, but cannot appear.** This does not establish the human-intended meaning of either formula.

A second distinction: if no admissible infinite trace satisfies P, then W_M(P,Q) is empty for every Q. This is *model-relative unrealizability* of P, **not** evidence of semantic equivalence, and it is not automatically the same as classical vacuous satisfaction.

## Pinned experiment

- State set {0,1,2}, initial state 0, a iff state 0, b iff state 2.
- Broad model: 0->{0,1}, 1->{0,1,2}, 2->{1,2}.
- Restricted model: 0->1, 1->2, 2->2; every edge is in the broad model.
- Reference P=G(a->X^3 b), changed Q=G(a->X^n b), n in {1,2,4,6}.
- Check both P-and-not-Q and Q-and-not-P via the existing complete finite-product checker. Check satisfiability of each formula on each model via a separate reachable-safe-cycle algorithm.
- Run: `python -m src.dynamics_masking_audit` and `python -m unittest discover -s tests -v` **only in GitHub Actions cloud**, not on the user's laptop.

## Falsification controls

1. Fail if the supposed restricted edge relation is not a subset of the broad relation.
2. Fail if a restricted separating witness does not exist in the broad model.
3. Explicitly label a required formula that has no satisfying infinite admissible trace.
4. Do not count repeated mutations of one source instruction as independent requirements.
5. Distinguish resource exhaustion from exact negative conclusions.
6. Report both directions, all tested offsets, and all missing witnesses.
7. If independent model checking contradicts the reported classifications, retract the diagnostic.

## Data and literature gate

- English et al., *VLTL-Bench* (2025), https://arxiv.org/abs/2507.00877 , already benchmarks grounded translation and trace-based verification; its upstream code also studies trace sensitivity. This work cannot claim to be first in either area.
- Beer et al., *Efficient Detection of Vacuity in Temporal Model Checking* (2001), DOI https://doi.org/10.1023/A:1008779610539 , and Kupferman & Vardi, *Vacuity Detection in Temporal Model Checking* (2003), DOI https://doi.org/10.1007/s100090100062 , establish prior art on misleading successful verification.
- Potential rights-cleared **different-task** source: Cohn & Blackwell, *QSTRBench* (2026), https://github.com/RobBlackwell/QSTRBench , advertises CC BY 4.0 for its dataset and recorded model results for qualitative spatial/temporal reasoning. This is NOT NL-to-LTL translation; check file-level provenance, model-output terms, and data schemas before importing. Do not combine task metrics. Repository also contains separately licensed third-party tools.
- Potential method baseline: https://github.com/kantaroslab/ConformalNL2LTL (Apache-2.0 repository), which already covers conformal correctness for NL-to-LTL. A repository license does not automatically settle all external dataset or model-output rights.
- VLTL-Bench's GitHub repository has no verified redistribution license as of the previous audit. Do not import its recorded outputs without authorization.

## Confirmatory stop gates

Minimum 30 distinct independently authored and adjudicated source instructions, held-out by source and template, with rights-cleared actual model predictions. Require matched baseline comparisons, source-clustered uncertainty, independent interpretation review, and multiple physical model assumptions. A reduction in discovered mismatches from restricting dynamics is **not** an improvement in semantic correctness. If the physics-specific effect is explained by classical vacuity or trace-selection baselines, reject novelty. If the 30-source gate is unmet, report a feasibility study only.

## Compute, publication, and integrity

Standard GitHub-hosted runners on this **public** repo only; no GPU, paid model inference, secret keys, large downloads, caches or artifacts. GitHub states standard hosted runners are free on public repositories: https://docs.github.com/en/billing/concepts/product-billing/github-actions (rechecked 2026-11-02). Runner availability is not guaranteed; verify each run's conclusion before reporting. No laptop compute. All source and prose AI-assisted, subject to independent scientific review and venue-specific disclosure. November 22 is an internal target, not a promised publication date.
