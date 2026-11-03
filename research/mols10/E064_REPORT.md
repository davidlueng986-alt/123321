# E064 — CLOSED-only complete paratopy frontier for 3-MOLS(10)

**Executed:** 2026-11-03 17:46 UTC (2026-11-04 01:46 Asia/Hong_Kong).  
**Global proposition:** There exist three pairwise orthogonal Latin squares of order 10.  
**GLOBAL STATUS: OPEN.** No 100/100/100 witness, no unrestricted nonexistence certificate, no individual order-10 branch proved UNSAT.

## 1. Goal-backward theorem: 1,700 branches constitute complete unrestricted coverage

Let a hypothetical full triple be \(A,B,C\). Independently rename each square's symbols so that its entire first row is \(0,1,\ldots,9\). Use one common row permutation fixing row 0 to make \(A[r,0]=r\). Then define \(f(r)=B[r,0]\) and \(g(r)=C[r,0]\) for each \(r\in\{0,\ldots,9\}\).

**Necessary conditions, rigorously derived:** \(f(0)=g(0)=0\), and the restrictions of \(f,g\) to \(\{1,\ldots,9\}\) are permutations satisfying, for each \(r>0\), \(f(r)\ne r\), \(g(r)\ne r\) and \(f(r)\ne g(r)\). Indeed, the three first-row pairwise overlays contain every diagonal pair \((v,v)\); a duplicate at \((r,0)\) would contradict orthogonality. Therefore \((\mathrm{id},f,g)\) forms a 3×9 Latin rectangle on the remaining nine labels.

The following operations preserve the existence of a **complete** triple and their effect on the first-column pair \((f,g)\) depends solely on the pair, so they induce sound equivalence on the branch inventory:

1. For every permutation \(p\) of labels \(1,\ldots,9\), simultaneously relabel rows, columns and all three squares' symbols by \(p\), fixing 0. This conjugates both \(f\) and \(g\) by \(p\).
2. Exchange the B and C squares: \((f,g)\mapsto(g,f)\).
3. Exchange A and B and reorder rows to restore A's identity first column: \((f,g)\mapsto (f^{-1},g\circ f^{-1})\).
4. Transpose all three Latin squares and independently rename the B/C symbols to restore identity first rows: \((f,g)\mapsto (f^{-1},g^{-1})\).

Together these are the 3×9 rectangle's isotopy/paratopy actions. Every hypothetical order-10 triple is equivalent to a full triple satisfying **one of the 1,700 canonical B/C first-column pairs** in `E064_12_representatives.jsonl`, with A first column and all three first rows identity. Conversely, each SAT solution in any branch is a genuine unrestricted 3-MOLS(10) witness after an independent full overlay check.

**Closure implication:** If all 1,700 branches are proved UNSAT with complete proof-carrying coverage, then 3-MOLS(10) does not exist. If any branch yields verified three full 10×10 Latin squares with 100/100/100 distinct pair overlays, then 3-MOLS(10) exists. The 1,700 cases are a COMPLETE FRONTIER, not 1,700 solved cases.

**Prior-art / independent external verification:** Both counts have appeared in combinatorial enumeration tables: **2,877** isotopy classes of 3×9 Latin rectangles in Brendan McKay's Latin-square data (https://users.cecs.anu.edu.au/~bdm/data/latin.html), and **1,700** paratopy classes in OEIS A393633 (https://oeis.org/A393633). We do **not** claim these enumerations are new mathematics. New project deliverable is the independently replayable, fully scoped reduction from our OA solver to these existing complete catalogues.

## 2. Independently executed group computations

Eight cycle types for the restricted B first-column permutation (on nine symbols):

| Type | Centralizer size | Allowed C first columns | Isotopy orbits |
|---|---:|---:|---:|
| 2+2+2+3 | 144 | 43,424 | 318 |
| 2+2+5 | 40 | 43,412 | 1,094 |
| 2+3+4 | 24 | 43,400 | 1,820 |
| 2+7 | 14 | 43,400 | 3,100 |
| 3+3+3 | 162 | 43,390 | 290 |
| 3+6 | 18 | 43,388 | 2,442 |
| 4+5 | 20 | 43,386 | 2,178 |
| 9 | 9 | 43,387 | 4,843 |

Total **16,085** ordered isotopy orbits. Verified by (i) generator-based exhaustive orbit traversal and (ii) independent enumeration of all centralizer elements plus Burnside's fixed-point formula. All eight counts, centralizer sizes, and allowed-C counts agree exactly. Taking the action of square permutations S₃ gives **2,877** orbits, checked both by disjoint-set union and by Burnside (`(16085 + 3*371 + 2*32)/6 = 2877`). Adding simultaneous row/column transpose reduces to **1,700** paratopy orbits, again checked by DSU and Burnside (`20400/12 = 1700`). All action involutions and S₃ relations passed.

