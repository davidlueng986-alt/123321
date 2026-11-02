# E038 — Exact certification of 360 four-row obstructions and triadic resource-forcing cuts

**Timestamp:** 2026-11-02 13:58 UTC. **Global status: OPEN.**

## Primary-source check
- Bright, Keita & Stevens, *Electronic Journal of Combinatorics* 33(1), P1.30 (2026-02-13): https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 — explicitly calls 3-MOLS(10) open; their SAT results are restricted to a 4x4 subsquare hypothesis.
- Barnoff & Bright, arXiv:2605.02132 (2026; https://arxiv.org/abs/2605.02132) — SAT/Euler–Parker improvements for orthogonal **pairs**, not a triple.
- Targeted 2026-11-02 searches found no independently checkable unrestricted triple or exhaustive nonexistence proof. Negative search evidence is not a proof of continued openness.

## Falsifiable objective (nonduplicate of E037)
E037 tested 360 legal 4-row partial triples, 30 per each of the 12 normalized second-row cycle types, reporting 43 exact zero-support contradictions and **317 numerical LP infeasible statuses without exact certificates**. The primary objective was to convert **every one of the 317** into a standalone, exact, independently checked mathematical certificate, then extract cheaper generalizable local cuts beyond E037's 15 pairwise Hall projections.

## Exact result: 360/360 fixed-prefix exclusions
For each fixed prefix, let `A x = 1, x >= 0` be the column-aware residual exact-cover relaxation: one constraint for each missing ordered pair in AB/AC/BC and each missing (column,symbol) in A/B/C, and a candidate column for each permitted future (column,a,b,c) placement. This ignores missing-row assignments, so feasibility is **necessary**, not sufficient, for a full 3-MOLS(10) extension.

- **43/360**: exact zero-support demand (no candidate can satisfy a required resource).
- **317/360**: exact integer Farkas certificate `y` with `sum(y)>0` and `y^T A_j <= 0` for **every** candidate `j`. If `Ax=1, x>=0`, then `0<sum(y)=y^T Ax=sum_j x_j(y^T A_j)<=0`, contradiction. The generator used numerical HiGHS only to propose `y`; the independent JavaScript checker reconstructs the candidate set and verifies every integer inequality without SciPy, LP, or floating-point operations.
- Independent verifier **PASS 360/360**, plus prime-order n=5 positive full-triple control and deliberate mutation rejection of both dual and zero-support certificates. Full certificate JSON SHA256 `2a470b6ad366acc430def383461826b03bb01d03b8bc8b14cb415d8b5a876127`.
- Across the **same 360 fixed prefixes**, dropping the fourth row gives **360/360 numerical LP-feasible** three-row prefixes (12 types x 30). This identifies a striking sampled k3→k4 feasibility transition, **not** a universal theorem. Those positive LP results are numerical, not exact primal witnesses.

## New exact pruning rule: triadic resource forcing
Every candidate placement consumes exactly one demand from each of six classes (`P_AB,P_AC,P_BC,C_A,C_B,C_C`). Find three *distinct* required demands `d1,d2,d3` with `d1,d2` from **different** resource classes such that **every** permitted candidate `t` obeys:

`1[d1 in t] + 1[d2 in t] - 1[d3 in t] <= 0`.

Summing over a hypothetical complete cover gives `1+1-1 <= 0`, contradiction. This is a sound **three-resource** Hall-like inequality, not in general implied by the 15 pairwise bipartite Hall projections. It is cheap to detect via support-set intersections, and it never excludes an entire orbit merely because one fixed prefix fails.

- Applied to the 317 nonzero-support prefixes: **59/317** have an exact triadic obstruction; **51** of those were **not** rejected by E037 Hall15.
- Thus, on the original 360 biased samples, E037 Hall15's **65** rejections plus the **51** new-only triads yield **116/360** local rejections by the combined cheap rules (versus 65/360 Hall15 alone).
- Independent JavaScript verifier **PASS 59/59**, each checking all candidate placements and exact inequalities; mutation rejected. Known affine 3-MOLS at n=5,7,11, k=2,3,4, all passed the triad test (no false obstruction).
- A sparse integer-dual MILP probe on **one Hall15-surviving prefix per each of the 12 cycle types** found independently verified certificates of **3–9** nonzero demand weights (support sizes `[5,7,7,5,7,9,7,7,7,7,5,3]`). The 3-term case witnesses an especially simple forced-common-resource contradiction.

## Failures and limitations
- An attempted **all-317 sparse-MILP minimization** was interrupted by a runtime timeout after logging partial progress; it produced no completed aggregate output. **Do not count** a completed 317-sparse run. The successful 12-type sparse probes are separate and complete.
- All 360 prefixes are E037 **sampled** and nonuniform. They are **not** exhaustive over the 162,959 globally normalized first-two-row orbits, much less all extensions of each orbit. **Zero** complete orbits have been ruled out. No full 100/100/100 witness exists in this project's verified results. No unrestricted nonexistence certificate.
- No defensible ETA. Novelty of the triadic cut relative to general hypergraph matching / Farkas theory is not asserted; it is a new tested pruning implementation in this workspace.

## Reproduce (CPU, no GPU)
Unzip the self-contained archive into one directory; all scripts use paths relative to their own directory. Execute:

1. `OPENBLAS_NUM_THREADS=1 python E038_generate.py` — 317 exact integer duals + 43 zero-support certificates (~12.2 s).
2. `node E038_verify.js` — independent 360/360 exact verification and negative/positive controls.
3. `OPENBLAS_NUM_THREADS=1 python E038_sparse_probe.py` — 12 sparse ±1 motifs (~3 s).
4. `node E038_verify_sparse.js` — independent 12/12 exact verification.
5. `OPENBLAS_NUM_THREADS=1 python E038_triads.py` — 59 triadic obstructions and Hall15 comparison (~0.6 s).
6. `node E038_verify_triads.js` — independent 59/59 exact verification.
7. `OPENBLAS_NUM_THREADS=1 python E038_positive_controls.py` — n5/7/11 affine controls.
8. `OPENBLAS_NUM_THREADS=1 python E038_k3_controls.py` — numerical k3 LP controls (not a proof).

The self-contained Drive ZIP contains the E037 sample inputs, E035 residual model, E038 scripts, certificates, all witnesses, summaries and manifest. Files are **not** public global certificates.

## Next highest-value action
Integrate triadic forcing after zero-support and Hall15 in the **globally symmetry-complete** E033 row-extension search; use exact Farkas certificates for deeper branches. Then either (a) find a genuine k4 LP-feasible prefix and pursue 10 rows, or (b) prove **all** normalized first-two-row orbit extensions impossible with independently verified coverage. Prioritize mathematical generalization of 3/5/7-weight motifs and search for counterexamples, not more biased k4 sampling. Verify any 100/100/100 triple independently before announcing resolution.

## Verified archive and public replay links
- Drive full E038 bundle: https://drive.google.com/file/d/1O40oOCu5JEFdDpAk5416YJHqQVbkRplC/view
- Standalone 12 sparse certificates: https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/E038_PUBLIC_12_CERTIFICATES.json
- Standalone 12-case independent Node verifier: https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/E038_verify_public_12.js
- Full 360 exact certificates and 59 triad witnesses are in the Drive bundle; the 12 public sparse witnesses are a **subset**, not a global certificate.
