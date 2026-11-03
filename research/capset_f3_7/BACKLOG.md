## CAP-036 (2026-11-03 UTC)
- [LOCAL EXACT / CI PENDING] CAP035 full CI 41586983947 SUCCESS. Fixed CAP027 occupancy has trivial affine monomial quotient stabilizer (31,104 maps exhaustively checked); do not assume translation or coordinate-permutation symmetry of conditional SAT instance. See CAP036 code/report.
- [P0] CPU-bounded proof-logged SAT on CAP035 CNF with independent SAT witness or UNSAT certificate checking; timeout UNKNOWN. Explore full AGL4 and internal-fiber symmetries only with proof of preservation.
- [P1] CAP019/Thackeray classification referee and >=237 construction; exact r3(7) OPEN.

## CAP-034 (2026-11-03 UTC)
- [EXPLICIT LOCAL SAT WITNESS; CI PENDING] Two unique CAP027 special lines (7,6,6) and (7,7,4) sharing 0000 fiber ARE jointly realizable: 30-point F3^7 cap on five fibers. See cap034_shared_two_lines_witness.py and CAP034 report. Two-line-only contradiction hypothesis FALSIFIED.
- [P0] Check CI; extend to connecting quotient lines or all 81 fibers via bounded proof-logged shared-variable SAT/PB. UNSAT needs independently checked proof, timeout UNKNOWN.
- [P1] CAP019/Thackeray 110-cap classification referee; balanced/no-112; >=237 lower-bound search. Exact r3(7) OPEN.


## CAP-033 (2026-11-03 UTC)
- [LOCAL EXACT; CI PENDING] CAP027 formal285 has unique 766 and 774 quotient lines sharing 7-fiber 0000; force non-9-extendable 7-cap orbit by CAP032C. See CAP033 report/checker. Not a global bound.
- [P0] Test simultaneous shared-fiber point-level compatibility for these two lines and then all 1080; bounded proof-logged SAT, UNKNOWN on timeout, independent proof/witness checker.
- [P1] Independently referee CAP019/Thackeray 110-cap classification; maintain balanced/no-112 and >=237 search.

## CAP-032 (2026-11-03 UTC)
- [ANALYTIC; CI PENDING] CAP027 occupancy has exact random-independent-fiber E[3AP]=131198/75, including 5207/3 cross-fiber. This is NOT an exclusion or probability bound. See CAP032 report and checker.
- [P0] Proof-logged shared-fiber SAT/PB pilot with exact occupancy, independent proof/witness validation; timeout UNKNOWN.
- [P1] CAP019 classification referee and balanced/no-111 branches; do not claim novelty.

## CAP-031 next gate (2026-11-03 ~01:55 UTC)
- [LOCAL EXACT PASS; CI PENDING] Verified 1080 quotient lines, 9477 internal and 787320 cross-fiber affine triples = 796797 total. Code cap031_factorization.py and report CAP031_SHARED_FIBER_EXACT_FACTORIZATION_2026-11-03.md.
- [P0] Instantiate CAP027 81-fiber occupancy as exact shared-variable CNF/PB, bounded proof-logged SAT. SAT must yield independently checked actual coordinates; UNSAT requires verifiable proof. Timeout is UNKNOWN. This excludes only a fixed occupancy, not all 285 caps.
- [P1] Continue CAP019/Thackeray hostile referee, balanced/no-111, nonlocal >=237 search. No novelty or global bound claimed.
## CAP-029 final CI verification (2026-11-03 00:04 UTC)
- [DONE / FULL CI GREEN] https://github.com/davidlueng986-alt/123321/actions/runs/41549413947 on code SHA 176a2d93ea2a99a48c98d3d30e8987d97f5a8707. All exact unit tests and CPU certificate steps passed. Preserve earlier failed CI runs as evidence.
- [P0] Next bounded mathematical work: simultaneous shared-fiber point-level constraints or independent Thackeray 110-cap completion referee; avoid repeating local count-only relaxations.

## CAP-029 CI regression follow-up (2026-11-02 ~23:58 UTC)
- [CI FAIL] 41549068067: repaired 19-point witness passes all six CAP-028 tests, but new extension-census regression test failed because check() asserts on invalid candidate instead of returning False. This is a test harness bug, not cap failure.
- [LOCAL FIX] Add admissible() catching AssertionError for invalid additions. Check next CI on the exact new commit before declaring success.

## CAP-029 CI failure referee and exact 4D witness repair (2026-11-02 23:52 UTC)
- [CRITICAL VERIFIED] CAP-028 CI 41542279551 **FAILED**: claimed W766 was 17 points (7,5,5), not 19 (7,6,6). Never promote failed CI as evidence.
- [LOCAL EXACT PASS / NEW CI PENDING] Enumerated all 81 F3^4 points: five single additions, three compatible pairs, unique balanced (7,6,6) pair = (1,1,2,0)+(2,1,2,1). Independent direct 1080-line check validates repaired 19-point cap and all 12 local profiles.
- [P0] Check full CI for this exact CAP-029 commit; if red, inspect logs and repair before new mathematical claims.
- [P1] Shared-fiber simultaneous 3AP compatibility, nonradical normal constraints, Thackeray 110-cap completion independent referee; continue balanced/no-111 and >=237 search.
- [META] Local 4D liftability of every quotient line does NOT establish a global 285-point 7D cap; r3(7) OPEN. No priority/novelty claim.

## CAP-007J global 89-slice theorem (2026-11-02 10:56 UTC)
- [EXACT ELEMENTARY PROOF / FULL CI GREEN run 41433674492] Every hypothetical 237-cap in F3^7 has an affine 6D hyperplane containing >=89 points. Exact 2nd/3rd moment contradiction -35,076 if all slices<=88; independent 236-witness JS moment replay; Python 9-cap regression and 75-profile exhaustive check. Proof/script/test: CAP007J_HYPERPLANE_THIRD_MOMENT_89_GATE_2026-11-02.md, cap007j_hyperplane_moment_gate.py, test_cap007j_hyperplane_moment_gate.py.
- [P0] Confirm new CI with 236-point regression fixture; if failure, diagnose before promoting. CAP-007I is **separate** concurrent 5922-transform 112+112 additive-hole experiment, do not overwrite or conflate.
- [P1] For global slice-based proof, use necessary range 89..112; CAP-007H currently only addresses exactly112. Derive additional cap-specific fourth-moment / cross-slice constraints or classification cuts for 89..111, with exact proof certificates. Second+third moment alone cannot force90 even with integer direction multiplicities: 238*(59,89,89)+267*(76,78,83)+65*(76,79,82)+523*(77,80,80) exactly matches 1093 directions and both moments (formal histogram, not a cap).
- [META] This does NOT improve global bound 291 or prove existence of 237; literature novelty unverified. Avoid extrapolating the 112-slice conditional model or restricted local neighborhoods to all caps.

## CAP-005G rational LP duals (2026-11-02 03:58 UTC)
- [LOCAL EXACT PASS / CI PENDING] 848 additional six-fiber neighborhoods have exact-rational LP dual certificates independently checked by mod-3 arithmetic. Cumulative restricted exclusions 295,922 / 296,010; 88 remain unresolved. Local artifact SHA256 0a49469949dca1e9a55e6cffab62306eec7a0e9f9e9bace17289e1e26bd4e7db (SciPy version may change certificate).
- [P0] Confirm GitHub CI and 848-dual JSON artifact; on failure inspect checker/solver rather than counting exclusions.
- [P0] Attack 88 positive LP-gap cases with exact rational cutting planes, outsider-triple and deletion-cover inequalities, certified SAT/UNSAT or independent >=237 witness. LP gap is not evidence of feasible cap.
- [P1] Nonlocal occupancy-changing constructions and independently certifiable global upper bounds; local 6-fiber results cannot settle r3(7). Literature novelty unverified.

