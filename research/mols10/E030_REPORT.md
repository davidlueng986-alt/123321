# E030 — First-Principles / Structural Audit (2026-11-02 ~09:55 UTC)

**Global status: OPEN.** No unrestricted 3-MOLS(10) construction or nonexistence certificate found in the checked primary sources. This is a structural and reproducibility audit, NOT a solution.

## Question and prior context
Read the living Google Drive journal, latest branch STATE.json and E016/E027/E028/E029 search code. E027–E029 completed exhaustive orthogonal-mate enumeration for ten SPECIFIC Q squares (eight BKS Appendix Q, Egan B/C). E025–E026 restricted Latin-trade neighborhoods are logically subsumed for their six fixed Q by E027's full mate enumeration, subject to the exact-cover implementation being correct. Avoid more local trade searches on these Q.

Primary literature:
- Gill & Wanless, *Pairs of MOLS of order ten satisfying non-trivial relations* (2023), https://arxiv.org/abs/2204.10996 ; https://doi.org/10.1007/s10623-022-01149-6 . They establish that no orthogonal pair with a nontrivial F2 4-net relation extends to a triple.
- Bright, Keita & Stevens, *Myrvold's Results ... SAT Investigation*, EJC 33(1) P1.30 (2026-02-13), https://arxiv.org/abs/2503.10504 (v2 2026-01-21), https://doi.org/10.37236/13960 . Their eight residual cases are *families*, not eight individual Q.
- Barnoff & Bright, *Improving SAT Solvers on Orthogonal Latin Square Problems*, https://arxiv.org/abs/2605.02132 (v2 2026-07-04). This improves pair search, not unrestricted triples.
- Bright, Keita & Stevens, *Orthogonal Latin Squares ... Two Relations*, https://arxiv.org/abs/2509.09633 . Restricted certified enumeration.

## New computation A — paratopy-invariant structural audit
Input: eight exact published BKS Q matrices from E023/E024, Egan A/B/C from near_triple.json, Parker A/B from parker_pair.json = **13 concrete Latin matrices**. Every one independently passes Latin row/column checks.

For each axis among (row, column, symbol), for each of the C(10,2)=45 pairs of parallel classes, calculate the cycle-length partition of the union of their two perfect matchings on the other two coordinates. Count the cycle types, and sort the three resulting histograms. This is a **paratopy invariant**: row/column/symbol relabelings conjugate the permutations; coordinate permutations only reorder the three histograms. Distinct signatures prove NON-paratopy; equal signatures do not prove equivalence.

Two separate algorithms (symbol-permutation cycles and connected components of 2-regular bipartite graphs) agree for all 13 matrices. Positive control applies arbitrary row/column/symbol permutations and a transpose to Egan A, preserving signature; a deliberately invalid Latin matrix fails validation.

Result: **12 distinct invariant signatures** among 13 matrices. Eight BKS Q, Egan A/B/C are pairwise distinguishable from one another and from Parker A/B. The only collision is **Parker A vs Parker B**; their equivalence is UNDETERMINED by this test. Therefore at least **12 distinct paratopy classes are represented** by these concrete matrices, but this says nothing about completeness of order-10 Latin squares or about global triple existence.

## New computation B — F2 incidence rank
A pair (A,B) gives a 100 x 40 binary incidence matrix with one 1 in each of the row, column, A-symbol and B-symbol blocks. Its rank is at most 37 because of the three trivial parallel-class dependencies. Any pair with rank <37 has a nontrivial relation, hence is excluded from any triple by Gill–Wanless (2023).

For the **eight BKS published (Z,Q) pairs, Egan (A,B), Egan (A,C), and Parker (A,B)**, independently implemented row and column GF(2) eliminations both give **rank 37/37 in all 11 cases**. Egan (B,C) is only 91/100, so it was deliberately NOT treated as an orthogonal pair.

**Negative finding:** rank is a sound literature-derived necessary filter but fails to prune ANY of these 11 known valid orthogonal pairs. Do not present full rank as evidence of extendability.

## New computation C — mate-compatibility graph
From the previously complete E027/E028/E029 mate lists, form a graph for each fixed Q: vertices = normalized orthogonal mates, edges = direct 100/100 orthogonality of the two mates. A triple containing Q exists iff the graph has an edge (assuming exhaustive mate lists). This provides a different direct validation route from the previous common-transversal obstruction.

