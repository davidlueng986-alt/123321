# CAP-056 — Direct full-root feasibility attempts after true Lasserre-2

**Date:** 2026-11-08 (Asia/Hong_Kong). **Exact unsolved target:** determine `r_3(7)` in `F_3^7`. **User-defined result status:** **NOT DONE (ATTEMPTED)**. No ≥237-point cap, no independently verified complete UNSAT proof, no new published-scale mathematical breakthrough. Nothing in this report establishes `r_3(7)=236`.

All scripts directly implement a logically complete decision test for the **existence of exactly 237 points** under the previously proven CAP-052 dense-hyperplane/center normalization. In this form 11 points are mandatory, 52 are forbidden, and 2,124 remain unrestricted Boolean variables; 226 of these must be selected, with ≥79 selected within the 677 free points of the distinguished dense 6D hyperplane and ≥3 further antipodal pairs around the center. The ambient cap property forbids all 796,797 affine lines in `F_3^7`. Existing actual 236-point construction is not claimed to be globally optimal.

## Actual attempt A — native Z3 on the whole root (NOT DONE)

`cap056_direct_root_sat.cpp` builds **the entire** anchored n=7 cap instance, not a symmetry-conditioned subset. It enforces all 11 fixed inclusions and 52 exclusions, exactly enumerates all affine lines and classifies them into 55,554 satisfied, 11,475 residual binary, and 729,768 residual ternary clauses. It adds ≥226 remaining selections, ≥79 dense-H selections, and ≥3 extra antipodal pairs among 331 possible pairs (four pairs guaranteed by the anchors).

Compiled against the actual installed `libz3.so.4` and **executed** with a 45,000-ms solver timeout. Model-building time **0.514 seconds**. Z3 returned `UNKNOWN (timeout)` after **45.562 seconds**. No satisfying assignment, no UNSAT certificate. It is invalid to report the timeout as a disproof.

## Actual attempt B — HiGHS integer model with ALL 6D hyperplane cuts (NOT DONE)

Independent NumPy/SciPy sparse code `cap056_direct_root_milp.py` builds the same **complete root** with 2,124 Boolean point variables and 329 Boolean free/free antipodal-pair auxiliaries. Alongside all 741,243 nontrivial residual affine lines, the solver enforces **all 3,279 affine 6D cosets** of the 1,093 projective normal directions to contain at most the established `r_3(6)=112` cap points. Total: **745,183 constraints and 4,538,234 nonzero coefficients**; the exact root uses 226 free selected points, ≥79 in dense H and ≥3 additional centered pairs.

An important adversarial audit detected a **false early infeasibility** in the initial encoding: the intended auxiliary constraint `z - x ≤ 0` was mistakenly implemented as `z + x ≤ 0`, forcing almost all antipodal pairs to zero. **This result was invalid and discarded**, before making any mathematical claim. The corrected script explicitly asserts **every** such sparse matrix row has coefficients `(z,+1)` and `(x,-1)`.

**Corrected run:** built model in **2.31 seconds**. HiGHS used a 38-second solving time limit and returned `status=1, Time limit reached`, after **41.15 seconds total**, with no feasible integer 237-cap. This is **UNKNOWN**, not a certificate.

### Exact fractional positive control (what does *not* prove nonexistence)

`cap056_fullroot_fractional_audit.py` gives a simple **rational** feasible point of the **entire above LP relaxation**, **including every 6D coset cut and all pair-auxiliary rows**:

- Each of the 677 free dense-H points has value `79/677`.
- Each of the 1,447 free non-H points has value `147/1447`.
- Each of the 329 free/free antipodal-pair auxiliaries has value `79/677` (the same as both H endpoints); the two mixed anchor/free pairs contribute `2·79/677`.
- Hence the total free cardinality is **exactly** `677·(79/677)+1447·(147/1447)=226`; the H threshold holds at equality 79, and 331 viable extra antipodal terms sum to `331·79/677 > 3`.
- Every residual binary 3AP inequality obeys `x_i+x_j ≤ 2·79/677 < 1`. Every residual ternary inequality obeys `x_i+x_j+x_k ≤ 3·79/677 < 2`.
- Every 6D affine hyperplane has at most 11 fixed selected points and 729 free points, each ≤79/677; hence its weighted total is ≤`11+729·79/677 = 65038/677 <112`, regardless of orientation.

