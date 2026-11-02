# CAP-005H — Symmetry quotient and exact integer rounding (2026-11-02)

## Mathematical scope
Fix the independently verified Calderbank–Fishburn 236-point cap B in F_3^7. Release exactly six of the 27 four-dimensional fibers indexed by the first three coordinates; keep all original points outside those fibers fixed. This is a restricted reconstruction problem, NOT the global r_3(7) problem.

The previous CAP-005G independently checked 848 rational LP duals and left 88 unresolved six-fiber subsets out of C(27,6)=296010. Its GitHub Actions run 41386314239 is SUCCESS (confirmed this cycle).

## Exact new result
Four explicitly coded affine transformations preserve B point-by-point as a set, verified with exact mod-3 arithmetic. Their induced action on the 27 fiber labels generates a group of order 16. Exact orbit enumeration yields 19,464 orbits on all 296,010 six-fiber subsets, with orbit-size histogram 1:2, 2:18, 4:139, 8:1683, 16:17622.

The 88 CAP-005G unresolved subsets are exactly seven complete orbits: three of size 8 and four of size 16. Canonical representatives and sizes:
- (0,1,2,4,5,18): 8; fractional LP gap 6.
- (0,1,3,4,5,18): 16; gap 2.
- (0,1,3,5,8,18): 16; gap 10.
- (1,2,3,4,8,18): 16; gap 1/2.
- (1,2,4,5,7,18): 16; gap 2/3.
- (1,3,5,7,8,18): 8; gap 9/2.
- (1,4,5,7,8,18): 8; gap 7/2.

For the two 16-element orbits with LP gaps below 1, an exact rational dual certificate bounds the number of selected points in the released fibers by respectively 137/2 and 206/3. Both have baseline occupancy 68. Since the number of points is integral, both bounds imply at most 68, hence no improvement. The affine automorphisms transfer these two exact certificates to all 32 members of the two orbits. Therefore cumulative six-fiber exclusions increase from 295,922 to **295,954 of 296,010**, leaving **56** cases in five orbits.

The independent checker reconstructs all 236 original points, checks all original cap lines, reconstructs the 1,951 outsiders and all secants, verifies every stated dual pair/triple is a genuine mod-3 collinearity constraint, checks nonnegative rational multipliers and full variable coverage, and verifies the strict objective < baseline+1. It also checks the 16-group action and that the two certified orbits are contained in the previous 88 cases. No floating-point solver result is trusted as a proof.

## Reproduction and limits
CPU only, no GPU, no paid compute, no random seed. From repository root, after installing scipy (used only to propose duals):

    OPENBLAS_NUM_THREADS=1 python research/capset_f3_7/cap005_h_rounding_dual_generator.py --out /tmp/cap005_h_rounding_duals.json
    OPENBLAS_NUM_THREADS=1 python research/capset_f3_7/cap005_k6_lp_dual_certificate.py --out /tmp/cap005_k6_lp_duals.json
    python research/capset_f3_7/cap005_k6_symmetry_quotient.py /tmp/cap005_k6_lp_duals.json --out /tmp/cap005_h_symmetry.json
    python research/capset_f3_7/cap005_k6_symmetry_rounding_check.py --duals /tmp/cap005_h_rounding_duals.json --certificate /tmp/cap005_k6_lp_duals.json

The two duals were locally generated with SciPy 1.17.0 and independently verified with exact Fraction arithmetic. The 88-case orbit classification was also independently checked against the actual GitHub CI artifact capset-k6-rational-duals-848 (run 41386314239). Local deterministic CPU validation PASS; new CI for this commit is pending at initial write.

Exploratory, NON-CERTIFYING: seven bounded HiGHS binary MILP target-237 feasibility checks all reported infeasible in ~0.04–0.06 seconds per representative, with a known 236-point baseline feasible at target 236. Solver status without a separately checkable integer UNSAT certificate is NOT accepted as a theorem for the remaining 56 cases.

## Strategy audit
The 88 apparently difficult cases were mostly symmetry duplicates; seven orbit representatives suffice. Two orbits are now rigorously excluded by integer rounding. For the five remaining orbits, seek independently checkable cutting-plane or exhaustive UNSAT certificates rather than treating HiGHS infeasibility as proof. Avoid overfitting to the fixed 236-cap neighborhood: nonlocal constructions and global upper bounds remain essential.

Literature check 2026-11-02: Cairn Commons (status dated 2026-10-03) still reports 236 <= r_3(7) <= 291; Thackeray arXiv:2206.09804 reports no 289-point cap (preprint, not independently reviewed here). Grace–Voloch (2026) concerns algebraic complete capsets and does not settle the exact 7D maximum. Novelty of this restricted computation is not established. No >=237 construction, no stronger global bound, and r_3(7) remains OPEN.
