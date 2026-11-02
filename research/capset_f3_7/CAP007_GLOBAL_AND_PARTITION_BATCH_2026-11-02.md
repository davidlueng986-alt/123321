# CAP-007G / CAP-006B — bounded batched global modelling and independent falsification (2026-11-02)

## Grounding, safety and scope

Continued from CI-GREEN CAP-006A projection audit and CAP-005M corrected blossom CI, without touching other branches or math problems. The exact open problem remains r3(7), not merely finding 237. No new >=237 cap and no new competitive global upper bound. All tests below are CPU-only; no GPU or paid service.

## Experiment 1 — Full global 237-target CNF (not neighborhood search)

Encode each x in F3^7 by a Boolean variable indicating selection. For each unordered affine line {u,v,w}, impose (¬x_u∨¬x_v∨¬x_w). Number of points = 2187; number of lines = 2187×2186/6 = **796797**, independent of the 236-cap fixture. Add an EXACT at-least-237 sequential counter using 490353 auxiliary variables, requiring 492540 total variables and **1775353 clauses** with affine-basis fixing.

Full affine-span symmetry breaking: a cap with at least 237 points cannot lie in a 6-flat, because r3(6)=112. Every affinely spanning set contains an affine frame of eight affinely independent points; an affine automorphism sends that frame to 0,e1,...,e7. Then 8 points must be selected and 28 other points determined by their secants must be excluded. This is a valid no-loss reduction, unlike invariance under an arbitrarily chosen subgroup.

The sequential implication encoding is equisatisfiable: s[i,j] -> s[i-1,j] OR (x_i AND s[i-1,j-1]), with s[N,237] true. An assignment with at least 237 points extends to a valid prefix counter; conversely the implications plus final unit imply at least 237 selected. No solver outcome has been asserted.

The local file /mnt/data/capset_n7_target237.cnf was produced in 5.2 CPU seconds (approx 35 MB; **SHA-256 eddbfcdb6dd1380e59dcafd83cc701a058a8ee8acbae5073d3b4ddd03bc95d12**). This artifact remains local unless separately shared; the reproducible generator is in GitHub. Generator supports n=1..7, optional basis, DIMACS and summary. Tiny n=2 exhaustive test and n=3 9-cap assignment test pass; direct known 236 cap satisfies target236 without normalization and fails target237 as expected.

A CPU MILP control on the same global line constraints returned a rigorously checked 9-point n=3 witness with solver optimal status. The n=4 normalized model found a 20-point valid cap within 16 s, but the solver timed out without establishing the 20 upper bound (dual 22); this **does not** constitute an n=4 computational proof. Novelty of the CNF encoding itself is NOT claimed.

Reproduce:
```bash
python -m unittest discover -s research/capset_f3_7 -p 'test_cap007_*.py' -v
python research/capset_f3_7/cap007_global_exact_model.py --n 7 --target 237 --basis --out /tmp/capset_n7_target237.cnf
sha256sum /tmp/capset_n7_target237.cnf
```

## Experiment 2 — EXACT negative result for overly coarse global occupancy inequalities

Take ANY full-rank linear quotient F3^7 -> F3^3, split into 27 four-dimensional fibers with integer occupancies c_u. The known exact caps r3(4)=20, r3(5)=45, r3(6)=112 yield for every fiber c_u<=20; each of the **117** quotient affine lines L: sum_{u in L} c_u<=45; and each of the **39** quotient affine planes P: sum_{u in P} c_u<=112. No cross-fiber compatibility condition is used.

**Exact optimum of these three types of count-only constraints: 333**, NOT a cap construction. An explicit 27-integer vector summing to 333 satisfies all 117+39 quotas (largest line occupancy 38, plane occupancy 112). Independently verified by pure integer arithmetic.

Proof of the 333 upper bound without trusting MILP:
M=sum c_u<=336 from the 6D plane quotas. For M=334, 335, 336, in each of 13 parallel classes, the three plane counts must respectively be permutations of (111,111,112), (111,112,112), (112,112,112). Double counting point-pair incidences gives
SUM_{all 39 planes} occupancy(P)^2 = 4*M^2 + 9*SUM_{27 fibers} c_u^2.
Indeed each point appears in 13 quotient planes and each unordered pair in four. The left side minus 4M² is nondivisible by 9 for M334,335,336, with remainders 6,4,3. Contradiction. Therefore M<=333. Since feasible count vector of sum333 is provided, this is exact optimum of this RELAXATION.

**Strategic falsification:** Pure subspace size quotas cannot approach the known <=291 upper bound, let alone solve r3(7). Higher-value cuts must use cap-specific intersections, cross-slice sumsets, classifications of large lower-dimensional caps, or proof-logged global SAT/SDP. Do NOT promote 333 as stronger than existing global bounds.

Reproduce: `python research/capset_f3_7/cap007_quotient_limits.py`.

## Experiment 3 — 320 matched 8-fiber release neighborhoods in three inequivalent linear projections

Using the same known 236-point baseline, three full-rank 3x7 projections (previous CAP-006A baseline Q=2884; low concentration Q=2096; high Q=3186) and exactly the SAME 320 uniformly sampled eight-fiber release masks (Python Random seed 20261102), independently recomputed every outsider's secant incidence. N(T) counts individually admissible outsiders if the old points outside T are fixed. It does NOT enforce outsider mutual compatibility.

Results:

