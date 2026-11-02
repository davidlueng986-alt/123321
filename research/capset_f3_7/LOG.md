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

## 2026-11-01 19:55 UTC | CAP-004C CI confirmation | VERIFIED COMPUTATION
- GitHub Actions run https://github.com/davidlueng986-alt/123321/actions/runs/41344134381 completed SUCCESS at commit 6d103c4b2c8cb46f98db99604f42062c04b7c3d7, including new exact order-120 orbit script in the branch-specific workflow. This upgrades CAP-004C from local verified / CI pending to CI GREEN. The exact theorem remains restricted; global r3(7) remains OPEN.

## 2026-11-01 21:00 UTC | CAP-004D subgroup-lattice | VERIFIED LOCAL EXACT GROUP AUDIT; CI PENDING
- Continued from CAP-004C CI-green optimum 236 (order-120 invariance), after reading STATE, LOG, BACKLOG, Drive ledger and folder, latest dedicated branch commit, and literature status. Tested the proposed order-60/40/24 subgroup directions *before* expensive cap search.
- Standalone CPU-only, deterministic arithmetic probe `python /mnt/data/capset_subgroup_probe.py` (ephemeral scratch, no seed) recovered |E|=120, derived subgroup |[E,E]|=60, derived perfect, center size 2, trivial intersection. Order distribution of E: {1:1,2:31,3:20,5:24,6:20,10:24}.
- Falsified an initial hypothesis: E itself is NOT perfect (derived order 60, not 120); corrected the proof. Exact finite-group deduction: no subgroup of order 40 (index 3), because every transitive E->S3 coset action would factor through C2. An order-60 subgroup DOES exist, but its 21 orbits on all 729 points of F3^6 coincide exactly with E's 21 orbits. Therefore order-60 invariant 7D caps are precisely the already-exhausted order-120 invariant caps, and their restricted optimum is 236. The 60-orbit single-slice valid mask count is independently 174.
- Constructed an explicit order-24 subgroup (generated by elements of orders 3 and 2 in the derived subgroup plus central involution). Its F3^6 action has 45 orbits: sizes 1×1, 6×4, 8×4, 12×16, 24×20; 33 individual orbits are cap-valid. Raw 2^45 subset-max DP is not viable.
- Durable certificate script: `c6_subgroup_lattice_certificate.py`; proof/audit: `C6_SUBGROUP_60_24_CERTIFICATE_2026-11-01.md`. Command: `python research/capset_f3_7/c6_subgroup_lattice_certificate.py`; CI workflow now executes it, run https://github.com/davidlueng986-alt/123321/actions/runs/41349642936 (status to be rechecked).
- Meta-audit: order 60 gives NO additional search freedom, order 40 impossible, order 24 is first substantive symmetry relaxation among these three but has high orbit-mask complexity. CAP-004E must first quantify conflict-hypergraph pruning / SAT feasibility; otherwise pivot to 27-block affine twisting. No >=237 witness; no global upper bound improvement; literature novelty not established. Global r3(7) OPEN.

## 2026-11-01 21:01 UTC | CAP-004D CI confirmation | VERIFIED COMPUTATION / CI GREEN
- GitHub Actions https://github.com/davidlueng986-alt/123321/actions/runs/41349642936 completed SUCCESS at commit 1087b11c03e386a7dff293598821966a1b9321c8, including the new `c6_subgroup_lattice_certificate.py` step and existing independent 236-point verifier and CAP-004C exhaustive order-120 theorem. This upgrades CAP-004D from local-only to CI-GREEN. No global r3(7) result.

