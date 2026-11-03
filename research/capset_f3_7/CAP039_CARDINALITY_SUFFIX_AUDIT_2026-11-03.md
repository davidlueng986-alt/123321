# CAP-039 — Independent cardinality-suffix audit (2026-11-03)

## Scope and provenance
Continues CAP-038, whose independent arithmetic checker established the 796,797-clause 3AP prefix. CAP-035 appends two Sinz at-most counters per one of 81 fibers, enforcing exactly the CAP-027 formal 285 occupancy. This run audits the cardinality suffix only; it does NOT solve SAT or prove any upper bound. Deterministic CPU only; seed 390039; no GPU/paid compute.

## Mathematical correctness argument
For an at-most-k constraint on signed literals x_1,...,x_n (where a signed literal is interpreted as a Boolean proposition), define auxiliary s(i,j) to mean at least j of x_1,...,x_i are true, for 1<=i<n,1<=j<=k. CAP-035 clauses propagate all required positive implications: x_i=>s(i,1), s(i-1,1)=>s(i,1), x_i AND s(i-1,j-1)=>s(i,j), and s(i-1,j)=>s(i,j). The overflow clauses x_i=>NOT s(i-1,k) forbid k+1 true inputs. Clauses NOT s(i,j) for j>i prevent impossible prefix states. Hence any input with >k true literals forces a contradiction by unit propagation; conversely for <=k true inputs, choosing s(i,j) equal to the true prefix-threshold predicate satisfies every clause. This applies equally to the counter on negated literals, so the two counters together encode exact-k. The proof does not depend on a SAT solver.

## Reproducible experiment
Run `python3 research/capset_f3_7/cap039_cardinality_audit.py`. Local execution on Python stdlib: PASS, 162 counters, 59,049 total variables (2,187 primary plus 56,862 auxiliary), 135,561 suffix clauses, 7,938 valid constructive witnesses and 4,050 invalid input vectors refuted by independent unit propagation. Seed 390039. Suffix SHA256 (clause lines without DIMACS header): `992e7f9dd4b75199d511a4253fd868f047c04fe38fe6b38b1b8ffd5eb`. Total complete CNF clauses should be 932,358. No solver was installed locally (pysat/pycosat/z3 and kissat/cadical/minisat unavailable). No SAT/UNSAT outcome.

## Self-audit and caveats
The independent implementation follows the same published Sinz encoding but uses a separate code path, constructive assignments, and unit propagation rather than CAP-035's small truth-table test. The 12,000 sampled cases do not exhaust 2^27 assignments, but the argument above proves soundness and completeness for every input. The suffix hash has NOT yet been compared byte-for-byte against a CAP-035-generated file; such a comparison and CI must be done before calling full end-to-end CNF independently verified. A fixed occupancy UNSAT would exclude only that pattern, not yield a global bound.

## Research decision
Stop low-value count-only/symmetry repetitions. Next run: compare full DIMACS suffix hashes, install/use a free CPU SAT solver if possible with bounded time and proof logging (UNSAT requires independently checked proof), or pivot to CAP-019 110-cap classification referee and nonlocal >=237 constructions. Novelty: standard Sinz encoding and audit, no novelty claim. Current known public status remains 236 <= r3(7) <= 291 (Thackeray 2022 preprint proposes <=288); exact optimum OPEN.
