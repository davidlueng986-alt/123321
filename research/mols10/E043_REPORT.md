# E043 — All 14 noninitial four-row subsets of 156 six-row witnesses have exact fixed-prefix obstructions
Date: 2026-11-02 18:54 UTC. **GLOBAL 3-MOLS(10) STATUS: OPEN. 0/162,959 complete normalized orbits excluded.**

## Objective
E039 had already checked the first four rows of each of 156 E036 six-row partial 3-MOLS witnesses. E042 showed no marginal pruning from three transported forbidden motifs. E043 instead examines the 14 *other* four-row subsets of each six-row witness: 156 × 14 = **2,184 ordered fixed prefixes**, pairwise distinct as arrays. These are not complete orbit exclusions.

## Exact result
Each of 156 source witnesses was independently checked as three 6×10 partial Latin squares with all three overlays containing 60 distinct pairs. Each of 2,184 selected 4×10 prefixes is valid (all three 40/40/40 overlays). The residual exact-cover relaxation ignores which of the six remaining rows receives a cell; it uses six resource classes: P_AB, P_AC, P_BC and C_A, C_B, C_C, with 360 required demands per prefix. Every genuine ten-row extension must satisfy these constraints.

Full six-class LP scan: **184 exact zero-support**, **2,000 numerical HiGHS infeasible**, 0 feasible, 0 UNKNOWN; 8.67 s CPU. Numerical LP statuses are not proof. Separate exact integer Farkas dual generation succeeded for **all 2,000**: for each certificate integer weights y obey sum(y)>0 and sum of six weights for every permitted placement ≤0. A separate Node.js integer-only verifier rebuilt all resource demands and 870,931 allowed placements and checked **2,184/2,184 PASS**; min dual RHS +1, maximum candidate score -6. Corrupted dual weights were rejected with "positive candidate dual 0". Exact positive primal controls: affine triples over F_5/F_7/F_11, **370/370** four-row subsets, 26,170 residual cell placements, PASS.

An initial unbatched dual generation run was interrupted after ~600 cases and was not counted; eight bounded disjoint batches produced the full 2,184 exact certificates. All 2,184 ordered four-row prefix arrays are distinct; no isotopy-class uniqueness claim.

## Interpretation and limitations
This is a collection of *conditional* exact nonextension certificates, not a universal theorem on all order-10 four-row prefixes, not a proof of nonexistence, and not a 100/100/100 construction. Six-row partial triples can exist despite the impossibility of extending their particular four-row subsets to ten rows. Combining with E039's 156 first-four-row obstructions gives 2,340 sampled fixed-prefix obstructions from the 156 witnesses, not exhaustive prefix or orbit coverage. **0 / 162,959 full orbits excluded.**

## Reproducibility and artifact status
Local full bundle `E043_MOLS10_RESEARCH_BUNDLE.zip`, SHA256 `f24a39e547d62d7ec55b054a9c61127d6742835d23918d05d86485e15d8a4538`, includes E036_WITNESSES.json, SciPy scan/generator, 2,184 exact certificates, standalone JS verifier, positive controls, mutation output, input hashes and replay README. Full exact data SHA256 `7d5115f5dda74f59f7263965f265281d25f9f3cf7bd862c83c5b57a3a748fc4f`. **The binary bundle is NOT stored in this repository**; available as this conversation's generated attachment. Google Drive binary upload attempted but blocked by BLOCKED_FILE_REFERENCE; do not claim it uploaded. This GitHub report records scope, counts and audit evidence but cannot substitute for full certificate bytes. Independently reproducible zero-support example: E036 witness index 0, rows (0,2,3,4), uncovered required demand P_AC(5,0).

Reproduce from E036 source: for each orbit 0..155 and each four-element subset of {0,...,5} other than (0,1,2,3), construct residual placements (column c and symbols a,b,d) absent from fixed columns and three fixed pair overlays. Test all six demand classes; if support is nonzero, solve LP A x=1, x≥0; for numerical infeasible cases optimize dual y with Aᵀy≤0, y∈[-1,1], then set integer w_i=floor(scale*y_i+1e-9)-1 and *directly* verify sum(w)>0 and max_t Σ_{i∈t} w_i≤0. Scale used: 30 in 1,810 cases, 100 in 190. Integer verifier must check every allowed placement, not trust solver status.

## Literature (fresh check 2026-11-02)
- Bright–Keita–Stevens, EJC 33(1) P1.30 (2026-02-13), https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 — restricted 4×4 subsquare study.
- Barnoff–Bright, arXiv:2605.02132v2 (revised 2026-07-04), https://arxiv.org/abs/2605.02132 — hybrid SAT for orthogonal pairs.
No independently checkable complete unrestricted solution located; search absence is not a proof.

## Next
Seek a genuine legal k4 prefix that passes full six-class LP using structurally different random/constraint-guided generation, then invest in symmetry-complete proof-producing SAT with independent certificates. Avoid E042 costly low-benefit motif matching.