# E049 — Three-column cyclic fourth-row rewrites (2026-11-03 00:43–00:50 UTC)
Status: GLOBAL 3-MOLS(10) OPEN. This is a bounded local-neighborhood experiment, NOT a proof of nonexistence.

## Primary status
Fresh targeted web/arXiv search 2026-11-03 UTC: no independently verified unrestricted solution found. Primary references: https://arxiv.org/abs/2503.10504 ; https://arxiv.org/abs/2605.02132 . Absence of search hits is not proof.

## Objective and method
E046 exhausted single two-column swaps; E047 exhausted two disjoint swaps; E048 exhausted relative row permutations and static intercalates. E049 tests a distinct move: cycle the values in the FOURTH row on a triple of columns, independently in any nonempty mask of the three squares, with a common cycle orientation. Eight exact source k4 triples from E047_SOURCES.json; 120 column triples x 2 directions x 7 square masks x 8 sources = 13,440 exhaustive proposals. Validate each square's row permutations and column distinctness, and 40/40/40 pair overlays. For each valid proposal enumerate all 10^4 potential residual placements (column, A, B, C), retaining those not violating any used column-symbol or pair-symbol resource; check whether every required residual resource has at least one legal placement.

## Observations
13,440 proposals; 133 valid modified k4 prefixes, 133 distinct moves (not an isotopy classification); counts per source 0/70/140/210/280/350/420/490 = 15/15/11/16/22/20/12/22. Masks 1..7: 23,33,5,24,8,11,29. 24 valid prefixes have an EXACT zero-support resource obstruction, hence cannot extend; 109 have full resource support, which is only a necessary condition and does NOT imply LP feasibility or extendibility. Candidate placement counts among valid prefixes range 376..425. One witness: source 0, columns (0,5,8), direction 1, mask 4: 403 legal residual placements but required C(square index 2,column 9,symbol 5) has zero legal support. The zero-support argument is an exact finite enumeration, independently replayable from source and script.

## Reproduce
Input https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/E047_SOURCES.json ; code https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/E049_cycle3.js . Run `node research/mols10/E049_cycle3.js`; optional `--write` creates E049_RESULTS.json. Built-in assertions cover total counts, zero support, per-source counts. Initial in-tool JS enumeration and a separate in-tool resource-support enumeration were completed. CI replay NOT YET confirmed. No claims about LP feasibility of 109 support-positive prefixes.

## Limitations, failure evidence, next action
No global orbit excluded; 0/162959 full symmetry orbits. Most valid moves still require six-class LP. Next: run E049 script in clean CI, independently verify zero-support cases, and prioritize six-class LP for 109 support-positive cases; then target symmetry-complete proof-producing search rather than correlated local moves. No 100/100/100 triple or global negative certificate.
