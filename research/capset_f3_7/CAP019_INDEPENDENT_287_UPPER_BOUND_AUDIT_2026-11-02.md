# CAP-019 — Independent audit of Drive v6 claimed upper bound r₃(7) ≤ 287
**2026-11-02 · Dedicated branch research/capset-f3-7 · CPU-only exact integers · NEW CANDIDATE THEOREM, REFEREE PENDING**

## 1. Decision and scope
Read current Drive CAPSET_F3_7 ledger (latest CAP-016/017/018 v6.0 claims) and the dedicated GitHub STATE/LOG/BACKLOG/CI. Prior GitHub CAP-015S import and exact PSD CI are green. Drive v6.0 is newer than GitHub v5 and asserts a global bound of 287, stronger than the 288 bound claimed in Henry Thackeray's 2022 arXiv:2206.09804 preprint. A 2026 paper by Grace–Voloch still says exact cap sizes are known only up to dimension 6. Chose an independent, bounded, **no-GPU audit of the 287 claim**, rather than further restricted 236-witness perturbations.

Drive source files, preserved unchanged:
- v6 Python: https://drive.google.com/file/d/1GHVpOykFyXQYoS509BHV90GQyBBcJzxm/view ; SHA256 d269e26909fc89c533387a17cf8a07461f8fbf75b581986ff19e11343cfa4f3f
- v6 evidence JSON: https://drive.google.com/file/d/1W0oD_x_j9nlB98U6oDkFUOcouEMD1Mz3/view
- Independent verifier: `test_cap019_287_upper_bound_certificate.py`; exact 28-rank-case data: `CAP019_287_upper_bound_certificate.json`.
- Full local expanded audit `test_cap019_upper_287_certificate.py` ran six tests (including Fourier, 28 quadratic classes, 4 moments, a counterexample to an invalid intermediate claim); compact committed CI verifier ran two tests in 0.078s. No randomness, GPU, external optimizer, or paid compute.

**Important:** This is an independent integer-certificate audit with a mathematical proof outline below, NOT yet an independent specialist referee review of the full theorem. External 110-cap completion remains a 2022 preprint dependency. Do not represent the new 287 as a community-accepted published bound or as the exact r₃(7).

## 2. Proof architecture, with explicit assumptions

Let A ⊂ F₃⁷ be a hypothetical cap of M points. For every projective normal u (1093 directions), let (a,b,c) be the three affine hyperplane counts, sorted a≥b≥c. By Potechin 2008, a,b,c≤112; all 112-caps in AG(6,3) are affinely equivalent. By Thackeray 2022 (arXiv:2206.09804), every 110-cap in AG(6,3) is a 112-cap with two points removed, hence each ≥110 slice can be completed to a maximal 112-cap.

