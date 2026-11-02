# CAP-020 — Antipodal secant separation and a stricter common-tangent lemma
**2026-11-02 14:54–15:?? UTC · exact CPU-only · theorem-level combinatorial proof plus finite witness census · novelty NOT established**

## 0. Research decision and provenance
Read the live dedicated Google Drive Ledger, folder, GitHub STATE/LOG/BACKLOG, recent commits and all-green CAP-019 CI before choosing this experiment. CAP-019 proposes a **provisional** global upper bound 287 (not a published accepted result), and its most valuable outstanding issue is a hostile proof review of CAP-017B. This run tests a nontrivial independent structural strengthening of CAP-017B rather than repeating the 28-case certificate.

Fresh literature check (2026-11-02): Potechin, *Maximal caps in AG(6,3)*, DCC 46 (2008), proves 112 and uniqueness up to affine equivalence; Thackeray, arXiv:2206.09804v1 (2022), Theorem 3.9 explicitly asserts every 110-cap is a 112-cap minus two points (preprint; proof uses extensive lower-dimensional classification and computer checks); Grace–Voloch, *Algebraic Capsets*, JCD (published 2026-05-21), says exact values known only n<=6. Public dimension-7 trackers still list 236<=r3(7)<=291 and separately flag preprint <=288. Search did not establish priority/novelty of the present antipodal lemma. References:
- https://doi.org/10.1007/s10623-007-9132-z
- https://arxiv.org/html/2206.09804 (Theorem 3.9, §3)
- https://doi.org/10.1002/jcd.70024

## 1. General antipodal-secant lemma (elementary, not computational)
Let H ⊂ F_3^n be a cap with H=-H and 0∉H. For any nonzero z, let E_z be the family of unordered distinct pairs {x,y}⊂H satisfying x+y+z=0.

**Lemma.** All 2|E_z| endpoints are in *different* antipodal orbits {x,-x}. In particular, the E_z edges are pairwise disjoint.

**Proof.** For fixed x,z the other endpoint y=-z-x is unique, so distinct edges have no shared endpoints. Suppose an antipodal collision: an endpoint x of {x,y} and an endpoint -x of {-x,w} occur (including the possibility that both are on one edge). We have y=-z-x and w=-z+x. Since H=-H, the three points x, -y=z+x, w=x-z all lie in H. For z≠0 they are pairwise distinct: each equality would force z=0 in F_3. Their sum is x+(z+x)+(x-z)=3x=0, a forbidden nontrivial 3-term progression. Contradiction. QED.

**Corollary (antipodal deletion cost).** Let H'⊂F_3^n be a second cap with H'=-H'. If z∈H'\H, z≠0, then D=H\H' must hit each E_z edge. Because D=-D and no two E_z endpoints belong to the same antipodal orbit, D contains at least |E_z| entire antipodal orbits, hence **|H\H'| ≥ 2|E_z|**. The factor 2 is essential: a naive unstructured deletion bound only gives |H\H'|≥|E_z|.

## 2. Exact canonical 112-cap certificate
The known centered canonical 112-cap H⊂F_3^6 is built from the 10 cyclic 3-subsets of a 2-(6,3,2) design (10×8=80 ternary weight-3 points) plus the 32 even-parity full-support sign vectors, totaling 112. The standalone script independently verifies size112, no 3AP, H=-H, 0∉H, and counts every one of the 6216 unordered pairs.

Exact secant histogram over all 729 points z:
- z∈H (112 points): 0 distinct-point secants (the convolution has one diagonal representation);
- z=0 (1 point): 56 distinct-point secants, each an antipodal pair; **the general lemma explicitly excludes z=0**;
- z∉H∪{0} (616 points): exactly 10 secants each, with 20 endpoints in 20 distinct antipodal orbits.

