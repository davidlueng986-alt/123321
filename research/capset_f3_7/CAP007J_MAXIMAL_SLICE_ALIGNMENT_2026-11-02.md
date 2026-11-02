# CAP-007J — Maximal-six-dimensional-slice structural audit (2026-11-02)

## Problem and research priority

The exact r_3(7) remains OPEN. Public 2026-10-03 status: published 236 <= r_3(7) <=291; Thackeray's 2022 preprint arXiv:2206.09804 claims <=288 but its entire proof has not been independently checked in this project. This iteration does not claim a new 237-point cap or a better global upper bound.

This iteration attacks a **broader conditional subproblem**, not an edit radius around a fixed 236-cap: if two parallel six-dimensional affine hyperplanes each contain a maximal 112-cap S and T, how many third-slice points can avoid all cross-slice collinear triples? Potechin (2008, DOI 10.1007/s10623-007-9132-z) proved that all 112-caps in AG(6,3) are affinely equivalent. Therefore, after fixing one canonical S, the second T ranges over all affine linear transforms of a canonical 112-cap. We exhaust a small explicitly defined linear-transform neighborhood and prove new, universally applicable Fourier identities, but **do not exhaust GL(6,3)**.

## Fourier-energy structural lemma (valid for any two 112-caps, conditional on Potechin's uniqueness theorem)

Let S,T be arbitrary 112-point caps in F_3^6, and let F_S(u) = sum_{s in S} omega^{<u,s>}, where omega^3=1 and omega !=1. Exact arithmetic on the canonical 112 cap gives the following two-level nonzero Fourier spectrum:

- precisely 112 nonzero u have |F_S(u)|^2=529;
- precisely 616 nonzero u have |F_S(u)|^2=16;
- at u=0, |F_S(0)|^2=112^2.

By Potechin affine uniqueness, this multiset of Fourier magnitudes applies to **every** maximal 112-cap. Define H_S and H_T as the 112-element sets of nonzero frequencies at which magnitude squared is 529, and k=|H_S intersection H_T|. Then by exact convolution Parseval:

E(S,T) := #{(s,t,s',t') in S x T x S x T : s+t=s'+t'}
 = [112^4 + 728*16^2 + 2*112*16*513 + k*(513)^2]/729
 = **218624 + 361*k**.

The identity is a general theorem about any pair of maximal 112-caps, not merely the local orbit family. Its novelty in the literature has NOT been established. Since the third affine slice must avoid -(S+T), the number q of individually available points satisfies the Cauchy support inequality:

q <= 729 - 112^4 / (218624 + 361*k).

For example, q>=13 is impossible if k<=3. Thus a 237-cap with two 112-point parallel slices requires k>=4 (an extremely weak necessary condition). This is NOT a new 237 exclusion or a 236 global bound. All computations here use exact integer arithmetic; Python test independently computes additive energies for 5 matrices rather than trusting the Fourier formula.

## Exact affine-translation reduction

Let E(S,T)=F_3^6 \ (-S-T) denote the third-slice candidate set. For any translation t in F_3^6,

E(S,T+t) = E(S,T)-t.

Therefore translating only T changes neither |E| nor its cap-packing number. There is no need to search 729 different translations for each relative linear transform. Unit tests compare the explicitly enumerated candidate sets for four translations. This equivalence is mathematical, not a sampling observation.

## Exhaustive, finite linear-neighborhood experiment

Fix the canonical 112-point S and complementary 112-point T from the known 236 cap. Let G be the set of 81 nonidentity elementary GL(6,3) coordinate operations: 6 sign multiplications, 15 coordinate swaps and 60 elementary shears (two nonzero multipliers for each ordered pair of coordinates). Include identity and all products of at most two operations. There are exactly **3812 distinct 6x6 matrices** (deduplicated by all 36 F3 coefficients).

For every matrix M in this finite family we compute E(S,M T) from all 112x112 cross-slice pair sums. Exact census:

| |E| | distinct matrices |
|---|---:|
| 0 | 3505 |
| 1 | 126 |
| 4 | 60 |
| 12 | 121 |

Total 3812. Every one of the 121 twelve-point candidate sets is independently checked to be a cap. Thus the restricted family of 7D caps with a fixed 112-slice S, an entire 112-slice M T and an arbitrary third slice has **maximum 112+112+12=236**. This is a rigorous finite restricted optimum, NOT a bound on every affine equivalence class of a 112+112 cap pair. Outside this finite neighborhood, a 237-point construction may still exist.

The exact Fourier-heavy intersection k vs available q histogram within this family is:

- k=0: q=1 (126 transforms)
- k=8,12,16,20,64,80: q=0 (240,1440,1020,720,15,70 respectively)
- k=32: q=4 (60 transforms), or q=12 (121 transforms)

This refutes using the additive-energy/Fourier overlap k alone as a sufficient test for 13 available points: even k=80 does not guarantee a single hole. Stronger phase-sensitive correlations and the full support indicator of the convolution are needed.

## Reproduction and independent verification

No GPU, cloud or paid compute; no randomization in the certified finite census. The named fixture is the repo's verified `candidates/calderbank_fishburn_236.txt`, not an unobserved external dataset. Commands:

```bash
python research/capset_f3_7/cap007j_112_alignment.py --out /tmp/cap007j_results.json
python -m unittest discover -s research/capset_f3_7 -p 'test_cap007j_112_alignment.py' -v
```

Local output: `3812` matrices, hole histogram `{0:3505, 1:126, 4:60, 12:121}`, Fourier spectrum `{16:616, 529:112}` for each canonical cap, 121 cap-valid hole sets; 3 independent arithmetic/translation unit tests passed in 12.144 seconds. No SAT/UNSAT proof is inferred. GitHub CI state must be checked separately before tagging CI GREEN.

## Meta-audit and prioritized next hypotheses

1. **CAP-007K [P0]: double-coset reduction of all relative 112-cap alignments.** Factor left stabilizer of fixed S and right stabilizer of canonical T before enumerating GL(6,3); to prove q<=12 for ALL pair alignments, provide complete double-coset coverage or an independent global proof, not random sampling. An exhaustive 3812-element local region is insufficient.
2. **CAP-007L [P0]: exploit exact two-level Fourier spectrum and phase-sensitive convolution supports.** Try stronger exact moment/SDP or classification-based inequalities for q<=12; test on orientations with k=32 but q in {4,12} and k=80,q=0. Do not treat energy as a proxy for support.
3. **CAP-007M [P0]: exclude or discover target237 in conditional 112+112+t>=13 case**, without assuming one of the 112 caps has a special relative orientation. If solved, conditional CAP-007H still requires handling 112+111+14, 112+110+15, and all other slice sizes. Even full conditional 112-hyperplane UNSAT would NOT solve global n7.
4. **CAP-007N [P0]: global cap hyperplanes all <=111.** This branch is untouched by any 112-anchored certificate; develop globally valid constraints and proof-logged SAT tests.
5. **CAP-008 [P1]: independent statement audit.** Affine uniqueness relies on Potechin's published theorem; code checks the spectral facts for canonical representatives. Re-run fresh integer convolution and affine covariance on at least two independent implementations before publication claims.

Original problem unchanged: find *matching independently reviewed lower and upper bounds* for exact r_3(7), not only a 237-point cap. Maintain hourly campaign and dedicated-branch governance.