## 2026-11-01 21:03 UTC | CAP-004E order-24 high-slice exhaustive pilot | VERIFIED LOCAL EXACT ENUMERATION; CI PENDING
- Extended CAP-004D's explicit 24-element subgroup to a bounded, exhaustive high-slice theorem. Enumerated 3,556 distinct forbidden within-slice orbit masks on 45 orbits; 12 orbits individually contain a line. Exact recursive include/exclude search on remaining 33 orbit variables visited 87,862 nodes and found exactly 11,434 cap-valid single-slice masks (max 112).
- Of those masks, exactly 48 have size 112 and 96 have size 104; hence exactly 144 have size >=104. Exhaustively tested all 10,440 unordered pairs of such high slices with exact 6D cross-sum shadows, choosing the largest permitted third cap-valid orbit mask. **Restricted optimum = 236**, witness slice sizes 112+112+12. Largest third slice across the 10,440 pairs was 16.
- Independent direct coordinate-level 7D mod-3 checker PASS on reconstructed 236 witness (27,730 unordered pairs); no >=237. Pure CPU stdlib, deterministic/no seed. Local scratch command `python /mnt/data/capset_order24_highpairs.py` (~15–17 seconds; ephemeral); durable `python research/capset_f3_7/c6_order24_high_slice_exact.py`, included in branch-specific GitHub CI workflow. Report `C6_ORDER24_HIGH_SLICE_236_CERTIFICATE_2026-11-01.md`; CI https://github.com/davidlueng986-alt/123321/actions/runs/41349990526 (pending at write time).
- **Scope limitation:** proves only order-24-invariant caps with at least two of three slices >=104 have size <=236. Remaining 65,373,895 unrestricted unordered pairs of 11,434 slice masks have NOT been searched. Thus no order-24 full optimum and no global r3(7) bound.
- Meta-audit: initial 2^45 complexity fear overstated (conflict propagation leaves 11,434 masks quickly), but 65M pairs still require better upper bounds / shadow caching / branch-and-bound; alternative non-invariant 27-block affine twists remain live. No literature novelty claim.

## 2026-11-01 21:05 UTC | CAP-004E CI confirmation | VERIFIED COMPUTATION / CI GREEN
- GitHub Actions https://github.com/davidlueng986-alt/123321/actions/runs/41349990526 completed SUCCESS at commit b707e064080257e6f03d07c9517fea630475a6b5. It executes `c6_order24_high_slice_exact.py` (11,434 valid masks, 10,440 exact high-slice pairs, optimum 236) plus the independent 7D verifier and all earlier branch checks. The theorem is restricted to order-24-invariant caps with at least two slices >=104; no global r3(7) upper bound.

## 2026-11-01 21:56 UTC | CAP-004F exact order-24 SAT encoding | COMMITTED; CI PENDING
- Continued from CAP-004E (10,440 high-slice pairs CI green). Full 24-group search was still open (65,373,895 pairs); no extrapolation from high-slice theorem.
- Derived a bijective exact CNF encoding for **all** 24-invariant 7D caps: 3×45=135 primary orbit variables; within-slice line conflicts and cross-slice 0/1/2 orbit triples, with a weighted threshold >=237 via Tseitin DP. This covers low-slice families missed by CAP-004E. SAT/UNSAT has NOT been decided.
- Added deterministic stdlib CNF generator, direct mod-3 verification of the known 236 witness, clause evaluation for target 236 (all satisfied) and 237 (only target objective fails), and GitHub CI artifact export. No GPU, no solver, no randomness. Commands: `python research/capset_f3_7/c6_order24_sat_encoding.py --target 236`; `python research/capset_f3_7/c6_order24_sat_encoding.py --target 237 --out /tmp/capset_order24_target237.cnf`.
- CI pending at commit time; any failed CI must be debugged before accepting the encoding. No >=237 witness, no restricted UNSAT certificate, no global bound improvement. Novelty not established; exact SAT encoding is a standard reduction.
- Meta-audit: SAT may replace 65M Python pair checks, but a solver's UNSAT return alone is insufficient: require independently replayed proof. Keep non-invariant affine twists and global upper-bound research alive.

## 2026-11-01 22:00 UTC | CAP-004F CI confirmation | VERIFIED ENCODING ONLY / DECISION OPEN
- GitHub Actions https://github.com/davidlueng986-alt/123321/actions/runs/41354696903 SUCCESS at commit d4bcab974cd5703119c7671afe868ac202846863, including exact orbit SAT generator and independent 236-point checker.
- Measured: 45 orbits, 135 primary variables, 3,556 within-slice forbidden orbit sets, 20,313 cross-slice ordered orbit triples; 30,981 structural clauses. Target-237 DIMACS: 30,241 total variables (30,106 auxiliary), 149,028 clauses. SHA256: 322eba0828cbfdd9809074bf579d7fdae70b25695bdfef4592c76203f4eb34a6. CI artifact: https://github.com/davidlueng986-alt/123321/actions/runs/41354696903/artifacts/13102867770 (30-day retention).
- Target-236 model replay: 30,121 variables, 148,549 clauses, known 236 witness satisfies ALL clauses; same witness fails exactly the objective clause of target-237. This does NOT decide target-237 satisfiability. No solver run, no UNSAT proof, no >=237 witness, no global bound.
- Literature recheck: Versluis 2017 291 published thesis bound; Thackeray arXiv:2206.09804 claims no 289-cap, hence <=288 if proof correct; 2026 Grace/Voloch algebraic complete-cap paper not a new 7D maximum. Novelty of this encoding not established.


