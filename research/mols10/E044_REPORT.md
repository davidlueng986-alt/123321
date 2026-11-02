# E044 — Independent randomized k4 prefixes: exact six-resource obstructions

**UTC:** 2026-11-02 19:49–19:53. **GLOBAL STATUS: OPEN**; 0/162959 complete symmetry orbits excluded. No 100/100/100 triple or unrestricted nonexistence certificate.

## Primary literature checked
- Bright, Keita & Stevens, *Myrvold's Results on Orthogonal Triples of 10×10 Latin Squares: A SAT Investigation*, EJC 33(1) #P1.30, published 2026-02-13: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 . Explicitly open unrestricted problem; 4×4-subsquare special cases.
- Barnoff & Bright, *Improving SAT Solvers on Orthogonal Latin Square Problems*, arXiv:2605.02132v2, revised 2026-07-04: https://arxiv.org/abs/2605.02132 . Hybrid SAT/Euler–Parker for orthogonal PAIRS, not a full triple.
- Targeted 2026-11-02 search: no independently verified new unrestricted resolution located. Absence of search hits is not proof.

## Falsifiable new experiment
E039/E043's 2340 four-row prefixes were all drawn from 156 preselected E036 six-row witnesses, each with first-square second-row cycle type 2+2+2+2+2. E044 uses an independent deterministic randomized generator: first rows are 0..9; second rows of all three squares are randomly chosen derangements, pairwise distinct at every column; third and fourth rows are built by bounded MRV DFS enforcing all row, column, and overlay uniqueness. Seed 20261102; 512 attempts; per-row 12000-node bound; 512 valid 40/40/40 four-row partial triples. Raw ordered-prefix overlap with the E036 2340 = 0; this does NOT prove isotopy inequivalence. Samples cover 11 of 12 derangement cycle types (the rare 2+2+2+2+2 is absent). Sampling is nonuniform.

For each fixed k4 prefix, residual candidate t=(column,a,b,c) consumes one of each of six resources P_AB,P_AC,P_BC,C_A,C_B,C_C. A full triple would require exact cover Ax=1, x>=0. An integer Farkas dual y with sum(y)>0 and y^T A(:,t)<=0 for every permitted t proves that PARTICULAR prefix nonextendible. A mandatory resource with no legal candidate is a separate exact obstruction.

**Actual results:** 471 numerical LP-infeasible cases, 41 exact zero-support, zero feasible/unknown. Every numerical negative was upgraded to an exact integer Farkas certificate; min dual sum +3, max candidate dual score -6. An independent Node.js verifier reconstructs 512 partial Latin rectangles, all 200094 legal residual placements, all 471 integer inequalities and 41 zero-support contradictions; 512/512 PASS, mutation rejection PASS. This does NOT exclude any full orbit.

**Parent controls:** The first three rows of each of the same 512 cases are 512/512 NUMERICALLY six-resource LP-feasible, max residual 9.71e-13. No exact rational primal certificate claimed. This sampled k3->k4 feasibility cliff is not a universal theorem.

**Failed/unknown experiments:** E041 deleted-cell integer exact-cover pilot timed out on eight 4-second MILP runs; these are UNKNOWN, not UNSAT. The 512 randomized prefixes are not exhaustive or uniform; cannot conclude universal k4 obstruction.

## Reproduction
Files: E044_disjoint_probe.py, E044_certify.py, E044_verify.js, E044_k3_controls.py; reuse existing E035_column_residual.py. Run in research/mols10:

```sh
OPENBLAS_NUM_THREADS=1 python E044_disjoint_probe.py --attempts 512 --seconds 95
OPENBLAS_NUM_THREADS=1 python E044_certify.py
node E044_verify.js
OPENBLAS_NUM_THREADS=1 python E044_k3_controls.py
```

Local complete bundle with 512 prefixes, 512 exact certificates, k3 controls, logs and SHA256 manifest: E044_MOLS10_RESEARCH_BUNDLE.zip. Data SHA256: E044_RESULTS.json a3321997c8ac90bf802366a9f6de769dbedac11b22d78c27265ec0644ecd480d ; E044_CERTIFICATES.json be75a0786f265a1b5d06853d5a07a8dd22022d344584b3acc9a8176c2e385f01 ; E044_K3_CONTROLS.json 33122658c28a7080a7e5bb7bf49d1bb5cc3e7a390f72f2c81ba6a07ea8c2f3ce. Local ZIP SHA256 06be58a9171686fe617bf09a7c0161969eaf517ebfc3ca2e0d1851bc45e11997. Full certificate bytes are in the local downloadable bundle; DO NOT claim them committed unless separately uploaded.

**Next:** Constraint-guided search targeting a k4 six-class LP-feasible prefix, not another greedy sample; independently rationalize any positive LP primal; continue proof-producing symmetry-complete SAT. Maintain global OPEN status.

## Remote independent replay and persistent evidence (2026-11-02 19:59 UTC)

GitHub Actions CPU-only independent run https://github.com/davidlueng986-alt/123321/actions/runs/41514534121 **SUCCEEDED on attempt 2**. It regenerated all 512 prefixes and all 512 exact certificates, ran the independent Node.js verifier, obtained 512 PASS / 471 integer dual / 41 zero-support / 200094 allowed placements / mutation rejected, and committed the full regenerated JSON and logs to GitHub: https://github.com/davidlueng986-alt/123321/commit/42dbc1ae9fd2a928c6f525d247dc820432b2d627 . This is an independent execution environment, though the verifier algorithm was the same checked JS implementation.

Attempt 1 FAILED due to an **empty E035_column_residual.py on the repository branch**, not a mathematical contradiction; restored the model in https://github.com/davidlueng986-alt/123321/commit/22296cab5d426beaa0e9c40fa90f426318409442 , then reran successfully. Keep failure as reproducibility evidence.

Remote-generated SHA256: E044_RESULTS.json 839b6d134a29e1343c08bee50db67cade1ddb588df65d692a43a665b4945f242 ; E044_CERTIFICATES.json a399916900ee4334959aaae64e63e62a0517757876ba4828235ef1834092e00f ; E044_K3_CONTROLS.json 3e6ca472e4cb37084b8238afe0bb7f6af5709922e01554b01f343125f7bc2c66 . These differ from local SHA256 because runtime/timing and solver implementation versions differ; both exact verifiers passed. **Full 512-case data are now publicly persisted in GitHub**, superseding the earlier 'local-only' caveat. Google Drive binary ZIP upload attempted and FAILED BLOCKED_FILE_REFERENCE; Docs journal is updated.
