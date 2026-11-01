# MOLS10 E006–E007: k-symbol trade neighborhoods and independent Parker-A sampling

Research date: 2026-11-02. The general three-MOLS(10) existence question remains **OPEN**. All tests below hold for a **fixed** first Latin square A and a selected valid orthogonal mate B. No general nonexistence claim.

## E006 — Exact local re-partition of k symbols (k=3,4,5)

A k-symbol trade is defined by selecting k B-symbol classes, forming their union of k*n cells, and re-partitioning this exact support into k A-transversals (each meets rows, columns and A-symbols once). Re-coloring the chosen transversals yields a new B' still Latin and orthogonal to A. The implementation enumerates **all** such alternative partitions on each selected support, unless a numeric cap is reached; cap usage is reported explicitly.

Implementation: `k_symbol_trades.py` (`repartitions_on_support`, `scan_k`), with independently verified witnesses and `test_k_symbol_trades.py`. The experiments below did **not** hit the 1000-solutions-per-support cap. This is an exhaustive examination of the **restricted k-symbol support neighborhood**, not the entire space of mates, not a proof of global nonexistence, and not an unrestricted k-cell trade.

| Pair, fixed A/B | k | Possible selected supports | Supports with proper alternative | Verified alternative partitions | Best common transversal count among neighbors |
| --- | ---: | ---: | ---: | ---: | ---: |
| Egan A/B | 3 | 120 | 0 | 0 | — |
| Egan A/B | 4 | 210 | 3 | 6 | 4 (baseline 14) |
| Egan A/B | 5 | 252 | 18 | 36 | 4 (baseline 14) |
| Egan A/C | 3 | 120 | 24 | 24 | 1 (baseline 7) |
| Egan A/C | 4 | 210 | 84 | 93 | 3 (baseline 7) |
| Egan A/C | 5 | 252 | 162 | 237 | 3 (baseline 7) |
| Parker A/B | 3 | 120 | 22 | 26 | 0 (baseline 0) |
| Parker A/B | 4 | 210 | 70 | 98 | 0 (baseline 0) |

Every counted neighbor is verified Latin and orthogonal to the fixed A. No neighbor passes the necessary >=10 common-transversals/full-cell-support screen. Number of alternate partitions ignores symbol relabeling duplicates within each support but may contain duplicates across different supports.

**Structural observation:** The famous near-triple A/B pair is **locally isolated** under complete re-colorings of any two or three B-symbol classes. Four/five-symbol flips exist, but none tested yields more than four common transversals. This makes simple small-support repair around that exact pair a less promising investment; it does NOT rule out six or more symbols or changing A.

## E007 — Bounded Parker-A mate sampling

Parker A has exactly **1104** single-A transversals. Under the same seeded exact-cover algorithm as E004, 12 seeds (0–11), 20000-node hard limit and **0.5-second per-seed** timeout:
- **11** searches returned `UNKNOWN_BUDGET` — not UNSAT.
- Seed **8** returned a valid additional first-row-normalized orthogonal mate B' after 303 nodes, independently passing the Latin-and-orthogonality verifier.
- The new *labeled* mate differs from the historically printed Parker B after a simple first-row symbol normalization. This does not establish nonisomorphism.
- This seed-8 pair has **0** common transversals and is therefore also unextendible as a *fixed pair*.
- A prior unbounded-in-aggregate 40-seed Parker run was interrupted by an execution timeout, and must remain labeled `UNKNOWN_TIMEOUT`.

Repeat the bounded experiment using:
```python
from sample_mates import transversals_single, make_mate, transversals_pair
from verify import analyze
import json
A, B = json.load(open('parker_pair.json'))['squares']
T = transversals_single(A)
assert len(T) == 1104
statuses=[]
for seed in range(12):
    mate, result = make_mate(A, T, seed, node_budget=20000, second_budget=0.5)
    statuses.append(result['status'])
    if mate is not None:
        assert analyze([A,mate],10)[0]['orthogonal']
        print(seed,len(transversals_pair(A,mate)[0]))
print(statuses)
```

**Reproducibility warning:** Wall-clock timeouts are hardware sensitive, hence exact per-seed UNKNOWN/SAT counts need not be stable on all runners. Seed 8 can be replayed with a sufficient budget and is independently checked via the witness predicate. The correct statement is that the **observed** execution produced 11 unknown and one witness.

## Next priorities

1. Stop spending substantial compute on near-triple A/B under <=5-symbol re-coloring. Choose a genuinely new first Latin square or search 6+ symbol high-support trades if justified by lower-cost screening.
2. Optimize bounded Parker-A mate generation, measuring node/time efficiency and diversity, and keep separate SAT/UNSAT/UNKNOWN states.
3. Investigate a candidate generator biased toward high **common transversal cell coverage** rather than arbitrary orthogonal mates; count+coverage are necessary but not sufficient for an extension.
4. Review the broader published 2026 SAT literature before making novelty claims, and separate a fixed-pair certificate from a universal conclusion.

See also `E003_E005_REPORT.md` and `E003_E005_RESULTS.json`.
