# CAP-007J2 — Fourier self-duality, strongly regular graph, and arbitrary-second-slice identity (2026-11-02)

## Scope and source
The target remains exact r3(7), not merely ≥237. Based on a direct, independently verified canonical 112-cap S in F3^6 extracted from the existing 236 cap. Potechin, *Maximal caps in AG(6,3)*, Designs Codes Cryptogr 46 (2008), proves all 112-caps are affine equivalent (DOI 10.1007/s10623-007-9132-z). No claim of literature novelty or a new global upper bound is made.

## Exact integer identities
The canonical S is centrally symmetric (S=-S), has 112 points and excludes 0. For every z in F3^6, direct integer convolution of all 112² ordered pairs confirms:

* `(1_S*1_S)(0)=112`;
* `(1_S*1_S)(z)=1` for `z ∈ S`;
* `(1_S*1_S)(z)=20` for all other nonzero `z` (616 points).

Thus S is a regular partial difference set. The Cayley graph on F3^6 with adjacency `x ~ y` iff `x-y ∈ S` is **strongly regular with parameters `(729,112,1,20)`**. Graph adjacency and common-neighbor counts follow exactly from the convolution above; no graph package or solver is used.

The unnormalized Fourier transform has an especially simple exact form (for an order-3 character):

```
    F(1_S)(u) = 112    if u = 0,
                -23    if u ∈ S,
                  4    if u ∉ S ∪ {0}.
```

Hence the set of *nonzero high-magnitude Fourier frequencies is exactly S itself*: the canonical 112-cap is Fourier self-dual in this coordinate system. The second canonical 112-cap T also has this identity. For any affine image `S'=M S+t`, the high Fourier support is `M^{-T} S`, itself a 112-cap. Fourier self-duality `H_S=S` need not persist under arbitrary change of coordinates; the structural two-eigenvalue spectrum does.

**Uniqueness of center:** Every 112-cap is an affine image of centrally symmetric S and has at least one reflection center. If it had two, their composition would be a nonzero translation preserving the set, forcing its cardinality divisible by 3, impossible for 112. Thus the center is unique. This provides a canonical affine normalization for all maximal 112-slices; it does not impose a restriction on a hypothetical seven-dimensional cap with no 112-slice.

## Formula extending beyond two maximal slices
Fix a centered 112-cap S and let `H_S` be its 112 nonzero Fourier high frequencies (equal to S in the canonical basis). For **any** subset T of F3^6, with `m=|T|`, exact Parseval gives

```
E(S,T) = [ (112² - 16)m² + 16·729·m
           + 513 ∑_{u∈H_S} |F(1_T)(u)|² ] / 729.
```

The second slice T is *not required* to have 112 points or even to be a cap. This generalizes CAP-007J's `E(S,T)=218624+361k` identity for two maximal 112-caps. The formula can be applied to 112+111+14, 112+110+15 etc. conditional branches without presupposing two full maximal slices. It is not yet a nontrivial upper bound on r3(7); use it together with cap-specific constraints to bound sumset support.

## Independent exact tests

```
python research/capset_f3_7/cap007j_strongly_regular.py
python -m unittest discover -s research/capset_f3_7 -p 'test_cap007j_strongly_regular.py' -v
```

Tests: exact full convolution for BOTH canonical 112 caps, all 729 ternary characters with exact integer phases, graph parameters and a separate direct additive-energy check on second-slice cardinalities 32,80,100,110,111,112 (all PASS; ~0.93s on local CPU). No randomness, GPU, paid compute or optimizer. GitHub CI pending; the arithmetic identity is independently derivable from the displayed convolution certificate.

## Research strategy

1. CAP-007K: reduce relative 112-cap alignment search using stabilizer double cosets and center normalization (not naive full GL6 enumeration). Determine if any pair of maximal 112-caps has ≥13 unused cross-slice sums; if yes, check whether 13 form a cap; if no, prove exact conditional 112+112 slice upper 236 with independently checked exhaustive certificate.
2. CAP-007L: strengthen energy-only bounds by cap-specific constraints, higher Fourier moments, and phase-sensitive convolution. Exact energies alone do not pin down support (CAP-007J found k=32 with either 4 or 12 holes).
3. CAP-007M: incorporate arbitrary T spectral identity into conditional 112+111+14 etc SAT/SDP cuts, retaining proof-logged validation.
4. CAP-007N: solve or cut down global cases in which every six-dimensional hyperplane contains ≤111 cap points. None of the 112-anchored results address them.

Do not mark the global cap-set problem solved without independently reviewed matching lower and upper bounds. Preserve failed experiments and continue research automation.

## CAP-007J3 direct graph-edge form of arbitrary-second-slice energy (2026-11-02T11:12:52.892Z)

A useful stronger *interpretation* of the displayed universal spectral identity follows without any Fourier calculation beyond the already independently verified regular partial difference set. Let G be the Cayley SRG(729,112,1,20) whose connection set is the centered maximal 112-cap S, let T be ANY subset with m points, and let e_G(T) count the unordered pairs of points in T adjacent in G. Because the difference-multiplicity in S is 112 at zero, 1 on S, 20 elsewhere, directly summing over ordered differences of T yields

```
E(S,T) = 112*m + 2*e_G(T) + 20*(m*(m-1)-2*e_G(T))
       = 20*m*m + 92*m - 38*e_G(T).
```

**This exact identity applies to arbitrary T**, not only another maximal cap, and is useful for converting Fourier/sumset constraints into simple induced-subgraph edge constraints. Local exact direct integer tests using the standard S and T equal to the first m elements of the known second 112-cap give:

| m | e_G(T) | E(S,T) |
|---:|---:|---:|
| 32 | 16 | 22,816 |
| 80 | 400 | 120,160 |
| 100 | 640 | 184,880 |
| 110 | 784 | 222,328 |
| 111 | 800 | 226,232 |
| 112 | 816 | 230,176 |

All E values match independently enumerated 112*m ordered sums and the Fourier formula. For T a maximal 112-cap, combining E=218624+361*k gives **2e_G(T)=2240-19*k** (k even). This is a discrete structural constraint; alone it does NOT bound the third-slice complement tightly enough to exclude 237. Next priority is graph+cap joint inequalities and phase-sensitive support, not optimizing E in isolation. Novelty unestablished.