A non-orthogonal invertible shear x↦(x0+x1,x1,x2+x3,x3,x4,x5) independently reproduces the histogram and orbit separation. A direct 364-projective-direction signed Fourier check on H and the sheared cap confirms 56 high directions each and 20 common high directions for this test pair; the two primal 112-caps intersect in 40 points. **The updated verifier additionally checks the entire high-direction sets**, not just their counts: D(H)=projectivization(H), and D(AH)=projectivization(A^{-T}H) for the shear. This establishes the needed finite Fourier self-duality premise for the canonical representative without relying on source-agent assertions.

Since Potechin proves that every maximal112 cap is affinely equivalent to H, and 112≡1 mod3, its barycenter b=Σ_{x∈S}x is exactly its affine translation center. After subtracting b, every maximal112 cap is a linear image of H and is centrally symmetric, avoids zero and has the same 10 secants at every nonzero outsider.

**New restricted structural consequence:** for any two *distinct centered* 112-caps H1,H2⊂F_3^6, choose z∈H2\H1 (nonzero); then
```
|H1\H2| >= 20,   |H1∩H2| <= 92.
```
The same applies to their Fourier high-frequency supports D1,D2: each is a centered maximal112 cap (linear contragredient image of H). Therefore their projective high-frequency intersection size m* satisfies **m*≤46**, or m*=56 when D1=D2. No values 47,…,55 are possible. This is a *rigorous consequence of Potechin uniqueness + the independently certified canonical secant count*, not a claim of novelty.

## 3. Refinement of CAP-017B
CAP-017B proves for d=d1+d2≤4 and distinct completed 112-caps, with common high-direction count m*:
```
c <= floor(3*m* (44+d) / (2*m*+16-d)).
```
For 3≤m*≤46 the right side increases with m*, hence substitute 46 instead of the previous worst-case 55. For m*≤2, its existing exceptional z=0 proof gives c≤1. For m*=56 (identical dual caps), existing CAP-019 special-case argument gives c≤d, and the refined numeric bounds below still hold.

| d | previous CAP-017B c bound | CAP-020 refined c bound |
|---|---:|---:|
|0|57|**56**|
|1|59|**58**|
|2|61|**59**|
|3|63|**61**|
|4|64|**63**|

The improved lemma is independent of the Thackeray 110-completion theorem **once the two slices are already known to be contained in 112-caps**. Applying it to arbitrary 110/111 slices still inherits the separate completion dependencies.

## 4. Independent verification and limits
```bash
python research/capset_f3_7/test_cap020_antipodal_secant_gap.py
python -m unittest discover -s research/capset_f3_7 -p 'test_cap020_antipodal_secant_gap.py' -v
```
Local Python 3 stdlib: **5/5 PASS in 0.157s**, no randomness, no GPU, no paid compute, no external solver. A failed *scratch* Fourier assertion during exploratory work was due to comparing a list [22,45,45] with a tuple (22,45,45), not a mathematical counterexample; corrected and reran successfully (56+56 high directions, 20 common for the shear). The zero-vector secant exception is covered by a negative-control test.

**No new global upper bound:** Independently recomputed admissible sorted slice-profile sets for M=291,290,289,288,287 using the old vs refined bounds: both give exactly 186,194,202,211,219 profiles respectively. This refinement helps smaller-M profile searches but **does not strengthen CAP-019's candidate r3(7)≤287** or solve r3(7).

**CI caveat:** Local tests are green; check the newly triggered GitHub Actions conclusion separately. CAP-019 earlier CI is already green, but a green finite-certificate CI is not a full theorem referee.

## 5. Meta-audit and next action
This run strengthens the previously loose common-tangent proof and removes a previously unexploited m*=47..55 branch without any GL(6,3) enumeration. However, it does not address the dominant balanced/no-112-slice regime at M≈236–287, so its immediate global leverage is limited. Do not keep spending runs optimizing 112-conditioned bounds unless they tighten a finite global certificate. Next P0: hostile independent review of CAP-017B affine/Fourier assumptions and the Thackeray 110-completion dependency; then target new 5D codimension-two moments/constraint cuts that actually restrict the balanced regime. No >=237 witness, no matching upper/lower bound; r3(7) remains OPEN.
