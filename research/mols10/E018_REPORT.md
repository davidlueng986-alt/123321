# MOLS10 E018 — Independent compact MILP, bounded Parker attempt (OPEN)

**Timestamp:** 2026-11-01 21:47–21:51 UTC. **Scope:** independently formulated exact fixed-first-square MILP for historical Parker A, not unrestricted 3-MOLS(10). Read `STATE.json` at prior E017 state commit `235df6ab4b8883fe27cfb644982e85c3ca841d36` and [living Drive journal](https://docs.google.com/document/d/1NDPWEMM3Cf5HrhdOcV6pVE9tCI-kxKbavxcfIBFva3k/edit) before experiment.

## External resolution audit
Primary [Bright–Keita–Stevens, *Electronic Journal of Combinatorics* 33(1), #P1.30, 2026-02-13](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30) explicitly states unrestricted 3-MOLS(10) open. [Barnoff–Bright, arXiv:2605.02132v2, 2026-07-04](https://arxiv.org/abs/2605.02132) concerns SAT techniques for orthogonal *pairs*, not a triple. Targeted web/arXiv search 2026-11-01 found no independently checkable complete witness or unrestricted proof. Search absence is not proof of absence.

## Exact integer model and proof
For a fixed Latin square A of order n, enumerate **all** its transversals `T_0,...,T_(m-1)` using a standalone symbol/column-mask DFS (independent of E016/E017). Binary x_i selects transversal i as a B-symbol class; y_i similarly for C. Require, for each cell q, `sum_(i:q in T_i) x_i = sum_(i:q in T_i) y_i = 1`. These exact covers imply `sum_i x_i = sum_i y_i = n`. Let `K(i)={j: |T_i ∩ T_j|=1}`. Impose

```
sum_(j in K(i)) y_j >= n*x_i,    sum_(j in K(i)) x_j >= n*y_i
```

for every i. Because exactly n opposite-side transversals are selected, when x_i=1 all selected y_j must lie in K(i), and vice versa. Thus every B-class intersects every C-class in exactly one cell, exactly the B/C orthogonality condition. Conversely any 3-MOLS containing A yields such binary vectors. **Hence the binary MILP is equivalent to fixed-A triple existence, without E015's partial-support approximation.** It is not a global model covering arbitrary A.

Optional valid cuts: if two disjoint A-transversals T_i,T_j have no C-compatible transversal covering some cell, they cannot both be B classes (nor both C classes). Add `x_i+x_j<=1`, `y_i+y_j<=1`. The exhaustive Parker pair audit found **226** blocked pairs among **236,104** disjoint unordered pairs (0.09572%), giving **452** valid cuts. All 1104 individual T_i passed the one-class cell-support check. The pair cuts are therefore weak locally; deeper search is needed. This pair-level count is a new *project computation*, not a claim of literature novelty.

## Actual bounded experiments (SciPy 1.17 / HiGHS, Python 3.13, CPU)
See `E018_RESULTS.json` for commands, timings, source SHA-256 and failures.

| Input | Transversals | Variables | Rows | HiGHS status | Evidence |
|---|---:|---:|---:|---|---|
| GF(4) order 4 | 8 | 16 | 48 | 0 / optimal | SAT; independently verified 16/16/16 overlays |
| One intercalate-traded cyclic order 6 | 32 | 64 | 136 | 2 / infeasible | Complete fixed-A UNSAT negative control |
| Parker A | 1104 | 2208 | 2408 | 1 / time limit (8s) | **UNKNOWN**, no incumbent |
| Parker A + 452 valid cuts | 1104 | 2208 | 2860 | 1 / time limit (8s) | **UNKNOWN**, no incumbent |
| Order 6 + cuts | 32 | 64 | 544 | 2 / infeasible | Complete negative control |

Parker base model: **873,976 nonzeros**, setup 0.852s, total 11.205s. Cut model: **874,880 nonzeros**, setup 3.411s, total 14.984s. Solver time limit is separate from preprocessing. **No Parker MILP UNSAT certificate** and no 100/100/100 witness. This neither independently confirms nor refutes E017's Parker fixed-A exclusion; it establishes a second exact encoding with positive/negative controls.

Failures preserved: first attempted cyclic order-6 negative control had zero transversals and triggered a zero-variable `milp` error (now handled by a mathematically valid early UNSAT return). First paircuts edit shadowed `coo_matrix` and caused `UnboundLocalError`; fixed before completed tests. Both Parker MILPs timed out, so results remain UNKNOWN. No DRAT/FRAT certificate or symmetry coverage for unrestricted A.

## Reproduction

```bash
cd research/mols10
OPENBLAS_NUM_THREADS=1 python E018_compact_milp.py --case gf4 --seconds 6
OPENBLAS_NUM_THREADS=1 python E018_compact_milp.py --case order6 --seconds 5
OPENBLAS_NUM_THREADS=1 python E018_compact_milp.py --case parker --seconds 8
OPENBLAS_NUM_THREADS=1 python E018_compact_milp.py --case parker --seconds 8 --paircuts
```

Input `parker_pair.json` first square SHA256 (compact JSON): `1694eda37452b6709d8f8d77d8dfcddae08e18c6a94e4aabc102bec6323c1c77`. Code local SHA256: `65b879abdbf62f2a1d652d93ee3a324e843bdcd96cf9a18f829a7e71637fb224`. [Code commit](https://github.com/davidlueng986-alt/123321/commit/8c429d2551d6a2a031f16d0ee80912bf50c2a55f); [results commit](https://github.com/davidlueng986-alt/123321/commit/778d3c58a3f148dbc1aa4e020f3c47326735849b).

**Next E019:** Add sound symmetry breaking to the exact MILP; test longer but bounded SAT/MILP with complete solver status and, if UNSAT, independent proof certificate; prioritize importing the eight published Myrvold unresolved orthogonal pair types as diverse first-square inputs. Do not repeat Parker 8-second UNKNOWNs without a substantive formulation change. **Global status: OPEN.**
