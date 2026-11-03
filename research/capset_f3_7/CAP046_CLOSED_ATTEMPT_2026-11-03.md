# CAP-046 — CLOSED ATTEMPT: Direct global 237-decision and constructive refutation search

**Date:** 2026-11-03 UTC. **Decision:** the user explicitly disabled the hourly capset task. `Cap Set Hourly Research` automation ID `6ae77c6ed4f4819191afec5f9b63437a` was successfully updated to `is_enabled=false`. No recurring task has been created. Research now occurs only when explicitly requested.

## One goal, with two possible proof outcomes

Exact target: determine `r3(7)`, currently open. A **known independently verified cap of 236 points** proves `r3(7)>=236`. To close with value 236 one needs an **independently checked proof that no cap of size 237 exists**. Finding a verified 237-cap would refute the proposed equality 236, but still would not determine exact value without a matching global upper bound. This run deliberately attempted both directions: exact global feasibility and nonlocal construction search. **Neither completed the open problem.**

Latest public status independently rechecked 2026-11-03: https://cairn-commons.com/problems/cap-sets-dim-7 (236<=r3(7)<=291, open, a 2022 preprint claims <=288). Thackeray completion and our CAP019 provisional<=287 remain unreviewed for unconditional claims.

## A. Full seven-dimensional *root-equivalent* global 237-cap MILP — actually executed

Model Boolean point selectors `x_p` on all **2187 points** of F3^7. Exact 796797 affine lines give `x_a+x_b+x_c<=2`. Sound root-preserving affine symmetry: fix 0,e1,...,e7 selected and their 28 forced forbidden secant points excluded; any >=237 cap spans 7D because r3(6)=112. Sound *global* CAP007J moment theorem: any 237-cap has a 6D affine hyperplane containing >=89 points; because r3(5)=45, this hyperplane affinely spans 6D and may be normalized to coordinate `x7=0` with seven frame vertices inside H and one outside. Add `sum x>=237` and `sum_{p in H} x_p>=89`.

Actual SciPy HiGHS sparse matrix: **796799 rows, 2187 binary primary variables, 2393307 nonzeros**. Matrix constructed successfully using independent mod3 integer enumeration, 796797 exact line rows; independent 236-cap checker separately verified the baseline. The first root MILP call returned **no status** before a 60s external execution timeout. A second `timeout -k 3s 22s python -u cap_closed_global_root.py` printed the exact matrix dimensions and exited **124 (timeout)** before any SAT/UNSAT response, despite requesting internal `time_limit=17`. The solver likely did not complete root presolve within that budget. This is **UNKNOWN**, not an UNSAT certificate, not evidence that 237 is impossible. Full comparable source `cap046_closed_root_global_mip.py`.

No expensive GPU/paid compute used. The full root decision remains completely open.

## B. Genuine 237-witness search beyond the 236 baseline — actually executed

Load canonical 236 cap from `candidates/calderbank_fishburn_236.txt` (SHA256 of normalized 236-point newline text: `a32ca7df9d3d82b696773934463af7226a35ce185bd8690620f8a03c58f986ab`); independently verify all 27730 unordered pairs, distinctness and zero 3AP.

Generate nontrivial affine images `g(B)` by random products of GL7 elementary row transformations, plus occasional translation. For each set union `U=B union g(B)`, solve the exact 0-1 cap problem on U (every third point of a chosen pair inside U forbids simultaneous choice of its triple). Since B is always inside U, each union admits a 236-cap; test whether any contains >=237. All solutions returned by HiGHS are direct-rechecked by mod3 arithmetic, not trusted by score.

Deterministic seeds: `20261103` initial ten 300-point pool runs (ten trials, seven distinct transformation matrices); `202611031` 1400-probe nonlocal pool generation.

Results, all *restricted pools* only:

| | overlap | |U| | 3AP hyperedges | solver report | status |
|---|---:|---:|---:|---|---|---|
| first 10 local trials |172|300|832 or 1024|best 236, solver-reported optimum in each|COMPLETE restricted optimum only|
| nonlocal |140|332|1440|236 optimum reported|COMPLETE restricted optimum only|
| nonlocal |133|339|2025|time limit, reported upper244|UNKNOWN for >=237|
| nonlocal |112|360|2652|236 optimum reported, 5.9s|COMPLETE restricted optimum only|
| nonlocal |98|374|2266|time limit, reported upper237|UNKNOWN for >=237|
| nonlocal |72|400|2974|time limit, reported upper251|UNKNOWN for >=237|
| nonlocal |48|424|3782|time limit, reported upper266|UNKNOWN for >=237|
| nonlocal |24|448|4674|time limit, reported upper288|UNKNOWN for >=237|

