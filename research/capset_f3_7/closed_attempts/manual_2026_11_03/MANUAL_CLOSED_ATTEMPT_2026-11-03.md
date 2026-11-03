# CAPSET-F3-7 — goal-first manual CLOSED attempt (Fourier-pruned construction + global moment obstruction)

**2026-11-03 UTC · CPU only · actual search executed · result OPEN.**

The user asked to continue manually, **not** to reactivate hourly research. The CAPSET automation `6ae77c6ed4f4819191afec5f9b63437a` remains **disabled**, verified before work. Only exact closure of `r_3(7)` counts as a solution. No new >=237 cap, no verified new full-dimensional upper bound, no equality of global lower/upper bounds this attempt.

## Root decision

With an independently checked 236-point F3^7 witness, `r3(7)=236` holds iff **no cap with 237 points exists**. An honest 237-point witness would only disprove this candidate equality and would need a matching upper bound to determine the exact answer.

## Attack A — full 7D 237-point local search using an explicit violation objective

Built an exact fixed-cardinality 237-point ternary 3AP-violation annealer in C++17. It starts with the verified 236 cap plus one outsider and maintains `g[v]` = number of selected pairs whose third point is `v`. A single exchange `u -> v` changes the number of violated triples by

    -g[u] + g[v] - 1[(-u-v) belongs to the selected set].

It updates all pair counts incrementally, and checks its complete score periodically by independently enumerating the 27,966 unordered pairs of the selected 237 points. The full assertions-enabled run:

    g++ -O3 -std=c++17 closed_anneal237.cpp -o anneal
    ./anneal 6000000 2026110309

returned `DONE ... iterations=6000000 best_conflicts=10 best_overlap=236 accepted=3412595 secs=7.67789`. This is a near-cap with ten forbidden triples, **not a cap**. The prior 2.5m run compiled with `NDEBUG` also reported ten, but the assertions-enabled rerun is the authoritative evidence. Do NOT promote the absence of zero in this finite trajectory to a proof.

## Attack B — use established exact Fourier duality as a safe construction-search gate

The six-dimensional canonical symmetric 112-cap `S` has complete Fourier spectrum `F_S(0)=112`, and `F_S(u)=-23` for `u` in `S` (112 frequencies) and `+4` for all other 616 nonzero frequencies. The second 112-cap `T` also satisfies the same exact self-dual character spectrum. This fact and its inversion were **already present in the project's CAP-025 Fourier audit**. No mathematical priority/novelty claim is made here.

For any invertible linear transformation `M`, let `B=M*T`, `Q=M^{-T}*T`, `I=S∩Q`, `t=|I|=|S∩B|`. For `z != 0`, the convolution (number of cross-slice forbidden representations) obeys

    r(z) = 16 + 4*(1_S(z) + 1_B(z)) + (3*c0(z)-t)/2,
    c0(z) = number of k in I such that k·z = 0 (mod 3).

At origin, `r(0)=t`. Thus for `0<t<32`, **every** `r(z)>0`, i.e. the third slice has NO admissible point; for `t=0`, only origin might be admissible. So any attempted 112+112+13 construction necessarily has `t>=32`. The gate is exact and **does not discard any possible construction within this family**.

Independent standard-library implementation (`spectral_identity.py`) computed every Fourier coefficient of S and T exactly; for 40 reproducible matrix transforms with seed `2026110306`, it compared **all 729 pointwise convolution values** from the formula against an independent 112×112 direct sum, all equal.

The optimized C++17 `spectral_pruned_237.cpp` then searched five separate deterministic seeds. It samples invertible matrices via elementary GL(6,3) row operations, removes duplicates **within each seed run** (not across seeds), calculates `t` cheaply, and only performs the full convolution for the mathematically eligible exceptional cases. If >=13 admissible holes appear, it seeks a 13-cap in those holes, then independently verifies all 237 F3^7 points. All five actual completed runs:

| seed | generated matrices | distinct within run | full hole evaluations | max holes | candidates with >=13 holes |
|---|---:|---:|---:|---:|---:|
| 2026110308 | 2,000,000 | 1,979,708 | 20,201 | 12 | 0 |
| 2026110311 | 4,000,000 | 3,954,149 | 39,525 | 12 | 0 |
| 2026110312 | 4,000,000 | 3,954,411 | 39,076 | 12 | 0 |
| 2026110313 | 4,000,000 | 3,954,593 | 39,451 | 12 | 0 |
| 2026110314 | 4,000,000 | 3,954,479 | 39,619 | 12 | 0 |
| TOTAL | 18,000,000 | 17,797,340 **sum of per-run unique, not globally deduped** | 177,872 | 12 | 0 |

