# E040 — Exact 21/22/23-cell forbidden partial patterns (2026-11-02 15:50–16:00 UTC)

**Global status: OPEN.** No verified complete 100/100/100 triple; no unrestricted nonexistence certificate. **0/162959 complete (f,g) symmetry orbits excluded.**

## Literature check
Primary sources: [Bright–Keita–Stevens, EJC 33(1), P1.30, published 2026-02-13](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30); [Barnoff–Bright, arXiv:2605.02132v2, revised 2026-07-04](https://arxiv.org/abs/2605.02132). Fresh 2026-11-02 targeted searches did not locate an independently checkable unrestricted solution. Absence of search hits is not proof.

## Falsifiable question
E039 certified 516 **40-cell fixed four-row prefixes** as nonextendable, including sparse integer Farkas duals. Can a *strict subset* of the 40 fully specified whole-cell triples still be certified nonextendable by the same dual? Can its exact minimum be certified without trusting MILP?

## Sound lemma
Let F be fully specified cells of three partial order-10 Latin squares with distinct resources. Resources are the three ordered-pair classes P_AB/P_AC/P_BC and three column-symbol classes C_A/C_B/C_C. A completion must use each resource exactly once. Let U(F) be resources already used by F. A remaining candidate placement (c,a,b,d) is **allowed** if none of its six resources is in U(F). If an integer vector y on resources satisfies (i) sum_{e not in U(F)} y_e > 0 and (ii) for every allowed candidate t, sum_{e in t} y_e <= 0, then **no full triple can extend F**. Indeed, summing the candidate inequalities over all remaining cells contradicts the positive sum over uncovered resources. This ignores remaining row-permutation constraints, so it is a sound relaxation.

## New exact results
Exploratory minimum hitting-set MILP on 46 E039 sparse duals (source `E039_SPARSE_EXTRA.json` in E039 archive) identified three especially compact cores. For these three, a **separate exact combinatorial minimality certificate** was independently checked:

| Cycle type / source prefix | Dual support | Source cells | Certified forbidden core | Positive-weight candidates (all 10,000 placements) | Allowed residual candidates |
|---|---:|---:|---:|---:|---:|
| (2,2,6) / 3 | 9 | 40 | **21** | 400 | 2696 |
| (2,2,6) / 2 | 5 | 40 | **22** | 260 | 2449 |
| (2,2,6) / 4 | 5 | 40 | **23** | 250 | 2427 |

For each core, the exact dual residual RHS is **+1**, and every compatible candidate has dual weight <=0 (maximum 0). Therefore each **21/22/23-cell partial pattern itself** is impossible inside any full 3-MOLS(10).

**Exact minimum/uniqueness, precisely scoped:** For every cell j in each core, an explicit positive-weight candidate t_j conflicts with **exactly that one** cell among the original 40 cells. Any subset of those 40 that blocks all positive candidates must contain j. The selected core blocks every positive candidate. Hence it is the **unique minimum blocker for this fixed dual among subsets of the original 40 cells**, *not* the globally smallest forbidden pattern across all duals/prefixes.

## Independent verification
Public [three certificates](E040_EXACT_MINIMAL_CORES.json) contain the original 3×4×10 prefix, dual weights, selected 21/22/23 cells, and 66 singleton-conflict forcing witnesses. Run `node E040_verify_public.js E040_EXACT_MINIMAL_CORES.json`. Independent integer-only Node.js reconstructs all 10,000 possible column/triple placements for each case, verifies source Latin/overlay validity, every positive candidate is blocked, all 66 singleton witnesses, the positive dual RHS, residual counts and nonpositive candidate weights, plus corruption rejection. **3/3 PASS**. Full Python exploratory source, 46-case scan, and a second independent JS verifier were also clean-replayed locally in `E040_MOLS10_RESEARCH_BUNDLE.zip`.

## Failures and uncertainty
Among the 46 exploratory fixed duals, many needed 25–40 cells; minimum observed was 21. Solver-reported optimum for the other 43 cases is not independently proof-certified. All three certified patterns come from one f cycle type, and none excludes a whole global (f,g) orbit. No claim of publication novelty. The local ZIP was generated and SHA256 clean-replayed; **Google Drive binary upload failed with CONTAINER_SESSION_EXPIRED**, so do not claim it is stored in Drive.

## Next action
Canonicalize the 21-cell forbidden pattern under valid isotopies/paratopies and test **actual incremental pruning** against the symmetry-complete E033 12-cycle/162959-orbit search. If no new branches are pruned beyond E039 projected LP, abandon this line and prioritize a genuine k4 LP-feasible counterexample or proof-producing unrestricted search. Independently replay any full 100/100/100 immediately.
