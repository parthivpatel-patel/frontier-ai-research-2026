# Novelty and falsification gate: temporal evidence verification (2026-11-21)

Status: **research design, not a demonstrated discovery**. This document records candidate prior art and discriminating tests. Bibliographic items must be checked against primary papers before manuscript submission; the list is not a completed systematic review.

## Claim boundary

Candidate contribution: a **joint evaluation protocol**, not invention of bitemporal databases, selective prediction, missing-data bounds, retrieval-augmented generation, or factuality verification. The protocol combines (i) evidence versions and public-availability cutoffs, (ii) abstaining verification with shared unknown truth labels, (iii) partial-identification bounds under archive missingness, and (iv) cross-domain evaluation of NLP claims, mathematical statements and physics claims. A combination of established methods is not automatically novel.

## Closest prior-art families to audit

1. **Temporal knowledge and time-sensitive QA:** Dhingra et al., *Time-Aware Language Models as Temporal Knowledge Bases* (2022), and subsequent temporal QA benchmarks. Compare whether publication-time evidence admission is already operationalized.
2. **Retrieval-grounded verification:** Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (2020); Thorne et al., *FEVER: a Large-scale Dataset for Fact Extraction and VERification* (2018). Compare claim-level provenance, retrieval and verification, not just accuracy.
3. **Selective prediction:** Geifman and El-Yaniv, *Selective Classification for Deep Neural Networks* (2017); examine risk–coverage and abstention conventions. Our selective-error formula is not new.
4. **Partial identification / missingness:** Manski, *Partial Identification of Probability Distributions* (2003); Little and Rubin, *Statistical Analysis with Missing Data*. Worst-case bounds and missingness sensitivity are established.
5. **Bitemporal provenance:** Snodgrass, *Developing Time-Oriented Database Applications in SQL* (2000); valid time and transaction time are established. Historical web capture time is not necessarily original publication time.
6. **Mathematics and physics verification:** compare proof-checking and theorem-proving benchmarks separately from natural-language scientific claim checking. A truth label for a theorem cannot be treated as a timestamped measurement; a physics result may be revised or superseded.

## Explicit falsification criteria

- **Novelty failure:** an earlier study already jointly implements cutoff-aware source-version admission, archive-missingness bounds and selective verification with shared-label evaluation, with materially equivalent experiments. Then characterize this work as replication or extension, not novel discovery.
- **Leakage failure:** post-cutoff revisions, archival captures or model-generated summaries enter the historical evidence set. Quarantine affected samples and recompute.
- **Validity failure:** source timestamps cannot be independently authenticated; report a restricted archived-only estimand or abstain from historical-public-availability claims.
- **Identification failure:** sharp shared-label bounds include zero or both signs for the paired risk difference. Do not assert a winner.
- **Performance failure:** improvements disappear against matched retrieval budget, model family, coverage, latency and time cutoff; do not claim superiority.
- **Domain failure:** effect is confined to one domain or depends on ambiguous theorem/physics labels; report domain-specific findings without cross-domain generalization.

## Reproducible experiment plan (not yet executed)

Freeze a public dataset manifest containing claim ID, domain, query time, evidence version hash, independent timestamp provenance, annotation protocol and adjudicator disagreement. Use a fixed historical cutoff per item. Split by source and time to prevent near-duplicate leakage. Compare (A) closed-book verifier, (B) cutoff-blind retrieval, (C) cutoff-aware retrieval, and (D) cutoff-aware retrieval with abstention and missingness bounds. Keep model, token budget and retrieval corpus matched wherever feasible. Report risk–coverage curves, calibration, leakage rates, subgroup breakdowns, label disagreements, source exclusion rates and paired uncertainty. Use exact small-frame enumeration only for synthetic oracle tests; scale with a separately validated solver, not exponential enumeration.

**Cloud gate:** no workload is authorized merely because a provider advertises a free tier. Before running, independently verify current quota, signup/card requirement, availability, billing safeguards, job time limits, and public/private data policy. No user laptop inference, training, model downloads or simulation. If zero-cost availability cannot be established, stop at a reproducible preregistration.

## Publication gate

Separate (1) authored code, (2) tests actually run with immutable CI SHA/logs, (3) observed model outcomes, and (4) theoretical claims. The present work supports (1) and a proposed protocol, not (3). Cite primary literature, publish negative results, disclose AI assistance as required by the venue, and never claim human-only authorship when assistance was used.
