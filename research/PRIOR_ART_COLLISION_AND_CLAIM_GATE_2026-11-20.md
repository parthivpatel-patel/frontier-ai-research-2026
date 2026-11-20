# Prior-art collision audit and claim downgrade (2026-11-20)

Status: literature-screening note, NOT an original theorem, experimental result, or exhaustive systematic review.

## Why this gate is necessary

The current project combines selective AI answer verification, accepted/rejected-pool audits, risk–coverage curves, sequential auditing and cross-domain NLP/mathematics/physics tasks. These ingredients have substantial prior art. A cross-domain combination alone is not sufficient evidence of novelty.

## Closest work checked (primary-source links)

1. Geifman & El-Yaniv, *Selective Classification for Deep Neural Networks*, NeurIPS 2017, https://papers.neurips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html . Already provides rejection/risk–coverage framing and risk guarantees; do not claim selective verification or abstention as novel.
2. Angelopoulos, Bates, Fisch, Lei & Schuster, *Conformal Risk Control*, ICLR 2024, https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html . Already studies calibrated risk control, including NLP losses; do not claim distribution-free risk control as new.
3. Xu, Karampatziakis & Mineiro, *Active, anytime-valid risk controlling prediction sets*, 2024, https://arxiv.org/abs/2406.10490 . Already addresses adaptive labeling and anytime-valid sequential risk control; do not claim active auditing or optional-stopping validity as novel.
4. Xu, Guo & Wei, *Selective Conformal Risk Control*, posted Dec 2025, https://arxiv.org/abs/2512.12844 . Already explicitly combines selective classification and conformal risk control; the project must compare directly against this baseline.
5. Angelopoulos, *Conformal Risk Control for Non-Monotonic Losses*, 2026, https://arxiv.org/abs/2602.20151 . Explicitly includes selective classification; the project must not assume monotonic-risk arguments apply to its abstention loss without proof.

These are verified bibliographic leads/abstract-level comparisons, NOT completed full-text proof-level comparisons. Further backward/forward citation review is required.

## Narrowest candidate contribution (unproven)

A reproducible **paired, fixed-budget, domain-stratified verifier evaluation protocol** that separates (i) selective error among accepted answers, (ii) correct-answer rejection among rejected answers, (iii) label-audit uncertainty, and (iv) end-to-end computational cost across scientific reasoning domains. This is a candidate empirical *evaluation contribution*, not an asserted novel statistical method.

## Frozen test design

- Define each task ID, prompt, model/version, generation seed where supported, raw answer, reference solution, verification rule, and domain before examining test outcomes.
- Domain-specific validity: NLP claims require explicit evidence or deterministic scoring rules; mathematics requires independently checkable derivations/counterexamples; physics requires unit/dimensional checks, explicit assumptions, numerical tolerances and physical-regime boundaries. Human adjudication must be blinded to verifier identity.
- Freeze verifier policy and threshold using a calibration partition. Never select thresholds on the final held-out partition. Separate a third audit sample where necessary for claims of confidence coverage.
- Compare a no-verifier baseline, a score-only abstention baseline, matched random rejection, matched compute-cost verification, and a domain-specific deterministic verifier where available. Add published SCRC/CRC baselines only if assumptions and implementation are compatible; otherwise explicitly record exclusion.
- At equal accepted count k>0, report errors on the full accepted set of each policy, not merely their intersection. Record discordant accepted sets and paired task-level differences. If k=0, selective risk is undefined; report coverage zero, not error zero.
- Audit accepted and rejected pools with known inclusion probabilities. A zero-error audit is not zero population risk. Precommit finite-population bounds and simultaneous domain adjustment; do not re-use a fixed-sample bound under adaptive stopping.
- Keep all compute on verified no-charge standard public GitHub Actions runners or other separately verified free cloud. Avoid GPU, model downloads, third-party paid APIs and local execution. A free runner is not proof that external model inference is free. Prefer tiny transparent fixtures for statistical tests; label them synthetic, never real model evidence.

## Falsification / publication gates

1. **Novelty failure:** if prior work already demonstrates the same joint evaluation and no defensible new empirical finding emerges, downgrade to a replication/benchmarking or methods report.
2. **Utility failure:** if the proposed verifier does not outperform strong baselines at matched accepted coverage and cost with uncertainty intervals, report null result.
3. **Generalization failure:** if improvement is restricted to one domain or disappears under independent adjudication, prohibit cross-domain superiority claims.
4. **Statistical failure:** if audit inclusion probabilities, calibration separation or optional-stopping rules are violated, withhold guarantees.
5. **Compute failure:** if no verified $0 inference route exists, do not run model experiments; publish reproducible plans and validated synthetic checks only.
6. **Integrity failure:** if task provenance, evaluation data, model identity, or assistance disclosure cannot be established, do not submit a discovery manuscript.

## November 22 decision

Publication is conditional. With only passing synthetic unit tests and no held-out model evidence, publish a transparent methodology/preregistration or negative novelty audit, **not** a claimed AI breakthrough. Record AI assistance as required by the destination venue. No expenditure or user-laptop compute authorized.
