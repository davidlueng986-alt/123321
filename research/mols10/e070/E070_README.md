# E070 — R4 rigorous 5-net PSD obstruction, standalone research archive

**Global state OPEN, 0/1700 full branches proved UNSAT.** Eight of eight canonical first-column cycle types have partial-point exact integer incompatibility certificates, NOT full root exclusions.

- Read `E070_REPORT.md` for theorem proof, quantification and exact scope.
- `E070_EIGHT_CYCLE_TYPES_EXACT_CUTS.json`: 8 integer certificate records, one representative per cycle type.
- `E070_R4_COMPRESSED_EXACT_CERT_BRANCH0.json`: 22 point tuples, exact integer quadratic -90, sound 38-literal conditional clause.
- `E070_R4_COMPRESSED_EXACT_CERT_BRANCH400.json`: 24 tuples, -92, sound 42-literal conditional clause.
- `E070_PSD_ORACLE_BENCHMARK.json`: 8 type random greedy path measurements; NOT evidence of whole-branch closure.
- `E070_dynamic_oracle.py`: integer-certifying adaptive partial-OA R4 oracle (floating screening, integer proof gating).
- `E070_INDEPENDENT_VERIFY.py`, `E070_EIGHT_CYCLE_INDEPENDENT_VERIFY.py`: independent verifier scripts.

## Reproduce no false positives and all exact integer certificates

```sh
bash E070_REPLAY.sh
```

Requires Python 3, NumPy (for positive examples, spectral oracle). The exact 8-type proof checker uses only the Python standard library. `E064_12_representatives.jsonl` is bundled for reference. No GPU or external services needed.

## Why this matters—and what it does NOT show

The necessary theorem for every point subset S in a hypothetical OA(100,5,10,2) is `25I-5A_S+2J >= 0`, where A_S has adjacency 1 iff two distinct points agree on one OA coordinate. Each integer violation is an **exact, independently checkable mathematical nogood**. But a finite collection of 10 such nogoods does **not** eliminate an entire E064 symmetry class; no global nonexistence proof or full SAT witness has been generated.

## E070-B: full five-coordinate solver integration

[Actual DLX search logs and exact-gated PSD pruning](E070_R4_SOLVER_INTEGRATION.md). R4 pruning 547,452 times with strict exact integer gates in 18 s, branch0 remains UNKNOWN. Run `E070_REPLAY.sh` to regenerate the features, compile, run a short proof-sound search smoke test, and independently check its first integer-cut certificate. No end-to-end SAT improvement or global UNSAT certificate is claimed.