### 2a. Common-tangent slice lemma (CAP-017B), explicitly rederived
Complete two largest slices S₁′,S₂′ of sizes 112−d₁ and 112−d₂ to 112-caps S₁,S₂, with d=d₁+d₂≤4. By affine shear, simultaneously center S₁ and S₂. For a centered 112-cap, Fourier coefficients at nonzero frequencies are **−23** on 112 frequencies (56 projective directions), **+4** on the other 616. Let their dual high-frequency projective supports intersect in m* directions (0≤m*≤56). For z in F₃⁶ and m(z)=# common high-frequency directions orthogonal to z, Fourier inversion gives
```
r(z) = 16 − 16·1[z=0] + 4·(1_S1(z)+1_S2(z)) + 3m(z) − m*
```
where r(z)=#{(x,y)∈S₁×S₂:x+y=z}. This is an identity, not an assumption about an arbitrary orientation. For a point z in the third slice, absence of cross-slice triples after deleting d points implies r(z)≤d, since each deleted point removes at most one representation of any fixed z. For z≠0,
```
m(z) ≤ (m*−16+d)/3.
```
For each common high-frequency direction u, both completed 112-caps have slice counts (45,45,22) at levels (+1,−1,0). Two *disjoint* six-dimensional hyperplanes through the third slice, using (+1,+1,+1) and (−1,−1,−1) across the three main slices, have at most 112 points each. Therefore the third-slice +1 and −1 counts sum to at most 44+d, and its u=0 count is at least c−44−d. Double counting (z,u) with u·z=0 gives
```
m* (c−44−d) ≤ c(m*−16+d)/3,
c ≤ floor(3m*(44+d)/(2m*+16−d)).
```
If m*=0, r(z)≥16 for z≠0 and at most the single z=0 can be unblocked when d≤4, so c≤1. **Important deleted-point edge case:** if m*=56, the centered caps coincide; their full convolution has r(z)=1 on the 112 cap points, r(z)=20 on the other 616 nonzero points and r(0)=112. Although r(z)>0 everywhere *before* deletion, deleting up to d≤4 points can free at most d of the 112 singleton-representation points (each is a unique diagonal pair), so c≤d. Merely saying the full convolution has no holes is insufficient when d>0. For 1≤m*≤55, the double-count inequality applies and gives the **universal conditional** bound
```
c ≤ floor(165*(44+d)/(126−d)),  d=0..4,
values = [57,59,61,63,64].
```
The affine shear and the sign z→−z only permute third-slice coordinates; they do not affect counts or orthogonality. The canonical 112-cap was independently rebuilt from the 2-(6,3,2) block design; a second pure-Python implementation checked all 364 projective Fourier directions of H and H′ and the convolution identity at all 729 vectors, finding 12 cross holes. The universal lemma relies additionally on the published affine uniqueness theorem, not just this one numerical example.

### 2b. Exact moments and finite dual functional
For a cap, any three distinct points are affinely independent; for the 1093 directions,
```
Σ S₂ = 364M²+729M,
Σ S₃ = 121M(M−1)(M−2)+1092M(M−1)+1093M,
S_j=a^j+b^j+c^j.
```
Enumerate **all sorted triples** 0≤c≤b≤a≤112, a+b+c=M, excluding only those forbidden by the proven conditional tangent lemma when a,b≥110. The independent stdlib verifier checked respectively 186, 194, 202, 211 admissible triples for M=291,290,289,288. Exact nonnegative functionals Δ_M = α_M S₃ − β_M S₂ + γ_M:
```
M   (α, β, γ)                     Σ Δ_M
291 (631,174486,3197526333)     −3033966
290 (617,170139,3097556132)    −22713024
289 (302,83061,1502493511)     −20848032
288 (211,57752,1036689408)      +4557600
```
Every admissible profile has Δ_M≥0. Hence M=291,290,289 are excluded by moment sums alone, and M=288 needs extra residue information.

### 2c. Exact 288-cap exclusion: all 28 Gaussian-quadric classes
For M=288, let b=Σ_{x∈A}x ∈F₃⁷. A projective direction u is Type-0 iff u·b=0 (all three slice counts share the same residue r); otherwise Type-1 (residues 0,1,2). Type-0 common residue equals Q(u)=−Σ_{x∈A}(u·x)² mod3. If b=0: 1093 Type-0 directions, Q on F₃⁷; if b≠0: 364 Type-0 directions, Q restricted to a six-dimensional kernel, plus 729 Type-1 directions. Every quadratic form over F₃ is diagonalizable; all ranks and square classes were enumerated **independently by three-state exact dynamic programming**, giving 15+13=28 projective residue spectra.

