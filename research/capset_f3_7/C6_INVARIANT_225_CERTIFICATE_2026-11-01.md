# CAP-004B — exact optimum in the 240-invariant C6 orbit family (2026-11-01 UTC)

**Status:** VERIFIED COMPUTATION on local independent Python arithmetic; GitHub Actions verification required for full branch-level CI status. **Not** a new global bound on r_3(7).

## The restricted theorem

Let H be the 112-point cap in F3^6 obtained from the 0-slice of the published Calderbank–Fishburn 236-cap, transformed by the six independently checked Paley magic-basis normals in `paley_magic_basis_240_certificate.py`. Let G be **all 240 signed coordinate permutations** preserving H. Act on F3^7 by fixing the first coordinate and applying G to the last six. Then the largest G-invariant cap in F3^7 has **exactly 225 points**.

This says nothing about general caps: the verified 236-point construction is not G-invariant in these coordinates. It is a finite structural obstruction, not a bound r_3(7)<=225.

## Exact finite proof/certificate

1. Enumerate all 6! 2^6 signed permutations and retain exactly the 240 preserving H. Their 13 orbits partition all 729 points of F3^6, with sizes [1,12,60,120,40,60,120,60,120,60,12,40,24].
2. Enumerate all 729^2 ordered pairs of 6D points, classify their third point `-x-y mod 3` by orbit. There are exactly **247** distinct unordered orbit-triples arising from nondegenerate within-slice lines, and **1,195** ordered orbit-triples arising from cross-slice lines. Within-slice lines require x!=y; cross-slice lines may use equal six-coordinate tails because their seven-dimensional prefix coordinates are distinct.
3. Enumerate every one of the 2^13 orbit subsets for a single affine slice. Exactly **22** are cap-compatible, with maximum slice size 112. Their cardinality histogram is: 0:1, 1:1, 12:2, 24:2, 40:2, 52:2, 60:2, 64:2, 72:4, 100:2, 112:2.
4. For every unordered pair of valid slice masks (**22*23/2=253**), calculate the exact forbidden orbit mask for the third slice by cross-slice addition. A subset-maximum dynamic program over all 2^13 masks chooses the largest valid third slice. Permuting the three prefix slice labels preserves cap-compatibility, so unordered pairs suffice. Exhaustive maximum **225**, achieved by slice cardinalities **112+112+1** and masks **(530,3200,1)** in the deterministic orbit order of the script.
5. Rebuild all 225 seven-dimensional points and run an independent direct exact all-pairs `(-x-y)%3` checker. PASS. The upper bound is a complete exhaustive integer enumeration over the defined G-invariant family, independent of MILP/SAT solver correctness.

## Reproduction

```bash
python research/capset_f3_7/c6_invariant_exact_optimum.py
```

No random seeds, no GPU, no external solver. Also independently implemented and executed a standalone version in the ephemeral local CPU runtime; both give 225 with the same 13 orbit sizes, 247/1195 line-orbit triple counts, 22 slice masks, 253 pair tests and 112+112+1 witness. GitHub branch file is the durable replay artifact.

## Strategy / novelty audit

The 112-cap, magic basis, order-240 subgroup and 225-point lift were already present in the project (and 225 is below the known 236 construction). The **restricted optimum** was not previously recorded in this branch; do not assert it is a new theorem in the wider literature without a dedicated equivalence and publication search. Contemporary sources still report 236<=r_3(7)<=291, with a preprint claim of 288 (not independently upgraded to a published global bound).

This refutes the strategy of searching for a 237-point cap **while retaining this entire 240-element symmetry group**. Next explore controlled symmetry-breaking (subgroups of index 2/3/5, or non-invariant 27-block twists) rather than simply increasing MILP timeouts. A future lower bound >=237 requires an independently checked explicit witness and a fresh literature comparison.

Sources:
- https://cairn-commons.com/problems/cap-sets-dim-7
- https://onlinelibrary.wiley.com/doi/10.1002/jcd.70024
- https://github.com/davidlueng986-alt/123321/blob/research/capset-f3-7/research/capset_f3_7/paley_magic_basis_240_certificate.py
