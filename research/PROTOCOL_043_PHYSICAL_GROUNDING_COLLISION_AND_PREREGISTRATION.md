# Protocol 043 — Physical grounding collision audit and preregistered evaluation

Date: 2026-11-03. Status: design only; no experiment executed; no novelty or performance established.

## Closest prior art and collision assessment

1. **SENTINEL** (Zhan et al., 2025; https://arxiv.org/abs/2510.12985) already combines natural-language safety requirements, temporal logic, plan checking, and physically detailed trajectory verification for embodied agents. Therefore a broad claim that this project first joins LLMs, physics, and formal verification is untenable. The paper must explicitly compare against its semantic/plan/trajectory decomposition, and distinguish scientific claim verification from embodied-agent safety.
2. **GinSign** (English et al., 2025; https://arxiv.org/abs/2512.16770) learns grounding of language spans to typed system-signature predicates and constants. This challenges any claim that typed predicate grounding or lightweight non-LLM grounding is new. Include a typed-signature grounding baseline.
3. **VLTL-Bench** (English et al., 2025; https://arxiv.org/abs/2507.00877) supplies state spaces, grounded temporal specifications, traces, and intermediate ground truth. Use as an external benchmark; do not claim that grounded NL-to-LTL evaluation is novel.
4. **NeuroNL2LTL** (Quansah and Bonnah, 2026; https://arxiv.org/abs/2605.22874) uses an intermediate representation and verifier feedback. This challenges claims of novelty for intermediate representations and verifier-in-the-loop repair.
5. Classical forward simulation, model checking, and counterexample-guided abstraction refinement are prior art, not proposed algorithmic inventions.

These are abstract-level comparisons only. Before publication, inspect full papers, implementations, licenses, datasets, and evaluation protocols; do not infer absent capabilities from abstracts.

## Narrow research question

Given a fixed natural-language scientific requirement and an independently authored physical transition model, does a **traceable evidence gate** (typed grounding + explicit physical assumptions + independently checkable certificate + abstention on unresolved assumptions) reduce *unsafe accepted claims* relative to equally resourced NL-to-logic and verifier baselines **at matched acceptance coverage**?

A reduction is an empirical hypothesis, not a finding. The contribution, if any, must be a demonstrated combination of evaluation design, failure taxonomy, or a specific new technique that survives prior-art scrutiny.

## Pre-registration: examples and partitions

Build at least three families with manually reviewed ground truth: (A) finite-state kinematics/energy constraints, (B) discrete conservation or flow constraints, (C) temporal safety requirements with observation aliasing. Use exact rational arithmetic where feasible. Include physically impossible but logically satisfiable traces; valid physical counterexamples; ambiguity in units, reference frames, and boundary conditions; incomplete models; and intentionally wrong physical assumptions.

Separate source templates and physical-system structures between development and held-out test. Prevent near-duplicate paraphrase leakage. Freeze the test manifest, seeds, baseline configurations, and acceptance criteria before measuring outcomes. Record provenance and licensing for every sample.

## Baselines and ablations

B0: deterministic template/typed parser plus classical model checking.
B1: NL-to-logic translation with manually supplied correct grounding and identical verifier.
B2: NL-to-logic with automatically predicted typed grounding and identical verifier.
B3: B2 plus independent physical-model certificate gate.
B4: B3 plus explicit abstention for incomplete or unverified assumptions.

If no genuinely free, authorized model inference endpoint is available, execute deterministic B0 and the exact-arithmetic controls first; mark learned-model baselines as blocked, not simulated. Do not compare against an imaginary model output.

## Primary endpoint and statistical plan

Primary: unsafe-acceptance rate among all labeled unsafe cases, reported with numerator, denominator, and uncertainty interval, at matched overall acceptance coverage. Secondary: selective risk/coverage curve, false rejection, grounding accuracy, certificate-checker disagreement, latency, and abstention by failure class. Report both macro-averaged domain scores and micro-averaged sample scores. Use paired bootstrap at the physical-system/template cluster level; disclose seeds and all attempted specifications. No significance or superiority claim without completed runs.

## Falsification / stop criteria

Reject a positive contribution claim if (1) improvements disappear at matched coverage, (2) typed grounding or classical checking matches performance, (3) a single physical-model error yields unsafe 'verified' outputs without detection, (4) leakage or baseline inequity explains gains, (5) independently reproduced results disagree materially, or (6) full-text literature audit finds an equivalent previously published approach. Publish negative outcomes when scientifically useful.

## Cloud-only, zero-cost execution gate

GitHub documentation states standard GitHub-hosted runners in public repositories are free; larger runners are billed, and storage has plan-specific allowances. Sources: https://docs.github.com/en/actions/concepts/billing-and-usage and https://docs.github.com/en/billing/reference/actions-runner-pricing (checked 2026-11-03). This is platform-level eligibility, **not** verification of account billing settings, repository visibility at dispatch, artifact storage usage, or available runner capacity. Before any run: confirm repository is public, workflow uses only standard ubuntu-latest, no paid marketplace actions/services, no GPU/larger runner, no billable storage expansion, and account-specific safeguards; set timeout-minutes and concurrency cancellation; keep artifacts small and short-lived. Do not trigger workflows until these checks are complete. User laptop is browser-only.

## Reproducibility and integrity

Keep exact source code, environment versions, immutable input hashes, seeds, raw predictions, trace witnesses, certificate checker decisions, workflow URLs, and raw CI logs. Distinguish authored tests from executed tests. Disclose AI assistance as required by publication policy. Do not claim an original physics theorem or general continuous-system guarantee from finite-state controls.

## Immediate next implementation

Add a manifest-driven benchmark validator that checks domain-disjoint splits, sample identifiers, units, model-assumption provenance, and output evidence before evaluation. First test it with synthetic fixtures on confirmed free cloud compute. Only then launch a controlled benchmark, after the cloud billing gate is verified.
