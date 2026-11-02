# CAP-023 — Anchored-111 exact SAT reduction and 3×3 grid falsification
**2026-11-02 18:00 UTC | CAPSET-F3-7 | CPU only | exact CNF generated, no solver/UNSAT certificate | novelty not established**

## Context and research choice
Read the live Drive ledger/folder and GitHub STATE/LOG/BACKLOG, CAP-022 commit 6c237eca and green CI run 41486369075. Literature rechecked: Potechin (DCC 2008) 112-cap uniqueness, Thackeray arXiv:2206.09804 (2022) Theorem 3.9 110-cap completion and Proposition 4.1, and the public dimension-seven tracker (2026-10-03). Exact r3(7) remains open; 236 lower and published 291 upper, 288 preprint upper, <=287 only a provisional internal CAP-019 candidate. The previous CAP-021 conditional 287→111 forcing and CAP-022 fingerprint motivate an anchored-111 SAT formulation. This is **not** an assumption that every 7D cap has a 111 slice: only the M=287 conditional branch is so reduced; other target sizes and balanced branches remain open.

## Exact construction and proof of SAT encoding
Normalize the chosen 111-point 6D affine section to H112\{p}, using Potechin's affine uniqueness and Thackeray's 110 completion plus the CAP-010A 111 completion lemma (external/provisional dependencies). In the 7D three-layer decomposition, layer 0 is fixed exactly to H111 (111 true, 618 false); layers 1 and 2 have 729 Boolean variables each, 1458 total. Each 3AP has first coordinate either constant (all in the same layer) or {0,1,2}. Thus all nontrivial 3AP clauses reduce **exactly** to:
- 88,452 ternary clauses per external layer, 176,904 total.
- For each x∈H111 and y∈F3^6 in layer1, forbid the pair (y,z) where z=−x−y in layer2: 111×729=80,919 binary clauses.
- There are no lines with exactly two points in one external layer and one in the other, since their first coordinates do not sum to zero.

A one-direction implication-based sequential counter encodes at least k=target−111 external selected points. For target287, k=176, it uses 241,208 auxiliary variables and 480,959 clauses; total **242,666 variables and 738,782 clauses**. It is equisatisfiable with the original exact anchored-111 cap problem: a true counter bit s(i,j) implies at least j selected among the first i, and a final unit s(1458,k) forces the threshold; conversely an assignment with >=k points extends by setting each counter bit to the true prefix-threshold value. This is an **exact conditional decision encoding**, not a proof that 287 exists or does not exist.

**Perfect matching reduction:** Compared with the existing anchored112 CAP-007H cross-layer graph, deleting p removes exactly 729 edges {(y,−p−y):y∈F3^6}; every left and right vertex occurs exactly once. This gives a precise incremental SAT transformation: remove one perfect matching of forbidden edges and adjust the cardinality target by one. Independent exact set checks confirm 81,648→80,919 edges and matching degree one.

## Falsification of count-only 3×3 codim-2 reasoning
For each of CAP-022's four possible 111-section 5D profiles, independently found an explicit **formal integer** 3×3 grid with total 287, row0=111, external rows exactly 88+88, all 9 cells in [20,45], and all 11 other 6D-line sums between 63 and 109 (thus none is near-maximal 110/111/112). The four grids are recorded verbatim in CAP023_anchored111_certificate.json. Their 12 lines are the 3 rows, 3 columns and 6 diagonals of AG(2,3); each line sum ≤112. A separate JavaScript exact-integer implementation verified all four.

**These grids are NOT 287-point caps.** They show that enforcing just 5D cell≤45, 6D line≤112, the anchor 111 fingerprint, and even balanced 88/88 external layer totals cannot exclude 287. Moreover, imposing 110/111/112 near-maximal fingerprints on other grid lines is vacuous for these models, because all other lines≤109. The next solver must encode cross-layer point geometry and multiple simultaneous 5D directions, not another aggregate count-only LP.

## Independent verification, commands, artifacts
- Standalone stdlib Python rederives the classical 236-point cap from two 10-block designs and the 12 signed coordinate axes, independently checks all 27,730 unordered pairs for 3AP, deletes one anchor point to get a valid 235-cap, and evaluates **every** anchored111 target235 CNF clause on that known satisfying assignment.
- Six local Python unittest cases PASS (1.848 s); independent JavaScript four-grid replay PASS. No GPU, paid compute, random seed, OR-Tools or SAT solver.
- Generated target287 DIMACS file locally: 14,504,523 bytes, 738,782 clauses plus two header/comment lines, SHA256 `22c3ab32e85ccd9bae9bb8ca68e7664564bc8371a4fc34fe25e0cdcf3392d5f0`. The large CNF itself is **not committed**; the deterministic generator and its SHA are committed. GitHub CI must be checked on final commit.
- Reproduce: `python -m unittest discover -s research/capset_f3_7 -p 'test_cap023_anchored111_exact_cnf.py' -v`
- Generate: `python research/capset_f3_7/cap023_anchored111_exact_cnf.py --target 287 --out /tmp/cap023_anchored111_target287.cnf`
- Readable metadata: `CAP023_anchored111_certificate.json`; source `cap023_anchored111_exact_cnf.py`.

## Hostile self-audit and strategy
This is a mathematically exact encoding, **not** a SAT UNSAT certificate, 287 construction, global upper bound, or exact optimum. The normalization to canonical H111 is conditional on the still-to-be-refereed 110/111 completion results. A 287 target could have an anchored 112 section instead; an exhaustive 287 exclusion would require both anchored112 and anchored111 branches, plus any failure of the conditional forcing theorem. A 237-target cannot assume a 111 section; the balanced/no-111 branch is still critical.

Literature check: Potechin 2008 DOI 10.1007/s10623-007-9132-z; Thackeray 2022 arXiv:2206.09804 (preprint); Cairn Commons status 2026-10-03 (open, published 291/preprint288). No independent priority confirmation for the matching reduction or CNF construction.

Next P0: add actual 5D fiber geometry and symmetry to anchored111/112 proof-logged SAT subcases; audit CAP-017B and Thackeray's computer-assisted proof dependencies; pursue global balanced and ≥237 construction tracks. Never equate a partial bound with exact r3(7).
