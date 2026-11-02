# E032 — Residual triangle-hypergraph hierarchy and certified integrality gaps

**2026-11-02 ~10:25–10:42 UTC. Global 3-MOLS(10) status OPEN.**

## Context, primary sources and limits
Read the living Math Agent Google Drive journal, GitHub `STATE.json` (last E031), and E031 direct search, LP dual, independent replay and CNF code. Latest targeted literature check found no checkable unrestricted solution: Bright–Keita–Stevens (2026), https://arxiv.org/abs/2503.10504 ; Barnoff–Bright (2026), https://arxiv.org/abs/2605.02132 ; Keita (2026) thesis https://cs.uwaterloo.ca/~cbright/group/amadou_thesis.pdf . No paper/source search proves absence of unpublished work.

### Objectives
1. Audit whether E031's 12 exact five-row LP duals add actual pruning versus cheaper sound unit propagation.
2. Locate a genuinely distinct obstruction at earlier row depths. Test **fractional LP vs integral residual hypergraph exact cover** with independently checkable exact rational *positive* witnesses and exhaustive independent *negative* replays.
3. Implement bounded joint direct-search A/B, positive small-order and independently scripted controls, preserving all failures and sampling limitations.

## Exact mathematical reduction
After k complete valid partial rows, form uncovered pair-edge classes `E_AB,E_AC,E_BC`, each of size `n(n-k)`. Every future cell `(a,b,c)` corresponds to one allowed triangle covering three edges. Any genuine triple completion yields a **0/1 perfect exact cover** of this hypergraph. Necessary filters of increasing strength:

- Support: every residual pair-edge lies in an allowed triangle.
- Unit propagation: if any uncovered edge lies in exactly one *currently compatible* triangle, force it, and delete competing triangles. A missing alternative/overlap proves no completion. This is an EXACT, sound integer exact-cover inference, not LP.
- Fractional exact-cover LP: `Mx=1,x>=0`. Complete LP infeasibility excludes the prefix; rational Farkas dual is independently checkable.
- Integer exact cover: `Mx=1,x in {0,1}`. Independent complete Algorithm X exclusion can distinguish true integer obstructions from LP. An integral SAT residual solution remains only NECESSARY: row/column Latin constraints are not part of this residual model.

## Results A — large reproducible biased-sample sweep
All prefixes were *complete-row* partial Latin triples, with all three partial overlays injective, verified independently. Samples are DISTINCT labeled prefixes, but selected by DFS and **NOT random or exhaustive representatives**. Repeated/symmetric structures may occur. No proportions generalize to the whole search space.

| Sample | k | Seed | Support-passing prefixes | Unit UNSAT | Fractional LP UNSAT | LP SAT |
|---|---:|---:|---:|---:|---:|---:|
| K4_SUPPORT | 4 | 0 | 160 | 0 | 160 | 0 |
| K4_SEED71 | 4 | 71 | 250 | 0 | 0 | 250 |
| K4_SEED131 | 4 | 131 | 250 | 0 | 56 | 194 |
| K5_SUPPORT | 5 | 0 | 120 | 120 | — | — |
| K5_SEED19 | 5 | 19 | 1500 | 1500 | — | — |
| K5_SEED71 | 5 | 71 | 400 | 400 | — | — |
| K5_SEED131 | 5 | 131 | 400 | 400 | — | — |
| K3_SEED71 | 3 | 71 | 200 | 0 | 0 | 200 |

**E031 audit finding:** All **12 original E031 five-row LP-dual examples themselves** were retrieved from the local E031 artifact, and ALL 12 were independently found to be UNIT_UNSAT by both Python and standalone Node.js (forced counts [13,2,2,13,15,2,16,5,23,5,1,1]). Their rational LP certificates remain valid, but add NO marginal pruning over sound unit propagation for these 12 exact instances. This is not a proof that every order-10 five-row prefix is unit-UNSAT. Very different k4 seed outcomes disprove any naïve uniform-failure inference.

## Results B — genuine LP integrality gap
All **660** k4 prefixes independently classified by integer triangle exact-cover MILP:
- seed 0: 160 MILP UNSAT (all LP UNSAT).
- seed 71: 250 MILP SAT (all LP SAT).
- seed 131: 71 MILP UNSAT and 179 SAT; of the 71 UNSAT, 56 are LP UNSAT and **15 are LP FEASIBLE**.

