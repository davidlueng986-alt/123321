# E067 — First-Principles Global Obstruction Audit for 3-MOLS(10)

**Executed:** 2026-11-05 23:10 UTC / 2026-11-06 07:10 HKT. **Global mathematical status: OPEN.**

**Only success criterion:** independently verified three 10×10 Latin squares with pairwise 100/100/100 ordered-pair overlays, or a complete unrestricted independently checked nonexistence proof. E067 does not meet either. The MOLS10 hourly automation remains disabled.

## Goal-backward finding: CPU is not the primary *diagnosed* bottleneck

E066's independently obtained 1,700-branch ledger has all 1,700 `UNKNOWN_BUDGET` after approximately **13,658.47 aggregate solver seconds** (~3.79 serial CPU-hours), zero SAT and zero checkable UNSAT proofs. It is wrong to assert that extra CPU alone will close these large searches; it is also wrong to assert that the known formulation can never close without a new theorem. The evidence supports a propagation / proof-search / domain-specific constraint bottleneck, without a credible quantitative ETA.

Published 2026 Barnoff–Bright hybrid SAT + Euler–Parker solver shows a large improvement on *two-square* order-10 constructions (some CaDiCaL cases failed within 7 days, with the hybrid median around 5,100s). This is NOT a reported result for 3-MOLS(10), but confirms that architecture can matter more than a modest CPU multiplier. Source: https://arxiv.org/abs/2605.02132 .

## 1. Five-net graph obstruction: global theorem, vacuous at E064 root

For an OA(100,5,10,2), regard its 100 distinct 5-tuples as vertices. Two distinct vertices are adjacent iff they share one of their five coordinates. They cannot share two coordinates by the OA condition. Every vertex has `5(10−1)=45` neighbors. Two adjacent vertices share `(10−2)+(5−1)(5−2)=20` common neighbors; two nonadjacent vertices share `5(5−1)=20`. Hence its symmetric collinearity adjacency matrix `A` satisfies the **exact integer identity**

`A² = 25 I + 20 J`,   `AJ = 45J`.

It follows that `A − (45/100)J` has spectrum `0` (all-ones) and `±5` (on the perpendicular space), so every principal submatrix of the centered matrix has spectral norm at most 5.

The normalized first row and first column already fix 19 physical 5-tuples. For each of all **1,700 E064 classes**, we assembled their 19×19 induced adjacency graph in two independently implemented ways: explicit five-coordinate comparisons and a combinatorial adjacency rule. Both agree for all cases, and all eigenvalues lie in `[-5,5]`, with no violations. An independent 25-point positive-control OA from GF(5) passes the general 5-net collinearity equation.

**A stronger negative insight: root-level spectral pruning is provably powerless, not merely empirically unsuccessful.** With the 19 fixed points ordered as origin, 9 other first-row points, and 9 other first-column points, the induced adjacency is

```
           [ 0      1^T       1^T ]
  A[S,S] = [ 1      J-I       D^T ]
           [ 1       D        J-I ]
```

where `D = I + P_f + P_g` is a **3-regular 9×9 bipartite incidence matrix**, since first-column permutations are distinct derangements. An eigenvector `[0, 1^9, −1^9]` has eigenvalue exactly `5` for the centered matrix, independently of `f,g`. On the 16-dimensional sum-zero subspace the eigenvalues are `−1 ± σ_j(D|_{1⊥})` and thus lie in `[-4,2]` since `||D||≤3`. The remaining 2D subspace has the two eigenvalues `(49±√13201)/40` ≈ `4.09739012`, `−1.64739012`. Thus, **every valid E064 first-column class automatically satisfies this bound**. No first-column branch can be excluded using only this 19-point spectral inequality.

**Audit failure preserved:** Initial hand-coded adjacency omitted the edges from the common origin `(0,0)` to the other nine first-column points, spuriously yielding 1,700 spectral violations. Independent tuple comparison exposed the error; it was fixed before any theorem/UNSAT claim. The original incorrect intermediate was not used to exclude branches.

## 2. Necessary GF(2) relation obstruction: valid but needs a deeper search state

Gill–Wanless (2022/2023) proved that any orthogonal pair of order 10 whose associated 4-net has a **nontrivial binary relation** cannot extend to three MOLS(10). They enumerate 18,526,320 such **pair species** (not E064 first-column classes). See https://arxiv.org/abs/2204.10996 and primary data https://users.monash.edu.au/~iwanless/data/MOLS/ .

A complete 4-net(10) has 40 row-incidence vectors over GF(2) (ten for each of four coordinate classes). Three dependencies are always trivial, from equal sums over each class. Therefore `rank_GF2(H)≤37`. A full 3-MOLS(10) **necessarily has rank 37 in every one of its five 4-coordinate projections**. This is valid because any four OA coordinate directions can be reinterpreted as an extendable orthogonal pair, with the fifth direction its mate.

New root-level sound screen: take the 19 fixed five-tuples of a canonical first-column branch, plus an **overapproximation** of *all individually locally permitted* cell placements, ignoring many simultaneous Latin/orthogonality constraints. The rank of their projected incidence span is an **upper bound** for the rank of any genuine completion. If this upper bound were ≤36 in any 4-net projection, then the whole first-column branch would be mathematically impossible.