All **24 normalized mates** of ten specified Q give **25 candidate mate-pair overlays** and **zero edges**. Maximum observed overlay = **76/100** (Egan B). Per-Q maxima: UW68, UX60, VX62, WW N/A (one mate), WX N/A, XX64, SX56, UU N/A, Egan B76, Egan C60. No 100/100/100 witness. This reconfirms only ten fixed-Q exclusions; graph computation uses the prior mate lists, so it is not an independent certificate that those lists were exhaustive.

## First-principles critique of E001–E029
1. **Objective mismatch:** pair construction (100/100) is necessary but weak. The target is an OA(100,5,10,2) / 5-net, not a 4-net; success metrics should measure *third-square extendability*, not merely number of mates or near-overlays.
2. **Local-search overinvestment:** E025/E026 neighborhood exclusions became redundant when E027 exhaustively enumerated every mate of the same Q. Ex post, this was low marginal information. Do not repeat.
3. **Sample-to-population fallacy:** eight published residual examples do not exhaust eight Myrvold families. Ten fixed Q do not exhaust paratopy classes. Twelve distinct signatures demonstrate some genuine diversity, not global coverage.
4. **Independent implementations share assumptions:** E027 bitset and Algorithm X both use the same transversals, source matrices, and mathematical reduction. Independent agreement reduces coding risk, but cannot replace input provenance audit, encoding proof, or independently checkable UNSAT certificates.
5. **Symmetry proof obligation:** labeling each mate's symbol by its unique column in row 0 is sound because ten disjoint transversals partition row 0, and mate-symbol relabeling cannot affect orthogonality. Other proposed symmetry cuts MUST have an explicit proof of completeness.
6. **Weak proxy traps:** E022 showed all 1647 pair roots passed cell-support yet only 45 exact covers existed. Full cell support, common-transversal count >=10, and GF2 rank 37 are NECESSARY but not SUFFICIENT.
7. **Literature-derived constraint:** a triple must have all its pair 4-nets rank 37. Our 11 valid pairs already have rank 37, so this does not by itself explain their failure.

## Falsifiable new hypotheses and experiment priorities
**H1 (highest priority):** A third-square-aware joint SAT/CP-SAT solver on the 5-net/OA formulation will produce more *verified* triple-feasible partial states per CPU minute than a pair-only generator followed by an extension test. Build two encodings under identical symmetry and budgets, log propagations/conflicts and verified partial assignments, and avoid claiming advantage without an A/B run. Test n=4 positive and n=6 negative before order 10.

**H2:** Early *exact-cover incompatibility* between proposed symbol classes is a stronger pruning signal than cell support. Extract small, replayable pair-root or triple-root obstructions from E022 and integrate them as sound lazy clauses into a joint search. Compare node counts and wall time on same fixed Q; count only exact logical cuts.

**H3:** Use paratopy signature as a cheap duplicate rejection (different signature => definitely new class; equal signature => unknown). For any generated Q, first verify Latin, then GF2 rank of candidate pairs, then exact mate compatibility. A new Q must not be labeled 'nonisotopic' solely from a different random seed.

**H4 (structural):** Rather than forcing a 4x4 subsquare, search rank-full 4-nets without this assumption, with 5-net symmetry across all five parallel classes. A direct full 5-net SAT encoding has a different bias than BKS residual-family pair search; this is a research hypothesis, not an established performance claim.

## Evidence and limitations
- Reproducible paratopy and rank code: `E030_structural_audit.js` (Node); independently replayed after GitHub commit, all controls PASS.
- Direct mate graph code: `E030_mate_graph.py`; local replay on E027/E028/E029 full JSON artifacts PASSED; source recompute mode provided. Result: `E030_MATE_GRAPH_RESULTS.json`.
- Failure/negative evidence: zero mate graph edges; rank-37 filter rejected zero of 11 pairs; Parker A/B signature collision unresolved. No GPU used.
- No claim of DRAT/FRAT proof, complete paratopy classification, new published theorem, unrestricted nonexistence, or valid triple.
- GitHub Actions CI for E030 not yet verified.

**NEXT E031:** build a tiny direct OA(100,5,10,2) constraint model with justified normalization; prove correctness on n=4 and n=6 controls; perform a bounded order-10 smoke run and record SAT/UNSAT/UNKNOWN accurately. Compare to existing fixed-Q exact-cover route only under matched compute. Preserve input, solver version, seed, wall time, and proof evidence.
