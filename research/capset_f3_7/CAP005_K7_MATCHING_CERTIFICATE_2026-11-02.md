# CAP-005M — Seven-fiber disjoint conflict matchings (2026-11-02)

## Exact restricted statement
For the fixed classical 236-point cap B in F3^7, with only seven of the 27 first-three-coordinate 4D fibers allowed to change, the CAP-005M independent JS pilot found 500 further symmetry orbits (7440 neighborhoods) that cannot improve B. **CI verification pending.** This is not a global upper bound or a new record.

## Proof principle
Let E(T) be all outsiders individually compatible with the original B points outside released fibers T. CAP-002B established that any improvement needs at least 17 outsider insertions. If x,y in E(T) and z=-x-y mod 3 is a fixed original point outside T, at most one of x,y may be inserted. A vertex-disjoint matching of m such conflicts forces at least m outsiders omitted; if m>=|E(T)|-16, no improvement is possible. All edges and disjointness are independently verified, not inferred from solver infeasibility.

## Experiment and audit
Reconstructed in JS the exact 2,946,160 outsider incidences, 862,906 elementary exclusions, and 1,665 orbits covering 25,124 survivors. Greedy matchings with five deterministic edge orders yielded 500 orbit certificates with 18<=N(T)<=32, excluding 7,440 neighborhoods disjoint from CAP-005L's 576 N17 exclusions. Expected totals: 870,922 / 888,030 excluded; 17,108 unresolved in 1,128 orbits. Python generator and independent checker are committed for GitHub CI. CPU only, no seed, GPU, or paid compute.

Reproduce:

```bash
python research/capset_f3_7/cap005_k7_symmetry_quotient.py --out /tmp/k7.json
python research/capset_f3_7/cap005_m_k7_matching_generator.py /tmp/k7.json --out /tmp/matching.json
python research/capset_f3_7/cap005_m_k7_matching_check.py /tmp/matching.json /tmp/k7.json
```

## Strategy meta-audit
Pair-conflicts with fixed original points alone cannot exclude every low-N neighborhood; N>32 is unexamined here. Future: outsider-triple/odd-cycle cuts, nonlocal constructions, and certified global bounds. Latest literature check (2026-11-02): Cairn Commons lists OPEN 236..291; Thackeray arXiv:2206.09804 claims <=288; Grace–Voloch 2026 does not claim exact r3(7). Novelty not established.
