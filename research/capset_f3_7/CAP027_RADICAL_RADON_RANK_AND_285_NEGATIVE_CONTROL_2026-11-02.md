# CAP-027 — Radical Radon p-rank and exact 285-point count-only negative control
**2026-11-02 ~21:48 UTC | exact CPU only | Python 6/6 + independent Node PASS | GitHub CI pending | r3(7) OPEN**

## Continuity, literature and claim scope
Read the current CAPSET-F3-7 Drive Ledger/folder, GitHub STATE/LOG/BACKLOG, recent commits and Actions. Final CAP-026 head `e2b8f3238cdd` has successful CI run 41524558297. Sources checked 2026-11-02: Thackeray 2022 arXiv:2206.09804 (110-cap completion and preprint bound 288), Potechin 2008 (112-cap uniqueness), Grace–Voloch 2026 *Algebraic Capsets* (exact dimensions only n<=6), public n7 tracker 2026-10-03 (open). Classical affine-incidence p-rank methods are known; **novelty not established**.

## Conditional structural consequence of CAP-026
Suppose A⊂F3^7 is a hypothetical 285-cap with every affine 6D section <=109. CAP-026's independently finite-checked necessary theorem gives barycenter b≠0 and Q(u)=−Σ_{x∈A}(u·x)^2 of anisotropic rank2 on b-perp. Thus the radical W=rad(Q|b-perp) is a **4D vector subspace**; because x1²+x2² is anisotropic over F3, the Q-zero directions in b-perp are **exactly** PG(W), all 40 projective directions (not an arbitrary 40-set).

For every nonzero u∈W, the three affine slice sizes n0,n1,n2 obey, mod3,
```
n0+n1+n2=|A|=0,
n1−n2=u·b=0,
n1+n2=−Q(u)=0.
```
Hence **all three n_j are divisible by 3**. This is an exact congruence for 120 affine 6D sections.

Project along W to the quotient F3^7/W-perp ≅ F3^4. Each of its 81 fibers is an affine 3-flat, with size f(t)≤r3(3)=9. The 120 constraints are
```
Σ_{t:u·t=s} f(t) ≡0 (mod3),  u∈PG(3,3), s=0,1,2.
```
For each of the [4 choose 2]_3=130 two-dimensional normal subspaces U⊂W, the nine affine 5D cells form a 3×3 grid g(i,j), each cell ≤r3(5)=45. All 12 affine line sums vanish mod3. The F3 rank of the 12×9 incidence matrix is 6, so **exactly** the 3-dimensional kernel
```
g(i,j) ≡ a+b*i+c*j (mod3), a,b,c∈F3
```
is allowed. This is a solver-ready necessary per-grid residue constraint, not a cap construction.

## Exact Radon p-rank: why these constraints alone are weak
For k=2,3,4 let R_k be the affine hyperplane incidence matrix over F3, with 3(3^k−1)/2 rows and 3^k columns. Each row is
```
1[u·t=s]=1−(u·t−s)^2 (mod3).
```
Rows span the degree≤2 polynomial evaluations: sums/differences across s generate constants and linear terms, and polarization of squares generates cross terms. The degree≤2 monomials are independent functions on F3^k. Thus rank R_k=binom(k+2,2): **6,10,15**. Independent literal Gaussian elimination confirms all three values. For k=4, the 120×81 matrix has rank15 and **nullity66**: radical hyperplane congruences alone cannot rigidify 81 fiber counts.

## Exact falsification: count-only 285 fiber assignment
Let P[0..80] enumerate F3^4 lexicographically, E={t:t0=t1=0} (9 points), S={P[7i mod81]:0≤i<11} (11 points), and set
```
f(t)=3+1_E(t)+3*1_S(t).
```
Independent Python and Node.js exact calculations verify:
- Total Σf=285; fiber histogram {3:63,4:7,6:9,7:2}; all fibers ≤7<9, but **not all fiber counts divisible by3**.
- All **120** W-normal affine 6D sections have sizes **84..108**, all divisible by3 and ≤109.
- All **1,170** affine 5D cells over **130** normal 2-planes have sizes **27..45**, respecting the exact 5D cap bound45.
- All 130 3×3 grids have affine-linear residue patterns mod3.

**This is NOT an actual 285-point cap.** It is an integer relaxation only: no 3D fiber point sets, cross-fiber 3AP compatibility, remaining 324 Q-nonzero b-perp directions or 729 Type1 directions are represented. It falsifies the tempting inference that radical constraints force individual 3D fibers to be divisible by3, and shows that adding all 130 codim2 count-only grids and local 3D/5D cap-size bounds still cannot exclude 285.

## Reproduce and strategy audit
```bash
python -m unittest discover -s research/capset_f3_7 -p 'test_cap027_radical_radon.py' -v
node research/capset_f3_7/cap027_radon_independent.js
```
Local Python **6/6 PASS** (~0.19s), independent Node PASS. No random seed, GPU, paid compute, external solver or unpublished witness. The attached JSON records deterministic inputs/results; new GitHub CI must be checked before calling the branch fully green.

**Meta-audit:** Stop trying to exclude 285 by radical p-rank + 3×3 count-only bounds alone; explicit negative control survives. Next: exact point-level cross-fiber 3AP and proof-logged SAT; full rank2 Q pattern across the other 1053 directions; independent Thackeray computer-assisted 110-completion referee and CAP019 provisional <=287; balanced/no-111 regime and >=237 witness work. No new accepted bound, no >=237 cap, and exact r3(7) remains OPEN.
