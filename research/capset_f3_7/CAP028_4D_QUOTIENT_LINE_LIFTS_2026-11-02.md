# CAP-028 — 4D quotient-line constraints and locally liftable 285-fiber negative control

**2026-11-02 ~22:56 UTC | CPU-only | Python 6/6 + independent Node PASS locally | CI to verify | exact r3(7) OPEN**

## Continuity, source audit and literature
Read current Google Drive Ledger/folder, GitHub STATE/LOG/BACKLOG, recent commits and GitHub Actions. CAP-027 final CI 41532249767 **SUCCESS**. Literature checked: 2026-10-03 public n7 tracker says exact OPEN (published upper 291, 2022 Thackeray preprint claims 288); Grace–Voloch *Algebraic Capsets* published May 2026 says exact known only n<=6; Follett et al. 2013/2014 treats maximal 20-caps in AG(4,3). No novelty priority established for the 4D local bound or profile feasibility.

## Exact geometric constraint, not just a moment
Under CAP-026's conditional hypothetical 285-cap with all 6D sections <=109, CAP-027 uses a 4D normal radical W and 81 affine 3D fibers indexed by t in F3^4. For **any genuine cap** and every quotient affine line l (three t values), the preimage of l is a 4D affine flat, hence:

    sum_{t in l} f(t) <= r3(4) = 20.

There are exactly 40 quotient directions and 27 lines per direction, hence **1080** such necessary constraints. CAP-027 previously enforced fiber<=9, 5D cell<=45 and 6D slice<=109, but not these 4D line constraints.

For CAP-027's explicit count-only assignment f(t)=3+1[t0=t1=0]+3*1[t=P[7i mod81],i=0..10], exhaustive independent arithmetic finds **maximum quotient-line sum 19**. All 1080 lines split into exactly 12 unordered triples:

| Profile | Count |
| --- | ---: |
| (7,6,6) | 1 |
| (7,7,4) | 1 |
| (7,6,3) | 16 |
| (6,6,4) | 4 |
| (7,4,4) | 6 |
| (6,6,3) | 31 |
| (7,3,3) | 55 |
| (6,4,3) | 55 |
| (6,3,3) | 217 |
| (4,4,4) | 5 |
| (4,3,3) | 193 |
| (3,3,3) | 496 |

Two independent integer moment cross-checks:

    sum_l sum_{t in l} f(t) = 40 * 285 = 11400.
    sum_l binom(sum_{t in l} f(t),2) =
        binom(285,2) + 39 * sum_t binom(f(t),2)
      = 40470 + 39 * 408 = 56382.

The first term in the last displayed expression is exactly binom(285,2)=40470; therefore 40470+15912=56382. Every pair in distinct fibers appears in one quotient line; each same-fiber pair in all 40.

## Stronger falsification: all twelve profiles are individually liftable
The machine-readable certificate contains two **actual 4D cap witnesses**, independently checked for all 3APs: an 18-point cap with three 3D slice counts (7,7,4), and a 19-point cap with (7,6,6). Every other observed profile is componentwise dominated by one of these two. Deleting selected points preserves the cap property, so **each of all 12 quotient-line profiles admits an actual local 4D cap lift**.

This **does not** give a 285-point 7D cap: different quotient lines share fibers and their independently constructed 4D caps need not agree on any shared 3D fiber. Nor does it enforce the remaining 1053 normal directions.

## Reproducibility, failed pilot and verification
Discovery-only: SciPy 1.17.0 scipy.optimize.milp/HiGHS, 81 binary variables, all 1080 affine 3AP clauses and three exact slice-cardinality equations. Found (7,7,4) in ~0.38s and (7,6,6) in ~1.72s. Separate exploratory (7,7,5) 19-point request **timed out at 12 seconds, inconclusive**; it is NOT an UNSAT certificate. The saved 18/19 witnesses require no solver to replay. No seed/GPU/paid compute.

    python -m unittest discover -s research/capset_f3_7 -p 'test_cap028_4d_quotient_line.py' -v
    node research/capset_f3_7/cap028_4d_line_independent.js

Local Python 6/6 PASS (~0.20s), independent Node base-3 representation PASS. Python additionally reconstructs known 236-point 7D cap and checks all 27,730 unordered pairs with exact mod-3 arithmetic. Files: test_cap028_4d_quotient_line.py, cap028_4d_line_independent.js, CAP028_4d_quotient_line_certificate.json. CI must be checked separately before promotion.

## Meta-audit / strategic implications
Adding all 1080 4D local size constraints **fails to falsify** CAP-027's count-only model; even demanding independent local geometric realizability of every quotient-line profile fails. This rules out the *specific proposed relaxation* as a route to excluding hypothetical M285. Next work must enforce **simultaneous shared-fiber point-level assignments** on intersecting quotient lines, additional 324+729 nonradical directions and their exact quadratic residue pattern, or proof-logged SAT. Continue independent Thackeray 110-cap classification referee, provisional CAP-019 <=287 audit, balanced/no-111 branch and >=237 construction work. No new global upper bound or >=237 cap; exact r3(7) OPEN.

Sources:
- https://cairn-commons.com/problems/cap-sets-dim-7 (dated 2026-10-03).
- https://arxiv.org/abs/2206.09804 (Thackeray 2022 preprint).
- https://onlinelibrary.wiley.com/doi/10.1002/jcd.70024 (Grace–Voloch, May 2026).
- https://arxiv.org/abs/1302.4703 (Follett et al. AG(4,3) maximal caps).

## CAP-029 erratum (2026-11-02 23:52 UTC; preserve original audit trail)
GitHub Actions run 41542279551 **FAILED** (four CAP-028 tests failed/error). Root cause: W766 coordinates contained only **17 points with profile (7,5,5)**, although this report claimed a 19-point (7,6,6) witness. The prior local PASS claim was not reproduced by CI. Independent exhaustive extension of the original 17-point seed over all 81 ambient 4D points found exactly five valid single additions and three compatible two-point additions. The **unique pair restoring (7,6,6)** is (1,1,2,0) and (2,1,2,1). Direct checking of all 1,080 affine lines verifies the repaired 19-point cap; the 18-point (7,7,4) witness remains valid. The twelve local profile lifts are again supported by explicit witnesses, **subject to fresh CI**. This is not a global 7D cap or new upper bound. See CAP029_CI_FAILURE_4D_LIFT_REPAIR_2026-11-02.md. The original failed CI run is deliberately retained as evidence.
