# MOLS10-E002 — Exact fixed-pair nonextension certificates (2026-11-01)

**Scope: two specific orthogonal pairs, NOT the unrestricted 3-MOLS(10) problem.**
Original matrices: Egan & Wanless, https://users.monash.edu.au/~iwanless/data/MOLS/neartripleMOLS10.txt .
The first three Latin squares are A, B, C. A/B and A/C are orthogonal, B/C is not (91 distinct pairs).

## Lemma: fixed-pair extension iff 10 disjoint common transversals
For a fixed orthogonal pair X,Y of order n, each symbol class of any third Latin square Z orthogonal to X and Y has exactly one cell in each row, column, X-symbol and Y-symbol. These are n pairwise disjoint common transversals, covering all n² cells. Conversely, if n disjoint common transversals exist, label their cells 0..n-1 to construct a Latin Z orthogonal to X,Y. Thus an exact transversal enumeration with maximum disjoint packing <n proves this fixed pair has no third mate.

## Pair (A,B), 0-based indices (0,1)
SHA256(json.dumps([A,B], separators=(',',':'))):
47f9bad62f68b317ff0fc8ae72278b07355ceac64a502e2af0030473d0c405c2

Exactly 14 common transversals, each represented by 10 column digits in row order:
```
0312978456
0386741592
0419285367
0456897123
0564231978
0564978123
0752639814
0978312645
4681503792
5249160387
6735024819
7104985263
8520679134
9063748521
```
12 uncovered cells (0-based row,col):
(0,1), (0,2), (0,3), (1,8), (2,9), (3,7), (4,4), (5,5), (6,6), (7,0), (8,0), (9,0).
Maximum number of pairwise disjoint common transversals = 7 (EXACT subset search). Hence **no third mate for this exact A,B**.

## Pair (A,C), 0-based indices (0,2)
SHA256(json.dumps([A,C], separators=(',',':'))):
6db5f6f5d6e1bb0743c6a9e59eeb633ac0490f8a001975083065a4f2b2b79018

Exactly 7 common transversals:
```
0123456789
0231978456
0312645897
0456789312
0564123978
0645897123
0789231564
```
36 uncovered cells; maximum disjoint packing = 1 (EXACT). Already fewer than ten possible symbol classes, so **no third mate for this exact A,C**.

## Reproduction and independent replay
```bash
cd research/mols10
python3 -m unittest discover -p 'test_*.py' -v
python3 transversals.py near_triple.json --pair 0 1 --output pair_AB.json
python3 transversals.py near_triple.json --pair 0 2 --output pair_AC.json
```
The script enumerates all 10! row-column permutations, checks both symbol uniqueness conditions, and independently repeats enumeration using a separate bitmask DFS. It then exhaustively searches all disjoint subsets (14 or 7 candidates). The input pair is validated as Latin and orthogonal. No timeouts or heuristic search are used in these certificates.

**Interpretation:** This does NOT prove 3-MOLS(10) impossible, nor does it show these results are novel in the literature. It provides a verified screening criterion for selecting new pairs: number of common transversals, cell coverage, and maximum disjoint packing.
