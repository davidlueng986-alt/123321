# E070 — R4 direct mathematical attack: exact Gram-PSD forbidden configurations in 3-MOLS(10)

**Date:** 2026-11-07 (UTC+8). **GLOBAL STATUS: OPEN.** **Confirmed complete E064 first-column paratopy classes ruled out: 0 / 1,700.** No full 100/100/100 witness. No LRAT-certified full root-branch UNSAT. This report documents a **new mathematical R4 pruning theorem with actual exact contradiction certificates at deeper partial-OA nodes**, not a claimed resolution or closure percentage.

## Target, and why E069 was insufficient

The target remains **at least one entire E064 first-column class** rigorously `UNSAT`, or a single full verified `SAT` witness (which settles the entire problem). E069's abstract parity/Gram formula outputs do not depend on the canonical `B_col0,C_col0` values and cannot by themselves achieve even 1/1700. The following R4 attack explicitly takes the E064 branch permutations and partial interior tuples as inputs.

## Full 5-coordinate Gram-PSD necessary condition — exact derivation

Assume OA(100,5,10,2) exists. Represent its 100 points by 5-tuples `(r,c,A,B,C)`. Form a **50×100 incidence matrix** `H` whose 50 rows are the 5×10 coordinate-value lines; `H_{line,point}=1` iff that point belongs to that line. Since each line contains 10 points, lines of the same direction are disjoint, and any two lines of different directions intersect at one point,

```
G = H H^T = 10 I_50 + (J_5 - I_5) ⊗ J_10.
```

This **fully specified** matrix `G` has eigenvalue `50` on the global constant subspace (dimension 1), `10` on the class-balanced subspaces (dimension 45), and `0` on class-constant sum-zero subspace (dimension 4). For *any* selected subset `S` of `m` points, its 50×m incidence submatrix `H_S` satisfies

```
H_S H_S^T <= G  in PSD/Loewner order,
```

because `G - H_S H_S^T = H_{S^c} H_{S^c}^T` is PSD. Therefore `I_m - H_S^T G^+ H_S` is PSD, where `G^+` is the Moore–Penrose pseudoinverse. Every column of `H_S` belongs to the image of `G`, since it has exactly one 1 per coordinate-direction block; no kernel caveat is ignored.

For any two distinct OA points, their five tuples share **at most one coordinate**. Write `A_S` for the symmetric adjacency matrix with `(A_S)_{ij}=1` iff `i≠j` and the two tuples share exactly one coordinate; its diagonal is zero. Then the elementary spectral decomposition of `G^+` gives the exact identity

```
H_S^T G^+ H_S = (1/10) (5 I_m + A_S) - (4/100) J_m.
```

Multiplying `I_m - H_S^T G^+ H_S >= 0` by 50 yields the **unconditional necessary theorem**

> **THEOREM E070-R4:** For every point subset of an OA(100,5,10,2),
>
> `Q_S = 25 I_m - 5 A_S + 2 J_m` is positive semidefinite.
>
> Hence for **every integer vector** `v ∈ Z^m`, `v^T Q_S v >= 0`.

No SAT solver, conjectural assertion, or floating point computation is needed to check a *counterexample configuration*: one integer vector with `v^T Q_S v < 0` rigorously excludes every hypothetical full 3-MOLS containing these tuples. For a subset of a known complete 5-net, negative values are impossible. The **theorem is necessary, not sufficient**; a partial tuple set passing PSD might nevertheless be impossible for other reasons.

### The exact certificate: 22-point branch-0 partial assignment

Take E064 canonical branch 0: `B_col0=[0,2,1,4,3,6,5,8,9,7]`, `C_col0=[0,3,4,1,2,7,8,9,5,6]`. Choose **22** point tuples: a subset of the 19 standardized first-row/first-column points and 8 interior points. Every pair of selected five-tuples agrees on at most one coordinate (all pairwise OA constraints pass).

The independent integer certificate in `E070_R4_COMPRESSED_EXACT_CERT_BRANCH0.json` has

```
  25·Σ(v_i²)                 =    999,600
   2·(Σ v_i)²              =     88,200
  -5·Σ_{i≠j, A_ij=1}v_i v_j= -1,087,890
  --------------------------------------
  v^T (25I-5A+2J) v         =        -90
```

All 22 point tuples and all 22 integer components of `v` are stored in the JSON. The checker reconstructs every matrix entry using native Python integer arithmetic, verifies every pairwise coordinate constraint, and verifies the CNF literal mapping. A companion **branch-400** certificate comprises 24 tuples, 42 literals and has integer quadratic `-92`.

For a solver using E065 first-row/A-first-column normalization, the 22-point branch-0 contradiction yields a mathematically sound **38-literal implied clause** forbidding the corresponding set of A/B/C variable assignments. This is not a complete branch-0 exclusion: other interior choices remain possible. It is significantly smaller than E068's 116-literal one-pair cut, though they are different types of partial-pattern obstruction and raw literal length alone does not establish real solver speed-up.

## All eight E064 cycle types: integer certificates, independently verified

