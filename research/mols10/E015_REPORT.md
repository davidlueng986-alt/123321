# MOLS10 E015 — partial B-class exact-once pruning (sound and executable)

**Timestamp:** 2026-11-01T18:55 UTC. **Global status:** OPEN. **Inputs:** Egan–Wanless near_triple.json; Parker parker_pair.json; explicit new-A orthogonal pairs E012_WITNESSES.json. **No global solution.**

## Structural lemma

Fix a Latin square A. Each symbol class T of any Latin B orthogonal to A is an A-transversal. If a third Latin C is orthogonal to both A and B, each C-symbol class U is an A-transversal and **|U∩T|=1 for every B-symbol class T**. This is strictly stronger for a *partial* B assignment than E014's condition of avoiding repeated selected B symbols, because exactly-once also forbids missing a selected symbol.

For selected, pairwise disjoint A-transversals T_1,...,T_k intended as B classes, precompute for each T the bitset
`Compat(T)={U : U is an A-transversal, |U∩T|=1}`.
Let `Candidates = intersection_i Compat(T_i)`. If some cell x is not contained in any U in Candidates, then **no completion of the selected B classes can be part of a 3-MOLS triple**. Proof: the C class through x would be a U in Candidates containing x, contradiction. This is a necessary condition, not a sufficient condition for a triple.

Implementation: E015_partial_mate_prune.py uses 840–1080-bit integer compatibility masks, bitset intersections, and 100 cell-support masks; the oracle is monotone (adding classes can only remove compatible U). The exact-cover DFS is randomized but reproducible (seed=0); pruning itself is exact and sound.

## E015-A: exhaustive minimal exact-once subset sizes

All subsets of fixed B-symbol classes of size < k were exhaustively checked. First blocking certificates (zero-based):

| Pair | Minimum k | Number of blocking subsets at k | Selected B symbols | Blocked cell |
|---|---:|---:|---|---|
| Egan A/B | **3** | 18 / 120 | {0,1,6} | (6,6) |
| Egan A/C | **3** | 18 / 120 | {0,1,9} | (0,5) |
| Parker A/B | **2** | 3 / 45 | {7,8} | (7,7) |
| E012 trade_12 | **3** | 73 / 120 | {0,1,4} | (0,8) |
| E012 trade_20 | **2** | 2 / 45 | {1,8} | (7,1) |

**Independent replay:** For each of five listed blocked cells, all 10!=3,628,800 permutations were enumerated separately from the bitset oracle; the number of A-transversals containing the blocked cell and meeting each selected B-symbol class exactly once was zero. This independently validates the positive obstruction certificates. The *minimum* k claims rely on exhaustive subset checks in the committed program and CI regression.

**Positive control:** On the explicit GF(4) order-four triple, after k=0,1,2,3,4 classes of B, all 16 cells remain covered by C-compatible A-transversals; at k=4 exactly four compatible transversals remain. The pruning oracle does not falsely reject this known triple.

## E015-B: bounded coverage-directed search on changed A

`python3 E015_partial_mate_prune.py --seconds 4 --indices 12 20 30 --seed 0`

| E011 A trade index | Status | DFS nodes | Prefixes rejected by exact-once support | Time |
|---|---|---:|---:|---:|
| 12 | **UNKNOWN_BUDGET** | 4,194 | 3,193 | 4.000 s |
| 20 | **UNKNOWN_BUDGET** | 4,313 | 3,327 | 4.004 s |
| 30 | **UNKNOWN_BUDGET** | 4,672 | 3,650 | 4.000 s |

No candidate passed the complete 100-cell joint-transversal support filter during these **bounded** runs. The ~76–78% node-level rejection fraction is measured on explored nodes only, not a fraction of all possible pairs. There is no UNSAT claim and no 3-MOLS witness.

## Audit, uncertainty, and next step

- Code: E015_partial_mate_prune.py; tests: test_E015_partial_mate_prune.py; input witnesses: E012_WITNESSES.json. Compare E014_symbol_obstruction.py for the weaker at-most-once minimum sizes (6/5/3/5/5); the different values are expected, not contradictory.
- Literature check: Bright–Keita–Stevens EJC 2026 https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; Barnoff–Bright arXiv 2605.02132 https://arxiv.org/abs/2605.02132 ; no independently checkable complete resolution located in this iteration.
- All results are conditional on the specified first square or explicit fixed pairs; any search stopped by a time limit is UNKNOWN.
- **Next E016:** improve DFS with cell-to-transversal candidate lists (avoid scanning all 1000 transversals per cell), cache compatible bitset intersections, branch ordering by potential C-support, and benchmark against unpruned search on matched seeds/time. Then run a bounded scan across nonparatopic changed-A variants, seeking a pair with >=10 joint transversals and all 100 cells supported. Independently replay any candidate and exact-cover third mate before announcing a resolution.
