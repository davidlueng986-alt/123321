# MOLS10 E021 — independent unary exact-cover replay and Egan countercontrol

Run: 2026-11-02 00:49–00:54 UTC. GLOBAL STATUS OPEN. No unrestricted proof or 100/100/100 triple.

## Fresh primary-source screening
- Bright–Keita–Stevens, Electronic Journal of Combinatorics 33(1) P1.30, published 2026-02-13: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; https://arxiv.org/abs/2503.10504
- Barnoff–Bright, arXiv:2605.02132, July 2026 revision: https://arxiv.org/abs/2605.02132
- Bright–Keita–Stevens, arXiv:2509.09633 v3 (2026-08-20): https://arxiv.org/abs/2509.09633 . Its SAT enumeration concerns orthogonal PAIRS, not triples.
- Targeted fresh search for complete 3-MOLS(10) construction or nonexistence certificate found no independently verifiable unrestricted resolution. Absence of hits is not a proof of openness.

## Objective and mathematical reduction
Independently certify all E020 Parker unary roots, rather than rerun E017 fixed-A two-mate DFS. Also test whether Parker's compact unary obstruction generalizes to Egan first A.

For fixed A, every B-symbol class U is an A-transversal. If a triple (A,B,C) exists, the ten C-symbol transversals form an exact cover of all n^2 cells, each meeting U exactly once. For each U, exhaustively solve this constrained C exact-cover problem. A root is forbidden if its C exact cover is UNSAT. If the union of all surviving U misses any cell, that fixed A cannot belong to a triple.

The independent implementation enumerates all n! row-column permutations, builds cell incidence and overlap graph, then uses memoized remaining-cell Algorithm X with MRV. Memoization on remaining-cell masks is valid: for fixed U, the eligible future C classes are exactly those in the original U-compatible pool wholly contained in the remaining cells. Node cap is 200,000 per root, with explicit UNKNOWN on exhaustion.

## Actual bounded CPU results
| First A | Transversals | SAT roots | Exhaustive UNSAT roots | UNKNOWN | DFS nodes | Max nodes/root | Uncovered cells |
|---|---:|---:|---:|---:|---:|---:|---:|
| Parker published A | 1104 | 28 | 1076 | 0 | 1369521 | 4853 | 13 |
| Egan published A | 1080 | 114 | 966 | 0 | 690262 | 1380 | 0 |

Parker surviving root indices: [26,29,50,55,165,167,195,202,380,395,438,453,512,531,547,563,577,643,663,727,844,850,853,915,924,950,963,1060].
Parker 13 uncovered flattened cells (zero-based): [2,13,24,35,46,50,61,77,78,79,88,97,98].
These reproduce E020 exactly, with a different search-state representation and 10! enumerator. Parker fixed-A exclusion is independently corroborated. It remains conditional and is not a general solution.

Egan 114 surviving roots cover all 100 cells: unary coverage obstruction FAILS to exclude Egan A. This is a useful negative result and does not imply that a triple exists; E016 used a different fixed-Egan exclusion.

Input SHA256 Parker: 1694eda37452b6709d8f8d77d8dfcddae08e18c6a94e4aabc102bec6323c1c77.
Input SHA256 Egan: 965a201951eb261b3ec9c8575163e8d7a6f70e384fd90699a77bc59a1b0ebc33.
Local Python elapsed: Parker 14.89 seconds, Egan 9.60 seconds; no GPU.
GF(4) positive control: independently verified Latin squares and 16/16/16 pairwise overlays; all eight unary roots SAT.

## Failures and limitations
- Initial independent prototype used expensive Python list filtering and timed out after 120 seconds. No UNSAT claim from this timeout; replaced with incidence/overlap bitsets and retained memoization.
- Generalizing order n temporarily caused a positional CLI TypeError when audit(args.cap) passed an integer as the square. Fixed to audit(cap=args.cap), then reran both complete cases.
- No SAT/DRAT/FRAT certificate; both implementations share the same mathematical reduction. No unrestricted symmetry coverage, no general nonexistence proof, no triple witness. Novelty not established.

## Reproduce
Run from research/mols10:
1. python E021_independent_replay.py --cap 200000 --out E021_RESULTS_replay.json
2. python E021_egan_audit.py
3. python test_E021_controls.py

All stdlib; no external solver. The Egan script writes E021_EGAN_RESULTS.json. Checked-in E021_RESULTS.json summarizes both experiments and failures. CI was not yet verified at report creation.

## Next E022
Explore a pair-root C exact-cover obstruction on Egan A: given two disjoint B classes U,V, every C class must intersect both exactly once. Begin with a bounded symmetry-diverse sample; do not run a huge unrestricted search without an informative pilot. Alternatively import Myrvold's eight published residual structures with independently validated input arrays. Keep global OPEN and research enabled.
