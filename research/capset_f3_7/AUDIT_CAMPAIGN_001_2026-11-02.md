# CAPSET-F3-7: Integration of independent Math Agent Campaign 001 v2.0

**Audit date:** 2026-11-02
**Source records (Google Drive):**
- Research Log 001: https://docs.google.com/document/d/1DmvhnazPwH5NkXSqEI5DZoSQwDkr7p6sozJBVIV1o-I/edit
- Original Campaign 001 v2.0 execution report: https://docs.google.com/document/d/1_TWv6RzjYtBHJCawC6aT-q4ulBBdKuFaR7_nUaWp7lY/edit
- Dedicated Cap Set research ledger: https://docs.google.com/document/d/1eaL6YYNB80X9DwmPCVZ0mnuwSVIjSSPvpJ19uoZPQTM/edit

This is an **independent reproduction/audit** of a different agent's results, not an ownership transfer. This repo is scoped exclusively to the cap-set question and must not overwrite the other parallel mathematics track.

## Results independently checked in this repository

| Campaign claim | Independent method | Status |
|---|---|---|
| Classical 236-cap (n=7) with slices 112+112+12 | Direct enumeration from Bierbrauer–Edel support blocks, exact pair checker | VERIFIED COMPUTATION |
| Completeness of classical 236-cap | All 1,951 exterior points each incident with >=1 original secant | VERIFIED COMPUTATION |
| n=7, M=236, 1,093 projective directions, 12 slice patterns | `hyperplane_spectrum_certificate.py` (pure Python) | VERIFIED COMPUTATION |
| n=7 exact Parseval sum = 20,445,388 | Integer double-counting / independent enumeration | VERIFIED COMPUTATION |
| n=7 frequency (112,112,12)=1 and (96,96,44)=16 | Independent histogram calculation | VERIFIED COMPUTATION |
| Classical Edel Property-(ER) 496-cap in n=8 | `edel496_reproduction.py` from the 112/112/12 fibers; `verify_capset.py` | VERIFIED COMPUTATION |
| n=8 M=496, 3,280 projective normals, 17 patterns | Exact n=8 independent enumeration | VERIFIED COMPUTATION |
| n=8 Parseval sum 269,980,240; (236,236,24) occurs twice | Exact integer count | VERIFIED COMPUTATION |

These are reproductions of known constructions and combinatorial identities, **not new world records**. 496 is below the reported n=8 lower-bound record 512.

## Claims from Campaign 001 not yet independently audited

- C6 'Paley conference magic basis', 6 normals, 240-group, 13 symmetry orbits and two disjoint 112-caps.
- Claimed CP-SAT OPTIMAL solutions in dimensions 3–7: a solver optimum in a specified symmetry-restricted search family is not global optimality unless accompanied by independent argument.
- The proposed 252-point admissible 10D object and claimed dimension-480 recursive construction: independently verifying 252 points is not the same as enumerating or kernel-verifying an astronomical 480D set; the inductive construction theorem and its exact hypotheses must be audited separately.
- Report references executable `capset_swarm_solver.py` and `capset_verified_witnesses_2026_11_01.json` but these objects were NOT observed as files in the `04_EXPERIMENTS_AND_PROOFS` folder during this audit. Only the native Google Doc report was directly available. Do not claim direct artifact replay of the other agent's scripts.
- The 27-block twisting / rotated-subblocks hypotheses remain **UNVERIFIED** as discoveries of improved caps.

## Mathematical deductions for future searches

**Global necessary hyperplane condition, conditional only on the accepted theorem r3(6)=112:**
If a cap A in F3^7 has |A| = M, then for every nonzero linear normal, the three affine 6D slices sum to M and each has size <=112; therefore each has size >= M-224. In particular for M>=237 each of all 3,279 affine hyperplanes has at least 13 points. This is a simple combinatorial necessary condition, not a sufficient condition.

**Parseval caveat:** The sum of squared slice counts is a general identity for ANY finite point set; it alone cannot rule out a cap of size 237. To strengthen a global upper bound, combine it with cap-specific restrictions and validated polynomial/SDP/flag constraints.

**Change of research direction:** The 236-cap's 10/16/17-deletion local barriers eliminate certain low-radius edits, not all candidate 237 constructions. Follow Campaign 001's 27-block / hyperplane method using independent candidate sets and exact verification rather than trying only tiny perturbations of a fixed 236.

## Reproducible new experiments: coordinated coordinate-fiber reconstruction

`fiber_saturation_certificate.py` uses 189 coordinate 5D fibers (21 coordinate pairs times 9 values): 165 release no exterior point; 24 release exactly one exterior point. In the 9 aligned fibers given by fixed `(x1,x2)`, each alone releases zero exterior points.

The 9 aligned fibers each contain three 4D blocks. Releasing k=2 of them yields candidate counts 0 (20 pairs), 1 (8 pairs), 2 (8 pairs). Releasing k=3 yields up to 21 exterior candidates; releasing k=4 yields up to 138.

`fiber_reconstruction_milp.py` builds the **exact** reduced cap search with all frozen points as constraints and independently checks each incumbent. Eight of the most promising triple-fiber releases and eight four-fiber releases were run using SciPy/HiGHS; all 16 models were solved to certified optimum 236 in a local experiment, and replayed by CI.

An exploratory five-fiber target-237 MILP has ~637 variables, ~35,455 constraints, and did NOT complete proof of feasibility or infeasibility in a short CPU window. Status: **INCONCLUSIVE (TIMEOUT)**, NOT an obstruction theorem.

## Governance and next steps

1. Prioritize source retrieval for original Campaign 001 code/witness artifacts, then independently audit 240-group orbit claims.
2. Build a solver around **multiple** 5D fibers at once, but use known C6 orbit structure and block shadow constraints to reduce variable counts before paying for larger CPU budgets.
3. Compare alternative seeds (not necessarily affine equivalent to Calderbank–Fishburn 236), use 27-block twist operators, score shadow overlap, and preserve exact witnesses.
4. For upper bounds, combine Parseval + cap-specific cross-slice constraints and independently validate every LP/SDP dual certificate. A solver timeout is never a proof.
5. Do not close campaign after a lower-bound improvement. The exact r3(7) objective requires matching independent lower and upper bounds.

Status tags: all reproduced numeric facts above = VERIFIED COMPUTATION (subject to their linked code/CI); all unexamined source reports = REPORTED/UNVERIFIED; 237 remains OPEN.
