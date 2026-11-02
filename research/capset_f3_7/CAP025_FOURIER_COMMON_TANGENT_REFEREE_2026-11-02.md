# CAP-025 — Hostile referee of CAP-017B Fourier/common-tangent premise
**2026-11-02 ~19:51–20:00 UTC · CPU-only, exact F3 integer arithmetic · no new global bound**

## Research continuity and source checks
Read the current dedicated Drive ledger/folder, branch STATE.json/LOG.md/BACKLOG.md, recent commits and CI. CAP-024 commit `12726ec3c6` has **complete GitHub Actions SUCCESS** (run 41505596201). Previous CAP-019 proposed a **provisional** 287 global upper bound, which hinges on the universal CAP-017B Fourier/common-tangent lemma and Thackeray's 110-cap completion. Rather than repeating anchored-111 grid relaxations, this run independently checked the *theorem premise* and located its exact proof dependencies.

Primary sources checked on 2026-11-02:
- Henry (Maya) Robert Thackeray, arXiv:2206.09804v1, **Theorem 3.9** (every 110-cap in AG(6,3) extends to 112), **Proposition 4.1** (stronger 112/112 and 222-combined slice bounds), and **Theorem 4.2** (no 289-cap). https://arxiv.org/html/2206.09804
- Potechin (2008), *Maximal Caps in AG(6,3)*, DOI https://doi.org/10.1007/s10623-007-9132-z, uniqueness of affine 112-cap.
- Grace & Voloch, *Algebraic Capsets*, published May 21, 2026, https://doi.org/10.1002/jcd.70024; exact n=7 remains unresolved.
- Public status tracker https://cairn-commons.com/problems/cap-sets-dim-7 (as of 2026-10-03: published 291, preprint 288, best known 236).
No public priority claim for an independently reviewed 287 upper bound was located. Search non-detection does not establish novelty.

## Independently derived universal Fourier identity (conditional on Potechin classification)
For a **centered** 112-cap `S` in `F3^6`, the canonical block-design representative `H` has Fourier transform `F_S(0)=112` and, for nonzero frequencies `u`, `F_S(u)=-23` on 112 vectors (56 projective directions) and `+4` on the other 616 vectors. A linear image has the same pattern with contragredient dual support; no assumption that two caps have identical orientations is needed. Both are centrally symmetric, so the transform is real.

For centered `S,T`, let `D_S,D_T` be their 56 projective negative-Fourier supports, `I=D_S∩D_T`, `m=|I|`, and `m(z)=|{u∈I:u·z=0}|`. Inverse Fourier, using `Σ_{u≠0}χ_u(z)=729δ_{z0}−1`, `Σ_{u∈D_S^{±}}χ_u(z)=4−27·1_S(z)` for `z≠0`, and `Σ_{u∈I^{±}}χ_u(z)=3m(z)−m`, yields the **exact pointwise identity**
```
r(z) = #{(x,y)∈S×T:x+y=z}
     = 16−16·1[z=0]+4·1_S(z)+4·1_T(z)+3m(z)−m.
```
At `z=0`, `r(0)=2m=|S∩T|`. This follows from the actual affine duality of the canonical 112-cap and its GL images, **not** from a floating SVD or a sample-alignment assumption.

**Affine centering check.** If the two main 7D layers have affine centers `b0,b1` at layer coordinates `t=0,1`, the invertible affine shear `x↦x−b0+t(b0−b1)` centers both. The third layer shifts by `b0+b1` in F3. This preserves all three-point collinearity relations and the third-layer size. Thus the Fourier lemma is legitimately applicable to arbitrary affine 112-completions.