(Values in “reported upper” are solver floating-point bound diagnostics, NOT rigorous globally certified upper bounds.) The solver did **not** receive 236-point warm starts in timed-out cases; reported incumbents below 236 in those runs are uninformative, because B is already a 236-cap within every pool.

Further **explicit decision** MILP `sum x>=237` reported infeasible for 360-point pool, but does not emit a standalone independently checked UNSAT proof; 448-point pool feasibility timed out after 16s. Neither result proves *global* nonexistence. No verified >=237 cap found. Code: `cap046_closed_affine_union.py`. Stop pursuing mild affine unions without a reason they could cover fundamentally different cap families.

## C. Adversarial exact countermodel against a tempting “instant upper-bound” proof

A hopeful route to `r3(7)<=236` was to take CAP007J's root-necessary 89-point dense-hyperplane result and **force >=90** by combining all 1093 normal-direction second/third moment identities with Type0/Type1 barycenter residue counts and the *full rank/sign value spectrum of a quadratic form* on the 6D hyperplane of Type0 directions.

This route is **falsified at the aggregate level** by a concrete **integer**, not fractional, direction histogram with all slices at most 89:

| sorted 6D slice counts | normal directions |
|---|---:|
| (59,89,89) | 126 |
| (60,88,89) | 129 |
| (71,81,85) | 2 |
| (73,77,87) | 5 |
| (73,80,84) | 1 |
| (75,77,85) | 1 |
| (76,79,82) | 126 |
| (76,80,81) | 297 |
| (78,78,81) | 112 |
| (78,79,80) | 294 |

All rows have sum237. Pure integer audit checks:
- 1093 projective directions.
- `S2=20618289` and `S3=1651763205`, the exact global identities for a hypothetical 237-cap.
- Exactly **729 Type1** normal directions (mod3 slice residues all different).
- Exactly **364 Type0** normal directions with equal residues, split `(N0,N1,N2)=(112,126,126)`.
- These Type0 residue counts are the *exact spectrum of the valid quadratic form* `Q(u)=u1²+...+u6²` on the projective normals in F3^6, checked by enumerating all 3^6-1 nonzero vectors modulo ±.

**This is NOT a 237-cap, nor a realizable hyperplane assignment.** It proves rigorously that *this particular family of aggregate moment/barycenter/quadratic-spectrum necessary conditions is insufficient* to force a 90-point hyperplane, let alone exclude all 237-caps. The absent crucial ingredient is **pointwise geometric coherence across directions**, with the same selected 237 points generating all hyperplane counts. Program `cap046_aggregate_max89_falsifier.py`, entirely standard library and deterministic. Avoid wasting further cycles on aggregate moment refinements unless new pointwise compatibility lemmas are added.

## Audit and conclusion

**CLOSED ATTEMPT OUTCOME: OPEN.** No 237-cap construction, no proof of no 237-cap, no new independently verified global numerical upper bound. The root-complete full 237 feasibility formulation exists, but did not return SAT/UNSAT within CPU budget. Exact 236 witness remains valid.

The hourly automation has been **paused by explicit user request** (confirmed by the automation update response). Do not restart it or create another recurring research task without explicit instruction. No edits to other math branches or MOLS10.

Only defensible next root-closing pathways are (1) genuinely new *pointwise global* cap constraints with a proof bridge to the ten root-exhaustive CAP040H branches, strong enough for independently proof-logged UNSAT, or (2) global nonlocal construction methods yielding actual >=237 points, followed by solving the matching upper bound. Merely finding more unreviewed restricted certificates or running an unbounded CPU solver without completed proof is not closure.

Commands:
```bash
# ROOT full global MILP, explicit OS timeout, truthful UNKNOWN on termination
timeout -k 3s 22s python research/capset_f3_7/cap046_closed_root_global_mip.py --seconds 17

# Root aggregate necessary-constraint falsifier, exact integer calculation
python research/capset_f3_7/cap046_aggregate_max89_falsifier.py

# Nonlocal 237 constructive search in two matched affine pools, bounded
OPENBLAS_NUM_THREADS=1 python research/capset_f3_7/cap046_closed_affine_union.py --buckets 112 96 --seconds 12 --mode feasibility
```

**Novelty not claimed.** These are a deliberately bounded, genuinely goal-first closure attempt and a proof that one tempting aggregate method is insufficient. The exact value r3(7) is still unknown.
