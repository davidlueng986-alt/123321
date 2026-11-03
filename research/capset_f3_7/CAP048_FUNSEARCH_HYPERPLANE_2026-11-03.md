# CAP048 — Independent nonlocal 237 construction attempt: FunSearch 8D→7D hyperplanes

2026-11-03 UTC. Goal: seek >=237-point cap in F3^7 by restricting an existing 8D cap to a suitable 7D affine hyperplane. This is a constructive disproof attempt (a 237 witness would refute `r3(7)=236` but not close exact maximum). **Outcome: negative for THIS source and operation only; root remains OPEN**.

## Input construction, provenance and independent arithmetic

Reimplemented the priority-based greedy cap constructor from the publicly released Google DeepMind FunSearch `cap_set.ipynb` notebook (https://github.com/google-deepmind/funsearch/blob/main/cap_set/cap_set.ipynb). Recreated 512 DISTINCT points in F3^8, verified with independent direct mod-3 arithmetic that none of 512 choose 2 = 130816 pairs has its third collinear point in the set. This agrees with FunSearch's known 512-point n=8 construction; no novelty claimed. Code and full 512-point source witness are included in this artifact.

## Exhaustive dimension-7 hyperplane-slice census

All 3^8−1=6560 nonzero F3^8 normals modulo sign yield 3280 projective normal classes. For every class, computed all three affine levels (0,1,2), each a 7D affine flat. Every subset of an 8D cap is a cap in that flat. All 3280*3=9840 7D hyperplane slices were checked exactly with ternary dot products. Their maximum cardinality is **208**, reached for exactly 8 projective orientations (16 affine hyperplanes due two tied levels each). Representative normal (1,0,0,0,1,1,0,0) has sizes (96,208,208). Histogram of the maximum of three sizes in each normal direction:

`{171:384,172:448,174:256,176:912,178:64,180:288,182:256,184:288,188:192,190:64,192:32,196:16,200:24,202:32,204:16,208:8}`

Sum histogram entries = 3280. Thus **this particular FunSearch 512-cap has no affine 7D section of size >=237**. This is an exact finite, reproducible rejection of a plausible **nonlocal construction mechanism**, but not a global upper bound and not a proof that other 8D caps cannot yield >=237 slices. A source with >=711 points in 8D would guarantee by averaging an affine hyperplane of >=237 points, but 512 is far below that necessary mean threshold; conversely an 8D cap with <711 could still have such a large slice if imbalanced.

## Reproduce

```
python cap048_funsearch_512_7d_probe.py
```

Requires numpy, CPU only. The program rebuilds all 512 points by priority-greedy, checks every 8D 3AP pair, enumerates all 3280 projective normals and each ternary affine level, asserts counts. Pseudorandom seed: none. Runtime bounded seconds. No GPU or paid compute.

Evidence: `cap048_funsearch_512_7d_probe.py`, `FUNSEARCH_512_SOURCE_POINTS.txt`, `funsearch_512_7d_probe.log` and spectral CAP047 bundle. No SAT/UNSAT certificate of the full n7 existence problem; the exact r3(7) problem remains OPEN. **Strategy stop:** don't repeat this input and mere hyperplane restriction; pivot only to a genuinely new n7 constructive family or global proof-logged target-237 SAT.