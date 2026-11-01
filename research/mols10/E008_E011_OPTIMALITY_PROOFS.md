# E008–E011 — Exact conditional optimality certificates, signed transversal duals, and genuinely different first Latin squares
**Research date:** 2026-11-02. **Global status:** 3-MOLS(10) remains OPEN. **Novelty:** No claim of originality without paper-level literature comparison.

## 1. Core mathematical lemma (exact, solver-independent)

Let `A,D` be two fixed Latin squares of order `n` that are orthogonal, and `X` be ANY Latin square orthogonal to `A`. For each symbol `s` in `X`, its locations `T_s={(i,j):X_ij=s}` meet every row, every column and every A-symbol once: an **A-transversal**. The `n` sets `T_s` partition the `n²` cells.

The number of distinct ordered pairs in overlay `(D,X)` equals:
```
U(D,X) = sum_{s=0}^{n-1} |{D_ij : (i,j) in T_s}|.
```
**Binary deletion-set certificate.** Choose a cell subset `R`. If for every A-transversal `T`:
```
|{D_ij : (i,j) in T}| <= |T \ R| = n - |T intersect R|,
```
then summing over all `X`-symbol classes proves:
```
U(D,X) <= n² - |R|.
```
The proof uses only set partition and an exact finite check of the certificate on every A-transversal, NOT a probabilistic solver claim.

**Signed rational weighted certificate.** More generally, choose integer cell weights `z_ij` and positive integer denominator `q` such that for EVERY A-transversal `T`:
```
sum_{(i,j) in T} z_ij <= q * (n - |{D_ij:(i,j) in T}|).
```
Summing over the partition gives
```
U(D,X) <= floor(n² - (sum_{all cells} z_ij)/q).
```
Negative weights are perfectly valid, since each cell appears exactly once in the partition. This is a discrete LP-dual argument; all published certificate checks below use **integer arithmetic** and independent data, not floating-point optimizer output.

## 2. E008 — FIX Egan–Wanless (A,C): exact best score = 91

Source inputs: `near_triple.json`, squares indexed `A=0,B=1,C=2`, reproducing Egan–Wanless 2016's public dataset: https://users.monash.edu.au/~iwanless/data/MOLS/neartripleMOLS10.txt .

Choose the following nine 0-based cell positions:
```
R = {(0,1),(0,2),(0,6),(0,9),(3,8),(5,0),(5,1),(6,0),(9,0)}.
```
For all **1080** A-transversals, exhaustive exact replay verifies
```
distinct_C(T) <= 10 - |T intersect R|.
```
The smallest slack is 0; 30 transversals are tight. A first implementation enumerated ALL `10!=3,628,800` row-column permutations; an independent bitmask DFS returned the IDENTICAL 1080 A-transversals. The standalone `dual_certificates.py` verifier and `test_dual_certificates.py` repeat this validation, including a deliberately corrupted certificate that must fail.

Consequently, for EVERY Latin `B'` orthogonal to this fixed A:
```
U(B', C) <= 100 - 9 = 91.
```
The published B has `U(B,C)=91`, hence **91 is globally optimal over every choice of B' with this A,C fixed**. The attainable witness is independently checked Latin and orthogonal to A.
Machine-readable certificate: `E008_DUAL_CERTIFICATE.json`. This is a stronger conditional optimization statement than simply counting common transversals of A,C.

## 3. E010 — FIX Egan–Wanless (A,B): exact best score = 91

A simpler nine-cell binary deletion certificate was not found for the A,B direction; a signed half-integer certificate works.

Use `q=2` and the **exact** 10×10 integer numerator matrix in `E010_EGAN_AB_WEIGHTED91.json`. Its entries sum to **18**. For every one of the **1080** A-transversals, `signed_dual.py` verifies:
```
sum z_ij(T) <= 2*(10 - distinct_B(T)).
```
Minimum slack 0, with 61 tight transversals. Thus any Latin `C'` orthogonal to fixed A obeys
```
U(B, C') <= floor(100 - 18/2) = 91.
```
Published C attains 91, so this bound too is **optimal for the fixed A,B**.

**Branch-pruning consequence:** The famous A,B,C near-triple cannot be repaired by changing JUST one of the three squares. Changing B alone or C alone is blocked by these global conditional optimality certificates; changing A alone leaves the already non-orthogonal B,C unchanged. A complete 3-MOLS(10) construction must leave this two-square-fixed neighborhood. This does **not** establish that no other complete triple exists.

