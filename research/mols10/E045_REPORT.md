# E045 — LP-guided fourth-row rounding: 574 exact fixed-prefix obstructions

**2026-11-02 20:52–20:59 UTC. GLOBAL 3-MOLS(10): OPEN; 0/162959 complete normalized orbits excluded.**

## Read and external check
Read living [Google Docs journal](https://docs.google.com/document/d/1NDPWEMM3Cf5HrhdOcV6pVE9tCI-kxKbavxcfIBFva3k/edit), current STATE.json, E044 source and report, E033 orbit results. Fresh primary check: [Bright–Keita–Stevens EJC 33(1) P1.30 (2026-02-13)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30), [Barnoff–Bright arXiv:2605.02132v2 (2026-07-04)](https://arxiv.org/abs/2605.02132). Targeted 2026-11-02 search found no independently checkable unrestricted solution. No negative inference from absence of hits.

## Falsifiable question and method
Can a fourth row chosen from a numerically feasible k3 six-resource LP solution retain k4 six-class LP feasibility better than random MRV row generation? Take 48 distinct k3 parents from E044, evenly spaced across its 512 cases. For each, solve k3 Ax=1,x>=0; restrict each fourth-row placement to positive LP support; MRV DFS enforces one triple per column and one of each symbol in each square, ordering by LP weight with seeded Gamma perturbations. Twelve attempts per parent, deterministic seed 20261102045, 12000 DFS-node bound per attempt. This is a **heuristic**, not an exhaustive search.

**574 distinct valid k4 prefixes** from 576 attempts (two duplicate suppressions). Each has 40/40/40 overlays. All 574 raw ordered prefixes are distinct from E044's 512; isotopy inequivalence is NOT proved. Screening: 544 LP-infeasible, 30 exact zero-support, 0 feasible/UNKNOWN.

Every one of the 544 numerical negatives was upgraded to an **integer Farkas dual**: integer y indexed by 360 uncovered resources, sum(y)>0, and sum_{d in placement t}y_d<=0 for all legal residual placements. Other 30 have a missing mandatory resource with zero legal placements. Independent Node.js integer-only replay rebuilds 600 resource IDs, all 574 prefixes, **232513** legal placements, checks 574/574 exact certificates, and rejects a deliberately corrupted dual. **Exact PASS**. These certify only these **fixed prefixes**, not a full symmetry orbit or unrestricted nonexistence.

## Matched-parent A/B control
Same 48 k3 parents, 12 random MRV fourth rows each (576): 75 exact zero-support, 501 *numerically* LP-infeasible, 0 feasible/UNKNOWN. LP-guided support has fewer zero-support failures (30/574 = 5.2%) than matched random (75/576 = 13.0%), **but still zero k4 LP-feasible**. Repeated samples within parent are correlated; a naive Fisher test p≈2.7e-6 is descriptive only, not an independent-population claim. Improving local support does not by itself remove global fractional obstructions.

## Failed side experiment and audit
Attempted 200000 random prolongations of four GF(9) affine rows to ten columns via 12 symbol-9 swaps: zero valid k4. **Restricted stochastic failure only**, no nonexistence theorem. Preliminary 128-parent x24 run interrupted during JSON serialization: incomplete JSON discarded; partial log preserved locally. Monolithic certificate run interrupted after ~400: discarded and rerun in six bounded disjoint batches, 574/574 exact PASS. k3 LP feasibility is numerical only, no exact rational primal certificate.

## Reproducibility
Source input files already public on branch: E044_RESULTS.json, E044_disjoint_probe.py, E035_column_residual.py. E045 local attached bundle includes E045_guided.py, E045_certify.py, E045_verify.js, E045_random_control.py, E045_affine_prolongation.py, all 574 prefixes and exact certificates, matched controls, logs, and SHA256 manifest. Run E045_guided.py --parents 48 --per-parent 12 --seconds 40; certify in six disjoint batches [0,110),[110,220),[220,330),[330,440),[440,550),[550,574), merge sorted by index, then node E045_verify.js. Independent clean ZIP replay: SHA256 and Node verifier PASS.

Local E045 ZIP SHA256: `ef323379084290153e73de60ea87127251a6286345e0e72f0da8028394e4593c`. Do not claim binary uploaded to Drive unless separately confirmed.

## Next
Seek **joint** fourth-row + residual fractional LP feasibility (phase-I infeasibility minimization) rather than merely maximizing positive LP support. Continue unrestricted 12-type / 162959-orbit proof-producing SAT with justified symmetry coverage. No 100/100/100 candidate or complete negative proof; research remains active.


## Independent GitHub Actions replay — 2026-11-02 21:02 UTC
CPU-only [workflow run 41524497856](https://github.com/davidlueng986-alt/123321/actions/runs/41524497856) **SUCCESS**, independently regenerating the guided k4 sample, exact certificates, matched controls, and executing the standalone integer-only Node.js verifier. The remote solver environment generated **570** distinct guided k4 prefixes, not the local **574**: **532** exact integer Farkas duals + **38** exact zero-support, **231303** residual candidates, **570/570 PASS**, mutation rejected. Matched random controls reproduced **501 numerical LP-infeasible + 75 exact zero-support** on 576 attempts. Both local and remote samples have zero k4 LP-feasible cases, but sample counts/inputs differ due solver/runtime dependence. Do **not** claim byte-for-byte deterministic reproduction across environments; both result sets were independently exact-verified.

Full remote input JSON, 570 certificates, control JSON, logs and SHA256 were **persisted publicly** in [commit ea4f14b](https://github.com/davidlueng986-alt/123321/commit/ea4f14b861f58652481cfbb82b8954d626aed74a). Remote SHA256: E045_GUIDED_RESULTS.json `20db4e622328d960263255d5fb17979ef486614cdad9bf5c0800cecb3c1da95a`; E045_CERTIFICATES.json `f5ceb943344d04901a302703f667291f432174ac707b6fbf11840b64003de564`; E045_RANDOM_CONTROL.json `eecf568b0465426c59e4581e8224178588215d81ea13343b7d8bbdb04f7351a4`. Local ZIP remains a separate 574-case verified evidence set; Google Drive binary upload still FAILED BLOCKED_FILE_REFERENCE.
