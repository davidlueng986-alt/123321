# E024 — Six remaining published Myrvold Appendix pairs (2026-11-02 03:50 UTC)

## Status
**3-MOLS(10) remains OPEN.** No verified complete 100/100/100 witness and no unrestricted exhaustive nonexistence proof. Literature rechecked: Bright–Keita–Stevens, *Electronic Journal of Combinatorics* 33(1) (2026), P1.30 (2026-02-13), https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; https://arxiv.org/abs/2503.10504 ; Barnoff–Bright, arXiv:2605.02132v2 (2026-07-04), https://arxiv.org/abs/2605.02132 . No independently checkable complete solution found as of this iteration; absence of search hits is not a proof.

## Objective and scope
E023 already independently replayed the source's **SX** and **UU** example TRP pairs (both zero common transversals). This E024 targets the **six different published example pairs** UW, UX, VX, WW, WX, XX on printed pp.32–33 of the primary paper, avoiding any repeat of SX/UU. Importantly, one pair per type is NOT exhaustive coverage of any of the eight Myrvold residual families.

## Actual computation
Source appendix: https://www.combinatorics.org/ojs/index.php/eljc/article/download/v33i1p30/pdf/ (rendered PDF page indices 31,32, manually crosschecked). For each exact published pair P,Q, verified that P and Q are Latin; constructed Z[r,c] = the unique t such that P[t,c]=Q[r,c]; verified that Z is Latin and all 100 pairs (Z[r,c],Q[r,c]) are distinct; independently counted common transversals of Z,Q with row-by-row bitmask DFS and a **full 10! permutation replay**.

| Published pair type | Latin P,Q,Z | overlay(Z,Q) | common transversals (DFS) | independent 10! | supported cells | Third square for THIS fixed pair |
| --- | --- | --- | ---: | ---: | ---: | --- |
| UW | PASS | 100 | 0 | 0 | 0 | impossible |
| UX | PASS | 100 | 0 | 0 | 0 | impossible |
| VX | PASS | 100 | 0 | 0 | 0 | impossible |
| WW | PASS | 100 | 1 | 1 | 10 | impossible |
| WX | PASS | 100 | 0 | 0 | 0 | impossible |
| XX | PASS | 100 | 0 | 0 | 0 | impossible |

**WW unique common transversal:** row→column permutation (0-indexed) = [9,4,7,2,8,6,0,5,3,1], flattened cells [9,14,27,32,48,56,60,75,83,91]. Six exhaustive 10! checks = 21,772,800 permutation candidates; all completed in ~12 CPU seconds. GF(4) positive control independently checked pairwise overlays 16/16/16. No GPU, timeout or solver UNKNOWN. For each fixed pair, a third square requires ten disjoint common transversals; all six have fewer than ten, hence **UNSAT_FIXED_PAIR** (direct finite combinatorial obstruction).

## Artifacts
- Reproducible Python and exact 12 source arrays: [E024_appendix_six_replay.py](E024_appendix_six_replay.py). Run `python E024_appendix_six_replay.py` from this directory.
- Machine-readable results: [E024_RESULTS.json](E024_RESULTS.json).
- Prior SX and UU source-replay files: [E023_REPORT.md](E023_REPORT.md).
- Primary source above. No external code was needed.

## Failures and uncertainty
Direct container PDF download failed DNS resolution; used web PDF text plus rendered page images and independently checked all Latin/orthogonality properties. Source arrays are manually transcribed, not binary-extracted; a wrong-but-valid Latin transcription is a residual risk mitigated by visual inspection. No formal DRAT/FRAT certificate. **These six fixed-pair exclusions do not exclude the six entire pattern families.** The combined E023/E024 eight example exclusions are not a proof that no triple has a 4×4 subsquare, much less unrestricted 3-MOLS(10). Novelty of this simple fixed-pair replay relative to prior work not established.

## Next falsifiable action (E025)
Avoid repeating source examples. Generate **additional distinct orthogonal pairs** in Myrvold residual types (especially WW, the only source example with any common transversal), record isotopy/paratopy normalization, and screen for common-transversal counts and full 100-cell support. If a candidate has ≥10 and full support, attempt exact-cover third-square completion. Alternatively, produce a certified SAT proof for a rigorously stated restricted family. Do not treat solver timeout as UNSAT.
