# CAP-037 — Full AGL(4,3) stabilizer audit (2026-11-03 UTC)

## Result
The CAP027 fixed 285-point **formal occupancy** has trivial stabilizer in the **entire affine group AGL(4,3)**, strengthening CAP036's affine-monomial-only result. This is a statement about the occupancy function, not about a 285-point cap. It gives **no new bound** on r_3(7).

## Exact proof and finite certificate
Let Q=F3^4, E={(0,0,u,v)}, S={Q[(7i) mod 81]:0<=i<11} in Python lexicographic product order, and f(q)=3+1_E(q)+3*1_S(q). The nine positions with f in {4,7} are exactly E, so every affine stabilizer preserves E. Consequently its block form is (x,y)->(Ax,Cx+Dy+t), where A,D in GL(2,3), C arbitrary 2x2, t in F3^2. The two seven-occupancy points are (0,0,0,0) and (0,0,2,1), so the unordered pair must be preserved. Exactly 12 (D,t) pairs do this. Enumerate all 48*81*12=46,656 candidates and test preservation of the nine six-occupancy points; precisely the identity passes. Preservation of E, the two seven-points and the nine six-points implies preservation of all four occupancy classes.

## Reproduction
`python3 research/capset_f3_7/cap037_full_agl_stabilizer.py`
Expected output: `PASS full AGL4 stabilizer = identity; tested 46656 candidates; no seed`.
Local independent audit also enumerated all 31,104 affine monomial maps and found only identity (CAP036 reproduction). CPU-only; no randomness, GPU or paid compute. GitHub CI must independently pass before this is CI-certified.

## Strategy and limitations
No quotient AGL(4,3) symmetry breaking is available **for this fixed occupancy**. This does not rule out fiber-coordinate symmetries, nor symmetry reductions for unrestricted cap search. The fixed occupancy SAT problem remains UNKNOWN, and a conditional UNSAT would not prove a global bound. Prioritize proof-logged shared-fiber SAT, independent CAP019/Thackeray referee, and >=237 witness search. Full-group enumeration is elementary, novelty not claimed.
