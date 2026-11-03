# CAP-044 — Independent barycentric orbit regression (2026-11-03 UTC)

Scope: independent CPU-only recheck of CAP-040/043's H-preserving ninth-point quotient, prompted by root-proof completeness risk. This is a regression audit, **not** a new theorem, solver result, or global bound.

Independent implementation: enumerate F3^7 as Python itertools.product(range(3), repeat=7); frame F={0,e1,...,e7}; third(a,b)=(-a-b) mod 3; filter points p with p[6]=0 excluding frame and all 28 frame secant thirds. For each surviving p, compute affine barycentric coordinates (1-sum(p[:6]),p[:6]) mod 3. Sorting these seven entries gives the orbit invariant under permutation of H's seven frame vertices. The ten sorted tags have orbit sizes 105,35,140,210,21,42,105,1,35,7 (lexicographic tag order), summing to 701. Recompute the nine-selected-point secant-third distinct counts for one representative per tag: nine classes have 36, one has 35. Exact assertions passed locally with Python 3, deterministic, no random seed, GPU, paid compute, or SAT solver.

Reproduction: run the following standalone Python code:

```python
from itertools import product
from collections import Counter
v=list(product(range(3),repeat=7)); z=(0,)*7
F=[z]+[tuple(int(i==j) for i in range(7)) for j in range(7)]
third=lambda a,b:tuple((-x-y)%3 for x,y in zip(a,b))
forbidden=set(F)|{third(a,b) for i,a in enumerate(F) for b in F[i+1:]}
H=[p for p in v if p[6]==0 and p not in forbidden]
classes={}
for p in H:
    key=tuple(sorted(((1-sum(p[:6]))%3,)+p[:6]))
    classes.setdefault(key,[]).append(p)
counts=Counter(len({third(a,b) for i,a in enumerate(F+[ps[0]]) for b in (F+[ps[0]])[i+1:]}) for ps in classes.values())
assert len(H)==701 and len(classes)==10
assert sorted(map(len,classes.values()))==[1,7,21,35,35,42,105,105,140,210]
assert counts==Counter({36:9,35:1})
print('CAP044 PASS',len(H),counts)
```

CAP-043 exact commit 145da5f571898459c3c700446de28ae3a8b9f1b8 CI run 41631698651 was checked SUCCESS on 2026-11-03. New unrelated closure-batch commits coexist on this branch; do not mistake closure-batch CI for Cap Set CI. This check supports orbit bookkeeping only, not exhaustiveness of all global 237-cap proof leaves without CAP-040 dense-H premise. All ten SAT statuses remain UNKNOWN. Strategy: stop further census repeats; next run must prioritize proof-logged bounded CPU SAT or an independently reviewed global lemma. Exact r3(7) OPEN.
