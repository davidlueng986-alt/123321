# E041 — Exact new non-isotopic 22-cell forbidden partial pattern
**UTC 2026-11-02 16:49–16:52; GLOBAL STATUS OPEN.** No 100/100/100 triple or unrestricted nonexistence certificate. **0 / 162,959** full (f,g) symmetry orbits excluded.

## Sources read / freshness
Read the living [Google Docs journal](https://docs.google.com/document/d/1NDPWEMM3Cf5HrhdOcV6pVE9tCI-kxKbavxcfIBFva3k/edit), [STATE.json](STATE.json), [E040 report](E040_REPORT.md), [E040 exact certificates](E040_EXACT_MINIMAL_CORES.json), [E040 verifier](E040_verify_public.js), [E033 orbit enumeration](E033_RESULTS.json), and E039 report. Primary sources checked 2026-11-02: [Bright–Keita–Stevens, EJC 33(1), P1.30, published 2026-02-13](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30) and [Barnoff–Bright, arXiv:2605.02132v2, revised 2026-07-04](https://arxiv.org/abs/2605.02132). Targeted searches found no independently checkable unrestricted solution; search absence is not proof.

## Falsifiable subproblem
E040 proved its 23-cell pattern minimum **for a fixed dual** among subsets of its 40 source cells, not for all duals. Test all one-cell deletions under the full six-resource-class fractional exact-cover relaxation, then demand a new *integer* Farkas certificate for any remaining infeasible subset.

## Bounded actual computation and negative evidence
For each E040 motif (21/22/23 fixed cells), remove each fixed cell in turn. Rebuild six classes of remaining resources: P_AB, P_AC, P_BC, C_A, C_B, C_C (600 total). Enumerate all 10,000 column/symbol-triple placements, construct the sparse incidence matrix, and run SciPy HiGHS LP feasibility. **66 deletion tests + 3 original-core controls** (CPU, no GPU). Results:
- E040 21-cell core: **21/21** deletion LPs numerically feasible; original infeasible.
- E040 22-cell core: **22/22** deletion LPs numerically feasible; original infeasible.
- E040 23-cell core: **22/23** deletion LPs numerically feasible; deleting **zero-based row-major cell index 27** remains infeasible; original infeasible.

The 65 feasible outcomes have small numerical residuals but **no independently verified rational primal certificates**. Do not promote them to exact mathematical statements. The single infeasible outcome was upgraded to an exact integer dual, as below.

## New exact result
From the 23-cell E040 motif #2, delete cell 27. A second LP minimizing L1 norm of a normalized dual found **seven nonzero integer weights**:
```
+P_AC(1,6) +P_AC(9,6) +P_BC(8,6) +C_A(9,8)
-C_C(3,6) -C_C(7,6) -C_C(9,6)
```
For the new **22 fully specified cells**, exact independent integer-only verification proves uncovered RHS **+1**, **2,596** allowed residual placements, and maximum allowed placement dual score **0**. Summing inequalities over a hypothetical completion gives 1 <= 0, impossible. There are **293** positive-score placements in the unrestricted 10,000 placement universe, all blocked by the 22-cell pattern. Each retained cell has a positive-score placement conflicting with **exactly that one** retained cell, giving 22 explicit singleton witnesses and fixed-dual deletion minimality.

The [certificate](E041_NEW_22_SPARSE_CERTIFICATE.json) contains the 3×4×10 source prefix, the 22 cell indices, seven weights and 22 witnesses. Run `node E041_verify.js E041_NEW_22_SPARSE_CERTIFICATE.json` to independently reconstruct all 10,000 placements, check Latin/overlay source validity, exact Farkas inequality, singleton witnesses and a deliberate corruption rejection. **PASS**. Separately, 100 deterministic random row/column/independent-symbol isotopies were checked over 10,000 placements each (**1,000,000 exact placement checks**, PASS); this is a regression test, not an orbit-complete enumeration.

## Why this is a genuinely new local pattern
E040's earlier 22-cell core occupies **10 columns**; this new 22-cell core occupies **9**. Occupied-column count is invariant under row/column/symbol isotopies and permutations of the three squares, so these two 22-cell patterns are not isotopic. E040's 21-cell pattern also occupies 10 columns, so cannot be contained in the new 9-column pattern under those symmetries. The new 22-cell pattern strictly strengthens E040's source 23-cell nogood. However, a full six-class LP at the same node would already detect the obstruction, so incremental runtime benefit remains unmeasured.

## Reproduce / limitations / next
Run `python E041_lp_minimality.py` (SciPy + NumPy), `node E041_verify.js E041_NEW_22_SPARSE_CERTIFICATE.json`. Full local ZIP with numerical logs, source scripts, exact certificate and isotopy regression was clean-extracted and replayed; SHA256 `1732120a6dc18bd3c33767779ca38c989afe84e6fa8b2a9aa7b6feb97492ce3d`. The 22-cell forbidden-pattern theorem is **restricted**, not a global orbit exclusion, and no publication novelty is claimed. The 65 numerical LP-feasible deletions lack exact primal replay. Next: benchmark isotopy-aware nogood marginal cuts against E040 and E039 projected LP, then prioritize symmetry-complete proof-producing search if gain is negligible. Any complete triple must be independently verified as 100/100/100.
