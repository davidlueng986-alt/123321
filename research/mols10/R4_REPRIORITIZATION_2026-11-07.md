# 3-MOLS(10) R4 re-assessment — OPEN, Universal Mathematics still a primary CLOSED route

**Date:** 2026-11-07. **Global state: OPEN.** No independently checked complete 100/100/100 witness; **0/1700** full E064 paratopy classes certified UNSAT. The user rightly challenged an earlier over-general conclusion: implementation gaps in E069's three claimed algebraic audits do **NOT** show that the universal-theorem route is low value. R4 must remain a primary, potentially highest-leverage research track.

## Scope correction

Four routes can close the original theorem: R1 mathematically sound cuts *plus certified closure of remainder*, R2 one fully independently verified SAT triple, R3 globally complete checked UNSAT, R4 an unconditional contradiction under the hypothesis OA(100,5,10,2). R4 may close ALL 1700 classes at once. A weaker branch-conditional structural contradiction can also close one or many E064 classes; either is meaningful progress.

**Proven by source inspection (E069 original `E069_R4_universal_theorems.py`):**

- The computed parity/cocycle matrix uses only `m` and `n=10`, with no E064 canonical first-column permutations `B_col0` or `C_col0` as inputs. The formal system and its 512-to-32 projection show no inconsistency **of that chosen abstract linear system**. They do not prove every realizable orthogonal pair extends to a triple, nor rule out stronger geometric parity constraints.
- The 5-star weight-profile count and generic code properties are likewise symbolic or sampled on one Egan 4-net. They do **not** establish a global 5-net existence obstruction or certify every claimed Hull identity.
- The Gram matrix `M=10 I_50 +(J_5-I_5)⊗J_10` depends only on the hypothetical net parameters `(n,k)=(10,5)`, not on any representative. Its feasible spectrum/ranks alone cannot exclude a particular first-column class. The published code hardcodes `srg_krein_feasible = True` and does not calculate its purported Smith normal form. These are audit deficiencies of E069, not a verdict on R4.

**Empirical branch-dependent input audit:** exact 1,700 canonical `B_col0`, `C_col0` permutations were examined for parity:

| parity B | parity C | Number of E064 classes |
|---|---|---:|
| even | even | 474 |
| even | odd | 435 |
| odd | even | 369 |
| odd | odd | 422 |

Total 1700. These are **descriptive signatures only**, not proved forbidden configurations. Neither the four parity groups nor individual f/g types are known impossible. **Do NOT infer a single UNSAT class from this audit.**

## Exact 1/1700 milestone obligation

Fix E064 canonical index `i` with full normalized OA(100,5,10,2) constraints `F`, and all 18 first-column unit assumptions `C_i`. A complete order-10 branch exclusion means certifying `F ∧ C_i = UNSAT` with sound mathematical case coverage and an independently checkable proof. A new structural theorem may instead prove `C_i ∧ (necessary conditions of full 5-net) ⇒ false`, but the embedding/normalization and necessity of every asserted condition must be rigorously justified. If `F ∧ C_i` is SAT and its three full Latin squares and 100/100/100 overlays verify, **the whole problem is CLOSED YES**. There is no mathematical guarantee any class is UNSAT: all 1700 might be SAT in principle, and we currently know neither existence nor nonexistence.

**The global, purely symbolic E069 R4.1–R4.3 computations are independent of `C_i` and currently feasible, so they cannot distinguish one of these 1700 cases or establish 1/1700 UNSAT without being strengthened.**

## R4 research prioritization, not another Egan-only local loop

1. **Global theorem:** seek new unavoidable constraints coupling ALL FIVE coordinate directions (row,column,A,B,C), not identities satisfied by each abstract 5-net parameter list. Inspect parity/cocycle plus GF(2) incidence-code / quadratic-form compatibility, but treat candidate incompatibilities as hypotheses until proved.
2. **Branch-conditional theorem:** derive parity and code constraints that explicitly depend on the first-column pair `(f,g)` (and then safe deeper partial rows, if root-level constraints are intrinsically weak). Check the 8 derangement cycle types and all 1700 canonical branches exhaustively. A direct contradiction at one branch would be a legitimate first full branch closure; an overapproximate screen with zero exclusions is not.
3. **Independent math-to-SAT bridge:** any additional derived clause must be provably implied by the ORIGINAL OA constraints, not only assumed true in an augmented CNF; independently check certificates. For each candidate branch, distinguish `SAT_WITNESS_VERIFIED`, `UNSAT_CERT_VERIFIED`, and `UNKNOWN`.
4. **Scientific falsification:** if a proposed invariant yields 0 exclusions or no search benefit, retire that *specific test*, not the entire R4 route. Prior root-level spectral/GF(2) upper bounds (E067) excluded 0/1700 and are not a reason to abandon mathematical proofs.

## Existing research references

- Francetić, Herke, Wanless, *Parity of Sets of Mutually Orthogonal Latin Squares* (2017): https://arxiv.org/abs/1703.04764 — published upper bound on realized OA parity information, not universal equality.
- Gill, Wanless, *Pairs of MOLS of order ten satisfying non-trivial relations* (2022): https://arxiv.org/abs/2204.10996 — a conditional global obstruction to extension for full orthogonal pairs with certain GF(2) relations.
- Bright, Keita, Stevens, *Myrvold's Results on Orthogonal Triples of 10×10 Latin Squares: A SAT Investigation* (2026): https://doi.org/10.37236/13960 — rigorous exclusion of certain **restricted** types, not the unrestricted three-square question.

**Status remains OPEN. Next unit of actual progress should be one rigorously certified full E064 branch UNSAT, one checked full SAT triple, or a mathematically valid lemma covering multiple classes. No automatic hourly research reenabled.**
