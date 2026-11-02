# CAP-005I — Complete exact six-fiber reconstruction barrier (2026-11-02)

## Theorem (restricted)
Let B be the verified Calderbank–Fishburn 236-point cap in F_3^7 and partition F_3^7 into the 27 four-dimensional affine fibers indexed by the first three coordinates. Fix any subset T of at most SIX fibers. Keep all points of B outside T unchanged, but allow arbitrary replacement of points inside T. Then every resulting cap has at most 236 points.

This is a theorem about a fixed neighborhood of a fixed 236-point construction, NOT a global upper bound on r_3(7).

## Proof structure and finite certificates
Earlier CAP-005A through CAP-005G certified 295,922 of the 296,010 six-fiber choices, leaving 88. CAP-005H verified four affine automorphisms preserving B, generating a 16-element action on the 27 fiber labels. The 88 survivors form seven complete orbits (three size-8, four size-16).

For each orbit representative, let F=B outside T be fixed, and V contain original B points inside T plus only outsiders whose original secants each touch T. Every possible replacement is F union a subset of V. The following inequalities hold for binary selection variables:
- If a,b in V have third mod-3 collinear point in F, x_a+x_b<=1.
- If a,b,c in V are collinear, x_a+x_b+x_c<=2.
- For a triangle of the pair-conflict graph, x_a+x_b+x_c<=1.
- For a FIVE-cycle of that graph (including cycles with chords), the sum of its five selection variables <=2.
- For each variable, x_p<=1.

The five-cycle inequality follows because an independent set of a 5-cycle has size at most 2. A pair-conflict edge is independently checked to have its third collinear point in the immutable fixed set F.

SciPy/HiGHS proposes nonnegative dual multipliers. They are rationalized (denominator <=1000), then scaled by 1001/1000 to create strict exact coverage. The independent checker does NOT import SciPy or the generator. It reconstructs B and all 1,951 outsiders, original secants, each variable universe, and verifies every selected pair/triple/triangle/cycle inequality using mod-3 arithmetic, exact nonnegative Fraction multipliers, full variable coverage >=1, and objective STRICTLY below baseline occupancy+1. Thus integrality proves every representative has at most its baseline occupancy. Verified affine automorphisms transfer each certificate to its entire orbit, covering all 88 remaining cases.

Combined with the previously CI-verified 295,922 exclusions, ALL 296,010 six-fiber modifications are excluded from improving 236. The baseline B itself is feasible, hence the exact restricted optimum is 236.

## Reproduction
CPU-only; no GPU, paid compute or random seed. Run from repository root:

    OPENBLAS_NUM_THREADS=1 python research/capset_f3_7/cap005_k6_lp_dual_certificate.py --out /tmp/cap005_k6_lp_duals.json
    OPENBLAS_NUM_THREADS=1 python research/capset_f3_7/cap005_i_oddcycle_dual_generator.py --out /tmp/cap005_i_oddcycle_duals.json
    python research/capset_f3_7/cap005_i_oddcycle_dual_check.py /tmp/cap005_i_oddcycle_duals.json /tmp/cap005_k6_lp_duals.json

Local exact independent checker PASS for seven rational duals, covering 88/88 survivors. The generated certificate JSON is about 60 KB. Its local SHA256 on SciPy 1.17.0 is 8a7b5e080ee8f90167f03bec27da5410880b3b945c16fb067b31ec0d2ced6ecd; solver version may change certificate bytes, so trust the exact checker, not the hash. A dedicated GitHub CI artifact archives the certificates. New CI is pending at initial write.

Earlier seven binary MILP infeasible statuses were noncertifying and were NOT used in this proof. The proof relies only on independently checked rational inequalities and exact group action.

## Meta-audit and literature
The entire fixed-coordinate <=6-fiber reconstruction route is now exhausted. Repeating it will not improve the lower bound. The next substantive work should change the partition or the baseline construction, test genuinely nonlocal occupancy-changing templates, and seek globally valid upper bounds. Even this complete restricted theorem does not determine r_3(7).

Public status checked 2026-11-02: Cairn Commons dated 2026-10-03 lists 236<=r_3(7)<=291; Thackeray arXiv:2206.09804 reports exclusion of 289-point caps, a preprint claim not independently reviewed here. The 2026 Grace–Voloch paper studies algebraic complete capsets, not the exact 7D maximum. Novelty of this restricted computation is not established. No >=237 witness, no global upper bound improvement, r_3(7) OPEN.