| projection Q | maximal N(T) sampled | release masks with N>=17 | masks with N(T) > old points released |
|---|---:|---:|---:|
| baseline 2884 | 124 | 37 / 320 | 1 |
| low 2096 | 2 | 0 / 320 | 0 |
| high 3186 | 45 | 19 / 320 | 0 |

The only sampled positive naive gain margin is at T=(0,1,5,6,8,11,18,19), baseline 236, where 85 old points are releasable and 124 outsiders are individually eligible (naive margin +39). A solver model containing ALL exact pair/triple collinearity constraints among the 209 variable points returned a valid 236-point cap and integer optimum 85 for this released region (HiGHS 2.6 s, CPU); however this MILP optimum lacks a stand-alone independently reviewable dual/UNSAT proof and must remain **solver-reported, not independently certified**. Its ordinary LP relaxation optimum is 110.5, showing a 25.5 integrality gap. This is an adversarial example of how misleading N(T) can be. It also falsifies using occupancy concentration Q as a monotone predictor of improvement.

No other 8-fiber masks have been solved to optimality; these are pilot data only. The three different matrices are not proved inequivalent under the entire automorphism group of B (only their occupancy profiles differ). Identical uniform masks are used across matrices to reduce selection bias; 320 finite samples are not the full binomial(27,8) space.

Reproduce:
```bash
python research/capset_f3_7/cap006b_partition_pilot.py
OPENBLAS_NUM_THREADS=1 python research/capset_f3_7/cap006b_reconstruction_milp.py --seconds 12
```

## Primary literature and intellectual pivot

- Thackeray, *The cap set problem: Up to dimension 7*, arXiv:2206.09804, especially Theorem 4.2 and Lemma 2.1 about near-extremal 5D/6D cap structures: his exclusion of 289 uses **classification and cross-slice geometry**, not only dimension-wise occupancy quotas. https://arxiv.org/abs/2206.09804
- TU Delft Versluis thesis (2017) gives published 291 global upper bound by recursive upper-bound approaches. https://repository.tudelft.nl/record/uuid%3A6818b21f-038d-4700-afcd-e6dac79e7e82
- FunSearch (Nature 2024) finds generating programs, not just local point moves: https://www.nature.com/articles/s41586-023-06924-6
- X-evolve (arXiv:2508.07932) evolves parameterized solution spaces and asymptotic constructions, not an n7 exact solution.

## Highest value next hypotheses (prioritized; all falsifiable)

**CAP-007H [P0]** Decompose arbitrary n7 cap into three 6D slices, but do NOT force their sizes to be 112+112+12. Add cross-slice convolution constraints and classified high-size 6D caps as *conditional* cutting planes, then test proof-logged SAT/ILP on small n where exact optima are known.

**CAP-008B [P0]** Establish proof-checkable global symmetry reductions beyond one affine basis (e.g., stabilizer orbit representatives of a second/third selected point). Never use a symmetry assumption that excludes legitimate cap candidates.

**CAP-006C [P0]** Nonlocal generator-family search (priority-program and admissible-template evolution) that need not remain near Calderbank–Fishburn. Apply direct independent F3 checker to every candidate and compute affine equivalence before counting distinct constructions.

**CAP-007I [P1]** Add exact 5D/6D *configuration-specific* forbidden occupancy profiles from peer-reviewed classification, not just cardinality constraints. Audit Thackeray's source proofs, not just a short abstract.

**CAP-008C [P1]** Certificate audit and adversarial tests: independent geometric checker, deliberately corrupted witness, affine conjugacy and normalization, proof-logged solver artifact checks.

**CAP-006D [P2]** Structured eight-plus-fiber rewrites are worth exploring only after demonstrating an exact compatible outsider packing, not because N(T) is large. Abandon a fixed neighborhood if only loose LP gap remains.

## Conclusions and honesty boundary

The global model is now a concrete, reproducible open decision problem; no SAT solver has returned an independently verified SAT witness >=237 or UNSAT proof. The exact 333 occupancy relaxation shows why naive slicing quotas cannot close the gap. The 8-fiber pilot reveals a strong integrality gap; the solver-reported restricted optimum 236 is not a rigorous certified exclusion. No novelty asserted; campaign continues.

## CAP-007H supplement (2026-11-02T10:49:06.157Z): conditional globally meaningful branch
Potechin 2008 (DOI 10.1007/s10623-007-9132-z) proves all maximal 112-caps in AG(6,3) are affinely equivalent. Any seven-dimensional 237-cap that has a 112-point affine hyperplane can therefore be mapped to a fixed explicit 112-cap in the first slice x0=0. The other two six-dimensional slices have 729 possible points each; each is itself a cap. Every fixed point c in the 112-set and any y in slice1 forbids exactly z=-c-y in slice2. This yields exactly 2*88452=176904 within-slice line clauses, 112*729=81648 cross-slice pair clauses and one at-least-125 sequential cardinality counter. No target237 SAT/UNSAT result yet.
Generated local DIMACS: 175958 variables / 606095 clauses, SHA256 93faf29af90fb4b33ae68e08d889e02d0d5a43565afabf9f5878772738f4f830 (11MB); known 236 witness satisfies 236-target and fails 237-target on full independent clause evaluation. This is a much broader proof target than changes near the 236-point baseline, but it is still conditional on having an extremal 112 hyperplane. Certification must come from a proof-logging solver and independent checker, not a solver status alone. Novelty not established.
