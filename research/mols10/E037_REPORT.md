# E037 — Evidence-first 3-MOLS(10) global-distance audit and all-15 Hall projections

Timestamp: 2026-11-02T13:15:08.904561+00:00. **Unrestricted 3-MOLS(10) remains OPEN.**

## Real distance to solution
The prior E033 classification yields **12 canonical cycle types and 162,959 two-row (A,B) orbit representatives**. As checked against latest STATE.json (E036), **zero whole orbits have been proved UNSAT**; no 100/100/100 witness or unrestricted negative proof. The E036 156/156 six-row construction for one f-type is a positive *partial* result, not a measure of being near a 10-row witness. This project has **no defensible ETA**. A bounded search node count is not a solved fraction.

## New mathematically sound necessary condition
After k complete rows, let `P0,P1,P2` be the remaining ordered symbol pairs AB/AC/BC, and `C0,C1,C2` be the remaining (column,symbol) demands in each square. Every full completion uses exactly one resource from each of these six classes per future cell, each class having `n(n-k)` demands. Therefore for **every unordered pair of classes** (15 pairs), candidate future placements induce a perfect matching. If any one of the 15 bipartite graphs violates Hall's condition, the **specific partial triple** cannot be extended. Previous E035 code checked only 6 incident pair-to-column projections.

## Actual experiments (not exhaustive)
* Deterministic f-type 2+2+2+2+2 experiment: 1,000 independent-seeded three-row and 1,000 four-row valid prefixes (some may be isomorphic or sampling-order correlated). At k3 **0/1,000** violate all-15 Hall. At k4, old-six rejects **155/1,000**; all-15 rejects **179/1,000**, with **24 new-only**. First 100 were 15 versus 18.
* Cross-type sanity: 30 valid four-row prefix examples for each of the 12 lawful f cycle types (**360 total**). Exactly **43** have a directly proven zero-support demand; remaining **317** returned SciPy LP `INFEASIBLE_SOLVER` (no exact Farkas dual for this batch — classify as numerical evidence). No LP-feasible candidate found in this nonuniform sampling. Old-six Hall rejects **57**, all-15 rejects **65** (+8). Independent pure Python matcher rebuilt all **360** cases and agreed exactly. These are **not** 360 globally excluded orbit classes.
* A concrete new-only Hall witness (`E037_NEW_HALL_WITNESS.json`) has **2** distinct `C0` column-symbol demands whose entire `C1` neighbor set has only **1** member (matching 59/60). Standalone stdlib verifier reconstructs each allowed placement (348) and proves exact Hall deficiency; a deliberately corrupted neighbor set is rejected. Positive controls from complete affine triples at n=5,7,11 also pass.
* Ten additional independent f=2^5 random-g greedy constructions reached six valid rows with overlays 60/60/60, but all their chosen four-row prefixes fail column-aware support or LP, and their chosen six-row prefixes cannot make a seventh with this fixed greedy route. This is deliberately **not** claimed to rule out any orbit.

## Important failed experiment
A 5-restart × 1800-step LP-guided optimization attempted earlier was killed by a 200-second wall limit, with no complete output; do not count an improved score or infer solver success. The principal bottleneck is repeated large LP optimization; a candidate 58.3/60 from E035 was a relaxation and does not quantify closeness.

## Impact and honest limitations
The all-15 Hall extension is a **sound, cheap global-search pruning rule**, but its empirical incremental rejection is small: +24/1000 and +8/360. Alone it does not establish meaningful global progress toward a solution. Most (295/360) four-row examples that survive Hall15 were still LP-infeasible according to the numerical solver, highlighting the need for stronger **exact, reusable and genuinely global** branch elimination.

## Next action toward complete solution
1. Feed the 15 Hall projections into a fully symmetric exhaustive **12-type / 162,959-orbit** OA solver. Every orbit requires a completed search or verified positive witness, not a sample.
2. Prioritize **constructing a counterexample to the apparent four-row LP barrier** (a valid 4-row partial 3-MOLS(10) whose column-aware residual LP is feasible); if none, seek an exact universal obstruction theorem. Biased samples cannot prove universal infeasibility.
3. Add exact rational Farkas/DRAT-LRAT proof logging for any branch labelled UNSAT; audit sound symmetry coverage and aggregate completion.
4. If a complete 3-square candidate arises, replay independently every Latin row/column and all three 100 distinct pair overlays; only then claim SOLVED and stop hourly research.

## Sources
- GitHub public project STATE.json and E033/E036 reports: https://github.com/davidlueng986-alt/123321/tree/math-agent-mols10/research/mols10
- Bright, Keita, Stevens 2026: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30
- Barnoff & Bright, 2026: https://arxiv.org/abs/2605.02132
- Living journal: https://docs.google.com/document/d/1NDPWEMM3Cf5HrhdOcV6pVE9tCI-kxKbavxcfIBFva3k/edit

## Executable replay
`python E037_construct.py`, `python E037_all_pair_hall_1000.py`, `python E037_all_cycles_hall.py`, `python E037_hall_witness.py`, `python E037_verify_independent.py`, `python E037_crosscheck_all_cycles.py` (run from directory; require SciPy and E035_column_residual.py on PYTHONPATH). Exact witness and full sampling JSON included. Failed long optimization script retained, not counted as evidence. No credential material included.
