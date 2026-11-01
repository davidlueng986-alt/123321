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
