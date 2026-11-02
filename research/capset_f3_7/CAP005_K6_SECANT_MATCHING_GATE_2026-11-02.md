# CAP-005D — Six-fiber secant-matching necessary gate (2026-11-02)

## Scope and theorem
Continue from CAP-005C (all five fixed first-three-coordinate F3^4 fibers excluded by exact rational duals, CI 41365141220). Let B be the independently verified known 236-point cap in F3^7. Partition the space into 27 fibers by the first three coordinates. Fix any six fibers T and freeze every B-point outside T. The following is a **necessary-only** census for changes within T; it is not a full six-fiber no-improvement theorem and does not bound global r3(7).

For each outsider x in fiber f, a baseline secant a+b+x=0 either has both a,b in f or has endpoints in a distinct pair of fibers {g,h} with g+h=-f. As g ranges outside f, h=-f-g is a fixed-point-free involution; thus these nonlocal fiber pairs are disjoint (a matching). An outsider x is admissible after releasing T only if f in T and T intersects every active pair. This is an exact necessary condition for retaining all frozen baseline points. It is not sufficient to select several outsiders simultaneously.

The independently checked baseline has 1,951 outsiders and minimum 10 distinct original secants per outsider; those secants have pairwise disjoint original endpoints. Consequently any improvement that inserts at least one outsider must delete at least 10 original points, so a released T with fewer than 10 admissible outsiders cannot improve 236.

## Complete deterministic census (CPU only)
All C(27,6)=296,010 six-fiber release sets enumerated. Exactly 288,878 have <=9 admissible outsiders, hence are **rigorously excluded from improvement**. The remaining 7,132 (2.41%) are NOT resolved by this gate. Exactly 1,072 have >=20 admissible outsiders. The maximum is 92 admissible outsiders, attained by 16 release sets (listed in generated JSON artifact). These 92 are only individually admissible candidates, **not** a cap set, nor a 237 witness.

Histogram of distinct active nonlocal fiber pairs per outsider: {1:8, 2:16, 3:64, 4:142, 5:712, 6:297, 7:320, 8:8, 9:384}. The full 6-fiber histogram is in the CI JSON artifact. As regression, the k=5 histogram exactly reproduces CAP-005C's previous 80,730-set necessary gate. Every maximum group was independently replayed using the uncompressed original secant-edge masks, giving 92/92 agreement. The original 236 cap was checked by the direct arithmetic verifier. No randomness, GPU or paid compute. Local run about 11 seconds for the initial census; rerun exact timings depend on CPU.

Reproduce:
```
python research/capset_f3_7/cap005_k6_secant_matching_gate.py --out /tmp/cap005_k6_gate.json
python -m unittest discover -s research/capset_f3_7 -p 'test_cap005_k6_secant_matching_gate.py' -v
```

## Bounded non-certifying feasibility pilot
On three of the 16 maximum-92 groups — (0,1,3,5,8,18), (0,1,3,7,8,18), (9,10,12,14,17,18) — a separate SciPy/HiGHS MILP encoding of all 7D collinearity constraints with frozen points returned **infeasible** for target >=237, in ~0.025–0.035 seconds each locally (164 binary variables, 2,050 unique line constraints; 164 frozen original points). Command:
```
python research/capset_f3_7/cap005_k6_milp_pilot.py --time-limit 5
```
These solver statuses are **exploratory only**: no LRAT/DRAT, independently checked branch-and-bound proof, or exact dual certificate was produced. They cannot be cited as rigorous six-fiber exclusions. The LP relaxation on these samples was 82 variable points versus 72 original points released, so a simple LP dual does not certify them either. This falsifies the heuristic that a large secant-cover candidate count by itself predicts a 237 cap.

## Strategy audit
The 5-fiber barrier is genuinely structural but local. Extending the elementary gate to six fibers leaves 7,132 cases, and the largest necessary candidate count is highly misleading. Next: exploit 27-fiber symmetry to reduce these 7,132 cases, seek exact integer UNSAT certificates for representative 92-candidate groups, and explore nonlocal templates rather than assuming nearby edits reach the record. Independently pursue global upper-bound certificates. This branch does NOT establish literature novelty. No >=237 verified construction, no stronger global upper bound; r3(7) OPEN.

External source check 2026-11-02: https://cairn-commons.com/problems/cap-sets-dim-7 still lists 236 <= r3(7) <= 291; Thackeray arXiv:2206.09804 asserts absence of 289-point caps (preprint, not independently re-proved here); Grace–Voloch 2026 discusses algebraic complete capsets but does not settle n=7.