## 2026-11-01 22:49 UTC | CAP-004G complete order-24 invariant exact optimum 236 | LOCAL EXACT COMPUTATION, CI PENDING
- Continued from CAP-004F (237-target CNF encoding CI GREEN, SAT/UNSAT unknown), reading the current GitHub STATE/LOG/BACKLOG, Drive ledger/folder, subgroup scripts, prior CI and latest literature. Did not rerun excluded order-240/120/60 searches.
- Key exact reduction: 11,434 valid orbit-union masks in each 6D slice; affine permutations of the three slices allow ordering weights wA>=wB>=wC. A >=237 witness requires wA+2*wB>=237 and 237-wA-wB<=wC<=wB. Cross-slice shadow and bitset incidence exhaust ALL possible third masks, not just the >=104 high-slice case.
- Independent local scratch reconstruction of order-24 orbits and forbidden triples: 45 orbits, 3,556 forbidden masks, 11,434 valid masks. Full deterministic CPU C++17 (-O3) finite enumeration covered 65,373,895 unordered slice-mask pairs; 3,436,063 visited, 3,424,629 passed safe weight gate and were checked exactly. Result: NO >=237 cap in the FULL specific order-24-invariant family. Runtime ~14.0 seconds for C++ check plus ~1.5 seconds input generation; no seed/GPU/paid compute.
- Known 236-point order-120 witness is also order-24 invariant; direct mod-3 coordinate verifier PASS. Therefore **restricted exact optimum =236**. This is NOT a global r3(7) upper bound and NOT a new 237 construction.
- Durable scripts: c6_order24_full_exact_data.py, c6_order24_full_exact.cpp, test_c6_order24_full_exact.py; report C6_ORDER24_FULL_EXACT_236_CERTIFICATE_2026-11-01.md. CI push triggered, confirmation pending; do not claim CI GREEN until checked.
- Falsified strategy: solving the CAP-004F order-24 SAT instance is no longer needed to decide this restricted family (it can serve as independent proof audit). Pivot CAP-005B toward genuinely non-invariant 27-block affine twists, smaller symmetry and certified global upper bounds. Literature novelty not established; global exact r3(7) remains OPEN. External 236/291 status page (2026-10-03) and Thackeray 288 preprint rechecked.

## 2026-11-01 | CAP-005A | exact 27-fiber reconstruction barrier | LOCAL CPU PASS, CI PENDING
- Prior CAP-004G GitHub Actions 41359681030 is SUCCESS; its complete order24 restricted optimum=236 is CI green.
- Independently replayed known 236 cap via exact mod-3 checker; 1951 outsiders, 10..56 original secants per outsider.
- Exhaustively enumerated 27+351+2925+17550=20853 choices of <=4 released coordinate F3^4 fibers (indexed by first three coordinates). Outsider admissibility requires each original secant to touch a released fiber.
- Complete histograms k1 {0:27}; k2 {0:335,1:16}; k3 {0:2501,1:408,2:8,4:8}; k4 {0:12510,1:4320,2:408,4:160,5:96,6:56}. Max outsiders 0,1,4,6.
- Every outsider requires >=10 deletions from the original cap, so no replacement confined to <=4 fibers can improve 236. This is NOT global r3(7) progress; literature novelty unverified.
- Scratch run deterministic CPU ~2.6 s, no seed, GPU, paid compute, or optimizer. Code cap005_27_fiber_barrier.py, test_cap005_27_fiber_barrier.py; report CAP005_27_FIBER_BARRIER_2026-11-01.md. CI pending for this commit.
- Meta-audit: pure translations of fixed fiber patterns preserve 236 size. Pivot to >=5 released fibers or occupancy-changing non-invariant templates; keep global upper bound research distinct.

