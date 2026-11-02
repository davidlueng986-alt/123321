# 3-MOLS(10) — Research log (append-only chronological entries)

## MOLS10-E000 | 2026-11-02 | Baseline and workflow startup
Question: Do 3 mutually orthogonal Latin squares of order 10 exist?
External status: OPEN based on 2026 Bright–Keita–Stevens paper, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 .
Source baseline: https://users.monash.edu.au/~iwanless/data/MOLS/neartripleMOLS10.txt .
Result: the first three Egan–Wanless arrays all satisfy Latin row/column properties. Exact unique overlay pairs: [100,100,91]. Nine repeated and nine missing B–C ordered pairs. NOT a witness.
Repro: `near_triple.json`, `verify.py --diagnostic`, and `test_verify.py`; local Python smoke tests passed prior to GitHub submission. Read GitHub Actions for independent CI execution.
Literature scope: the 2026 SAT study handles a restricted 4×4-subsquare condition and does not settle the general triple question.
Decision: H1, build an exact third-square extension SAT/exact-cover model for a fixed pair, validate on small orders and report limits. If fixed pair has no extension, do NOT infer universal nonexistence.
Next run: inspect latest CI, implement and test H1; persist any experiment and next action.


## MOLS10-E001 | 2026-11-02 | Fixed-pair extension baseline (known mathematics)
Hypothesis: a third Latin square C can be searched by four all-different constraints per cell: row-symbol, column-symbol, (A-symbol,C-symbol), (B-symbol,C-symbol).
Method: exact backtracking with minimum-remaining-value cell selection and explicit max_nodes/max_seconds guards; exhaustion is UNKNOWN, never UNSAT.
Small-order verification:
- Order 3: fixed known orthogonal pair using slopes 1 and 2 modulo 3; complete fixed-pair search returns UNSAT_FIXED_PAIR.
- Order 4: pair from GF(4) using slopes 1 and 2; search returns SAT and independent checker confirms 16/16/16 ordered pairs with third square.
- Published order-10 near-triple: witness verifier confirms 100/100/91 (not solved).
GitHub CI: https://github.com/davidlueng986-alt/123321/actions/runs/41333555421 — success after regression suite including the small-order extension tests.
Caveat: no general 3-MOLS(10) result claimed; fixed-pair UNSAT does not prove the unrestricted problem.
Next: benchmark published A,B order 10 under bounded resources, then build and benchmark a proper SAT/CP-SAT formulation, keeping exact input hashes and proof status.


