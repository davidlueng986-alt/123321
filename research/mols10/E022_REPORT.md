# MOLS10 E022 — Egan pair-root C exact-cover obstruction

**Run:** 2026-11-02 01:45–01:50 UTC. **GLOBAL PROBLEM STATUS: OPEN.**
Scope: fixed published Egan–Wanless first Latin square A only. No unrestricted 3-MOLS(10) witness or proof.

## Primary literature and external-status check
- Bright–Keita–Stevens, *Electronic Journal of Combinatorics* 33(1), P1.30, published **2026-02-13**, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; reports the unrestricted triple problem open, studies a 4×4-subsquare restricted family.
- Barnoff–Bright, arXiv:2605.02132v2, **2026-07-04**, https://arxiv.org/abs/2605.02132 ; improvements concern orthogonal pairs, not a triple.
- Bright–Keita–Stevens, arXiv:2509.09633, https://arxiv.org/abs/2509.09633 ; SAT enumeration concerns orthogonal pairs with two relations, not a triple.
- Fresh targeted 2026-11-02 search found no independently checkable unrestricted solution since E021. Search absence is **not** a mathematical proof of openness.

## New necessary condition and proof
Let A be fixed. Every symbol class of a potential B is an A-transversal (10 cells, exactly one per row, column, and A-symbol). Let U,V be any two **disjoint** B-symbol classes. Every C-symbol class W is also an A-transversal, and B⊥C implies
`|W∩U|=|W∩V|=1`.
The ten C-symbol classes must exactly partition the 100 cells. Therefore, if the exact-cover problem over A-transversals W satisfying both intersection equations is infeasible, U and V cannot coexist in a triple. This is a necessary condition, not a global theorem.

If every B-class must come from a unary-surviving set S, then each such class must have at least one pairwise-disjoint partner V∈S for which the pair-root C exact cover is SAT. Otherwise that class cannot be in B. If the union of all pair-SAT-supported B roots fails to cover all 100 cells, B cannot exist. This implication does **not** assume uniqueness of C or infer UNSAT from timeouts.

## Computation
Input: published Egan first A, compact JSON SHA256
`965a201951eb261b3ec9c8575163e8d7a6f70e384fd90699a77bc59a1b0ebc33`.
- 1080 A-transversals independently enumerated.
- Unary exact-cover screening: 114 SAT, 966 exhaustive UNSAT, 0 UNKNOWN.
- Among 114 unary survivors: **1647 disjoint pairs**.
- Pair-root C exact cover: **45 SAT / 1602 exhaustive UNSAT / 0 UNKNOWN**. DFS 38,318 nodes total, max 78 nodes per pair, cap 20,000; local CPU ~9.88s including unary preprocessing.
- **All 1647 pairs pass the weaker cell-support screen**: their allowed C-transversals collectively cover all 100 cells. Thus E015-style support alone rejects none; pair-root exact-cover feasibility adds genuinely stronger information.
- The 45 pair-SAT cases involve only 14 B-root indices:
  `[69,88,94,106,124,125,168,197,632,696,832,873,979,1018]`.
- Their union misses **12 cells**, flattened zero-based:
  `[1,2,3,18,29,37,44,55,66,70,80,90]`.
- Explicit SAT pair roots (69,632) have a valid C exact cover with A-transversal indices
  `[826,380,714,920,0,309,446,616,993,1029]`.
- Example exhaustive UNSAT pair roots (30,714). The 45 returned SAT witnesses all use the same C partition up to ordering; **this does not prove uniqueness of C**.

**Conditional conclusion:** The specific Egan published A cannot belong to a 3-MOLS(10) triple. This was already excluded by the E016 full fixed-A DFS; E022 supplies a shorter, independently cross-checked obstruction. It does **not** exclude arbitrary order-10 Latin squares.

## Independent replay and controls
- A separate recursive transversal enumerator plus SciPy/HiGHS binary exact-cover MILP independently checked **all 1647 pair-root instances**: exactly 45 feasible, 1602 solver-complete infeasible, 0 unknown; all results agree with stdlib DFS. Local MILP batch ~12.18s.
- Independently replayed all 45 SAT witness partitions, verifying every cell covered exactly once and each C class meets both roots once.
- GF(4) positive control: three actual order-four MOLS, overlays 16/16/16; all 6 disjoint B-symbol-class pairs C-completable.
- Local `python -m unittest -v test_E022_pair_exact_cover`: 4 tests PASS, including explicit SAT, UNSAT, UNKNOWN-budget classification.
- No GPU used. No DRAT/FRAT proof certificates. HiGHS infeasibility is solver-complete **for each fixed instance** but is not a formal independently verified UNSAT proof file.

## Reproduce / exact sources
1. `cd research/mols10 && python E022_replay.py --cap 20000 --out E022_REPLAY.json`
2. `python E022_independent_milp.py --input E022_REPLAY.json --all --output E022_MILP_REPLAY.json` (requires numpy/scipy)
3. `python -m unittest -v test_E022_pair_exact_cover`
4. `python E022_positive_control.py`

Files: [stdlib replay](E022_replay.py), [independent MILP](E022_independent_milp.py), [summary data](E022_RESULTS.json), [unit tests](test_E022_pair_exact_cover.py), [positive control](E022_positive_control.py).
The generated full replay JSON lists every pair and SAT witness; it can be regenerated from the above code. The GitHub summary records aggregate results and a representative witness.

## Failures, uncertainty, next step
- First 100-pair bounded pilot found 100 UNSAT, but **no extrapolation** was made until all 1647 were checked.
- Pair-root cell support was **vacuous** on all 1647 pairs, showing why exact-cover reasoning matters.
- Both Egan and Parker fixed-A exclusions are conditional. There is no unrestricted symmetry coverage or 100/100/100 triple. Novelty relative to the existing literature is not established.
- **E023:** stop expanding only Egan/Parker local neighborhoods; retrieve the eight published Myrvold residual pair-pattern cases from primary-source supplementary material, validate their full arrays, and test third-square exact-cover extension on source-verified pairs. In parallel consider certificate-producing SAT for the compact pair-root fixed-A exclusion, rather than repeating the same DFS. Preserve UNKNOWN separately.

Keep the existing MOLS10 automation enabled; no verified global resolution.
