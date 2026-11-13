# Protocol 061 — Audit-label firewall, pre-registration, and evaluation leakage gate

Status: research protocol, not an empirical finding. Date: 2026-11-13.

## Motivation and scope

Protocols 055–060 establish mathematical limitations and exact finite-population audit fixtures. They do not establish an original AI method. The next empirical risk is **evaluation leakage**: an audit system can look calibrated by selecting which claims to audit, selecting model thresholds, or choosing reported subgroups after seeing their truth labels. Even a mathematically valid inclusion-probability witness cannot repair such leakage.

This protocol applies jointly to natural-language claims, formal mathematical statements, and physics claims (including units, dimensions, boundary conditions, and regime of validity). The three domains must also be reported separately.

## Frozen experimental objects

Before accessing held-out truth labels, version and hash: (1) the claim population and family identifiers, (2) source documents and any near-duplicate grouping, (3) verification prompts and verifier versions, (4) audit-design probabilities and complete sampling-design witness where applicable, (5) calibration procedure, (6) abstention and escalation thresholds, (7) primary estimands, (8) uncertainty method, (9) baseline definitions, and (10) exclusion criteria.

Do not tune any of these using the held-out evaluation labels. If an unavoidable change occurs, mark the original evaluation exploratory and create a fresh untouched evaluation partition.

## Family-disjoint splitting

Split by provenance family **before** generating paraphrases or perturbations. A family includes shared source theorem, proof template, physical model, numerical example, or upstream document. All derivatives remain in the same partition. Record duplicate-detection rules before evaluation; report sensitivity to alternative grouping.

Calibration and threshold tuning use development families only. The test set is a single-use, held-out set. A claim whose correctness is ambiguous or depends on an unspecified physical regime must not be silently coded false or true; record an adjudication state and pre-specified handling.

## Audit selection and identification

A selected audit subset is not representative by default. Record audit probabilities and the actual realized sample, including empty samples and nonresponse. Never estimate inclusion probabilities by inspecting held-out truth labels. If the design has zero inclusion probability for a claim, full-population truth totals generally cannot be identified without additional assumptions. If pairwise inclusion probabilities vanish, a conventional unbiased design-based variance estimator may be unavailable; use a defensible conservative bound, change the design, or state that uncertainty is not identified.

An exact complete-design witness certifies a **supplied** design; it is not a general-purpose feasibility solver and does not certify the data-generating process.

## Primary comparison and stopping rule

Pre-register a primary endpoint: false acceptance rate among released claims at a fixed target release coverage, reported by domain and pooled only with pre-specified domain weights. The proposed dependence-aware verifier must be compared against (a) a calibrated single verifier, (b) naive independent-evidence aggregation, (c) duplicate/family-aware aggregation, and (d) selective prediction with calibration and matched coverage. All methods receive identical information and audit budgets.

Report false rejections, audit cost in number of human/independent labels, abstention rate, and worst-family error. Use family-level uncertainty and design-aware audit uncertainty; show sensitivity to shifts in claim family and verifier error correlation.

A claimed gain is **falsified** if it disappears under family-disjoint evaluation, matched coverage and equal audit budget, a stronger calibrated baseline, or an independent replication. If uncertainty intervals do not separate, state inconclusive rather than successful.

## Multiple testing and transparent reporting

Freeze one primary comparison before test-label access. Label all additional metrics and subgroup analyses secondary or exploratory. If several variants are tested, disclose the complete search and use an appropriate multiplicity correction or a new confirmation set. Report failures, missing labels, code and prompt revisions, seed schedules, and exact model versions.

## Zero-cost execution gate

Do not launch a cloud workflow until repository-specific Actions entitlement, standard-runner eligibility, workflow permissions, usage limits, and any billing/card exposure have been checked. Use only standard free public-repository runners with explicit timeout, concurrency, and no paid external API, large runner, artifact-retention expansion, or paid storage. Published free-tier policy is not proof of account-level availability. Do not use the user's laptop for training, inference, downloads, or simulations.

## Novelty and publication gate

Prior art includes selective classification, conformal risk control, dependence-aware ensemble aggregation, survey sampling, partial identification, active learning, and audit allocation. A practical combination of these is not automatically novel. Any proposed contribution must specify the exact theorem, algorithm, or empirically demonstrated capability absent from the closest prior work, with direct paper-by-paper comparison.

No public manuscript should claim validated reliability, original theory, or superior performance until independent literature verification and cloud-executed, reproducible held-out tests support those claims. Disclose AI assistance and limitations in accordance with the chosen venue.

## Immediate reproducible deliverables

1. Add a machine-readable frozen evaluation manifest with dataset-family partition hashes and protocol version.
2. Add negative controls for leaked paraphrase families, label-dependent audit selection, and test-set threshold tuning.
3. Confirm account-specific free-cloud safeguards; then run existing exact-rational fixtures and publish their logs.
4. Audit the closest published methods and document precisely which contribution, if any, survives.

No tests or cloud workloads were executed as part of this protocol-only commit.
