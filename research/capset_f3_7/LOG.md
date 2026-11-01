# CAPSET-F3-7 Research Log (append only)

## 2026-11-02 | BOOTSTRAP
Claim status: OPEN, externally reported record size 236; this branch has not yet independently verified a 236-point witness.
Scope: separate from other ongoing mathematical project.
Hypothesis CAP-001: recover 236-point construction from primary literature and reverify as a regression fixture.
Completed: created dedicated branch and operating protocol. Not completed: substantive search or novel proof.
Next: establish deterministic checker and provenance-preserved published baseline; then test one controlled candidate search methodology.


## 2026-11-02 | CI calibration run 41333612331 | VERIFIED COMPUTATION
- GitHub Actions: https://github.com/davidlueng986-alt/123321/actions/runs/41333612331
- 5 exact verifier unit tests passed.
- Command: python research/capset_f3_7/search_baseline.py --seed 7 --rounds 2 --out /tmp/capset_candidate.txt ; python research/capset_f3_7/verify_capset.py /tmp/capset_candidate.txt
- Scores: 135 on first round, 136 on second; exact arithmetic checker: VERIFIED cap dimension=7 size=136.
- Interpretation: purely a calibration result, substantially below the external 236-point record. Artifact was temporary on GitHub runner and not retained, so a future source commit is needed for durable witness replay. The fixed seed and implementation support regeneration.
- Next: CAP-001 reproduce known 236-point baseline and inspect construction before spending search compute.

## 2026-11-02 CAP-001 complete: published 236-cap reproduction

Status: VERIFIED COMPUTATION, not a novel record.
- Original Bierbrauer/Edel Table 1, Table 2 construction reproduced.
- 236 unique vectors in slices 112+112+12; checked all 27,730 pairs by exact arithmetic.
- CI run: https://github.com/davidlueng986-alt/123321/actions/runs/41334225851
- All 1,951 outside points are blocked. Exact min/max secants per outside point: 10/56.
- Proof: secants through a fixed external point form disjoint pairs in the cap; adding one external point requires removing at least 10 old points.
- Fixing the first two 112-point slices leaves exactly 12 permissible third-slice points (the original 12). Any alternative third-slice point requires at least 11 removals from the first two slices.
- Reproducible analysis: RESULTS_2026-11-02.md; generate_calderbank_fishburn.py; analyze_secants.py; analyze_slices.py.
- Next: coordinated >=10-point reconstruction; do not spend cycles on single-point swaps.

## 2026-11-02 | CAP-002A exact outsider-pair cover audit | VERIFIED COMPUTATION
- Enumerated all 1,902,225 unordered pairs of points outside published 236-cap.
- For each pair, combined their secant matchings; if their own third point lay in the old cap, forced its removal. The union is alternating paths/even cycles, so exact minimum vertex cover per component is floor(number of vertices / 2). Computed minimum deletions required for each pair.
- Exhaustive integer result: global minimum deletions to add any TWO outsiders = 16, attained by 888 outsider pairs. GitHub run: https://github.com/davidlueng986-alt/123321/actions/runs/41334968239
- Second method: independent SciPy HiGHS MILP solved one 16-case and 100 fixed-seed additional outsider pairs; results supported the minimum 16, but this sampled check is not a second all-pairs proof.
- Necessary constraint near THIS 236-cap: to improve total size by any edit, delete at least 16 originals and insert at least 17 outsiders. Not a global bound on r3(7).
- Restricted-model pilot: 24 outsiders with 10 secants each, at least one outsider required; SciPy/HiGHS found certified optimum after deleting 10 and inserting 1, resulting in 227 points. This is an intentionally restricted feasibility benchmark, not a competitive search result.
- Code: analyze_pair_replacement.py, audit_pair_milp_spotcheck.py, reconstruction_milp.py.
- Next CAP-002C: explore structural pools of >=17 outsiders and exact MILP/SAT reconstruction; avoid simple greedy/small-radius swaps.

## 2026-11-02 | CAP-003D Campaign 001 integration + exhaustive fiber structure | VERIFIED COMPUTATION / INCONCLUSIVE SEARCH
- User supplied the evolving Drive Research Log 001, whose Research Log 003 links independent Math Agent Campaign 001 v2.0. Sources: https://docs.google.com/document/d/1DmvhnazPwH5NkXSqEI5DZoSQwDkr7p6sozJBVIV1o-I and https://docs.google.com/document/d/1_TWv6RzjYtBHJCawC6aT-q4ulBBdKuFaR7_nUaWp7lY
- Cross-reproduced the original 236-point 7D cap and constructed the known Edel Property-(ER) 496-point 8D cap. Independently verified 496 with exact cap checker. This is BELOW the reported 512-point 8D record.
- Independently enumerated all 1,093 7D and 3,280 8D projective hyperplane normals. Checked 7D 12 slice-spectrum types, Parseval second-moment integer sum 20,445,388, with 1 direction of (112,112,12) and 16 directions of (96,96,44). Checked 8D 17 spectrum types, Parseval 269,980,240, with two directions (236,236,24). CI: https://github.com/davidlueng986-alt/123321/actions/runs/41337974694
- Source-report caveats: scripts capset_swarm_solver.py and capset_verified_witnesses_2026_11_01.json referenced by the other agent were not located in its Drive experiments folder; its 240-group C6 magic basis, 252-vector admissible witness and 480D recursive theorem were not independently verified in this run. CP-SAT 'optimal' in a symmetry-constrained subfamily is NOT global optimality.
- Full 189 coordinate codimension-2 5D-fiber audit: 165 admit no exterior point if all outside original points frozen; 24 admit exactly one. In particular none of the nine x1/x2-aligned 243-point fibers releases any new exterior point. With k=2 of these aligned fibers: 20 pairs permit no outsiders, 8 permit one, 8 permit two; with k=3 up to 21, k=4 up to 138. Check: fiber_saturation_certificate.py.
- Exact reconstruction MILP with ALL frozen original points and unrestricted newly admitted points in each released k-fiber union. Eight promising k=3 and eight k=4 combinations solved to certified OPTIMAL final cap size exactly 236, and solutions replayed with independent exact triple checker. CI: https://github.com/davidlueng986-alt/123321/actions/runs/41337854727
- k=5 attempt imposing candidate cap >=237: 653 binary variables, 34,900 constraints; HiGHS reached 12-second time limit with no primal solution or infeasibility certificate. Explicit status INCONCLUSIVE, not an exclusion result. CI: https://github.com/davidlueng986-alt/123321/actions/runs/41338120217
- Prior independent integer/rational certificates also passed CI: symmetry subgroup size 3,840, 14 outsider orbits, 16-removal isolation; no-enlargement weighted duals for particular 48, 71 and 116 outsider candidate pools. CI: https://github.com/davidlueng986-alt/123321/actions/runs/41337166017
- Global necessary condition (uses known r3(6)=112): any hypothetical |A|>=237 cap has at least 13 points in EACH of its 3,279 affine hyperplanes. The Parseval square identity by itself holds for all sets and does not prove a cap upper bound.
- Next CAP-004: bring in independent 112-cap automorphism/orbit templates, introduce 27-block twist and structured search involving >=5 fibers. Avoid broader MILP with no symmetry reduction unless bounded research objective is explicit. Preserve evidence, negative results, and a proper novelty audit.