`E070_EIGHT_CYCLE_TYPES_EXACT_CUTS.json` stores a separate negative-quadratic certificate for a representative of **each** of E064's eight B-column cycle types. The independent integer verifier `E070_EIGHT_CYCLE_INDEPENDENT_VERIFY.py` checked **8/8** exactly (including all pairwise OA constraints, branch-normalization consistency, negative integer quadratic, and DIMACS variable mapping).

| E064 branch | B-column cycle type | Selected partial points | Implied CNF clause literals | Exact integer `v^T Q v` |
|---:|---|---:|---:|---:|
| 0 | (2,2,2,3) | 22 | 43 | -2 |
| 104 | (2,2,5) | 26 | 54 | -28 |
| 440 | (2,3,4) | 32 | 65 | -18 |
| 833 | (2,7) | 24 | 52 | -8 |
| 1271 | (3,3,3) | 26 | 48 | -27 |
| 1339 | (3,6) | 28 | 59 | -18 |
| 1528 | (4,5) | 22 | 41 | -53 |
| 1588 | (9) | 26 | 50 | -45 |

The separately minimized branch-0 certificate is **38** literals (better than the 43-literal eight-type sample); branch-400 also has **42** literals. **Eight types having local contradictions does not mean eight top-level classes have been eliminated.** Their *other* completions are untested, and no 1/1700 global proof has been completed.

## Real, but bounded, pruning measurement

`E070_PSD_ORACLE_BENCHMARK.json` ran one **fixed-seed random greedy partial-OA path** for each of the eight first-column cycle types. After 19 normalized root points, it selected an increasing number of interior five-tuples, retaining only candidates satisfying all pairwise coordinate restrictions and all previous PSD tests. At selected depths it screened **all** remaining pairwise-compatible candidate placements against the new PSD condition by an eigenvalue/Schur-complement calculation. The local candidate pool always started at **21,249** for the tested branches.

At interior depth **16**, additional candidate rejection by PSD was:

```
branch 0:    1005 / 3373  = 29.80%
branch 104:    73 / 3177  =  2.30%
branch 440:    13 / 3125  =  0.42%
branch 833:   304 / 3117  =  9.75%
branch 1271:  308 / 2704  = 11.39%
branch 1339:  482 / 3104  = 15.53%
branch 1528: 1810 / 3787  = 47.80%
branch 1588:   76 / 2936  =  2.59%
```

At interior depth **20**, rejection ranged **28.30%–92.22%** across these eight paths. At depth 0 or 4 it was zero; at depth 8 it was zero except branch 0's 2/9316. **These are conditional random-path candidate-cut measurements, not the overall SAT speed-up, not a representative population distribution, not proof of full-branch UNSAT, and not a count of solved E064 classes.**

## Soundness / cross-controls / proof pipeline

- `E070_INDEPENDENT_VERIFY.py` independently checks the branch-0 and branch-400 exact integer obstructions and tests complete **order-5 and order-7 5-nets** (three explicit finite-field Latin squares) against the corresponding generalized Gram-PSD identity. Both positive controls pass.
- `E070_EIGHT_CYCLE_INDEPENDENT_VERIFY.py` checks all eight exact integer certificates with **no NumPy, SciPy, floating eigenvalues, or SAT library**.
- `E070_dynamic_oracle.py` first uses fast floating-point eigenvalues to propose a cut, then **requires an exact negative integer vector** before emitting a sound clause. If no exact certificate is found, it reports `NO_PSD_CONTRADICTION_CERTIFIED`, never UNSAT.
- The R4 theorem is a conditional global necessary invariant derived from the full five-coordinate geometry. This paper does **not** invent a new globally established impossibility theorem: it demonstrates proof-producing separation for partial assignments.
- Adding these clauses to a solver preserves satisfiability, but any final global UNSAT proof also requires proof-lifting/independent mathematical checking of every injected lemma. An LRAT proof of augmented CNF alone is not a standalone proof of the *original* formula unless injected cuts are justified.

## Strict 1/1700 proof obligation — not yet met

To certify even one full canonical root branch `i`, we must show **every** full OA satisfying its `B_col0,C_col0` either violates a necessary algebraic condition or leads to a complete independently checked UNSAT proof. The current eight integer certificates exclude **specific partial tuples only**. They do not cover the exponentially many remaining interior choices.

**Next direct R4 attack:** instrument the full normalized 5-dimensional OA exact-cover/SAT search with this **adaptive PSD-separation oracle**, emitting exact checked integer certificates (and corresponding clauses) whenever a partial set becomes spectrally impossible; benchmark branch 0 plus other types against the untouched baseline with identical budgets. Derive stronger group-level cut families and seek an exhaustive 1/1700 proof, not just additional certificates from random paths. Parallel positive search for a full verified 100/100/100 witness remains essential.

**Status:** `OPEN`; full root branches ruled out: **0/1700**; partial R4 certificates: **10** individually integer-checkable examples (eight types plus two optimized; branch0 duplicated as a type but distinct sample), zero full 100/100/100 witnesses. Hourly automations remain disabled.
