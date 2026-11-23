# Paired prediction semantic bridge (2026-11-23)

Status: analytical derivation, not executed or claimed novel. Companion to the held-out cross-domain protocol.

For binary propositions with authenticated truth t_i in {0,1}, freeze each model's accepted binary answer a_mi and acceptance indicator s_mi. Error is e_mi = a_mi XOR t_i. Abstentions have no error contribution. If a source asserts t_i XOR t_j = p, then for accepted answers e_mi XOR e_nj = p XOR a_mi XOR a_nj. This follows by associativity and cancellation of XOR. It is not valid for arbitrary free-text answers or ambiguous proposition semantics. In particular, two models answering the same proposition oppositely have complementary error labels, not independent labels.

With fixed positive acceptance counts K_A and K_B, Delta = c + sum_i w_i t_i, where c = sum_i s_Ai a_Ai/K_A - sum_i s_Bi a_Bi/K_B and w_i = s_Ai(1-2a_Ai)/K_A - s_Bi(1-2a_Bi)/K_B. For abstentions set the unused answer placeholder to zero. This is obtained by expanding XOR on binary variables. Optimize this objective over the existing source-attributed truth constraints, rather than independently optimizing two model error sets. This preserves shared truth and paired dependence. The unrestricted sharp baseline is c plus the sum of negative weights for the lower endpoint and c plus the sum of positive weights for the upper endpoint; authenticated hard labels fix their contributions. These are elementary binary optimization identities, not novel theorems.

## Hand-checkable falsification fixture

Two items, both models accept both. A answers (0,0), B answers (0,1). Then Delta = t_2 - 1/2. Unrestricted sharp interval [-1/2,1/2]. If authenticated t_1=0 and one source asserts t_1 XOR t_2=0, budget zero yields {-1/2}; budget one restores [-1/2,1/2]. If both models instead give identical answers and acceptance, Delta is exactly zero for every feasible truth assignment. Independent marginal error bounds can incorrectly suggest a nonzero width even in that identical-model case. An empty feasible set is infeasible, not a zero-width interval.

## Experimental implications

Use a paired shared-truth unrestricted baseline as the primary comparator, not the difference of separately optimized marginal intervals. Compare both only to quantify the effect of pairing. Freeze binary answer extraction and abstention before truth access; exclude ambiguous free text by predeclared rules and report exclusions. Apply to binary NLP entailment propositions, mathematical claims and physically specified propositions only where independent adjudication is available. No model outputs or empirical results are asserted here. Next implementation gate: compare direct truth enumeration against the affine objective for every binary prediction and acceptance pattern on small frames, including unequal denominators and infeasible evidence. Run only on verified free standard public GitHub runners; no laptop workloads or paid APIs.
