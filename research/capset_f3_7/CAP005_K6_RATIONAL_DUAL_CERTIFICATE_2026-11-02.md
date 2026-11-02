# CAP-005G — Exact rational LP dual certificates for 848 six-fiber neighborhoods (2026-11-02)

## Scope and theorem

Fix the independently verified 236-point cap B in F_3^7 at `candidates/calderbank_fishburn_236.txt`. Partition the space by the first three coordinates into 27 affine F_3^4 fibers. For a choice T of exactly six fibers, keep every point of B outside T fixed, but allow arbitrary replacement inside T.

CAP-005E and CAP-005F had already rigorously excluded 295,074 of the 296,010 possible six-fiber neighborhoods, leaving 936. This run produced **848 further independently checkable exact rational dual certificates**, leaving **88 unresolved**. Thus, conditional on the already-CI-verified earlier certificates, the cumulative restricted exclusion is **295,922 / 296,010**. This is not an unrestricted upper bound for r_3(7), nor a proof that the six-fiber restricted optimum equals 236: 88 cases remain.

## Finite inequality certificate

For T, let F be the original points outside T (fixed). Let E_T be the outsiders x whose every B-secant contains at least one original point inside T. Every replacement cap is contained in F union V, where V is the union of the original B points inside T and E_T.

For each distinct a,b in V with c=-a-b in F, the inequality x_a+x_b<=1 holds. For each distinct collinear triple a,b,c in V, x_a+x_b+x_c<=2 holds. For every p in V, 0<=x_p<=1. These are valid for **all** integral replacement caps; their linear relaxation is therefore a rigorous upper bound.

A certificate contains nonnegative rational multipliers y_L for selected pair/triple line inequalities and z_p for selected x_p<=1 inequalities such that every variable has total coefficient at least 1. If sum_L y_L RHS(L)+sum_p z_p <= |B intersect T|, then the number of selected variable points cannot exceed the original occupancy of T. Adding the fixed points gives total <=236. This is weak duality, checked with exact Fraction arithmetic; the LP solver is **not** trusted as proof.

The independent verifier (separate code, no SciPy or generator imports) reconstructs all 1,951 outsiders and their original secants by direct mod-3 arithmetic, reconstructs each E_T, verifies every listed inequality is geometrically valid, checks exact rational nonnegativity, every variable's coefficient coverage, and the objective. It checks 848 distinct groups and disjointness from the previously certified 680 groups. The previous 680 certificates are independently checked in the same CI workflow.

## CPU-only experiment

Local experimental reproduction used SciPy 1.17.0 / HiGHS, OPENBLAS_NUM_THREADS=1, no random seed, GPU, or paid compute. Full 936-group LP census returned 848 instances with optimum exactly the baseline occupancy; the remaining 88 had LP gaps: 16 each of 0.5, 2, 10, and 2/3; 8 each of 3.5, 4.5, and 6 (the gap values are **LP relaxation gaps**, not valid caps). The 848 candidate duals were converted to rational coefficients with denominator <=1,000,000, then all 848 passed an independent exact-arithmetic checker. Local certificate file: ~1.4 MB; local SHA256 `0a49469949dca1e9a55e6cffab62306eec7a0e9f9e9bace17289e1e26bd4e7db` (a CI rerun with a different SciPy/HiGHS version may produce a different, equally valid certificate; trust the exact checker, not this hash).

From repository root:
```sh
OPENBLAS_NUM_THREADS=1 python research/capset_f3_7/cap005_k6_lp_dual_certificate.py --out /tmp/cap005_k6_lp_duals.json
python research/capset_f3_7/cap005_k6_clique_cover_certificate.py --out /tmp/cap005_k6_clique_cover.json
python research/capset_f3_7/cap005_k6_lp_dual_check.py /tmp/cap005_k6_lp_duals.json --previous /tmp/cap005_k6_clique_cover.json
```

Scripts: `cap005_k6_lp_dual_certificate.py`, `cap005_k6_lp_dual_check.py`; GitHub Actions workflow archives the JSON for 30 days. **At initial write: local CPU exact checker PASS; new GitHub CI still pending.** The branch CI must be inspected before promoting this result to CI GREEN.

## Strategy and literature audit

The remaining 88 cases exhibit a genuine fractional LP gap (not a 237-point witness). Next: stronger cuts (odd-cycle/triangle rank constraints, deletion-cover inequalities), exact MILP/SAT with independently checkable proofs, or different nonlocal constructions. This line of local reconstruction research alone cannot establish global r_3(7); prioritize globally valid upper bounds in parallel. The publicly tracked 2026-10-03 status remains 236<=r_3(7)<=291; Thackeray (arXiv:2206.09804) claims no 289-point cap (preprint, not independently reviewed here). Recent Grace–Voloch 2026 work on algebraic complete capsets does not establish the exact 7D maximum. Literature novelty of this restricted computational certificate has **not** been established.

No >=237 verified construction; no stronger global upper bound; exact r_3(7) remains OPEN.
