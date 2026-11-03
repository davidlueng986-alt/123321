# CAP-041 — Root-equivalent dense-H SAT presolve, branch H00 (2026-11-03)

**Objective:** directly accelerate one **globally covering proof leaf** of the CAP040 exact r3(7) decision tree. This is NOT another fixed 236-witness neighborhood or fixed-285 occupancy search. It supplies no 237 cap, UNSAT certificate or improved numerical upper bound. All computations CPU-only, standard library, no GPU or paid compute.

## Parent goal and bridge

A 237-point cap can be normalized to a high-density hyperplane H (>=89 selected points) containing seven selected affine frame vertices and one further selected point of one of 10 complete S7 types, with the eighth frame vertex outside H; see CAP040_ROOT_FIRST_PROOF_DAG_2026-11-03.md and CAP007J's exact-moment theorem. The root proof is UNSAT for **ALL TEN** H branches; each H leaf is a complete global 237-point SAT instance under sound normalization. CAP041 presolves the first leaf (H00, ninth point 1222220) by *literal substitution*, without excluding any possible solution in that leaf.

## Exact substitution lemma

Let S be nine selected points, Z={-s-t:s,t in S,s!=t} their forced nonselected secant third-points. Direct F3 arithmetic finds |S|=9 and |Z|=36 for H00; S∩Z=∅. The remaining F3^7 points form U of size 2142. The dense H={x7=0} contains eight selected S points and 28 forced Z points, so U∩H has 693 points.

Each affine 3AP line meets Z, S, U in exactly one of three relevant patterns:

* Contains Z: its negative 3AP clause is automatically true, discard.
* Contains one S and two U: replace forbidden triple by a **binary** negative clause on U.
* Contains no S and no Z: retain the **ternary** negative clause on U.

A line with two S always contains a point of Z, by the definition of Z. Direct exhaustive enumeration of **all 796797 affine lines** yields:
- Dropped by forced-zero Z: 38718.
- Binary clauses from one selected point: 9513.
- Ternary clauses among free U points: 748566.

Any cap satisfying original units S=true, Z=false corresponds uniquely to a solution of these reduced 3AP constraints. Since |S|=9, root target |A|>=237 becomes |A∩U|>=228. Since |S∩H|=8, dense-H target |A∩H|>=89 becomes |A∩U∩H|>=81. Both are exactly encoded by standard implication-only sequential at-least counters, whose equisatisfiability has been independently small-truth-table verified.

**Thus CAP041 H00 SAT iff CAP040H H00 SAT.** This is a true root-preserving reduction, not a heuristic.

## Measured CPU result, branch H00 only

| Metric | CAP040H unbranched | CAP041 compressed H00 |
|---|---:|---:|
| Total variables incl counters | 553505 | **517533** |
| Total CNF clauses | 1896555 | **1786028** |
| Original point variables | 2187 | **2142** |
| Dense-H point variables | 729 | **693** |
| General at-least counter auxiliary | 490353 | **462498** |
| Dense-H at-least counter auxiliary | 60965 | **52893** |

The uncompressed same-H00 branch adds 9 unit clauses to the displayed unbranched baseline, so the exact clauses saved relative to its branch-equivalent original model are **110536**. Compared with the original 553505 total vars, **35972** variables are removed (~6.5%).

Actual local bounded execution: generated **full branch H00 DIMACS and 2142-entry free-ID→original-point mapping**, SHA256 `b59faca48cdd649e1574c06f36dd1ff2dab982cdac05b22b8d306e0f76b276c4`. Full DIMACS roughly 36 MB; reproducible from GitHub source, local only (not claimed uploaded to Drive/GitHub). No SAT solver was executed; SAT status remains UNKNOWN. The model can be used with an independent proof-logging solver. SAT witness must be mapped back through `.mapping.json` and independently checked in F3^7; UNSAT requires an independently checked proof artifact.

## Evidence, failure, reproduction

Initial all-ten Python census pilot redundantly recomputed 2.39M point pairs for every branch, reached only eight branches before a strict 45s local CPU limit; **INCOMPLETE**, not a 10-way verified result. Replaced by bounded complete one-branch generator and a first/exceptional branch configure regression. No speculative result for the other 9 cases.

```bash
python research/capset_f3_7/cap041_root_presolve.py --branch 0 --out /tmp/CAP041_H00.cnf
sha256sum /tmp/CAP041_H00.cnf
python -m unittest discover -s research/capset_f3_7 -p 'test_cap041_root_presolve.py' -v
```

Source: cap041_root_presolve.py, test_cap041_root_presolve.py. The latter checks exact line counts, SHA-pinned FULL DIMACS, the free-ID mapping, and exceptional branch H09's one overlapping secant-forced zero. CI must pass on exact commit before promotion. All H leaves remain SAT/UNSAT UNKNOWN.

## Next attack on actual theorem

Run matched small CPU budget, proof-logged SAT on H00 compressed vs uncompressed with independent proof/witness checker. If solver remains UNKNOWN, measure propagation and derive universal compatibility cuts reducing the ten root branches. Do not start indefinite fixed285 count-only/prefix certificate experiments merely to increase experiment IDs. Keep separate nonlinear construction branch to disprove r3(7)=236; a 237-witness would not settle the exact maximum.

Literature novelty of this standard literal-substitution encoding is not established; external proof of a global <=287 bound from CAP019 remains provisional.
