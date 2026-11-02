# CAP-005K — Exact symmetry quotient of seven-fiber necessary survivors (2026-11-02 UTC)

**Scope:** The same independently verified 236-point Calderbank–Fishburn/Edel cap and the same fixed 27 fibers indexed by the first three coordinates as CAP-005J. Only modifications to exactly seven fibers are considered. The result is **not** a global bound on r_3(7) and is not a >=237 construction.

## Result (bounded CPU computation)

CAP-005J independently proved that exactly 25,124 of the 888,030 seven-fiber release sets survive the necessary gate N(T)>=17. Four explicit affine automorphisms of the baseline (checked on all 236 points) induce a 16-element group G on the 27 fibers. Its action preserves the exact outsider secant requirements, hence N(gT)=N(T) for every g in G.

An exact orbit partition of those 25,124 survivors gives **1,665** symmetry classes, with orbit-size histogram:

| Orbit size | Number of orbits | Covered release sets |
|---:|---:|---:|
| 4 | 3 | 12 |
| 8 | 185 | 1,480 |
| 16 | 1,477 | 23,632 |
| **Total** | **1,665** | **25,124** |

The 8 maximum-N=198 release sets form exactly **one** orbit of size 8. At N=17 there are 37 orbits (576 sets). These are *necessary-only* survivors; high N does not imply compatible outsiders or a 237-point cap. Symmetry reduces the number of exact representative problems by 15.09x, without ruling out any additional cases by itself.

## Independent verification and commands

Generator: `cap005_k7_symmetry_quotient.py` uses the previously CI-verified outsider-incidence census (now optionally exposing its exact per-neighborhood counts), the verified affine stabilizer, and complete orbit partition. Independent checker: `cap005_k7_symmetry_check.py` does **not** use the incidence generator or its ranking; it reconstructs all F3 secants directly, checks N(T) for every one of the 1,665 representatives, checks all orbit disjointness and coverage, and validates baseline occupancy. CAP-005J's separate C++ direct all-888,030 census independently establishes the total of 25,124, so 25,124 distinct, individually admissible orbit members exhaust the survivors.

```bash
python research/capset_f3_7/cap005_k7_symmetry_quotient.py --out /tmp/cap005_k7_symmetry.json
python research/capset_f3_7/cap005_k7_symmetry_check.py /tmp/cap005_k7_symmetry.json
```

Deterministic CPU-only; no GPU, paid compute or random seed. JSON output records all 1,665 representatives, their exact N(T), orbit sizes and released-baseline occupancies. CI archives this output for reproducibility. This run's independent second implementation in JavaScript, operating on the 236-point fixture via the GitHub connector, separately obtained 1,665 orbits, histogram (4:3, 8:185, 16:1477), 25,124 covered sets and a single N=198 orbit. Do not call the new CI GREEN until the workflow has completed.

## Strategy meta-audit

The symmetry quotient is a 15x reduction, **not a cap-size improvement**. Target the 37 N=17 orbits first with exact fixed-point conflict/clique and deletion-cover inequalities; then use rational LP duals/odd-cycle cuts for moderate N. Large-N orbits (N=198) are not inherently promising because many outsiders can be mutually incompatible. Keep a parallel nonlocal construction and global upper-bound program: even excluding all seven-fiber edits around this one baseline would not solve r_3(7).

## Literature (rechecked 2026-11-02)

Cairn Commons status page (reviewed 2026-10-03) still lists the problem OPEN with 236 <= r3(7) <= 291; Thackeray's arXiv:2206.09804 preprint argues no 289-point cap (conditional upper bound 288; full proof not independently checked in this project). Grace–Voloch, *Algebraic Capsets*, Journal of Combinatorial Designs, first published 2026-05-21, develops algebraic constructions, not an established exact solution of r3(7). This restricted quotient's novelty in the wider literature remains unestablished.

**No >=237 witness. No new global upper bound. Exact r3(7) remains OPEN.**
