# E025 — Coupled proper two-symbol Latin trades around six published order-10 orthogonal pairs
**Run:** 2026-11-02 ~04:47 UTC (bounded CPU only)  
**Global status:** OPEN; no verified 3-MOLS(10) witness or unrestricted nonexistence certificate.

## Literature / nonduplication audit
Read the living Google Doc, `STATE.json` at branch head `c1fc9032a441d3ed4851ff804b09776d5d3eebe8`, and the E023/E024 source-verified replay code. The previous E024 iteration already exhausted common transversals of the six **specific** published examples; do not repeat that computation as if it were new. Rechecked Bright–Keita–Stevens, *Electronic Journal of Combinatorics* 33(1), P1.30 (2026-02-13), https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; arXiv https://arxiv.org/abs/2503.10504 ; and Barnoff–Bright https://arxiv.org/abs/2605.02132 (v2 2026-07-04). Search through 2026-11-02 found no independently verifiable unrestricted resolution; lack of a search hit is not a proof of openness.

## Falsifiable subproblem
Can an orthogonal pair `(Z,Q)` from any of the six published residual-pattern examples UW, UX, VX, WW, WX, XX be moved to a **different** orthogonal pair by a proper two-symbol Latin cycle flip in either square, or by one such flip in **each** square simultaneously?

For symbols `x,y`, their 20 cells form a 2-regular bipartite row–column graph. A swap `x↔y` restricted to those cells preserves the Latin property **iff** it is a union of whole connected components: in each affected row and column, both `x` and `y` must be swapped together. Enumerate all nonempty, non-full component subsets. The empty and full subsets are excluded: full is merely global symbol relabeling. Enumerating all pairs of independently generated proper flips in the two squares is exhaustive **for this neighborhood**.

## Actual computation and evidence
Inputs: exact P,Q arrays in `E024_appendix_six_replay.py`; construct `Z=P^{-1}Q`. For each case verify Latin P,Q,Z and overlay(Z,Q)=100, generate all proper component flips, assert Latin on every variant, and count exact overlay cardinality. Independent JavaScript implementation (flat arrays and Uint8Array uniqueness) and Python implementation (tuple-set overlay) agreed on double-flip counts and maxima.

| Type | Proper Z flips | Proper Q flips | Coupled tests | Maximum overlay | New orthogonal pairs |
| --- | ---: | ---: | ---: | ---: | ---: |
| UW | 118 | 138 | 16,284 | 96 | 0 |
| UX | 108 | 118 | 12,744 | 96 | 0 |
| VX | 126 | 108 | 13,608 | 96 | 0 |
| WW | 154 | 130 | 20,020 | **98** (4 candidates) | 0 |
| WX | 100 | 100 | 10,000 | 96 | 0 |
| XX | 132 | 114 | 15,048 | 96 | 0 |
| **Total** | **718** | **728** | **87,704** | 98 | **0** |

Also tested all **1,446** single-side proper flips; none preserved pair orthogonality. As a bounded third-flip pilot, allowed one additional proper two-symbol component flip in either square for every *best* double-flip candidate in each case (**96,768** trials), all nonorthogonal. For WW specifically, expanded to **all 96 double-flip candidates with overlay >=96**, yielding **26,184** additional third-flip trials, no orthogonal pair (best 98). These follow-up sets overlap; do not add them as distinct searches.

The four WW 98/100 double-flip candidates are **near-pairs only**: both component squares remain Latin but they are **not orthogonal**. They are not a third square or an answer to 3-MOLS(10).

**Negative evidence:** No new orthogonal pair in the fully specified one- and two-flip neighborhood of any of these six *specific* pairs; no successful repair in the precisely bounded three-flip pilots. This is not a result for the six residual **families** and does not cover general Latin trades or arbitrary pair changes.

## Reproduction
```sh
cd research/mols10
python E025_coupled_trades.py
# writes E025_RESULTS.json with full overlay histograms, best examples and follow-up results
```
Code: https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/E025_coupled_trades.py (commit https://github.com/davidlueng986-alt/123321/commit/e2eb2c51956d743c69a536bc0bd7a1bd96144501).  
Summary: https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/E025_SUMMARY.json (commit https://github.com/davidlueng986-alt/123321/commit/1d484050ad92189bc2802f0f4f796d0750b53731).

## Failure modes / limitations / next action
No independent SAT proof certificate; instead exhaustive enumeration over a *small explicitly defined* local move class. A local `git ls-remote` attempt failed DNS resolution; GitHub connector reads and writes succeeded. No randomness or GPU. The source examples' isotopy/paratopy classes were not exhaustively classified. The constrained trade route failed to produce a new pair, so **E026 should not repeat the same neighborhood**. Highest-value next step: obtain a *new* WW residual-pattern SAT model from the authors' published encoding with a blocking clause against the original witness, or use a larger multi-symbol orthogonal-array trade neighborhood with strict independent Latin+orthogonality replay; then compute common transversals, 100-cell support, and exact-cover third-square feasibility.

No global resolution; keep existing automation enabled.
