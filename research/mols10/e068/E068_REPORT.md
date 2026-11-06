# E068 — Goal-Backward Deep Partial Pair Pruning: 12 exact sound 3-MOLS(10) nogoods

**Experiment date:** 2026-11-06. **Global order-10 status: OPEN.** 0/1700 E064 first-column classes proved UNSAT. No complete 100/100/100 witness; no universal nonexistence proof.

## The direct CLOSED implication

Suppose `A,B,C` is a full 3-MOLS(10). Pick *any* cell `(r0,c0)`. Let `d=C[r0,c0]`. The 10 cells of `C` bearing symbol `d` form a **common transversal of A and B**, passing through `(r0,c0)`: exactly one cell from every row, every column, every symbol class of `A`, and every symbol class of `B`. Therefore:

> **SOUND PARTIAL-PAIR NOGOOD.** If a set `Q` of already fixed A/B symbol assignments rules out **every possible row→column permutation through a selected anchor** with no duplicate *known* A-symbols or B-symbols, then **no 3-MOLS(10) completion can contain all assignments Q**. All unassigned A/B cells are treated as wildcards. This is a safe overapproximation, not a probabilistic score.

A single such nogood is a clause `∨_{(square,row,col,value)∈Q} ¬x(square,row,col,value)` in the **full five-coordinate** one-hot model. This is an *implied clause*, not a guessed additional axiom. Its soundness is justified by the preceding transversals theorem and by complete enumeration of the wildcard-relaxed permutation problem for that specific `Q`.

## What was actually done

We used the well-known Egan–Wanless 2016 published `100/100/91` near triple. A and B are a **complete orthogonal pair** (overlay AB 100) with exactly 14 common transversals and 12 cells not on any common transversal. These 12 anchor cells are:

`(0,1), (0,2), (0,3), (1,8), (2,9), (3,7), (4,4), (5,5), (6,6), (7,0), (8,0), (9,0)`.

For each anchor, build a *partial pair* by progressively deleting individual known entries from the 200 possible `(square∈{A,B},row,col)` assignments. An exact C++ MRV backtracking checker tests whether any row→column permutation through the anchor survives distinctness of **known** A/B symbols; missing values are unrestricted. Deletion is retained if zero anchor transversal remains. 30 independently shuffled deletion orderings per anchor (360 complete elimination runs). Minimize each output one literal at a time, checking every possible single deletion. Best core:

- **Anchor in original Egan gauge:** `(3,7)`.
- **Only 116 fixed A/B cell-symbol values out of original 200** are needed to prohibit a common transversal through that cell.
- **84 of the 200 A/B entries are unconstrained wildcards**, yet every full triple containing those 116 values is impossible.
- All 12 anchors produced deletion-minimal nogoods under this explicit relaxed transversal checker, with core sizes `[119,120,123,121,118,116,122,124,123,118,120,122]`.
- An extra **1,000 random deletion orders** for the best anchor did not improve upon 116; this is a local minimization, **not** proof of globally smallest possible obstruction.

**Independent checker:** a Python implementation uses a *fixed row-order* traversal instead of the C++ MRV algorithm. It independently validates the 12 impossible partial patterns, and for **every one of their 1,446 individual known-symbol deletions** (sum of core sizes) it finds a witness transversal in the relaxed model. (This confirms one-literal minimality of the generated cores; it says nothing about global minimum among all cores.) On a **GF(5) complete 3-MOLS positive control**, all 25 cells admit valid A/B common transversals, so the checker does not wrongly eliminate a known existence case.

**Normalize and export SAT cuts:** `E068_normalize_clause.py` renames A and B symbols to make each first row `0..9` and permutes common rows so A first column is `0..9`, matching the full E065 CNF gauge. The best obstruction maps to anchor `(1,7)` and generates a **116-literal implied DIMACS clause**. All 12 independently verified forbidden patterns are exported as 12 sound implied clauses. Proof of logical implication is independent of the SAT solver, but the 12 clauses have **not** been benchmarked for generic CDCL acceleration.

## Critical scope and next decision

**This is an exact partial-assignment cut, NOT a new global nonexistence result.** The partial cut covers complete 3-MOLS assignments that contain a particular normalized 116-symbol pattern. It is **not forced** by a whole E064 first-column branch; therefore **0/1700 top-level classes are excluded**. Clauses derived from a fixed historic pair are unlikely to hit many generic branches unless an invariant **template family** or dynamic generation algorithm is integrated into search.

A defensible next step is **general on-demand cut generation for arbitrary deep partial pairs**, not repeatedly finding more slightly smaller Egan cores. In CDCL/CP search, when partial A/B assignments exclude all possible common transversals through *any* one of the 100 cells, learn a nogood consisting of the known entries used in the conflict (ideally minimized); if exact verifier is too costly, use an explicitly safe relaxation/Hall constraint first. Separately benchmark rank-37 GF(2) upper-bound cuts. Need measure triggered cuts on actual generic E064 branches, and independently verify every cut before proof claims.

## Reproduction

Run from this `e068` directory:

```bash
python E068_independent_verify.py
python E068_normalize_clause.py
# C++ repro optional; source supplied and precomputed cores can be independently verified.
g++ -std=c++17 -O3 E068_partial_transversal_core.cpp -o E068_partial_transversal_core
./E068_partial_transversal_core E068_egan_AB.txt 3 7 20261106 30
```

Files: `E061_near_triple.json` (source fixture), `E068_egan_AB.txt`, `E068_partial_transversal_core.cpp`, `E068_all_12_anchors.json`, `E068_best_core.json`, `E068_independent_verify.py`, `E068_independent_results.json`, `E068_leave_one_out_witnesses.json`, `E068_normalize_clause.py`, `E068_normalized_sound_nogood.json`, `E068_all_12_sound_nogoods.json`, `E068_12_nogoods.dimacs.txt`, `E068_nogood_dimacs_clause.txt`, `E068_MANIFEST.json`.

**All results are reproducible from source without GPU, internet or an external SAT engine.** The raw Egan fixture is a *known two-square pair* and is not a new 3-MOLS(10) construction. This experiment does not change global OPEN status.
