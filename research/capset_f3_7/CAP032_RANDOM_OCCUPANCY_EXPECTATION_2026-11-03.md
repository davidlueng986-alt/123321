# CAP-032 — Exact random occupancy baseline (2026-11-03 UTC)

Status: exact analytic calculation, NOT a cap witness, NOT an upper bound, NOT SAT/UNSAT evidence. Continues CAP-031's shared-fiber model.

Let Q=F_3^4, H=F_3^3. Use CAP-027 fixed occupancy f(q)=3+1[q_0=q_1=0]+3*1[q=P[7i mod 81], 0<=i<11], where P is lexicographically enumerated Q. For each q, choose an independent uniformly random f(q)-element subset of H. Then X is the number of collinear triples in the resulting 285-point set.

There are 117 affine lines in H. A fixed internal triple is present with probability (f)_3/(27)_3. Thus E[X_internal]=117 sum_q (f(q))_3/(27*26*25)=341/25=13.64.

For every quotient affine line {q,r,s}, exactly 729 full-space triples project to it. Every such triple occurs with probability f(q)f(r)f(s)/27^3, so E[X_cross]=(1/27) sum_{quotient lines} f(q)f(r)f(s). Direct deterministic enumeration of 1080 quotient lines gives sum=46863, hence E[X_cross]=46863/27=5207/3.

Therefore E[X]=341/25+5207/3=131198/75 = 1749.306666..., even though each fiber is tiny (3,4,6,7). This is an EXACT expectation under the specified product measure, not a bound on the minimum number of triples, not a proof that the 285 occupancy pattern is impossible, and not a probability estimate for obtaining a cap. It quantifies the geometric burden missed by count-only relaxations. In particular, naive independent uniform fiber sampling is not an appropriate high-yield search strategy; use coordinated shared-variable SAT/PB or conditional sampling with 3AP propagation instead.

Independent algebra check: the quotient-line sum can be computed by summing f(q)f(r)f(-q-r) over all ordered distinct q,r and dividing by 6. Internal expectation uses the 117=(27*26)/6 affine lines in H. No GPU, paid compute, SAT solver or random seed used.

Reproduce with Python stdlib: enumerate Q=itertools.product(range(3),repeat=4), build f, then for q<r compute s=-q-r mod3 and count only r<s; assert 1080 lines and sum(f[q]*f[r]*f[s])==46863. Assert sum(f)==285 and histogram {3:63,4:7,6:9,7:2}. This report is not independently CI-verified until the corresponding branch CI passes.

Meta-audit: the main bottleneck remains global point-level compatibility, not local occupancy feasibility. CAP-019 <=287 classification dependency remains unreviewed. Preserve balanced/no-111 and >=237 construction branches. No new >=237 witness or global upper bound; exact r3(7) remains OPEN.
