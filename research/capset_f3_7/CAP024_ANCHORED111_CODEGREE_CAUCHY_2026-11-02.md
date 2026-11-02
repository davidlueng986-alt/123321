# CAP-024 — Exact anchored-111 cross-layer codegrees and a pointwise necessary cut
**2026-11-02 19:00 UTC · deterministic CPU-only · 5/5 local tests PASS; independent JS replay PASS · GitHub CI pending**

## Continuity, motivation and scope
Read the dedicated Drive Ledger/folder, GitHub STATE/LOG/BACKLOG, recent commits and CI. CAP-023 final commit `fe8878748` has full **SUCCESS** run 41496869032. CAP-023's four 287-point 3×3 count-only models were not cap sets; the next useful layer is **pointwise cross-layer geometry**, not more aggregate line-count constraints. Current public status remains open: published 291 upper, Thackeray 2022 preprint 288, internal CAP-019 candidate 287 subject to hostile referee. No new ≥237 witness or global numerical bound in this step.

## Exact graph codegree theorem
Let H be the canonical centered 112-cap in F₃⁶, p∈H, and A=H\\{p} be the anchored 111-cap. Define the forbidden bipartite graph G_A with two copies of F₃⁶, edge x—y iff −x−y∈A. Each side has 729 vertices, degree 111 and 80,919 edges. For distinct left vertices x,x+t, the number of common forbidden right neighbors is
```
κ_A(t) = |A ∩ (A+t)|, t != 0.
```
Independent integer enumeration of all 728 nonzero t finds the **exact codegree histogram**
```
κ_A=0: 2 differences; κ_A=1: 110; κ_A=19: 220; κ_A=20: 396.
```
A direct second implementation forms explicit right-neighbor sets and intersects them for **all 728 differences**; results agree. Independent Node.js implementation uses a different point encoding and deletes a *different* anchor point; its histogram also agrees.

The histogram has an elementary derivation: for centered H, κ_H(t)=1 at 112 differences t∈H and 20 at the remaining 616 nonzero t (the classical Games-graph autocorrelation, independently checked). Removing p gives
```
κ_A(t) = κ_H(t) − 1[p+t∈H] − 1[p−t∈H].
```
The two indicators cannot both be 1, since p−t,p,p+t would be three collinear H points. Exactly 222 distinct differences ±(q−p), q∈H\\{p}, lose one count; precisely ±p lie in H, and 220 lie outside H. This proves the stated distribution for **any** p and, via affine uniqueness/completion, conditionally for all 111-anchors.

Each four-cycle of G_A is specified by an unordered left pair and an unordered common-neighbor right pair. Therefore
```
#C4(G_A) = (729/2) Σ_{t≠0} binom(κ_A(t),2) = 41,137,470.
```
For H112 the corresponding count is 42,661,080; deleting one anchor point destroys **1,523,610 four-cycles**. These are exact graph integrity fingerprints, not an independent bound on r₃(7).

## New necessary pointwise inequality for anchored-111 SAT
Let B and C be chosen external-layer subsets of sizes b,c, with **no** forbidden cross edge between them. For each right vertex y define D(y)=|{x∈B:(x,y)∈G_A}|. Then D(y)=0 for y∈C, ΣD=111b, and
```
Σ_y D(y)^2 = 111b + 2 Σ_{unordered {x,x'}⊂B} κ_A(x−x').
```
By Cauchy–Schwarz on the at most 729−c nonzero positions of D,
```
(111b)^2 ≤ (729−c) [111b + 40*binom(b,2) − 2*E(B)],
E(B)=Σ_{x<x' in B}(20−κ_A(x−x')).
```
Hence the exact **integer necessary cut**
```
E(B) ≤ floor((111b + 40*binom(b,2) − ceil((111b)^2/(729−c)))/2).
```
For the balanced anchored-111 target287 branch b=c=88, this yields **E(B)≤7,018**. Each pair whose difference lies in H112 has κ_A≤1, so there can be **at most 369 such pairs** among B. The same bound applies after swapping the two external layers. For arbitrary target287 with b+c≥176, choose a 176-point subset; since each external slice has ≤112, the exact-size cases have 64≤b≤112 and c=176−b. The machine-readable certificate records all 49 integer cuts. This is a **necessary, not sufficient** inequality; no 287-cap exclusion follows yet. It is a candidate proof-preserving quadratic/pseudo-Boolean strengthening for SAT or CP-SAT, not an UNSAT certificate.

## Reproduction and falsification
```bash
python -m unittest discover -s research/capset_f3_7 -p 'test_cap024_anchored111_codegrees.py' -v
```
Standalone local script: **5/5 PASS, 0.271 s**; independent expanded Python 5/5 PASS, 0.466 s; independent Node.js integer implementation PASS with a different p. No randomness/seed, GPU, solver or paid compute. The known 235-point anchored111 witness (112+111+12) passes cross-free and the new cut, with exact E(B)=17,420≤22,757. A deliberately forbidden edge fails the independent graph check. The four CAP-023 formal integer grids are not promoted to caps or proof certificates.

## Meta-audit and literature
The H112 autocorrelation is related to the **known Games graph**, so neither the codegree computation nor the simple Cauchy inequality is claimed to be new in literature. References: Potechin (2008), DOI 10.1007/s10623-007-9132-z; Thackeray (2022 preprint) arXiv:2206.09804; 2026-10-03 Cairn Commons dimension-seven status. A targeted 2026-11-02 search found no confirmed global 287 publication; absence of search results is not proof of novelty.

Next: test whether these exact pairwise cuts materially strengthen CAP-023 solver relaxations, without claiming exclusion unless proof-logged; independently referee CAP-017B/110-completion and CAP-019; maintain balanced/no-111 and ≥237 construction branches. The exact value r₃(7) remains **OPEN**.
