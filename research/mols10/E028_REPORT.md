# E028 — Complete fixed-Q orthogonal-mate enumeration for published SX and UU
**UTC:** 2026-11-02 08:09 | **Global 3-MOLS(10): OPEN**

## Literature status and attribution
Primary source: Curtis Bright, Amadou Keita, Brett Stevens, *Myrvold's Results on Orthogonal Triples of 10 × 10 Latin Squares: A SAT Investigation*, Electronic Journal of Combinatorics 33(1) #P1.30, published 2026-02-13: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; arXiv https://arxiv.org/abs/2503.10504 . Secondary relevant work: https://arxiv.org/abs/2605.02132 . Targeted search on 2026-11-02 found no independently checkable unrestricted resolution. Absence of search results is not a proof.

## Objective / why this is nonduplicative
E027 exhaustively enumerated orthogonal mates for six specific published fixed Q squares (UW,UX,VX,WW,WX,XX), but SX and UU were previously only excluded as *fixed pairs* in E023. Here **fix only the source SX or UU Q**, exhaustively enumerate *every* Q-orthogonal mate Z up to symbol relabeling of Z, and test each for possible third-square extension. This is stronger than checking the published pair alone, and completes the eight **specific** published Q examples. It does **not** eliminate the eight Myrvold families.

## Exact mathematical reduction
Each symbol class of a Q-orthogonal mate Z must be a transversal of Q (one cell in each row, column, and Q-symbol). Conversely, any exact-cover partition of the 100 cells into ten disjoint Q-transversals defines a Latin Z orthogonal to Q. Unordered partitions correspond bijectively to mates modulo relabeling Z symbols. Normalize Z by assigning each chosen transversal the column index of its first-row cell, so Z[0,c]=c. Enumerate all Q-transversals, then all exact covers. For each resulting pair (Z,Q), enumerate all common transversals: a third Latin square would require ten pairwise disjoint common transversals.

## Actual complete results
| Specific published fixed Q | Q transversals | Normalized orthogonal mates | Additional mates | Common transversal counts | Bitset nodes | Independent Algorithm X nodes |
|---|---:|---:|---:|---|---:|---:|
| SX | 864 | **2** | **1** | 0, 0 | 57,110 | 34,710 |
| UU | 816 | **1** | **0** | 0 | 40,048 | 24,753 |
| **Total** | **1,680** | **3** | **1** | all zero | **97,158** | **59,463** |

For SX, both the published mate and the additional distinct normalized mate are orthogonal to Q (100/100), yet neither has a common transversal with Q. For UU, the published mate is the unique orthogonal mate up to symbol relabeling, and it has no common transversal. Therefore neither of these **two particular fixed Q matrices** can occur in a 3-MOLS(10) triple.

Combining E027 and E028: all eight **particular published Appendix Q squares** are excluded as a possible member of a triple, via complete fixed-Q mate enumeration. This does **not** exclude all Q within any residual family, nor prove unrestricted nonexistence. The new SX mate is a genuine orthogonal pair, not a triple. Novelty relative to all external literature is not established.

## Independent validation and reproducibility
- Source P and Q from `E023_SX_pair_replay.py` and `E023_UU_pair_replay.py`, originally transcribed from the BKS Appendix. Reconstruct Z[r,c]=unique t with P[t,c]=Q[r,c], check Latin and overlay 100, recover the published normalized mate exactly once for each Q.
- `E028_SX_UU_fixed_Q.py` calls `E027_fixed_Q_exhaustive.py` (bitset exact cover) and `E027_dlx_independent.py` (separately implemented mutable-set Algorithm X). The two implementations independently enumerate Q-transversals and obtain **identical complete sets of all three normalized mate matrices**, not only identical counts.
- A third independent checker enumerates all `10! = 3,628,800` row-column permutations for **each** of the three mates, **10,886,400 permutations total**. All three common-transversal counts are zero, agreeing with the recursive checker.
- Local executed source: `cd research/mols10 && python E028_SX_UU_fixed_Q.py > E028_full.json`. The published repository code uses existing E023/E027 modules; local run used copies of those existing modules and the same wrapper. Elapsed wall times in the replay were approximately SX 9.37s and UU 6.16s, without GPU.
- Source-Q SHA256 compact JSON: SX `4395c594803efb29f388784b4cafa96b07729e17278ed50674bafe6bb7f5a4df`; UU `397714f132cc7b2ef237aadc925646e7396ad8e1ebd1e09c4ca3d571cfebda86`.
- Local full output JSON SHA256 `3fd56d03efb475bfbbcc0cdeb330c5f78ac48beab0fc13a69a4293bd1dc67e2a` (contains timing fields; hashes may differ between reruns).
- Compact data: `E028_RESULTS_SUMMARY.json`. No CI completion is claimed for E028; local execution passed.

## Failures and uncertainty
1. Container `git ls-remote` failed DNS. The connected GitHub API was used for source review and writes; no claim of successful local git clone.
2. An optional source-audit patch attempt failed with a Python quoting `SyntaxError`; **no results from that failed attempt were accepted**. The source-audit function was corrected, and both exact-cover algorithms and full 10! replay were rerun successfully.
3. No DRAT/FRAT proof certificate, no unrestricted classification of order-10 squares or all Myrvold residual families, no 100/100/100 triple. Exhaustiveness is for these two exact Q matrices only.

## Specific E029 next action
Stop checking these eight published fixed Q examples. Acquire **genuinely different** Q from the authors' public SAT encoding (or independent orthogonal-pair generation), prove it is not merely a symbol-relabeling of an already checked Q, verify Latin and 100/100 overlay, compute exact common-transversal count/support, and if necessary solve the third-square exact-cover problem. Prefer a bounded SAT pilot with explicit model blocking and reproducible inputs. If positive, require independent 100/100/100 replay; if negative, do not extrapolate from a single Q. Keep the research automation active.
