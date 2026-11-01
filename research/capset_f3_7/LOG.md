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