Elapsed for the five completed runs was 3.02 + 7.30 + 7.63 + 6.75 + 8.37 = **33.07 CPU seconds** (tool wall times slightly larger). The 25m-in-one-run trial was **terminated at a tool timeout and yielded no final summary**; it is not included in totals. The GL(6,3) group contains 84,129,611,558,952,960 matrices, so this is emphatically NOT exhaustive over the class, and the class itself excludes caps not having two 112-point slices. **No 237 witness found.**

## Attack C — test whether current universal hyperplane moments can close 287 without more pointwise structure

Root-level 2nd/3rd hyperplane moments of an M-point F3^7 cap, over all 1093 projective normals, are

    total directions = 1093;
    sum(a²+b²+c²) = 364*M² + 729*M;
    sum(a³+b³+c³) = 121*M*(M-1)*(M-2) + 1092*M*(M-1) + 1093*M.

For M=287, 219 local sorted 6-flat triples survive the team's CAP-020 conditional high-slice rules. A **formal integer occupancy histogram** was found by HiGHS that satisfies all three aggregate equalities, with every 6-flat count <=112 and all tested CAP-020 single-direction restrictions:

| sorted (a,b,c) | number of projective directions |
|---|---:|
| (112,109,66) | 132 |
| (112,88,87) | 2 |
| (99,97,91) | 45 |
| (99,96,92) | 164 |
| (97,96,94) | 1 |
| (96,96,95) | 749 |

Independent pure-integer check: sum directions `1093`, S2 `30191539`, S3 `2920545005` exactly. This is **NOT an actual 287-point cap** and does not imply one exists. It proves only that this particular system of aggregate moment + per-direction size inequalities cannot establish a global <=286 bound. Additional quadratic rank/residue constraints or real pointwise intersection constraints are needed. A subsequent exploratory linear-program relaxation of the quadratic rank spectra remained feasible for 13/15 barycenter-zero ranks and 13/13 barycenter-nonzero kernel ranks, but this did NOT exhaust all quadratic configurations/pointwise cap constraints.

**Hostile audit:** An earlier scratch version misclassified the barycenter-zero residue classes for M=287 and falsely printed an infeasibility result. The arithmetic was corrected; those preliminary assertions are **REJECTED**. The fixed rank script `moment_rank_287.py` is the one included as exploratory evidence. The failure and correction are preserved to avoid false mathematical claims.

## Decisions

- Root state: **OPEN**. No independently verified >236 cap. No rigorous global <=236 (or stronger independently reviewed new upper bound). No proof certificate.
- Do not use hourlies, do not generate meaningless verifier-only experiments.
- Slices 112+112 are a *conditional* root subtree, not globally exhaustive; no nonexistence proof can be inferred from millions of failed searches.
- The self-dual Fourier filter makes the two-112 construction test >100 times cheaper per random matrix by skipping almost all full convolutions, but further sampling alone is unlikely to close dimension7. For a mathematical closure, a global classification/proof-logged SAT UNSAT covering every 237-point candidate is required.
- The aggregate moment-only route cannot prove a global <=286 without new pointwise restrictions; do not mistake the formal integer histogram for a cap construction.
- Next attempts only on explicit user request, as per disabled automation.

## Sources and rerun

Authoritative original fixture: `research/capset_f3_7/candidates/calderbank_fishburn_236.txt` (GitHub blob `bb75562499071945a07273e439a892c55a8d6b9f`), previously independently verified 236 distinct points and 0 3AP.

Project's previous CAP-025 preexisting dual Fourier theorem: `research/capset_f3_7/CAP025_FOURIER_COMMON_TANGENT_REFEREE_2026-11-02.md`.

Public status as of 2026-11-03: https://cairn-commons.com/problems/cap-sets-dim-7 (236 <= r3(7) <= 291; Thackeray preprint claims <=288). https://arxiv.org/abs/2206.09804 (preprint). The project's provisional <=287 is still explicitly under independent referee, not promoted here.

Build and rerun under a system with C++17, Python3, SciPy:

    python spectral_identity.py
    g++ -O3 -std=c++17 spectral_pruned_237.cpp -o spectral_pruned_237
    ./spectral_pruned_237 4000000 2026110311
    g++ -O3 -std=c++17 closed_anneal237.cpp -o closed_anneal237
    ./closed_anneal237 6000000 2026110309
    python moment_287_feasibility.py
    python moment_rank_287.py

The sources read `witness236.txt` in the working/extracted directory or the repo canonical `research/capset_f3_7/candidates/calderbank_fishburn_236.txt`; set environment variable `CAPSET_WITNESS` to override. The ZIP includes `witness236.txt`. No API keys or personal credentials are bundled.
