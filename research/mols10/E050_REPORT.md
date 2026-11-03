# E050 — Source-0 six-class LP screening (2026-11-03 01:xx UTC)

Status: OPEN. Scope: only source key 0 of E047_SOURCES.json, not all E049 109 support-positive prefixes.

## Objective
E049 found 133 valid 3-column cyclic fourth-row rewrites, 109 with complete resource support but no six-class LP evaluation. Evaluate the source-0 subset using a new standalone Python/SciPy implementation.

## Exact setup
Enumerate all 120 column triples x 2 orientations x 7 nonempty square masks = 1680 proposals from E047_SOURCES.json source 0. Check row/column Latin constraints and all three 40-cell pair overlays. For each valid prefix, enumerate residual placements (column,a,b,c) avoiding all used column-symbol and pair-symbol resources. The six-class equality relaxation has one demand per unused column-symbol or pair-symbol, and each legal placement covers exactly six demands. Solve A x = 1, x >= 0 with scipy.optimize.linprog(method='highs').

## Observations
15 valid proposals, consistent with E049's source-0 count. Eight have exact zero-support demands (unconditional fixed-prefix non-extension, assuming complete candidate enumeration); seven have full support but HiGHS reports numerical LP infeasibility. **No exact integer Farkas certificates were extracted for the seven numerical cases**, so they remain provisional numerical observations, not exact mathematical non-extension proofs. Zero LP-feasible cases in this 15-case sample. All results are local, not global. No symmetry orbit eliminated.

## Reproducibility and limitations
A standalone Python script and JSON output were generated in this run's sandbox: e050.py and results.json. The GitHub connector cannot directly ingest those local bytes in this run, so this commit records the experiment and explicit non-certified boundary, rather than falsely claiming code is in GitHub. Input: https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/E047_SOURCES.json ; prior E049 code: https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/E049_cycle3.js . Primary status references: https://arxiv.org/abs/2503.10504 and https://arxiv.org/abs/2605.02132 . Fresh 2026-11-03 targeted search did not find independently verified unrestricted resolution; absence of hits is not proof.

## Next
Extract exact rational/integer Farkas certificates for seven numerical infeasible cases and independently replay the eight zero-support cases; then evaluate remaining E049 sources (94? actual count: 109 full-support overall, 7 from source 0, so 102 full-support outside source 0). Advance symmetry-complete proof-producing SAT rather than treating correlated local samples as global coverage.
