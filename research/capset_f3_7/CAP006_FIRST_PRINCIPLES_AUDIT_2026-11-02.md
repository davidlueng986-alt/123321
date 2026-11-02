# CAP-006A — First-principles strategic audit and affine-partition falsification (2026-11-02)

## Status and guardrails

Research objective remains **exact** r_3(7), not merely a 237-point improvement. Checked branch STATE/LOG/BACKLOG and Drive ledger; CAP-005L is CI-GREEN, while CAP-005M remained CI-IN-PROGRESS at the time of this audit. This document makes no claim of a 237-point witness or new global upper bound. All quantities below concern the fixed, independently checked 236-point baseline.

## Premature assumptions to reject

1. **Local rigidity is evidence of global optimality.** False inference. A proof that no edit of <=6 fibers improves a particular cap says nothing about arbitrary caps outside that neighborhood. The fraction of excluded subsets among C(27,k) is a metric of *local coverage*, not probability that 236 is globally maximal.
2. **The first-three-coordinate partition is representative.** Falsified by the projection census below. Affine automorphisms of the fixed cap need not act transitively on all rank-3 quotient maps.
3. **More symmetric constraints alone will reach r_3(7).** Not justified. Order-24 invariant optimum 236 and even complete k7 local exclusion would still have no globally exhaustive bridge.
4. **Independent CI means independent mathematical review.** Not necessarily. Algorithmically independent checkers are valuable; shared assumptions about search family, orbit completeness and certificate semantics still require adversarial and metamorphic tests.
5. **A high number N(T) of separately admissible outsiders predicts a candidate cap.** No: compatibility constraints and loss of baseline occupancy remain. 198 outsiders in CAP-005J is a necessary-only quantity.
6. **A solver 'infeasible' is a theorem.** Only exact independently verified duals, exhaustive finite enumerations with trusted reductions or proof-logged SAT/ILP certificates qualify.
7. **A successful restricted result is new in the literature.** Novelty remains unverified; avoid claiming priority.

## New bounded CPU-only falsification: rank-3 linear projections

For each full rank P:F_3^7 -> F_3^3, let c_u=|B cap P^{-1}(u)| and Q(P)=sum_u c_u^2. Every fiber has dimension 4. This Q measures **baseline occupancy concentration**, not the likelihood of a new cap or an upper-bound certificate.

After an independent direct mod-3 cap test (236 distinct points, zero collinear triples):

- All C(7,3)=35 coordinate projections: exactly TWO sorted occupancy profiles, 15 maps containing coordinate 0 with Q=2884 and four empty fibers; 20 maps excluding coordinate 0 with Q=2290 and no empty fibers.
- The previously fixed first-three projection (coordinates 0,1,2) belongs to the concentrated Q=2884 class; it is **not representative** even of coordinate projections.
- Deterministic xorshift32 pseudorandom sample of 512 distinct full-rank 3x7 maps, seed=20261102: Q min=2096, lower median=2234, max=3186; zero-fiber range 0..3; two sampled maps satisfy Q>=2884.
- Example sample with Q=3186, 3 empty fibers and maximum occupancy 18: rows 1221212 / 1001110 / 0002220. Example with Q=2096, no empty fibers and maximum occupancy 12: 0002112 / 2012111 / 1101000.
- This is not a published new theorem: it is a reproducible finite observation about a known cap. It **falsifies** the working assumption that a single fixed rank-3 quotient captures typical local geometry.

Reproduce (Python stdlib, deterministic, CPU-only, no GPU or external service):

```bash
python research/capset_f3_7/cap006_projection_audit.py --out /tmp/cap006_projection.json
python -m unittest discover -s research/capset_f3_7 -p 'test_cap006_projection_audit.py' -v
```

CI status is pending until the dedicated branch workflow completes; do not promote as CI-GREEN prematurely.

## Source-oriented comparison

- Romera-Paredes et al., Nature 2024 and DeepMind FunSearch official repo: search for functions generating cap sets; 512 in dimension 8 is distinct from 237 in dimension 7. https://github.com/google-deepmind/funsearch
- Zhai et al. X-evolve, arXiv:2508.07932 (2025): evolve parameterized solution spaces, report asymptotic cap-set constant >=2.2203; not an exact n=7 solution. https://arxiv.org/abs/2508.07932
- Thackeray arXiv:2206.09804 reports no 289-point 7-caps (thus <=288 conditional on the proof), not independently proof-audited here. https://arxiv.org/abs/2206.09804
- Grace–Voloch, Algebraic Capsets (2026), DOI 10.1002/jcd.70024: algebraic extension-field construction and completeness. It does not establish exact r3(7).
- Public status page (dated 2026-10-03) gives published 236<=r3(7)<=291; preprint claim <=288 not to be presented as peer-reviewed or independently proven in this project. https://cairn-commons.com/problems/cap-sets-dim-7

## Research hypotheses and falsification tests

H1 [P0] **Partition-adaptive multi-fiber search.** The global choice of linear quotient P is a search variable, not a constant. Benchmark at least three inequivalent occupancy profiles (Q=2096, 2884, 3186) with the SAME exact candidate generator, fixed CPU budget and seeds. Score (i) certified 237 witness, (ii) number of independent feasible >236 candidates, (iii) exact restricted bound achieved, NOT raw N(T).

H2 [P0] **Globally exhaustive 6D-slice formulations.** Represent an arbitrary cap as A_0,A_1,A_2 subsets of F3^6, each a cap, and impose all cross-slice zero-sum exclusions. Crucial: permit *all* slice profiles totaling s, not just 112+112+12. Develop valid lower dimension cuts and proof-logged SAT/ILP. Start with n=4/5/6 as controls; ensure global optimality before attempting n=7.

H3 [P1] **New generators / solution-space evolution.** Adapt FunSearch/X-evolve style priority and parametric support-pattern programs to F3^7, independent of existing 236 fixture. For any size>=237 use a separate mod-3 arithmetic checker and file a complete witness.

H4 [P1] **Global moment / Fourier / SDP bounds.** Parseval holds for every set and is NOT a cap-specific upper bound; add genuinely cap-specific triangle-free constraints, slice interactions, and validate exact rational or proof-logged SDP/LP duals; benchmark on known r3(5)=45 and r3(6)=112.

H5 [P1] **Adversarial proof auditing.** Perform metamorphic tests under random affine transforms (all sizes and third-point relations preserved), inject negative examples into checkers, run independent third implementation on witness/certificates and test orbit-family coverage rather than only arithmetic.

H6 [P2] **Explore other 236 or smaller independent construction families.** Determine affine inequivalence before comparing, and avoid assuming the classical 236 point is the only local basin.

## Strategy change (proposal)

For the next ~4 bounded cycles allocate 35% to truly nonlocal lower-bound construction, 35% to global certified upper-bound formulation/benchmarking, 20% to independent checker/certificate audit, <=10% to continuing original fixed-coordinate k7 exclusions. Explicit reassessment after four cycles. These are suggested priorities, not measured success probabilities.

## Scientific interpretation

Current restricted results are real and useful if their certificates replay, but the bottleneck is *coverage of the global configuration space*. The campaign must maintain two separate ledgers: globally meaningful bounds and restricted lemmas. The exact problem remains OPEN; no >=237 cap or stronger global certified upper bound is claimed.
