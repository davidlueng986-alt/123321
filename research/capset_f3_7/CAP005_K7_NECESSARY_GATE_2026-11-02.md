# CAP-005J — Seven-fiber necessary-gate census (2026-11-02 UTC)

**Scope:** Fixed independently verified Calderbank–Fishburn/Edel 236-point cap B in F_3^7, partitioned by the first three coordinates into 27 four-dimensional fibers. Release **exactly seven** fibers T, retain all original points outside them, and permit arbitrary replacement inside them. This is **not** a global result for r_3(7).

## Exact computational result

- C(27,7) = **888,030** seven-fiber release sets.
- **862,906 / 888,030 = 97.1708163%** rigorously excluded from improving 236 by a necessary outsider-count gate.
- **25,124** remain unresolved by this gate. Do **not** infer feasibility or existence of a 237-cap from this count.
- Maximum individually admissible outsiders: **198**, attained by exactly eight release sets:
  - (0,1,3,5,7,8,18), (0,1,4,5,6,8,18),
  - (0,2,3,4,7,8,18), (0,2,4,5,6,7,18),
  - (9,10,12,14,16,17,18), (9,10,13,14,15,17,18),
  - (9,11,12,13,16,17,18), (9,11,13,14,15,16,18).
  Each has baseline released-fiber occupancy 84, but 198 is only separate-point admissibility, not mutual cap compatibility.
- Sum of admissible outsider counts over all seven-fiber sets: **2,946,160**. Histogram has **98** distinct count values; full JSON produced by CI.
- For 1,951 outsiders, the distinct cross-fiber secant-pair matching-size histogram is
  {1:8, 2:16, 3:64, 4:142, 5:712, 6:297, 7:320, 8:8, 9:384}.

## Mathematical gate and proof scope

Let F_i be the fiber of index 9*x_0 + 3*x_1 + x_2. For an outsider x not in B, a secant is an unordered pair a,b in B with x=-a-b (mod 3). Write f(x) for its fiber index. If f(a)=f(b), then f(x)=f(a); such secants are automatically released when x's fiber is released. For the remaining secants, the unordered endpoint fiber pairs E_x are disjoint (a matching); this property is checked exhaustively from the exact 236 points.

An outsider x can be added while all baseline points outside a seven-fiber set T remain fixed **only if** f(x) is in T and, for every {i,j} in E_x, at least one of i or j is in T.

Let N(T) be the number of outsiders satisfying this necessary condition. The previously independently certified pair-removal lemma for this baseline states: inserting any two outsiders requires deleting at least 16 original points; inserting a single outsider requires at least 10 deletions. Consequently any strict improvement over 236 requires **at least 17 outsiders**. Thus N(T) <= 16 rigorously excludes improvement in that release neighborhood.

This is only a necessary test: outsiders counted by N(T) can conflict with each other, and large N(T) need not yield any cap.

## Two independent exhaustive computations

1. **Incidence enumeration:** cap005_j_k7_gate_incidence.py independently verifies the baseline by direct mod-3 arithmetic, enumerates all outsider secant matchings, and generates exactly the seven-fiber sets admitting each outsider. For a matching with k pairs, the number of incident release sets is

       sum_{t=0}^{6-k} C(k,t) * 2^(k-t) * C(26-2k, 6-k-t).

   Each set has a unique choice (one or both endpoints) for every matching pair, so no duplicate counting. Seven-fiber masks are indexed by combinatorial-number-system rank. Expected and observed incidence totals both equal 2,946,160.
2. **Direct exhaustive checker:** cap005_j_k7_gate_direct.cpp independently reconstructs the baseline and all 27,730 secants, checks every outsider fiber matching, enumerates **all 888,030** seven-fiber masks directly, and tests the outsider condition for each mask without using the incidence generator or its rank function. It separately verifies the full histogram, totals, and all eight maximizing sets.
3. cap005_j_compare.py compares **all 98 histogram bins** and eight maximizers, not just aggregates.

**Reproduction commands (CPU-only, deterministic, no random seed):**

    python research/capset_f3_7/cap005_j_k7_gate_incidence.py --out /tmp/cap005_j_k7_incidence.json
    g++ -O3 -std=c++17 -Wall -Wextra -pedantic research/capset_f3_7/cap005_j_k7_gate_direct.cpp -o /tmp/cap005_j_direct
    /tmp/cap005_j_direct research/capset_f3_7/candidates/calderbank_fishburn_236.txt > /tmp/cap005_j_k7_direct.json
    python research/capset_f3_7/cap005_j_compare.py /tmp/cap005_j_k7_incidence.json /tmp/cap005_j_k7_direct.json

Local execution against independently reconstructed baseline: Python ~5.45 s, C++ ~0.57 s; full histogram comparison PASS. CI must separately reproduce before status becomes CI GREEN. No GPU or paid compute.

## Strategy meta-audit

CAP-005I proved the full <=6 fixed-coordinate-fiber neighborhood has restricted optimum 236. The seven-fiber gate eliminates 97.17% of release sets but leaves **25,124** (including eight with N=198). It cannot by itself rule out all seven-fiber edits and is not a construction strategy. Do not repeat six-fiber work. Prioritize (a) quotient the 25,124 survivors by the verified 16-element affine stabilizer, (b) stronger exact rational LP duals for low-N cases, (c) genuinely nonlocal changes involving many fibers and alternative affine partitions, and (d) globally valid upper-bound certificates. Prefer routes with a plausible path beyond 236 or toward a matching global upper bound.

## Literature/novelty audit (2026-11-02)

Checked the cap-set status page (https://cairn-commons.com/problems/cap-sets-dim-7, dated 2026-10-03), Thackeray's arXiv:2206.09804 (claims exclusion of 289-point caps), and Grace–Voloch *Algebraic Capsets* (Journal of Combinatorial Designs, published 2026-05-21). No independently verified >=237 cap or global matching bound identified in this check. The public page states 236 <= r_3(7) <= 291, with a stronger preprint claim <=288; the latter proof has **not** been independently audited here. Novelty of this restricted seven-fiber census has **not** been established.

**Conclusion:** A new independently reproducible restricted necessary-gate result, not a solution of the exact open problem r_3(7).
