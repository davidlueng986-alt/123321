# CAP-055 — True anchored Lasserre level-2 implementation and direct closure attempt

**Research date:** 2026-11-08 (local). **Target:** determine the exact maximal three-term-progression-free cap size in `F3^7`, currently OPEN. **Final outcome:** **NOT DONE (ATTEMPTED)**. There is **no** valid >=237 cap and **no** independently checkable global proof that 237-caps do not exist. No numerical bound or major mathematical novelty is claimed.

This work continues CAP-052's genuinely root-equivalent dense 6-flat centred normalization and addresses CAP-054's weak level-1 PSD no-go, rather than re-running H3's conditional order-5 automorphism branch. It does not restart the disabled hourly research automation, touch MOLS10, or upload any External Advisor Brief.

## Root equivalence

Suppose a cap of **exactly 237** points exists in F3^7 (any cap of >=237 points contains one). By CAP-052's exact geometric normalization, one can assume 11 fixed included points, 52 fixed excluded points and 2,124 free points. The fixed dense 6-flat H has 10 included, 42 excluded and 677 free points; it must contain at least 89 selected points total, hence at least 79 free selected points. Around a fixed excluded centre q=0 in H, at least seven selected antipodal pairs are required. Four such pairs are fixed by the anchors; the other three are to be found among 331 compatible remaining pairs (2 fixed/free and 329 free/free). The full set of 796,797 F3^7 affine lines yields exactly 55,554 tautological clauses, 11,475 *binary* forbidden pairs of free points and 729,768 *ternary* forbidden triples of free points. A 237-cap in this normal form must select **exactly 226 free points**.

## Actual true degree-2 Lasserre / SOS model

For each squarefree set S of free points of degree <=4, let y_S be a formal moment, with y_empty=1. Define the level-2 Boolean moment matrix

`M2[S,T] = y_(S union T)` for `|S|,|T| <=2`, and require `M2 >= 0`.

All y_U whose monomial U contains a forbidden binary pair or forbidden 3AP triple are identically zero, **including every degree-four extension**. This directly encodes `E[x_a x_b x_c]=0` and `E[x_a x_b x_c x_d]=0` for every forbidden line, not just a weak first-moment inequality `E[x_a+x_b+x_c] <=2`.

For the **exact** selection size 226 among free points, impose the whole Boolean ideal of cardinality equalities

`sum_(i free and i notin S) y_(S union {i}) = (226-|S|) y_S`

for **all** admissible `|S|<=3`. The prior simplification `sum_i y_i=226` alone is not the full cardinality localizer and is materially weaker. The 6-flat condition is the positive semidefinite localizing matrix `L_H[S,T]=E[x_S x_T (sum_{i in Hfree} x_i -79)]` for `|S|,|T|<=1`. The centred antipodal-pair condition is the PSD localizer `L_pair[S,T]=E[x_S x_T (sum_{viable pairs} x_a x_(-a) -7)]` after substitution of fixed points. Under substitution, its polynomial has constant -3, two linear and 329 quadratic terms. All coefficients, line partitions and sample localizer entries were generated exactly in `cap055_global_anchored_l2.py`.

**Soundness:** Every true normalized 237-cap produces a rank-one moment matrix and all the required localizers. Therefore an independently checked negative-one SOS dual certificate for this model would prove no 237-cap and, with the existing verified 236 witness, close the root at r3(7)=236. An SDP numerical solver declaring infeasibility without rational certification is not enough.

## Actual execution and results

1. `cap055_global_anchored_l2.py` generates the **whole global line ideal** without dropping 3AP constraints and exposes a lazy moment / localizer operator for arbitrary squarefree terms up to degree four. It counted all 796,797 lines and all 11,475 binary and 729,768 ternary forbidden local moment patterns; checked the H and pair-centred localizers. A 12-free-point test window with a genuine 13-point anchored cap produced the expected rank-one 79x79 PSD local moment matrix. Random independent checks confirm the zero-monomial condition is equivalent to cap consistency for anchored sets with at most four free points. **This constructs the correct model; it is not a full global SDP solve.**
2. `cap055_level2_moment.py` builds actual t=2 moment matrices and performs a cutting-plane PSD outer approximation on F3^2. The 46x46 true n=2 matrix has 172 nonzero squarefree moments; F3^3 uses a 379x379 matrix and 17,929 moments. For n=2, 50 LP/eigen-separation iterations generated 947 cutting planes but failed to converge: residual minimum eigenvalue ~ -0.519, outer LP upper ~6.0. This is **UNKNOWN**, not a proof.
3. `cap055_level2_projection.py` used alternating projections onto the real PSD cone and Boolean moment consistency. In n=2, the known four-cap was PSD to ~1e-15. Target n=2,k=5 after 500 steps had PSD gap ~0.117 and negative eigenvalue ~-0.106 (inconclusive). In n=3, the nine-cap given by the graph `z=x^2+y^2` is an exact cap and has rank-one PSD moment; the n=3,k=10 projection remained negative with gap ~0.884 after 80 steps (inconclusive).
4. `cap055_cardinality_localizer.py` implemented **all** exact-size degree-<=4 cardinality equations: the n=2 target5 pure LP is FEASIBLE (118 linear rows and 172 moments); n=3 target10 pure LP is FEASIBLE (3,187 rows, 17,929 moment variables). Thus the cardinality equations alone do not close the problem: genuine PSD is necessary.
5. `cap055_full_t2_projector.py` combined all exact-size cardinality equalities and the PSD cone on n=2,k=5. After 1,500 iterations the residual PSD gap stabilized at ~0.36456 and min eigenvalue ~-0.12889 with equality residual <1e-15. **This is numerical failure to find a feasible point, NOT an infeasibility certificate.**
6. **Positive-control actual exact degree-2 SOS proof:** `cap055_n2_exact_sos_disproof.py` assumes a five-cap exists in F3^2, averages it over all 432 elements of AGL(2,3), and derives all unique moments through degree4 from the complete fixed-cardinality identities. The forced moments are `y0=1, y1=5/9, y2=5/18, y3=5/36, y4=5/54`. The explicit ten-term quadratic polynomial

