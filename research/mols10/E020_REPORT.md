# MOLS10 E020 — Unary exact-cover obstruction for Parker first square

**Run:** 2026-11-01 ~23:45–23:50 UTC. **Global status: OPEN.** **Scope: one specified first Latin square, not unrestricted 3-MOLS(10).**

## Sources checked before experiment
- Bright–Keita–Stevens, *Electronic Journal of Combinatorics* 33(1), P1.30 (2026-02-13): https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; arXiv: https://arxiv.org/abs/2503.10504 .
- Barnoff–Bright, arXiv:2605.02132v2 (2026-07-04): https://arxiv.org/abs/2605.02132 .
- Targeted fresh November 1 searches for order-10 orthogonal triples and new arXiv claims. **No independently verified unrestricted solution found.** Absence of a search hit is not a proof of openness.

## Why change direction from the E019 plan?
E019's 23,296 rooted depth-3 cell-support cuts are valid, but E017 already checks the **full partial support condition at every DFS node**. Adding only those cuts to the old DFS would duplicate its pruning. Instead we tested a **strictly stronger exact-cover necessary condition at depth 1**, potentially yielding unary exclusions and a shorter fixed-A certificate.

## Mathematical lemma (fixed A)
Let \\(\\mathcal T(A)\\) be all transversals of Latin square \\(A\\). For each \\(U\\in\\mathcal T(A)\\), define \\(E_A(U)\\) as existence of ten pairwise disjoint transversals \\(V_0,\\ldots,V_9\\) covering all 100 cells, with \\(\\lvert V_j\\cap U\\rvert=1\\) for each \\(j\\).

If \\((A,B,C)\\) is a triple, every symbol class \\(U\\) of \\(B\\) satisfies \\(E_A(U)\\), witnessed by the ten symbol classes of \\(C\\). Thus a transversal for which \\(E_A(U)\\) is false **cannot** appear as a \\(B\\)-symbol class in a triple. If the union of all surviving \\(U\\) does not cover every cell, no triple containing this particular \\(A\\) exists.

The exact-cover solver enumerates all A-transversals, restricts candidate C-symbol classes to those intersecting \\(U\\) once, and recursively selects pairwise-disjoint classes. At each step it branches on the uncovered cell with the fewest eligible classes (MRV). This is complete for the finite exact-cover instance if no budget is hit; an exhausted branch proves **only that fixed root** infeasible.

## Actual bounded computation
Input: published Parker first square (embedded in code), compact-JSON SHA-256 `1694eda37452b6709d8f8d77d8dfcddae08e18c6a94e4aabc102bec6323c1c77`.

- **1,104** transversals of Parker A, each tested as a possible B-symbol class.
- **1,076** roots: `UNSAT_EXHAUSTIVE` for existence of compatible C exact cover.
- **28** roots: `SAT` with an explicit 10-transversal C partition replayed cell-by-cell.
- **0** `UNKNOWN_BUDGET`; per-root 0.25-second / 100,000-node cap, maximum observed 4,853 nodes. Total **1,371,185** DFS nodes (1,359,676 in UNSAT roots, 11,509 in SAT roots); ~**9.155 s** CPU for full 1,104-root scan (includes setup).
- Surviving indices: `[26,29,50,55,165,167,195,202,380,395,438,453,512,531,547,563,577,643,663,727,844,850,853,915,924,950,963,1060]`.
- **13 cells not covered by any surviving root**: zero-based flattened indices `[2,13,24,35,46,50,61,77,78,79,88,97,98]`.

**Consequence:** No 3-MOLS(10) triple can have **this specified Parker first square A**. This is a new compact conditional computational certificate independent of the E017 two-square-partition DFS strategy; it does **not** classify all order-10 first squares.

## Cross-checks
- A second stdlib enumerator checked all \\(10!=3,628,800\\) permutations; its ordered 1,104 transversal masks exactly match the DFS enumeration (local ~2.54 s).
- Independently formulated SciPy/HiGHS MILP (one C exact-cover partition) gives solver-complete **INFEASIBLE** for roots 0, 109, 250 (2.605 s / 2.899 s / 2.940 s); **FEASIBLE** for roots 26, 29, 55 (1.007 s / 3.100 s / 1.302 s), with 100-cell independent replay. These are **six spot checks**, not independent solver certificates for all 1,104 roots.
- GF(4) positive control: 8/8 transversals satisfy unary exact-cover SAT; no false fixed-A exclusion. Full stdlib GitHub CI regression runs all 1,104 Parker roots and GF4.
- The E018 exact two-mate Parker MILP 8-second attempts remain **UNKNOWN**; E020 does not reinterpret them as UNSAT.

## Reproduction and evidence
```sh
cd research/mols10
python E020_unary_exact_cover.py --limit 1104 --seconds 0.25 --nodes 100000 --output E020_FULL_REPLAY.json
python -m unittest -v test_E020_unary_exact_cover
# Optional separate solver implementation, requires scipy:
OPENBLAS_NUM_THREADS=1 python E020_milp_replay.py --roots 0,26,109 --seconds 8
```
- `E020_unary_exact_cover.py`: full exact-cover enumeration and per-root output, no third-party packages.
- `test_E020_unary_exact_cover.py`: independent 10! transversal enumeration and GF4 control; checks all 1,104 root statuses and uncovered cells.
- `E020_milp_replay.py`: independent MILP spot-checks, using n! enumeration.
- `E020_RESULTS.json`: checked-in compact summary. Full per-root trace is reproducibly generated by the main script but **not** checked in as a separate 1,104-case JSON file.

## Failures, limits, next action
No budget failures in E020. Independent HiGHS checks cover only 6 roots; exhaustive result relies on correct stdlib DFS implementation and regression tests, not an externally checked SAT/DRAT/FRAT proof. Novelty relative to literature is unestablished. The 13-cell obstruction excludes only the exact labeled Parker A and its symmetry equivalents; it is **not** an unrestricted impossibility proof.

**E021:** independently verify all 1,076 unary UNSAT roots using a different exact-cover implementation or proof-producing SAT; classify the 28 survivors under Parker autotopisms, and apply the unary screen to the 8 published Myrvold residual first-square constructions. Avoid re-running the already exhausted Parker E017 DFS. Keep global OPEN and automation enabled.
