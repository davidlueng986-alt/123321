# CAP-004E — Exact order-24 high-slice restricted optimum 236
**Date:** 2026-11-01 UTC. **Status:** exact CPU enumeration, local scratch independently checked; GitHub Actions CI must be confirmed separately. **Global problem r3(7): OPEN.**

## Precise theorem (restricted)
Let `K` be the explicit order-24 subgroup constructed in `c6_subgroup_lattice_certificate.py`, acting on the last six coordinates of `F3^7` and fixing the first coordinate. Consider `K`-invariant cap sets `A` such that at least **two** of their three parallel 6D slices have size **>=104**. Then

`|A| <= 236`,

and equality is attained by an explicit `112+112+12` cap verified by direct mod-3 arithmetic. This does NOT determine the maximum over all `K`-invariant caps, nor any unrestricted bound on `r3(7)`.

## Exhaustive proof by orbit masks
The 24-group has 45 orbits on 729 points of `F3^6`, with orbit-size histogram `1:1, 6:4, 8:4, 12:16, 24:20`. Enumerate all ordered distinct tail pairs `a,b`; their third line point is `c=-a-b` mod 3. Compress the within-slice forbidden triples to **3,556** distinct orbit bitmasks. Twelve individual orbits contain a line and are forbidden outright.

A complete recursive include/exclude search on the remaining 33 orbit variables (checking every newly completed forbidden mask) visits **87,862** recursion nodes and produces exactly **11,434** internally cap-valid orbit unions. Maximum slice weight is 112. Of these, **48** have weight 112 and **96** have weight 104; there are exactly **144** valid slices of weight >=104.

For each unordered pair of the 144 high-slice masks, compute the exact cross-slice forbidden orbit shadow from `a+b+c=0`. The third slice is the highest-weight of the 11,434 cap-valid masks disjoint from the forbidden shadow. Exhaustive **144*145/2 = 10,440** unordered pairs give maximum total **236**, with maximum third-slice size **16** among tested pairs. The maximizing pair has slice sizes 112,112,12; its 236-point witness passes the separate `verify_capset.verify` direct 7D arithmetic checker (all 27,730 unordered pairs). The equality construction is known, not a new record.

This is a complete finite proof for the stated **two slices >=104** family: permuting the three first-coordinate values covers any choice of two high slices, and the cross-shadow enumerates every possible third-slice orbit union.

## Reproduction
```bash
python research/capset_f3_7/c6_subgroup_lattice_certificate.py
python research/capset_f3_7/c6_order24_high_slice_exact.py
```
Pure Python stdlib, deterministic, no seed, no GPU, no external solver. Local independent scratch run: `/mnt/data/capset_order24_highpairs.py` (transient, ~15–17 seconds CPU). Durable repository script and CI workflow above are authoritative.

## Meta-audit and next decision
The raw `2^45` orbit-mask state space was a misleading complexity proxy: the within-slice conflict hypergraph reduces it to 11,434 valid masks quickly. However a full unrestricted pair search has `11,434*11,435/2 = 65,366,? ` unordered pairs; many cannot reach 237 even with 112 in the third slice. A simple necessary score filter leaves ~54 million **ordered** pairs, still too expensive for naive Python cross-shadow + full mask scans. Next: use pair weight bounds, shadow memoization, orbit incidence bitsets, symmetry equivalence and exact branch-and-bound to attack all order-24 pairs; or switch to non-invariant 27-block twists. Do not extrapolate the >=104 theorem to all 24-invariant caps.

No >=237 witness; no global upper-bound improvement; novelty relative to all external literature unverified. As of 2026-11-01, public status remains open (236 lower, published 291 upper; Thackeray preprint states no 289-caps): https://cairn-commons.com/problems/cap-sets-dim-7 ; https://arxiv.org/abs/2206.09804 .
