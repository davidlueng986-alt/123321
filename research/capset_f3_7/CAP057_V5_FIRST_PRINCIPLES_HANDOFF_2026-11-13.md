# CAP057 — v5 migration handoff and first-principles restart

**Date:** 2026-11-13 UTC. **Owned original question:** determine the exact value of `r_3(7)`, the largest no-three-in-line set in `F_3^7`.

**Mathematical status: OPEN.** An explicit 236-point construction is verified; the current literature reports 288 as a preprint upper bound (Thackeray 2022). No new ≥237 cap, matching upper bound or complete universal proof was found in this run. No autonomous or GitHub scheduled work was started.

## v5 authority / reading completed

Read canonical `00_START_HERE.md`, `01_AI_OPERATING_SYSTEM/AGENTS.md`, `problem_registry.json` schema v5 and the CAPSET workspace `00_CURRENT_RESEARCH_STATE.md` after relocation. Registry explicitly assigns CAPSET-F3-7 to this existing manual solver, not default A135508. Live code is on the *unchanged* branch `research/capset-f3-7`, with latest previous CAP056 GitHub STATE, report and evidence. v5 treats previous records as evidence, not a mandatory research roadmap.

## First-principles decomposition (root-complete but not itself progress)

Let `G=F_3^6`. For any cap `A` in `F_3^7`, define three parallel six-flat layers `A_0,A_1,A_2 ⊂ G`. Every 3-point affine line either lies within one layer or uses exactly one point from each of the three layers. Therefore

```
A cap  <=>  A_0,A_1,A_2 each cap AND (A_0+A_1) ∩ (-A_2) = ∅.
```

If a 237-cap exists, existing CAP007J implies one choice of six-flat contains at least 89 points. Thus the *root obstruction* can be attacked as a cap-constrained additive sumset incompatibility for a dense `A_0` of size 89–112, not merely as a raw 2187-variable triple packing MILP.

Potential theorem sufficient to close r3(7)=236: **for all three 6D caps `A_i`, if `max_i |A_i| ≥89` and `Σ|A_i| ≥237`, then `(A_0+A_1)∩(-A_2)` is nonempty** (after relabeling so a dense layer is `A_0`). This is a logically equivalent mathematical target, NOT a proved inequality or a novel claim. A serious proof would have to exploit cap-specific sumset expansion, Fourier structure and cross-layer compatibility; generic set-addition inequalities and homogeneous LP are much too weak. This recasts where a global contradiction needs to arise.

## Actual new attempts, rather than repetitions of CAP056

**A. Why standard local 236→237 mutations stall.** Reconstituted the canonical 236-point source fixture and independently verified all 27,730 unordered source pairs against the mod3 cap condition. Its 1,951 outsiders have centered-secant degrees 10..56. Exactly **24** outsiders attain minimal secant degree **10**. For each such outside point `q`, its ten obstructing secants are disjoint; to select `q`, at least one endpoint per secant must be removed. Enumerated *all* `24 × 2^10 = 24,576` choices removing exactly one endpoint from each secant, then retaining `q` and all other source cap points. In every case there are **zero additional immediately addable points**. An independent direct GF3 complete-pair recomputation verified 25 representative combinations. This is only a narrow statement about the old 236 witness, **NOT an upper bound**, but explains why one-point seeding and short-kick annealing fail structurally. Do not continue optimizing these local searches.

**B. Complete conditional 112-slice problem, unrestricted other layers.** Fixed one source 112-cap as `A_0` in `G`; because 112-cap in AG(6,3) is affinely unique, this is the full branch for any 237-cap with some 112-point six-flat (not full root, since CAP007J only forces ≥89). Allowed *all* 729 possible points in both other layers. Built **1458 Boolean variables, 258556 linear constraints**, consisting of 2×88452 internal six-dimensional 3AP lines, 81648 forbidden cross-layer pairs, and four cardinality/symmetry/bound constraints. Added `|A_1|+|A_2|=125` (sufficient by downward closure) and `|A_1|≥|A_2|` without loss. Independent positive control exactly reproduces the historical `(112,112,12)` 236-cap. HiGHS 5-second bounded run returned **UNKNOWN / time limit** (676 LP iterations, zero completed B&B nodes); no integer 237 witness and no UNSAT proof. A 90-second enclosing run was externally terminated without a solver verdict; do not count it as an additional completed proof attempt.

