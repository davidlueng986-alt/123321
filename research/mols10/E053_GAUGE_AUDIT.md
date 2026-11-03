# E053 | 2026-11-03 UTC | Six-class dual gauge compression audit

Status OPEN. Primary-source check: https://arxiv.org/abs/2503.10504 and https://arxiv.org/abs/2605.02132; no independently inspectable unrestricted solution found in targeted fresh search.

**Objective.** E052 reports seven dense 360/360 integer Farkas vectors. Investigate whether coefficient density is partly a coordinate/gauge artifact before spending CPU on new LPs.

**Exact lemma.** Six residual demand classes have equal size 60; every legal placement uses one demand from each class. For any integer vector c=(c_0,...,c_5) with sum(c)=0, set y'_{k,j}=y_{k,j}-c_k. For each placement t, sum_{d in t} y'_d=sum_{d in t} y_d. Also sum_d y'_d=sum_d y_d-60 sum(c)=sum_d y_d. Consequently a Farkas certificate remains exactly valid under this five-dimensional integer gauge. This lemma is unconditional for the specified six-class incidence structure, but says nothing about global 3-MOLS(10).

**Bounded computation.** Deterministic JavaScript generated 1200 synthetic six-class placements and a 360-component integer vector, applied c=[13,-7,4,0,-10,0]. All 1200 placement scores and RHS were exactly invariant; nonzero count changed 347 -> 341. This is a unit test of the algebra, NOT a test of E051's missing actual vectors and NOT a new fixed-prefix exclusion. No solver/GPU cost.

**New falsifiable compression target.** For each class k let f_k(v) be frequency of weight v. Find integer shifts c_k maximizing sum_k f_k(c_k) subject to sum_k c_k=0. This is a small dynamic program over observed weights (with zero-count baseline); revalidate every legal placement with independent integer-only checker. Independent per-class modes may violate sum(c)=0 and are NOT automatically sound. No guarantee sparse certificate exists.

**Failures/limitations.** Actual E051 JSON/generator are still not in GitHub; local container/Python runtime returned ConnectionError, preventing application to actual E051 vectors. Synthetic result must not be counted as certificate progress. Global orbit exclusions remain 0. Earlier E052 gcd=1 observation does not preclude gauge compression.

**Next.** Restore E051 data to GitHub, apply gauge-constrained DP to seven actual duals, verify with independent checker, and resume remaining E049 LP screens. No resolution.

# E053 — Exact gauge symmetry for six-class residual Farkas duals
# Each legal placement covers exactly one demand in each of six classes.
# Each class has 60 demands for an order-10 four-row prefix.
# For integer shifts c[0..5] with sum(c)=0, define y'[k,j]=y[k,j]-c[k].
# Every placement score changes by -sum(c)=0.
# RHS sum(y')=sum(y)-60*sum(c)=sum(y).
# Thus exact certificate validity is invariant under this 5-dimensional integer gauge.
# Sparse compression is an integer optimization: maximize sum_k frequency_k(c_k)
# subject to sum_k c_k=0. Do NOT claim that choosing independent modes works.
# Test E053: deterministic 1200 synthetic legal six-class placements, y=360 integers,
# c=[13,-7,4,0,-10,0]; score and RHS invariance PASS (1200/1200).
# Nonzero counts 347 -> 341; this is synthetic, NOT an E051 certificate test.
# Follow-up: load actual E051 360-weight vectors, solve constrained mode DP,
# verify all original placements, and publish code/data + CI.