## 2026-11-01 18:54 UTC | CAP-004B 240-invariant orbit optimum | VERIFIED COMPUTATION
- Built an exact no-solver certificate for the **restricted** family of F3^7 caps invariant under the known order-240 signed-permutation group acting on six trailing coordinates (Paley magic-basis coordinates).
- Recovered 13 orbits of F3^6, 247 within-slice orbit-line classes and 1,195 ordered cross-slice orbit-line classes. Exactly 22 of 8,192 single-slice orbit unions are caps (max slice 112).
- Exhaustively checked all 253 unordered pairs of admissible slice masks; subset-max DP yields a rigorous **restricted optimum of 225**, attained by 112+112+1 (masks 530,3200,1). Rebuilt the 225 points and independently checked all triples by direct F3 arithmetic. This is NOT an upper bound on r3(7).
- CPU-only local run: `python /mnt/data/capset_c6_orbit_exact.py` (standalone reimplementation, ephemeral); durable replay: `python research/capset_f3_7/c6_invariant_exact_optimum.py` (pure stdlib, no seed). CI success: https://github.com/davidlueng986-alt/123321/actions/runs/41338916833
- Evidence: C6_INVARIANT_225_CERTIFICATE_2026-11-01.md. No >=237 witness and no stronger global bound. Source status still 236 <= r3(7) <= 291, with a separate 288 preprint claim.
- Meta-audit: Full 240 symmetry cannot produce 236 or 237. Change strategy to **proper subgroup** symmetry breaking and non-invariant 27-block twists; do not search this saturated orbit family further. Adjacent signed-relative template CI was separately green; do not confuse it with this theorem.

## 2026-11-01 19:53 UTC | CAP-004C index-two order-120 invariant exact optimum | VERIFIED LOCAL COMPUTATION; CI PENDING
- Continued after CAP-004B's full 240-group optimum=225; read current STATE/LOG/BACKLOG, latest CI and signed-template commits. No rerun of already excluded full-group family.
- Built canonical index-two subgroup of even coordinate permutations inside the verified 240-element signed-permutation stabilizer. Verified 120 elements, parity(permutation)=parity(sign-mask), 21 six-dimensional orbits.
- Exact orbit-line enumeration: 780 within-slice classes, 4,089 ordered cross-slice classes. Enumerated 174 valid single-slice orbit masks (maximum 112 points).
- Exhaustive 3-slice optimization via 2^21 subset-max DP and cross-shadow: all 15,225 unordered mask pairs covered, 7,598 explicitly evaluated; remaining pairs safely pruned using the proven third-slice upper bound 112. Exact restricted optimum **236** with masks (462848,344128,1048576), slice sizes (112,112,12).
- Reconstructed full 236-point witness and independently checked all unordered pairs by direct mod-3 arithmetic in a separate local scratch implementation (PASS; CPU ~3.6 seconds, deterministic, no seed/GPU). Repo script calls separate `verify_capset.verify`; branch CI workflow now runs it. **CI green not yet asserted at log time**.
- Code: `c6_even120_invariant_exact_optimum.py`; report: `C6_EVEN120_236_CERTIFICATE_2026-11-01.md`. Reproduce: `python research/capset_f3_7/c6_even120_invariant_exact_optimum.py`.
- Recent preexisting concurrent branch commits also independently excluded >236 in 1,920 signed images of complementary 112-cap pairs (CI 41339098901), and checked related Hill 112-cap pairs (CI 41339111555); do not confuse with this subgroup theorem.
- **Scope:** exact optimum in ONE order-120-invariant family only. No >=237 witness, no stronger global upper bound, no proof of r3(7). Novelty relative to external literature not established. Literature status cross-check: Thackeray arXiv:2206.09804 (288 claim); Versluis 2017 (291); public status still open.
- Meta-audit: reducing symmetry from 240 to 120 raises restricted optimum from 225 to 236, but this 120 group still cannot reach 237. Next CAP-004D: proper subgroups of 120 or 27-block affine twists; bound model size before CPU search. Do not spend time on full-240 or even-120 invariant families again.
