# Protocol 024 — Post-hoc grounded-proposition alias diagnostic

Date: 2026-11-02 (US Eastern). Session 027. **Exploratory, post-hoc analysis, not preregistration.** The analyst inspected the 15 nonmatching formulas from Protocol 023 before defining this diagnostic. Report that selection explicitly in any paper.

## Question and motivation

Protocol 023 counted 485/500 exact token-string matches in the lifted VLTL-Bench Navi file. An exploratory inspection of the 15 mismatches revealed cases in which the prediction used two distinct proposition IDs, while the reference reused one ID and the supplied proposition dictionary assigned the IDs identical grounding metadata. Does a strictly metadata-conditional alias rewrite account for some exact-string nonmatches? This tests evaluation sensitivity, **not** whether an AI correctly understood the original instruction.

Upstream: English et al. (2025), https://arxiv.org/abs/2507.00877 , https://github.com/Dubascudes/VLTL-Bench . Same pinned upstream commit and byte-verified file as Protocol 023: commit 383baea8210b93fe9fa7d14edd4757e5b3464e82, file translation_eval/nl2tl/gt_lifting/navi.jsonl, Git blob c21575fca5e224968b56f0192b8bc0ddbaedac46, 356248 bytes.

## Frozen analysis plan before the next cloud execution

- Use only the standard free public GitHub-hosted runner. Fetch one pinned file in memory with Protocol 023's 1 MiB bound, SHA-1 Git blob verification and 20-second timeout. No local laptop work, API inference, model downloads, paid services, caches, or external-data publication.
- Preserve the existing whitespace-only exact match definition and the same 500 records.
- For a nonmatching record only, compare the complete JSON grounding dictionaries for every proposition ID. Require nonempty canonical action and argument metadata, valid declared IDs, and exact equality of all metadata fields after JSON key ordering. Fail closed if metadata is missing, malformed or a proposition is undeclared.
- Rewrite only whitespace-delimited proposition ID tokens to the smallest numeric ID within each identical-metadata group. Do not alter LTL operators, scope, parentheses, or unrelated tokens. If both rewritten strings match, classify as a **metadata-conditional alias-only mismatch**; otherwise classify as unresolved.
- Report only aggregates: exact string matches, alias-only mismatches, unresolved mismatches, and the resulting conditional metadata-agreement fraction. Never print or commit individual external instructions, predictions, proposition dictionaries or references. Keep the raw-language Conformal file separate and out of scope.
- The partition must sum to the number of nonblank predictions. Network-free constructed tests must cover aliasing, different groundings, scope changes, undeclared symbols, malformed metadata, and source-integrity failure.

## Conditional mathematical statement

For any trace semantics in which proposition symbols p and q denote the **same Boolean predicate at every state**, replacing p by q in an LTL formula preserves truth by structural induction on the formula. This is classical substitutivity, not a novel theorem. Identical upstream proposition dictionaries supply only *claimed* predicate identity. They do **not** independently establish correct grounding, equivalence of original human instructions, or safe physical execution.

## Falsification and interpretation limits

- If no mismatches are explained, report zero. If a purported alias changes operator structure or the metadata differ in any field, do not call it equivalent.
- If the cloud aggregate differs from exploratory inspection, investigate without changing the pinned protocol and disclose the discrepancy.
- Even a high conditional fraction is **not model accuracy**. The proposition dictionary and reference are evaluation metadata, not a deployable verifier input; the oracle firewall remains mandatory for any future method comparison.
- This diagnostic cannot establish a new algorithm, improved model, physical safety, independent human ground truth, or calibrated selective risk. No confirmatory statistical inference from the post-hoc selected mismatch subset.
- VLTL-Bench has no confirmed redistribution license in the inspected pinned repository; do not publish upstream records. Its paper already addresses lifted versus grounded verification, so this is at most a reproducibility/evaluation sensitivity result.

## Baselines and future go/no-go

Prior art: VLTL-Bench (English et al., 2025); ConformalNL2LTL (Wang et al., 2025, https://arxiv.org/abs/2504.21022); SCP-NL2TL (Wang et al., 2026, https://arxiv.org/abs/2608.05439). The proposed physics-assumption uncertainty method remains untested on human-adjudicated, source-disjoint predictions. Do not infer novelty or superiority from alias normalization. If independent data cannot be secured, pursue a scoped negative/methodological report by the conditional November 22 target.

GitHub confirms standard hosted runners in public repositories remain free as of its 2026 pricing update: https://github.blog/changelog/2026-01-01-reduced-pricing-for-github-hosted-runners-usage/ . No card or billing changes are required for the existing public repository's standard runner.
