# CAP-031 | Exact shared-fiber 3AP factorization | 2026-11-03 UTC

## Scope and provenance
Continues CAP-030 after checking branch STATE/LOG/BACKLOG, Drive ledger and GitHub Actions. CAP-030 CI run 41556385711 SUCCESS on SHA 4a29329f44a7e667bdc5165787d221b3829dbd76. No claim of literature novelty: this is an elementary encoding identity, not a new bound.

## Exact factorization theorem
Choose a splitting F_3^7 = F_3^4 × F_3^3. Write each point (q,u), q in F_3^4, u in F_3^3. A 3-point affine line is an unordered triple of distinct points summing to zero. Projection onto F_3^4 has exactly two possibilities: (a) all three q coincide; or (b) three distinct q form a quotient affine line. The case exactly two equal quotient coordinates is impossible because q+q+r=0 implies r=q in characteristic three.

There are 81 fibers; each fiber has 27 points and 27*26/6=117 affine lines, giving 9,477 internal 3AP clauses. There are (81*80/6)=1,080 quotient affine lines; each has 27²=729 lifts, indexed by (u,v), with third point -u-v. This gives 787,320 cross-fiber clauses. Total **796,797** distinct 3AP clauses, equal to 2187*2186/6, the direct ambient-space count. Each 3AP is counted exactly once.

## Exact CNF and shared-fiber semantics
Use 2,187 Boolean point variables x[q,u]. For each internal line and cross-fiber lifted triple, emit clause (¬x_a ∨ ¬x_b ∨ ¬x_c). Add a cardinality constraint Σx≥K (K=285 is a targeted hypothetical branch, NOT the global objective). For CAP-027's specific count-only negative control, additionally impose Σ_u x[q,u]=f(q) for all 81 q. Crucially, all 1,080 quotient lines reference the SAME variables x[q,u], enforcing compatibility that independent 4D lifts cannot capture. A satisfiable result under f would only certify a 285-point cap if an independent 3AP checker validates the 2,187-bit assignment; UNSAT under f excludes ONLY that occupancy pattern, not all 285-point caps.

## Reproduction
Run `python3 research/capset_f3_7/cap031_factorization.py` (stdlib; no seed/GPU/paid compute). Expected output: `PASS 1080 9477 787320 796797`. The 1,080 quotient lines are enumerated as canonical sorted triples. This verifies combinatorial counts and factorization, **not** SAT satisfiability/unsatisfiability, and no LRAT certificate exists yet.

## Meta-audit and next gate
CAP-027/028 count-only and independent-line liftability are demonstrably too weak. CAP-031 gives an exact, finite, globally shared-fiber model but the naive CNF is nearly 0.8 million clauses. Next bounded experiment: instantiate fixed f(q), apply unit propagation and exact fiber cardinalities, then run bounded proof-logging SAT; if timeout report UNKNOWN, never UNSAT. Preserve independent Thackeray completion referee, balanced/no-111, and >=237 constructive searches. No new witness or global upper bound; r_3(7) OPEN.
