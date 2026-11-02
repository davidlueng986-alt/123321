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
