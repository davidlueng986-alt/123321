# CAPSET-F3-7 — Research Backlog (2026-11-02)

**Exact problem:** determine r3(7). External lower 236; accepted stated upper 291, preprint states 288; investigate each primary source again before announcing any novelty. Current independently verified best construction 236. A 237 construction is only a partial breakthrough.

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
