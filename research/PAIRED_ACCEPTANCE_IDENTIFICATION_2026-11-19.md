# Paired selective-risk decomposition and identification limits

Date: 2026-11-19. Status: analytic protocol, not an empirical result or novel theorem.

## Why equal coverage is insufficient

For two fixed verifiers A and B applied to identical candidate answers with binary error E_i=1-Y_i, partition the roster into four disjoint acceptance cells: n11 (both accept), n10 (only A accepts), n01 (only B accepts), and n00 (neither accepts). Let e11, e10, e01 count erroneous answers in the corresponding cells. Then

- coverage(A) = (n11+n10)/n; coverage(B) = (n11+n01)/n.
- selective error(A) = (e11+e10)/(n11+n10), when denominator >0.
- selective error(B) = (e11+e01)/(n11+n01), when denominator >0.

When achieved coverage is exactly matched, n10=n01=k. The denominators agree, and the difference in selective errors is **(e10-e01)/(n11+k)**. Errors in the shared-acceptance cell cancel. Thus any observed difference at equal coverage comes entirely from the *discordantly accepted* answers. This identity is elementary, not a new scientific discovery.

Consequences: (1) equal risk can conceal substantial decision disagreement; (2) a claimed improvement requires checking which method accepts correct answers on discordant items; (3) if k=0, the two selective risks must be identical on the fixed roster at equal coverage; (4) if both accept zero items, both selective risks are undefined.

## Paired uncertainty and effective sample information

The roster is paired, but answers from the same source family, template, document, or generating model can be dependent. Independent item-level bootstrap intervals may be anti-conservative. Report n11,n10,n01,n00, e10,e01, and family counts. For uncertainty, predeclare source-family-level resampling when sufficiently many independent families exist; with few families, state that cluster-bootstrap inference is unreliable and report sensitivity analyses rather than significance claims. Keep calibration and held-out sets strictly separate.

A large nominal sample size with tiny k has little information about *differences* between methods. Report the discordance fraction (n10+n01)/n and the number of independent families represented in discordant cells, not only overall accuracy.

## Counterexample to interpreting coverage matching as verification-quality matching

Suppose n11=40, n10=n01=10, n00=40. Both methods accept 50% of the 100 items. If e10=8 and e01=2, selective error(A) exceeds selective error(B) by 6/50 = 12 percentage points, regardless of e11. If both methods incurred different evidence-retrieval costs, this contrast does not by itself identify a superior method under a matched resource budget. This is a synthetic arithmetic illustration, not measured model performance.

## Predeclared falsification gates

1. **Pairing:** item IDs, candidate answers, correctness labels and held-out membership must be identical across methods; otherwise report a system-level comparison, not a verifier-only contrast.
2. **Budget:** compare full-roster measured costs in identical units, including abstentions and failures; apply the predeclared 5% tolerance and report the raw totals. Zero/zero measured cost is uninformative about computational equivalence.
3. **Coverage:** do not call two frozen thresholds 'matched coverage' unless their achieved acceptance counts match or a prespecified tolerance is reported. If not, present coverage-risk tradeoffs without claiming an equal-coverage win.
4. **Discordance:** publish the four-cell table and discordant-cell error counts. A claimed difference with k=0 at exactly equal coverage indicates an accounting bug.
5. **Source shift:** stratify by NLP, mathematics and physics source families and report adverse or undefined cells, rather than hiding them in pooled averages.
6. **Leakage:** no held-out labels, scores, family identifiers or examples may be used to retune operational thresholds.
7. **Multiplicity:** fix a primary contrast and domain weighting before evaluation; label other comparisons exploratory.
8. **Novelty:** this decomposition is standard paired contingency-table reasoning. A publishable contribution must establish a substantive new empirical phenomenon, method or theorem relative to the closest literature, not merely present these identities.

## Proposed zero-cost validation

Implement a deterministic pure-Python test fixture for the partition identity, zero acceptance, identical accept sets, and unequal coverage. Execute on GitHub-hosted CI only after verifying current repository/account eligibility and runner billing exposure. No local laptop execution, GPU download or model inference is required. Cloud model evaluations remain gated on verified no-charge quota and data licenses.

## Publication discipline

As of this note, no real-model result, independent CI pass, source-shift robustness finding or novelty finding follows from the algebra. The November 22 date is a conditional checkpoint; a preregistration or methods note is acceptable if empirical claims cannot be validated.
