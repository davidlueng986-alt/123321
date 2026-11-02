# CAP-010A — Unique completion of every 110/111-cap in AG(6,3) (2026-11-02)

## Exact result and provenance

**Theorem (conditional only on two published classification results).** Every 110-point cap in AG(6,3) has precisely two distinct points that can be added individually while retaining the cap property, and admits exactly one 112-point cap completion. Every 111-point cap in AG(6,3) admits exactly one 112-point completion. Moreover, any cap obtained by deleting at most nine points from a maximal 112-cap has no additional point outside that original 112-cap that can be added.

**Proof.** Use the known maximal 112-cap S. By an independent direct finite computation of all 6216 unordered pairs, every point outside S is the third point of exactly 10 secants of S, except one distinguished point which is the third point of 56 secants. Each point outside S has >=10 pairwise vertex-disjoint secants, since for fixed z each s in S has at most one possible partner s'=-z-s. Removing d<=9 points cannot meet all ten disjoint secants. Therefore S minus any d<=9 has no admissible outside-S extension. Every removed point remains addable because S itself is a cap.

Potechin, *Maximal caps in AG(6,3)* (Designs Codes Cryptogr 46, 2008, pp.243-259, DOI 10.1007/s10623-007-9132-z) proved all maximal 112-caps are affinely equivalent. Thus the 10-secant minimum and nine-deletion stability hold for any maximal 112-cap.

Thackeray, *The cap set problem: Up to dimension 7* (2022 preprint, arXiv:2206.09804) states every 110-cap in AG(6,3) is obtained by deleting two points from a 112-cap. Fix an arbitrary 110-cap U and a completion S. The stability above implies the only possible single-point extensions of U are the two points S\\U. Therefore S is the unique 112 completion. For an arbitrary 111-cap T, remove one t to get 110-cap U; by uniqueness U has exactly two addable points, so t lies in its unique completion S and T is contained in S. Every 112 completion of T is also a completion of U, hence S is unique.

This theorem does NOT say 110/111 caps have no 112 completions; they always do. It also does NOT rule out a 237-cap in F3^7, since cross-slice compatibility is still unproved.

## Independent finite evidence

- Direct independent JavaScript mod3 audit of classical 236-cap first 112 slice: outside secant histogram 10:616 and 56:1; all 6216 deletion pairs tested against all 617 external points; zero outside extensions.
- Reproducible stdlib Python generator/checker: `python research/capset_f3_7/cap010a_110_111_unique_completion.py --exhaustive`.
- Unittest: `python -m unittest discover -s research/capset_f3_7 -p 'test_cap010a_110_111_unique_completion.py' -v`.
- Tests verify cap property, distinctness, exact 6216 secants, disjointness of every external secant family, 6216 deletion-pair cases, and 10/56 histogram.
- No GPU, paid compute, random seed, or SAT solver needed. The published classification premises have not been independently reproved in this project. Novelty NOT established: this may be a known corollary of 110-cap classification.

## Strategic consequences for global n7 target237

This closes a genuine logical gap: previously the anchored 112-slice model treated 111 and 110 second slices as arbitrary. Now all 110/111 second slices can be represented as deletions of one/two points from some maximal112 second slice, without excluding valid caps, conditional on the cited classification results.

Use the already-derived centered 112+112 Fourier lower bound for nonzero third-slice points:
r_{S,T}(z)>=16-k/2, where k=|S∩T| is even and S,T are centered 112 caps. Deleting d points from T removes at most d representations at any z. Therefore for 112+111+14 (d=1), if k<=28 no nonzero third-slice positions are available; at most z=0 remains, so 237 is impossible. Hence k>=30 is necessary. For 112+110+15 (d=2), k<=26 likewise leaves at most z=0; k>=28 necessary. The special z=0 is deliberately retained: if k=0 or k<=d, it can be a hole. These are global conditional overlap cuts, not a global cap upper bound.

**Meta-audit:** The Drive ledger has newer CAP-009A/B structural notes not present in GitHub STATE at the time of this run; this report does not claim novelty for the 112+112 Fourier lower bound and does not overwrite other research branches. The SRG(729,112,1,20) is historically the *Games graph* and is not a newly discovered graph (external literature check 2026-11-02). Avoid novelty claims on that result. Current bottleneck is proof-logged exhaustive treatment of remaining high-overlap 112+110/111 profiles and no-112-hyperplane branch.

## References

- https://doi.org/10.1007/s10623-007-9132-z
- https://arxiv.org/abs/2206.09804
- https://en.wikipedia.org/wiki/Games_graph (prior graph identification, not a primary proof source)

No new >=237 witness; no stronger global numerical bound; r3(7) remains OPEN.
