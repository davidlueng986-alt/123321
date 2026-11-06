# CAP-054 — H1 symmetry-broken SDP / H3 order-5 construction: direct attempts

**Date:** 2026-11-07 UTC. **Goal:** determine the exact r₃(7). **Result: NOT DONE (ATTEMPTED).** No valid ≥237 cap and no complete global proof of nonexistence. No improved bound or literature novelty is claimed. Hourly CAPSET automation remains disabled.

The previous External Advisor Brief is **not** contained in this artifact or its ZIP and is excluded from Google Drive uploads.

## Status of the two hypotheses

**H1 (SDP).** We grounded the only provably global route in CAP-052's single dense-centred normal form (selected 11, excluded 52, free 2,124; slice H≥89; at least seven centred H antipodal selected pairs). The exact residual linear group `B₄ × S₂` has order `2⁴×4!×2=768`. It preserves the chosen points, excluded points, H and the antipodal-pair requirement. Independent canonical-form and Burnside calculations agree: 81 free singleton orbits and **12,822 unordered free-pair orbits**. Direct Lasserre level-2 basis of subsets of 2,124 free points up to size two has 2,256,751 rows/columns; a naive double-precision dense PSD matrix would occupy 37.06 TiB. This estimate is NOT an impossibility proof for block-diagonal symmetry reduction. We did not solve a genuine level-2 SDP or obtain a dual certificate.

**Precise no-go for a WEAK level-1 SDP.** We built an explicit rational pseudo-solution using the average of **64 non-cap samples of size exactly 237**. Every sample contains CAP-052's 11 anchors, avoids its 52 excluded points, contains ≥89 H points and ≥7 antipodal pairs, and avoids every 3AP that uses a selected anchor. The 64-sample Gram matrix `M = BᵀB/64`, where each row of B is `(1, X)`, is PSD *by construction*. Its first moments have `Σ_p x_p=237` and satisfy every affine-line **linear** inequality `x_a+x_b+x_c≤2`. The independent checker enumerated ALL **796,797 lines** and observed maximum integer numerator `128/64=2`; free singleton frequencies are at most `16/64`. Any forbidden anchor pair has zero second-moment. The 64 concrete samples each violate **820–932 genuine three-point constraints** among free points. They are not caps; they witness only that `PSD level1 + first-moment 3AP + anchor restrictions` cannot establish a 237-point contradiction. This does not invalidate any genuine level-2 Lasserre or Schrijver triple SDP, which must explicitly impose third-order moments `E[x_a x_b x_c]=0` and higher localizations.

**Crucial overlooked published negative result for naive H1.** Dion Gijswijt's 2005 *Matrix Algebras and Semidefinite Programming Techniques for Codes*, §7.1, Proposition 45, exactly proves that a specific fully Hamming-symmetric Schrijver-type three-point SDP cap bound has optimum `1+(3ⁿ−1)/2`: in n=4 it yields **41** (actual 20), in n=7 **1094** (target around 236). This does **not** say every symmetric or symmetry-broken SDP is equivalent to moments; it explicitly refutes the naive hope for that particular triple-SDP. Thus H1 must use a genuinely stronger localizing algebra / level2+ with anchor preserving subgroup and a mathematically checked dual, rather than merely relabeling a weak 3-point relaxation. Source: https://citeseerx.ist.psu.edu/document?doi=3f2a5e8ecdae9271f31e39ae56217a5baa784b42&repid=rep1&type=pdf (pp. 77–79, Proposition 45).

**H3 (Kramer–Mesner C₅).** An order-five affine automorphism of F₃⁷ is conjugate to the direct sum of the irreducible 4D module `F₃[x]/(x⁴+x³+x²+x+1)` and the identity on 3D; affine translations are removed because 5 is invertible modulo3. This action has exactly **27 singleton point orbits** and **432 five-cycles**, totaling 459 orbit variables. We enumerated all **796,797** affine lines and reduced the cap condition to **864 unique binary** and **147,357 unique ternary** hyperedge constraints (no one-orbit forbidden terms). Added all 27 invariant AG4, 117 invariant AG5, and 39 invariant AG6 correct capacity inequalities, 183 subflat cuts in total. Entire integer program has 459 binary variables, 148,404 inequalities, 456,192 nonzeros. The root unrestricted-in-this-symmetry MILP run 25s yielded `UNKNOWN` with no feasible cap237. It is CONDITIONAL on C₅ symmetry and does **not** cover a 237-cap without this automorphism.

For EXACTLY 237 under C₅, the number f of selected fixed points satisfies `237=5c+f` with `0≤f≤r₃(3)=9`, so **f∈{2,7}**, cycles selected 47/46. Both cases contain ≥2 selected fixed points, which can be canonically moved by the affine centralizer to `(0,0,0,0,0,0,0)` and `(0,0,0,0,1,0,0)`. We solved both complete C₅-exact-237 branches using **two independent solvers**: HiGHS MIP (f2 20s; f7 22s) and native Z3 SAT (f2 22s; f7 22s). All four attempts returned `UNKNOWN/timeout`; none produced a candidate or proof. An independently written witness checker is included, but cannot report success without a 237 witness.

