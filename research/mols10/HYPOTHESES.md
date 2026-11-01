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
