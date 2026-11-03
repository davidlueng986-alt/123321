# CAP-043 — Frame secant collision audit (2026-11-03 UTC)

## Scope and provenance
Continues CAP-042 (ten dense-hyperplane ninth-point branches). Independent small integer checker using a **different** base-3 encoding (least-significant coordinate first), rather than CAP-042's most-significant-first implementation. No SAT solve or global upper bound is asserted.

## Exact finite result
Fix the standard affine frame F={0,e1,...,e7} in F3^7 and restrict ninth point p to the distinguished hyperplane H (seventh coordinate zero). Exclude F and the third points of frame secants. Under the S7 permutations of the seven H-frame vertices, the 701 eligible ninth points form ten classes of sizes 7,35,1,105,42,21,210,140,35,105 (in sorted barycentric-tag order). For nine representatives, the 36 unordered pairs of the nine selected points yield 36 distinct forced-zero third points. The exceptional tenth class yields only 35: in this checker's least-significant-first point encoding, representative p=4=e1+e2 gives the collision third(0,p)=third(e1,e2)=8. Thus two distinct selected secants share their third point. The 35 count is not an omitted constraint or off-by-one bug.

## Independent reproduction
`python3 research/capset_f3_7/cap043_secant_collision_audit.py` (Python standard library, deterministic, no seed, no GPU/paid compute). Expected: 10 classes, 701 candidates, forced-zero list [36]*9+[35], sole collision at branch 9. This checks local secant bookkeeping, **not** the correctness of a solver proof. Compare with CAP-042's independent incidence census and its CI.

## Strategy audit
The ten-leaf root reduction remains exhaustive only subject to the CAP-040/041 dense-hyperplane moment and symmetry arguments. CAP-043 explains the exceptional branch's 35 forced zeros; it cannot prune that branch. Stop spending cycles on further census-only work: next priority is a bounded proof-logged SAT pilot with independent checker and exact SAT/UNSAT/UNKNOWN reporting, then CAP-019 upper-bound referee and >=237 nonlocal constructions. Exact r3(7) OPEN; no novelty claim.