Exact computation over all 1,700 canonical representatives:

- Initial three projections `(R,C,A,B)`, `(R,C,A,D)`, `(R,C,B,D)`: **all rank upper bounds exactly 37**, zero classes excluded.
- Extended to **all five projections** of five coordinate directions: **(37,37,37,37,37) for every representative**, zero classes excluded.

This does **not** show that a completed orthogonal pair has no relation; it shows only that the root overapproximation has enough freedoms that no relation is *already forced*. High-value next step: invoke this rank oracle on **deeper partial states** when A/B values have been propagated, and learn a globally valid no-good for any explicit nontrivial relation. Do not generate all 2^40 possibilities blindly. The original relation templates (6,965) are available from the Gill–Wanless dataset and are worth studying before implementing invariant cuts.

## 3. Globally sound transversal packing obstruction: powerful on complete pairs

For any orthogonal pair `(A,B)`, a third Latin square orthogonal to both exists **iff** the pair has ten mutually disjoint common transversals. Nine disjoint transversals force the tenth; eight disjoint plus bipartite residual 20-cell resource graph also close the construction. This is exact, not a statistical proxy.

We independently reimplemented exhaustive common-transversal enumeration and maximum set packing for two published complete orthogonal pairs:

| Complete 10×10 orthogonal pair | GF(2) 4-net rank | Total common transversals | Max disjoint | Excluded as possible A/B of 3-MOLS? |
|---|---:|---:|---:|---|
| Egan–Wanless 2016 pair A/B | 37 (maximal) | 14 | 7 | **Yes** |
| Wanless `crimpedMOLS.txt` order-10 pair | 37 (maximal) | 0 | 0 | **Yes** |

Both examples verify Latin rows/columns and exactly 100 pair overlays. The crimped pair was directly transcribed from https://users.monash.edu.au/~iwanless/data/MOLS/crimpedMOLS.txt ; the Egan pair was supplied by the project's E061 archive. These tests demonstrate that **passing the GF(2) rank obstruction does not ensure enough common transversals**, so the two families of global cuts are genuinely complementary. These are restrictions on two *specific complete pairs*, not a proof that every first-column class is impossible.

## 4. Mathematical next steps with potentially large pruning leverage

1. **Candidate-pair elimination as a deep SAT/CP propagation rule.** During construction of any four coordinate classes, compute an upper bound on attainable rank over GF(2) from the currently allowed placement supports. A strict bound `<37` is an exact contradiction. When a complete orthogonal pair is encountered, test all five 4-net projections; any nontrivial relation is a valid Gill–Wanless global cut. A symbolic relation is more general than banning one enumerated pair, and can prune many unrelated completions if integrated as a shared learned clause under justified symmetry.
2. **Require a 10-transversal exact-cover decomposition as soon as an orthogonal pair is fixed.** Use bitset exact maximum packing; if the maximum is <10, reject that pair (Egan and crimped controls). For eight disjoint common transversals test the remaining 20-cell resource-conflict graph for bipartiteness; if bipartite, instantly output and verify 100/100/100. For partial pairs, derive rigorous upper bounds from a relaxation of possible transversals; do not confuse an approximate count with an UNSAT certificate.
3. **Known strong restricted obstructions:** Myrvold/Bright–Keita–Stevens 4×4 Latin subsquare pattern classification and the known exclusion of triples involving a Latin square with nontrivial autoparatopism. These constrain deeper *square structures*, not arbitrary E064 first-column pairs. Do not conflate exclusions of pairs within 20 specific subsquare patterns with unrestricted triple nonexistence. Sources: https://arxiv.org/abs/2503.10504 and classical McKay–Meynert–Myrvold.
4. **Parity constraints only after proving their exact form for OA(100,5,10,2).** Francetić–Herke–Wanless, https://arxiv.org/abs/1703.04764 , derives general parity identities; blindly fixing permutation signs at the E064 root is unsafe and may erase real solutions.
5. **Solver design:** Branch over full four-direction projections and add (1),(2) as adaptive cuts, rather than separately giving each of the 1,700 root classes a few seconds of uninformed generic CNF SAT. Use a proof-producing SAT solver with independently checked LRAT for every excluded class; retain UNKNOWN verbatim.

**Do not claim a fraction solved:** The 18,526,320 published eliminated *pair species* are **not** E064 branches; the root screening has removed **0/1700** of those. E066's completed 1700-case bounded ledger contains **1700 UNKNOWN**, not 1700 negative proofs.

## Reproduction and evidence

`python E067_spectral_scan.py && python E067_spectral_independent.py && python E067_GF2_three_projections.py && python E067_GF2_five_projections.py && python E067_Egan_transversal.py && python E067_crimped_pair.py && python E067_verify.py`

Includes canonical E064 1700 representatives, E061's published neartriple fixture, all 1700-row result datasets, independent spectral crosscheck, E066 full-sweep conclusion summary, SHA-256 manifest, and exact source/negative-result logs. No full solution is asserted.