Final orbit-size histogram in the ordered-isotopy quotient: 8 of size 1, 8 of size 2, 115 of size 3, 2 of size 4, 516 of size 6, and 1,051 of size 12; weighted sum `16,085`.

## 3. Full end-to-end controls

`E064_small_order_control.py` independently and exhaustively enumerates all admissible ordered B/C pairs under the full finite group for smaller orders, then solves every canonical first-column branch with the **full five-coordinate DLX**, not the former four-coordinate relaxation:

| n | Raw ordered first-column pairs | Paratopy classes | Complete full-OA outcome |
|---:|---:|---:|---|
| 4 | 2 | 1 | 1 SAT, independently verified 16/16/16 |
| 5 | 24 | 2 | 1 SAT, verified 25/25/25; 1 branch exhaustive UNSAT |
| 6 | 552 | 3 | 3/3 branches exhaustive UNSAT; 1,203 total DLX nodes |

Thus the **same globally complete branch scheme actually closes n=6**, while n=10 remains OPEN. The old unrestricted n=6 DLX needed 200,601 nodes; the new scheme needs 1,203 across three branches. These node counts are implementation measurements and must not be extrapolated to order 10. The solver's `UNSAT_EXHAUSTIVE` is an exhaustive replayable algorithmic result, not an independently formalized DRAT/LRAT proof.

## 4. Order-10 tests — all negative in the *epistemic* sense

- Every one of the 1,700 canonical first-column pairs was screened against all 1,000 exact-cover resource classes after the 19 forced first-row/first-column cells. **0/1,700 had zero support; no globally impossible branch was certified by this easy test.** 36,123,300 allowed cell placements occurred across these 1,700 tests, not independent partial solutions.
- Ten widely separated branch representatives from all eight restricted B-cycle types were probed with SciPy HiGHS on the *complete 810-equation residual 5-coordinate LP*. **10/10 numerically feasible**, errors at most 3.34e-10. This is not an exact-rational integer witness, nor a full MOLS solution. More sampling of this weak LP is not a priority.
- Twenty-five sampled canonical first-column branches received ~0.45s full DLX each: 25 UNKNOWN_BUDGET, no SAT or exhaustive UNSAT.
- Two different canonical branches were searched for ~12s each: 1,638,400 nodes and 1,556,480 nodes, respectively, both UNKNOWN_BUDGET.
- Three additionally replayed branches at ~0.1s each remain UNKNOWN_BUDGET. **0 full-order-10 branch proofs completed**.

Hence neither 1700 nor 1,700 minus any amount should be presented as a resolved fraction. No legitimate progress-to-CLOSED percentage or ETA can be inferred.

## 5. Files and reproduction

Execute `bash E064_REPLAY.sh` in this folder. It compiles the two independent 16,085-orbit enumerators, the S₃/transpose quotient generator, full five-coordinate OA DLX and root-support screen; it regenerates **all 1,700** unique representatives, validates every first column, checks both independent Burnside counts, and independently enumerates complete order-4/5/6 solution/control branches. No network access required. Run `python E064_BRANCH_RUNNER.py --start 0 --count 5 --seconds 1 --max-nodes 1000000` for explicitly bounded on-demand order-10 branches; the runner immediately checks any SAT witness and writes the complete 100/100/100 matrices. **Do not interpret UNKNOWN as UNSAT.** There is no scheduled automation.

Independent verification resources: `E064_ordered_orbit_counts.jsonl`, `E064_independent_burnside.jsonl`, `E064_quotient_counts.txt`, `E064_small_order_cover_12.json`, `E064_all1700_root_support.json`, `E064_root_lp_probe.json`, `E064_sample_branch_results.json`, `E064_deep_branch_0000.json`, `E064_deep_branch_1699.json`, and SHA256 `E064_MANIFEST.json`.

## 6. Research decision

**Only objective: unrestricted CLOSED.** The known 3×9 paratopy classification gives a mathematically complete 1,700-branch search frontier. Unlike E052–E057 fixed-prefix certificate polishing, each globally closed branch here would directly satisfy a named obligation in a full nonexistence proof. The obstruction is still algorithmic: exact 5D branches remain enormous under plain DLX and weak LP. The next defensible step is proof-producing CDCL/LRAT or stronger exact constraint propagation *within the same complete 1,700 representatives*; independently validate every completed branch, or produce one full 100/100/100 triple. No claim of novelty for 1,700 catalogue itself, and **no claim of resolution**.

Hourly MOLS10 automation remains disabled at the user's request. Work in this report was executed only during the present chat turn.
