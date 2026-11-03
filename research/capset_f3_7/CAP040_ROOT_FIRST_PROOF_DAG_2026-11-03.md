# CAP-040 — Root-first, complete proof DAG for exact r₃(7)

**Date:** 2026-11-03 UTC. **Scope:** the full seven-dimensional cap-set decision problem, NOT a neighborhood of the 236-point witness and NOT the fixed formal 285-point occupancy of CAP027–039. **Status:** deterministic CPU finite symmetry audits PASS locally; repository CI pending on full code; SAT/UNSAT UNKNOWN; no new cap or global numeric upper bound.

## Root theorem: precise proof obligation

A 236-point cap is independently checked in `candidates/calderbank_fishburn_236.txt`. Consequently

```
r3(7)=236
    iff no cap of size >=237 exists
    iff the ROOT GLOBAL SAT-237 problem is UNSAT.
```

An independently checked >=237 witness would disprove `r3(7)=236`, **not** determine the exact maximum. The campaign terminates only at matching global lower/upper bounds.

## Route A: 13 exhaustive affine-frame ninth-point cases

Every cap with >=237 points affinely spans F3^7: otherwise it lies in some affine 6-flat, contradicting the known r3(6)=112. Choose any eight affinely independent cap points and transform them to the simplex vertices B={0,e1,...,e7}. The remaining cap points avoid all 28 third points `-b_i-b_j` from pairs of B.

