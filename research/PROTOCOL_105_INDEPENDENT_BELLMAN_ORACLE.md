# Protocol 105 — Independent exact-rational Bellman oracle and zero-probability branch discipline

Date: 2026-11-15. Status: mathematical specification and preregistered validation design; **not an executed test or empirical finding**.

## Purpose and independence boundary

Protocols 093–104 develop a complete-policy enumerator, structural preflight, and witness scoring. None of those alone certifies that a returned witness maximizes expected reward. This protocol specifies a *separately implemented* finite-horizon Bellman oracle for tiny instances, using posterior masses over explicit worlds rather than generating complete contingent policy trees. The oracle must not import the enumerator, its policy-generation helpers, or its value-selection logic. Agreement between independently implemented algorithms is stronger evidence than scoring a witness with the same objective, but is not a formal proof of correctness on arbitrary inputs.

## Exact model and recurrence

Let n binary claims have a finite world set W subset {0,1}^n, with nonnegative rational prior masses p(w) summing to 1. Verification of i costs positive integer c_i, reveals w_i without noise, and pays reward w_i when verified. An action cannot be repeated. The available budget is integer b. The history is represented by a subset H of worlds compatible with observations; its unnormalized mass M(H)=sum_{w in H} p(w) must be strictly positive for reachable states.

Define V(H,R,b) as maximum *conditional* expected additional reward, where R is the set of unverified claims. Let A={i in R: c_i <= b}. If A is empty, V=0. Otherwise, for each i in A, define H_x={w in H: w_i=x}, m_x=M(H_x)/M(H), and

Q_i(H,R,b) = m_1 [1 + V(H_1,R\\{i},b-c_i)] + m_0 V(H_0,R\\{i},b-c_i).

Then V(H,R,b)=max(0,max_{i in A} Q_i). Use Fraction throughout, including all input masses and all comparisons. In an outcome branch with m_x=0, contribute exactly zero **without evaluating or recursing into** V(H_x,...). This avoids undefined posterior conditioning and prevents impossible branches from contaminating the oracle. Deterministic tie-breaking (e.g., smallest claim index) must be recorded but is not part of the value theorem.

For independent verification implementations, construct H from observation masks rather than passing tree nodes. Cache states by (observed-claim mask, observed-true mask, remaining budget); the remaining action set follows from the observed mask. Validate that no cache key represents an impossible observation. The oracle must refuse inputs exceeding explicit n, world-count, and state-count ceilings before potentially expensive work, and the cloud process must also have an independent hard timeout and memory limit. A state-count cap inside recursion alone does not ensure bounded memory.

## Hand-checkable test vectors

**A. One fair claim:** W={0:1/2,1:1/2}, c=(1), b=1. Bellman value=1/2. STOP value=0. A legal STOP witness must pass legality and score checks but fail any assertion that it is optimal.

**B. Two perfectly correlated fair claims:** W={(0,0):1/2,(1,1):1/2}, c=(1,1), b=2. First verify either claim. If true, verify the other; if false, stop. Bellman value=3/2. A noncontingent always-verify-both policy has value=1. A branch-swapped legal policy (verify second only after false) has value=1/2. All three may be valid witness trees: only the first is optimal.

**C. Two independent fair claims:** four equally weighted worlds, c=(1,1), b=2. Optimal value=1; contingent stopping after observing false is suboptimal because the other claim still has marginal expected reward 1/2.

**D. Impossible observation:** W={(0,0):1/2,(1,1):1/2}. After observing claim 1 false, the branch where claim 2 is true has posterior probability zero. No division by zero, synthetic epsilon mass, or artificial positive reward is allowed.

**E. Permutation invariance:** permuting claim indices, costs, and every world coordinate consistently must preserve optimal value; the chosen witness may differ because of tie-breaking.

**F. Scale invariance of unnormalized internal masses:** multiplying all *internal* world weights by the same positive rational factor leaves every posterior ratio and value unchanged; external input validation must still require normalized priors.

## Cross-check and falsification gates

1. Independently implement Bellman recursion with exact Fractions and posterior masks; do not copy Protocol 093 enumeration logic.
2. Compare Bellman values to Protocol 093 complete enumeration and Protocol 099 bounded certificate on every admitted tiny fixture; compare values, not exact witness shape.
3. Independently score each returned witness; require score <= Bellman value, and require equality for witnesses claimed optimal.
4. Deliberately substitute legal suboptimal witnesses from B; legality must pass, optimality must fail. Deliberately corrupt probability masses, repeated actions, and branch structure; admission or legality must fail.
5. Mutate posterior normalization, branch rewards, and zero-mass handling; require tests to detect each mutation.
6. Report number of fixtures, actual cloud job URL/commit, runner image, test exit codes, wall time, memory ceiling, and any refusals. Never infer a pass from committed code.

## Scientific interpretation and limitations

This oracle certifies optimality *within the explicit finite model and its assumed prior and perfect observations*. It cannot validate real-world calibration, truth labels, verifier reliability, or claims of benefit for NLP, mathematics, or physics. In particular, the reward sum of verified true claims is not equivalent to correct scientific adjudications per cost; false acceptance, false rejection, abstention, and label provenance need a separately preregistered empirical objective. Comparing against an optimal planner that uses the same true generative prior is a diagnostic ceiling, not a realistic deployed baseline. Empirical experiments must compare under matched available information and include prior misspecification.

## Zero-dollar execution gate

Do not launch anything until this repository's Actions permissions, standard GitHub-hosted runner availability, and billing settings have been checked. Use only documented free standard public-repository runners, no paid APIs, no larger runners, no local training/inference, and no large downloads. The current protocol is a specification; **no tests or cloud workloads were run as part of this protocol**. The November 22 decision checkpoint is conditional on independently verified evidence, not a publication promise.