## 4. E009 — Historical Bose–Shrikhande–Parker pair: exact upper bound 77

Input source `parker_pair.json`, copied from P. W. M. John p.114: https://sites.ualberta.ca/~dwiens/stat568/misc%20resources/PWJohn.pdf .

A binary 22-cell deletion set `E009_PARKER_DUAL_CERTIFICATE.json` yields the independently checked bound `U(B,C')<=78`. More strongly, `E009_PARKER_WEIGHTED77.json` supplies an exact **signed half-integer certificate** with denominator `q=2`, ten rows of ten integer numerators, and sum of numerators **45**. Exhaustive DFS verifies the inequality above for all **1104** A-transversals, with minimum slack 0 and 267 tight cases. Hence:
```
U(B,C') <= floor(100 - 45/2) = 77
```
for any Latin `C'` orthogonal to this fixed Parker A. The 77 is a **verified upper bound**, not a known attainable value and not a statement about arbitrary order-10 pairs. The numeric LP optimizer suggested 77.5; the published exact signed numerator certificate is what makes the integer upper bound rigorous.

The Parker pair itself has **zero** common transversals (E003), so an extension is impossible even without this sharper quantitative near-orthogonality bound. The extra information is *how far from orthogonality any hypothetical third mate must remain*.

## 5. E011 — Move to genuinely different first-square structures

Starting from Egan A, enumerated every 2-symbol row/column trade graph, flipped each proper connected component (one representative per complementary pair), and generated **48 Latin first-square variants**. Every resulting square was verified Latin. The single-square transversal-count histogram is:
```
{840:6, 872:3, 892:6, 904:10, 912:3, 924:3, 928:3, 948:5, 952:3, 1000:6}
```
versus **1080** for the original A. Since transversal count is invariant under the usual row/column/symbol isomorphisms (and all three-coordinate parastrophes), each candidate is provably **not isotopic/paratopic to the original A**. No candidate remains orthogonal to the original published B or C. This does not mean they lack other mates.

Twelve tiny-budget fixed-A mate attempts on the first twelve variants (seed 0, per-seed 0.2 s) all returned `UNKNOWN_BUDGET`, NOT UNSAT. A previous unrestricted 48×2 attempt exceeded the local execution limit and produced no reliable full result: label it `UNKNOWN_TIMEOUT`.

Reproducible first-square generator: `first_square_trades.py` and `test_first_square_trades.py`.

## 6. Interpretation and research decision

The conditional dual certificates are **actual finite mathematical proofs**, not sample-based estimates. In contrast, E011's mate generation is incomplete. None of E008–E011 proves or disproves existence of any 3-MOLS(10) globally. The novelty of conditional bounds in the external mathematical literature remains **unverified**.

Next `E012`:
1. First perform a quick prior-art search for weighted transversal bounds and any published 91-optimal near-triple claims.
2. Do **not** allocate further compute to changing only B or C with Egan A and the other published mate fixed — both directions are now exactly optimal at 91.
3. Use the 48 nonparatopic-to-A Latin structures as candidates, but seek valid mates with a stronger structured SAT / MILP or constraint-programming model; measure `UNKNOWN` explicitly.
4. To approach a real triple, prioritize pairs with at least 10 joint common transversals and full 100-cell support before expensive exact-cover partition search.
5. Consider stronger, proof-audited normalizations in the full OA(100,5,10,2) representation; ensure no invalid simultaneous first-column normalizations. See proofatlas.ai collaboration route on this problem, but independently audit all claims.

Primary open-status reference: Bright, Keita & Stevens, EJC 33(1) 2026, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 .

### Replay (Python 3.12, standard library only)
```bash
cd research/mols10
python dual_certificates.py E008_DUAL_CERTIFICATE.json --independent
python dual_certificates.py E009_PARKER_DUAL_CERTIFICATE.json --independent
python signed_dual.py E009_PARKER_WEIGHTED77.json
python signed_dual.py E010_EGAN_AB_WEIGHTED91.json
python -m unittest discover -p 'test_*.py' -v
```
The discovery optimizers used SciPy/HiGHS locally, but the replay and GitHub CI have **no SciPy dependency**.
