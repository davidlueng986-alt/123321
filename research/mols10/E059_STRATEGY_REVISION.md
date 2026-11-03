# E059 — CLOSED-INVALID proof routes and current decisive obligations

**2026-11-03; global question 3-MOLS(10) OPEN; MOLS10 hourly automation paused by user.**

## Refuted sufficient nonexistence routes

- `N-A-Fractional`: **FALSE**, explicitly. Legal cyclic 4x10 triple `d_A=0,1,4,8; d_B=0,6,1,9; d_C=0,7,9,2` has an exact rational column+pair residual LP primal of 120 nonzero placements, each 1/2. Independent Python and Node.js check all 360 equations.
- `N-A-Integral`: **FALSE**, explicitly. Four disjoint common transversals of the published Egan–Wanless orthogonal pair yield a legal 4x10 partial triple, with the remaining 60 OA(100,4,10,2) points providing a true integral 360/360 residual six-resource cover. Seven disjoint common transversals analogously yield a legal 7x10 partial triple with a 30-point integral 180/180 residual cover. These do not form the missing Latin rows.

**Logical diagnosis:** The 6-resource relaxation entirely omits the fifth (row) coordinate. Its integer feasibility is merely a partial embedding in an `OA(100,4,10,2)` (pair of MOLS) and is not enough to prove `OA(100,5,10,2)` (three MOLS). Any universal nonexistence proof must use row factorization or a stronger 5-coordinate theorem. Do not optimize old Farkas duals as the main path.

## Direct existential route: 9x10 completion endgame

Jäger, Markström, Öhman and Shcherbak, EJC 31(1) P1.53 (2024), Fig. 3, already give a 9x10 3-MOLR. Our independent transcription and replay confirms 90/90/90 partial overlays; the column-forced last rows produce 93/93/93, not 100/100/100. In nine choices of an 8-row restriction of this source, all 5,392 last-two-row Latin completions have been independently enumerated and rejected, scope restricted to these exact nine sources.

New precise objective: search for a 9x10 three-MOLR whose forced last rows simultaneously give 100/100/100, equivalently all three missing-pair permutations match their forced row pairings. This is a direct witness-search target, not a theorem that all such partials fail.

## Global nonexistence route

Need a complete independent proof that no 5-net exists, retaining all five OA coordinate classes. The E033 162,959 orbit representatives quotient only A/B's two-row frontier; every C second row and all later continuation branches must be included, and every UNSAT conclusion requires a complete proof certificate. **0 global orbits closed so far**.

## Prohibited metrics and stop conditions

No counting partial rows or LP certificates as percentage of the full problem. Report full witness only after independently verifying 3 Latin squares and all overlays 100/100/100; report negative theorem only with unrestricted proof and independent coverage. For any uncertain result use `UNKNOWN`.

Primary reports and code in `E059_REPORT.md`; scientific prior Jäger et al. (2024) https://doi.org/10.37236/9049 and Egan–Wanless (2016) https://doi.org/10.1090/mcom/3010.
