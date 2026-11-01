# CAP-004C — Exact optimum 236 under the index-two order-120 subgroup (2026-11-01 UTC)

**Status:** VERIFIED LOCAL COMPUTATION; CI status must be checked separately. **Scope:** only caps invariant under the specified order-120 group. **Not** a global upper bound on r_3(7), and **not** a 237-point construction.

## Context and hypothesis

Previous CAP-004B showed that full 240-element signed-permutation symmetry in the reconstructed six-dimensional Paley magic basis forces a seven-dimensional cap of size at most 225. Test whether the canonical index-two subgroup restores the classical 236-point construction, and rigorously determine the optimum in that larger invariant family.

Start with the independently checked 112-point six-dimensional cap H from the Bierbrauer–Edel / Calderbank–Fishburn 236 construction, transformed by the six-normal basis in `paley_magic_basis_240_certificate.py`. Let G be its 240 signed-coordinate permutations. Each g=(P,mask) has parity(P)=popcount(mask) mod 2. Therefore the kernel G_even={g: parity(P)=0} has exactly 120 elements and is a subgroup.

## Exact finite enumeration

- The order-120 action on F_3^6 has **21 orbits**, sizes in script output.
- Its 6D within-slice cap constraints collapse to **780** orbit-index triple classes; the cross-slice constraints collapse to **4,089** ordered classes.
- Recursive exact orbit-subset enumeration leaves **174** valid single-slice masks. The maximum weight of such a slice is **112**.
- For each pair of valid slice masks, the forced third-slice cross-sum shadow is an orbit union. A 2^21-entry subset-max DP finds the largest cap-valid third-slice mask outside that shadow.
- There are 174*175/2 = **15,225** unordered slice pairs. A safe bound (each third slice <=112) permits skipping pairs incapable of improving the incumbent; **7,598** pairs were evaluated explicitly. This pruning is mathematically exact, not a heuristic timeout.
- **Restricted optimum = 236**, achieved by slice sizes **112+112+12** and deterministic orbit masks **(462848,344128,1048576)** in the script's lexicographic orbit ordering.
- The resulting explicit 236-point set was reconstructed from the orbit masks and passed an **independent coordinate-level mod-3 triple checker**, distinct from orbit constraints.

This proves that breaking the full 240 symmetry to its even-permutation order-120 subgroup recovers 236, but cannot produce 237 **while preserving that subgroup**. The same number as the classical record is not evidence for global optimality.

## Reproduction

```bash
python research/capset_f3_7/c6_even120_invariant_exact_optimum.py
```

No GPU, paid compute, random seed, or MILP is required. Independent scratch reimplementation in local CPU environment: approximately 3.6 seconds, output 21 orbits, 174 valid masks, optimum 236, direct triple checker PASS. The durable GitHub script is run by the branch-specific CI workflow; check its latest run for green status.

## Meta-audit / decision

CAP-004B (full 240) yielded 225; CAP-004C (index-two 120) yields 236. Hence reducing symmetry matters sharply, but the next target >=237 must break **this particular 120-element subgroup too**, or use a construction outside this coordinate template. Do not extrapolate to arbitrary index-two subgroups without proving classification. Next investigate proper subgroups of 120 (e.g. 60/40/24), with orbit counts and an explicit complexity gate, or controlled 27-block affine twists. Avoid rerunning already excluded full-240 and even-120 orbit unions.

## Source/novelty

As of 2026-11-01, accessible literature index still reports the exact seven-dimensional value open, 236 <= r_3(7) <= 291; Henry R. Thackeray's arXiv:2206.09804 abstract states there are no 289-caps, suggesting 288 conditional on accepting that preprint's proof. This restricted theorem's originality relative to all published work has **not** been established; classify as a new verified computational observation within this project only.

Primary checks: https://arxiv.org/abs/2206.09804 and https://repository.tudelft.nl/record/uuid:6818b21f-038d-4700-afcd-e6dac79e7e82
