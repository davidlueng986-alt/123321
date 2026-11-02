# E027 — Exhaustive orthogonal mates for six fixed published Q squares
**UTC:** 2026-11-02 06:53 | **Global status:** OPEN

## Literature and provenance
Primary source: Bright–Keita–Stevens, *Myrvold's Results on Orthogonal Triples of 10×10 Latin Squares: A SAT Investigation*, Electronic Journal of Combinatorics 33(1), #P1.30 (2026-02-13): https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; arXiv: https://arxiv.org/abs/2503.10504 . Also checked Barnoff–Bright https://arxiv.org/abs/2605.02132 . Targeted web searches on 2026-11-02 found no independently verified unrestricted solution; this is not evidence of impossibility.

## Objective and distinction from E026
E026 exhausted one-sided 3–5-symbol changes around six particular orthogonal pairs, but could not rule out larger recolorings. Here **fix only the published second Latin square Q**, and enumerate *every* orthogonal mate Z of Q, modulo symbol relabeling of Z. This is a complete fixed-Q search, not a neighborhood search and not a classification of all Q in any Myrvold type.

## Exact reduction
A symbol class of Z must be a transversal of Q: one cell in each row, column and Q-symbol. Conversely, any partition of the 100 cells into ten disjoint Q-transversals defines a Latin square Z orthogonal to Q. Distinct unordered partitions correspond bijectively to Z modulo independent symbol relabeling; labeling each selected transversal by its first-row column gives a canonical Z with row zero [0,...,9]. Enumerate all Q-transversals, then all exact-cover partitions of the 100 cells. For each resulting (Z,Q), enumerate all common transversals. A third Latin square would require **ten** disjoint common transversals; finding 0 or 1 excludes extension of that fixed pair.

## Exhaustive results
| Published fixed Q | Q-transversals | Complete partitions | New mates beyond published Z | Common transversal counts over all mates | Bitset nodes | Independent DLX nodes |
|---|---:|---:|---:|---|---:|---:|
| UW | 848 | 3 | 2 | 0,0,0 | 51,243 | 30,990 |
| UX | 820 | 2 | 1 | 0,1 | 43,982 | 26,767 |
| VX | 848 | 2 | 1 | 0,0 | 48,849 | 29,520 |
| WW | 808 | 1 | 0 | 1 | 41,216 | 25,004 |
| WX | 812 | 1 | 0 | 0 | 42,369 | 25,813 |
| XX | 812 | 3 | 2 | 0,0,0 | 45,900 | 28,193 |
| **Total** | **4,948** | **12** | **6** | **all ≤1** | **273,559** | — |

**Restricted conclusion:** each of these six *specific* published Q squares cannot belong to a 3-MOLS(10) triple. In particular, WW and WX have a unique orthogonal mate up to relabeling, and the other four have respectively 3/2/2/3 mates. The six additional mates are real orthogonal pairs, not triples. The UX additional mate has one common transversal, insufficient for extension. No unrestricted proof; the existence of other Q within each family is untouched. Novelty relative to the complete literature is not established.

## Independent replay
- Primary exhaustive bitset exact-cover program: [E027_fixed_Q_exhaustive.py](E027_fixed_Q_exhaustive.py), commit https://github.com/davidlueng986-alt/123321/commit/22f1b2465b611351e1ba505ebc6061cb1b20a6dc
- Independent mutable-set Algorithm X implementation, independently enumerating Q-transversals: [E027_dlx_independent.py](E027_dlx_independent.py), commit https://github.com/davidlueng986-alt/123321/commit/e5cd4177f976b0f1015459642fec315be79a1312
- Original published matrix transcriptions and conversion P,Q→Z: [E024_appendix_six_replay.py](E024_appendix_six_replay.py).
- Compact results and input SHA-256 digests: [E027_RESULTS_SUMMARY.json](E027_RESULTS_SUMMARY.json), commit https://github.com/davidlueng986-alt/123321/commit/fc6241c4f5831ea67bdee7d5d906a1b4b3086d1f
- Reproduce: `cd research/mols10 && python E027_fixed_Q_exhaustive.py > E027_full.json && python E027_dlx_independent.py > E027_independent.json`. For each label, compare sorted JSON-serialized `mate` matrices to independent `mates`; both enumerate identical complete sets. Independently check Latin rows/columns and 100 ordered pairs for all 12, and common transversal counts [0,0,0], [0,1], [0,0], [1], [0], [0,0,0].
- Local full-output SHA256 (elapsed time fields make first hash run-specific): bitset `61a8249c96b8c19228c4b1f4e955f16b99b55e397f0c5e0c98e8219685078fcb`; independent `394a11733f398671034bef8dba7bb2ccf92844ccb494957b94ec96ba47a7194c`.
- No GitHub Actions CI completion is claimed for E027.

## Failed experiments preserved
1. HiGHS MILP alternative-mate model for WW/UW/UX/VX/WX hit 12-second limits, status **UNKNOWN** (not UNSAT). The full six-label batch also exceeded the outer timeout. No false infeasibility claim.
2. Naive row-0-first Python exact-cover recursion exceeded outer timeout; superseded by independent mutable Algorithm X with MRV, all six complete.
3. Previous E026 six-symbol MILP pilot remains UNKNOWN for seven cases; E027 does not retroactively certify those solver runs.

## Uncertainty and next action
The fixed-Q enumeration is exhaustive conditional on source matrix transcription and correct exact-cover implementations; independent implementations agree exactly on all matrices. No third-square witness, no unrestricted symmetry coverage, no DRAT/FRAT certificate, no proof for all Myrvold residual-family Q. Next: extend fixed-Q enumeration to SX/UU and independent source verification, then seek a genuinely different Q (rather than repeat symbol trades), preferably from published SAT encoding or explicit orthogonal-pair search. Verify any candidate as three Latin squares and 100/100/100 overlays before claiming resolution. Continue hourly research.