## 2026-11-01 | CAP-005A CI + CAP-005B k=5 necessary gate | GREEN / LOCAL PILOT
- CAP-005A GitHub Actions https://github.com/davidlueng986-alt/123321/actions/runs/41364610380 SUCCESS, including new independent direct mod-3 fixture and exhaustive <=4-fiber unittest.
- Bounded CPU-only exploratory extension: 80,730 five-fiber release sets. Necessary-only outsider counts histogram {0:44392,1:25872,2:5384,3:344,4:1434,5:1576,6:1136,7:152,9:128,10:152,11:32,12:16,13:32,14:40,15:16,18:8,20:8,22:8}. Eight sets permit 22 outsiders; so the <=4 simple obstruction does NOT extend to five fibers by the same argument.
- Reproduction after this commit: python research/capset_f3_7/cap005_27_fiber_barrier.py --max-k 5. Local scratch ~7.4s including setup. CI for k5 extension pending. No witness >=237, no global upper bound.
- Next: test the eight maximizers with exact MILP/SAT including deletions and all triple constraints; timeouts inconclusive. Do not equate necessary candidate pool with a feasible cap.

## 2026-11-02 | CAP-005C | all five-fiber edits excluded by exact rational LP duals | LOCAL EXACT / CI PENDING
- Confirmed prior CAP-005B necessary-condition gate CI GREEN: https://github.com/davidlueng986-alt/123321/actions/runs/41364749101.
- Full 80,730 five-fiber release sets: 80,418 admit <=9 outsiders and are excluded by the already-certified >=10 original deletions needed for any outsider. The remaining 312 sets admit >=10 outsiders (max22).
- Constructed exact 7D triple constraints for each of these 312 released sets with other 22 fibers frozen; SciPy HiGHS proposed LP dual multipliers. Converted every nonzero dual to Fraction denominator<=1000 and independently checked y,z>=0, A^T y+z>=1, and exact b^T y+sum(z)<=original released count. All 312 PASS locally (~20s CPU).
- Therefore full restricted <=5-fiber optimum=236, **not** a global r3(7) upper bound. Source cap005_k5_rational_duals.py, report CAP005_K5_RATIONAL_DUAL_CERTIFICATE_2026-11-02.md. Command: python research/capset_f3_7/cap005_k5_rational_duals.py --out /tmp/cap005_k5_rational_duals.json (SciPy required). CI artifact of 312 rational duals pending.
- No GPU, paid compute, randomness, >=237 witness, or global improvement. Novelty unverified. Meta-audit: k5 necessary-only gate looked inconclusive, but rational LP duals close it; move to >=6 or nonlocal/global strategies.

## 2026-11-02 | CAP-005C CI confirmation — SUCCESS, 312 rational duals retained
- GitHub Actions https://github.com/davidlueng986-alt/123321/actions/runs/41365141220 SUCCESS for commit 515e1e7d4585855d7a3d1a1cdcf660708e5b235d.
- CPU-only workflow installed SciPy 1.16.3, recomputed all 80,730 five-fiber release sets and independently checked the exact Fraction dual inequalities for each of the 312 LP subproblems. No floating-point LP status is accepted as proof without exact dual verification.
- Artifact of all 312 duals: https://github.com/davidlueng986-alt/123321/actions/runs/41365141220/artifacts/13107126157 (GitHub Actions retention 30 days). The generator and exact checker remain durable in source code after artifact expiry.
- Restricted optimum 236 for <=5 coordinate 4D-fiber edits. No >=237 witness, no global upper bound improvement, no literature novelty claim. Continue campaign.

