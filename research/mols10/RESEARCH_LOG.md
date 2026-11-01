# 3-MOLS(10) — Research log (append-only chronological entries)

## MOLS10-E000 | 2026-11-02 | Baseline and workflow startup
Question: Do 3 mutually orthogonal Latin squares of order 10 exist?
External status: OPEN based on 2026 Bright–Keita–Stevens paper, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 .
Source baseline: https://users.monash.edu.au/~iwanless/data/MOLS/neartripleMOLS10.txt .
Result: the first three Egan–Wanless arrays all satisfy Latin row/column properties. Exact unique overlay pairs: [100,100,91]. Nine repeated and nine missing B–C ordered pairs. NOT a witness.
Repro: `near_triple.json`, `verify.py --diagnostic`, and `test_verify.py`; local Python smoke tests passed prior to GitHub submission. Read GitHub Actions for independent CI execution.
Literature scope: the 2026 SAT study handles a restricted 4×4-subsquare condition and does not settle the general triple question.
Decision: H1, build an exact third-square extension SAT/exact-cover model for a fixed pair, validate on small orders and report limits. If fixed pair has no extension, do NOT infer universal nonexistence.
Next run: inspect latest CI, implement and test H1; persist any experiment and next action.


## MOLS10-E001 | 2026-11-02 | Fixed-pair extension baseline (known mathematics)
Hypothesis: a third Latin square C can be searched by four all-different constraints per cell: row-symbol, column-symbol, (A-symbol,C-symbol), (B-symbol,C-symbol).
Method: exact backtracking with minimum-remaining-value cell selection and explicit max_nodes/max_seconds guards; exhaustion is UNKNOWN, never UNSAT.
Small-order verification:
- Order 3: fixed known orthogonal pair using slopes 1 and 2 modulo 3; complete fixed-pair search returns UNSAT_FIXED_PAIR.
- Order 4: pair from GF(4) using slopes 1 and 2; search returns SAT and independent checker confirms 16/16/16 ordered pairs with third square.
- Published order-10 near-triple: witness verifier confirms 100/100/91 (not solved).
GitHub CI: https://github.com/davidlueng986-alt/123321/actions/runs/41333555421 — success after regression suite including the small-order extension tests.
Caveat: no general 3-MOLS(10) result claimed; fixed-pair UNSAT does not prove the unrestricted problem.
Next: benchmark published A,B order 10 under bounded resources, then build and benchmark a proper SAT/CP-SAT formulation, keeping exact input hashes and proof status.