**C. Much broader fixed-two-Hill trade, not minimal local swaps.** Fixed `A_0` and an original second 112-cap `B`. Let the solver delete *any subset* of those 112 B-points and choose *any* cap `C⊂G` from all 729 positions, subject to `C∩(-A_0-(B\R))=∅`. Maximized `|C|-|R|`; profit ≥13 would give ≥237. Built a full **841 Boolean variable / 100996 constraint** MILP (all 88452 ternary constraints in C plus 12544 cross-compatibility implications). This represents all 2^112 deletion patterns (but NOT arbitrary replacement points in layer B). Historical known feasible profit12 was separately checked in the matrix. HiGHS 5-second bounded run returned UNKNOWN; it found only profit1 although profit12 is independently known feasible, a clear solver cold-start failure; neither the reported incumbent nor LP relaxation is a bound on true optimum. Enclosing 90-second run interrupted without decision.

**D. Independent source and model checks.** Source witness 236 unique, zero 3AP, 27,730 pairs; all full-layer source controls passed. At least 25 direct independent recomputations checked candidate ejection residuals from scratch (without incremental cov counts). A smaller finite condition is not a world-level mathematical result; no public novelty claim.

## What to abandon or seriously challenge

- **Do not use conditional Hill112 as a global normalization:** CAP007J gives ≥89, not 112. Even an UNSAT proof for all 112-slice completions does not resolve the original question.
- **Do not spend another unchanged 38s/150s on CAP056 MILP:** false UNSAT arose from a sign bug and was retracted; true runs processed almost no branching.
- **Do not treat plain level-2 SDP quartic orbit enumeration as an implementable strategy** without an actual proof-preserving quotient/sparse dual; CAP055/056's raw memory scale is vast.
- **Do not count 24,576 blocked local swaps as mathematical progress toward the exact theorem.** It is only negative evidence about a particular basin.
- **Do not assume 236 is optimal.** A larger construction would refute that guess without closing the exact optimization problem; keep constructive and upper-bound paths both conceptually live.

## Highest-value next mathematical action

Seek a **cap-specific sumset expansion theorem** for triple layers in `F_3^6` that directly excludes `a+b+c=237` with `a≥89`. This must use structure missing from generic Kneser / second-moment / all affine-six-flat LP relaxations, perhaps spectral constraints on cap-constrained complement `G \ (A_0+B)` and an exact, certificate-producing branch decomposition by large 6D slices. In parallel, constructions must allow changing whole outer layers, not only perturbing the canonical 236 witness. Disproof must cover every `a=89..112`, and every support branch; any residual UNSAT must have an independently checkable certificate. Neither requirement has been met.

**Required next handoff:** model the sumset incompatibility with provably complete slice normalization and identify a nontrivial valid inequality that cuts the known fractional root pseudo-cap *for ALL large slices*. Without a concrete candidate, remain OPEN rather than multiplying local experiments.

## Reproducibility / artifacts

The source archive includes `make_witness.py`, `witness236.txt`, `degrees.py`, `cap057_trade_search.cpp`, `independent_trade_control.py`, both full conditional MILP sources, their 5-second runnable versions, source controls, all bounded solver logs and results. No paid compute, no GPU, no scheduled Actions, no model handoff to another mathematical problem.

**Outcome:** `NOT DONE (ATTEMPTED)`, no new rigorous bound or ≥237 point witness. This handoff supersedes earlier routine backlog ordering, not the original theorem or existing evidence.

## v5 portable evidence
- Handoff: https://drive.google.com/file/d/15IZnuIz0bQZI6JuCIMcNPlSOS7hi1yl4/view?usp=drivesdk
- Code/complete small logs: https://drive.google.com/file/d/1d9iqQWKnZYnm-6ok3HdXO6GnQRR_lKHG/view?usp=drivesdk (SHA256 c07aa8171c9166970bae01715c4e4250be32234805d8675809ae539c7c096368)
