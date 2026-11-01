# CAP-004F — Exact SAT/CNF reduction for the entire order-24-invariant family
**Date:** 2026-11-01 UTC. **Scope:** restricted to the explicit order-24 subgroup in CAP-004D. **Status:** encoding committed; CI verification pending at creation. This is NOT a proof of UNSAT or an upper bound.

## Mathematical equivalence
For each of the 45 orbits O_i on F3^6 and each first-coordinate slice s in F3, introduce x_(s,i) ∈ {0,1}. A 24-invariant cap A corresponds bijectively to the union of chosen slice-orbits. Every affine line in F3^7 either lies within one slice or meets all three slices once. Enumerate within-slice forbidden sets of orbit indices {i,j,k} for distinct a,b,c with a+b+c=0, and cross-slice ordered orbit triples (i,j,k) for arbitrary tails a,b,c with a+b+c=0. Forbid all chosen triples using clauses (¬x_(s,i)∨¬x_(s,j)∨¬x_(s,k)) with duplicate literals removed, and (¬x_(0,i)∨¬x_(1,j)∨¬x_(2,k)). Thus the structural clauses hold iff the selected union is a cap.

Weighted cardinality is Σ_(s,i) |O_i| x_(s,i) ≥ 237. The exact Tseitin recurrence P_(i,t) ↔ P_(i−1,t) ∨ (x_i ∧ P_(i−1,t−|O_i|)), with P_(0,0)=true, P_(0,t>0)=false, gives an equisatisfiable CNF. Unlike a bounded search over pairs, this model includes **all** 24-invariant three-slice configurations, without any high-slice assumption. SAT means a verifiable >=237 witness; UNSAT needs a separately checked proof (DRAT/LRAT), not merely solver exit status.

## Replay
```bash
python research/capset_f3_7/c6_order24_sat_encoding.py --target 236
python research/capset_f3_7/c6_order24_sat_encoding.py --target 237 --out /tmp/capset_order24_target237.cnf
```
The 236-point order-120-invariant witness is also order-24-invariant. The script independently reconstructs and checks its 236 distinct 7D points using direct mod-3 arithmetic, checks all structural CNF clauses, verifies full satisfaction of the 236-target encoding and that exactly the objective clause fails for the 237-target encoding. These tests validate a known model, **not** completeness of an UNSAT search. No random seed, GPU or paid compute.

## Decision / meta-audit
The 65,373,895-pair direct enumeration can be replaced by a compact orbit SAT instance with 135 primary variables plus deterministic threshold auxiliaries. Next inspect variable/constraint counts and run a bounded CPU SAT feasibility test if an available solver supports verifiable certificates. If SAT, independently check the 7D point set; if UNSAT, obtain and replay a proof certificate before claiming a restricted upper bound. Keep non-invariant 27-block twists and global upper-bound work alive. External novelty not established; CNF reductions are standard.

## CI-confirmed results (2026-11-01 22:00 UTC)
- CI SUCCESS: https://github.com/davidlueng986-alt/123321/actions/runs/41354696903 (commit d4bcab974cd5703119c7671afe868ac202846863).
- 3,556 distinct within-slice forbidden orbit sets, 20,313 ordered cross-slice orbit triples, 30,981 structural clauses.
- Target 236: 30,121 variables, 148,549 clauses. Known 236 witness passes independent arithmetic checker and satisfies all clauses.
- Target 237: 30,241 variables (135 primary + 30,106 auxiliaries), 149,028 clauses. Known 236 witness violates ONLY the final objective clause, as expected. **SAT/UNSAT not decided.**
- Deterministic DIMACS SHA256: `322eba0828cbfdd9809074bf579d7fdae70b25695bdfef4592c76203f4eb34a6`.
- CI artifact (30-day retention): https://github.com/davidlueng986-alt/123321/actions/runs/41354696903/artifacts/13102867770 . Re-generate after expiration using the commands above.
- Fresh literature check (2026-11-01): Versluis (2017) reports 291; Thackeray (2022, arXiv:2206.09804) claims no 289-point 7D caps; Grace/Voloch (2026) discusses small complete caps, not a new 7D maximum. No novelty claim.
