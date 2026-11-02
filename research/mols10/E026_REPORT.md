# E026 — Exhaustive one-sided 3–5-symbol orthogonality-preserving trade exclusion

**UTC:** 2026-11-02 05:43–05:47. **Global status: OPEN.** No triple and no unrestricted nonexistence proof.

## Source/nonduplication audit
Read the living [Google Docs journal](https://docs.google.com/document/d/1NDPWEMM3Cf5HrhdOcV6pVE9tCI-kxKbavxcfIBFva3k/edit), branch `math-agent-mols10` `STATE.json` and E025 report/code before experimenting. Branch HEAD before E026 was `f6c93c082de50bd644c60d6777e5908c84685203`. E025 had exhaustively checked **proper two-symbol cycle flips in one/both squares** and bounded third flips. E026 instead changes **3, 4, or 5 complete original symbol classes in one square**, while keeping the orthogonal mate fixed; this is a different, larger local move class.

Primary literature checked: Bright–Keita–Stevens, *Electronic Journal of Combinatorics* 33(1), P1.30 (published 2026-02-13), https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; https://arxiv.org/abs/2503.10504 ; Barnoff–Bright https://arxiv.org/abs/2605.02132 (v2 2026-07-04). Targeted November 2026 searches found no independently checkable unrestricted resolution; search absence does not prove openness.

## Falsifiable question and complete encoding
For each of the six *specific published* orthogonal pairs UW, UX, VX, WW, WX, XX, let `Z=P^-1 Q`. Fix `Q` and choose `S`, a subset of `k` original symbols of `Z`. Can the `10k` cells where `Z` has symbols in `S` be recolored to form a **different** Latin square `Z'` orthogonal to `Q`, without changing any other cells?

Binary variables `x[cell,color]` assign one of `k` symbols to each selected cell. Exactly-one constraints apply to each cell and to every `(row,color)`, `(column,color)`, and `(Q-symbol,color)`. Because `Z,Q` are orthogonal, each row, column and Q-symbol fiber has exactly `k` selected cells. These constraints are necessary and sufficient for Latin `Z'` and orthogonality `Z',Q`. Fix all selected entries of row 0 to their original colors **without loss of generality**: any candidate can be independently relabeled on `S` to match row 0. Exclude the original normalized assignment by a single no-good inequality. Consequently, solver-complete UNSAT rules out all **nontrivial** recolorings of the selected symbol classes, modulo global symbol relabeling.

## Actual bounded computation
For **each** of the six fixed pairs, exhaustively tested all `C(10,3)=120`, `C(10,4)=210`, `C(10,5)=252` symbol subsets using SciPy/HiGHS MILP, each with a one-second per-instance cap. Every one of the **3,492** instances returned solver-complete **INFEASIBLE** (status 2), zero SAT, zero UNKNOWN. Runtime was a few seconds on CPU, no GPU.

| Pair | k=3 UNSAT | k=4 UNSAT | k=5 UNSAT | UNKNOWN |
|---|---:|---:|---:|---:|
| UW | 120 | 210 | 252 | 0 |
| UX | 120 | 210 | 252 | 0 |
| VX | 120 | 210 | 252 | 0 |
| WW | 120 | 210 | 252 | 0 |
| WX | 120 | 210 | 252 | 0 |
| XX | 120 | 210 | 252 | 0 |
| **Total** | **720** | **1,260** | **1,512** | **0** |

An **independently implemented exact 3-color DFS** checked all 720 k=3 cases, yielding exactly one row-0-normalized solution (the original) for every case. Total DFS nodes by pair: UW=166, UX=168, VX=190, WW=176, WX=172, XX=176, i.e. 1,048 nodes. This is a second algorithm, not another call to HiGHS.

**Nonvacuous positive control:** for genuine GF(9) orthogonal pair `Z=r+c`, `Q=r+αc` over `F3[α]/(α²+1)`, the same MILP finds a **nontrivial three-symbol trade** on `S={0,1,2}`, changing 18 cells and independently satisfying Latin + 81/81 orthogonality. Separate exact DFS counts four normalized solutions (three nontrivial). Thus the formulation does not universally forbid such moves.

## Failures and limits
A full WW k=6 exploratory sweep exceeded the outer execution budget and was **not** classified UNSAT. A separately bounded 0.5s-per-instance pilot on the first eight lexicographic six-symbol sets returned **one** solver-complete UNSAT and **seven UNKNOWN/time-limited**. These outcomes are preserved and not extrapolated. No SAT/DRAT/FRAT proof certificate, no family-wide classification, no unrestricted symmetry coverage, and no 100/100/100 witness. k>=6 remains open for these fixed pairs. The result concerns one-sided recoloring of symbol classes; simultaneous changes to both squares, arbitrary trades, and other members of the eight residual families are **not** excluded. Newness relative to all historical literature not established.

## Reproduction
```bash
cd research/mols10
python E026_symbol_support_milp.py
python E026_independent_3color.py
```
Input source: [E024_appendix_six_replay.py](https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/E024_appendix_six_replay.py). Code commits:
- [MILP + GF9 positive control](https://github.com/davidlueng986-alt/123321/commit/3094adde0c9b5647150aa63ec5f872cdbdac88e7)
- [Independent 3-color DFS](https://github.com/davidlueng986-alt/123321/commit/1b396707e0ef362be0e223c5956dd89dcc2926c6)
- [Summary results + failures](https://github.com/davidlueng986-alt/123321/commit/fb9ec4c9772c40b8f824905df825c5070669f7f1)

## Specific next action E027
Stop spending cycles on one-sided k<=5 moves for these six published examples. Obtain **new orthogonal pairs** via source SAT encoding with blocking clauses and rigorous symmetry normalization; alternatively search **two-sided** larger orthogonal-array trades. If a candidate appears, independently verify both Latin squares and 100/100 orthogonality, then enumerate common transversals and test exact-cover third-square completion. Keep global OPEN automation enabled.
