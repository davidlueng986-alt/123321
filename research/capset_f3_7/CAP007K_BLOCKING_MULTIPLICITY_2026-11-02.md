# CAP-007K pilot — cross-slice blocking multiplicity (2026-11-02)

Independent integer-only JavaScript audit completed for all 3812 unique relative GL(6,3) matrices of elementary-word-length <=2, using the independently checked canonical 112+112+12 known cap fixture. No paid compute or GPU.

For a fixed pair of 112-point slices S and T transformed by a relative linear matrix M, set r_M(z)=|{(s,t) in S x MT : -s-t=z}|. Then the third slice may only use z with r_M(z)=0; its potential positions H_M are the zeros of r_M.

Verified exact cross-tab, 3812 matrices:

| holes | minimum positive r(z) | number of matrices |
|---:|---:|---:|
| 0 | 5 | 70 |
| 0 | 6 | 720 |
| 0 | 7 | 15 |
| 0 | 8 | 1260 |
| 0 | 10 | 1440 |
| 1 | 16 | 126 |
| 4 | 10 | 60 |
| 12 | 11 | 121 |

**Restricted deletion-resilience lemma.** In every one of the 121 relative alignments with |H_M|=12, all other 717 points have at least 11 representations, each with a distinct second-slice t. Therefore deleting at most 10 points of the second 112-cap cannot create any new eligible third-slice point. If no modification to the first slice, a one-sided removal of <=10 points from the second slice cannot raise total above 236 within this family. The third slice still can contain at most 12 points, irrespective of internal line constraints.

This is a finite exact restricted theorem, NOT a global statement for all GL6 alignments, all 112-point caps, or other profiles such as 112+110+15. The entire 3812-matrix family is only a small subset of GL6(3). No >=237 construction, global bound, or novelty claim.

Reproduce: `python research/capset_f3_7/cap007k_cross_slice_resilience.py`; `python -m unittest discover -s research/capset_f3_7 -p 'test_cap007k_cross_slice_resilience.py' -v`. Python CI pending. Independent JavaScript count found exactly the cross-tab above. The independent checker does not assume any preexisting histogram, computes all 12544 pair sums for each matrix, checks total, zeros and positive minimum, and verifies deterministic expected output.

**Research decision:** The correct universal search primitive is the entire multiplicity vector r(z), not only hole count, Fourier overlap, or sample N(T). For arbitrary slice sizes S,T, candidate third slice is contained in zeros r(z), and deletion robustness is controlled by the low-r(z) tail. Follow-up: derive phase-sensitive global bounds on low multiplicity from cap-specific Fourier and classification, prove GL6 relative alignment double-coset coverage, and maintain an independent no-112-hyperplane branch. This experiment alone makes no progress on the global numerical upper bound; its value is a reusable structural diagnostic.