The 15 LP-feasible/integer-infeasible k4 instances have indices `[34,36,54,55,57,58,59,60,65,66,76,80,148,155,156]` in the *seed131* list. For EACH:
1. SciPy/HiGHS produced a positive fractional LP solution; `E032_fractional_witness.py` rationalized all nonzero values and then verified **every** exact edge equation with Python `Fraction`, including denominators up to 15 (or 12).
2. An independent pure-Python Algorithm X exhaustively returned UNSAT in **165–395** nodes without timeout.
3. An independent pure-Node.js verifier recreated allowed triangles from the stored raw prefixes, verified every rational fractional equality with **integer arithmetic**, and independently exhausted the integral exact-cover DFS in **247–555** nodes without timeout. Result 15/15 pass.

Therefore these 15 states establish concrete integer-versus-fractional integrality gaps for the **restricted residual triangle-cover problem**. These are not new unrestricted 3-MOLS(10) results, not a global 5-net nonexistence proof, and novelty against all prior literature has not been established.

Separately, 16 k4 LP-infeasible prefixes yielded **exact rational Farkas certificates** (positive sums `3` to `5`, also `10/3`, `7/2`); standalone Node.js integer checker verified all 16 from raw prefixes, with all allowed triangles checked. These LP certificates do add information beyond support/unit at k4.

## Results B2 — deletion-minimal 87-edge integral UNSAT core (new structural target)
For k4 seed131 case index34, the full residual triangle system has **180 exact-cover edge equations**. By repeated solver-complete MILP checks, a deterministic seed71 deletion pass removed 93 equations, leaving **87**. The restricted 87-equation system remains integer UNSAT while the original system has a verified exact fractional solution (hence so does the restriction).

**Independent pure Node.js verification (separate from the MILP minimizer):** Reconstructed all allowable `(a,b,c)` triangles from the raw prefix; exhaustive DFS verifies the 87-edge restricted system **COMPLETE_UNSAT in 4,514 nodes**. Removing **each of the 87 edges individually** produces SAT; all 87 one-edge deletion tests independently replayed in 152,659 DFS nodes total (maximum 4,988 nodes per SAT instance). Therefore this is rigorously a **deletion-minimal integer UNSAT subsystem**, not just a random 87-edge subset. It is *not* a globally smallest UNSAT core; exhaustive search over all subsystems has not been done. The complete row/column problem is not proven UNSAT unrestricted.

Code: `E032_minimal_core_fast.py`, `E032_verify_core.js`, `E032_verify_core_irreducible.js`; data: `E032_MINIMAL_INTEGRAL_CORES.json`. Initial attempt to run three instances/two seeds exceeded outer execution timeout after several partial successes; no result from the incomplete batch was accepted. The bounded one-instance version completed and was independently checked.

Potential next mathematical target: find a concise parity or cut obstruction supported on this 87-edge core, then test whether the same minimal forbidden pattern appears in other k4 prefixes under *proven* symmetries. This could yield a genuinely reusable lemma instead of accumulating local exclusions.

## Results B3 — GF(2) obstruction conjecture falsified on these instances
A direct GF(2) Gaussian-elimination audit of residual exact-cover equations `Mx=1 (mod 2)` found **GF2_FEASIBLE for all 15 integrality-gap systems** (rank 151 of 180 equations) and for the deletion-minimal 87-edge core (rank 87 of 87 equations). Therefore no inconsistency of the *linear XOR equations alone* explains these particular integer obstructions. This rules out a simple GF(2)-linear explanation for the selected core, **not** more sophisticated parity arguments that rely on integrality, inequalities or nonlinear constraints. Code/result: `E032_GF2_audit.py` / `E032_GF2_AUDIT.json`.

## Results C — bounded solver comparisons (no global conclusion)
`E032_search_benchmark.py` tests full triple direct row search, preserving first-row normalized three squares, A first-column normalization, B/C swap ordering, and supports `none/support/unit/lp`. All filters are logical necessary conditions. For order 10 with **100,001** DFS nodes, seed 0/71/131 respectively:
- No-pruning: `UNKNOWN_BUDGET` all three.
- Support: `UNKNOWN_BUDGET` all three; support prunes `1591/1742/1407` prefixes.
- Unit: `UNKNOWN_BUDGET` all three; unit prunes `5942/8142/5370` prefixes, mostly at k5.
- LP lazy (12,001 nodes, seed0/71): `UNKNOWN_BUDGET`; seed0 prunes 615 at k4, seed71 1138 at k5. Different budgets and branch orders prohibit score claims.

Small controls: full joint solver order4 SAT and order5 SAT, independently validating full Latin + all three pair overlays. Orders2/3 are exhaustive normalized UNSAT. Order6 and 10 remain UNKNOWN. Separate actual finite-field triples for n5/n7/n11 retain fractional LP SAT and unit-survival from prefixes k1 through k5, guarding against unsound trivial rejection.

