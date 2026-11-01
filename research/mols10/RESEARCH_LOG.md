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


## MOLS10-E002 | 2026-11-01 09:53 PST (2026-11-01 17:53 UTC) | Complete common-transversal obstruction for two fixed pairs
Status check: 3-MOLS(10) still OPEN. Primary 2026 Bright–Keita–Stevens publication: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; latest relevant 2026 arXiv work https://arxiv.org/abs/2605.02132 concerns orthogonal pairs and SAT improvements, not a complete triple. No reliable later full solution found in this run.
Source input: first three Egan–Wanless matrices from https://users.monash.edu.au/~iwanless/data/MOLS/neartripleMOLS10.txt , verified against original text.
New exact equivalence (for fixed pair X,Y): a third Latin square Z orthogonal to both is equivalent to a partition of all n² cells into n pairwise-disjoint common transversals (each meets all rows, columns, X-symbols and Y-symbols once).
Experiment: enumerated ALL 10! row-column permutations, requiring both X and Y symbol uniqueness; independently cross-checked complete results using a separate bitmask DFS, then exhaustively enumerated disjoint transversal subsets. No timeouts/heuristic UNSAT.
Pair (A,B), input SHA256 47f9bad62f68b317ff0fc8ae72278b07355ceac64a502e2af0030473d0c405c2: EXACTLY 14 common transversals, 12 cells in none, maximum disjoint packing 7. Thus this particular orthogonal pair has no third mate.
Pair (A,C), input SHA256 6db5f6f5d6e1bb0743c6a9e59eeb633ac0490f8a001975083065a4f2b2b79018: EXACTLY 7 common transversals, 36 unsupported cells, maximum disjoint packing 1. Thus this particular orthogonal pair has no third mate.
Both results independently replayed locally; GitHub CI: https://github.com/davidlueng986-alt/123321/actions/runs/41334010585 — success, including published-pair regression tests. Certificate with all 21 permutations: E002_FIXED_PAIR_CERTIFICATES.md. Code: transversals.py, test_transversals.py.
Research impact: **conditional negative results only**; these are NOT evidence that arbitrary 3-MOLS(10) cannot exist and not claimed novel. Crucially, the prior next action (bounded search on the published pair) is now superseded by a complete exact certificate, avoiding wasted SAT compute.
Next action E003: obtain genuinely different order-10 orthogonal pair instances (e.g. original author's Myrvold-MOLS repository https://github.com/curtisbright/Myrvold-MOLS and associated solutions/data), verify provenance, screen common-transversal count and coverage; prioritize pairs with >=10 transversals and full cell coverage. For high-transversal pairs (>20), use a scalable exact-cover/SAT packing backend and preserve UNKNOWN on timeouts. Do not rerun A/B or A/C except for regression.
