# Protocol 066 — Prior-art collision audit and falsifiable contribution boundary

Date: 2026-11-13. Status: literature-screening note, **not** proof of novelty, a complete systematic review, or an experimental result.

## Scope and proposed estimand

The project investigates whether a provenance-aware, budgeted verification policy can reduce the **false-acceptance rate among released scientific claims at matched release coverage** across NLP, mathematics, and physics. This is a *candidate empirical question*, not an established contribution. Audit cost, family-level dependence, verification errors, and missing truth labels must be explicitly represented.

The current manifest remains DRAFT_NOT_FROZEN; all dataset hashes, model versions, audit budget, cloud authorizations, and outcome measurements are unresolved. A successful metadata validation alone is not scientific evidence.

## Directly relevant published prior art

1. Geifman and El-Yaniv (NeurIPS 2017), *Selective Classification for Deep Neural Networks*, https://papers.nips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html . Already establishes prediction rejection to trade coverage for error/risk. **Collision:** abstention and risk–coverage curves are not novel.
2. Angelopoulos, Bates, Fisch, Lei, and Schuster (ICLR 2024), *Conformal Risk Control*, https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html . Controls expected monotone losses using calibration. **Collision:** calibrated risk control is not novel. Its assumptions must not be silently transferred to adaptive, correlated, partially audited claim populations.
3. Angelopoulos (2026), *Conformal Risk Control for Non-Monotonic Losses*, https://arxiv.org/abs/2602.20151 . Extends risk control to nonmonotonic losses and multidimensional parameters under stability-dependent guarantees. **Collision:** simply changing the loss or using multiple knobs is insufficient for novelty.
4. Marcondes e Resende et al. (2026), *ReCIRC: Rectified Conformal Risk Control*, https://arxiv.org/abs/2609.38112 . Studies input-varying calibration while retaining marginal control. **Collision:** heterogeneous or conditional risk budgets alone are not novel.

This is an initial collision screen, not a comprehensive audit of active auditing, survey sampling, fact verification, selective labels, or scientific reasoning literature. Before claiming originality, search those fields and document the closest mathematical equivalences.

## Specific non-novel claims to avoid

- A new method because it abstains on low-confidence claims.
- A new guarantee because it uses a calibration split or conformal-style threshold.
- A new method because it weights audit costs or clusters related claims, without showing what differs from established sampling and dependent-data inference.
- A novel AI/physics discovery because the benchmark includes physics questions. Subject coverage is not a physics contribution.

## Minimum adversarial baseline matrix

At equal released-claim coverage and a prespecified verification budget compare: (A) confidence-only selective release; (B) calibrated risk control when its assumptions apply; (C) random budget-matched audits; (D) provenance-family stratified audits; (E) candidate adaptive family-aware audit policy. Report false acceptance among released claims, family-cluster confidence intervals, total audit cost, and the fraction with unobserved labels. If assumptions preclude a method, state why rather than supplying a fabricated score.

## Falsification and publication gates

- **No improvement:** candidate does not outperform the strongest valid baseline on prespecified held-out families after uncertainty and multiplicity adjustment.
- **Dependence failure:** claimed guarantees break under shared-source or paraphrase clusters; effective independent sample count must be examined.
- **Selection bias:** outcomes are selectively observed and the missing-label mechanism is not identified or sensitivity-bounded.
- **Leakage:** a claim family, source passage, threshold, or audit truth label crosses the calibration/test firewall.
- **Domain failure:** aggregate improvement hides deterioration in mathematics or physics; report all three domains separately.
- **Cost failure:** an apparent advantage disappears at equal *actual* verification expenditure.
- **Novelty failure:** the proposed mathematical object reduces to an established selective classification, risk control, or sampling estimator under an explicit mapping.

A publishable negative finding is acceptable if it is reproducible and useful. Do not describe a theoretical guarantee without a proof and its assumptions. Do not assert novelty without an expanded, dated prior-art comparison.

## Feasibility and compute constraints

No GPU, laptop inference, model downloads, paid API, or cloud job is authorized by this document. Before experiments, independently confirm the specific cloud account's zero-cost entitlement, whether a card is required, limits and billing exposure, and available capacity. Use only verified free cloud compute; stop rather than assume free-tier eligibility. Record runtime and cost evidence in the manifest. Human review of claim truth and provenance remains an explicit data requirement.

## Immediate next evidence

Freeze a sourced literature matrix, predefine the family-level estimand and missing-label sensitivity analysis, bind actual claim records to hashes, and run the existing standard-library validation suite on a confirmed $0 cloud runner. The November 22, 2026 target is contingent, not a reason to weaken the gates.
