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
