# CAP-004G — Exact full order-24-invariant optimum is 236 (CPU finite enumeration)

**Date:** 2026-11-01 UTC. **Scope:** only the specific order-24 subgroup acting on the six trailing coordinates defined in CAP-004D. **Status at creation:** local independent CPU computation PASS; dedicated GitHub CI triggered by commit and awaiting verification. **Global** \(r_3(7)\) **remains OPEN.**

## Exact mathematical reduction

Continue from CAP-004F's verified 45 orbit partition, 3,556 within-slice forbidden orbit masks and 11,434 cap-valid single-slice orbit unions. Let \(V\) denote this **complete** family of valid orbit masks, each with exact point weight \(w(M)\). Let \(S(i,j)\) be the bitmask of all orbits containing a point \(-a-b\), for \(a\in O_i,b\in O_j\). For masks \(A,B\), their forbidden third-slice orbit mask is
\[
F(A,B)=\bigcup_{i\in A,j\in B}S(i,j).
\]
A valid third-slice mask \(C\in V\) completes a 7D cap iff \(C\cap F(A,B)=\varnothing\).

Every permutation of the three first-coordinate slices is induced by an affine bijection of \(\mathbb F_3\). Thus we may order their weights \(w(A)\ge w(B)\ge w(C)\). A hypothetical cap of size at least 237 must have \(w(A)+2w(B)\ge237\), and the third slice must satisfy
\[
237-w(A)-w(B)\le w(C)\le w(B).
\]
This gives a **complete safe pruning rule**, not a heuristic.

For each pair of masks \(A,B\) in descending-weight order, with \(A\)'s index no greater than \(B\)'s, the checker constructs a bitset of **all** valid third-slice masks whose weights lie in the required interval. It intersects that bitset with the complements of the precomputed incidence bitsets for every forbidden orbit in \(F(A,B)\). A nonempty result would yield an explicit >=237 witness. An empty result for every eligible pair is an exhaustive exclusion.

## Measured finite computation

- Six-dimensional orbits: **45**; valid single-slice masks: **11,434**; maximum single-slice size: **112**.
- All unordered first/second slice pairs mathematically covered: **65,373,895**.
- Pairs visited including the first failing weight gate per outer iteration: **3,436,063**.
- Pairs passing the safe \(w(A)+2w(B)\ge237\) gate and checked by exact cross-shadow bitsets: **3,424,629**.
- Result: **no third slice of sufficient weight** for any eligible pair.
- Lower witness: the known order-120-invariant 236-point cap, also invariant under this order-24 subgroup, independently reconstructed and checked by direct coordinate arithmetic.
- Therefore the exact optimum in **this full order-24-invariant family** is **236**.

The local scratch run was deterministic CPU-only C++17 (-O3), about **14.0 seconds** for the exhaustive pair checker after a Python orbit-data generation step (~1.5 seconds); no random seed, GPU, paid compute, SAT solver or heuristic stopping rule. The C++ computation is a finite exhaustive proof **conditional on correct program semantics and verified input generation**; CI replay and external independent review are separate confidence levels.

## Durable replay / independent checks

From the repository root:

```bash
python research/capset_f3_7/c6_order24_full_exact_data.py --out /tmp/capset24_data.txt
g++ -std=c++17 -O3 research/capset_f3_7/c6_order24_full_exact.cpp -o /tmp/capset24_checker
/tmp/capset24_checker /tmp/capset24_data.txt
python -m unittest discover -s research/capset_f3_7 -p 'test_c6_order24_full_exact.py' -v
```

The Python generator independently enumerates all within-slice forbidden triples from exact mod-3 arithmetic, checks 11,434 valid masks, builds the complete orbit cross-shadow, and replays the known 236 witness using the separately implemented \`verify_capset.verify\` coordinate checker. The C++ program checks all potential >=237 ordered-by-size triples. The unit test compiles and reruns it on GitHub Actions, checks all enumeration counts and the lower witness. The earlier CAP-004F SAT encoding is an independent formulation but has **not** been solved by a SAT solver; do not label it SAT-UNSAT certified.

## Meta-audit / strategy

This exhausts **one specific 24-element symmetry family**. Further SAT solving of exactly the same order-24-invariant 237 CNF is now redundant for mathematical discovery (unless used as independent certification). In particular, no >=237 set can retain this subgroup symmetry, and no larger global upper bound follows. Pivot CAP-005B to genuinely non-invariant 27-block affine twists / lower-symmetry orbit partitions, while retaining global upper-bound certification as a separate line. Novelty relative to mathematical literature is **not established**; do not claim a publication-level new theorem or a global solution.

## External status recheck

The public dimension-seven problem status page (dated 2026-10-03) still reports \(236\le r_3(7)\le291\), while Thackeray's 2022 preprint arXiv:2206.09804 states that no 289-point 7D cap exists (a proposed upper bound of 288). Neither the preprint's full proof nor the novelty of this subgroup enumeration was independently reviewed in this run. The exact global value is still unknown.

Sources: https://cairn-commons.com/problems/cap-sets-dim-7 ; https://arxiv.org/abs/2206.09804 .
