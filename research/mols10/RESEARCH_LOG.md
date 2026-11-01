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
