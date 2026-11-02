# Protocol 005 — Minimal learned NLP feasibility and source-disjoint evaluation gate

Date: 2026-11-01 US Eastern. **Exploratory engineering study only. Not a new scientific method.**

## Data provenance
External source: Chiari & Mateis, *Datasets supporting automated requirement formalization from natural language to temporal logic*, Zenodo, 2026-10-25, https://zenodo.org/records/23649257 . Source commit a38a73a351c07a3d17cb561098485cd4416c5375; 25-row CSV blob 6f6d2e01707e777be9cd0197698f8f19b4381fc8. The authors explicitly do **not** certify semantic labels as ground truth. Only the five strict temporal-offset rows from ONE original requirement are adjudicated.

## Trained model and controls
- Training: 45 **synthetic** labeled texts (5 independently authored paraphrase templates x the nine number words one–nine). No external requirement is in training.
- Model: genuinely fitted multinomial naive Bayes on lowercase word counts, Laplace smoothing, equal class counts, no external dependencies. The task is classification of a numeric temporal offset, **not** NL-to-LTL generation, reasoning, or physical simulation.
- External evaluation: five strict-template mutations, with target offset independently extracted from the unambiguous numeric phrase. The inherited source formula encodes offset 3; all five mutated rows encode another offset. No other 20 source rows are labeled.
- Ablation: retrain and evaluate after masking all number words. This asks whether the model exploits the number token rather than temporal reasoning.
- Leakage check: exact external sentences absent from training. The training templates are authored and not sampled from the external CSV.
- Independent sample unit: original human requirement, not its repeated mutations. External sample size in independent units is **ONE**. Do not calculate population confidence intervals or treat 5 rows as 5 independent tasks.

## Cloud-verified results
GitHub Actions run: https://github.com/parthivpatel-patel/frontier-ai-research-2026/actions/runs/41381210222 ; 76/76 unit tests passed on a standard GitHub-hosted runner.

| Diagnostic | Observed | Scope |
| --- | ---: | --- |
| Synthetic training examples | 45 | 5 authored templates x 9 labels |
| Strict held-out external mutations | 5 | One original requirement |
| Learned model correct on those mutations | 5/5 | Number-word extraction only |
| Number-masked learned model correct | 1/5 | Ablation; ties resolve to label 1 |
| Inherited formula mismatches | 5/5 | Label inheritance, not model prediction |
| Independent external source instructions | 1 | **No statistical generalization** |

These numbers are directly present in the cloud run log. Perfect 5/5 accuracy is **not** evidence of reliable NLP, broad generalization, or novel research: all examples use the same source wording, the task is simple, and the labels are extracted under a very narrow grammar. The ablation confirms reliance on the explicit number token.

## Publication and falsification gate
**BLOCKED** until:
1. At least several dozen independently authored source requirements across multiple temporal patterns can be independently adjudicated without inheriting unchecked labels. The tentative minimum is 30 independent sources and 3 template families; this is a feasibility gate, not a statistical power calculation.
2. Train/test/validation splits are disjoint by original source requirement AND template family. Mutation siblings cannot cross boundaries.
3. Real learned NL-to-formal model outputs, not just a number-word classifier, are available under a lawful $0 arrangement; use pre-existing published predictions if accessible. No heavy local inference.
4. At least two physically distinct dynamics families have valid, independently justified natural-language requirements and physically admissible counterexamples. Do not infer human intent from physics alone.
5. Fair comparison to semantic-probe, verifier-in-the-loop, and intent-alignment methods; same oracle information, comparable budgets, coverage and abstention.
6. Holdout results, uncertainty at the independent-source level, negative controls and code/data provenance survive external reproduction.
7. Full-text novelty review establishes a contribution not already supplied by the closest 2025–2026 work. Otherwise pivot or report a replication/negative result without novelty claims.

## Resource policy
Use only standard GitHub-hosted Linux runners in this public repository, with five-minute job timeouts and Python standard library. No model weights, GPUs, cloud credit cards, paid APIs, or laptop computation. GitHub's billing policy https://docs.github.com/en/billing/concepts/product-billing/github-actions states standard runners in public repositories are free; larger runners in public repositories are billable. This project uses no artifacts or cache writes in the workflow. No charge was initiated.

## Scientific integrity
No model provider (OpenAI, Anthropic, Google DeepMind) has been tested. No frontier-model result, new theorem, physical-NLP integration, or paper acceptance is claimed. All model examples are synthetic training; the five test sentences come from a published external dataset whose labels are unverified. The external authors are credited and not accused of wrongdoing. Disclose AI coding/research assistance according to the target venue.
