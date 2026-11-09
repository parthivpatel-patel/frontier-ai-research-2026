# Protocol 158 — Paired discordance and matched-coverage identifiability

Date: 2026-11-09. Status: preregistered mathematical audit; no model results.

## Motivation
Protocols 154–157 distinguish unconditional yield, selective accuracy and family weighting. Equal coverage alone does not make two selective verifiers answer the same items. A comparison must preserve case identity and report *where* decisions disagree.

## Required paired record
For each held-out original problem i, record: immutable problem_id, physics_family, paraphrase_group_id, system_id, returned (Boolean), correct (Boolean only when returned), and evaluation split. A missing response is not silently a wrong answer; define a separately reported failure/timeout class. The paired analysis requires exactly one valid record per (problem_id, system_id), matching original IDs across systems, and no train/test group overlap. Abstentions contribute zero to unconditional correct-answer yield, but are excluded from conditional accuracy denominators.

Let Y_Ai = 1 if A returns a correct answer and 0 otherwise, and Y_Bi likewise. Define n10 = count(Y_A=1,Y_B=0) and n01 = count(Y_A=0,Y_B=1). For N paired independent original problems,

  Delta_yield = (n10 - n01) / N.

The common successes and failures cancel in the paired difference. Under a sharp equal-probability null conditional on D=n10+n01 discordant pairs, n10 is Binomial(D, 1/2). A two-sided exact McNemar-style p-value is min(1, 2 * P[Binomial(D,1/2) <= min(n10,n01)]). This exact binomial calculation is inappropriate when original problems are dependent, or paraphrases from one original are treated as independent. In those settings, resample independent original-problem clusters or, if the estimand is across physics families, report family-level contrasts and sensitivity; small numbers of families limit uncertainty claims.

## Constructed falsification example
Two systems each return exactly two answers across four cases. A returns on {1,2}; B returns on {3,4}. Equal coverage = 1/2, yet their answer sets are disjoint. Comparing conditional accuracy without matched answer-set disclosure confounds selection with correctness. This is a mathematical counterexample, not empirical evidence.

## Required analysis
1. Report N, both coverage rates, overlap of returned sets, the 2x2 returned/abstained contingency table, and the 2x2 unconditional-correctness contingency table.
2. Report both unconditional yield and selective accuracy, plus incorrect-answer yield and timeout rate.
3. Use original-problem IDs as resampling units, with paraphrase variants nested inside them; do not bootstrap individual paraphrases independently.
4. Predefine family weighting (case-weighted and equal-family), uncertainty procedure, random-abstention baseline, and an always-answer baseline.
5. Treat zero-return selective accuracy as undefined, not zero.
6. Report both matched-return subset accuracy (descriptive, post-selection) and full paired yield (primary); do not treat matched-return subset as causal.
7. Apply multiple-comparison correction if searching across families, prompts, thresholds or verifier variants.

## Falsification and release gates
- Reject a claimed unconditional benefit when the paired confidence interval includes zero or the sign reverses under preregistered family weighting.
- Reject a claimed selective-reliability benefit when it disappears against a matched-coverage random-abstention control, or only arises through disjoint selection without demonstrated utility improvement.
- Reject leakage-sensitive results when original-problem or paraphrase groups cross train/test boundaries.
- Do not claim a new statistical theorem: the paired binary analysis and McNemar test are established methods.
- Do not claim physics/NLP performance, novelty, coverage guarantees or publication readiness before independent experiments and prior-art checks.

## Deterministic implementation acceptance criteria
Build a standard-library-only oracle accepting two manifests keyed by original problem ID. Reject duplicates, missing IDs, invalid Booleans, and correct=True on an abstention. Verify n10+n01 plus concordant cells equals N; verify Delta equals the direct difference in per-system unconditional yields. Verify the four-case disjoint-coverage example, complete abstention, and identical outputs. Tests are specified here but not claimed executed.

## Cost and integrity
No training, model inference or large downloads are needed to review this protocol. Cloud test execution must wait for verified account-specific $0 quota and billing safeguards. All code, datasets, model provenance, generated content and AI assistance should be disclosed consistent with venue policy.
