# E055 — Gauge optimization audit (2026-11-03 UTC)

Status: 3-MOLS(10) OPEN; no unrestricted orbit eliminated.

Primary literature checked: https://arxiv.org/abs/2503.10504 ; https://arxiv.org/abs/2605.02132 ; targeted November 2026 search. No independently verifiable unrestricted solution found (absence of hits is not a proof).

Read the living Drive journal and GitHub STATE.json/latest commits before experiment. Objective: independently challenge E054 pair-coordinate-ascent gauge compression rather than repeat local trade search.

Inputs: E051_CERTIFICATES.json (SHA256 b27b2d81946aa1c1e5c3bd2a7a350e0060c7049d8751d0bb670f8bd105223b52), E054_RESULTS.json; seven real exact integer dual vectors.

Exact bounded experiment: For each of six resource classes, find most frequent integer coefficient. Exhaustively choose each of six classes as free, set other five offsets to their modes and the sixth to negative sum; score exact integer zeros. Across seven certificates, resulting nonzero counts are 249,261,261,258,256,255,259, identical to E054. This is a six-choice restricted search, NOT global optimality. The six-class gauge invariance preserves every placement score and RHS exactly; source certificates had previously passed 15/15 exact checks over 6210 placements.

Failed attempt preserved: attempted a full six-class MILP (binary selection of class coefficient values, six one-hot constraints and one integer weighted zero-sum constraint) with SciPy HiGHS and 12-second/case budget. First returned incumbent was feasible in exact sum but gave only 45 zero coefficients versus known 99, status 1 (time limit). This is not a verified optimum; process subsequently timed out. The result is NOT evidence that the prior gauge was optimal. Numerical weighted coefficients ~millions require careful scaling/feasibility checks. Source scripts: E055_exact_gauge.py (experimental; not reliable as optimal solver) and E055_modal_gauge.py (exact integer restricted audit), local JSON E055_MODAL_RESULTS.json.

Reproduction algorithm: group the 360 coefficients by six classes; for free=0..5, take the mode in five classes and offset_free = -sum(other offsets); maximize sum_k frequency_k(offset_k); count 360-score. Verify sum offsets exactly zero and compare with E054 counts. No new mathematical nonextension result.

Next: avoid wasting CPU on unscaled floating MILP; use exact meet-in-middle or branch-and-bound with explicit incumbent and exact arithmetic for global gauge optimality. Higher priority remains uploading E051/E054 full certificates and verifiers for independent CI replay, then screening the remaining 102 E049 support-positive prefixes and symmetry-complete proof-producing SAT.

Uncertainty: the true gauge optimum may improve on E054. The original 162959-orbit count is inherited, not independently established in this iteration. No complete witness or unrestricted nonexistence certificate.
