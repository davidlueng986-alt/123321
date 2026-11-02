# CAP-005F — Six-fiber fixed-point conflict clique certificates (2026-11-02)

## Precise restricted theorem
Let B be the independently checked 236-point cap in F_3^7 at candidates/calderbank_fishburn_236.txt. Partition F_3^7 into 27 affine F_3^4 fibers by the first three coordinates. In a neighborhood T of exactly six fibers, points of B outside T are held fixed, and points inside T may be deleted/replaced arbitrarily.

CAP-005E certified that 294,394 of all C(27,6)=296,010 choices of T cannot improve 236, using the necessary condition that any improving replacement must insert at least 17 outsiders. For another **680 distinct** previously unresolved choices of T, we now provide a direct exact certificate that at most 16 outsiders can coexist with the fixed B points. Therefore **295,074 of 296,010** six-fiber neighborhoods are rigorously excluded; **936 remain unresolved**. This is NOT a global upper bound, and the exact six-fiber restricted optimum is not yet proved.

## Mathematical certificate
For each released-fiber set T, let E_T be the outsiders whose every B-secant has an endpoint in T. Every cap agreeing with B outside T can add outsiders only from E_T.

Make a conflict graph H_T on E_T: connect x,y if z=-x-y (mod 3) lies in B outside T. Since z remains fixed, no valid cap can select both endpoints of an H_T edge. A partition of E_T into q cliques of H_T proves at most q outsiders can be added. The deterministic DSATUR algorithm colors the complement of H_T, generating q<=16 for 680 previously unresolved T. Each color class is a clique in H_T, so this is a checkable proof, not an optimizer status.

The independent checker reconstructs B, all 1,951 outsiders, every original secant, each complete E_T, and directly checks every pair in every clique by mod-3 arithmetic. It checks exact coverage and no duplication, as well as the 680 unique released sets. The certificate JSON is a standalone finite witness, generated and archived by CI.

## Local bounded reproduction
Commands from repository root:
```sh
python research/capset_f3_7/cap005_k6_clique_cover_certificate.py --out /tmp/cap005_k6_clique_cover.json
python research/capset_f3_7/cap005_k6_clique_cover_check.py /tmp/cap005_k6_clique_cover.json
sha256sum /tmp/cap005_k6_clique_cover.json
```
Local CPU generator PASS (~18.4 s); independent checker PASS (~1.6 s). Generated JSON SHA-256: `12bf1b9787390691072e6b627afaf73fa44fcab3db13c35479d004fa57bb830f`. No random seed, GPU, or paid compute. GitHub CI confirmation pending at this write; do not label CI green before inspecting run. No >=237 witness or improved global upper bound.

## Strategy audit and literature
The previously neglected fixed-original-point conflicts yield a non-optimization certificate, reducing unresolved neighborhoods from 1,616 to 936 (42.08% of survivors). Remaining cases may require outsider-triple hypergraph conflicts and exact deletion-cover inequalities, not simply more symmetry-restricted searches. Nonlocal occupancy-changing constructions and independently auditable global upper bounds remain higher-level priorities. Literature novelty of this restricted certificate has NOT been established. Public problem tracker dated 2026-10-03 still reports 236<=r3(7)<=291; Thackeray arXiv:2206.09804 reports no 289-point cap (preprint claim, not independently checked here). Exact r3(7) remains OPEN.
