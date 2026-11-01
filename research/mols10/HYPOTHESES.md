# Mathematical hypotheses (none assumed true)

## H1 — Fixed-pair extension (highest priority)
Given explicit order-10 orthogonal Latin squares A,B, is there a Latin square C orthogonal to both? Formulate SAT/CP-SAT or exact cover with all row, column and pair constraints. Verify instances on n=3/n=4 first. A conditional unsatisfiable instance is **not** proof of global nonexistence.

## H2 — Near-triple collision elimination
Published Egan–Wanless baseline: 100/100/91. Seek certified Latin trades that repair repeated B–C pairs without breaking A–B and A–C constraints. Evaluate all 3 pair overlays. Prove or precisely scope any exhausted trade neighborhood.

## H3 — Search-completeness preserving symmetry reduction
Use row/column/symbol/isotopy/paratopy symmetries only with explicit completeness argument; save canonical transforms. Never assume a convenient normalization that might exclude solutions.

## H4 — Auditable structural lemma
Propose a precise new lemma for a defined subclass, check prior literature, then prove it via Lean or independently checked UNSAT certificate. Do not promote restricted results to the general theorem.

## Portfolio policy
Do not rerun unsuccessful seeds without a changed hypothesis. Prefer short, falsifiable, reproducible experiments. Distinguish observations, working conjectures, conditional theorems and fully verified proofs.


## E002 evidence / H1 refinement (2026-11-01)
For fixed pair X,Y, n disjoint common transversals are necessary and sufficient for a third mate. The Egan–Wanless pairs (A,B) and (A,C) are now fully ruled out by complete exact enumeration (14 transversals / max packing 7, and 7 / max packing 1, respectively). These conditional obstructions do not settle the general problem.
New H1-SCREENING: sample genuinely distinct published orthogonal pairs; measure (1) transversal count, (2) cell coverage, (3) exact/approximate maximum packing. Necessary but not sufficient cheap filters are count >= 10 and all 100 cells covered. Once these pass, solve the disjoint-transversal exact-cover problem using a scalable backend. Verify each candidate with verify.py.
Source lead: https://github.com/curtisbright/Myrvold-MOLS . Avoid exhaustive search on the already eliminated Egan–Wanless pair. Check novelty before claiming a new theorem.


## E003-E007 evidence and E008 prioritization (2026-11-02)

- Parker historical pair has **0** common transversals (complete exact certificate). This is a third fixed-pair obstruction, NOT a theorem on every pair.
- For Egan A, a deterministic but biased 200-seed mate sampler yielded 91 distinct normalized B matrices, all with some unsupported cells; sample bias means no global probability bound follows.
- In the complete restricted k-symbol trade neighborhoods for Egan A/B, k<=3 has no nontrivial alternative, k=4 and k=5 each produce only neighbors with <=4 common transversals (below the original 14). This falsifies H2's naive "small-support repair helps" direction for these exact support sizes, not for arbitrary Latin trades.
- For Parker A with 12 small-budget randomized seeds, 11 searches were UNKNOWN rather than UNSAT; one seed produced a valid alternative mate which still has 0 joint transversals. Avoid treating resource exhaustion as evidence.

### H5 — Coverage-directed search (NEW PRIORITY)
Instead of maximizing arbitrary orthogonal mate count, attempt to choose a pair A,B whose **common transversals cover all 100 cells and number at least 10**. Both conditions are necessary but not sufficient for a triple. Test adversarial small-order controls and check generated B by independent verifier. New search objective is count of unsupported cells (first), then number / disjointness of common transversals (second). Never infer a proof from optimization values.

### H6 — Diverse first-square generation (NEW PRIORITY)
Replace the fixed Egan and Parker first squares by genuinely different Latin squares with a verified orthogonal mate, not merely a row/column/symbol permutation of the same OA. Paratopy equivalence tests should preserve the number of common transversals as one quick necessary invariant, but identical counts alone do not prove equivalence. Request primary published witnesses or reproducible SAT outputs before computational screening.

### Governance change
Prioritize H5/H6 over repetitive Egan A/B <=5-symbol local trades. Preserve E003–E007 evidence and exact program outputs in reports. Any candidate full triple must pass all three 100/100 overlays; any claimed nonexistence must supply unrestricted coverage/certificates.
