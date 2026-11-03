## UPDATE 2026-11-03 — E059 SUPERSEDES N-A (REFUTED)

Both universal four-row residual LP infeasibility and universal four-/seven-row INTEGER residual exact-cover infeasibility have explicit exact witnesses and are FALSE. See E059_REPORT.md and E059_STRATEGY_REVISION.md. The original N-A conjecture below remains only as historical record, NOT an active research objective. No unrestricted 3-MOLS(10) solution was found. The 2024 literature already provides a 9×10 triple of MOLR; direct endgame must include all five OA coordinates. Hourly MOLS10 automation remains paused by user request.

---

# MOLS10 — Goal-Backward Proof Program (operational charter)

Date: 2026-11-03. **Problem status: OPEN.** The prior hourly MOLS10 automation was disabled at the user's request. This document describes the work done in this interactive run only; no future autonomous execution is promised.

## The proposition we are trying to decide

P := there exist three order-10 Latin squares A, B, C with all three pairwise overlays containing 100 distinct symbol pairs; equivalently OA(100,5,10,2) exists.

**Completion conditions.** Positive: supply the three complete 10x10 matrices and independently check every Latin row/column and the A/B, A/C, B/C overlays. Negative: give a complete unrestricted formal proof, or a finite proof-checkable UNSAT certificate together with a mathematically justified equivalence-class coverage argument. Until either criterion is met, status is OPEN.

## Logical proof dependency graph (goal -> obligations)

- **Existence route (construct):** build a full A/B/C candidate -> independently validate exact 100/100/100 -> publish complete matrices, algorithms, provenance and checksum -> P proven.
- **Nonexistence route N-A (global four-row relaxation):** prove the universal theorem `for every legal order-10 k=4 partial triple Q, no nonnegative solution of M(Q)x=1 exists` -> every full triple induces a legal Q plus a feasible x, contradiction -> not-P proven. The theorem is *unproven*. For a potential shortcut, prioritize finding a single LP-feasible Q to falsify this sufficient nonexistence route. An LP-feasible Q would **not** prove P.
- **Nonexistence route N-B (symmetry-complete SAT):** prove every potential full triple is equivalent to one of the selected normalized branches -> generate the complete branch inventory (including C's second row and all later rows) -> get a formally complete UNSAT derivation for **each** branch -> independently check proof and branch coverage -> not-P proven. The E033 162,959 orbit count covers only the A/B *two-row frontier*, **not** whole triples. An UNSAT result from any one fixed continuation cannot close an orbit.

## Mandatory research decision rule

Every experiment must name its parent proof obligation, success criterion, failure criterion and scope. An experiment counts as *direct main-goal progress* only when it (a) yields a full validated solution, (b) proves an unrestricted structural theorem, (c) closes one fully normalized global branch with a complete independently checked proof, or (d) falsifies a major assumption, preventing further investment in a broken proof route. Merely counting partial prefixes, Farkas certificates, nodes, commits or local trade neighbors is **not** progress on P unless it closes an explicit obligation.

Discontinue broad E052–E057-style polishing of the same seven local dual certificates without a path to a global closure. Existing certificates remain valid restricted evidence, and should be kept for audit. Give priority to falsifying N-A, not generating additional N-A-supporting biased samples. Keep constructive whole-OA search active as a separate logically independent route.

## E058 actual computation and evidence

1. Independently constructed a legal 3-row order-10 triple of cyclic affine rows `S_a[r,c]=(c+a*r) mod 10`, `a=1,3,7`, `r=0,1,2`. All three partial overlays contain 30 distinct pairs. A universal balanced-symbol projection identity proves this prefix impossible to extend; an exact 420-resource/1,000-placement Farkas dual with RHS 20, maximum legal-placement score 0 was separately reconstructed and integer-checked. This **falsifies any broad reading** that all legal order-10 k=3 prefixes have a feasible residual LP. It does not refute a k=4 universality conjecture.
2. **Global necessary identity:** in any three pairwise orthogonal order-10 Latin squares, select *arbitrary* 5-element subsets of the symbols in each square, turn membership into binary labels. Exactly **25 of the 100 cells** have all three binary labels equal. Reason: in each pair of labels, exactly 50 of the 100 pairwise overlays disagree; summed disagreements = 150. Each cell contributes either 0 (all labels equal) or 2 (otherwise). Thus exactly `100 - 150/2 = 25` all-equal cells. No Latin condition is used, so it is a consequence solely of pairwise orthogonality, not a claimed novel general theorem.
3. C++ exhaustive checker optimizes all 252^3 balanced label triples for each of the **360 pre-existing biased four-row sample prefixes** (all 12 f-cycle types). The optimization loops over 252^2 partitions of the first two symbols and takes the top-five gains for C's partition; this is *mathematically equivalent* to checking 16,003,008 choices per prefix. **1/360** prefixes was excluded by exceeding 25 all-equal cells: index 222 with symbol-subset bitmasks (376,376,217) gives exactly **26** all-equal cells among its first 40 cells. Independent pure-Python replay checks legal 40/40/40 partial overlays and this count. On a complete GF(4) positive-control triple, it checked all 6^3=216 balanced labellings and obtained exactly 4 equal cells, confirming the n^2/4 identity.
4. Separate bounded attempt scored 360 existing k4 candidates for residual fractional packing; best by cycle type ranged approximately 56.48–57.38 against the necessary score 60. The subsequent perturbation search exceeded its tool execution budget; **NO perturbation result is counted or claimed**. 360 nonuniform sample failures provide no global coverage.

**Evaluation against the main theorem:** The binary identity and k3 negative control are exact and independently replayable, but the 5/5 label cut excludes only one of 360 already LP-excluded examples and **zero global symmetry orbits**. It is therefore deprioritized relative to N-A global proof and N-B complete SAT coverage. Never describe the k4 sample as a universal theorem. No full order-10 witness or unrestricted proof was found; **P remains OPEN**.

## Next mathematical decision, only in an explicitly requested future interactive run

Try to *falsify* N-A with a k4 LP-feasible exact rational witness using a genuinely new/global construction, or produce a complete symmetry enumeration/proof for **one whole** A/B two-row orbit (all compatible C rows and all continuations) as a pilot of N-B. Do not conflate a prefix-specific proof with orbit closure. If neither is feasible in the runtime budget, state UNKNOWN rather than multiplying decorative local experiments.

## Repro and audit

- `E058_cyclic_negative_control.py` emits exact Farkas integer weights and independently evaluates each legal placement.
- `E058_binary_projection_cut.cpp` enumerates exact optimal balanced partitions per input prefix; input `E058_k4_360_rows.txt` is generated deterministically from `E037_ALL_CYCLES.json`.
- `E058_independent_verify.py` independently checks the exact order-10 index-222 witness and GF(4) positive controls.
- `E058_BINARY_CUT_WITNESS.json` stores the exact fixed-prefix certificate; `E058_K3_EXACT_NEGATIVE_CONTROL.json` stores the integer Farkas witness.

Origin of biased 360 k4 prefixes: `E037_ALL_CYCLES.json` in E037 bundle; source is E037 rather than independent population sampling. Archive hashes are supplied in E058_MANIFEST.json. The independent Python replay does not rely on C++ output.
