# MOLS10 E019 — exact depth-3 C-support obstruction (2026-11-01, ~22:47 UTC)

## Status and provenance
**GLOBAL PROBLEM OPEN.** Fresh targeted search on 2026-11-01 found no independently verifiable complete 3-MOLS(10) construction or unrestricted nonexistence proof. Primary sources checked: Bright–Keita–Stevens, *Electronic Journal of Combinatorics* 33(1), P1.30 (2026), https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 and https://arxiv.org/abs/2503.10504 ; Barnoff–Bright, arXiv:2605.02132 (2026), https://arxiv.org/abs/2605.02132 . Search absence is not a proof of openness.

## Falsifiable objective
E018 found only 226 depth-2 C-support blockers among 236,104 disjoint unordered pairs of Parker A-transversals, while an 8-second exact MILP run remained UNKNOWN. Test whether depth-3 blockers are substantially stronger, **without repeating that unchanged MILP run**. Work with the published Parker first square A, SHA256 of compact JSON array `1694eda37452b6709d8f8d77d8dfcddae08e18c6a94e4aabc102bec6323c1c77`. Transversals are indexed by lexicographic DFS / permutation order.

## Mathematical validity
For a hypothetical triple (A,B,C), each B-symbol class is an A-transversal, and each C-symbol class is also an A-transversal. Since B and C are orthogonal, any C-symbol class intersects each chosen B-symbol class in **exactly one cell**. Thus, for any selected partial B-classes S, each of the 100 cells must belong to at least one A-transversal intersecting **every** member of S exactly once. A cell with no such transversal is a rigorous obstruction to extending that partial B assignment.

For three pairwise disjoint B-class candidates `T_i,T_j,T_k`, a witnessed unsupported cell yields the valid 0–1 cut `x_i + x_j + x_k <= 2` for the B-side of E018 exact MILP, and analogously on the C-side. This is a **necessary cut**, not an unrestricted theorem. It is sound even if all three depth-2 subsets are individually feasible by the same support test.

## Actual bounded computations
1. Parker A: **1,104** A-transversals; **236,104** unordered disjoint pairs; **226** depth-2 support blockers (E018 reproduced).
2. **Exhaustive rooted slice**, with first selected class fixed to transversal index 0: all **39,528** pairwise-disjoint triples `{0,j,k}` were tested. **29,973** (75.83%) have a C-support obstruction; **23,296** (58.94% of all rooted triples) are genuinely new depth-3 blockers: all three of their depth-2 subsets pass the cell-support test. The earliest explicit witness is `(0,109,250)`, unsupported cell index **41** (row 4, column 1, zero-based). This provides 23,296 valid rooted 3-way cuts for **each** B/C side, but they only activate if class 0 is selected.
3. Separate deterministic sampling: seed 19, 20,000 trials, each drawing a depth-2-surviving unordered pair uniformly and then a third class uniformly from those disjoint from both. All 20,000 attempts had eligible third classes; **10,140** were blocked and **9,860** passed the necessary support test. This is **not** a uniform sample of all unordered triples, and repeats are possible. Do not extrapolate its 50.7% to the entire search space.
4. Independent implementation replay: stdlib `itertools.permutations` enumerated all 10! row-column permutations, reproducing 1,104 A-transversals and independently reconstructing the complete rooted 39,528 / 29,973 / 23,296 counts. Independently checked ten sampled blocked witnesses and the rooted witness against all 1,104 possible C transversals. Local `python -m unittest -v test_E019_depth_support`: **2 tests passed in 4.096 seconds**. Main run **2.983 seconds** (local CPU). These are local results; CI not yet claimed.

## Reproduction
```sh
cd research/mols10
python E019_depth_support.py --sample 20000 --seed 19 --output E019_RESULTS.json
python -m unittest -v test_E019_depth_support
```
Code: `E019_depth_support.py`; results and explicit witnesses: `E019_RESULTS.json`; independent replay: `test_E019_depth_support.py`. No GPU used.

## Failures, scope, uncertainty
- E018 Parker MILP 8-second attempts remain **UNKNOWN**, not UNSAT. No new Parker MILP solver run was made here; this iteration measured a stronger cut family instead.
- 23,296 new blockers are exhaustive **only for the rooted index-0 slice**; not all Parker A triples, let alone arbitrary first squares.
- No full B/C exact-cover completion was attempted. Passing the support condition is not a proof of extendability.
- Neither a 100/100/100 triple nor an unrestricted impossibility certificate was obtained. Independent CI execution remains to be checked after commit.

## Concrete next E020 action
Implement a **lazy 3-way support-cut separator** for E018 exact MILP or SAT search, preferably on-demand at partial B/C assignments, rather than preloading all root-0 cuts. Add proven B/C symmetry breaking, benchmark GF(4) SAT and order-6 UNSAT controls, then run a short, explicitly time-limited Parker comparison. Preserve UNKNOWN and record solver nodes/cuts. In parallel import published Myrvold eight residual pair patterns to diversify first-square families.
