# Protocol 071 — paired-bound executable oracle and falsification cases

Date: 2026-11-05. Status: preregistered specification, not an empirical result.

## Scientific question
For a fixed collection of N scientific claims, does an assumption-explicit verifier reduce unsafe acceptance compared with a baseline at *matched coverage*, without relying on unverifiable truth labels?

## Definitions and exact oracle
For claim i, let A_i and B_i be binary acceptance decisions, and Y_i in {0,1,?} indicate independently adjudicated unsafety (1), safety (0), or unresolved truth (?). Define the paired difference in unsafe acceptance per submitted claim:
D = (1/N) sum_i (A_i-B_i) Y_i.

For known Y, its contribution is fixed. For unresolved Y, define c=A-B in {-1,0,1}. Its contribution belongs to [min(0,c), max(0,c)]. Therefore the sharp finite-sample identification interval is:
L = (sum_known cY + sum_unknown min(0,c))/N;
U = (sum_known cY + sum_unknown max(0,c))/N.
Sharpness follows because each unresolved binary Y can independently attain either endpoint. This assumes no additional physical or cross-claim constraints; if unresolved truth values are coupled, these bounds may not be sharp.

This is established partial-identification mathematics, not a novel theorem.

## Executable oracle cases (expected exact values)
Each tuple is (A,B,Y), with '?' for unresolved.
1. [(1,1,'?')] => [0,0].
2. [(1,0,'?')] => [0,1].
3. [(0,1,'?')] => [-1,0].
4. [(1,0,1),(0,1,0)] => [1/2,1/2].
5. [(1,0,'?'),(0,1,'?')] => [-1/2,1/2].
6. [(1,1,'?'),(1,0,1),(0,1,'?')] => [0,1/3].
7. [(0,0,'?'),(0,0,1)] => [0,0].
8. Empty input => controlled validation error, not division by zero.

Reject nonbinary acceptance decisions, truth values other than 0/1/? (including booleans disguised as numeric truth if schema forbids them), and inconsistent record counts. Compare rational results exactly, not via rounded displays.

## Matched coverage and negative controls
Compare A and B on identical submitted claims with exactly equal accepted counts, and separately report accepted count and unsafe-acceptance interval. Equal coverage is not equal correctness: A=[1,0], B=[0,1], Y=[1,0] yields D=1/2 even though both accept one of two claims.

Predefine five baselines: direct model judgment; self-consistency voting; unit/dimensional checks; symbolic-algebra-only checks; and assumption-explicit certificates. Do not imply these are novel baselines or that any has been run.

Report per-domain performance and macro-averages across mechanics, electromagnetism, thermodynamics, and quantum mechanics. Keep source families disjoint between development and test. Independent adjudicators must be blinded to verifier identity. Do not treat a filled reviewer-name field as evidence of actual independence.

## Falsification and publication gate
Reject the claimed improvement if: (i) the paired bound includes zero under prespecified uncertainty handling; (ii) advantage disappears under matched coverage or source-disjoint testing; (iii) adversarial assumption violations pass unchecked at unacceptable rates; or (iv) results require post-hoc exclusion of unresolved claims. Do not replace these with significance tests on selectively adjudicated subsets.

No experimental outcomes, cloud-run logs, or novelty claims are asserted here. Next action is to implement these exact oracle cases as regression tests and execute them on a verified no-cost hosted runner after account-specific billing/quota checks. No laptop computation or paid services are authorized.