`q=2*x0*x2 +3*x0*x3 +2*x0*x6 -2*x0*x7 +3*x1*x2 -2*x1*x6 -3*x2*x8 -4*x3*x4 -3*x3*x5 +3*x3*x6`

has EXACTLY `E[q^2]=-10/9` under these forced moments and the forbidden triple ideal. But `E[q^2]>=0` for every actual cap. Therefore a five-cap in F3^2 is impossible, proven by a degree-two SOS argument, checked with Python fractions and direct enumeration of all 432 affine actions. This is a rigorous low-dimensional **correctness control**, not a seven-dimensional breakthrough.
7. **Additional rigorous strength control:** `cap055_exact_rational_n2_certificate.py` exhibits an exact rational TRUE degree-2 PSD pseudo-moment (without imposing the exact `k=5` polynomial cardinality ideal) with expectation `9*(450/1000)=4.05` in F3^2. Its moments for allowed 0,1,2,3,4 subsets have integer numerators `(1000,450,178,66,28)` over 1000; the entire 46x46 moment matrix is strictly positive definite, verified with an integer-only 46-step Bareiss/Sylvester test. All forbidden triple and four-point extension moments are zero. This proves level2 moment **expectation-only** is not integral even for n=2; the exact fixed-cardinality localizing identities matter.
8. `cap055_sparse_sos_checker.py` verifies rational polynomial SOS infeasibility identities **exactly** modulo the Boolean, forbidden-pair and forbidden-triple ideals, with H/pair/local cardinality multipliers. It accepts the toy genuine identity `-1=(1-x)^2+(x-2)` for a Boolean variable constrained to 2, and rejects a deliberately invalid identity. **No global seven-dimensional dual certificate was found.**
9. Six independent tests in `test_cap055_exact_root.py` passed (complete full-root line partition, anchor geometry, H and pair terms, finite cap equivalence check, genuine rank-one moment, exact rational positive-control certificate and fake-SOS rejection).

## Actual root barrier, not a solver-timeout excuse

Before orbit symmetry reduction, the FULL anchored t=2 Boolean moment problem has a PSD basis of **2,256,751 monomials**, **847,224,947,626 potential squarefree moments of degree <=4**, **1,597,028,875 potential exact-cardinality identities of degree <=3**, and a dense moment matrix needing **~37.06 TiB** in double precision. Many moments vanish by the cap ideal, and symmetry allows block reduction, but CAP-054's residual symmetry group of order 768 does NOT by itself provide a complete small block diagonalization of this quartic algebra. The previous 81 singleton and 12,822 pair orbits help but do not show that quartic moment orbits, PSD blocks, and all localizers can be solved within the present 4 GiB / CPU-only environment.

**What is missing:** a full representation-theoretic orbit-block reduction of the selected anchors' residual group *including quartic moment symbols and the exact-size/H/antipodal localizers*, or a sound sparse dual SOS certificate supported on a tiny set of monomials that proves impossibility directly. Merely exporting the symbolic model or numerically stalling on n=2 is not mathematical closure. We did not pretend otherwise.

## Exact assessment

- Original unsolved `r3(7)` problem: **NOT DONE (ATTEMPTED)**.
- Full seven-dimensional level2 SDP solved: **NO**.
- >=237 construction or verified global `UNSAT` certificate: **NO**.
- Mathematical major breakthrough/new bound: **NO**.
- Actual true level2 implementation, localizers, global sparse model, exact independent low-dimensional SOS positive control: **YES**.

All logs, source, test results and exact certificates are retained. The advisor PDF/Markdown files are deliberately **not included** in the uploaded research archive. No new recurring automation, GPU or paid compute used.


Full runnable source ZIP (excludes all advisor documents): https://drive.google.com/file/d/1qaSt7JPgiPM0SIoVD9zW3XRA8H4O3xMz/view?usp=drivesdk
