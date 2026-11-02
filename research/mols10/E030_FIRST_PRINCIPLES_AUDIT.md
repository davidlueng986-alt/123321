# E030 — First-principles model reset (2026-11-02 UTC)

Status: OPEN. Audit of STATE.json and living Drive journal through E029. No global solution asserted.

## Core hypothesis
Treat 3-MOLS(n) as three exact-cover partitions of the n*n cells into n permutation transversals. Each transversal in one partition intersects every transversal of another partition in exactly one cell. This is equivalent to three pairwise orthogonal Latin squares; it does not fix any first square.

## Research risks corrected
* Fixed-Q exhaustive UNSAT only excludes that Q, not its isotopy family without explicit classification, and not unrestricted n=10.
* Common transversal count and support are necessary, not sufficient. Exact cover of compatible transversals is decisive.
* Two independent implementations can share an incorrect encoding. Test equivalence using small-order known positive/negative cases and independent matrix validation.
* Avoid equating local search nodes with global coverage.

## New falsifiable hypotheses
H30A direct symmetric triple-partition search; H30B early cross-partition propagation; H30C Hall/matching obstructions on cell-to-transversal hypergraphs; H30D canonical incidence-graph/isotopy hashing; H30E LP fractional exact-cover dual certificates; H30F randomized nonlocal construction with independently validated pair overlays; H30G direct TD(5,10) SAT with certified proof logging; H30H learning branch order from small-order controls, never learned pruning without soundness proof.

## Implementation
E030_direct_partition.py is an exact, intentionally unoptimized baseline. It has no unsound symmetry breaking. Node budget returns UNKNOWN_BUDGET, never UNSAT. Validate output squares with an independent 100/100/100 checker before any claim. Its computational scalability at n=10 is not established. The next optimization should avoid re-enumerating partitions for each A/B and use incremental compatibility bitsets and canonicalization.

## Next concrete action
Run n=2 (negative), n=3/4 (positive) tests; audit their outputs. Implement exact cross-partition compatibility propagation and benchmark against this baseline on n=4/5. Only then attempt bounded n=10 and preserve UNKNOWN honestly.
