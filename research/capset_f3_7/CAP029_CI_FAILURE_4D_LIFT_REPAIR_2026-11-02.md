# CAP-029 — Hostile CI referee and exact repair of CAP-028 4D local witness
**2026-11-02 23:52 UTC | CPU only | exact F3 arithmetic | no global r3(7) progress**

## Read-first continuity and critical falsification
Read the dedicated Google Drive Ledger/folder, GitHub STATE/LOG/BACKLOG, CAP-028 source, last branch commits and Actions runs. CAP-028 commit 36983f6, Actions run 41542279551 **FAILED** in its first unit-test step. Python failures: test_local_witnesses, test_all_profiles_lift, test_moments; Node test errored. These are real test failures, not an infrastructure outage. The 19-point W766 fixture actually contained only 17 points, profile (7,5,5). Consequently CAP-028's claimed six passing local tests and 12 profile lifts were not independently reproduced in CI. CAP-027 prior run 41532249767 was green.

## Bounded exact correction, no solver required
Retain the exact 17-point W766 seed and enumerate all 81 points of F3^4, using a direct arithmetic checker (no distinct a,b,c with a+b+c=0). Exactly **five** single-point additions preserve the cap:
(0,0,0,0), (0,1,0,0), (0,2,0,2), (1,1,2,0), (2,1,2,1).
Of their ten unordered pairs, exactly **three** produce a 19-point cap:
[(0,2,0,2),(1,1,2,0)],
[(0,2,0,2),(2,1,2,1)],
[(1,1,2,0),(2,1,2,1)].
Only the **last pair** produces slice counts **(7,6,6)**. Add those two points to W766; its 19 points contain zero complete affine lines among the 1080 in F3^4. The original W774 remains a verified 18-point (7,7,4) cap. Every one of the CAP-028 count model's twelve local profiles can now be lifted by deletion from one of these two actual caps. This restores only **local 4D realizability**; there is no globally consistent 285-point F3^7 cap.

## Reproducibility, failed pilot and independence
- Deterministic stdlib exact checker: `python -m unittest discover -s research/capset_f3_7 -p 'test_cap028_4d_quotient_line.py' -v`
- Independent base-3 Node verifier: `node research/capset_f3_7/cap028_4d_line_independent.js`
- Independent standalone Python audit enumerated five singles, three pairs, one balanced pair, all 1080 affine lines, both 4D witnesses and twelve local profiles: PASS. No random seed, GPU, paid compute or SAT solver.
- A separate discovery-only SciPy MILP pilot for a fresh 7/6/6 witness (seed=0 first objective) produced no feasible result before a **155-second tool timeout**; **UNKNOWN**, not UNSAT. It was unnecessary because the finite seed-extension audit found a valid certificate.
- The old CI failure must not be erased or described as passing. New GitHub CI must finish before upgrading status.

## Meta-audit
This is an evidence-integrity correction, not a new mathematical bound. Prior work had allowed a mismatch between a reported witness cardinality and the actual serialized coordinate list. Both Python and JS tests correctly caught it on CI; the earlier local PASS claim is not supported by that commit. Future claims require (a) coordinate count, (b) independent line checker, (c) green CI on the exact committed SHA. Continue shared-fiber point-level compatibility, nonradical quadratic normals, Thackeray 110-cap classification referee, and balanced/no-111 plus >=237 branches. Literature rechecked 2026-11-02: published upper 291; Thackeray 2022 preprint claims 288; exact r3(7) OPEN. CAP-019 candidate <=287 remains provisional and externally unreviewed.

References: https://cairn-commons.com/problems/cap-sets-dim-7 ; https://arxiv.org/abs/2206.09804 ; https://onlinelibrary.wiley.com/doi/10.1002/jcd.70024 .

## CI follow-up (2026-11-02 ~23:58 UTC)
New run 41549068067 also **FAILED** (96/97 tests passed). Crucially, all six original CAP-028 tests, including independent Node and all twelve local lifts, **PASSED** with the repaired coordinates. The only failure was the new CAP-029 *test helper*, which called the deliberately assertion-raising `check()` as a Boolean predicate when enumerating intentionally invalid additions. Replaced this with `admissible()` that catches AssertionError for invalid candidates. This is a regression-test harness error, **not a counterexample to the repaired 19-point witness**. Exact standalone Python and independent Node enumerations both found 5/3/1. Another CI run is required and not yet complete.
