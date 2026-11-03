# CAPSET-F3-7 — CLOSED ATTEMPT: Exact Fourier pruning of 112+112+13 (2026-11-03)

## Root obligation and result

**Root remains OPEN.** We seek the exact value `r3(7)`, not merely a 237-cap. An independently checked 236-point cap is in the project repository. A proof of no 237-cap would establish `r3(7)=236`; a 237-point witness would only disprove the tentative equality and require a matching upper-bound proof.

This run directly attacks the **constructive branch** `112 + 112 + 13 = 237` with a rigorous, universal-for-that-family Fourier identity. It mathematically eliminates all pairs whose dual intersection has cardinality 0<t<32, and proves that t=0 gives only one possible third-slice point. It **does NOT** prove that every possible 237-cap has this profile, or prove that `112+112+13` is impossible in full. The hard cases have t>=32.

## Exact regular-cap algebra

Let S be the canonical 112-cap in `F3^6` from the first coordinate-0 slice of the verified 236-point fixture; normalize its unique center to 0. The 112 points are centrally symmetric, exclude 0, and are 3AP-free. Exact integer enumeration of 112² differences yields, for all `u in F3^6`,

    R_S(u) = |{(a,b) in S²: a-b=u}|
           = 112, if u=0;
               1, if u in S;
              20, if u !=0 and u not in S.

Equivalently, for `f=1_S`, the ordinary convolution in the group algebra is

    f*f = 20*1_(F3^6) - 19*f + 92*delta_0.

This is checked independently on all 729 group elements (the `u in S` case is also forced by the symmetric cap condition). Under the ternary Fourier transform with characters `omega^(<xi,x>)`, `omega^3=1`, the 112-point set is **self-dual**:

    fhat(0) = 112;
    fhat(xi) = -23  if xi in S;
               4   if xi !=0 and xi not in S.

This is verified without floating point, by checking all 729 integer orthogonality counts `#{x in S:<xi,x>=0}`, which are exactly 112/22/40 for `xi=0`, `xi in S`, and other nonzero `xi`. The second 112-point slice of the verified 236-cap has the same exact fingerprint. Potechin (2008), *Maximal caps in AG(6,3)*, proves all maximal 112-caps are affine-equivalent; hence the centrally normalized spectral pattern applies to every maximal six-dimensional cap, subject to that published classification theorem.

## Rigorous convolution identity for ANY two affinely equivalent 112-caps

Take centrally symmetric caps S and T=M*T0 (invertible M over F3), with T0 a centrally normalized maximal 112-cap. Let Q=M^{-T}T0 denote T's negative-frequency eigenspace support. Define K=S intersect Q and t=|K|. Both S and Q are centrally symmetric; t is even. Let

    c_K(z) = #{k in K: <k,z>=0}.

For r(z)=#{(s,t') in S*T: -s-t'=z}, Fourier inversion gives **exactly**

    r(0) = t;
    r(z) = 16 + 4*(1_S(z)+1_T(z)) + (3*c_K(z)-t)/2     for z!=0.

Derivation: for nontrivial characters, `fhat_S=4-27*1_S`, `fhat_T=4-27*1_Q`. Multiply, expand `16-108*(1_S+1_Q)+729*1_K`, and invert using the self-dual transform of S and T. The sum is integral because K consists of antipodal pairs. All 729 values were independently checked against direct 12,544-pair integer convolution in 60 deterministic invertible-M cases, seed=2026110405: PASS.

### Formal consequence: an entire family is impossible

If t=0, `r(0)=0` and `r(z)>=16` for all z!=0. Thus exactly one third-slice site remains.

If `0<t<32`, then `t` is even, so t<=30 and for all z!=0:

    r(z) >= 16 - t/2 >= 1;

also `r(0)=t>0`. Therefore **no third-slice sites remain at all**. This is a proof, NOT a statement from random samples. The 112+112+13 construction is impossible in either case. The remaining t>=32 cases require separate work.

For t=32 specifically, the formula simplifies for z!=0 to

    r(z)=4*(1_S(z)+1_T(z)) + 3*c_K(z)/2.

An absent third-slice point must satisfy z outside S union T AND c_K(z)=0. This transforms the difficult remaining construction subproblem into an exact projective-hyperplane avoidance condition for the realizable intersection K.

## Adversarial false shortcut: rejected by explicit 32-point witness

**Do not** assume that every symmetric 32-point cap C subset S has at most 12 nonzero normals z with C intersect z^perp empty. We constructed an independently checked 32-point antipodal cap C subset S (16 representative vectors; their negatives are included), with **14** such nonzero normals:

Representatives:
`111212 112211 121222 122111 122122 112000 120200 102020 100102 100011 100012 100022 012001 010110 010022 001210`

