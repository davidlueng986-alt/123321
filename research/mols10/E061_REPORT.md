# E061 — CLOSED-Only Direct Mathematics: Full-OA DLX, Transversal Endgame, and Major Search Routes

**Date:** 2026-11-03. **Global mathematical status:** **OPEN**. **Only objective:** a fully verified 100/100/100 witness or unrestricted, independently replayable nonexistence proof. MOLS10 hourly automation remains disabled by user request.

## 1. A direct constructive closure criterion (mathematical lemma)

Let `A,B` be any pair of orthogonal order-`n` Latin squares, and call a **common transversal** a set of `n` cells containing every row, column, `A`-symbol, and `B`-symbol exactly once.

**Equivalence:** A third Latin square orthogonal to both `A` and `B` exists **iff** `A,B` have `n-1` mutually disjoint common transversals. The remaining `n` cells automatically form the `n`th common transversal: after `n-1` complete transversals, each row/column/`A`-symbol/`B`-symbol has exactly one uncovered cell. Assign a distinct `C`-symbol to each transversal. Conversely, the `C`-symbol classes from any complete triple are `n` disjoint common transversals.

**A stronger computational stopping condition:** Suppose **`n-2`** disjoint common transversals have been found. On their `2n` uncovered cells, make an undirected graph by connecting the two uncovered cells sharing each of the following four resource types: row, column, `A`-symbol, `B`-symbol. Each resource occurs exactly twice, so all edges are defined. The residual graph is bipartite **iff** its two color classes are two further common transversals. Any proper 2-coloring thus **completes the third square immediately**. For `n=10`, find **8 disjoint common transversals with a bipartite 20-cell residual graph**, or find **9** (which automatically forces the tenth). This is mathematically equivalent to solving the original existence problem, not a relaxation.

**Actually executed controls:** independent full order-4 and order-5 OA witnesses were used to reconstruct third squares from `n-1` known transversals, and from `n-2` transversals plus bipartite coloring. All three orthogonality overlays verified as `16/16/16` and `25/25/25`. Exact enumeration of Egan–Wanless 2016's **specified** orthogonal pair found **14 common transversals** and maximum **7 pairwise disjoint**; this pair cannot satisfy the criterion. That does NOT bound other order-10 pairs. Proof/checker: `E061_transversal_route.py`, `E061_two_transversal_completion.py`.

## 2. Direct unrestricted 5-coordinate OA(100,5,10,2) solver

Implemented `E061_full_oa_dlx.cpp`: standalone C++ DLX/Algorithm X, one 10-resource exact-cover choice per cell-value tuple `(row,column,A,B,C)`; constraints: 1 cell, 6 row/column symbol demands, and 3 ordered-pair demands. No fixed historical square or near-triple. Sound normalization: independently relabel each square to give first row `0..n-1`, then permute the rows to make `A[r][0]=r`; non-first-row values must differ pairwise and from the column index. The code also accepts the twelve canonical cycle types of `A[1]`, using E033's proved conjugation normalization.

### Executed exact controls

| Order | Result | Search nodes | Scope |
|:--:|:--|--:|:--|
| 3 | `UNSAT_EXHAUSTIVE` | 4 | no 3 MOLS(3), known |
| 4 | `SAT`, 16/16/16 | 17 | independently verified witness |
| 5 | `SAT`, 25/25/25 | 28 | independently verified witness |
| 6 | `UNSAT_EXHAUSTIVE` | 200,601 | finite exhaustive exact-cover replay; no standalone formal proof object |
| 10 | `UNKNOWN_BUDGET` | 1,687,552 in ~15 s | no complete witness, no branch ruled out |

For order 6, all four canonical `A[1]` cycle types `2+2+2`, `2+4`, `3+3`, `6` were exhaustively UNSAT in 11,782 / 14,791 / 16,127 / 14,301 nodes. For order 10, all twelve canonical `A[1]` cycle types were explored for ~1 s each; **all twelve remain UNKNOWN**, and max partial DLX depth was 68–72 selected points, not 68–72 complete row blocks. Seven additional fixed `A[1]=2^5, B[1]=(column+k)mod10` branches were tested with `k=2..8`, each for ~2s, all UNKNOWN; these do not enumerate all B representatives. **Zero of the 162,959 previously identified `(f,g)` two-row orbit frontiers is fully closed.**

