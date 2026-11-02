# E029 — Exhaustive fixed-Q mate audit of Egan–Wanless B and C
**Date:** 2026-11-02 ~09:04 UTC. **Global 3-MOLS(10) status:** OPEN.

## Source audit
Egan–Wanless near-triple original data: https://users.monash.edu.au/~iwanless/data/MOLS/neartripleMOLS10.txt ; canonical input in this repository: [near_triple.json](near_triple.json).
Recent primary sources: Bright–Keita–Stevens, *Electronic Journal of Combinatorics* 33(1) #P1.30, published 2026-02-13, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; arXiv:2503.10504v2 (2026-01-21), https://arxiv.org/abs/2503.10504 ; Barnoff–Bright, arXiv:2605.02132, https://arxiv.org/abs/2605.02132 . Targeted 2026-11-02 search found no independently checkable unrestricted resolution; lack of search hits is not a proof.

## Falsifiable objective and novelty relative to E028
E028 exhaustively excluded the eight **specific** BKS Appendix Q matrices. E002 had ruled out the **specific pairs** (Egan A,B) and (Egan A,C), but did not enumerate all other orthogonal mates of Egan B or C. Here fix **only** Egan B and then **only** Egan C, independently enumerate all mates modulo mate-symbol relabeling, and test every mate for common transversals. This is a stronger fixed-Q exclusion than E002; it is not a new unrestricted theorem and novelty relative to the whole literature is unestablished. Isotopy inequivalence to BKS Q was NOT checked.

## Exact reduction and scope
For fixed Latin Q, the symbol classes of a Latin mate Z orthogonal to Q form ten pairwise disjoint Q-transversals covering all 100 cells. Conversely, any such partition produces Z. Label each class by its column in row 0 to normalize symbol relabeling. Enumerate all Q-transversals and all exact-cover partitions. For each Z, a third square would need ten disjoint common transversals of (Z,Q). If fewer than ten common transversals exist, that fixed pair cannot extend. This reasoning covers every mate of the **exact fixed Q**, but no other Q or isotopy family.

## Complete computation
| Fixed Q | Q-transversals | Normalized orthogonal mates | Bitset nodes | Independent Algorithm X nodes | Common transversal counts | Common cell support |
|---|---:|---:|---:|---:|---|---|
| Egan B | 932 | **5** | 108,830 | 64,582 | 0,14,2,0,0 | 0,88,19,0,0 |
| Egan C | 864 | **4** | 59,173 | 36,254 | 0,0,7,0 | 0,0,64,0 |
| Total | 1,796 | **9** | 168,003 | 100,836 | all <10 | — |

All nine mates are Latin and have 100/100 orthogonality with their fixed Q. Both independent exact-cover implementations return the **identical complete set of nine canonical mate matrices**, not just the same counts. The known Egan A is recovered exactly once for each fixed Q. In an independent compiled C++ checker, **all 10!=3,628,800 row-column permutations were tested for each mate**, 32,659,200 total, reproducing the common-transversal counts and cell supports from Python's recursive checker.

**Restricted result:** neither the specific Egan B nor the specific Egan C can appear in any 3-MOLS(10) triple, regardless of which orthogonal mate is chosen. This does NOT imply that all squares isotopic to B or C are excluded by a demonstrated isotopy classification, although fixed-Q properties are invariant under isotopy; no global symmetry coverage is claimed.

## Reproduction and audit evidence
Run `cd research/mols10 && python E029_Egan_BC_fixed_Q.py > E029_full.json`. Script: [E029_Egan_BC_fixed_Q.py](E029_Egan_BC_fixed_Q.py). Input: [near_triple.json](near_triple.json). The script calls two independently implemented exhaustive engines [E027_fixed_Q_exhaustive.py](E027_fixed_Q_exhaustive.py), [E027_dlx_independent.py](E027_dlx_independent.py) and the independent 10! permutation checker [E028_SX_UU_fixed_Q.py](E028_SX_UU_fixed_Q.py). Summary: [E029_RESULTS_SUMMARY.json](E029_RESULTS_SUMMARY.json). All source matrix and output checks are exact integer operations; no GPU.

Local primary output SHA256 `bb64706bb4a1c99a3505662ad38811ea8379ace5784ccee66c4cdd06e75ab43f`.
Local independent output SHA256 `b307ffec28f050325022221efbe2aef9d6afdbff750c41b1c6a52583d56926a9`.
Local independent compiled C++ permutation-output SHA256 `8dec2a57afa6d26173b63548bd6518d3afe4cc28181ca948a4b9aebc6ef55bb7`.
Local standalone scripts generated these outputs; the committed wrapper provides equivalent replay from canonical repo inputs and existing engines. Do not claim GitHub CI passed without observing it.

## Failed experiments, limitations, next action
An initial local C++ checker-generation attempt failed with `ModuleNotFoundError` because `/mnt/data` was missing from `sys.path`. No results were accepted from that failed run; corrected and reran all nine 10! checks successfully. No timeout or UNKNOWN in completed enumerations. No DRAT/FRAT certificate, unrestricted symmetry coverage, isotopy classification, or 100/100/100 witness. The global problem remains OPEN.

**E030:** Stop rechecking these ten fixed-Q matrices (eight BKS Appendix + Egan B,C). Build an independent SAT encoding for new Q (prefer genuinely nonisotopic representatives with justified canonicalization), block known pairs and relabelings, and test common-transversal count and 100-cell support before third-square exact-cover completion. Preserve all UNKNOWN and failed SAT attempts.
