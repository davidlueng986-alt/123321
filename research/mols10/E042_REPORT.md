# E042 — Exact isotopy-aware forbidden-pattern nogood benchmark (2026-11-02 ~17:45–18:00 UTC)

**GLOBAL STATUS: OPEN.** No verified 100/100/100 triple and no unrestricted nonexistence proof. **0/162,959 full normalized orbits excluded.**

## Primary-source and state audit
Read the living Math Agent Google Docs journal, `STATE.json` (E041), E041/E040 certificates and verifiers, and E037/E036 inputs. Primary literature rechecked: Bright–Keita–Stevens, *Electronic Journal of Combinatorics* 33(1) P1.30, 2026-02-13, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; Barnoff–Bright arXiv:2605.02132v2, revised 2026-07-04, https://arxiv.org/abs/2605.02132 . Targeted current searches found no independently checkable unrestricted solution; absence of a hit is not a proof.

## Falsifiable question
Does applying **three existing exact forbidden partial patterns** (E040 21-cell and 22-cell, E041 new 9-column 22-cell) under **row permutation, column permutation, independent three-square symbol bijections, and square permutation** actually prune *additional* previously sampled four-row branches? These are known correct nogoods, but usefulness is unmeasured. Test exact containment, not just core equality.

## Method and inputs
For each source core, partition fixed cells by source column. Search an injective source-column -> target-column map using MRV backtracking, maintaining forward and reverse partial bijections for each square's symbols. Enumerate all 4! row and 3! square permutations. All 10-column bijections are implicitly considered by the backtracker; it stops only when a complete embedding is found or all assignments are exhausted. There is **no node cap** in the published `E042_replay.py` (a separate pilot used cap 20,000 per permutation; no cap was reached). This tests precisely the stated isotopy/square-permutation subgroup, **not** all paratopies, row-column interchange, or partial patterns spanning arbitrary nonconsecutive rows.

Inputs: E037 360 legal four-row prefixes (30 each for 12 normalized cycle types) plus E036 156 four-row prefixes taken from six-row witnesses (one per normalized g orbit in f=2^5). These 516 fixed prefixes are already known E039 LP-infeasible; this is a **marginal pruning benchmark**, not a fresh nonexistence theorem. E037 source archive: https://drive.google.com/file/d/1cMfISpjIlibPYySk0jfoDhD7-96j3ghA/view ; E036 witness JSON available in local E042 bundle. E040/E041 public certificate files are in this GitHub directory.

Input SHA256:
- E037_ALL_CYCLES.json: `1963301e0e611a33a61522ac30c5a24237faad8432dd23c0ddc8215202ce36a7`
- E036_WITNESSES.json: `4b1a2abb7e2ddade1c898ae23a50b086af0dd3545265a92c37dddd326b0f9462`
- E040_EXACT_MINIMAL_CORES.json: `34fa47572145828b6fa25c2065fd51ba63ddb4d8d5d4db205ced4606c3e61c6c`
- E041_NEW_22_SPARSE_CERTIFICATE.json: `9b1fdc2d83ae73728ce9075d747e98ee03c0419a883fa9158b532be045646604`

## Completed bounded experiment
**516 x 3 = 1,548** exact core/prefix embedding checks, all completed; **zero UNKNOWN**. All 4! x 3! isotopy choices searched for every nonmatch. Total ~111.4 s across five batches for first matcher. **Only 3 matches**:
- index 92: E040 22-cell core (its original source prefix)
- index 93: E040 21-cell core (its original source prefix)
- index 94: E041 22-cell core (its original source prefix)

**1,545/1,548 checks negative.** No motif hit in the other **513/516** prefixes. The 3 hits were already LP-infeasible; thus **zero incremental cuts over existing E039 LP** on this dataset. The original three source prefixes were independently equality-checked against input. Three self-match controls and nine randomly transformed row/column/symbol/square isotopy controls passed. Existing E041 independent integer-only Farkas verifier passed (22 cells, seven weights, RHS +1, 2,596 allowed placements), as did 100 exact isotopy certificate checks.

**Independent replay:** A separately written standard-library `E042_replay.py` reran all 1,548 checks in batches (0:100, 100:200, 200:300, 300:400, 400:516), reproduced exactly the three matches, and visited 2,447,321 DFS nodes over ~126.23 s. Five machine-readable replay JSONs are included in the local bundle. This replay is algorithmically similar but independently implemented; it is not an independent SAT proof of nonexistence.

## Failed approaches / negative evidence / scope
- Initial monolithic 516-prefix run was interrupted at ~150 prefixes by execution timeout; its partial output was **not** counted. Replaced by five bounded complete batches.
- An earlier exact rationalization attempt on E041 deletion-feasible LP primals using Fraction.limit_denominator up to 10^8 **failed** to satisfy any of the tested exact resource equalities; those 65 LP-feasible statuses remain numerical, **not exact primal certificates**.
- The forbidden-pattern matching algorithm has substantial overhead relative to a single LP solve on this sample (~0.2 s/prefix for three motifs in Python); speed comparisons are not normalized end-to-end and cannot be extrapolated to other search trees.
- None of 516 fixed-prefix exclusions excludes an entire normalized orbit; **global coverage 0/162,959**.

## Reproduce and next action
Put `E037_ALL_CYCLES.json`, `E036_WITNESSES.json`, `E040_EXACT_MINIMAL_CORES.json`, `E041_NEW_22_SPARSE_CERTIFICATE.json` next to `E042_replay.py`. Run `python E042_replay.py 0 100`, then offsets 100,200,300 with length 100 and 400 with length 116; expect only [92,E040_22], [93,E040_21], [94,E041_22]. Independently run `node E041_verify.js E041_NEW_22_SPARSE_CERTIFICATE.json`.

**Next:** deprioritize expensive 21/22-cell isotopy nogood matching on similar random k4 prefixes; seek sound cheaper invariant filters or a genuine LP-feasible four-row counterexample, but direct most budget to unrestricted 12-cycle-type/162,959-orbit proof-producing search. For any complete candidate, replay all 3 Latin and all 3 overlay 100/100/100 constraints independently. No claim of a global theorem or publication novelty.