## Common-tangent double count independently rederived
If the actual two largest slices are obtained from completed 112-caps by `d=d1+d2≤4` deletions, a third-slice point `z` must satisfy `r(−z)≤d`; each removed endpoint destroys at most one representation of a fixed target. Since `m(−z)=m(z)`, the sign is immaterial for orthogonality. For `3≤m≤55`, `r(0)=2m>d`, and every admissible third-slice point is nonzero with
```
m(z) ≤ (m−16+d)/3.
```
For every `u∈I`, the two completed 112-slices have 45 points at each of `u·x=±1`. The two corresponding **disjoint affine 6D hyperplanes in the full 7D ambient space** each contain ≤112 cap points. Therefore the third slice has at least `c−44−d` points with `u·z=0`. Counting orthogonal pairs `(u,z)` two ways gives
```
m(c−44−d) ≤ c(m−16+d)/3
(2m+16−d)c ≤ 3m(44+d).
```
For `m=0,1,2`, all nonzero `z` have `r(z)≥16−m>d`, so at most the exceptional origin can survive (`c≤1`). For `m=56`, the completed duals coincide and `r(z)=1` on their 112 cap points, `20` on other nonzero points and `112` at zero; deleting `d≤4` endpoints can create at most `d` holes (`c≤d`). These are the exceptional branches that a careless generic division misses.

**Additional exact small-overlap corollary (conditional, not a new global bound):** for `d≤4` and `3≤m≤15−d`, every nonzero `z` has `r(z)≥16−m>d` and `r(0)=2m>d`; hence **c=0**. This is sharper than the coarse tangent bound on those specific overlaps and is consistent with earlier CAP-009A zero-hole work. It does not alter the worst-case global profile dual at M288.

## Independent exact finite arithmetic (separate from prior Python tests)
Committed `cap025_fourier_referee.js` constructs the canonical 112-cap from 10 triples and 32 full-support vectors; independently checks the cap property; computes the complete 364-projective-direction Fourier spectrum of **each** cap; computes the 112×112 convolution by direct pairs; and checks the symbolic formula at **all 729 target vectors** for each of six cap pairs. The pairs include the classical dual complement, two nonorthogonal shears, a sign change, and two independently transformed caps.

| Pair | common negative projective directions m | primal intersection | convolution holes |
|---|---:|---:|---:|
| H / H | 56 | 112 | 0 |
| H / H' | 16 | 32 | 12 |
| H / T1(H) | 18 | 36 | 0 |
| H / T2(H) | 17 | 34 | 0 |
| H / T3(H') | 16 | 32 | 12 |
| T1(H) / T2(H') | 10 | 20 | 0 |

All **4,374** pointwise convolution comparisons passed (6×729), all six 364-direction Fourier censuses passed, and every pair satisfied `|S∩T|=2m`. In the `m=56` exceptional branch, deleting exactly `d=0,1,2,3,4` selected distinct cap points from the two layers produced respectively **0,1,2,3,4** holes, verifying the subtle `c≤d` exception. All operations are exact mod-3 integers; no RNG, external solver, GPU or paid compute.

Command (Node 20+ on standard Ubuntu GitHub runner):
```bash
node research/capset_f3_7/cap025_fourier_referee.js
python -m unittest discover -s research/capset_f3_7 -p 'test_cap025_fourier_referee.py' -v
```
The direct V8 execution of the exact same `audit()` source returned PASS on all checks. The Python wrapper is committed for GitHub CI; **CI outcome must be confirmed on the final commit**, not inferred from the earlier CAP-024 green run.

## Hostile-referee conclusions / boundaries
- **No Fourier counterexample found; symbolic CAP-017B double-count derivation checks out**, provided the canonical Fourier spectrum and affine uniqueness hold. Six finite tests are **not** an exhaustive GL(6,3) proof; the universal statement follows instead from the symbolic Fourier transform and Potechin affine classification.
- **Remaining external dependency is significant:** Thackeray Theorem 3.9 is a 2022 preprint with computer-assisted classification steps; this run read its actual theorem/proof (not only its abstract) but did **not** independently reproduce its 5D classification or Java searches. Therefore CAP-019 `r3(7)≤287` remains **provisional pending separate full mathematical referee**.
- Thackeray Proposition 4.1 already gives third slice ≤34 for 112+112 and ≤55 when two slices total ≥222, stronger than the coarse CAP-017B numerical bounds for d=0,1,2; do not claim those coarse numbers novel.
- The global balanced/no-111 branch and lower-bound 237 search are still open. This run found **no ≥237 witness, no stronger certified numerical bound, and no exact r3(7)**.

## Next priority
Referee Thackeray's 110-completion dependency with independent computational certificates; then strengthen global 287 anchored111 SAT with proof-logged point-level constraints, and in parallel address balanced/no-111 configurations near 237. Do not promote local fixed-anchor results to a global upper bound.
