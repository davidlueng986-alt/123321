# E060 — CLOSED-only mission: full OA search and exhaustive 6-row anchored endgames

**UTC date:** 2026-11-03. **Global status:** `OPEN` (no 100/100/100 witness; no unrestricted nonexistence proof). **Execution:** user-triggered only; hourly automation remains paused.

## The single success criterion

CLOSE 3-MOLS(10): either supply complete three 10x10 Latin squares and independently check all Latin rows/columns and all three 100/100/100 orthogonality overlays, or supply an unrestricted mathematical proof / proof-checkable UNSAT with complete symmetry coverage. Local results, code, search nodes and certificates do not count as closing the problem.

## Main route A: unrestricted full five-coordinate OA(100,5,10,2) model

Represent a candidate as an assignment `(r,c,a,b,d)` covering exactly ten exact-cover resources: one `(r,c)` cell, six `(square, row/col, symbol)` pairs, and three `(square-pair, symbol-pair)` combinations. A full integral exact cover therefore is *equivalent* to three MOLS of order n, not a four-coordinate relaxation.

Complete sound symmetry normalizations:
1. Independently relabel each square's symbols so that its first row is `0,1,...,n-1`.
2. Permute physical rows 1..n-1 to make A's first column `0,1,...,n-1`.
3. Every non-first-row triple `(a,b,d)` consists of pairwise distinct symbols: any equal pair `(x,x)` already occurs in the first row at column x. Each component is distinct from c in column c because of the normalized first row.
4. In column 0, force `a=r` from the normalization. All remaining legal options are exhaustively represented; no unproved `B`/`C` second-row normalization.

The exact-cover model has `10*n^2` equalities, each binary option has ten incidences. Script `E060_full_OA_milp.py` builds the sparse matrix and invokes SciPy/HiGHS with 0-1 integrality and bounded walltime.

| Order | Options | Equalities | Nonzero incidences | Outcome |
|---|---:|---:|---:|---|
| 4 | 64 | 160 | 640 | `SAT`, independent JavaScript Latin + 16/16/16 validation PASS |
| 5 | 413 | 250 | 4,130 | `SAT`, independent JavaScript Latin + 25/25/25 validation PASS |
| 10 | **41,338** | **1,000** | **413,380** | **`UNKNOWN_BUDGET`**, HiGHS time-limit ≈21.45 sec (configured 20 s). |

The order-10 search did NOT exclude any branch, and there is NO proof of unsatisfiability. The solver returned no primal incumbent. Its 41,338 choices are a smaller but still very hard full OA model, not an end-to-end speedup claim.

## Secondary construction route: published nine-row source, deeper endgame

Source: Jäger, Markström, Öhman, Shcherbak (2024), *Enumeration of Sets of Mutually Orthogonal Latin Rectangles*, EJC 31(1) #P1.53, Figure 3. Published 9×10 triple is independently transcribed in `E059_2024_9x10_analysed.json` and previously checked at 90/90/90. This is ONE historical 9×10 example, **not the set of all 9×10 triples**.

Prior E059 checked all 9 eight-row restrictions from that example; 5,392 complete last-two-row Latin combinations; 0 100/100/100.

E060: for each of `C(9,2)=36` seven-row restrictions, exhaustively enumerate row eight as three simultaneous Latin row permutations preserving all 80/80/80 partial overlays, and then enumerate all two-row Latin completions of each square, checking the full 100/100/100. Result: **36/36 exact fixed-prefix UNSAT**, zero UNKNOWN, zero complete witness.

To push a further row back, for each of `C(9,3)=84` six-row restrictions, independently generate all seventh rows via every Latin matching in each square and all cross-square allowed overlay pairs; then run the complete seven-row endgame above for each. Actual run: **84/84 fixed six-row anchors UNSAT**, **431** valid seventh-row triples exhaustively extended, **0** timeouts/UNKNOWN, **0** full witness, ≈17.88 s on local Python+NumPy. Across these 84 anchors each square had 784–896 valid candidate seventh rows; compatibility mask intersections are complete. Earlier pure-Python non-vectorized pilot independently reproduced the first five seventh-row counts `[3,4,5,5,5]` and excluded those five anchors.

**Scope:** This establishes the finite statement that no full 3-MOLS(10) contains the same six physical rows, simultaneously across all three squares (with this row/symbol alignment), as any of the 84 six-row restrictions of **this one** 2024 source. Row permutations of the full triple preserve that statement. It does **NOT** exclude arbitrary six-row partial triples, any complete E033 first-two-row orbit, or prove global nonexistence. It also does not justify a quantitative fraction of the unsolved global space.

## Proof integrity / failures

- Positive controls n4/n5 passed independent JavaScript full-output replay. The JS checker also audits 84 result records and totals but **does not independently re-prove the 84 UNSAT statuses**. The complete Python enumeration is supplied for reproducibility.
- The E060 global MILP exhausted a *20-second time budget*. `UNKNOWN` is not `UNSAT`.
- Previous universal k4 column-aware LP/ILP infeasibility approaches are refuted by E059 exact counterexamples; E060 did not reuse them as global gates.
- All historic published sources are credited; no novelty claim for the 9-row source.

## Reproduce

```bash
# in research/mols10; requires numpy and scipy
OPENBLAS_NUM_THREADS=1 python E060_full_OA_milp.py
OPENBLAS_NUM_THREADS=1 python E060_seven_row_completion.py --seconds 10
OPENBLAS_NUM_THREADS=1 python E060_all_six_row_extensions.py
node E060_validate_outputs.js
```

`E060_full_OA_milp.py` outputs full order4/order5 witness matrices and a strictly bounded order10 result; the exhaustive anchored scripts write structured JSON results. The input `E059_2024_9x10_analysed.json` is already in this branch.

## Only next useful actions toward CLOSED

1. **Existence:** improve a full five-coordinate OA solver (not a four-coordinate relaxation), ideally with globally sound symmetries and cross-square row search, so that a returned 100/100/100 candidate can be independently replayed. Exploit 2024 MOLR only as a source of seeds, not a completeness assumption.
2. **Nonexistence:** prove a universal obstruction on *all* valid six-row triples, or exhaustively cover *all* normalized first-two-row `(f,g)` orbits AND every `C` continuation with independent proof objects. The 84 anchored exclusions do not start closing that global obligation.
3. Avoid more polishing of the 84 local exclusions without a convincing path to an unrestricted theorem. Main goal stays CLOSED, current result stays OPEN.

Source links: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v31i1p53 ; https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 .