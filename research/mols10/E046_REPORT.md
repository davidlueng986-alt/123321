# E046 — Local fourth-row trade neighborhood: exact LP obstruction is robust but old certificates do not transport

**UTC:** 2026-11-02 21:44–21:50. **Global 3-MOLS(10): OPEN.** No unrestricted positive witness or negative proof; **0/162,959** complete normalized symmetry orbits excluded.

## Literature and state reviewed
Read the [living Google Docs journal](https://docs.google.com/document/d/1NDPWEMM3Cf5HrhdOcV6pVE9tCI-kxKbavxcfIBFva3k/edit), [STATE.json](STATE.json), the latest E045 report, source code, and commits. Fresh review: Bright–Keita–Stevens, *Electronic Journal of Combinatorics* 33(1) #P1.30, published 2026-02-13, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; Barnoff–Bright, arXiv:2605.02132v2, revised 2026-07-04, https://arxiv.org/abs/2605.02132 . Targeted November 2 web/arXiv checks found no independently verifiable unrestricted solution. Failure to find one is not a proof of nonexistence.

## Falsifiable subproblem
E045's LP-guided 570 k=4 partial triples all have exact fixed-prefix nonextension certificates. Are they trapped merely by the original dual, or does their local neighborhood remain LP-infeasible after a valid *two-column fourth-row swap*? This is a **different neighborhood experiment**, not another generation of independent k4 prefixes.

For each of the 570 publicly persisted E045 remote prefixes, choose each nonempty mask of the three squares (7 masks) and every unordered pair of columns (45). Swap the two fourth-row entries in the selected squares. Each of the 179,550 proposals is tested for all three Latin row/column conditions and all three 40/40/40 overlays. For valid moves, independently enumerate all legal residual (column,A,B,C) placements and all 360 uncovered six-class demands. Test zero support and whether the **old** integer Farkas certificate still applies, with weights on originally used resources extended by zero. Old certificate failure does NOT imply LP feasibility.

## Exact local computation
- **570/570** source prefixes independently rechecked against their original integer certificates (532 Farkas duals + 38 zero-support).
- **179,550** bounded moves attempted; **7,428 valid**, **172,122 invalid**.
- Across valid moves: **578 exact zero-support**; **6,850 have positive support for every uncovered demand**.
- The old source certificate remains a valid exact obstruction in only **343** valid moves; **7,085** invalidate that particular certificate.
- **All 6,850 positive-support neighbors invalidate their old source certificate**, but their LP status is NOT established by this observation.
- **2,992,090** legal residual placements enumerated across valid moves.
- Separate bitmask-based implementation (different candidate/validity logic) reproduced every one of the 7 mask-level valid/zero/positive counts. This is a consistency check, not a proof about unsearched neighborhoods.

Mask-level valid / zero / positive: 1: 1484/115/1369; 2: 1342/110/1232; 3: 612/51/561; 4: 1371/114/1257; 5: 626/46/580; 6: 651/48/603; 7: 1342/94/1248.

## Follow-up: bounded actual six-class LP phase-I probe
Take every eighth source (indices 0,8,...,568). For each source, choose the **first** valid positive-support swap under masks 1 and 7 (if any); run SciPy HiGHS on its full 360-demand LP. For numerical infeasibility, obtain a bounded dual and round conservatively to exact integer weights. Independent Node.js verifier reconstructs the 600 resource universe, tests every legal candidate and checks sum(weights)>0, each candidate score<=0.

**131 unique neighbor prefixes** selected from **71 distinct sources** (65 mask-1, 66 mask-7), no exact ordered-prefix duplicates and no overlap with the 570 E045 originals. **131/131 numerical LP-infeasible upgraded to exact integer Farkas certificates**; **0 LP-feasible, 0 UNKNOWN**. Independent Node.js replay: **131/131 PASS**, **52,920** legal candidate placements. Additional audit: **131/131 deliberate positive-weight mutations rejected**; original certificate invalid on every selected neighbor (**124 source duals + 7 source zero-support certificates**). All 131 new duals are exact fixed-prefix nonextension certificates.

This is *not* an unrestricted negative theorem. The 131 cases are a deterministic, highly biased sample of 7,428 valid one-swap neighbors. The other neighbors have not received new LP certificates. Even a complete one-swap neighborhood proof for all 570 sources would not cover any full normalized orbit.

## Reproduce and provenance
Inputs: [E045_GUIDED_RESULTS.json](E045_GUIDED_RESULTS.json) Git blob `db9fc7211d681516e0d338473d95d8abe39af0df`; [E045_CERTIFICATES.json](E045_CERTIFICATES.json) Git blob `173d10f19aaf85c288d54a1282534838fa04b472`, from [E045 remote evidence commit](https://github.com/davidlueng986-alt/123321/commit/ea4f14b861f58652481cfbb82b8954d626aed74a).

```sh
cd research/mols10
node E046_trade_scan.js > E046_TRADE_REPLAY.json
node E046_independent_support.js > E046_INDEPENDENT.json
OPENBLAS_NUM_THREADS=1 python E046_phase1.py > E046_PHASE1.log
node E046_phase1_verify.js > E046_PHASE1_VERIFY.json
node E046_phase1_audit.js > E046_PHASE1_AUDIT.json
```

Source: [E046_trade_scan.js](E046_trade_scan.js), [E046_independent_support.js](E046_independent_support.js), [E046_phase1.py](E046_phase1.py), [E046_phase1_verify.js](E046_phase1_verify.js), [E046_phase1_audit.js](E046_phase1_audit.js). Evidence: [E046_TRADE_RESULTS.json](E046_TRADE_RESULTS.json), [E046_PHASE1_RESULTS.json](E046_PHASE1_RESULTS.json), [E046_PHASE1_VERIFY.json](E046_PHASE1_VERIFY.json), [E046_PHASE1_AUDIT.json](E046_PHASE1_AUDIT.json). Remote CPU workflow: https://github.com/davidlueng986-alt/123321/actions/runs/41531858521 (check final status separately).

## Negative evidence, caveats, next action
No LP-feasible k4 found in 131 chosen local neighbors; this is an empirical restricted search outcome with exact certificates, not a universal k4 theorem. The old dual's poor transfer rate makes **transporting one source Farkas cut** an ineffective stand-alone local-search oracle. **Next:** diversify the move generator (two disjoint swaps / 3-row rewrites) and use joint LP phase-I optimization rather than support-only ranking; in parallel, prioritize symmetry-complete proof-producing SAT with justified coverage. If any exact 100/100/100 triple or unrestricted exhaustive certificate appears, independently replay before changing status.
