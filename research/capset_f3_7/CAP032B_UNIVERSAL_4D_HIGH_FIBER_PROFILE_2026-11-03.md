# CAP-032B — Universal high-density AG(4,3) parallel-fiber profile certificate

**Date:** 2026-11-03 UTC. **Status:** independent pure-Python and C++17 local exhaustive computations PASS; GitHub CI verification to be checked on the final source commit. CPU-only, deterministic; no GPU or paid compute. **No new F3^7 cap of size >=237 or improved numerical global upper bound.**

## Unrestricted 4D structural theorem

Let C be ANY cap in F3^4, split by ANY nonzero linear functional into three parallel affine F3^3 slices C0,C1,C2. Then for prescribed sizes |C0|=a, |C1|=b (a,b in {6,7,8,9}), the following are the exact attainable maxima of |C2|:

| a | b | exact max | max individually available holes |
|---|---|---|---|
|6|6|8|9|
|6|7|6|7|
|6|8|6|7|
|6|9|3|4|
|7|7|4|6|
|7|8|3|4|
|7|9|2|2|
|8|8|2|3|
|8|9|2|2|
|9|9|2|2|

Particularly, **if two parallel 3D slices each contain at least seven points, the third has at most four**, i.e. (7,7,5) is impossible although 19 <= r3(4)=20. Since subsets of caps are caps, exact (7,7) excludes any (a>=7,b>=7,c>=5); analogous threshold implications apply to every row. Known 18-point cap with profile (7,7,4) in CAP028/CAP029 realizes sharpness.

## Full finite proof, with independent checkers

A 3D point is encoded by 0..26; a k-cap by a 27-bit mask. Two distinct points p,q forbid r=-p-q (mod3). Exhaustive counts of 3D caps:
- |A|=6: 107406, affine orbit sizes (6318,25272,75816).
- |A|=7: 126360, affine orbit sizes (50544,75816).
- |A|=8: 63180, affine orbit sizes (6318,18954,37908).
- |A|=9: 2106, affine orbit size 2106.

Orbit cover is checked through 12 explicit affine generators: 3 translations, two swaps, one sign and 6 shears, generating AGL(3,3). The generator code checks cap validity and each orbit's complete coverage.

For each first-slice orbit representative A and *every* second k-cap B, independently compute H = F3^3 \ (-(A+B)). The possible third slice must be a cap subset of H, and any such subset yields a valid 4D cap with A and B since the within-slice and cross-slice constraints are then both met. The independent C++17 checker enumerates all cap subsets of each H whose size could increase the current optimum; it reproduces all 10 exact maxima and witnesses of attainability.

Independent Python implementation separately enumerates ALL 252720 (representative 7-cap, arbitrary 7-cap) pairs. Hole-count histograms:
- first orbit size 50544: H=0:2916,1:15471,2:72036,3:29457,4:6399,5:81.
- second orbit size 75816: H=0:1728,1:18090,2:69471,3:31860,4:5103,5:81,6:27.

In the 189 cases with >=5 holes, exhaustive five-subset checks find **zero** five-point 3D caps. The existing verified CAP029 (7,7,4) witness is checked independently again. This proves exact optimum 4 for the 7+7 case.

Reproduce:
```bash
python -m unittest discover -s research/capset_f3_7 -p 'test_cap032b_universal_fiber_profiles.py' -v
python research/capset_f3_7/cap032b_universal_fiber_77.py
g++ -O3 -std=c++17 -Wall -Wextra -pedantic research/capset_f3_7/cap032b_universal_high_fiber.cpp -o /tmp/cap032b
/tmp/cap032b
python research/capset_f3_7/cap032b_4d_threshold_cuts.py
```

## Consequence for ALL 7D caps, and adversarial negative control

For any rank-4 quotient F3^7 -> F3^4 there are 81 parallel 3D fibers and 1080 quotient affine lines. Every genuine 7D cap must satisfy the threshold inequalities above on every quotient line. This is a **universal, redundant strengthening** over the local cardinality r3(4)=20, so it may help proof-logged shared-fiber SAT/CP solving but is NOT itself a new global numerical upper bound.

The independently checked CAP027 *formal 285-point occupancy* satisfies ALL 1080 such profile cuts, despite these cuts correctly rejecting an artificial (7,7,5) line. Thus the formal285 model still stands as a counterexample to count-only sufficiency. It is not a cap witness. We should prioritize two-or-more quotient lines sharing the SAME 3D fiber point assignments, and all nonradical directional constraints, rather than more single-line quota relaxations.

## Source/novelty boundary and research strategy

Bruen–Wehlau, *Caps and Colouring Steiner Triple Systems* (1998) already describes that any 20-cap in AG(4,3) has 3D parallel section sizes either {2,9,9} or {6,6,8}; Follett et al. (2014) studied partitions of AG(4,3) into maximal caps. These results are consistent with our table. Originality of the 19-point and smaller-profile refinements is **not established**. See https://mast.queensu.ca/~wehlau/published_versions/caps_sts.pdf and https://sites.lafayette.edu/mcmahone/files/2015/01/PartitionsAG43.pdf.

**Future P0:** (1) proof-logged point-level two-quotient-line SAT/PB, then all 1080 shared lines, optionally pinned to CAP027 occupancy for a *conditional* countermodel test; (2) hostile independent Thackeray 110-cap classification referee underpinning CAP019 provisional <=287; (3) maintain no-112-slice and independent >=237 construction branches. Do not solve the wrong restricted problem or promote any solver timeout to UNSAT. Exact r3(7) remains OPEN.
