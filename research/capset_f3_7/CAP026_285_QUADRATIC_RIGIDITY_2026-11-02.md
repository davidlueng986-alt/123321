# CAP-026 — Exact quadratic rigidity at the 285-point slice-forcing boundary
**2026-11-02 20:xx UTC · deterministic CPU-only · 4 local unit tests PASS · GitHub CI to be checked · no new global upper bound**

## Continuity, selection and external literature
Read the current dedicated Google Drive Ledger and folder, GitHub `STATE.json`, `LOG.md`, `BACKLOG.md`, recent commits and CI. CAP-025 head `8e3b5416f1` has final GitHub Actions **SUCCESS** run 41514324725. Literature rechecked: Thackeray, arXiv:2206.09804 (2022, preprint), proves 110-cap completion and no 289-cap; Potechin (2008) classifies 112-caps; Grace–Voloch (2026) says exact sizes only known for n≤6; Cairn Commons 2026-10-03 lists 236≤r3(7)≤291, with preprint claim ≤288. Targeted searches did not establish priority/novelty for this specific 285-point rigidity statement. No claim of published novelty.

**Research decision:** CAP-021 already proved unconditionally that every cap of size ≥286 has a ≥110-point affine 6D slice. It also exhibited a *formal* 285-point direction histogram with all slices ≤109, showing ordinary second/third moments alone cannot lower that threshold. We test whether the exact barycenter/quadric residue law eliminates that 285-point countermodel. It eliminates all but one quadratic rank class, but **does not prove a stronger slice-forcing threshold**.

## Precise unconditional structural theorem
Let `A⊂F3^7` be a hypothetical **285-point cap** whose every affine 6D hyperplane has ≤109 points. Write `b=Σ_{x∈A}x∈F3^7`. Then:

1. **b≠0**.
2. On the 6D vector hyperplane `b^⊥`, the quadratic form
   `Q(u)=−Σ_{x∈A}(u·x)^2 (mod 3)` has **rank exactly 2 and anisotropic type**, equivalent to `u_1²+u_2²` with four zero directions.
3. Among its 364 projective normals, the exact Q-value counts are `(N0,N1,N2)=(40,162,162)`. The other 729 projective normals are Type-1 (all three affine slice counts have different residues modulo 3).

This is a **necessary** condition on hypothetical caps, not a 285-point construction or a new numerical upper bound. It uses only r3(6)≤112 indirectly through the imposed max109 hypothesis; the finite proof below requires **no 110-cap classification, no Thackeray theorem and no CAP-017B common-tangent lemma**.

## Self-contained exact proof
For each of the 1093 projective directions `u`, let the sorted affine slice sizes be `t=(a,b,c)`, `a+b+c=285`, `a≤109`. There are exactly **169** possible sorted triples. Let `S2(t)=a²+b²+c²`, `S3(t)=a³+b³+c³`. For any 285-cap, exact incidence counting gives
```
Σ_u 1=1093
Σ_u S2=29,773,665
Σ_u S3=2,860,326,405.
```
Let `B=Σ_{x∈A}x` (capital B to avoid conflict with the slice count `b`). Since 285≡0 mod3, the residues of the three slice counts are either all equal (**Type-0**, precisely when `u·B=0`) or are `{0,1,2}` (**Type-1**). On Type-0 directions, their common residue is `Q(u)=−Σ_x(u·x)² mod3`. Define `I_j(t)=1` when all three slice counts are `j mod3`, and `I_T(t)=1` for Type-1.

**Exact finite certificate, independently checked on all 169 triples:**
```
F2(t)=1176 I_2(t)+71,449,749−4064 S2(t)+15 S3(t) ≥0, Type-0 only
F1(t)=1176 I_1(t)+ 4,792,275− 272 S2(t)+   S3(t) ≥0, Type-0 only
F0(t)=S3(t)−271 S2(t)+4,765,200−28 I_T(t)−78 I_0(t) ≥0, all profiles.
```

If `B=0`, all 1093 directions are Type-0. Summing F1 and F2 yields:
```
1176 N1 ≥ 153,900 => N1 ≥ 131
1176 N2 ≥ 702,828 => N2 ≥ 598.
```
But the complete quadratic-form spectrum census in seven variables has 15 rank/sign classes. Rank zero or rank-one(+): N2=0; rank-one(−): N1=0; every rank≥2 has N2≤486. All 15 are impossible. Thus **B≠0**.

If `B≠0`, exactly 364 projective directions satisfy `u·B=0` and 729 are Type-1. Summing F0 yields
```
78 N0 ≤ 6,378 => N0 ≤ 81.
```
The 13 rank/sign classes of quadratic forms on the six-dimensional space `B^⊥` have N0≥94 **except** the rank-2 anisotropic class `diag(1,1,0,0,0,0)`, with N0=40. Its complete spectrum is (40,162,162). This proves the theorem. Every rank/sign spectrum is verified two independent ways: a three-state exact recurrence and brute-force enumeration of all projective vectors in F3^6 and F3^7.

## Crucial negative control — why this is not 285→110
The following **formal integer direction histogram**, NOT a realizable cap or a compatible assignment to 1093 actual geometric directions, satisfies the three global moments, the Type-0/Type-1 count and the surviving rank-2 Q spectrum:
```
(109,109,67) ×152
(100,95,90) ×1
(99,98,88)  ×1
(99,94,92)  ×1
(99,93,93)  ×1
(98,95,92)  ×1
(97,94,94)  ×10
(96,96,93)  ×39
(96,95,94)  ×726
(95,95,95)  ×161
```
These 1093 profiles have exactly S2=29,773,665 and S3=2,860,326,405; category totals `Q0=40,Q1=162,Q2=162,Type1=729`. Consequently **global S2/S3 + barycenter quadric value counts cannot exclude all 285-point max109 models**. No 285-point cap is claimed.

## Reproduction and scope
Committed verifier: `test_cap026_285_quadratic_rigidity.py`.
```bash
python -m unittest discover -s research/capset_f3_7 -p 'test_cap026_285_quadratic_rigidity.py' -v
python research/capset_f3_7/test_cap026_285_quadratic_rigidity.py
```
The locally developed equivalent stdlib checker passed **4/4 tests in 0.044s**, with 169-profile exhaustive inequality checks, 28 quadratic-form spectra cross-checked by brute force, the exact formal negative control, and an **independently reconstructed 236-point cap** verified against all 27,730 unordered pairs. GitHub source also compares its independent witness against the committed `candidates/calderbank_fishburn_236.txt`. Deterministic, no random seed, GPU, solver or paid compute. **GitHub CI status is separate and must be checked on final commit.**

## Meta-audit and next direction
The previous CAP-021 285-point moment-only negative control is genuinely defeated by barycenter Type counts, but a stronger *rank-2 anisotropic* negative control survives. This is progress in identifying exactly what aggregate moment arguments fail to capture, **not** a new cap bound. Further aggregate moment LPs without codimension-two geometric compatibility are likely low-yield. For global exact r3(7), prioritize (1) independent Thackeray 110-cap completion reproducibility and CAP-019 candidate ≤287 referee; (2) proof-logged anchored111/110 SAT point-level constraints; (3) the no-111-slice balanced branch; (4) ≥237 witness search with independent pairwise checker. No matching lower/upper bound, exact r3(7) remains OPEN.
