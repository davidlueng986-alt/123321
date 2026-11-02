# E035 — Direct completion and global-search attempt (2026-11-02, 11:53–12:14 UTC)

**Research status: OPEN. No triple of Latin order-10 squares with 100/100/100 pair overlays; no unrestricted nonexistence certificate. The hourly automation must stay enabled.**

## Why this run was necessary

Read the full six-row candidate and the preceding C++/MILP solver files. The E034 record ended with an independently verified six-row partial triple and an integral 40-triangle exact cover of all 120 missing *symbol-pair* constraints. The latter is not enough: an actual extension must also honor missing symbols in EACH column, and row Latin constraints. Earlier E034C already excludes the 39 specific Egan near-triple aligned 4-row anchors, so no more search is spent on them.

Primary/public status: Bright–Keita–Stevens EJC 2026, https://arxiv.org/abs/2503.10504 ; Barnoff–Bright July 2026, https://arxiv.org/abs/2605.02132 . A fresh Nov 2 search found no independently verified full order-10 triple or unrestricted negative certificate. Absence of hits is not proof.

## A. Decisive check of the candidate six-row partial triple

The saved `E034_SIX_ROW_SAT_PREFIX.json` contains 6x10x3 valid rows. The *unconstrained-by-columns* residual triangle hypergraph has exactly 40 mandatory triples forming a 120-edge integral exact cover. However, reconstructing legal column symbols shows 20 of those required triples have **zero permissible columns**. The independent `E035_column_residual.py` rebuilds every candidate quadruple `(column,a,b,c)` and all remaining exact constraints:

- 48 allowed column-specific quadruples (variables), against 240 exact-one requirements (120 pair edges + 120 column-symbol demands).
- **78 exact constraints have zero candidates**: 40 missing ordered-pair constraints and 38 column-symbol demands.
- This specific six-row partial triple is **UNEXTENDABLE** independently of solver heuristics; there is no complete 100/100/100 witness here.

## B. Full-column-aware residual LP relaxation, mathematically sound

For a prefix of `k` filled rows of three partial Latin squares of order `n`, let `x_(c,a,b,z) >= 0` for each symbol triple allowed in column `c`. Every genuine completion induces an **integral exact cover** of `3*n*(n-k)` unused AB/AC/BC pair edges *and* `3*n*(n-k)` missing per-column symbols, with each candidate covering 6 constraints. Thus the relaxation `A x = 1`, `x >= 0` is a necessary condition, not sufficient; `INFEASIBLE` excludes only the given prefix. Feasibility can equivalently be tested by maximizing `sum x` subject to `A x <=1`: required optimum is `n*(n-k)` (all 6*n*(n-k) constraints saturated).

Two completed 100-prefix k4 test batches (`E032_K4_SUPPORT.json`, `E032_K4_SEED131.json`) each gave **200/200 column-LP infeasible** (170 solver-infeasible, 30 support-zero). Separately, 8 deterministic-seed batches of 200 samples each (1,600 k4 prefixes) all failed (1,210 exact-cover unit UNSAT, 390 LP infeasible). All sampled prefixes are search-order-biased and cannot establish a universal order-10 obstruction. One longer 12,000-sample sweep was interrupted after progress was printed but before the final file was written, so it is NOT used as a certified dataset. As positive controls, affine 3-MOLS of prime orders 5, 7, 11 have column-aware LP feasible at k2/k3/k4; their n5/n7 and n5 k4 ILP were also feasible.

## C. Sharper mathematical cuts: exact finite Hall certificates

Every full completion induces a perfect matching between the `n(n-k)` missing column-symbol demands in one square and the `n(n-k)` uncovered ordered-pair demands of any overlay containing that square. Hence each of the six square-vs-overlay bipartite graphs must admit a perfect matching. Missing a perfect matching gives a sound Hall obstruction (not all general LP obstructions are Hall obstructions).

An independently checked concrete order-10 k4 example has **four** mandatory `C`-symbol demands (columns 5,6,8,9 all needing symbol 7 in square C), but those candidates can use only **three** uncovered `A,C` ordered pairs `(0,7),(1,7),(2,7)`. Thus `|N(X)|=3<|X|=4`, impossible in ANY true completion. `E035_verify_hall.js` reconstructs all available candidate cells from the prefix and verifies the inequality without MILP or SciPy. Positive k3 controls: 100/100 Hall-pass. Sample k4 Hall tests: 9/100 and 50/100 failures in two distinct biased datasets; Hall and unit each catch some different instances.