An affine automorphism permuting the eight chosen simplex vertices acts by permuting their *barycentric coordinates* (λ0,...,λ7), with sum λ_i=1 in F3. Hence orbits of a ninth point are classified **exactly** by the triple (#λ=0,#λ=1,#λ=2). Directly enumerating all 2187 ambient points produces 15 barycentric types. Two are unavailable: the eight basis vertices themselves, type (7,1,0), and their 28 secant thirds, type (6,0,2). The remaining **2151 compatible points form 13 complete S8 orbits** of sizes [1,56,28,56,280,8,420,168,56,560,280,70,168].

Therefore ANY hypothetical >=237 cap is affine equivalent to one containing the eight standard basis points **and one of 13 canonical ninth points**. Let SAT_i be the standard global 237-target CNF plus this ninth point and its sound secant-forced exclusions. Then:

```
No 237 cap  <=>  UNSAT(SAT_0) AND ... AND UNSAT(SAT_12).
```

This is a global exhaustive disjunction, independent of the particular 236-point construction. No SAT_i has been solved yet.

For the 13 representatives, the nine selected points force 36 distinct negative points in 12 classes and 35 in one class. Each canonical branch has 492540 variables and **1775361 or 1775362 clauses**. The standard encoding's at-least-237 counter is reused unaltered; only 8 or 9 additional unit clauses are needed beyond the 8-point frame.

Further branching is also provably complete: after fixing a ninth point, its stabilizer within S8 is S_{n0}×S_{n1}×S_{n2}. The tenth point's orbit is classified by the 3×3 contingency table of its barycentric coordinates relative to the ninth. Verified all 2142 or 2143 allowed tenth-point positions per branch; their number of stabilizer orbits is [11,62,48,73,138,29,167,114,62,187,138,67,115], total **1211**. Every class size is an exact product of three multinomial coefficients, checked against full point enumeration. The extra tenth-point branching is optional and may increase runtime; it is *not* an asserted solver performance gain.

## Route B: one moment-anchored, globally complete SAT problem

The already CI-GREEN CAP007J exact 2nd/3rd moment lemma proves every 237-cap has an affine 6D hyperplane containing >=89 points. Specifically, assuming every such hyperplane has at most 88 points yields nonnegative per-direction W+9V but exact total `Σ(W+9V)=-35076`, contradiction. Independent current-run arithmetic enumerated all 75 possible unordered slice profiles under the false max88 assumption. The threshold 89 is an established universal lemma, not an empirical guess.

Because **89 > r3(5)=45**, the cap intersection with that hyperplane spans the entire affine 6-flat. Choose seven cap points affinely independent within H, and one cap point outside H (exists since 237>r3(6)=112). Normalize to B={0,e1,...,e7} with H={x7=0}. Thus **without loss of any 237-cap**, add the globally valid constraint `sum_{x7=0} x >=89` to the already full 3AP CNF (796797 forbidden triples + at-least-237). Only the existing known-theorem dependencies r3(5)=45 and CAP007J are required.

The resulting **single root-equivalent SAT** has 2187 primary variables, 553505 total including independent sequential counters, and 1896555 clauses; its new high-slice cardinality counter has 60965 variables and 121202 clauses. A local complete DIMACS file of ~38 MB was generated and SHA256 was
`c45a3e74e885b070ab0bc7a4a0d71cdc976dd1c17b442bfd7fedca665e9e37be`.
SAT/UNSAT is UNKNOWN. A SAT solution still requires an independent full F3^7 witness verifier; UNSAT requires an independently checked DRAT/LRAT/FRAT-equivalent certificate.

Since a dense H is now distinguished, its normalizing stabilizer on the frame is S7, *not* the entire S8. Nine-point orbit tags are `(lambda_e7, count_7(lambda=0),count_7(lambda=1),count_7(lambda=2))`. Exhaustive 2187-point enumeration gives 36 S7 orbits, of which four are basis/secants, leaving **32 valid branch types** of total 2151. This is a different, no-loss optional branch cover for the moment-anchored model. Do **not** use the earlier 13 S8 cases together with a *fixed* H: S8 permutations moving e7 need not preserve H. This subtle point is an important proof soundness gate.

## Controls and actual executed evidence

- Independent current-run Python stdlib enumeration: 15 S8 types -> 13 selected cases, 2151 ninth candidates; 1211 stabilizer contingency-table tenth classes; 32 S7 types after sound dense-H anchoring; exact all classes and multinomial sizes.
- Exact group action test: all 8!=40320 permutations on each of 13 ninth representatives, agreeing with the 13 orbit sizes.
- Exhaustive small n=2 positive-control: every 4-point cap normalizes to canonical frame plus the unique permitted fourth-point orbit; initial empty second-level orbit condition detected during testing, then fixed with `max(...,default=0)`.
- Complete 237-target first-branch DIMACS generated locally, 492540 vars and 1775362 clauses; SHA256 `8d23ac06842a0fbdafab8aef244e54dd819770578c2c8023b04e565a330e19e9`.
- Complete 237-target moment-anchored DIMACS generated locally, 553505 vars and 1896555 clauses; SHA256 above.
- Existing known 236-point fixture and exact 7D cap verification integrated into repository unit tests; this fixture test was unavailable in scratch and must pass in GitHub CI. No paid/GPU compute. No SAT solver was executed. No numerical r3(7) bound improved.

Reproduce:
```bash
python research/capset_f3_7/cap040_root_orbits.py --out-json /tmp/CAP040_ROOT_BRANCHES.json
python research/capset_f3_7/cap040_root_orbits.py --branch 0 --cnf /tmp/CAP040_B0_237.cnf
python research/capset_f3_7/cap040_hyperplane_anchor.py --cnf /tmp/CAP040H_237_GE89.cnf
sha256sum /tmp/CAP040_B0_237.cnf /tmp/CAP040H_237_GE89.cnf
python -m unittest discover -s research/capset_f3_7 -p 'test_cap040*.py' -v
```

## Meta-audit and branch selection

This is the first **explicit root-complete proof DAG** in this project's current workflow: every subtask has a formal implication to the exact goal. However, symmetry alone does not make UNSAT easy: each CNF has ~1.8–1.9M clauses, and decomposing into 13 or 32 cases may make total proof search *harder*. No GPU/paid budget is authorized; avoid launching large unexplained sweeps.

Next P0 experiment: (1) audit full CNF counters and branch unit clauses against independent checker (2) bounded CPU proof-producing SAT pilot on moment-anchored instance and one of the 13 branches, with honest UNKNOWN on timeout (3) compare solver propagation with and without sound hyperplane anchor under identical constraints (4) if intractable, derive stronger truly universal cross-hyperplane lemmas rather than reverting to fixed 285-occupancy enumeration.

Proof readiness checklist for every leaf: `parent_goal`, `coverage_lemma`, `SAT instance/sha256`, `solver result`, `independent proof hash/checker`, `bridge to root`, `status`. All leaf SAT statuses currently UNKNOWN. For construction, even one independently verified >=237 cap is meaningful disproof of the equality 236 but not a solved exact maximum.

## Latest sources and novelty boundary

- CAP007J (CI-GREEN): exact >=89 hyperplane lemma: `CAP007J_HYPERPLANE_THIRD_MOMENT_89_GATE_2026-11-02.md`.
- Thackeray, arXiv:2206.09804 (2022 preprint), proves 110-cap 6D completion and claims no 289-cap 7D; computational classification dependency must be independently assessed: https://arxiv.org/abs/2206.09804.
- 2026-10-03 status page: https://cairn-commons.com/problems/cap-sets-dim-7 publicly lists 236<=r3(7)<=291 with a preprint claim <=288.
- CAP019 provisional <=287 is independent of CAP040 and remains mathematically unreviewed; do not promote it to verified.

**The whole objective is still OPEN.** Neither an >=237 witness nor proof of no 237 has appeared. Affine-frame symmetry normalization is standard; novelty is not established. CAP040's main contribution is a reproducible, logically closed research architecture replacing disconnected local experiments with global proof obligations.
