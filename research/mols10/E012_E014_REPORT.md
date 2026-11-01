# MOLS10 E012–E014 — new first-square pairs and minimal local obstruction certificates

**Research timestamp:** 2026-11-01T18:52:10Z (UTC). **Global status:** OPEN. **Scope:** all claims below are for particular explicit pairs or finite tested first-square variants, never a global solution.

## External status check (performed before this iteration)
- Bright–Keita–Stevens, *Myrvold's Results on Orthogonal Triples of 10 × 10 Latin Squares: A SAT Investigation*, Electronic Journal of Combinatorics 33(1), P1.30, 2026-02-13: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30
- arXiv:2503.10504v2, 2026-01-21: https://arxiv.org/abs/2503.10504 (explicitly says unrestricted triple remains open).
- Barnoff–Bright, *Improving SAT Solvers on Orthogonal Latin Square Problems*, arXiv:2605.02132, 2026-05: https://arxiv.org/abs/2605.02132 (improves discovery of PAIRS, not triples).
- Bright–Keita–Stevens, *Orthogonal Latin Squares of Order Ten with Two Relations*, arXiv:2509.09633v3, 2026-08-20: https://arxiv.org/abs/2509.09633 (restricted PAIR classification, not full triple resolution).
- No independently checkable new 100/100/100 witness or unrestricted nonexistence proof was found as of this search. Absence of a found paper is not a proof of absence.

## E012: Bounded HiGHS exact-cover on changed first square A

Unlike E004/E007, E012 does NOT hold the original first square fixed. Take the 48 verified nontrivial two-symbol trades of Egan A (E011). Each new A has 840–1000 A-transversals, distinct from the original A's 1080, and is therefore nonparatopic to original A.

MILP binary variable x_T for each A-transversal T, with 100 cell constraints sum_{T containing cell} x_T = 1. Selected 10 transversals become B symbol classes. **SAT** requires independently verified integral exact cover and pair overlay 100. HiGHS time limit is 6 s per case.

- Trade index 12 (symbols 1/2, 14 cells, 904 A-transversals): **SAT** in 4.297 s, explicit A,B in E012_WITNESSES.json; Latin + overlay 100 checked. All 10! permutations independently scanned: **0 common A/B transversals**.
- Trade index 20 (symbols 2/3, 14 cells, 904 A-transversals): **SAT** in 4.729 s, explicit A,B in E012_WITNESSES.json; Latin + overlay 100 checked. All 10! permutations independently scanned: **0 common A/B transversals**.
- Trade indices 30 (892), 40 (1000), 47 (840): **UNKNOWN_TIMEOUT**, 6 s each, not UNSAT.
- Positive control original A at 5 s: **UNKNOWN_TIMEOUT**, illustrating that a timeout cannot be taken as a structural obstruction.
- A further bounded weighted MILP on trade_12 to construct C orthogonal to A: **UNKNOWN_TIMEOUT_NO_INCUMBENT** (12 s).
- Trade_20 weighted MILP found a verified C with overlays **100/100/69** in 12 s; solver timed out with incumbent, gap about 0.10145, so **69 is NOT optimal**. This is a near-triple, not a 3-MOLS solution.

**Code:** E012_milp_traded_A.py, E012_WITNESSES.json, first_square_trades.py, sample_mates.py, verify.py. **Regression:** test_E012_E014.py. The explicit witnesses, not solver success labels, are the authoritative evidence.

## E013: Rejected single-transversal compatibility filter

For any A-transversal T used as one B-symbol class in a hypothetical triple, the union of A-transversals U with |T∩U|=1 must cover every cell (because the C-symbol classes would have this property). Implemented E013_compatibility_screen.py and checked original Egan A plus all 48 E011 traded A. All **49** first squares pass for **every** T: 0 excluded, compatibility degrees ranged 241..437, runtime about 7.1 s. Thus the filter is **vacuous** on this tested set; do not repeat without strengthening to joint constraints from multiple B classes.

## E014: Exact *minimum B-symbol* local obstruction (new conditional result)

Fix any orthogonal Latin pair (A,B), a subset S of B-symbols, and a cell x. If every A-transversal T containing x repeats at least one symbol from S in B, then **no third square C orthogonal to both A and B can exist**, since the C-symbol class containing x must be an A-transversal with all ten B symbols distinct.

To find the smallest possible |S| for this local obstruction, enumerate ALL A-transversals and ALL subsets S of size 0,1,... until some S blocks a cell. The exhaustive lower-k checks are essential to the **minimum** claim.

| Fixed pair | A-transversals | Minimum | Number of blocking subsets at minimum k | Exact example S | Blocked cell (0-based) |
|---|---:|---:|---:|---|---|
| Egan A/B | 1080 | **6** | 36 of 210 | {0,1,2,3,4,9} | (4,4) |
| Egan A/C | 1080 | **5** | 6 of 252 | {1,5,7,8,9} | (0,2) |
| Parker A/B | 1104 | **3** | 1 of 120 | {7,8,9} | (7,7) |
| Traded A/B index 12 | 904 | **5** | 2 of 252 | {0,2,6,8,9} | (1,1) |
| Traded A/B index 20 | 904 | **5** | 7 of 252 | {0,1,4,6,8} | (3,1) |

**Independent verification:** for EACH of the five listed certificates, a separate brute-force loop over all **3,628,800** column permutations confirmed the exact A-transversal count and **zero** eligible A-transversals through the blocked cell. This is independent of the bitmask DFS used to discover the obstruction. The smaller subsets were exhaustively checked in E014_symbol_obstruction.py; all had full cell coverage. Parker's particularly short conditional obstruction needs only three B-symbol constraints.

**Interpretation:** this is a structural explanation of why each of these **specific pairs** cannot extend, with small falsifiable local certificates. It does **not** eliminate other orthogonal pairs, nor prove unrestricted 3-MOLS(10) impossible. No literature novelty claim without comparison to prior combinatorial obstructions.

**Reproduction:**
```bash
cd research/mols10
python3 E014_symbol_obstruction.py
python3 -m unittest -v test_E012_E014.py
# optional (SciPy / NumPy): python3 E012_milp_traded_A.py --seconds 6 --indices 12 20 30 40 47
python3 E013_compatibility_screen.py
```

**CI:** https://github.com/davidlueng986-alt/123321/actions/runs/41338759633 (E012/E014 regression passed). Core commits: 810874a5f9e9b790a86b99c3203a9f35bd56158c, 7a3636335a307aece1c5ad578a27503aff48dc4f, 78bde9bf8a142b6fb56b19c9cd9f6aea64bc739e, efd4ffca8d22567b0816e8f741b57665a8f4a4d4.

## Next action E015

**Stop uniform random pair sampling as the primary approach.** The observed new-A mates have 0 common transversals; E013 one-transversal coverage is too weak. Derive a *joint* compatibility filter for 2–4 selected B-symbol classes (partial partition), using bitset intersections of A-transversal collision masks; prune partial mate exact-cover nodes as soon as some cell becomes blocked. Validate this pruning against known GF(4) triples (must not reject) and all five fixed-pair obstruction certificates (must reject). Then perform a strictly bounded coverage-directed search for a changed-A pair with >=10 common transversals and all 100 cells supported; only such a pair merits third-square exact cover.

**Uncertainty:** external literature could contain unindexed new work; only two new pairs were produced, and their fixed-pair nonextension is exact. No global existence/nonexistence inference. Solver timeouts are UNKNOWN. 
