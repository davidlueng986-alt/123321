# E054 — Real E051 Farkas gauge compression (2026-11-03 UTC)

STATUS: GLOBAL OPEN. This is certificate compression for seven fixed four-row prefixes, not an unrestricted proof or a new excluded symmetry orbit.

Sources checked: https://arxiv.org/abs/2503.10504 and https://arxiv.org/abs/2605.02132 ; targeted search 2026-11-03 found no independently verifiable full 3-MOLS(10) resolution.

INPUT: E051_CERTIFICATES.json (local 15-case dataset), E051_verify.py and E050 source0. Original exact replay: 15/15 PASS, 6210 residual placements.

METHOD: Partition the 360 demands into six groups of 60: three (square,column,symbol) and three (pair,symbol,symbol) groups. Every residual placement uses exactly one from each group. For integer offsets c[0..5] with sum(c)=0, y'[d]=y[d]-c[group(d)] leaves all column scores and RHS unchanged. Maximize the count of zeros using deterministic pair-coordinate ascent: for each pair i<j, hold c_i+c_j fixed and choose a frequency-supported replacement that improves the zero count. This is a heuristic, not an optimality proof.

RESULTS: Seven original certificates each 360 nonzero; transformed nonzero counts 249,261,261,258,256,255,259 (sum 1799 vs 2520; 721 coefficients removed = 28.61%). Offsets respectively: [999999,999999,-4999995,999999,999999,999999]; [999999,-4999995,999999,999999,999999,999999]; [999999,999999,999999,-4999995,999999,999999]; [999999,999999,999999,999999,-4999995,999999]; [-4999995,999999,999999,999999,999999,999999]; [999999,-4999995,999999,999999,999999,999999]; [999999,-4999995,999999,999999,999999,999999].

Independent transformed verification: 15/15 PASS; 6210 legal placements, every transformed dual preserves original exact RHS and max column score -5. The seven fixed-prefix certificates remain valid. No LP-feasible k4 prefix discovered, 0/162959 full symmetry orbits excluded.

AUDIT LIMITS: Local input certificates and full scripts are not yet committed to GitHub; this report alone is NOT a self-contained remote replay. First attempt to clone via container failed due DNS. Independent verifier ran locally. Next: publish full E051 input/certificates + E054 scripts, remote CI replay, then screen remaining E049 k4 prefixes and prioritize unrestricted symmetry-complete proof-producing SAT.