## D. Exact sparse Farkas cuts

For the stronger column+pair incidence matrix `A`, a dual `w` with `sum(w)>0` and for every allowed `(column,a,b,c)`, its six row weights sum <=0, rules out a complete extension exactly. Five target prefix LP duals were converted into integer certificates by conservative floor scaling and independently checked by Python. An integer MILP constrained to weights `{-1,0,1}` with objective minimizing support recovered **four tiny certificates** of sizes **3,5,7,9**, respectively; two additional chosen cases timed out under their 10s budget. All four certificates passed fully independent `E035_verify_sparse_dual.js` replay of every candidate and exact integer inequality. A 3-row certificate expresses the elementary consequence that **two mandatory column-symbol demands must both consume the same one-use ordered pair**. Minimality is only within the stated +-1 integer-dual MILP (when solver returned optimal), not a global mathematical minimal obstruction.

## E. Direct complete three-square SAT attempt, not solved

The system has `libz3.so.4` even though the Python `z3` module is missing. `E035_z3_ctypes.py` interfaces with Z3 through exact ctypes function signatures and uses the verified E031 full three-square OA CNF. For `n=4`, it returned **SAT** and the extracted full matrices independently passed Latin row/column and overlay `16/16/16`. For `n=6` and `n=10`, the solver returned **UNKNOWN** under each 4s and 15s bounded attempt. The order-10 instance has 33,000 Boolean variables / 101,795 clauses. No SAT assignment, unrestricted UNSAT proof, or DRAT/LRAT log was produced.

## F. Actual constructive search that moves partial arrays

`E035_local_search.py` implements randomized whole-row replacement in one of three partial Latin squares, keeping all k4 Latin row/column and all three partial pair overlays valid after every move. Objective is the maximum fractional packing of the column-aware residual constraints, whose necessary threshold for `k=4,n=10` is **60**. From an independently valid random k4 prefix, 400+300+400 iterations improved best fractional packing objective from **54.995779 to 58.309493**, always strictly short of required 60. The best partial arrays are saved and independently revalidated; **NO feasible fourth-row prefix was found**, and no inference is made about full 3-MOLS existence. The move acceptance is a heuristic with no proof of completeness.

## G. Actual next decisive action

1. The true problem remains solve-via-witness-or-unrestricted-proof, not number of local cuts. Continue exhaustive coverage of the E033 **12 cycle-type / 162,959 first-two-row orbit representatives** under globally justified symmetry; a bounded UNKNOWN never contributes to a nonexistence proof.
2. To improve that proof attempt, integrate inexpensive Hall and sparse integer cuts before any expensive full-column LP or exact-cover. Measure *globally different orbit branches excluded*, not random-prefix rejection rate.
3. For construction, invest in legal large-neighborhood searches or full SAT/CP-SAT that can actually produce a 100/100/100 witness, rather than farming near-triple closeness or local obstructions. If any purported SAT witness appears, independently replay the three 10x10 matrices and all three 100-pair overlays before publishing.

## Negative and ambiguous cases

- The much-discussed 6-row / 40-triangle candidate is definitively a **false lead** when column constraints are restored.
- The 12,000-prefix long scan was stopped by the tool timeout before saving a final JSON artifact. Do not report the incomplete run as an exhaustive classification.
- Sparse dual MILP 2/6 chosen prefixes UNKNOWN due to 10-second limits; no UNSAT or minimality claim for those.
- Z3 n6, n10 UNKNOWN under bounded time; no proof certificate.
- The stochastic k4 objective 58.309493 is a fractional relaxation, **not** an orthogonality score, not even a witness for k4 completion.

## Reproduce

`cd research/mols10 && bash E035_REPRODUCE.sh` (provided previous E032/E034 inputs at the indicated paths, or use the accompanying archived dependencies). Main source scripts `E035_column_residual.py`, `E035_bipartite_hall.py`, `E035_verify_hall.js`, `E035_verify_sparse_dual.js`, `E035_z3_ctypes.py`, `E035_local_search.py`, `E035_sparse_motifs.py`. Exact witness files `E035_HALL_WITNESS.json`, `E035_SPARSE_DUAL.json`, `E035_SPARSE_MOTIFS.json`, `E035_LOCAL_SEARCH_BEST3.json`. Individual exact certificates have their own model-independent JavaScript verifier. All existing E034C and E033 conclusions remain unchanged.
