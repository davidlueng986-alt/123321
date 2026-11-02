# E048 — Four-row alignment rigidity and 2×2 Latin intercalate rewrites

UTC 2026-11-02 23:50–23:56. **GLOBAL 3-MOLS(10) OPEN; 0/162,959 complete symmetry orbits excluded.** No 100/100/100 triple and no unrestricted negative certificate.

## Literature review
Primary sources checked: Bright–Keita–Stevens, *Myrvold's Results on Orthogonal Triples of 10 × 10 Latin Squares: A SAT Investigation*, EJC 33(1) #P1.30 (2026), https://arxiv.org/abs/2503.10504 ; Barnoff–Bright, *Improving SAT Solvers on Orthogonal Latin Square Problems*, arXiv:2605.02132v2 (2026-07-04), https://arxiv.org/abs/2605.02132 . Fresh November 2 targeted arXiv/web search found no independently checkable unrestricted resolution. Absence of hits is not proof of absence.

## Falsifiable objectives and method
E047 exhausted fourth-row-only two-disjoint-column swaps for eight sources. This iteration tests *different* transformations:
(1) Independently permute all four rows of B and C relative to A: 24²=576 relative row alignments for each valid four-row prefix, preserving the Latin row/column conditions but possibly breaking the three overlays.
(2) Enumerate all original 2×2 Latin intercalates [a b; b a] within *any* rows/squares of the eight E047 sources, apply each static-original-intercalate subset of size 1,2,3,4, and revalidate every row/column and all 40/40/40 pair overlays.
(3) Exact residual six-resource support for any new valid neighbor.

## Results — two independent input snapshots
**Local E045 574-case snapshot:** 512 E044 + 574 E045 + 479 E047 + 8 source records = 1,573 records; eight sources duplicate E045 local inputs. Exactly **1,565 distinct ordered prefixes**. Enumerated **901,440** B/C relative-row permutations. Exactly **1,565** valid alignments, all identity/identity. Python crosscheck on 128 deterministic prefixes (73,728 proposals) PASS.

**GitHub remote E045 570-case snapshot:** 512 E044 + 570 E045 remote + 479 E047 regenerated + 8 E047 local sources = **1,569 distinct ordered prefixes** (no duplicates in this snapshot). Enumerated **903,744** relative-row permutations. Exactly **1,569** valid alignments, all identity/identity. Independent CPU-only Node.js replay prints PASS; the original workflow incorrectly masked an early failed assertion through `tee` without `pipefail`, which was fixed. Use the final corrected workflow run as authoritative.

**Intercalates:** 60 original 2×2 intercalates across the eight sources, with per-source counts 15,3,6,8,4,6,11,7. Exactly **2,895** static subsets of sizes 1–4 tested. Only **one** valid changed 40/40/40 prefix: source 0, square B (index 1), rows (0,1), columns (1,4), a single 2×2 intercalate. All two-, three-, four-intercalate subsets failed validity. Python and independent JS enumerators agree.

**Exact new fixed-prefix obstruction:** The unique valid changed prefix has 416 legal residual placements but none covering missing resource C(square 2, column 9, symbol 5), resource ID **595**. An integer-only independent JS verifier enumerates 10,000 potential (column,A,B,C) placements, checks the 240 fixed resources, and verifies zero candidates covering resource 595. Consequently *this particular changed prefix* cannot extend to 3-MOLS(10). This is not an orbit-level result.

**Positive controls:** Affine 3-MOLS order 5, 7, 11 four-row prefixes yield 6, 18, 105 valid relative row alignments respectively; the rigidity detector is not trivially hard-coded to identity.

## Reproduce / evidence
Run `node research/mols10/E048_local_rigidity.js` at branch `math-agent-mols10`. Inputs: `E044_RESULTS.json`, `E045_GUIDED_RESULTS.json`, `E047_REGENERATED.json`, `E047_SOURCES.json`. CI: `.github/workflows/mols10-e048.yml` (CPU-only, timeout five minutes, strict `pipefail`). Separate local Python and JavaScript crosschecks, input snapshots, results and SHA256 are in the local E048 research bundle.

Failures retained: an early expected flat resource ID 529 was a human typo; the independent verifier correctly reported 595, which was fixed. An initial Python extension to 3/4 intercalate subsets had a syntax typo, fixed before any result was accepted. First GitHub CI run failed its assertion because it assumed local 574-case E045 data existed on remote; actual remote E045 is 570 cases. It was initially incorrectly reported green due missing `pipefail`; both the input count and CI failure propagation have been corrected.

## Limits and next action
These are **finite restricted neighborhood enumerations**, not symmetry-complete results. The 1,565/1,569 input sets are highly correlated and nonuniform; the observation that every sampled prefix has unique relative row alignment is *not* a universal theorem. No LP-feasible new k4 prefix, no full solution, and **0/162,959 complete orbits** excluded.

Next: prioritize k3→k4 joint construction directly optimizing six-class LP phase-I or symmetry-complete proof-producing SAT. Avoid further fourth-row-only and original-static-intercalate moves on the same eight sources. If investigating a universal row-alignment rigidity conjecture for order 10, explicitly seek counterexamples outside these correlated pools before any proof claim.
