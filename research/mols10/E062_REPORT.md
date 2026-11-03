# E062 — Closure attempt: 2,781 public pairs scanned; exact fixed-7-packing rigidity

**2026-11-03 UTC. Mathematical status: OPEN.** The **sole goal** is an unrestricted 100/100/100 order-10 triple or a complete, independently verified global nonexistence proof. No such object was produced in E062. MOLS10's hourly automation remains disabled at the user's request.

## 1. Fully completed systematic external-data construction test

Public source: Ian M. Wanless, [MOLS data](https://users.monash.edu.au/~iwanless/data/MOLS/MOLS10.txt) and [format specification](https://users.monash.edu.au/~iwanless/data/LSformat.html) (citing Egan and Wanless, *Mathematics of Computation* 85 (2016)). The public header `10 10 5562` means 5,562 separate 10×10 Latin squares, interpreted by the author as consecutive orthogonal **pairs**; 2,781 pairs were evaluated. Dataset SHA-256 `efc22cbdb1ffe0ea6173011a738fa6893304e787263913c218e0cb480144428d`.

GitHub Actions executed `E062_scan_wanless_pairs.py`, posted the complete machine-readable output `E062_WANLESS_PAIR_SCAN.json` back to branch `math-agent-mols10`. Every pair passed full Latin row/column and pair-orthogonality checks; the scanner then exhaustively enumerated all common transversals and computed the maximum disjoint packing by exact branch and bound. **Zero UNKNOWN_BUDGET cases.**

| # common transversals | # orthogonal pairs |
|---:|---:|
| 0 | 2,455 |
| 1 | 308 |
| 2 | 17 |
| 3 | 1 |

Maximum number of common transversals was **3**. Maximum number of *mutually disjoint* common transversals was **2** (packing sizes: 2,455 with 0, 317 with 1, 9 with 2). No order-10 triple constructed. This is a rigorous **FINITE PUBLIC CORPUS** screening result, not a classification or nonexistence theorem for all order-10 orthogonal pairs.

Direct supporting link: https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/E062_WANLESS_PAIR_SCAN.json

### Controls independent of the large corpus

- The historical Egan–Wanless near-triple's orthogonal pair has **14** common transversals, exact maximum **7** pairwise disjoint; two independent routines reproduce this result (6,837 nodes to enumerate transversals, 80 for exact packing).
- Independent published pair from `scheinerman/LatinSquares.jl/ortho10.txt` verified Latin/orthogonality but has **0** common transversals (6,666 enumeration nodes).
- Full order-4 and order-5 positive triples independently yielded packs of size `n−1` and reconstructed all three mutually orthogonal squares exactly (`16/16/16` and `25/25/25`).

## 2. A different, far more targeted direct-existence attempt

Instead of generic pair-generation, start from Egan–Wanless A/B and **retain seven already disjoint common transversals** (as fixed *cell sets*). Let A remain fixed but B vary. The new B must be (i) a Latin square, (ii) orthogonal to A, and (iii) contain each of its ten symbols exactly once along each of the seven chosen transversals. This forms an exact-cover system with **1,000 binary `(r,c,b)` options and 470 exact-cover equations**: 100 cells, 100 B-row/symbol, 100 B-column/symbol, 100 A/B pair, and 70 (transversal/symbol) equations. B's first row is fixed to its published values *without loss up to independent B-symbol relabeling*.

**New exact fixed-source rigidity result:** There is **exactly one** B satisfying these constraints, namely the original Egan B, up to B-symbol relabeling.

- Z3 via the actual system `libz3.so.4` evaluated the fully specified 1,000-variable exact-one Boolean problem, appended `B ≠ original B`, and returned **UNSAT in 0.066 seconds**.
- Independently written **C++ DLX / Algorithm X** reconstructed the 470 demand constraints and enumerated **all complete solutions**: **899 search nodes, 1 solution, precisely the original B, 0 distinct B** (`EXHAUSTIVE_UNIQUE_B`). This independently validates the Z3 negative result without importing the solver's verdict. The published B was also explicitly checked to satisfy all 470 resources, preventing accidental input inconsistency.
- The same 1,000-variable MILP setup was *much less effective*: 3 independent 4-second tests and a 25-second test all returned `UNKNOWN_BUDGET`. These outcomes do **not** contradict the complete DLX / Z3 result; they expose a serious algorithm/encoding choice difference.

**Scope:** The rigorous uniqueness statement is specific to one fixed order-10 A and seven chosen transversal cell sets. It is not a theorem for arbitrary MOLS pairs, and it does not exclude existence of 3-MOLS(10). It *eliminates* the proposed strategy "hold this A and seven transversals, alter only B". The correct goal-backward response is to vary A and/or which cell sets form the transversal packing.

## 3. Unrestricted-A/B constrained constructive branch

Allow **both A and B to vary**, still fixing the seven chosen C-transversal *cell sets*. C-symbols were relabeled so its first row could safely be normalized to the identity, and each of A and B's first rows was likewise normalized independently. The A-first-column row-order normalization was intentionally **removed** because it is not sound with fixed row-indexed C clues. This retains every full triple with the chosen C pattern up to the stated independent symbol normalizations.

The C++ five-coordinate DLX created **17,146 candidate 5-tuples** and explored **3,457,024 nodes in ~20.1 seconds**, reaching a depth of 67 placed cells before returning **`UNKNOWN_BUDGET`**. No complete triple; no branch-level UNSAT claim. Independently recomputed that every one of the 70 fixed C clues matched the published seven transversals exactly after the relabeling.

## 4. Direct proof obligations to CLOSED

**Existence:** Construct any order-10 A/B pair with nine disjoint common transversals; or eight transversals with a bipartite 20-cell residual graph. Both yield an independent full 100/100/100 verifier. The published random-pair corpus overwhelmingly lacks even *one* transversal; unconditioned random pair generation should not be the main research strategy. A jointly constrained 5-coordinate OA / two-mate SAT search conditioning on seven or more C-classes is more logically aligned with closing the problem.

**Nonexistence:** Neither 2,781 sampled pairs nor 899-node fixed-source rigidity nor 3.45M DLX nodes cover all symmetry classes. A valid negative resolution still requires a full unrestricted mathematical theorem or independently checked SAT/UNSAT certificate plus proven global branch coverage.

**Research status:** **OPEN, no validated order-10 100/100/100 witness and no unrestricted proof; zero globally completed E033 A/B orbit exclusions.** A credible completion percentage or ETA cannot be inferred.

## Reproduction and sources

Run `python E062_scan_wanless_pairs.py --input E062_LOCAL_TEST_PAIRS.txt` for the independent 14/7 Egan control, then provide `--url` (or a downloaded `--input`) for the public 2,781 pairs. `python E062_public_pair.py` independently verifies the second known orthogonal pair has 0 transversals. Run `g++ -O3 -std=c++17 E062_independent_fixed7_dlx.cpp -o e062_fixed7 && ./e062_fixed7` for the finite exact uniqueness statement. `python E062_repair_seven_packing_z3.py` is an independent UNSAT solver check (requires system Z3). `g++ -O3 -std=c++17 E062_full_OA_seven_C.cpp -o e062_full && ./e062_full 10 20 4000000` reproduces the bounded five-coordinate construction attempt. All generated cases and sources are included in the accompanying ZIP; the published 5,562-square corpus itself is **not redistributed**, only its derived summary and SHA-256 are saved on GitHub.