## CAP-005F CI confirmation (2026-11-02 02:59 UTC)
- [DONE / CI GREEN https://github.com/davidlueng986-alt/123321/actions/runs/41380252670] 680 exact independently checked clique certificates archived: https://github.com/davidlueng986-alt/123321/actions/runs/41380252670/artifacts/13113456508; 295,074 / 296,010 six-fiber edits excluded, 936 unresolved. JSON SHA256 12bf1b9787390691072e6b627afaf73fa44fcab3db13c35479d004fa57bb830f.
- [P0] 936 survivors: exact outsider-triple hypergraph constraints / deletion-cover certificates, and nonlocal constructions; do not infer a global bound from restricted local searches.

## CAP-005F fixed-original-point conflict clique certificates (2026-11-02 02:54 UTC)
- [LOCAL EXACT / CI PENDING] 680 of CAP-005E's 1,616 surviving six-fiber edits have a verifiable partition of all eligible outsiders into <=16 cliques of pairwise incompatibility. Independently replayed exact mod-3 certificate; 295,074 / 296,010 excluded in total; 936 unresolved. Certificate generator + independent checker + CI artifact added.
- [P0] Confirm GitHub CI and archived 680-clique JSON SHA256 12bf1b9787390691072e6b627afaf73fa44fcab3db13c35479d004fa57bb830f; do not claim CI success prematurely.
- [P0] For 936 survivors, test outsider triple hypergraph constraints and exact rational deletion-cover inequalities; require verifiable proof certificates or verified witnesses.
- [P1] Parallel nonlocal constructions and certified global upper bounds. Restricted local barriers cannot determine r3(7). Novelty unverified.

## CAP-005E CI confirmation (2026-11-02 01:58 UTC)
- [DONE / CI GREEN https://github.com/davidlueng986-alt/123321/actions/runs/41374998772] Independent C++17 exact pair-cover and full six-fiber pair-aware necessary census passed; 294,394 excluded, 1,616 unresolved.
- [P0] Seek independently checkable UNSAT certificates for 1,616 surviving neighborhoods; avoid unverified MILP infeasibility claims.
- [P1] Nonlocal 27-block occupancy-changing constructions and globally valid upper bounds. The global problem remains OPEN.

## CAP-005E pair-removal gate (2026-11-02 01:51 UTC)
- [LOCAL EXACT / CI PENDING] Independently recomputed CAP-002A 16-removal minimum over all 1,902,225 outsider pairs with new C++17 arithmetic/DSU verifier; 888 pairs attain 16.
- [LOCAL EXACT / CI PENDING] Applied >=17 insertions necessary for improvement to full CAP-005D six-fiber histogram: **294,394 / 296,010** release sets rigorously excluded, **1,616** unresolved; 5,516 additional exclusions (77.34% of previous unresolved).
- [P0] Certify >=237 UNSAT or reconstruct a witness in 1,616 survivors; prioritize low N=17..24 and high-N=92 classes using exact branch-and-bound, LRAT/DRAT or rational cutting planes. No MILP status without certificate counts.
- [P1] Explore nonlocal occupancy-changing templates and rigorous global upper bound. Restricted local barriers cannot determine r3(7). Novelty not established.

## CAP-005C CI confirmation (2026-11-02 00:06 UTC)
- CAP-005C [DONE / CI GREEN https://github.com/davidlueng986-alt/123321/actions/runs/41365141220] All <=5 coordinate 4D-fiber reconstructions rigorously excluded from improving 236. 312 exact-rational dual certificates archived in https://github.com/davidlueng986-alt/123321/actions/runs/41365141220/artifacts/13107126157. This is a local restricted theorem, not global.
- Next CAP-005D [P0] At least six released 4D fibers, nonlocal occupancy-changing templates, or global structural inequalities; maintain rigorous certificates and independent checker.

## CAP-005C update (2026-11-02 00:02 UTC)
- CAP-005B [CI GREEN run 41364749101] Five-fiber necessary-only gate exactly reproduced; it did not by itself exclude 237.
- CAP-005C [LOCAL EXACT RATIONAL / CI PENDING] All 80,730 five-fiber edit neighborhoods excluded: 80,418 by <=9 outsiders vs >=10 deletions; 312 by independently rational-checked LP duals for full triple constraints. Restricted <=5-fiber optimum=236, not global. See cap005_k5_rational_duals.py and CAP005_K5_RATIONAL_DUAL_CERTIFICATE_2026-11-02.md; CI should publish 312 duals.
- CAP-005D [P0] Explore >=6 fibers or genuinely non-coordinate/nonlocal occupancy-changing templates; do not repeat <=5 search.
- CAP-007 [P1] Certified global upper bound remains essential; preprint 288 not independently audited.
- META-AUDIT: Strong local rigidity does not determine r3(7). Novelty unverified.

## CAP-005B five-fiber pilot (2026-11-01 23:59 UTC)
- CAP-005A [CI GREEN run 41364610380] Rigorous <=4-fiber no-improvement theorem confirmed.
- CAP-005B [LOCAL EXACT NECESSARY GATE; CI PENDING] All 80,730 five-fiber releases examined; 8 admit 22 outsiders, so simple secant/deletion bound no longer excludes improvement. This is not a feasible 237 construction. Replay --max-k 5; prioritize these 8 for exact SAT/MILP with full triple constraints and independent witness verification.
- META-AUDIT: 4-fiber gate is a theorem; 5-fiber gate only candidate filtering. Avoid extrapolating from the former.

## CAP-005A update (2026-11-01 23:54 UTC)
- CAP-004G [CI GREEN] Full order24 invariant exact optimum=236 confirmed in run 41359681030; stop duplicate SAT exploration for discovery.
- CAP-005A [LOCAL EXACT / CI PENDING] All 20,853 release sets of <=4 first-three-coordinate F3^4 fibers: max admissible outsiders 0/1/4/6 for k=1/2/3/4. Since any outsider forces >=10 original deletions, cannot improve 236 inside <=4 such fibers. This is a restricted reconstruction barrier, NOT a global bound. See cap005_27_fiber_barrier.py and CAP005_27_FIBER_BARRIER_2026-11-01.md.
- CAP-005B [P0] Non-invariant occupancy-changing 27-block template, or exact >=5-fiber release constraints. Pure per-block translations preserve size and cannot produce 237.
- CAP-007 [P1] Independently certify a global upper bound. Published status 291; preprint 288 not independently reviewed.
- META-AUDIT: Avoid repeating symmetry-restricted searches and translation-only moves. Literature novelty still unverified; exact global r3(7) remains OPEN.

## CAP-004G update (2026-11-01 22:49 UTC)
- CAP-004G [LOCAL EXACT COMPUTATION / CI PENDING] Exhaustive full order-24-invariant 237 decision: 11,434 cap-valid slice masks, 65,373,895 unordered pairs covered; 3,424,629 pairs pass rigorous ordered-slice weight gate and are checked with exact cross-shadow bitsets. No >=237 cap; existing 236 witness independently direct-verified. **Full order-24-invariant optimum=236**, not a global r3(7) upper bound. Scripts: c6_order24_full_exact_data.py, c6_order24_full_exact.cpp, test_c6_order24_full_exact.py. Report: C6_ORDER24_FULL_EXACT_236_CERTIFICATE_2026-11-01.md. Recheck branch CI before marking GREEN.
- CAP-004F-SAT [DEPRIORITIZED] Existing 237-target CNF remains undecided by SAT solver, but its restricted decision is now settled by a separate exhaustive combinatorial computation; optional SAT UNSAT proof only for independent audit, not discovery.
- CAP-005B [P0] Pivot to genuinely non-order24-invariant 27-block affine twists, smaller stabilizers or asymmetrical template mixing. Must produce explicit >=237 candidate and independent 7D arithmetic check before any record claim.
- CAP-007 [P1] Investigate global upper bounds with cap-specific inequalities/certificates; preprint <=288 is not independently verified. Do not infer global bound from order24 exclusion.
- META-AUDIT: Order240, 120, 60, 24 invariant searches all now exhausted or redundant; future symmetry search must truly refine orbit partition and justify why it could reach 237. Literature novelty still unverified; exact global r3(7) remains OPEN.

## CAP-004F update (2026-11-01 21:56 UTC)
- CAP-004F-ENCODING [DONE / CI GREEN] Exact 135-primary-variable SAT reduction for **all** order-24-invariant F3^7 caps. Within-slice forbidden sets (3556) and cross-slice orbit triples; exact weighted cardinality >=237 via Tseitin DP. Deterministic CNF artifact generated in CI. Existing 236 model replayed by independent direct arithmetic checker. No SAT/UNSAT decision yet; no restricted or global upper bound established. See `c6_order24_sat_encoding.py` and `C6_ORDER24_SAT_REDUCTION_2026-11-01.md`.
- CAP-004G [P0] After CI, bounded CPU SAT attempt. If UNSAT, generate and independently check LRAT/DRAT certificate; if SAT, independently check all 7D points and check literature novelty. Solver timeout is inconclusive. Preserve CNF checksum and solver commands.
- CAP-005B [P0] Parallel non-invariant 27-block twists: full order-24 symmetry may still be too restrictive to reach >236.
- META-AUDIT: Encoding exactness is not solution of the decision problem. All global claims remain OPEN.

# CAPSET-F3-7 — Research Backlog (2026-11-02)

**Exact problem:** determine r3(7). External lower 236; accepted stated upper 291, preprint states 288; investigate each primary source again before announcing any novelty. Current independently verified best construction 236. A 237 construction is only a partial breakthrough.

## CAP-004E update (2026-11-01 21:03 UTC)
- CAP-004E [DONE / VERIFIED EXACT ENUMERATION, CI GREEN https://github.com/davidlueng986-alt/123321/actions/runs/41349990526] Explicit order-24 subgroup: 45 orbits, 3,556 internal forbidden orbit masks, 12 individually forbidden orbits, 87,862 recursive nodes, 11,434 cap-valid single-slice masks. Exactly 144 masks have size >=104 (48×112, 96×104). Exhaustive 10,440 unordered high-slice pairs yield restricted optimum **236** (112+112+12), independent direct arithmetic checker PASS. Script: `c6_order24_high_slice_exact.py`; report: `C6_ORDER24_HIGH_SLICE_236_CERTIFICATE_2026-11-01.md`. Does NOT exclude 237 in remaining order-24-invariant families.
- CAP-004F [P0] Full order-24 orbit search: 65,373,895 unordered valid-mask pairs before safe bounds. Build fast cross-shadow bounds, memoized max allowed third-slice weight and symmetry reductions; impose bounded CPU gate. Seek exact optimum only with complete coverage and certificate; timeouts inconclusive.
- CAP-005B [P0] Non-invariant 27-block affine twisting remains viable and may bypass all symmetry restrictions.
- META-AUDIT: 2^45 raw mask DP is unnecessary (11,434 valid masks after propagation); naive 65M pair enumeration is still excessive. Existing 10,440 high-slice pair exclusion is a proper restricted theorem, not global r3(7) progress.

## CAP-004D update (2026-11-01 21:00 UTC)
- CAP-004D [DONE / LOCAL EXACT CERTIFICATE; CI STATUS RECHECK] Derived subgroup of even120 has order 60, is perfect, and has EXACTLY THE SAME 21 F3^6 orbits as even120. Consequently its invariant 7D optimum is the already-certified 236. E has no order-40 subgroup (index-three coset-action proof). An explicit order-24 subgroup has 45 orbits (1×1,6×4,8×4,12×16,24×20), with 33 individually cap-valid orbits. See `c6_subgroup_lattice_certificate.py` and `C6_SUBGROUP_60_24_CERTIFICATE_2026-11-01.md`.
- CAP-004E [P0] For the explicit order-24 subgroup, build orbit-conflict hypergraph, count cap-valid slice masks using pruning, and set a strict CPU/complexity gate before cross-slice DP/SAT. Do NOT attempt raw 2^45 subset DP.
- CAP-005B [P0] Non-invariant 27-block affine twists and exact shadow feasibility remain parallel, since no subgroup-invariant family yet exceeds 236.
- META-AUDIT: Discard order-60 orbit search (same family as 120), discard nonexistent order-40 subgroup. The next meaningful symmetry relaxation is order24 or other genuinely orbit-refining subgroup. No >=237, no global bound, no novelty claim.

## CAP-004C update (2026-11-01 19:53 UTC)
- CAP-004C [DONE / VERIFIED COMPUTATION, CI GREEN] The canonical index-two even-permutation subgroup of the Paley 240-group has order 120 and 21 F3^6 orbits. Exact orbit-mask enumeration gives **restricted optimum 236** (174 valid masks, 15,225 unordered pairs with 7,598 safely evaluated; witness 112+112+12). Script: `c6_even120_invariant_exact_optimum.py`; report: `C6_EVEN120_236_CERTIFICATE_2026-11-01.md`. Independent direct checker PASS; CI https://github.com/davidlueng986-alt/123321/actions/runs/41344134381 SUCCESS. Not a global bound.
- CAP-004D [P0] Explore proper subgroups of this order-120 group, particularly order 60/40/24, but first compute orbit counts and SAT/DP feasibility. The 120-invariant family is exhausted; do not repeat it.
- CAP-005B [P0] Alternative: non-invariant 27-block affine twists, with exact shadow tests and explicit certificates.
- META-AUDIT: 240-invariant optimum 225 -> 120-invariant optimum 236. This is evidence that symmetry breaking matters, but neither family can contain a 237 cap. Check novelty before any public theorem claim. Global status OPEN.

## Completed — exact computational results

- CAP-001 [DONE] Reproduce original Calderbank–Fishburn 236 cap, 112+112+12 slices. Independent Python exact verifier and GitHub CI.
- CAP-002A [DONE] Secant saturation: 1,951 outsider points blocked, each on 10–56 secants; no edits with fewer than 10 deletions can add an outsider.
- CAP-002B [DONE] All 1,902,225 exterior pairs: min 16 originals must be deleted to admit a pair; 888 extremal pairs. 101 independent MILP spot checks. Follow-up symmetry-based complete enumeration of all minimum 16 deletion covers isolates exactly two outsiders.
- CAP-002C [DONE] Symmetry subgroup of order 3840, 14 exterior-point orbits, 3 orbits of min-16 outsider pairs; 48,71,116 candidate rational-dual exact certificates; six single-orbit no-improvement lemmas. Full checker in CI.
- CAP-003A [DONE] Independent reproduction of Google Drive Campaign 001 v2.0's 7D hyperplane spectrum (1,093 normals; 12 types; exact Parseval 20,445,388).
- CAP-003B [DONE] Independently reproduce known Edel 496-cap in 8D and verify 3,280-direction Parseval 269,980,240 with 17 slice types. 496 is not a new 8D record.
- CAP-003C [DONE] Exact 189 coordinate 5D fiber saturation audit: 165 zero-exterior, 24 one-exterior. Study aligned nine coordinate fibers (three 4D blocks each): top eight k=3 and eight k=4 reconstructions independently checked and certified optimum 236.
- CAP-003D [INCONCLUSIVE] First bounded k=5 MILP (653 binary vars, 34,900 constraints, 12 sec) for target total ≥237 timed out. No proof or witness. Larger neighborhoods demand structural reductions, not blind timeout increases.
- CAP-003E [DONE] Read Research Log 001, inspect Campaign 001 v2.0 report, reconcile verified and unverified claims. See AUDIT_CAMPAIGN_001_2026-11-02.md. Other agent's referenced executable solver and JSON witnesses were not found in the Drive experiment folder.

## CAP-004B update (2026-11-01 UTC)
- CAP-004B [DONE / VERIFIED COMPUTATION] Exact finite enumeration proves the maximum cap size in F3^7 **invariant under the full order-240 signed-permutation group** is 225. Counts: 13 orbits, 22 admissible single-slice orbit masks, all 253 mask pairs checked; independent 225-point arithmetic verifier; CI https://github.com/davidlueng986-alt/123321/actions/runs/41338916833. This is **not** a global r3(7) upper bound.
- CAP-004C [P0] Search proper subgroups of the verified 240 group (index 2/3/5 where they exist), calculate orbit decompositions, estimate SAT/MILP complexity, then run a bounded exact model. Do not repeat full-group orbit-union search.
- CAP-005B [P0] Test 27-block twisted constructions with controlled symmetry breaking and exact cross-shadow checks. A >=237 candidate needs a full explicit 7D witness and independent checker.
- META-AUDIT: Full 240 symmetry is provably too restrictive (225 < already known 236). The original unrestricted 236-neighborhood search also faces a >=16-removal barrier; focus on *structural* symmetry breaking rather than simply increasing CPU timeouts.
- Novelty classification: restricted theorem appears new to this branch, **not established as new in the mathematical literature**. Maintain global status OPEN and verified best 236.

## Next research decisions

- CAP-004 [P0] Independently reconstruct Campaign 001's 112-cap Paley Conference magic basis and C6 order-240 group orbits, if source code/witness can be obtained; verify their actual orbit sizes and that candidate cross-sum shadows are exact. Do not infer a new 237 result from 225/236 known caps.
- CAP-005 [P0] Implement 27-block coupled affine transforms with **twist/cross-shadow scoring** and exact line feasibility, using C6 templates instead of expanding arbitrary 653-variable MILPs. For each experiment, include full seed, source, duration, accepted/rejected candidate and certificate.
- CAP-006 [P1] Enumerate equivalence classes of promising k=5 fiber configurations using only verified subgroup actions; use symmetry-breaking and dual certificates to reduce states. Attempt an independent solver (CP-SAT) for a bounded target-237 instance; treat timeouts as inconclusive.
- CAP-007 [P1] Seek certified upper-bound improvement via Parseval coupled with genuinely cap-specific inequalities, e.g. slice-convolution shadows, moment constraints, polynomial/SDP dual proofs. Do not misrepresent Parseval (true for any point set) as a new cap upper bound.
- CAP-008 [P2] Formalize high-value structural lemmas or short rational dual certificates in Lean 4; require kernel checking and statement equivalence audit.
- CAP-009 [ONGOING] Read and reconcile Google Drive Research Log 001 + Cap Set ledger and own GitHub STATE.json each hourly cycle. Keep unrelated MOLS10 and other mathematical projects untouched.

## Decision rule

Each run must make one substantive tested hypothesis, mathematical computation, proof attempt, or falsification. Store exact reproducible evidence in this branch and a human-readable summary in the Drive ledger. Do not claim a world record unless independently verified and checked against the latest literature. Stop hourly project only if exact maximum r3(7) is rigorously settled with matching bounds and independent review, or user directs a stop.

## Old backlog snapshot

# Research backlog — CAPSET-F3-7

CAP-001 [DONE / VERIFIED COMPUTATION] Reproduced Calderbank–Fishburn 236 points from primary source; 236-line certificate, generator, independent verifier, 10-secants barrier and CI pass. See RESULTS_2026-11-02.md.
CAP-002 [PARTIAL] Deterministic seed=7 two-round greedy 136 verified by CI; no research claim. Reframe toward structured reconstruction using complete 236 witness.
CAP-003 [PARTIAL / VERIFIED COMPUTATION] With fixed 112+112 slices, exactly 12 third-slice points allowed. Every alternative third-slice point has >=11 disjoint cross-slice blockers. SAT encoding still TODO.
CAP-004 [P1/TODO] Affine symmetry/orbit structured search; test for repeated equivalent candidates.
CAP-005 [P1/TODO] Investigate certified upper-bound constraints and published 288 claim; independent source audit.
CAP-006 [P2/TODO] Formalize a verified candidate or structural lemma in Lean; require green CI and statement audit.

(Superseded by structured backlog above.)

## CAP-004F CI confirmation (2026-11-01 22:00 UTC)
- CI https://github.com/davidlueng986-alt/123321/actions/runs/41354696903 SUCCESS. Exact target-237 CNF: 30,241 vars / 149,028 clauses; 20,313 cross orbit triples; SHA256 322eba0828cbfdd9809074bf579d7fdae70b25695bdfef4592c76203f4eb34a6. 236 witness replay PASS. SAT status UNKNOWN; next bounded CPU SAT with proof production, not naive claim of UNSAT.

## CAP-005D update (2026-11-02T00:53:46.828Z)
- CAP-005D [VERIFIED EXACT NECESSARY GATE / CI GREEN https://github.com/davidlueng986-alt/123321/actions/runs/41369606221] Complete six-fiber necessary-only secant matching census: 296,010 release sets; 288,878 have <=9 admissible outsiders and are rigorously excluded by existing 10-deletion gate; 7,132 remain unresolved; max 92 admissible outsiders (16 groups). k5 regression and independent uncompressed secant checks pass. Script/report in dedicated branch; not a global bound and not an all-six-fiber theorem.
- CAP-005E [P0] Investigate 7,132 surviving six-fiber sets; first exploit affine-fiber symmetries to collapse equivalent cases. For representative 92-candidate groups, MILP says infeasible but is NON-CERTIFYING; produce independently checkable exact UNSAT/exhaustive certificate before any exclusion claim. High outsider counts are not cap witnesses.
- CAP-005F [P0] Do not overfit to fixed coordinate fibers: pursue genuinely nonlocal asymmetric 27-block template changes that can alter occupancy, and certified global upper-bound methods in parallel. Maintain global OPEN and 236 verified lower bound.

## CAP-005H update (2026-11-02 05:00 UTC)
- CAP-005G [CI GREEN] https://github.com/davidlueng986-alt/123321/actions/runs/41386314239 verifies 848 exact rational duals, leaving 88 six-fiber cases.
- CAP-005H [LOCAL EXACT / CI PENDING] A verified 16-element affine stabilizer acts on the 27 coordinate fibers. All 296010 six-fiber subsets collapse to 19464 orbits; the 88 unresolved are seven full orbits. Exact rational dual objectives 137/2 and 206/3 (<69) plus integrality eliminate two 16-element orbits, so 295954/296010 excluded, 56 remain in five orbits. See CAP005_K6_SYMMETRY_ROUNDING_2026-11-02.md. Do not promote until CI passes.
- CAP-005I [P0] Five remaining orbit representatives: (0,1,2,4,5,18), (0,1,3,4,5,18), (0,1,3,5,8,18), (1,3,5,7,8,18), (1,4,5,7,8,18). Find formal UNSAT proof/cutting-plane certificate or explicit >=237 witness; HiGHS MILP infeasible is noncertifying.
- CAP-007 [P0] Maintain independent global upper-bound and nonlocal-construction research. A full six-fiber barrier would still not settle global r3(7). Novelty not established.

## CAP-005I update (2026-11-02 05:05 UTC)
- CAP-005H [CI GREEN] https://github.com/davidlueng986-alt/123321/actions/runs/41391589830 confirms 16-element affine stabilizer and 32 integer-rounded exclusions.
- CAP-005I [LOCAL EXACT / CI PENDING] Seven independently checked rational duals using fixed-original conflict triangle and odd-five-cycle inequalities cover all 88 remaining six-fiber cases by symmetry. Together with CAP-005G's 295922 exclusions, the exact restricted optimum for ANY edit of <=6 of the fixed first-three-coordinate 27 fibers is 236. No global bound. Code/report: cap005_i_oddcycle_dual_generator.py, cap005_i_oddcycle_dual_check.py, CAP005_K6_ODDCYCLE_FULL_EXACT_236_2026-11-02.md. Await CI before promoting.
- CAP-005J [P0] Change strategy: do not spend cycles repeating this exact fixed-coordinate <=6-fiber neighborhood. Try alternative affine partitions, different 236-point baselines, nonlocal >6-fiber occupancy-changing templates, and certified global upper-bound methods. Keep exact r3(7) objective and literature novelty audit.

## CAP-005I CI final (2026-11-02 05:10 UTC)
- [DONE / CI GREEN / RESTRICTED ONLY] https://github.com/davidlueng986-alt/123321/actions/runs/41392035320 proves exact maximum 236 for all <=6 of the fixed 27 4D-fiber edits around the classical 236 cap. All 296010 six-fiber subsets excluded; seven exact odd-cycle dual certificates for the last 88. Artifact https://github.com/davidlueng986-alt/123321/actions/runs/41392035320/artifacts/13118250395.
- [P0] CAP-005J pivot to genuinely nonlocal >=7-fiber construction, alternative affine partitions and/or different baseline caps. [P0] CAP-007 global certified upper bound. Do NOT conflate this restricted maximum with r3(7). No exact global solution, continue hourly campaign.

## CAP-005J update (2026-11-02 05:57 UTC)
- CAP-005J [LOCAL TWO INDEPENDENT FULL CENSUSES PASS / CI PENDING / NECESSARY ONLY] Exactly seven fixed first-three-coordinate 4D fibers: all 888030 release sets enumerated by independent Python outsider-incidence and C++ direct-neighborhood methods; all 98 histogram bins and 8 maximum groups agree. Exactly 862906 neighborhoods (97.1708%) have at most 16 individually admissible outsiders and cannot improve the 236 baseline by the previously certified >=17-insertions barrier. 25124 unresolved; max N(T)=198 (8 groups). No candidate cap or global bound. Scripts cap005_j_k7_gate_incidence.py, cap005_j_k7_gate_direct.cpp, cap005_j_compare.py; report CAP005_K7_NECESSARY_GATE_2026-11-02.md. CI pending; do not claim CI GREEN before confirming.
- CAP-005K [P0] After CI, quotient 25124 survivors by known 16-element affine stabilizer and prioritize low-N representatives for exact rational dual or UNSAT certificates. Large N(T) is only individually admissible, not a witness.
- CAP-007 [P0] Independently investigate global upper bounds and genuinely nonlocal >=7-fiber/alternative-partition constructions; the fixed six-fiber theorem and seven-fiber necessary gate do NOT solve r3(7). Verify novelty against latest primary sources.

## CAP-005J CI final (2026-11-02 06:06 UTC)
- [DONE / CI GREEN / NECESSARY ONLY] https://github.com/davidlueng986-alt/123321/actions/runs/41397388094 independently verifies complete C(27,7)=888030 seven-fiber necessary census with Python incidence generation and C++17 direct enumeration, all 98 histogram bins identical. Exactly 862906 neighborhoods excluded from improving the fixed 236 baseline; 25124 remain unresolved. Maximum 198 individually admissible outsiders is not a feasible cap. Artifact https://github.com/davidlueng986-alt/123321/actions/runs/41397388094/artifacts/13119049955. Continue CAP-005K symmetry quotient / stronger certified exclusions and CAP-007 global/nonlocal work. No global improvement, no >=237 witness.

## CAP-005K update (2026-11-02 UTC)
- CAP-005K [LOCAL JS EXACT / NEW CI PENDING / NECESSARY ONLY] The 25,124 seven-fiber necessary survivors from CAP-005J form **1,665** orbits under the verified order-16 affine stabilizer. Orbit-size histogram: 3 of size 4, 185 of size 8, 1477 of size 16; 25,124 covered exactly. Eight N=198 cases are one orbit; N=17 has 37 orbits (576 cases). Local independent JS reconstructed all secants, 2,946,160 incidences, 25,124 survivors and orbit partition. New Python generator plus independent F3 checker in CI. No new exclusion/global bound/witness.
- CAP-005L [P0] Once CAP-005K CI succeeds, test all 37 N=17 representatives for certified pair conflicts or exact deletion-cover obstructions; then move to low/moderate-N representatives with rational LP duals or verified odd-cycle cuts. Do not confuse necessary N with compatible outsiders.
- CAP-007 [P0] Maintain global upper-bound proof search and genuinely nonlocal >7-fiber/alternative-partition construction search in parallel. Even complete k7 restricted exclusion cannot settle r3(7). Check novelty before any publication claim.

## CAP-005K CI final (2026-11-02 UTC)
- [DONE / CI GREEN / NECESSARY ONLY] https://github.com/davidlueng986-alt/123321/actions/runs/41402684579 independently verifies 1665 orbits covering all 25124 seven-fiber necessary survivors, including exact arithmetic N(T) for every representative. Full 1665-representative artifact: https://github.com/davidlueng986-alt/123321/actions/runs/41402684579/artifacts/13122077145 . No global result, no new exclusion. An exploratory N=17 JS pilot hit a recursion error and returned no valid data; retry only with explicit recursion guards and independent checks.
- [P0] CAP-005L: prioritize 37 N=17 representatives (576 neighborhoods) for exact fixed-original-point conflict certificates or deletion-cover inequalities; no numerical claims until independent arithmetic check and CI. Continue CAP-007 global and nonlocal parallel.

## CAP-005L update (2026-11-02 08:45 UTC)
- [LOCAL JS EXACT / CI PENDING / RESTRICTED ONLY] All 37 seven-fiber N=17 symmetry representatives (576 neighborhoods: 35x16+2x8) have explicit pair-with-fixed-original or outsider-triple conflict, so cannot include all 17 individually admissible outsiders; improvement requires >=17 insertions. Cumulative seven-fiber exclusions 863482/888030, 24548 unresolved in 1628 orbits. Independent Python certificate generator/checker added, CI pending. No global upper bound or >=237 witness.
- [P0] Confirm new CI and archive 37 certificates; [P0] test N=18..24 using disjoint conflict matching/clique-cover/deletion-cover certificates, then exact LP duals on moderate-N representatives. [P0] Continue nonlocal/global bound work, do not confuse local obstruction with exact r3(7).

## CAP-005L CI final (2026-11-02 08:52 UTC)
- [DONE / CI GREEN / RESTRICTED ONLY] https://github.com/davidlueng986-alt/123321/actions/runs/41415696843 verifies all 37 exact N=17 conflict certificates and their 576 seven-fiber neighborhoods, independently checking F3 arithmetic and symmetry. Artifact https://github.com/davidlueng986-alt/123321/actions/runs/41415696843/artifacts/13128405069. Seven-fiber exclusions 863482/888030; 24548 unresolved, 1628 orbits. Next N=18..24 matching/clique and global/nonlocal work; no global bound or witness.

## CAP-005M (2026-11-02T09:57:58.759Z)
- [LOCAL JS EXACT / CI PENDING] 500 N18..32 seven-fiber symmetry orbits, 7,440 neighborhoods, carry explicit vertex-disjoint fixed-point pair-conflict matchings. Expected 870,922 excluded / 17,108 unresolved. Confirm independent Python CI before promotion. See CAP005_K7_MATCHING_CERTIFICATE_2026-11-02.md.
- [P0] Outsider-triple and odd-cycle/deletion-cover cuts for remaining low-N orbits; [P0] independent global certified upper bounds and nonlocal cap constructions. Fixed partition cannot settle r3(7). No novelty assertion.

## CAP-005M corrective update (2026-11-02T10:02:52.469Z)
- [FAILED CI 41424961849] Greedy Python yielded 494 / 7352 instead of JS 500 / 7440 because canonical orbit representatives and greedy tie orders differ. Do not promote prior expected totals.
- [FIX / CI PENDING] Exact blossom matching replaces heuristic; arithmetic checker verifies only concrete disjoint fixed-original-point conflicts. Require new CI GREEN and actual counts before final state. No global bound.

## CAP-006A first-principles pivot (2026-11-02T10:07:35.245Z)
- [LOCAL JS EXACT / PYTHON CI PENDING] Fixed first-three-coordinate 27-fiber decomposition is provably nonrepresentative of coordinate 3D projections for the fixed 236 cap: 15 projections with Q=2884/four empty fibers, 20 with Q=2290/no empty fibers; 512 seeded full-rank maps span Q=2096..3186. Q measures density concentration only, not probability of improving 236.
- [P0] CAP-006B: select inequivalent projections (Q=2096, 2884, 3186), apply equal-budget exact multi-fiber search, verify all candidates independently; do not prematurely impose original partition constraints.
- [P0] CAP-007G: create truly *global* slice encoding A0,A1,A2 in F3^6, certify correctness by reproducing exact r3(4), r3(5), r3(6) before advancing n7; derive proof-logged upper bounds. Avoid assuming 112+112+12 for every extremizer.
- [P1] CAP-008A: adversarial metamorphic tests of every exact certificate/orbit group under random invertible affine maps and injected forbidden triples; test checker independence and certificate semantics.
- [P1] CAP-006C: parameterized constructor/priority-function evolution (FunSearch/X-evolve precedents) from scratch without the classical 236 seed. n7 record requires direct >=237 witness verification.
- [DEPRIORITIZED] Existing k7 exclusions: only pursue if they reveal transferable global inequalities or an actual 237 witness; score global progress separately from percentage of fixed neighborhoods excluded. Check CAP-005M CI before marking its pending 7,440 exclusions as proven.
- [NOVELTY OPEN] Do not claim these projection observations are new in literature. Exact r3(7) remains OPEN.

## CAP-005M CI final (2026-11-02T10:08:15.552Z) — merged after concurrent CAP-006A
- [DONE / CI GREEN / RESTRICTED ONLY] https://github.com/davidlueng986-alt/123321/actions/runs/41425618301 verified 524 exact pair-conflict matching certificates; 7,792 additional seven-fiber neighborhoods excluded. Cumulative 871,274/888,030; 16,756 remain in 1,104 orbits. Artifact https://github.com/davidlueng986-alt/123321/actions/runs/41425618301/artifacts/13132211988 . Earlier greedy CI failure preserved. Keep CAP-006A partition-adaptive/global direction prioritized; no global r3(7) bound.

## CAP-007G/CAP-006B batched first-principles pivot (2026-11-02T10:41:11.123Z)
- [LOCAL CODE + EXACT TESTS / CI PENDING] Globally exhaustive target237 SAT generator: 2187 point vars, 796797 line clauses, 490353 sequential counter aux, 1775353 clauses total with sound affine basis 8 fixed,28 forced zeros. DIMACS generated locally and SHA256 recorded. SAT status UNKNOWN, no UNSAT certificate.
- [EXACT DIAGNOSTIC / CI PENDING] 27-fiber count-only LP/ILP relaxation optimal=333, witnessed and analytically upper-bounded via 39-plane incidence identity modulo9. Too weak compared to 291; never spend major cycles adding only slice-size quotas.
- [LOCAL PILOT / CI PENDING] 320 matched deterministic 8-fiber release T across Q2884/2096/3186, max N(T)=124/2/45; no candidate >=237. Most promising original partition T=(0,1,5,6,8,11,18,19) exact MILP reports optimum236 and LP fractional110.5 for region of 85 baseline points. Solver status is NON-CERTIFYING until a separate exact proof.
- [P0] CAP-007H global slice cross-sumset SAT/ILP cuts, conditional on genuine 5D/6D cap classification and validated statement equivalence. Avoid fixed 112+112+12.
- [P0] CAP-006C independent, nonlocal, parameterized construction families + exact witness checks.
- [P1] CAP-008B proof-logged SAT, affine frame symmetry and independent checker mutation tests; benchmark 4D/5D known optima before global claims.
- [P2] Only pursue 8+fiber reconstruction if certificate strengths improve; raw N(T) large is meaningless due compatibility/integrality gap. Do not claim novelty or solve r3(7) prematurely.

## CAP-006C cross-dimensional construction transfer (2026-11-02T10:45:29.601Z)
- [LOCAL EXACT SOURCE REPLAY / CI PENDING] Independent audit of public 512-point n8 FunSearch cap, 3280 hyperplane directions: largest affine n7 section=208 (8 directions); 24 direction ×12 greedy quotient projection tests best 157. NO lower-bound record; cannot infer optimality or defeat more sophisticated projections.
- [LOW PRIORITY] Naive 8D hyperplane slicing or greedy quotient projection without reconstruction (observed too weak).
- [P0] CAP-006C2: general parametric admissible-set / generating-function search in n7 from independent starting families, certify every witness; full 237 target retained.
- [P0] CAP-007H: proof-logged global SAT with cross-slice structure rather than count-only quotas.

## CAP-007H anchored global subfamily (2026-11-02T10:49:06.157Z)
- [LOCAL CNF REPLAY / CI PENDING] Potechin affine uniqueness of maximal 112-cap in F3^6 permits a globally meaningful conditional model: any 7D cap with a 112-point hyperplane. Target237 CNF: 175958 vars,606095 clauses (176904 intra-slice cap clauses +81648 fixed-slice cross conflicts + sequential>=125 counter). Known236 112+112+12 assignment passes target236 and fails237; SAT status UNKNOWN. Reproducible 11MB CNF local SHA256 93faf29af90fb4b33ae68e08d889e02d0d5a43565afabf9f5878772738f4f830.
- [P0] Run certified/proof-logged SAT/UNSAT on anchored branch, then independent proof checker. If UNSAT, add sound conditional no-112 hyperplane cut to GLOBAL solver; do not claim r3(7)=236.
- [P0] Model cap configurations with all 6D hyperplane slices <=111; no argument yet that 237 caps must have 112 slice. Avoid unsupported assumption.

## CAP-007I anchored double-112 additive obstacle (2026-11-02T10:53:32.714Z)
- [LOCAL C++ EXACT / CI PENDING] Enumerated 5922 distinct relative 6D linear transforms of two 112-cap slices (identity, 60 elementary shears, all two-shear compositions, plus 4000 seeded length3/4 compositions). H=F3^6\(-X-Yg) has size 0 for 5732, 1 for127, 4 for61, 12 for2; none >=13. By itself this DOES NOT exclude 237 with two maximal slices for other g nor any profiles with <112.
- [P0] CAP-007J: rigorously reduce all relative GL6 transforms by stabilizer double cosets (if computationally tractable), or derive a universal additive/spectral restriction on H and cap(H).
- [P0] Keep CAP-007H anchored 112-slice 237-SAT with proof logging; no SAT/UNSAT conclusion yet.
- [P1] Test structurally different near-maximal six-dimensional slices 110,111 as conditional branches; Thackeray's classification provides mathematical constraints.

## CAP-007J new globally conditional spectral structure (2026-11-02T11:04:56.326Z)
- [LOCAL EXACT / CI PENDING] For any two 112-caps in F3^6, Potechin affine uniqueness + exact canonical Fourier audit yields two nonzero Fourier powers 529×112 and 16×616. Exact cross-additive energy E(S,T)=218624+361*k where k is heavy-spectrum intersection. Need phase-sensitive support cuts, as k alone does not determine the number of free third-slice points.
- [VERIFIED LOCAL FINITE FAMILY] All 3812 distinct GL6 matrices of elementary-word-length<=2: exactly 3505/126/60/121 with 0/1/4/12 third-slice holes respectively; no13. Any 729 translations are redundant by affine covariance. This is a restricted maximum236, NOT a universal 112+112 theorem.
- [P0] CAP-007K: compute automorphism group stabilizers and double-coset representatives for all relative 112-cap alignments. Exhaustive coverage or certified bound required before excluding 112+112+13 globally.
- [P0] CAP-007L: derive stronger phase-sensitive Fourier/moment and exact set-support inequalities; test against k=32 giving holes 4 or12, and k=80 giving zero holes, counterexamples to naive overlap prediction.
- [P0] CAP-007N: global target237 branch with every 6D affine hyperplane <=111. Proof of maximal-112-slice conditional case alone cannot resolve r3(7).
- [P1] CAP-008: independently audit spectral lemma statement under published Potechin 2008 affine-uniqueness theorem, and checker metamorphic cases. Literature novelty not established.

## CAP-007J2 structural amplification (2026-11-02T11:10:53.032Z)
- [LOCAL EXACT / CI PENDING] Canonical maximal112 cap is Fourier self-dual (high power frequencies=cap) and a regular partial difference set yielding Cayley SRG(729,112,1,20); extension to every 112-cap uses Potechin uniqueness + unique center argument.
- [P0] Use general cross-energy formula for arbitrary second slice size m to produce *cap-specific* conditional 112-slice inequalities, especially cases (112,111,14) and (112,110,15). Direct Parseval/energy by itself is not a cap upper bound.
- [P0] Analyze doubly reduced relative112-cap alignment through its strongly regular graph automorphism group; certified coverage required to claim 112+112+13 impossible globally.
- [P0] Separate global no-112-hyperplane SAT/ILP branch. Need matching upper and lower bounds before exact r3(7) solution.

## CAP-007J3 induced-edge energy (2026-11-02T11:12:52.892Z)
- [EXACT COROLLARY] For centered maximal112 first slice S and any second subset T, cross-additive energy is 20m²+92m−38 e_G(T) in SRG(729,112,1,20). For maximal112 T, e_G(T)=1120−19k/2. Use this to design cap-specific graph/SDP cuts; the identity alone cannot prove third-slice<=12.
- [P0] Combine induced SRG subgraph edge count with outsider support, third-slice cap compatibility, and exact proof-logged conditional search; cover all slice-size profiles and the no-112-hyperplane branch.

## CAP-007K multiplicity audit (2026-11-02T11:14:36.835Z)
- [LOCAL EXACT / CI PENDING] Enumerated 3812 pair-alignment matrices; 121 12-hole alignments all have minimum positive cross representation 11, giving one-sided deletion-resilience <=10 points in this restricted family. Novelty not claimed.
- [P0] Derive general cap-specific constraints on r(z)=1_S*1_T, low-multiplicity tails, phase-sensitive Fourier and cap(H) rather than only holes or total energy; test 112+111+14 and 111+111+15 profiles.
- [P0] Rigorously cover relative GL6 by automorphism double cosets; unenumerated alignment families remain OPEN.
- [P0] Keep separate global no-112-hyperplane search, as all 112-conditioned facts cannot exclude it.

## CAP-010A 110/111 unique completion and overlap cuts (2026-11-02T11:54:27Z)
- [LOCAL EXACT / PYTHON CI PENDING] Independently computed 10/56 outside secant histogram and exhaustively checked 6216 two-point deletions. With Potechin 112 affine uniqueness + Thackeray 110 extension: ALL 110/111 caps have unique maximal112 completion. For 112+111+14 need completed centered overlap k>=30; 112+110+15 need k>=28. Not a global n7 upper bound.
- [P0] Build exact symmetry reduced proof-logged SAT branches for 112+111+14 (k>=30) and 112+110+15 (k>=28); avoid restricting to small GL6 word families. Also test third-slice cap compatibility and >=237 total.
- [P0] Independently audit CAP-009A/B Drive-only stronger claims before GitHub promotion; spectral floating point bounds need rational certificates.
- [P0] Keep all-hyperplanes<=111 global branch; this is untouched by 112-anchored theorems.
- [NOVELTY] Classical (729,112,1,20) Games graph known in literature. Unique-completion corollary novelty unknown, no priority claim.


## CAP-013 cross-agent integration audit (2026-11-02 12:48 UTC)
- [P0 / CONFIRMED BUG] Fix CAP-011A source sign in Drive v4.0: Q must be -(centered.T @ centered) mod 3, then explicitly assert every cross-dimension verification flag TRUE. Original v4 JSON flags are false for 7D236, 8D496/512; do not falsely certify.
- [P0 / PROOF GAP] CAP-010B: exact integer Gram but float SVD/eigvalsh still decides eigenvalue multiplicity/maximum. Require an exact PSD/rank certificate, independent verifier and green CI; numeric lambda=425/576 and derived deletion bound remain unpromoted until proof.
- [P1 / EVIDENCE GAP] CAP-010C k28/30/32 across 3812 matrices: insist on standalone code/certificate and CI. CAP-008C B6 finite enumeration independently replay before promotion. Do not treat Drive-only CAP-012 self-audit as independent external confirmation.
- [VERIFIED MATH] CAP-011B global codim2 first/second/third moments and 89->>=33 5D subslice gate rederived exactly; CAP-011C cross-slice matching proof valid. Use these for new global five-dimensional incidence constraints rather than further fixed-236 local optimization.
- [P0 / GLOBAL] Preserve n7 target237 proof-logged SAT and all-hyperplanes<=111 branch. No >=237 witness or improved global bound.

## CAP-014-PSD exact spectral premise (2026-11-02 13:00 UTC)
- [LOCAL EXACT PASS / CI PENDING] Repaired Drive CAP-010B's float-SVD/float-eigvalsh proof gap for the *fixed classical* 112+112 slices: pure-integer 111x111 PSD certificate via symmetric Bareiss (rank 107, nullity 4) and independent mod-1e9+7 rank 107. Exact lambda_perp=425/576, verified independent 236-cap checker. Formula d>=ceil(64512m/(576m+47600)), for deletions from second 112-slice while first is frozen. See CAP014_EXACT_PSD_425_OVER_576_2026-11-02.md, cap010b_exact_psd_certificate.py and test_cap010b_exact_psd_certificate.py. No global bound.
- [P0] Confirm workflow https://github.com/davidlueng986-alt/123321/actions/runs/41449195256; if failure, investigate before promoting. GitHub unittest discovery includes the new test.
- [P0] Independently fix CAP-011A negative sign in other agent's Drive source (do not overwrite source without coordination), and audit CAP-014A/B/C claims separately; CAP-014-PSD is a different, disambiguated GitHub experiment.
- [P0 / GLOBAL] Focus 237-target all-hyperplanes<=111 branch, 5D incidence and proof-logged SAT. A restricted classical-pair spectral bound cannot prove exact r3(7).
- [META] Exact proof-integrity now improved, but marginal global-search leverage is low; do not over-invest in local fixed-pair perturbations. No >=237 witness; novelty unverified.


## CAP-015S external-agent v5.0 synchronization (2026-11-02 13:08 UTC)
- [DONE / LOCAL EXACT / CI PENDING] Original v5 source + complete evidence JSON from Drive copied into this dedicated GitHub branch; CAP-011A sign bug minimally fixed, 4 full witness cap checks + 8017 directions exact replay pass. No external agent source overwritten. See CAP015S_EXTERNAL_AGENT_V5_SYNC_2026-11-02.md and test_cap015_external_agent_v5_sync.py.
- [P0] Confirm GitHub CI success for imported artifact regression; do not promote without green run. CAP-014 fixed-pair exact PSD already green at 41449380778.
- [P0] Independently re-run Drive v5 CAP-013B 648-orbit GO6 group census and CAP-014C full 449064-pair DFS certificate; inspect mathematical completeness and subgroup/global scope before using to prune target237 branches.
- [P0] Global all-hyperplanes<=111 (no 112-slice) branch, together with five-dimensional incidence constraints and proof-logged SAT remains essential for exact r3(7).
- [P1] Check CAP-015A 12-class slice census (full 1093 directions) against independent witness arithmetic; preserve distinction cross-slice holes vs actual third-slice cap possibilities.
- [NOVELTY] Do not present group/fourier identities as new without external literature verification; classical Games graph historical.


## CAP-019 v6 upper-bound referee and exact-certificate priority (2026-11-02)
- [NEW CANDIDATE / CPU EXACT / CI PENDING] Independent finite certificate excludes all 28 quadratic rank classes at M=288, giving candidate global upper r3(7)<=287, conditional on CAP-017B common-tangent lemma, CAP-010A 111 completion and Thackeray 110-cap theorem. See CAP019_INDEPENDENT_287_UPPER_BOUND_AUDIT_2026-11-02.md and test_cap019_287_upper_bound_certificate.py. Do not promote to accepted published bound before independent theorem referee.
- [CONFIRMED ERROR / CORRECTED] Drive v6 rank0 variance 185664 and slope 3016 are invalid; correct budget182304, valid slopes214/77. Preserve original Drive v6 source; report correction in ledger.
- [P0 CRITICAL] Independent hostile audit of CAP-017B Fourier inversion, simultaneous affine shear, common high-frequency tangent double count, especially m*=0 and m*=56 with d>0; independently prove 110/111 completion dependency and verify Thackeray 2022 theorem's proof not just abstract.
- [P0] Confirm GitHub CI for new CAP-019 verifier; ensure all 28 cases and Fourier replay pass on branch. Obtain separate human/mathematical referee and priority literature review before external claim.
- [P1] Formalize finite 211-triple/28-quadratic-class certificate in Lean (or a second independent implementation) and write standalone publication-grade proof.
- [GLOBAL] If CAP-019 withstands review, exact r3(7) remains OPEN with 236<=r3(7)<=287; pivot to lower-bound improvements or stronger global upper-bound cuts. Do not stop automation without matching rigorous bounds.


## CAP-020 — antipodal secant separation and refined tangent bound (2026-11-02)
- [EXACT PROOF + LOCAL CPU 5/5 PASS / CI PENDING] General lemma: if H=-H is a cap, z!=0, then the endpoints of all secants through z are in distinct +/- orbits. Canonical centered112 has 10 secants at each of its 616 nonzero outsiders; a second centered112 cap replacing any point must delete >=20 original points. Hence distinct centered112 intersection <=92 and distinct dual high-direction overlap m*<=46. Report CAP020_ANTIPODAL_SECANT_GAP_2026-11-02.md; test_cap020_antipodal_secant_gap.py.
- [REFINED CAP-017B] For completed 112-slice pairs with total deletion d=0..4, third-slice bounds sharpen [57,59,61,63,64] -> [56,58,59,61,63]; equal duals m*=56 special case c<=d. Confirm CI before promoting status. This does not change M>=287 allowed profile counts, and does not improve global 287 candidate.
- [P0 REFEREE] Prove full CAP-017B as a standalone theorem (especially simultaneous affine centering, z=0 and m*=56, duality, 110/111 completion); independently inspect Thackeray 2022 Thm3.9 proof dependencies and machine-search steps. New 287 upper bound remains provisional.
- [P0 GLOBAL] Balanced/no-112-slice regime dominates exact r3(7); derive new 5D codim-2 incidence / Fourier / proof-logged SAT constraints. Avoid over-investment in local 112 overlap improvements without a quantified global certificate gain.
- [P1] Investigate whether antipodal deletion >=20 can be strengthened by *joint* constraints for all outsider points of second cap; proof must cover all GL6, not sample shears. Literature novelty not established.


## CAP-021 — exact moment-dual slice forcing and strategy change (2026-11-02 UTC)
- [LOCAL EXACT PASS / CI PENDING] New unconditional global gate: every M>=286 cap contains a >=110-point affine 6D section (161-profile exact dual, sum -2468100). For M287, **conditional on CAP-017B + Thackeray**, every cap has a >=111-point section (175-profile dual, sum -4531050). For M288, conditional >=112 section (189-profile dual, sum -29038176); does not improve CAP019 candidate <=287.
- [P0] Verify green GitHub CI for CAP021 and preserve conflict-aware append-only records. Test file test_cap021_slice_forcing.py; independent JSON CAP021_slice_forcing_certificate.json; report CAP021_SLICE_FORCING_LADDER_2026-11-02.md.
- [P0 MATHEMATICAL] Exploit forced 111-section for M287: use Thackeray/Potechin completion, 5D codim-2 incidence and Gaussian quadratic-residue spectra, plus proof-logged SAT. Do not treat a 111-section as necessarily a 112-section without a valid proof.
- [FALSIFIED] Pure global S2/S3 moments cannot force >=110 at M285 (explicit 1093-direction integer histogram with all sections<=109), nor >=112 at M287 under CAP017B (explicit histogram with all sections<=111). Histograms are NOT cap witnesses; use them as counterexamples to over-strong relaxation claims.
- [P0 REFEREE] Independently audit CAP017B/110-completion dependencies and the provisional CAP019 <=287 theorem before external publication; all finite dual checks passing does not replace theorem review.
- [LITERATURE PRIORITY] Thackeray 2022 Proposition 4.1(a) already yields third section<=34 for 112+112; Proposition 4.1(b) yields <=55 for two sections totaling >=222. These dominate CAP020 numerical bounds for d=0,1,2; integrate them in future low-M profile enumeration and revise novelty narrative. No priority established for CAP021.
- [KNOWN WITNESS] Existing 236-point cap independently rechecked (27730 pairs, zero 3AP, 2187/2187 coverage). No >=237 witness or stronger accepted bound; r3(7) remains OPEN.


### CAP-021 rank-2 Gaussian relaxation countermodel and CI policy addendum (2026-11-02 UTC)
- [FALSIFIED / EXACT] Aggregate global S2/S3 moments + projective Gaussian Q rank/sign spectrum **still cannot exclude 287**: exact 8-profile formal histogram matches rank2 Q=x1²+x2² value counts (121,486,486) and moments, with no CAP017B-forbidden profile. It is NOT a cap witness. Focus on actual per-direction 5D incidence/geometry, not more aggregate-only LP.
- [CI HYGIENE] Dedicated branch workflow now has concurrency cancel-in-progress; check final GitHub Actions result after latest commit. Local CAP021 Python stdlib 6/6 PASS; independent JS exact.


## CAP-022 — near-maximal 6D 5D-section fingerprints (2026-11-02 UTC)
- [LOCAL EXACT / CI PENDING] All 112 one-point and 6216 two-point deletions of canonical 112-cap checked over all 364 projective normals, with independent JavaScript aggregate replay. 111 has unique spectrum: (39,36,36)x110, (40,36,35)x198, (45,44,22)x45, (45,45,21)x11. 110 has exactly two spectra for canonical completion: 56 antipodal vs6160 other deletions. Counts of 45-point 5D subflats distinguish them: 22 vs40. Report CAP022_110_111_CODIM2_FINGERPRINTS_2026-11-02.md; test_cap022_110_111_codim2_fingerprints.py; JSON certificate.
- [P0] Confirm CI success at final CAP022 commit; independently referee Thackeray 110-cap completion and CAP010A 111 extension before promoting universal near-maximal slice fingerprint.
- [P0] Build anchored-111 3x3 codim2 grid constraints (all 9 cells <=45, all 12 grid lines <=112, exact row0 fingerprint), cross-layer 3AP constraints, and proof-logged SAT/ILP. Avoid treating aggregate-only histogram as geometric witness.
- [P0] Continue hostile referee CAP017B and provisional <=287 theorem; preserve balanced/no-112 branch and separate ≥237 lower-bound construction work. No stronger bound, no >=237 witness, no exact r3(7).
- [NOVELTY] No literature priority established; Thackeray 2022 already classifies 110 completion and stronger near-maximal geometry. Do not claim novel global result.


## CAP-023 — anchored111 exact SAT / count-only grid negative controls (2026-11-02 18:00 UTC)
- [DONE LOCAL EXACT / CI PENDING] Conditional anchored111 target287 CNF: 242666 variables, 738782 clauses; 14504523 bytes, SHA256 22c3ab32e85ccd9bae9bb8ca68e7664564bc8371a4fc34fe25e0cdcf3392d5f0. Generator, 6-case unittest, report and compact JSON certificate committed; no SAT/UNSAT decision or new bound. Existing CAP007H anchored112 and CAP023 anchored111 cross-graphs differ by exactly one 729-edge perfect matching.
- [FALSIFIED] Every one of the four possible anchored111 5D fingerprints admits a 287-point formal 3x3 integer grid with external rows 88+88 and all other 6D lines <=109; these are NOT actual caps. Stop relying on 3x3 line/cell counts alone for exclusion; include pointwise cross-layer incidence, multi-direction consistency and proof-logged solver certificates.
- [P0] Verify CAP023 GitHub CI on final branch commit, including independent known236/235 cap checks and exact CNF satisfying assignment. Re-run SHA256 on generated DIMACS if source changes.
- [P0] Design symmetry-reduced anchored111/112 SAT proof search for M287 and target237 subcases; do NOT treat anchored111 as global for target237. Add codim2 geometry cuts only with independently proved soundness.
- [P0 REFEREE] CAP017B common-tangent and Thackeray 2022 110 completion, CAP010A 111 completion and conditional CAP019 <=287 still require hostile mathematical audit.
- [P0 GLOBAL] Balanced/no-111 section branch and lower-bound 237 construction remain unaddressed by this reduction. Keep exact r3(7) campaign active.

## CAP-024 — anchored111 exact codegree / Cauchy necessary cut (2026-11-02 19:00 UTC)
- [DONE LOCAL EXACT / CI PENDING] 728-difference codegree histogram 0×2,1×110,19×220,20×396; 41,137,470 four-cycles; exact 49 b+c=176 Cauchy necessary cuts. 5/5 Python PASS + independent JS PASS. Source, report and JSON certificate committed in dedicated branch.
- [P0] Confirm final CAP-024 CI on exact commit. Do not treat green CI as SAT UNSAT or proof of r3(7).
- [P0 EXPERIMENT] Implement exact quadratic/pseudo-Boolean Cauchy pair cuts in anchored111 SAT/CP-SAT, measure solver node/relaxation impact with CPU bounded pilot; keep proof logging for UNSAT. Do not claim count-only grids excluded.
- [P0 REFEREE] Continue hostile proof review of CAP-017B common-tangent, Thackeray 110 completion, CAP-019 candidate global <=287.
- [P0 GLOBAL] Preserve balanced/no-111 and ≥237 witness branches; local anchored111 cuts alone cannot solve r3(7). Novelty not established.


## CAP-025 — Fourier/common-tangent hostile referee (2026-11-02 ~20:00 UTC)
- [EXACT JS V8 PASS / CI PENDING] Six independently transformed centered112 cap pairs: full 364-projective Fourier spectra, 4374 direct convolution identities, primal/dual intersection identity, and d=0..4 identical-dual deletion exceptions all passed. New JS + Python CI wrapper + standalone report committed. This is not exhaustive GL6 enumeration; universal proof is symbolic with Potechin classification.
- [P0] Confirm CI green on the **final CAP-025 commit**, including Node invoked through Python unittest. No GPU or solver.
- [P0 EXTERNAL REFEREE] Independently reproduce the classification/computer-assisted parts of Thackeray arXiv:2206.09804v1 Thm3.9 and its 5D dependencies before treating CAP019 ≤287 as independently established. Fourier premise appears consistent but finite tests alone are insufficient.
- [P0] Separate proof-logged anchored111 SAT target287 and balanced/no-111 lower-bound237 branch; the new small-m* zero-hole corollary does not improve global M288 finite dual.
- [NOVELTY] Thackeray Prop4.1 already dominates CAP017B coarse bounds at d=0,1,2. Neither small-overlap corollary nor 287 claim has verified priority.


## CAP-026 285-point quadratic-rigidity boundary (2026-11-02 ~20:55 UTC)
- [DONE / LOCAL EXACT / CI PENDING] On 169 admissible 285-point sorted max109 profiles, three exact integer nonnegative functionals + 28 independent projective quadric spectra imply: hypothetical 285-cap with all affine 6D sections<=109 must have NONZERO barycenter and ANISOTROPIC rank2 Q on 6D barycenter kernel (40,162,162). See CAP026_285_QUADRATIC_RIGIDITY_2026-11-02.md and test_cap026_285_quadratic_rigidity.py.
- [NEGATIVE CONTROL] Exact 1093-profile integer histogram matches global S2/S3 and surviving Q rank2 value counts, but is NOT a cap. Therefore moment+rank-spectrum LP cannot prove 285=>110. Prior CAP021 285 histogram violated barycenter Type counts; corrected negative control now respects them.
- [P0] Check exact final GitHub CI for CAP-026; all independent arithmetic must pass before promoting code certificate.
- [P0] Continue hostile reproducibility review of Thackeray 110-cap completion (2022 preprint) and candidate CAP-019 <=287. CAP-025 Fourier premise CI now SUCCESS 41514324725, but Thackeray computational classification not independently replayed.
- [P0] To improve global upper/lower bounds, impose genuine codimension-two affine incidence, per-direction quadratic FORM geometry (not just rank histogram), and proof-logged anchored111/110 SAT; balanced/no-111 branch remains open.
- [P1] Explore whether anisotropic rank2 Q can be excluded by joint 5D-subspace incidence, or provide an actual realizable direction assignment satisfying all 5D compatibility. Avoid presenting formal integer profiles as caps.
- [NOVELTY] No external priority established; current global numerical bounds unchanged and exact r3(7) OPEN.

## CAP-027 — radical affine Radon p-rank and count-only falsification (2026-11-02 ~21:48 UTC)
- [LOCAL EXACT PASS / CI PENDING] Conditional on CAP026 hypothetical M285 max109 rank2 anisotropic Q: its Q0 normals are exactly PG(W), W a 4D radical; all 120 affine 6D W-slices divisible3. Exact F3 affine Radon ranks k2,k3,k4 =6,10,15, so 120×81 radical matrix has nullity66. All 130 codim2 3×3 grids must have affine-linear residues mod3. Source/test/report/certificate CAP027.
- [FALSIFIED] Full 81-fiber nonnegative integer model of total285 with every fiber≤7, all 120 W-slices≤108 divisible3, all 1170 affine 5D cells≤45, all 130 grid congruences passes. Not a cap; remaining 1053 normals and cross-fiber 3AP absent. Do NOT claim these count-only constraints exclude M285, or that each fiber is 0 mod3.
- [P0] Confirm GitHub Actions CI at exact final CAP027 commit; check independent Node test, avoid green claims before completion.
- [P0 GEOMETRY] Replace 81-fiber count-only model by point-level 3D cap assignments with cross-fiber collinearity and remaining rank2/Type1 normals. Use proof-logged SAT/CP-SAT and independently checked UNSAT proof if attempting global bounds.
- [P0 REFEREE] Thackeray 2022 computational 110-completion and CAP019 <=287 remain provisional; preserve balanced/no-111 and ≥237 construction branches.
- [NOVELTY] Affine incidence p-ranks are classical; literature priority for CAP027 not established. Exact r3(7) OPEN.

## CAP-028 — 1080 quotient 4D lines / local liftability (2026-11-02 ~22:56 UTC)
- [LOCAL EXACT / CI PENDING] CAP027 285-count negative control survives all 1080 additional 4D-flat bound <=20 (maximum observed 19). All 12 quotient-line profiles individually realized by exact 18/19-point AG(4,3) caps and point deletions; independent Python 6/6 and Node PASS. Known236 7D regression PASS.
- [FALSIFIED] Adding all 4D quotient-line cardinality bounds plus independent per-line realizability **does not** exclude CAP027's count-only 285 model. This is NOT a 285 cap, no new upper bound. Separate (7,7,5) MILP timed out 12s; UNKNOWN, not UNSAT.
- [P0] Confirm GitHub CI green on final CAP028 head.
- [P0 GEOMETRY] Require simultaneous shared 3D fiber point-level assignments across intersecting quotient lines; independent local lifts do not imply global compatibility. Use proof-logged SAT/CP-SAT and independent exact checker.
- [P0] Check remaining 1053 directions and Q residue constraints; independent Thackeray 110-cap completion referee, CAP019 provisional <=287, balanced/no-111 and >=237 construction all remain active.
- [NOVELTY] Classical AG(4,3) max20 known; no new priority established. Exact r3(7) OPEN.

## CAP-030 (2026-11-03)
- [DONE / EXACT LEMMA] For each quotient line (i,j,k), require A_k disjoint from {-a-b:a in A_i,b in A_j}; reuse identical fiber assignments across all lines. CAP028 local witnesses have midpoint image sizes [23,19,19] and [20,19,20]. No global numerical improvement.
- [P0] Check CAP030 CI; build bounded shared-fiber SAT/PB pilot with independent verifier and proof-logged UNSAT where possible; continue Thackeray 110-cap completion referee and balanced/no-111 branch.

## CAP-032B universal AG(4,3) slice profile cut (2026-11-03T02:53:58.437Z)
- [LOCAL EXACT Python+C++ / CI PENDING] New complete high-density 3D parallel-slice compatibility table for ANY AG4 cap, verified by F3^3 AGL orbits and all second caps (sizes6..9). Universal (7,7) implies third<=4; 189 exceptional hole sets have no 5-cap, 252720 pairs independently checked. Exact 10-pair table in CAP032B report. No novelty claim and no new global r3(7) numeric bound.
- [NEGATIVE CONTROL] All 1080 quotient 4D lines of CAP027 285-point FORMAL count-only countermodel still meet the high-fiber cuts. Count-only relaxation remains too weak, not a 285 cap. Preserve prior CAP032 random-occupancy expectation as independent effort.
- [P0] Confirm CAP032B final GitHub full CI on code commit 784ad1b6ff34c0bcb245993747a5cbb0bc5da503 or later code-containing SHA; do not mark CI GREEN before completed pass.
- [P0] Implement GLOBAL shared-fiber multi-quotient-line compatibility: one common 3D cap variable assignment for intersecting quotient lines, proof-logged SAT/UNSAT, independent arithmetic checker; start with CAP027 formal285 fixed counts only as a CONDITIONAL test, not a global upper-bound proof.
- [P0 REFEREE] Verify Thackeray's 110-cap computer classification and CAP019 conditional <=287 from original sources and independent exact witness/classification; unresolved external premise prevents unconditional improvement claim.
- [P0] Preserve balanced/no-112-hyperplane and >=237 construction branches (independent of known236). Validate candidates, avoid inferring global bound from single-line profiles.

## CAP-032C globally valid shared-fiber orbit-type gate (2026-11-03T03:00:02.934Z)
- [LOCAL EXACT, CI PENDING] A 7-point AG3 fiber participating in an AG4 (7,6,6) parallel-slice cap MUST belong to the 50544-member AGL3 orbit of non-9-extendable 7-caps. Other 75816-member 7-cap orbit never works. Exact second-6-cap completions per fixed first representative: 27 vs0; full 19point witness checked. Distinguish from CAP032B count-only threshold cuts.
- [P0] Incorporate this semantic type restriction into CAP031's 81 shared-fiber SAT/PB model using verified 7-cap membership/9-completion predicates; check if CAP027 M285 formal count arrangement permits simultaneous consistent types across its 1080 quotient lines. Any UNSAT result on one fixed count arrangement remains conditional, NOT global bound.
- [P0] Find *multi-line* constraints needing actual shared internal 3D point arrangements, not only cap types; certify via proof logging and independent full 7D arithmetic.
- [P0 REFEREE] Independently audit Thackeray 110-cap classification under CAP019 provisional global <=287, before making unconditional bound claims; parallel balanced/no-112 and >=237 constructive search.
- [HONESTY] CA032B/C claims are universal necessary geometry and finite exact maxima in dimension4; no r3(7) numeric improvement, novelty unverified. Check latest GitHub Actions before CI promotion.

## CAP-035 (2026-11-03 05:56 UTC)
- [LOCAL CPU PASS / CI PENDING] Complete shared-variable 2187-primary-variable CNF generator with 796797 3AP clauses, fixed formal-285 81-fiber exact counts encoded by sequential counters. Exact 3AP prefix SHA256 in report; small counter encodings exhaustive truth-table checked. No solver run, status UNKNOWN.
- [P0] Confirm exact final CAP035 CI. Run a CPU-bounded proof-logged solver pilot; require independent DRAT/LRAT checker for UNSAT and independent 7D arithmetic for SAT. A fixed occupancy UNSAT is conditional only.
- [P0 META] Avoid low-value repetitions of count-only relaxation; prioritize shared-fiber geometric conflict, classification/upper-bound referee and balanced/no-112 and >=237 branches.


## CAP-037 (2026-11-03 UTC) — Full AGL(4,3) stabilizer
- [LOCAL EXACT PASS / CI PENDING] The CAP027 fixed formal 285 occupancy has trivial stabilizer in ALL AGL(4,3), not merely CAP036's monomial subgroup. Nine cells of occupancy 4/7 form the unique affine plane E; every affine stabilizer preserves it. The two 7-cells restrict (D,t) to 12 possibilities. All 48*81*12=46656 remaining affine block maps were checked against the nine 6-cells; only identity remains. Deterministic CPU-only, no seed. See cap037_full_agl_stabilizer.py and CAP037_FULL_AGL_STABILIZER_2026-11-03.md.
- [P0] Confirm CI for CAP037. Do not impose quotient AGL4 symmetry breaking on this fixed instance. Continue bounded proof-logged SAT with independent UNSAT verification, CAP019 external referee and >=237 search. This is not a 285 cap, not a global bound, no novelty claim.

## CAP-038 (2026-11-03 UTC)
- [LOCAL INDEPENDENT EXACT PASS / CI PENDING] CAP035 796797 forbidden-triple DIMACS prefix independently reconstructed by base-3 arithmetic; matching SHA256. CAP037 CI 41599046083 SUCCESS. See CAP038 report/checker.
- [P0] Independently audit auxiliary cardinality suffix and run CPU-bounded proof-logged SAT with verified UNSAT certificate or independently checked SAT witness; timeout UNKNOWN. Local solver absent.
- [P1] CAP019/Thackeray classification referee, balanced/no-112, nonlocal >=237 witness search. This fixed occupancy is not a global upper bound.

## CAP-039 (2026-11-03) — Cardinality suffix verified locally
- [LOCAL PASS / CI PENDING] 162 independent Sinz counters; proof of correctness via prefix thresholds; 7938 constructive valid witnesses, 4050 invalid unit-propagation contradictions. 59049 vars and 135561 suffix clauses; full CNF expected 932358 clauses. Seed 390039. See CAP039 report and script.
- [P0] Independently compare complete CAP035 DIMACS suffix hash and verify CI on current head. Then bounded CPU SAT solver with proof-logged UNSAT and independent checker; timeout UNKNOWN. Fixed285 UNSAT is conditional only.
- [P0] CAP019/Thackeray 110-cap classification referee; >=237 constructive branch and balanced/no-112 remain active. Avoid more count-only relaxation and symmetry studies unless directly feeding global proof.

## CAP-040 ROOT-PROOF DAG — mandatory proof-bridge scheduling policy (2026-11-03T10:35:36.503Z)

ROOT question: determine exact r3(7). Given verified 236, proving no 237-cap would finish exact r3(7)=236. Finding >=237 disproves that tentative equality but is NOT automatically exact optimum.

- [ROOT-COMPLETE / SAT UNKNOWN / CI PENDING] 13 S8 canonical affine-frame ninth-point branches cover ALL possible >=237 caps (all 2151 admissible ninth points), no assumption of symmetry of the unknown cap. Full proof requires ALL branches independently UNSAT with checked certificates. 1211 tenth stabilizer orbits are optional complete second-level split. CAP040 code and manifest.
- [ROOT-COMPLETE / SAT UNKNOWN / CI PENDING] CAP007J CI-green moment theorem forces some >=89 6D hyperplane in any 237-cap. Since r3(5)=45 and r3(6)=112, normalize 7 frame points inside dense H and 1 outside. One global SAT model plus >=89-of729 cardinality (553505 variables, 1896555 clauses) covers ALL hypothetical >=237 caps. H-preserving S7 lets choose a ninth point INSIDE H in 10 complete orbit types covering701 eligible positions; DON'T use S8 case normalization while keeping H fixed.
- [P0] Confirm CAP040 exact final CI, verify SHA256 8d23ac... and c45a3e... for complete generated DIMACS and independent known236 normalization positive control. If failure, preserve failure cause and correct on dedicated branch.
- [P0] Run BOUNDED free CPU solver with proof logging on one root-equivalent SAT instance (not fixed285 formal count), compare propagation before/after true hyperplane>=89 and ninth-unit anchoring; check available proof-producing SAT software and native checker. UNKNOWN/time-limit must never be promoted to UNSAT.
- [P0] If root SAT is intractable, derive universal cuts/structural classification that directly reduce these full global models. Every lemma must name its parent SAT branch, coverage impact, and certificate semantics; budget exploratory ideas separately.
- [P0] Maintain truly independent nonlocal >=237 constructive search with mod3 verifier; if SAT, export exact 7-digit witness, verify all 277... pair arithmetic and all 3APs (for N cap points, N(N-1)/2 pairs). Do not stop at lower-bound breakthrough.
- [P1] Hostile referee CAP019 provisional <=287 and Thackeray 110 cap completion theorem; paper's 2022 PDF uses earlier computer classifications and no independent replay yet, so no unreviewed claim.
- [META STOP RULE] A restricted 236-witness modification or fixed285 form occupancy UNSAT does NOT advance the root unless a proven global implication covers it. Stop reporting number of experiments/locally checked certificates as global proof progress. All proof-DAG leaf states currently UNKNOWN. Novelty not established. Existing hourly campaign remains active; do not alter MOLS10.

## CAP-041 root-equivalent global SAT presolve (2026-11-03T10:47:26.938Z)
- [LOCAL EXACT PASS / CI PENDING] CAP040H moment-anchored H00 full-global-237 branch compressed by explicit substitution of 9 selected points and 36 secant-forced zeros; 2142 free points, >=228 total-free and >=81 free-H. Exact all 796797 lines partitioned into 38718 tautologies, 9513 binary clauses, 748566 ternary. Completed root-equiv CNF 517533 vars/1786028 clauses, SHA256 b59faca48cdd649e1574c06f36dd1ff2dab982cdac05b22b8d306e0f76b276c4; free-id mapping saved locally, source code in GitHub. This is a proper child of a proven globally exhaustive 10-way proof branch, not a restricted fixed285 configuration.
- [P0] Confirm CAP041 GitHub CI on latest code, including whole DIMACS pinned hash and map, distinguish PASS code verification from actual SAT/UNSAT. CAP040 corrected full Actions run 41621025121 SUCCESS after earlier ordering assumption failure 41620367176 (retained audit record).
- [P0] Bounded free CPU proof-logging SAT pilot H00 compressed vs H00 uncompressed matched wallclock; require actual independently verified LRAT/DRAT-style proof for UNSAT and full 7D cap arithmetic for SAT. If unavailable/timed out, report UNKNOWN; don't imply completion.
- [P0] Optimize other nine dense-H branches only after confirming matched-benchmark benefit; first naive all10 enumeration timed out after eight, no ten-way compressed exhaustive result yet. Never misinterpret reduced CNF size as bound on r3(7).
- [P0] Alternative proof route: 13 globally complete S8 frame branches or unconditional nonlocal >=237 constructive search. Candidate CAP019 <=287 still requires hostile external 110-cap classification referee. Root r3(7) OPEN.

## CAP-042 (2026-11-03 UTC)
- [LOCAL EXACT PASS / CI PENDING] Independent full ten-branch incidence census closes CAP041 aborted eight-branch computation. H05, H07/H08 and H09 have distinct exact clause counts; do not reuse H00 counts indiscriminately. Source cap042_ten_leaf_incidence.py and CAP042 report.
- [P0] Check new CI; run bounded free-CPU proof-logged SAT H00 with independently verified SAT witness or UNSAT certificate. Timeout UNKNOWN. Root requires all ten branches proved UNSAT to establish <=236.
- [P1] CAP019 classification referee, nonlocal >=237 witness search; novelty unestablished; exact r3(7) OPEN.
