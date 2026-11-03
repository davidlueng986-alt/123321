# CAP-036 — Exact quotient occupancy symmetry audit (2026-11-03 UTC)

Continuation of CAP-035's exact fixed CAP-027 285-point fiber occupancy (not an actual cap). The quotient occupancy is
`c(q)=3+1[q0=q1=0]+3*1[q in {Q[7i mod 81]:0<=i<11}]`, with lexicographically enumerated Q=F3^4.

**Exact bounded result:** exhaustive evaluation of all 81 translations, 384 signed-coordinate permutations (monomial matrices), and their 31,104 affine combinations yields **identity alone** preserving the full 81-entry occupancy function. Thus the usual quotient translation or monomial symmetry-breaking constraints cannot safely be imposed on CAP-035's *fixed occupancy* instance without further proof. This does **not** establish the stabilizer in the full AGL(4,3), which is far larger; nor does it say that no other symmetry (including internal fiber transformations) exists.

Reproduce: `python3 research/capset_f3_7/cap036_occupancy_stabilizer.py`. Deterministic CPU-only; no seeds, GPU, paid compute, or SAT solver. Cross-check the 81-fiber histogram (63×3, 7×4, 9×6, 2×7) and all 31,104 candidate maps. This is an elementary finite enumeration, not claimed as new literature.

**Meta-audit:** CAP-035 is a valid formulation but no SAT/UNSAT solve is established. Given the large 796,797 triple clauses, first prioritize proof-logged CPU-bounded pilots and independent checker, with solver timeout UNKNOWN. Avoid invalid symmetry breaking. Even fixed occupancy UNSAT would not imply a global upper bound. Continue CAP-019 referee and independent >=237 construction attempts. Exact r3(7) OPEN.