This is **NOT A CAP**. It explains why simply adding *all* standard low-dimensional affine hyperplane inequalities does not close the integer feasibility question. Any actual `UNSAT` argument must exploit integrality or stronger cross-hyperplane/SOS structure.

## Actual SDP reduction barrier for CAP-055

A complete t=2 Lasserre matrix indexed by all squarefree degree≤2 subsets of the 2,124 free coordinates has 2,256,751 rows. The order-768 residual symmetry group is insufficient by itself to create a small plain orbit-indexed primal LP:

- Unrestricted distinct free 4-monomials: `C(2124,4)=845,627,918,751`.
- Invalid because containing one of the 11,475 forced-zero pairs: **at most** `11475·C(2122,2)=25,823,121,975`.
- Invalid because containing one of the 729,768 forbidden free triples: **at most** `729768·2121=1,547,837,928`.
- Thus ≥**818,256,958,848** distinct degree-four monomials survive this zero-ideal pruning. Any orbit has ≤768 members, so ≥**1,065,438,749** separate quartic moment orbits remain **before** cardinality linear identities, additional PSD algebraic reductions and representation-theoretic block compression. Just one float64 scalar per orbit takes ~**7.94 GiB**, exceeding current 4 GiB memory.

This is **not** an impossibility theorem for clever SDP/SOS methods: the linear cardinality relations can eliminate more variables, while a sparse dual certificate need not materialize the full primal moment space. It does **disprove** the plan "apply the order-768 symmetry and directly store every surviving quartic orbit parameter" under present memory.

## Final decision

**Exact `r_3(7)` remains OPEN.** The root SAT and MILP both ran and returned UNKNOWN; the strict integer false-UNSAT bug was caught; the complete SDP with all true localizers is not solved. There is neither an independently verified ≥237-point witness nor a global rational SOS/DRAT certificate for the opposite statement. No extra experiments will be rebranded as solved. The specific missing action is a **mathematically sound sparse global SOS dual** or a dramatically stronger complete exact-search compression; nothing currently shows a 768-order quartic primal reduction will fit the memory.

All actual source, stdout/stderr, proof-bound checks and correction evidence are in the companion ZIP. No External Advisor Brief is included. Hourly CAPSET automation remains disabled; no unrelated mathematics branch was changed.


## Verified durable evidence

Complete C++ native Z3, corrected independent HiGHS 0/1 full-root MILP, rational fractional-primal audit, raw stdout/stderr and JSON manifest: https://drive.google.com/file/d/1OrMmDi6Rkzd3KPcxXbcNSpJC7P9HSCcD/view?usp=drivesdk  (ZIP SHA256 `102c40b85d4de656ef697b6edc8ef159fbcedbe5852a29437a3110b4b97ad366`). Source contains no External Advisor Brief.

## Extended complete-root HiGHS run — 150 seconds, still UNKNOWN
We also spent the **full 150-second MIP solver budget** on the corrected 2453-binary,745183-constraint globally exhaustive CAP052 + ALL 3279 AG6 cuts model. Actual HiGHS output: **Time limit reached; zero branch-and-bound nodes; 6398 root LP iterations; primal bound inf; dual bound 0; no integer incumbent; no UNSAT certificate.** Solver time 150.06s; wall including build 153.27s. The long timeout therefore did NOT exhaust a proof tree, nor produce any cap. An exact fractional LP feasible point remains known. Updated source, all stdout/stderr: https://drive.google.com/file/d/1AnHRAiVuWmE3_hikxTgqV9ngDQhp-IVJ/view?usp=drivesdk ; concise note: https://drive.google.com/file/d/1uZEAtAy6x4K_ZGGgWeFttKwog3azGYlV/view?usp=drivesdk . SHA256 long ZIP 31b2711ab00b1675b6db5071c49811ddb0aedbd8260f792e199fd5ef6a9a9bb3. Root status unchanged: OPEN.