**Low-dimensional proof controls / formulation checks:** The same canonical 5-fold action in AG4 gives exactly 17 orbit variables, and exhaustive enumeration of all 131,072 masks yields **382 valid invariant 4D cap patterns**, maxima **20 without** and **16 with** the singleton fixed point. A separate AG5 51-orbit MILP found an actual verified **45-point** cap and reported optimal45, consistent with the known r₃(5)=45. Thus the order-5 action alone does not improve the true AG4/AG5 maximum.

**LP/integrality failure audit:** The full 459-variable continuous LP with all line-orbit inequalities plus 183 subflat cuts has optimum **336**, far above237. Twenty of its 27 four-dimensional fiber marginals lie **outside** the exact 382-pattern convex hull. Adding a Dantzig–Wolfe extended formulation with **10,314 local pattern variables** and 486 exact coupling equations makes all 27 fibers integrally admissible *in convex combination*. Yet the recomputed LP optimum remains **336**. Thus local AG4 integrality, even exact, does not cut the relevant fractional optimum; a genuine cross-fiber consistency theorem or higher-level PSD/cut is essential. This is a negative feasibility finding about the conditional C₅ relaxation, not a mathematical cap bound.

**Direct H3 constructive search:** A stochastic orbit-greedy method using exact forbidden triple hyperedges constructed actual verified C₅-invariant 7D caps up to **167 points** in 12 seeds with the f=2 fixed anchor; no 237-point cap. This is not competitive with the known 236 lower bound and is reported only as a failed construction attempt.

## Root decision and next non-substitute attack

- The unrestricted exact maximum remains unknown: known explicit lower 236; Thackeray 2022 proposed upper288. The 237 yes/no test alone determines whether 236 is optimal, but a 237 witness *only* refutes 236, not the precise maximum.
- **H1 must next implement a real level2+ localizing SDP** with `x_a x_b x_c=0` for every line, plus independent rational dual checking, using CAP052's order768 residual action. The previous naive 3-point SDP is *provably ineffective*; the 64-sample PSD countermodel shows why the weakest replacement is ineffective too. Full level2 at present size cannot be honestly claimed implemented or solved.
- **H3 must either find a verified C₅-invariant ≥237 cap or fully certify both f2/f7 branches UNSAT**, and even then this would exclude only that automorphism class, not all 237 caps. Four solver timeouts and weak LP relaxations make continued identical MIP/LP retries poor value. A qualitatively stronger cross-fiber exact geometry/certificate is needed.
- Do not misrepresent conditional or weak-relaxation work as an OPEN→CLOSED result; this run is **NOT DONE (ATTEMPTED)**. No new recurring schedule was created, no unrelated repository altered, and all External Advisor Brief files were excluded from upload.

## Reproduction

```bash
OPENBLAS_NUM_THREADS=1 python h3_order5_orbit_ilp.py --audit-only
OPENBLAS_NUM_THREADS=1 python h3_local_fiber_audit.py
OPENBLAS_NUM_THREADS=1 python h3_order5_exact_AG5.py
OPENBLAS_NUM_THREADS=1 python h3_order5_rooted_237.py --fixed 2 --seconds 20
OPENBLAS_NUM_THREADS=1 python h3_order5_rooted_237.py --fixed 7 --seconds 22
OPENBLAS_NUM_THREADS=1 python h3_local_integrality_hull.py
OPENBLAS_NUM_THREADS=1 python h3_order5_exact_AG4_hull_LP.py
OPENBLAS_NUM_THREADS=1 python h1_cap052_residual_symmetry.py
OPENBLAS_NUM_THREADS=1 python verify_h1_burnside_orbits.py
OPENBLAS_NUM_THREADS=1 python h1_level1_psd_countermodel.py
OPENBLAS_NUM_THREADS=1 python verify_h1_level1_psd_countermodel.py
# Z3 C++:
g++ -std=c++17 -O2 -Wall -Wextra -Werror h3_native_z3_5sym.cpp -o h3_native_z3_5sym -L/usr/lib/x86_64-linux-gnu -l:libz3.so.4
python h3_emit_sat_edges.py
./h3_native_z3_5sym h3_order5_hyperedges.txt 2 22000
./h3_native_z3_5sym h3_order5_hyperedges.txt 7 22000
```

All source files and direct machine-readable outputs are in the accompanying ZIP. Large non-cap pseudo-distribution is explicitly labeled **NOT CAPS**. If any future solver claims SAT, do not accept it without `verify_h3_order5_candidate.py` and/or independent full-F3 arithmetic; if UNSAT, require independently checked proof logs.


## Verified Drive evidence

- Report: https://drive.google.com/file/d/1O1hwnvyDMVlsUyigRX3ehPTlU3aO0V-E/view?usp=drivesdk
- ZIP containing ALL reproducible source, 64×237 PSD pseudo-distribution, exact checker and native Z3 logs (excludes any advisor documents): https://drive.google.com/file/d/1B6lBv3eM-WCpDe2j8R3jyUcL9l776JJT/view?usp=drivesdk
- ZIP SHA256: `404f4d93a832acc4862a64175e8bec64ce59d14c6cb46c0cd8285805c6d5f311`