## 2026-11-02T00:53:46.828Z | CAP-005D six-fiber secant matching and exact census | LOCAL EXACT PASS; CI PENDING
- Read latest dedicated GitHub STATE/LOG/BACKLOG, current Drive ledger/folder, latest branch head df7364c, and checked relevant current literature. Continued from CAP-005C CI-green, not from scratch.
- Proved the nonlocal secant fiber pairs for any outsider form a matching under g -> -f-g on F3^3. Exact CPU census over all C(27,6)=296,010 six-fiber release sets: 288,878 have <=9 individually admissible outsiders, so the preexisting 10-deletion barrier rigorously excludes improvement; 7,132 remain unresolved. Maximum admissible outsiders 92, in 16 sets; 1,072 sets have >=20. k=5 regression exactly matches previous CAP-005C counts. All 16 max groups independently checked by uncompressed original secant-edge masks. No >=237 witness, no global bound.
- Additional bounded MILP pilot on three max-92 groups returned infeasible in SciPy/HiGHS (164 variables, 2050 constraints; each <0.1 s local), BUT NO independently checkable UNSAT certificate: record as non-certifying exploration only. LP relaxation 82 versus 72 original released, so naive fractional dual cannot exclude these groups.
- Reproduce: python research/capset_f3_7/cap005_k6_secant_matching_gate.py --out /tmp/cap005_k6_gate.json ; python research/capset_f3_7/cap005_k6_milp_pilot.py --time-limit 5 ; python -m unittest discover -s research/capset_f3_7 -p 'test_cap005_k6_secant_matching_gate.py' -v. Deterministic, no seed, CPU-only, no GPU or paid compute.
- Files: cap005_k6_secant_matching_gate.py, cap005_k6_milp_pilot.py, test_cap005_k6_secant_matching_gate.py, CAP005_K6_SECANT_MATCHING_GATE_2026-11-02.md. CI pending. Literature novelty unestablished; exact global r3(7) OPEN. Next rank 7,132 surviving neighborhoods, seek exact proof certificates, and keep nonlocal construction/global-upper-bound lines alive.

## 2026-11-02T00:56:16.447Z | CAP-005D CI confirmation | EXACT NECESSARY GATE CI GREEN
- GitHub Actions https://github.com/davidlueng986-alt/123321/actions/runs/41369606221 SUCCESS at commit c88dde3cac38f75cad8c06068f844876cb2e1d91; exact verifier unit tests, full C(27,6) census, k5 regression, independent direct secant checks, and JSON artifact preservation all passed. Artifact https://github.com/davidlueng986-alt/123321/actions/runs/41369606221/artifacts/13109056258. Counts: 296010 sets, 288878 excluded by the existing ten-deletion gate, 7132 unresolved, maximum individually admissible 92 in 16 sets. Scope remains necessary-only for six specified fibers, not a full six-fiber optimum or global bound. The exploratory MILP statuses are not independently certified. r3(7) OPEN, no >=237 witness.

## 2026-11-02T01:51:49Z | CAP-005E six-fiber pair-removal gate | LOCAL EXACT PASS; CI PENDING
- Read dedicated GitHub STATE/LOG/BACKLOG, current Drive ledger and folder, latest CI (CAP-005D success 41369606221), and fresh literature. Continued from CAP-005D.
- Reused CAP-002A exact pair-removal lemma, independently reimplemented in C++17: all 1,902,225 outsider pairs, minimum 16 baseline removals, 888 pairs attaining 16; direct 236-point mod-3 cap check. Local C++ compile/run PASS ~2.12s, deterministic CPU only.
- CAP-005D six-fiber exact histogram re-evaluated locally: 294,394 of 296,010 release sets have <=16 individually admissible outsiders, so cannot improve 236; this adds 5,516 rigorous exclusions over the previous 288,878 <=9 gate. Only 1,616 remain unresolved (77.34% reduction). Local Python census ~20s, deterministic CPU.
- Proof: any improvement adding >=2 outsiders must delete >=16 originals; <=16 insertions cannot increase 236. A single outsider forces >=10 deletions. N(T)>=17 is necessary only, not sufficient.
- Code: cap005_pair_cover_independent.cpp, cap005_k6_pair_gate.py; report CAP005_K6_PAIR_GATE_2026-11-02.md. CI pending; no >=237 witness, no global upper bound, novelty not established.
- Meta-audit: CAP-005D neglected an already-certified stronger pair lemma. Focus on 1,616 surviving neighborhoods and certified UNSAT proofs, while separately exploring nonlocal constructions and global upper bounds. The previous three MILP infeasible reports remain noncertifying.
