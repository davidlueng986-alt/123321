# Research backlog — CAPSET-F3-7

CAP-001 [DONE / VERIFIED COMPUTATION] Reproduced Calderbank–Fishburn 236 points from primary source; 236-line certificate, generator, independent verifier, 10-secants barrier and CI pass. See RESULTS_2026-11-02.md.
CAP-002 [PARTIAL] Deterministic seed=7 two-round greedy 136 verified by CI; no research claim. Reframe toward structured reconstruction using complete 236 witness.
CAP-003 [PARTIAL / VERIFIED COMPUTATION] With fixed 112+112 slices, exactly 12 third-slice points allowed. Every alternative third-slice point has >=11 disjoint cross-slice blockers. SAT encoding still TODO.
CAP-004 [P1/TODO] Affine symmetry/orbit structured search; test for repeated equivalent candidates.
CAP-005 [P1/TODO] Investigate certified upper-bound constraints and published 288 claim; independent source audit.
CAP-006 [P2/TODO] Formalize a verified candidate or structural lemma in Lean; require green CI and statement audit.

CAP-002B [DONE / VERIFIED COMPUTATION] Exact full 1,902,225 outsider-pair minimum vertex covers: min 16 deletions, 888 extremal pairs, GitHub CI and 101 independent MILP checks passed. Added reconstruction_milp.py; restricted 24-candidate optimum also computed locally.\nCAP-002C [P0/TODO] Search structured pools of >=17 candidate new points, with at least 16 deletions and exact triple constraints. Benchmark structural ansaetze; write exact witness+independent verification on any improvement. Watch solver gaps/timeouts; never claim optimal if time-limited.\n\nFor EACH cycle select one measurable experiment. Log run ID, exact command, seed, source, observed value, failure type, verification status, insight and next hypothesis. Do not submit arbitrary construction as a result without rigorous independent exact checking. Full r3(7) resolution requires matching verified upper and lower bounds. This branch stays separate from other mathematical research projects.
