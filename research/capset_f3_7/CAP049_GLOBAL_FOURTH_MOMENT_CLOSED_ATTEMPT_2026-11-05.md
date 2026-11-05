# CAP-049 — Manual root-directed CLOSED attempt: exact global fourth-moment upper certificate

**Research date:** 2026-11-05 (UTC); **status: ROOT STILL OPEN**. CPU only, no GPU or paid compute. The hourly CAPSET research automation remains disabled; this was initiated manually.

## Root objective and genuine result

Determine exact `r3(7)`. We have the independently checked 236-point witness, so a complete proof of nonexistence of a 237-point cap would prove the exact value 236. **No such proof or >=237 witness was found.**

In this manual attempt we developed a **standalone exact-integer reproof of the established published bound `r3(7) <= 291`**, with a 184-case rational dual and a general fourth-moment identity. This is a **rigorous global upper bound**, not a new numerical record (the established public bound already equals 291). The core certificate is checked by two independent programs (Python stdlib and C++17) with no floating point in the proof. Prior `CAP019` claims a provisional `<=287` conditional on external 110-cap classification, but that claim is not being conflated with the reviewed result here.

## Direct theorem-level proof: no 292-point 7-cap

Let `A` be an assumed 292-cap in `F3^7`. For each of `D=(3^7-1)/2=1093` projective nonzero normals, the three parallel 6-dimensional slice sizes are `(a,b,c)`, with `0<=a<=b<=c<=112`, `a+b+c=292` (using the known theorem `r3(6)=112`). There are **exactly 184** integer triples meeting these conditions.

Define `S_k = Σ_normals (a^k+b^k+c^k)`. Counting ordered tuples of distinct cap points against the projective normals annihilating their affine span gives:

- `S2 = D*M + 364*M*(M-1)`.
- `S3 = D*M + 3*364*M*(M-1) + 121*M*(M-1)*(M-2)`.
- `S4 = D*M + 7*364*M*(M-1) + 6*121*M*(M-1)*(M-2) + 40*M*(M-1)*(M-2)*(M-3) + 1944*P`.

Here `P` is the number of coplanar unordered 4-subsets of `A`; each planar four-cap has exactly ONE pairing of its four points into two distinct pairs having the same affine secant third point `q=-x-y`. Conversely two distinct cap pairs with equal third point have disjoint endpoints and form a coplanar four-cap. Thus `P = Σ_{q∉A} binom(d_q,2)` where `d_q` is the number of cap pairs through external point q and `Σ d_q=binom(M,2)`.

At M=292, there are 1,895 outsiders and 42,486 secant pairs. Discrete convexity yields `P >= 455257` (1,099 outsiders have d=22 and 796 have d=23 in the balanced minimum). Thus

`S4 >= 303851985100`.

**Exact finite dual certificate:** For each of ALL 184 sorted integer triples as above, direct integer verification yields

`30464609312 - 2254590*(a²+b²+c²) + 16531*(a³+b³+c³) - 45*(a⁴+b⁴+c⁴) >= 0`.

Equality occurs only at (68,112,112), (90,90,112), (97,97,98). Summing over all 1093 normal directions and substituting exact S2=31,248,964 and S3=3,074,776,060 yields

`45*S4 <= 30464609312*1093 -2254590*31248964 +16531*3074776060 = 45*(1519259920124/5)`.

Together with the convexity lower bound,

`45*S4 >= 45*303851985100`, which exceeds the previous upper bound by the **positive exact integer 48,384**. Contradiction. Thus no 292-cap, and hence `r3(7) <=291`.

**Independent checks:** `cap049_global_fourth_certificate.py` enumerates all 184 cases using Python integers and checks all totals; `cap049_independent_cpp.cpp` recompiles and checks the 184-case inequality and 48,384 contradiction using independent C++17 integer code. The additional `cap049_fourth_moment_root_attack.py` independently computes S4 and the `Σ binom(d,2)` term from all 1093 hyperplane directions and all 27,730 pairs of the canonical 236 witness, and confirms `S4=130900831300`, P=198503 exactly.

## Closed-attempt audit: what would be needed to improve 291 to 290?

We also obtained a **second exact rational dual** for a hypothetical M=291 cap. Its certificate is