## Research hypotheses prioritized by *falsifiable value*
1. **H32A — adaptive depth-dependent pruning.** At k4 use LP (and sparingly integer cover) to eliminate cases missed by unit, at k5 use cheap unit propagation. Compare under equal walltime, not raw node counts. E032's seed dependence means adaptability is important.
2. **H32B — small integral UNSAT cores.** The 15 integrality gaps can be exhausted in ~165–395 Python nodes. Extract minimal subhypergraphs/integer nogoods, and prove sound lifting under permitted 5-net symbol/coordinate symmetries. Potential to yield *reusable mathematical obstructions*.
3. **H32C — proof-producing hypergraph solver.** Record an independently replayable *branching proof trace* for integral UNSAT, not only two independent algorithm replays. For global nonexistence every complete branch and symmetry orbit would need coverage.
4. **H32D — certificate sparsification.** Minimize support of rational Farkas duals (16 k4 examples), and test whether small templates generalize across prefixes via isomorphism-safe graph canonization.
5. **H32E — row/column-aware residual cuts.** Pair edges alone ignore Latin column constraints; augment triangles with future-row/column flow or extend exact cover with assignment geography, careful not to introduce unsound constraints.
6. **H32F — stronger CNF propagation.** Encode residual exact-cover/triple implication as native SAT clauses/short conflicts, compare with E031 33k-variable full direct CNF. Use proof-producing modern SAT backend; existing CNF was only *generated*, never solved.
7. **H32G — symmetry orbit quotient of partial 5-nets.** Current prefix counts are labeled and heavily seed biased; canonicalize entire 5-net incidence structure (row/col/square/symbol permutations) before estimating structural diversity.
8. **H32H — diversification before inference.** Seed0/71/131 k4 LP infeasibility 160/0/56 among 160/250/250 prefixes; any claim that 'all k4 fail' is refuted by these samples.
9. **H32I — branch-level incremental state.** Update residual hypergraph triangle incidence on every completed row using reversible trails, instead of rebuilding; benchmark cost and proof replay.
10. **H32J — cut quality objective.** Prefer a cut that excludes many *inequivalent* partial states per ms, not only a large raw prune count.
11. **H32K — integrality-gap families.** Classify the 15 witness hypergraphs by incidence spectra and graph automorphism; inspect whether a common parity/core obstruction explains them.
12. **H32L — early symbol/column matching bounds.** Cheap Hall checks at incomplete rows were slower in E031; investigate incremental matching maintenance only after narrowing domains.

## Failure / audit ledger
- Initial sample of 90 k5 prefixes was **not support-filtered**; all had unsupported pairs, so it was discarded for claims about incremental value. Reran 120+1500+400+400 prefixes that **passed support**, then confirmed unit UNSAT independently in JS.
- Initial Python-written file failed due to directory permissions; corrected and all experiments reran.
- One greedily minimized 3-instance/2-seed core sweep timed out after partial output; the completed single-case subset was rerun independently and verified.
- GitHub and Google Drive connector write attempts were blocked by platform safety checks, so this turn does NOT claim remote commits or Drive updates. Local sync notes and full bundle are preserved.
- Early conjecture 'LP may eliminate essentially all k4 states' was falsified by seeds 71 and 131. **Do not generalize** from seed0.
- Row solver order10 remains `UNKNOWN_BUDGET` regardless of pruning; no full order-10 witness, exhaustive certificate or global classification.
- LP feasibility alone does not imply integral residual completion; 15 independently replayed counterexamples.
- Numeric SciPy solver results are not accepted as exact proofs absent rational replay or independent integer-exact-cover enumeration.

## Reproduce (CPU-only)
```bash
cd research/mols10
python E032_sample_prefixes.py --n 10 --k 4 --goal 250 --budget 1000000 --seed 131 --filter support --output E032_K4_SEED131.json
python E032_integral_gap.py E032_K4_SEED131.json
python E032_independent_exact_cover.py
python E032_fractional_witness.py
node E032_verify_integrality_gap.js E032_INTEGRAL_GAP_CERTIFICATES.json
node E032_verify_certificates.js E032_EXACT_DUALS.json E032_SUPPORT_PREFIXES.json E032_K5_SEED19.json
```
Inputs/result hashes and additional modes in `E032_MANIFEST.json`. Commands for exact-cover scripts require the saved index list and seed-131 prefix file. No GPU required.

## Next concrete E033
1. Derive exact minimal integral UNSAT cores on the 15 certificate instances; independently verify proof traces, canonicalize under safe permutations.
2. Implement incremental reversible unit+LP+integral cuts in the direct row solver; benchmark across equal **walltime** and diverse seeds at n4,n5,n10 with independently validated full witnesses.
3. Run a genuine modern CDCL backend on E031 direct OA CNF if available, with proof logging for unrestricted claims; until then report UNKNOWN.
4. Maintain status OPEN and hourly automation enabled.
