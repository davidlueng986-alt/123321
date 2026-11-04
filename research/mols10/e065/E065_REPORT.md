# E065 — Direct complete 3-MOLS(10): two incremental SMT/SAT backends and independent proof pipeline

**Date:** 2026-11-04. **SOLE SUCCESS CRITERION:** mathematically **CLOSE** 3-MOLS(10), either by three independently verified order-10 Latin squares with all pairwise overlays `100/100/100`, or by an unrestricted proof of nonexistence with sound symmetry coverage and independently checked UNSAT proofs. **Current status: OPEN.** User-disabled hourly automation stays disabled.

## 1. Motivation and direct logical closure chain

E064 established a proven, complete and literature-consistent list of **1,700 first-column paratopy representatives**. Each representative fixes the first column of squares B,C while all three first rows and square A's first column are normalized to identity. All potential triples are equivalent to one of these cases. There is **no gap in the branch inventory**, subject to E064's group-action proof.

For positive closure: any branch SAT assignment must decode to three Latin squares of order 10 with **100 distinct pairs** in each A/B, A/C, B/C overlay. For negative closure: each of all 1,700 branches must have a full checkable UNSAT derivation (or one stronger universal proof). `UNKNOWN` does not count; no proportion-to-closure estimate is justified.

## 2. Native SAT backend A: Boolean CNF + incremental Z3 C API

`E065_cnf.py` writes DIMACS from first principles. For all three squares, each `(row,column)` has exactly one symbol, each `(row,symbol)` occurs exactly once, and each `(column,symbol)` occurs exactly once. For each of the three symbol-pair overlays, an auxiliary Boolean y indicates a cell exhibiting an ordered pair and implies the corresponding two x-values; a disjunction forces every ordered pair to appear at least once. Since there are exactly `n*n` cells and `n*n` ordered pairs, coverage implies they appear **exactly once**. First-row identity for each square and first-column identity in square A are sound normalizations. **No unproved B[1,0] < C[1,0] restriction is present.**

Order-10 CNF: **33,000 variables, 101,740 clauses**. `E065_incremental_z3.cpp` builds **one** native Z3 solver instance and passes branch B/C first-column assignments via `Z3_solver_check_assumptions`; it independently decodes and validates every SAT witness. Incremental reuse is technically enabled, but **performance gains from shared learned clauses have not been established**.

## 3. Native SAT/SMT backend B: 5-coordinate pseudo-Boolean exact cover

`E065_pb_oa.cpp` implements a **different logical encoding** from the CNF: one Boolean per legal full placement `(row,column,A,B,C)` after sound normalizations, and `Z3_mk_pbeq` equal-to-one constraints across **all ten resource classes**: row-column, row/column with each of three symbol variables, and the three pairwise symbol overlays. There are **41,338 order-10 Boolean placements and 1,000 exact-one equations**. The ROW coordinate is retained; no false four-coordinate relaxation is used.

A selected assignment is exactly a complete OA(n²,5,n,2). Each SAT model is independently verified using Python, not trusted solely on solver output.

## 4. Executed tests

| Test | CNF incremental Z3 | PB incremental Z3 | independent reference |
|---|---|---|---|
| order 4, first-column class | SAT; `16/16/16` | SAT; `16/16/16` | independent Python matrix checker |
| order 5, both first-column classes | class 0 **UNSAT**, class 1 SAT; `25/25/25` | SAME: class 0 UNSAT, class 1 SAT | full paratopy cover from E064 |
| order 6, all first-column classes | **3/3 UNSAT** under assumptions | **3/3 UNSAT** under assumptions | separately compiled C++ DLX exhaustively proved all 3 cases in 438+398+367=1,203 nodes |
| order 6, unbranched | UNKNOWN after 12 s | UNKNOWN after 10 s | demonstrates critical value of safe global symmetry branches |
| order 10, first three branches, 5 s each | 3/3 **UNKNOWN** | 3/3 **UNKNOWN** | neither SAT nor UNSAT demonstrated |
| order 10, **16** representatives sampled across **all eight** cycle types, 2 s each | **16/16 UNKNOWN** | **16/16 UNKNOWN** | 16 distinct cases per encoding; no branch closure |

The 16 branches include the first and midpoint representative from each of eight cycle types; remaining 16 further randomized sample IDs have been prepared but **not counted as tested**. No order-10 individual paratopy class is proved UNSAT. All SAT models generated in small-order controls were checked for every Latin row/column and all three overlays.

The **same** Z3 library underlies both encodings. They are independently written encodings and are crosschecked against an independent DLX algorithm for order 6; they are **not** independent UNSAT proof checkers for order 10.

## 5. Proof-carrying branch CNF, and remaining gap

`E065_branch_dimacs.py` converts a canonical branch into an ordinary, explicitly recorded **standalone DIMACS formula** by appending the necessary 2(n-1) first-column unit clauses to the full base CNF. The independent test at order 5 exactly reproduced **branch 0 UNSAT** and **branch 1 SAT** with the same Z3 engine. SHA-256 checksums are recorded.

`E065_cadical_proof.sh` is an **unexecuted optional external solver interface**: where CaDiCaL plus `lrat-check` are installed, run the standalone branch CNF with `--lrat --no-binary --no-factor`, distinguish result exit codes 10 (SAT), 20 (UNSAT), and 0 (UNKNOWN), independently verify SAT models using `E065_verify.py`, and refuse to declare an UNSAT branch closed unless the LRAT checker reports VERIFIED. The local container has `libz3.so.4` but **no installed CaDiCaL or lrat-check**, and outbound network access is unavailable. Thus **no LRAT proof has yet been generated or checked** in this run.

For any order-10 branch, a successful `UNSAT` proof would close that *one* branch only, not the theorem. An independently verified `SAT` witness would immediately close the whole existence problem.

## 6. Decision — no inflated progress

The complete normalized OA problem is now encoded by two executable incremental backends; the 1,700-branch inventory and independent small-order positive/negative checks are connected. The critical order-10 result **remains UNKNOWN for every tested branch**. No solver time estimate is defensible. Longer undirected brute-force runs would merely increase node/conflict counts; prioritize genuine proof-producing CDCL with externally checked proofs and strong branch-safe propagation, or novel unrestricted structural theorems.

**Scope:** no mathematical resolution yet; 0/1,700 order-10 classes proved UNSAT. No autonomous hourly tasks reenabled. All experiments in this report were executed interactively.