### Pair-generation benchmark

A separate `E061_pair_dlx.cpp` seeks an entirely *new* orthogonal pair rather than a fixed known one; exact controls for orders 3/4/5 SAT and 6 exhaustive UNSAT. For order 10, the original search and 10 randomized candidate-order seeds (~1.5s each) returned UNKNOWN. Pair generation must be upgraded with conflict learning rather than relying on plain DLX. No new pair or 8-packing was found.

## 3. Aggressive constructive local moves — independently falsified as an easy fix

Starting from Egan–Wanless 100/100/91 complete three Latin squares, considered transformations that **preserve Latin correctness**:

* All 16,110 combinations of two independent whole-row/whole-column swaps of B,C: none raises total distinct pairs above `291/300`.
* All 240 symbol-cycle (Latin bitrade) component moves in A/B/C: best remains 291. These change multiple rows/columns while preserving Latin conditions.
* All 57,123 ordered two-trade moves in Python: best remains 291.
* C++ exact depth-3 cycle-trade search, quotienting the complement component by global a↔b symbol relabeling and skipping immediate inverse: **3,702,370 search nodes**, best remains `291/300`, no 100/100/100 witness. Separate Python two-trade results are an independent lower-depth audit.

This is only a rigorously bounded **one fixed near-triple neighborhood**, not an unrestricted negative theorem. Research decision: do not continue polishing this very rigid local basin; switch to new pair species or truly global 5-coordinate SAT/CP with conflict learning. A score of 291 is not a percentage solved.

## 4. Relevance of earlier E060 result

The one published 2024 `9×10` three-MOLR source was exhaustively tested on **all 84 choices of six existing complete row triples**. Each fixed six-row anchor was ruled out via full row completion with zero timeouts. Consequently, in the same column/symbol coordinate system, any full triple can contain **at most five** of this source's nine row triples (in any row order). This is a sound **source-anchored separation statement**, not global exclusion. Thus constructive changes affecting only one, two, or three complete row triples of that published source are guaranteed not to close the problem.

## 5. Sole direct paths to CLOSED

**Existence:** (a) Find a different order-10 orthogonal pair with eight disjoint common transversals and bipartite residual graph, or nine disjoint common transversals outright. (b) Run a genuinely unrestricted full 5-coordinate OA(100,5,10,2) solver with strong symmetry, constraint propagation, and conflict learning; *any* SAT assignment must be independently checked all 100/100/100.

**Nonexistence:** Prove that all full 5-net candidates have a structural contradiction, or produce proof-carrying UNSAT with a mathematically complete and independently replayed branch inventory. The 12 canonical f cycle types are only the first branching layer; the 162,959 `(f,g)` frontier does not itself eliminate any continuations. Incorporate established Gill–Wanless GF(2) nontrivial-relation obstructions **only with a logically sound extension check**. Proof logging (e.g. LRAT) is required before announcing a global computer-assisted negative result.

### Limitations

Order 10 is still **OPEN**. There is no validated 100/100/100 witness, no unrestricted negative proof, **zero globally closed orbits**, and no credible solution ETA. The published sources are Gill–Wanless (2022/2023), Jäger et al. (2024), Bright–Keita–Stevens (2026), and Egan–Wanless (2016). No novelty claim is made for the basic transversal equivalence; the residual bipartite closure gate follows immediately from the resource exact-cover characterization.

## Reproduction

Run `bash E061_replay.sh` after extracting the archive (requires `g++`, `python3`). `E061_verify.py` independently verifies positive 3-MOLS witnesses and aggregate scope. Source, output JSON, README and SHA256 manifest are included. The E061 12-type and 10-seed probes are bounded exploratory records. Re-running exhaustively proves only the stated bounded/fixed scopes.