`15*S4 <= 9957864606*D -743397*S2 +5482*S3`,

checked against all 192 allowed triples of slice sizes <=112. Together with the same S4 identity, it implies `P<=548600572/1215=451523.104...` hence P<=451523. The elementary convexity lower bound from 42,195 secant pairs over 1,896 outsiders gives only `P>=448602`.

Therefore the **precise missing theorem** required by *this particular method* is `P>=451524`: an improvement of **2,922 coplanar quadruples** over basic convexity. This is a target for a genuinely cap-specific geometric argument, but it has NOT been proved. Even proving <=290 would still not determine the exact r3(7).

We explicitly tested another root-level hypothesis: could fourth moments + the basic secant-degree constraints force every 237-cap to have a hyperplane with >=90 points (improving CAP007J's >=89)? The answer is **NO at the level of these aggregate conditions**. A formal, not geometrically realizable, nine-profile integer histogram with all hyperplane counts <=89 matches all required S1,S2,S3,S4 and the exact minimum-compatible secant-degree count with P=187105. It is reproduced by `cap049_fourth_moment_root_attack.py`, with degrees 13:331,14:622,15:997 across 1,950 outsiders. **This is NOT a cap and does NOT refute the actual >=90 hypothesis; it refutes only a purported deduction from these aggregates.**

## Direct construction attack (full dimension, not fixed 112+112 fibers)

An independently written C++17 237-fixed-size hypergraph local search used exact ternary third-point arithmetic, the independently checked 236 baseline, and Metropolis swaps of selected and unselected points in all 2,187 global positions. Actual run `anneal_237_new 6000000 2026110501` completed, best **10 forbidden triples**; zero was never reached. This negative stochastic result proves nothing about global maximality. Full code and raw log are in the attached evidence ZIP. This attempt is different from the prior 6M swap run's exact code but did not improve its prior best conflict count.

## Proof assumptions, novelty and resource log

- Assumes only the published exact six-dimensional cap maximum `r3(6)=112`; no 110-cap classification, no special stabilizer or fixed 236-point reconstruction family is required for the <=291 certificate.
- All proof arithmetic exact integers; scipy/HiGHS used **only to discover** supporting rational duals and construct a formal negation model, and the resulting finite certificates were independently verified without any optimizer.
- Exact cap checker on 236 dataset: 236 distinct points, zero 3APs, all 27,730 unordered pairs; 1093 hyperplane direction counts checked independently. No 237-point witness.
- The upper bound 291 is **already published**; no novelty or priority claim. Literature confirms problem remains OPEN as of November 2026; Thackeray 2022 preprint claims <=288, project CAP019 conditional <=287 is under review.
- Earlier research was already at CAP048. This new CAP049 was explicitly root-directed and did NOT re-enable hourly automation. No related MOLS10 or unrelated repository branch was modified.

### Reproduce

```bash
python cap049_global_fourth_certificate.py
python cap049_fourth_moment_root_attack.py witness236.txt

g++ -std=c++17 -O2 -Wall -Wextra -Werror cap049_independent_cpp.cpp -o cap049_dual_check
./cap049_dual_check

g++ -std=c++17 -O3 anneal_237_new.cpp -o anneal_237_new
./anneal_237_new 6000000 2026110501
```

**Final status: OPEN.** All known globally exhaustive 237 SAT leaves remain UNKNOWN. The new verified global <=291 argument only re-proves the existing numerical bound. The next worthwhile attack must close the `P>=451524` gap (only if pursuing a 290 upper bound) with cap-specific geometry, or solve a true full-root SAT branch with independently checked proof, or construct a genuinely independent >=237 cap and then obtain a matching upper bound. No more routine recurring verification jobs.


## Durable raw artifacts

Complete runnable Python/C++17 scripts, exact 184-case dual certificate, 237 formal negative model, full 7D 6M-swap construction log, and canonical 236 fixture: https://drive.google.com/file/d/15RGWljWUdrMmAnOAABNCtcSZy9VYS0Eq/view?usp=drivesdk (ZIP SHA256 `1840c4da0731ea20851552bb6774b34c06ff7ef7d5379dc552ae2b9f5c0b46a7`).
