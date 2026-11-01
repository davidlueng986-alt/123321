# MOLS10 E016 — exhaustive exclusion for 49 specified first squares (not global)

**Timestamp:** 2026-11-01 19:51 UTC. **Problem status:** OPEN. **Source baseline:** `STATE.json` at 571a685085f11cd1b08139739c648a5b31558736; living Google Doc https://docs.google.com/document/d/1NDPWEMM3Cf5HrhdOcV6pVE9tCI-kxKbavxcfIBFva3k/edit .

## Literature / external claim recheck

Primary Bright–Keita–Stevens, *Electronic Journal of Combinatorics* 33(1), #P1.30, published 2026-02-13: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 . It explicitly says unrestricted 3-MOLS(10) remains open and only studies a restricted 4x4-subsquare hypothesis. Barnoff–Bright, arXiv:2605.02132v2, revised 2026-07-04, https://arxiv.org/abs/2605.02132 : improved SAT search for *pairs*, not an unrestricted triple. New web searches through 2026-11-01 found no independently replayable global positive or negative resolution. Absence from search is not a proof.

## New mathematical/computational finding

Fix **one specific** order-10 Latin square A. Enumerate *all* A-transversals T. A possible orthogonal mate B must partition the 100 cells into ten disjoint A-transversals T_i. If a third square C exists, each C-symbol class U is another A-transversal and intersects each T_i in **exactly one cell**.

Define `Compat(T)={U: |U intersection T|=1}`. For a partial partition `T_1,...,T_k`, every C-symbol class must belong to the intersection `P = intersection_i Compat(T_i)`. If there is any cell not covered by any U in P, **the partial B cannot extend to a triple**. This is the E015 sound necessary condition. We now search **every** B-partition, not just a time-limited prefix.

E016 precomputes `Disjoint(T)` as a bitset of A-transversals disjoint from T, maintains an `eligible` bitset by AND as B classes are chosen, and branches on the uncovered cell with the fewest eligible transversals (MRV). It never scans all A-transversals for every cell at every node. The full DFS returns `UNSAT_FIXED_A_EXHAUSTIVE` only when recursion returns naturally without node/time budget exceptions.

**Results:** The original published Egan–Wanless first square A (1080 transversals) and **all 48** proper two-symbol first-square trade variants from E011 were individually exhausted with no viable complete B partition. These are 49 named Latin squares, NOT all Latin squares of order ten. Original A: **24,875 DFS nodes**, 18,407 rejected by sound C-support pruning. Across 48 variants: **825,696 nodes**, 635,258 rejected; each search exhausted after 12,971–23,984 nodes. Total 49: **850,571 nodes**, 653,665 support prunes. No timeout and no full-support B found. The original-A result is stronger than E008/E010 (which only fixed A together with one other square). It is a **conditional fixed-first-square nonexistence computation**, not a universal theorem about order ten.

## Verification and benchmark

Matched baseline E015 slow MRV vs E016 eligible-bitset MRV, **identical seed, same 1,200-node cap**, changed-A indices 12/20/30 and seeds 0/1 (six matched pairs). The six baseline DFS times were 1.1266–1.2487 s; optimized DFS 0.0474–0.0528 s (approximately 21–26x **DFS-only** speedup, excluding setup). Every pair had identical node and prune counts (e.g. index12 seed0 1200 nodes/905 prunes). This is a speed comparison, not a mathematical advance by itself. E015-style slow-mode enumeration independently completed index12 at 17,377 nodes/13,324 prunes; optimized completed with identical counts. A different fast seed independently completed original A with 24,875 nodes/18,407 prunes.

**Positive control:** GF(4) order-four example is not rejected: `SAT_SUPPORT_ONLY`, 5 nodes, 4 compatible C-transversals. The support condition is necessary, not sufficient: `SAT_SUPPORT_ONLY` is *not* a triple witness and must undergo independent exact-cover completion and 100/100/100 replay. Regression tests check the compatibility and disjoint bitset invariants. Independent machine-checked DRAT/FRAT or proof-assistant certification has NOT been generated; these are reproducible exhaustive program traces, and source-code correctness remains an audit obligation.

**Inputs:** `near_triple.json` (published Egan–Wanless A), `first_square_trades.py` (48 deterministic trades), `E015_partial_mate_prune.py` (`setup`), `verify.py`. **Code:** `E016_bitset_search.py`; **results:** `E016_RESULTS.json`; **tests:** `test_E016_bitset_search.py`.

Reproduce:
```bash
cd research/mols10
python E016_bitset_search.py --original --indices 12 20 30 --seed 0 --nodes 250000 --seconds 30
python E016_bitset_search.py --original --seed 0 --nodes 250000 --seconds 30 --output E016_replay_all49.json
python -m unittest test_E016_bitset_search -v
```
The second command defaults to all 48 indices. Budget exhaustion must be reported `UNKNOWN_BUDGET`; never silently infer UNSAT. `E016_RESULTS.json` stores all 49 node/prune counts, not a cryptographic proof trace.

## Failed routes and uncertainty

All 49 tested first-square instances were excluded, so none yields a candidate full-support pair. This is *negative evidence for a tiny, explicitly defined neighborhood*, not a statement about the unrestricted space. Earlier E015 4-second runs were UNKNOWN and are superseded **only for these fixed A instances** by completed E016 DFS. The speed ratio omits setup costs; do not extrapolate it to all MOLS searches. External novelty relative to older specialized computational searches is unknown.

**Next E017:** (1) independently audit the exhaustive DFS and first-square variant generation with a structurally different exact-cover/SAT model and independent transversal enumeration; (2) identify other first squares outside the one-trade neighborhood, preferably from published pair catalogs or multiple trades, with proven nonparatopy or invariant diversity; (3) run the bounded first-square exclusion test and preserve `UNKNOWN` honestly. No global 3-MOLS(10) solution found; keep research running.
