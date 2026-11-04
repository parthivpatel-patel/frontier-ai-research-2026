# Protocol 061 — Physics verification novelty gate (2026-11-04)

Status: literature-scoping audit, **not** a claim of novelty, benchmark accuracy, or successful inference. Research remains independent of other repositories.

## Closest verified benchmark precedents

1. **PHYBench (NeurIPS 2025 Datasets and Benchmarks)**: 500 original physics problems, curation to reduce flawed items, and expression-edit-distance evaluation. https://papers.nips.cc/paper_files/paper/2025/hash/01e793f8cf5689aa0ea46a1b01071bea-Abstract-Datasets_and_Benchmarks_Track.html
2. **TPBench (2025)**: 57 theoretical-physics problems across undergraduate and research difficulty, evaluated with open and closed models. https://arxiv.org/abs/2502.15815
3. **QuantiPhy (CVPR 2026)**: more than 3,300 video/text quantitative physics instances with numerical kinematic ground truth; tests input faithfulness and physical numerical accuracy. https://quantiphy.stanford.edu/

These works defeat any unqualified claim that evaluating LLM physical reasoning, curating original physics questions, checking numerical answers, or measuring input faithfulness is novel. The present project must instead test whether *auditable, assumption-explicit certificates for language-derived physical claims* improve selective safety at matched coverage, including unresolved-truth bounds and source-clustered uncertainty. This is a **hypothesis**, not an established contribution.

## Discriminating experiment

Pre-register source families before seeing model outputs. Collect independently adjudicated claims with explicit physical regime, units, boundary conditions, dimensional consistency, numerical tolerance, provenance and adjudicator disagreement. Reserve a source-disjoint holdout. Include adversarially altered assumptions, missing parameters, ambiguous reference frames and impossible constraints. Never assign truth to unresolved cases merely to complete a benchmark.

Compare (A) answer-only acceptance, (B) language-only self-critique, (C) symbolic/dimensional checks without certificate provenance, (D) full assumption-explicit certificate verification, and (E) a matched-coverage randomized abstention control. Hold model, prompts, budget, data and threshold selection fixed where applicable; report compute and token cost.

Primary outcome: unconditional unsafe acceptance difference at a *predeclared matched coverage*, on adjudicated claims, with source-clustered uncertainty. Also report the full-population sharp partial-identification interval when truth is unresolved; report coverage, selective error, false rejection, source families and failure categories separately. Use paired source-level bootstrap only when enough independent clusters exist; otherwise report descriptive results without inferential claims.

## Falsification and stop criteria

- No defensible improvement if the paired uncertainty interval includes zero or the partial-identification interval does not establish a strict safety advantage.
- No claimed certificate benefit if a dimensional-only checker or matched abstention achieves comparable performance.
- No claimed generalization if results fail on held-out source families or perturbed physical assumptions.
- No claimed physical correctness where labels are disputed, solver assumptions are invalid, or certificate generation leaks reference answers.
- No publication-level empirical claim from synthetic unit tests alone.
- If benchmark size, cloud access, or independent adjudication is inadequate by 2026-11-22, release a methods/pre-registration report rather than an unsupported empirical paper.

## Reproducibility manifest requirement

For each experiment record: repository SHA, workflow/run URL, UTC start, runner type, runner cost eligibility, source family split hash, raw example manifest, adjudication provenance, baseline versions, threshold-freeze artifact, outputs, hashes, statistical script version and limitations. Do not treat a successful CI unit-test run as an AI benchmark.

## Zero-cost cloud gate

GitHub's billing documentation says **standard GitHub-hosted runners in public repositories are free**, while larger runners are charged even in public repositories. Official source: https://docs.github.com/en/billing/concepts/product-billing/github-actions . Use only a standard hosted runner on this confirmed public repository; no larger runners, paid model APIs, Codespaces, artifact accumulation, or external GPU services. Public-runner policy does not establish account-specific storage/budget status, so verify settings before any nontrivial new execution. No local laptop computation.

## Disclosure

Record model assistance and any generated claims/labels in the research log. No fabricated results, no asserted first-ever novelty, and no claims of human-only authorship when assistance was used.