Fourteen avoiding normals:
`001110 002220 010120 012002 020210 021001 110100 110121 111221 121121 212212 220200 220212 222112`

All 32 points belong to S and have zero 3AP conflicts; each listed normal has nonzero inner product against every one of the 32. Thus a naive *arbitrary-subset* proof of the desired 12 bound is **false**. Any true bound must exploit the stronger condition K=S intersect M^{-T}T0 and the second cap's full 112-point structure. Whether the explicit 32-cap can arise as that intersection is unknown. This is a concrete early-assumption failure and narrows the required theorem.

## Actual bounded constructive CPU search

A reproducible native C++17 search uses the *proved* condition `0<t<32 => no holes` as a sound pruning gate. It evaluates the actual third-slice holes for only t=0 or t>=32, then searches for a 13-cap in any hole set of size>=13. Every prospective >=237 witness triggers direct independent 7D point-pair arithmetic before acceptance.

Four deterministic jobs each generated 4,000,000 invertible matrices by elementary GL6 row operations, seeds `2026110311`, `...12`, `...13`, `...14`. Per-run distinct matrix counts were 3,954,149 / 3,954,411 / 3,954,593 / 3,954,479. **Sum of per-run unique counts: 15,817,632**, but cross-run duplicates are possible; this is *not* a count of globally unique GL6 elements.

Among the 15,817,632 within-run unique evaluations, 15,659,961 had `0<t<32` and were excluded rigorously by the algebraic lemma. A further 157,671 exceptional t=0 or t>=32 cases were checked by full direct 12,544-sum enumeration, with hole histogram `0:146704, 1:8289, 4:1961, 12:717`. Max holes observed=12, **no observed >=13**. Total of four C++ runs ~30 CPU seconds, no GPU or paid compute, no 237 witness. THIS SAMPLING IS NOT AN EXHAUSTIVE CLASSIFICATION OF GL6 OR A GLOBAL UPPER BOUND.

As a separate independent arithmetic control, C++ directly computed 150,000 additional random relative S-vs-MS pair configurations; no >=13 holes. An independent fresh spectral-pruned replay of 200,000 additional sampled matrices (seed 2026110406, witness path explicitly pinned) found 198,728 within-run distinct invertible matrices, 2,193 expensive hole evaluations after proof-based pruning, max 12 holes, and zero >=13. Its output is included as `spectral_pruned_200k_independent.log`. Its intersection histogram includes t=0,2,..,80,112 and demonstrates why the spectral argument does NOT cover t>=32. A second 200,000-sample exact integer run enumerated hyperplane-avoidance counts for 1,924 examples where |S intersect MS|=32: observed maxima six *projective* normals (12 vectors). This remains **empirical** and cannot be promoted to a theorem; the explicit 14-normal counterexample above shows why extra realizability assumptions matter.

## Remaining root work / decision gate

1. For `112+112+13`, **prove or disprove** an exact universal bound `#(F3^6\(-S-T))<=12` for all affinely equivalent maximal112 pairs by classifying realizable t>=32 intersections under GL6 (using automorphism double cosets or an exact alternative). Reject a merely sampled argument.
2. Even a complete proof of (1) closes ONLY one conditional 237-cap family. Globally complete closure requires either an independently verified >=237 set and matching rigorous upper bound, or a proof-checked UNSAT of the full target237 cover (the existing CAP040 ten dense-hyperplane cases), with a proof of exhaustive coverage.
3. The Z3 and HiGHS global-root attempts from CAP046 remain UNKNOWN due timeouts. No mathematical novelty is claimed for the Fourier Cayley-graph identity until literature is fully checked; related maximal-cap classification and strongly regular Cayley-graph techniques predate this work.
4. CAPSET hourly task remains disabled by explicit user request. No background work or recurring monitor is created.

## Exact reproduction

```bash
python cap047_spectral_112.py > spectral_exact_output.json
# Requires existing repository canonical 236 point fixture in ../capset_closed/witness236.txt
# The C++ sample program is spectral_pruned_237.cpp; uses verified fixture and records seed. For the version in this bundle, the verified witness must be present at the exact source-annotated path (or, in the portable version with a CAPSET_WITNESS environment override, set that variable to the file path).
g++ -std=c++17 -O3 spectral_pruned_237.cpp -o spectral_pruned_237
./spectral_pruned_237 4000000 2026110311
```

Exact CI status: pending until dedicated GitHub branch workflow runs the new Python verifier. Do not confuse checker passing with closing r3(7).

Sources: Potechin, *Maximal caps in AG(6,3)* (2008), DOI 10.1007/s10623-007-9132-z; https://arxiv.org/abs/2206.09804 (Thackeray 2022, upper288 preprint); public n7 status https://cairn-commons.com/problems/cap-sets-dim-7.