The local finite inequalities independently checked on all 211 admissible profiles are:
```
Type0 residue 2:   Δ≥19362
Type1:             Δ≥6032+77·(S₂−27650)
Type0 residue 0:   Δ≥214·(S₂−27648)
Type0 residue 1:   Δ=0 only at (112,109,67), with S₂−27648=1266;
                   otherwise Δ≥16830.
```
The exact variance budget is **B = Σ(S₂−27648) = 182304**. The required moment sum is ΣΔ=4557600. The exhaustive rank-case lower bounds:
- b=0, Q rank≥2 or rank1(−): N₂≥243 ⇒ ΣΔ≥243·19362=**4704966**.
- b=0, Q rank0: ΣΔ≥214·B=**39013056**.
- b=0, Q rank1(+): N₁=729; at most floor(B/1266)=144 directions can attain zero Δ ⇒ ΣΔ≥(729−144)·16830=**9845550**.
- b≠0, Q rank≥2 or rank1(−): N₂≥81 and 729 Type1 directions ⇒ ΣΔ≥729·6032+81·19362=**5965650**.
- b≠0, Q rank0: Δ variance slopes 77 and 214 ⇒ ΣΔ≥729·6032+77·(B−1458)=**18322470**.
- b≠0, Q rank1(+): N₁=243; at most floor((B−1458)/1266)=142 zero-Δ Type0 residue1 directions ⇒ ΣΔ≥729·6032+(243−142)·16830=**6097158**.

Every lower bound strictly exceeds 4557600. The **minimum across all 28 cases is 4704966**. This yields the candidate global theorem r₃(7)≤287 conditional on the cited 110-cap completion and the common-tangent lemma.

### 2d. A genuine error in v6: fixed rather than hidden
The Drive v6 proof states a variance budget **185664** and multiplies it by **3016** in its rank0 argument. Both are invalid as written. Correct budget: **182304**. The proposed per-direction inequality Δ≥3016·(S₂−27648) is false: admissible profile (111,108,69) has S₂−27648=1098 and Δ=235188, but 3016·1098=3311568. The rank0 case is repaired by the *verified valid* slope **214**, and the Type1 slope **77**; all 28 cases remain excluded. The original v6 Drive files are unchanged and the correction is recorded explicitly rather than silently rewriting source evidence.

## 3. Commands, verification and remaining risk
```bash
python -m unittest discover -s research/capset_f3_7 -p 'test_cap019_287_upper_bound_certificate.py' -v
python research/capset_f3_7/test_cap019_287_upper_bound_certificate.py
```
Local committed-source equivalent: **2/2 PASS, 0.078 seconds**, CPU only. Expanded independent local verifier: **6/6 PASS, 0.067 seconds**. The exact 28-case spectrum was independently recomputed in JS before committing JSON; minimum matched Python 4704966. GitHub Actions conclusion must be checked separately; do not claim CI green until confirmed.

**Referee tasks before public mathematical claim:** (i) have a separate mathematician/agent audit the Fourier inversion, simultaneous affine shear and common-tangent double count; (ii) check the published Thackeray 110-cap theorem proof and its dependency chain, not merely the abstract; (iii) independently verify the finite certificate from its 211 profiles; (iv) check whether a ≤287 bound has already been circulated; (v) prepare formal standalone proof, optionally Lean. No global exact r₃(7) is proved: **236 ≤ r₃(7) ≤ 287 remains a provisional new bound pending referee**, not matching bounds.

## 4. Literature checked on 2026-11-02
- Aaron Potechin, *Maximal Caps in AG(6,3)*, Designs Codes Cryptography 46 (2008), 243–259; unique affine class of 112-caps. https://doi.org/10.1007/s10623-007-9132-z
- Henry Robert Thackeray, *The cap set problem: Up to dimension 7*, arXiv:2206.09804 (2022): 110-cap completion, no 289-cap; **preprint**. https://arxiv.org/abs/2206.09804
- Cassie Grace & José Felipe Voloch, *Algebraic Capsets*, J. Combinatorial Designs 34 (2026), 459–463: exact dimensions known only n≤6. https://doi.org/10.1002/jcd.70024
- Targeted November 2026 search did not locate an independent public 287 upper-bound proof. Absence of search hits is NOT a novelty certificate.

**Meta-audit:** This is higher global mathematical leverage than further local fixed-236 deletion experiments; it addresses *all* hyperplane profiles, including the previously neglected no-112-slice branch. The key remaining risk is theorem-level proof review, not computation. Next step: hostile independent referee of CAP-017B and 110-cap dependency, then formalized/peer-reviewable writeup. Do not terminate hourly research until a matching lower and upper bound establishes exact r₃(7).
