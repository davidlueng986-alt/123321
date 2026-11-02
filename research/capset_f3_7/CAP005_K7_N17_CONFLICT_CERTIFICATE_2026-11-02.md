# CAP-005L — Exact conflict certificates exclude all N=17 seven-fiber neighborhoods (2026-11-02 UTC)

## Scope and antecedents

Continue from CAP-005K CI GREEN (run 41402684579, commit ed1fd72d1128bb4dd3595a6dfa454bd183ae2899). Fix the classical 236-point cap B and the 27 fibers indexed by the first three ternary coordinates. Allow changes to exactly seven of those fibers, fixing every original B point outside them. CAP-005J/005K verified 862,906 of 888,030 neighborhoods excluded by the <=16 individually admissible outsider gate; 25,124 survived, partitioned into 1,665 orbits under a verified 16-element affine stabilizer.

## Exact argument

For a seven-fiber neighborhood T, define E(T) as the outsiders whose every original-B secant has at least one endpoint in T. Any improved cap B' with B'\\B contained in T requires >=17 insertions (CAP-002A independent pair-removal barrier). If |E(T)|=17, all 17 outsiders must be inserted.

For every one of the 37 N(T)=17 symmetry-orbit representatives, a deterministic certificate exhibits either (i) distinct x,y in E(T) with -x-y in B outside T, or (ii) three distinct points x,y,z in E(T) with x+y+z=0 in F3^7. Thus all 17 outsiders cannot simultaneously be inserted, irrespective of deletions within T. The verified affine stabilizer transports each contradiction to its orbit. Orbit sizes: 35 of size 16, 2 of size 8, totaling 576 neighborhoods. This is a finite, exact, restricted obstruction, not a global cap-set upper bound.

New cumulative restricted exclusions: 862,906 + 576 = 863,482 / 888,030 (97.2357%); unresolved: 24,548 neighborhoods in 1,628 orbits. No >=237 cap, no global bound improvement.

## Independent reproducibility

Generator: `python research/capset_f3_7/cap005_l_k7_n17_generator.py /tmp/cap005_k7_symmetry.json --out /tmp/cap005_l_n17.json`.

Checker: `python research/capset_f3_7/cap005_l_k7_n17_check.py /tmp/cap005_l_n17.json /tmp/cap005_k7_symmetry.json`.

First regenerate and independently validate the prior input with `cap005_k7_symmetry_quotient.py` and `cap005_k7_symmetry_check.py`. The new checker independently re-derives all 236-point cap lines, outsider admissibility, all 37 witness relations, the 16-element fiber group and complete 576-orbit coverage; it does not import the generator. CI runs both and archives the exact JSON. CPU-only, deterministic, seed=null, no GPU or paid compute.

Independent JS cross-check performed before commit: enumerated all 2,946,160 seven-fiber outsider incidences, reproduced 576 N=17 neighborhoods / 37 orbits, and found a fixed-point pair or outsider triple conflict in all 37 representatives; 35 size-16 and 2 size-8 orbits. This preliminary computation is independent of the Python scripts; GitHub CI is still required for GREEN status.

## Meta-audit / next experiment

The seven-fiber local-search line can exclude neighborhoods but cannot certify global r3(7), even if completed. Next try N=18..24 representatives using matching/clique bounds, exact rational duals and deletion-cover certificates; cap CPU budgets. Reserve effort for nonlocal alternative partitions and certified global upper bounds. Novelty in literature unestablished; 2026-10-03 public tracker still lists 236 <= r3(7) <= 291, and Thackeray's 2022 arXiv:2206.09804 claims <=288 without independent project review. Do not claim exact r3(7).

## CI verification (2026-11-02 08:52 UTC)

GitHub Actions run https://github.com/davidlueng986-alt/123321/actions/runs/41415696843 completed **SUCCESS** at source commit 7f7a110768df27ccf76042c38317720b3c1421c6. Both generator and independent arithmetic checker passed for all 37 N=17 orbit representatives, covering 576 neighborhoods. Artifact (30-day retention): https://github.com/davidlueng986-alt/123321/actions/runs/41415696843/artifacts/13128405069. The claim remains restricted to the specified 236-point cap and seven-fiber modification family.