## MOLS10-E002 | 2026-11-01 09:53 PST (2026-11-01 17:53 UTC) | Complete common-transversal obstruction for two fixed pairs
Status check: 3-MOLS(10) still OPEN. Primary 2026 Bright–Keita–Stevens publication: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; latest relevant 2026 arXiv work https://arxiv.org/abs/2605.02132 concerns orthogonal pairs and SAT improvements, not a complete triple. No reliable later full solution found in this run.
Source input: first three Egan–Wanless matrices from https://users.monash.edu.au/~iwanless/data/MOLS/neartripleMOLS10.txt , verified against original text.
New exact equivalence (for fixed pair X,Y): a third Latin square Z orthogonal to both is equivalent to a partition of all n² cells into n pairwise-disjoint common transversals (each meets all rows, columns, X-symbols and Y-symbols once).
Experiment: enumerated ALL 10! row-column permutations, requiring both X and Y symbol uniqueness; independently cross-checked complete results using a separate bitmask DFS, then exhaustively enumerated disjoint transversal subsets. No timeouts/heuristic UNSAT.
Pair (A,B), input SHA256 47f9bad62f68b317ff0fc8ae72278b07355ceac64a502e2af0030473d0c405c2: EXACTLY 14 common transversals, 12 cells in none, maximum disjoint packing 7. Thus this particular orthogonal pair has no third mate.
Pair (A,C), input SHA256 6db5f6f5d6e1bb0743c6a9e59eeb633ac0490f8a001975083065a4f2b2b79018: EXACTLY 7 common transversals, 36 unsupported cells, maximum disjoint packing 1. Thus this particular orthogonal pair has no third mate.
Both results independently replayed locally; GitHub CI: https://github.com/davidlueng986-alt/123321/actions/runs/41334010585 — success, including published-pair regression tests. Certificate with all 21 permutations: E002_FIXED_PAIR_CERTIFICATES.md. Code: transversals.py, test_transversals.py.
Research impact: **conditional negative results only**; these are NOT evidence that arbitrary 3-MOLS(10) cannot exist and not claimed novel. Crucially, the prior next action (bounded search on the published pair) is now superseded by a complete exact certificate, avoiding wasted SAT compute.
Next action E003: obtain genuinely different order-10 orthogonal pair instances (e.g. original author's Myrvold-MOLS repository https://github.com/curtisbright/Myrvold-MOLS and associated solutions/data), verify provenance, screen common-transversal count and coverage; prioritize pairs with >=10 transversals and full cell coverage. For high-transversal pairs (>20), use a scalable exact-cover/SAT packing backend and preserve UNKNOWN on timeouts. Do not rerun A/B or A/C except for regression.


## MOLS10-E003 | 2026-11-02 | Historical Parker pair exact certificate
Read the published Bose–Shrikhande–Parker example in P. W. M. John, p.114 (https://sites.ualberta.ca/~dwiens/stat568/misc%20resources/PWJohn.pdf). Input `parker_pair.json`: Latin pair verified 100/100; canonical pair SHA256 1fea184b868434e5ecc9d9acb27061d0429850b5bc3e257ff31158a7bd632dfe. All 10! permutations and independent bitmask DFS found ZERO common transversals; row-prefix profile [1,10,70,329,1046,1983,2233,1471,318,21,0], with every 9-row prefix blocked at row 10. Thus this fixed pair has no third mate, NOT a general solution. Scripts: parker_frontier.py, exact_cover.py and tests. Full evidence: E003_E005_REPORT.md.

## MOLS10-E004 | 2026-11-02 | 200 reproducible seeded mates
Fix published Egan A (1080 single-A transversals). Seeded exact-cover produced valid mates for all 200 seeds (0..199), yielding 91 distinct first-row-normalized B arrays. Distribution of joint A/B transversal counts among those 91: {0:37,1:28,2:6,3:13,4:3,6:3,14:1}; NONE covers every cell. The lone count-14 mate (seed 14) equals the published normalized Egan B. These are biased heuristic samples, not an exhaustive search. Code: sample_mates.py; E003_E005_REPORT.md.

## MOLS10-E005 | 2026-11-02 | All two-symbol component flips for three pairs
Egan A/B: zero nontrivial two-symbol trades. Egan A/C: three proper swaps, each with only 1 common transversal. Parker A/B: three proper swaps, each with 0. Restricted neighborhood only. Code: two_symbol_trades.py and unit tests.

## MOLS10-E006 | 2026-11-02 | Exact k-symbol re-partition neighborhoods
For selected B-symbol classes, enumerate all A-transversal repartitions of their cells. No per-support cap reached. Egan A/B: k3 0 alternatives; k4 3 supports/6 neighbors, best 4 transversals; k5 18 supports/36 neighbors, best 4 (starting pair 14). Egan A/C: k3 24/24 best1; k4 84/93 best3; k5 162/237 best3. Parker A/B: k3 22/26 best0; k4 70/98 best0. Restricted support only; no universal conclusion. Code: k_symbol_trades.py and tests. Full data: E006_E007_REPORT.md.

## MOLS10-E007 | 2026-11-02 | Parker-A budget-controlled mate sampling
Parker A has 1104 single-square transversals. Twelve seeds (0..11) under 20,000 nodes / 0.5 seconds each: 11 UNKNOWN_BUDGET, seed 8 SAT and independently verified, but its A/B pair has zero joint transversals. A separate prior 40-seed experiment timed out: UNKNOWN, not UNSAT. See E006_E007_REPORT.md.

## Research decision after E007
Status still OPEN according to the 2026 peer-reviewed Bright–Keita–Stevens restricted SAT paper (https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30). Avoid rerunning Egan A/B for <=5-symbol trades. Next E008: change first square A, create structured/coverage-guided candidate search, and invest expensive exact cover only in pairs with >=10 joint transversals AND full support. Distinguish deterministic certificate vs heuristic sample vs timeout.


## MOLS10-E008 | 2026-11-02 | Exact 9-cell combinatorial optimality of Egan fixed (A,C)
Discovery: optimize distinct (B',C) ordered pairs over ALL Latin B' orthogonal to the fixed Egan A. Egan A has 1080 transversals. For each A-transversal T, check d_C(T) <= 10 - |T intersect R| for R={(0,1),(0,2),(0,6),(0,9),(3,8),(5,0),(5,1),(6,0),(9,0)}.
The inequality was checked by all 10!=3,628,800 column permutations and an independent exact bitmask DFS yielding identical 1080 A-transversals. Minimum slack0, 30 tight. Since B' symbol classes partition the 100 cells into 10 A-transversals, sum of d_C <=100-|R|=91. Egan B attains 91. Therefore **global conditional optimum exactly 91** for fixed (A,C), arbitrary B' orthogonal to A. Validity does not depend on SciPy. Program: dual_certificates.py, test_dual_certificates.py, E008_DUAL_CERTIFICATE.json.

## MOLS10-E009 | 2026-11-02 | Parker fixed pair weighted dual bound <=77
Fix historical Parker (A,B), from parker_pair.json. An exact 22-cell deletion certificate shows every possible Latin C' orthogonal to A has at most 78 distinct B,C' pairs. Better: half-integral signed cell weights z_ij/2 in E009_PARKER_WEIGHTED77.json have sum z=45. For EVERY one of 1104 A-transversals T, independently verify sum_T z <= 2*(10 - distinct_B(T)); smallest exact integer slack0, 267 tight transversals. Hence every such C' has <=floor(100-45/2)=77 distinct B,C' ordered pairs. Valid rigorous UPPER BOUND only: 77-attaining witness not found, not proved optimal, not a result on arbitrary pairs. Program signed_dual.py + tests; entirely integer arithmetic at verification.

## MOLS10-E010 | 2026-11-02 | Exact optimality 91 for Egan fixed (A,B)
For Egan fixed A,B, found an exact denominator-2 signed dual certificate E010_EGAN_AB_WEIGHTED91.json, 100 integer numerators sum=18. All 1080 A-transversals pass sum_T z <= 2*(10-distinct_B(T)), min slack0 and 61 tight. Therefore ANY Latin C' orthogonal to fixed A satisfies U(B,C')<=floor(100-18/2)=91; the original Egan C attains 91. Together with E008, the known near-triple cannot be improved by changing just B or just C; changing A alone cannot repair the unchanged B,C overlay. **Any actual triple constructed from this instance must change at least two squares**. This is a fixed-instance conditional statement; it does not resolve 3-MOLS(10).

## MOLS10-E011 | 2026-11-02 | Diverse first Latin square candidates
Generate exact row/column connected-component flips within each symbol pair of Egan A: 48 nontrivial representative Latin variants. All are valid Latin squares. Their single-square transversal counts range from 840 to 1000, whereas original Egan A has 1080; transversal count is preserved under isotopism and parastrophy, thus all 48 are nonparatopic to original A. No variant remains orthogonal to the published B or C. A bounded trial for the first 12 variants with only 0.2 s per seed returned 12 UNKNOWN_BUDGET, not UNSAT; a larger 48x2 attempt timed out without conclusive result. Code first_square_trades.py and tests.

## Research conclusion / next step E012
These mathematically exact certificates were discovered using SciPy/HiGHS LP/MILP locally but have standalone standard-library integer-only replayers in GitHub; independent Github Actions regression is the canonical audit. Not claiming external mathematical novelty without literature comparison.
Immediate actions: prior-art check weighted transversal bounds, then replace expensive near-triple one-square-fix optimization with new A and B candidate search; use structural SAT/CP-SAT with appropriate normalizations and bounded UNKNOWN; filter for >=10 joint common transversals with full cell coverage before proof-grade full packing. Full argument and reproducibility: E008_E011_OPTIMALITY_PROOFS.md. Global 3-MOLS(10) remains OPEN.

## MOLS10-E012–E014 | 2026-11-01 18:52 UTC | new A, bounded MILP, exact local obstructions

Primary literature checked: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; https://arxiv.org/abs/2605.02132 ; https://arxiv.org/abs/2509.09633 (v3 Aug 2026). No verified unrestricted resolution located; global status OPEN.

E012: SciPy/HiGHS binary 100-cell exact cover on changed first squares (E011). Trade indices 12 and 20 both produced explicit independently validated Latin+orthogonal pairs, 904 A-transversals each. Both have **zero common transversals** by independent full 10! enumeration; therefore neither fixed pair extends. Trade indices 30/40/47 each UNKNOWN at 6-second MILP limit. Third-square attempt for trade12 UNKNOWN at 12s; trade20 gave a verified but suboptimal **100/100/69** near-triple at 12s (solver gap ~0.10145). See E012_WITNESSES.json and E012_milp_traded_A.py.

E013: Tested necessary one-transversal compatibility support for original Egan A + all 48 first-A trades. **0 of 49 A** yielded any excluded A-transversal; 7.1s bounded exact scan. This filter is empirically vacuous here; preserve as negative evidence, do not repeat unchanged. E013_compatibility_screen.py.

E014: For each fixed orthogonal pair A,B, searched smallest B-symbol subset S such that a cell x is absent from all A-transversals using each B-symbol in S at most once. Exact minimal sizes: Egan A/B **6**, Egan A/C **5**, Parker A/B **3**, traded A/B index12 **5**, index20 **5**. Parker's three-symbol witness is S={7,8,9}, x=(7,7) zero-based. All smaller S subsets exhaustively tested; all five blocking witnesses independently replayed by 3,628,800 permutations each, 0 eligible A-transversals through blocked cells. E014_symbol_obstruction.py, test_E012_E014.py, CI https://github.com/davidlueng986-alt/123321/actions/runs/41338759633 (success).

Full exact numbers, proof scope, failures, code, sources, uncertainty and next experiment: E012_E014_REPORT.md. **Next E015:** use multi-B-symbol collision-mask coverage as a sound pruning oracle in partial B exact-cover construction; positive control GF(4), then bounded changed-A search targeting >=10 joint transversals with full support. These results are conditional on explicit pairs; unrestricted 3-MOLS(10) remains OPEN.

## MOLS10-E015 | 2026-11-01 18:55 UTC | sound partial-B-class exact-once pruning

Mathematical lemma: if a partial orthogonal mate B has selected A-transversal symbol classes T_1,...,T_k, every hypothetical C-symbol class U must meet each T_i in exactly one cell. Maintain the bitset intersection of Compat(T_i) over all A-transversals U. If no such U covers some cell, reject the B prefix soundly. This is necessary only; passing the filter is not a solution.

Exact exhaustive minimal B-class blockers (stronger than E014 at-most-once criterion): Egan A/B k=3 (18/120 blocking subsets), Egan A/C k=3 (18/120), Parker A/B k=2 (3/45), traded pair12 k=3 (73/120), traded pair20 k=2 (2/45). Five blocked-cell witnesses independently verified by 10! permutations each. GF(4) known positive triple passes every partial-prefix filter (k=0..4). Code E015_partial_mate_prune.py; test_E015_partial_mate_prune.py.

Bounded search, seed0, four seconds per new A: trade12 UNKNOWN after 4194 nodes (3193 pruned); trade20 UNKNOWN after 4313 (3327 pruned); trade30 UNKNOWN after 4672 (3650 pruned). No full-support pair found. No UNSAT or 3-MOLS claim. Details E015_REPORT.md; CI https://github.com/davidlueng986-alt/123321/actions/runs/41339094814.

Next E016: optimize candidate-list lookup and branching, benchmark pruning versus unpruned on matched seeds, then broader bounded scan for changed-A orthogonal pairs with complete common-transversal coverage. Global problem OPEN.

## E028 — 2026-11-02 08:09 UTC — SX/UU complete fixed-Q audit
**Objective:** Finish E027's outstanding two published Appendix Q, SX and UU, by exhaustive Q-orthogonal mate enumeration; stronger than E023 fixed-pair exclusion. **Global status OPEN.**

**Sources:** Bright–Keita–Stevens, EJC 2026-02-13 https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; arXiv https://arxiv.org/abs/2503.10504 ; relevant later pair work https://arxiv.org/abs/2605.02132 . Fresh 2026-11-02 search: no independently verified unrestricted result; search absence not proof.

**Method/evidence:** Q-transversals form exact-cover rows. Bitset DFS + independent mutable Algorithm X enumerate all partitions into 10 transversals, canonical mate symbols fixed by row 0. SX: 864 transversals, 2 complete partitions, bitset 57,110 nodes, independent 34,710 nodes. UU: 816 transversals, 1 partition, bitset 40,048 nodes, independent 24,753 nodes. One new normalized SX orthogonal mate; UU unique mate up to relabeling. All 3 mates Latin and 100/100 with Q. Full independent 10! permutation replay for each mate (10,886,400 permutations) finds **0 common transversals** for each. Both exact-cover algorithms produce identical full mate sets. Published normalized mate recovered once per Q. This excludes these two **specific** Q, and together with E027 all eight **specific** published Appendix Q. Not entire families or unrestricted nonexistence.

**Reproduce:** `python E028_SX_UU_fixed_Q.py > E028_full.json` from research/mols10. Source `E023_SX_pair_replay.py`, `E023_UU_pair_replay.py`; reusable E027 backends. Code commit https://github.com/davidlueng986-alt/123321/commit/8dc4ad2c0ce1f2224aaabd2646dd50c68749ee37 ; compact data commit https://github.com/davidlueng986-alt/123321/commit/5cc86c90307233ebe3f6c357120a61f4d53909f7 ; report commit https://github.com/davidlueng986-alt/123321/commit/40084b2c422ec5c6419942831782b64ea72b81f9 ; state commit https://github.com/davidlueng986-alt/123321/commit/4fdf434c0e843ed2bee5baa6a6651c691f64da7a .

**Failures/uncertainty:** local git DNS failed; first optional source-audit patch had quoting SyntaxError, corrected and full replay rerun; no false UNSAT inferred. No unrestricted symmetry coverage, SAT certificate, or triple. E028 CI not confirmed.

**E029 next:** stop fixed-Q repeats; obtain genuinely different nonisotopic Q via authors' SAT encoding, validate full pair and common-transversal coverage, then third-square exact cover if viable.

## E029 — 2026-11-02 ~09:04 UTC — Complete fixed Egan B/C Q-mate audit
- **Status:** OPEN; no unrestricted 100/100/100 witness or exhaustive nonexistence proof. Literature: BKS EJC 2026-02-13 https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; arXiv 2503.10504v2 https://arxiv.org/abs/2503.10504 ; Barnoff–Bright https://arxiv.org/abs/2605.02132 . Fresh targeted searches found no independently checkable unrestricted solution.
- **Nonduplicate objective:** E002 excluded only the two specific (A,B)/(A,C) pairs. E029 fixes Egan B and separately C, then exhaustively enumerates ALL orthogonal mates of each, modulo mate-symbol relabeling. Input `near_triple.json`.
- **Exact results:** B: 932 transversals, 5 mates, bitset 108830 nodes, independent Algorithm X 64582 nodes, common counts [0,14,2,0,0], support [0,88,19,0,0]. C: 864 transversals, 4 mates, bitset 59173 nodes, independent 36254 nodes, common counts [0,0,7,0], support [0,0,64,0].
- **Independent audit:** two exact-cover engines produce identical complete sets of nine canonical mate matrices; all nine Latin+100/100. Independent compiled C++ enumerated all 10! permutations for each (32,659,200 total), confirming all counts/support. Original Egan A recovered exactly once per Q. No UNKNOWN in complete runs.
- **Failed experiment:** initial C++ checker generation failed `ModuleNotFoundError` (missing /mnt/data on sys.path); discarded, fixed and reran all nine successfully. No GPU. No isotopy classification, SAT proof certificate, or unrestricted symmetry coverage. Restricted result excludes only these exact two Q, not the full open problem.
- **Code:** https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/E029_Egan_BC_fixed_Q.py ; commit https://github.com/davidlueng986-alt/123321/commit/6e57beccd1fe266e9e9b391cb86faa974776a38c .
- **Results:** https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/E029_RESULTS_SUMMARY.json ; commit https://github.com/davidlueng986-alt/123321/commit/107d7853c9712d6917fe15e963877f1b3741fe8c .
- **Report:** https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/E029_REPORT.md ; commit https://github.com/davidlueng986-alt/123321/commit/2f4ac31bf762523068f02e99bf5cff2e8f2d352a .
- **STATE:** https://github.com/davidlueng986-alt/123321/commit/d127a7b1cf28a4074ac9f432cd6a1cfcd65c23d2 .
- **Next E030:** generate genuinely new nonisotopic fixed Q using published SAT encoding and justified symmetry blocking; avoid all ten previously audited fixed Q. Check Latin+100/100, common transversals and support; exact-cover third square only if warranted.


## E036 — 2026-11-02 12:46–12:52 UTC (OPEN)
Primary status: Bright–Keita–Stevens EJC 2026-02-13 https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; Barnoff–Bright arXiv:2605.02132v2 (2026-07-04) https://arxiv.org/abs/2605.02132 ; no independently verifiable unrestricted solution in targeted current search.
Objective: test whether all 156 centralizer g-orbits for canonical f=(01)(23)(45)(67)(89) can be extended to six-row partial triples; avoid repeating E035 biased local-prefix exclusions.
Actual: 156/156 constructed and independently checked Latin six-row prefixes; all three pair overlays 60/60/60. Independent JS centralizer orbit union exactly 440192 legal g. Generated canonical witness SHA256 5b198704a6cd24cae9ba57b7f938ce121aba182df1fc78738d39ab92a2aff66f. Maximum per-row DFS nodes 12846. This is a restricted finite constructive theorem, NOT 3-MOLS(10).
Bounded failures: 3093 seeded row6 SAT choices from 156 fixed five-row prefixes; 3091 row7 exhaustive UNSAT for the fixed six-row prefixes, two row7 SAT (indices 39,47; 70/70/70). Both seven-row prefixes have exact eighth-row zero-support obstructions (133 and 156 mandatory constraints with no candidate); independently replayed. 10-restart-per-g exploratory batch all 156 reached six rows, zero reached seven. 50-restart exploratory batch interrupted without final output; NOT certified. No whole-orbit UNSAT and no global certificate.
Reproduce: python E036_reproduce.py; node E036_verify.js; python E036_lookahead_reproduce.py; node E036_verify_k7.js (from research/mols10). Generator commit https://github.com/davidlueng986-alt/123321/commit/d5c4c4ec0c8ee3c390ced97e480702574dabc9b4 ; independent JS commit https://github.com/davidlueng986-alt/123321/commit/94cd88b4628aa129697c309c5105f6aef74f8769 ; lookahead commit https://github.com/davidlueng986-alt/123321/commit/dba75521371ce23d8d3f0029972252464b545934 ; k7 verifier commit https://github.com/davidlueng986-alt/123321/commit/db1679b0f6c69df7344b7dc21af77efa393500dc ; report commit https://github.com/davidlueng986-alt/123321/commit/178e85a2622d2bb37ad273d694cb24fcdd743a8a ; STATE commit https://github.com/davidlueng986-alt/123321/commit/720d8dfce5902dc0b6db243516d978479ca0c7ea .
Next: sound column-aware Hall/LP/exact-cover lookahead before choosing row6/7; maintain unrestricted 12-type/162959-orbit proof-producing search. Uncertainty: restricted theorem only; 100/100/100 still OPEN.


## E042 — 2026-11-02 17:44–17:54 UTC
OPEN. Tested three existing E040/E041 exact 21/22-cell forbidden patterns under row/column/symbol isotopies and square permutations against 516 previously LP-infeasible k4 prefixes. 1,548 exact checks; only 3 positive embeddings (each original source), 1,545 negatives, 0 UNKNOWN, **0 marginal new cuts**. Independent separate Python replay completed all checks in five bounded batches (2,447,321 DFS nodes). Failed monolithic run excluded; three numerical LP primal rationalization attempts failed exact verification. No global orbit excluded (0/162,959). Source input hashes, full scope, links, reproducible commands, caveats and next action: [E042_REPORT.md](E042_REPORT.md); [E042_RESULTS.json](E042_RESULTS.json); [E042_replay.py](E042_replay.py). Google Drive journal updated separately.

## E043 | 2026-11-02 18:54 UTC | OPEN | 2,184 exact fixed-prefix obstructions

- **Primary review:** Bright–Keita–Stevens EJC 33(1) P1.30 (2026-02-13), https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; Barnoff–Bright arXiv:2605.02132v2 (2026-07-04), https://arxiv.org/abs/2605.02132 . Fresh targeted 2026-11-02 search found no independently checkable unrestricted resolution.
- **Objective:** E039 already certified 156 initial four-row prefixes from E036's 156 six-row partial triple witnesses. Test the 14 other four-row subsets of each, avoiding E039 duplicates and E042's costly unproductive isotopy-motif matching.
- **Input / code:** E036_WITNESSES.json, SHA256 4b1a2abb7e2ddade1c898ae23a50b086af0dd3545265a92c37dddd326b0f9462. New generator E043_reproduce.py, integer-only independent verifier E043_verify_reproduced.js, report E043_REPORT.md.
- **Exact result:** 156 × 14 = 2,184 pairwise distinct ordered fixed k4 prefixes; 184 exact zero-support demands and 2,000 exact integer Farkas duals, all for six-resource residual exact cover. Numerical scan 8.67 s, no LP-feasible or UNKNOWN, but statuses upgraded to exact witnesses. Independent Node.js replay 2,184/2,184 PASS; checked 870,931 allowed placements, min positive RHS +1, maximum candidate dual score -6. Mutation test rejected corrupted weights. Affine F5/F7/F11 positive controls 370/370 PASS.
- **Failed/incomplete:** Unbatched dual run interrupted after ~600; excluded from counts. Eight bounded shards covered all 2,184. No LP-feasible counterexample found in this *biased* sample. Complete ZIP SHA256 f24a39e547d62d7ec55b054a9c61127d6742835d23918d05d86485e15d8a4538 exists as local conversation attachment; Google Drive binary upload FAILED BLOCKED_FILE_REFERENCE, so no Drive ZIP claimed. Public GitHub includes report and generator/verifier but not full 2,184-case certificate data.
- **Critical scope:** All 2,184 are conditional fixed-prefix exclusions. With E039 initial subsets, 2,340 tested prefixes from these 156 six-row witnesses are obstructed. This does NOT exclude even one complete symmetry orbit: 0/162,959. No 100/100/100 triple or unrestricted nonexistence proof.
- **Next:** Search structurally different k4 prefixes passing full six-class LP; pursue proof-producing SAT with verified full symmetry coverage. Avoid repeating E036-derived biased sampling.


## E044 — 2026-11-02 19:49–19:53 UTC — OPEN

- **Literature:** Bright–Keita–Stevens, EJC 33(1) P1.30 (2026-02-13), https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; Barnoff–Bright arXiv:2605.02132v2 (2026-07-04), https://arxiv.org/abs/2605.02132 . No independently verified unrestricted solution found in targeted search.
- **Objective:** Break E036/E043 sample-source bias: generate 512 new valid four-row partial triples using independent randomized derangements and bounded MRV row search (seed 20261102), spanning 11 of 12 first-square second-row cycle types. Raw ordered-prefix overlap with 2340 E036-derived samples = 0 (not a claim of isotopy inequivalence).
- **Exact evidence:** 471 integer Farkas dual certificates plus 41 exact zero-support; independent Node.js verifier checks all 512 valid 40/40/40 prefixes and 200094 residual placements; 512/512 PASS, mutation rejected. k3 parents 512/512 NUMERICALLY LP-feasible (max residual 9.71e-13), not exact primal certificates.
- **Failures/limits:** E041 deleted-cell integer pilot 8 cases × 4 s each timed out, UNKNOWN. No k4 LP-feasible prefix found among 512 nonuniform random samples. 0/162959 global symmetry orbits excluded; no full triple.
- **Reproduce:** E044_disjoint_probe.py, E044_certify.py, E044_verify.js, E044_k3_controls.py; see E044_REPORT.md. Complete data+512 certificates are in local E044 ZIP SHA256 06be58a9171686fe617bf09a7c0161969eaf517ebfc3ca2e0d1851bc45e11997, not claimed persisted in GitHub/Drive.
- **Next:** Target a k4 six-class LP-feasible counterexample with constraint-guided generation, or symmetry-complete proof-producing SAT with independently checked certificates.


**E044 CI addendum | 2026-11-02 19:59 UTC:** First remote CI attempt failed because repository E035_column_residual.py was empty (not a mathematical failure); model restored in commit 22296cab5d426beaa0e9c40fa90f426318409442. Rerun https://github.com/davidlueng986-alt/123321/actions/runs/41514534121 PASSED 512/512 exact integer replay, 200094 candidates, 471 dual +41 zero-support and mutation rejection. GitHub Actions persisted complete regenerated JSON and logs in commit https://github.com/davidlueng986-alt/123321/commit/42dbc1ae9fd2a928c6f525d247dc820432b2d627 . This supersedes prior local-only data caveat. Local vs remote SHA256 differ due run times / solver versions; both verified exactly. Google Drive binary ZIP upload FAILED BLOCKED_FILE_REFERENCE, text journal updated. Global problem OPEN, zero complete orbit exclusions.
