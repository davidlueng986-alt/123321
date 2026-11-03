# E063 — Closed attempt: symmetry-complete 7-class C-pattern and exact theorem-based exclusions

Date: 2026-11-03 UTC. **GLOBAL 3-MOLS(10) STATUS: OPEN.** The sole objective is a mathematically complete positive 100/100/100 construction or unrestricted negative proof. Hourly automated work remains disabled.

## 1. Hypothesis / direct closure chain

If there is a complete orthogonal triple (A,B,C) extending the 70 known third-square cells of the seven common transversals from the Egan-Wanless pair, then C belongs to a finite explicitly enumerated family. Exhaustively classify **every** C completion up to symmetries preserving this fixed pattern, then try to find two orthogonal Latin mates A and B for each canonical representative. This does **not** cover all possible order-10 triples. Any SAT output would be independently tested for three Latin squares and all three pairwise 100/100 overlays; complete UNSAT with coverage would only exclude this fixed pattern.

## 2. Exact finite classification (complete within the fixed pattern)

- The E062 seven-symbol-class pattern has 70 fixed C entries, 30 blanks, and exactly three missing symbols per row/column (symbols 1,2,3).
- Fully enumerated all row permutations of the three missing symbols (six options per row) with column uniqueness enforced: **216 valid 10x10 Latin-square completions**. A separate `verify_E063.py` reproduces the complete 216-member set and checks all rows, columns, and the 70 fixed clues.
- The unlabeled blank-cell row-column bipartite graph has six color-preserving automorphisms; exactly three respect the seven fixed symbol-classes up to symbol relabeling. Combine these with the six permutations of the three unfixed symbols: exactly 18 explicitly certified symmetry actions.
- Verified all 18 actions on all 216 completions and their complete orbit partition: **14 equivalence orbits**: eleven orbits of 18 completions and three of 6 completions. Representative indices `0,1,2,3,4,7,8,9,11,15,17,18,25,32`.

## 3. Mathematical branch closures, not solver guesswork

McKay, Meynert, Myrvold, *Small Latin Squares, Quasigroups, and Loops*, J. Combin. Designs 15 (2007), 98–119, DOI https://doi.org/10.1002/jcd.20105, prove that a Latin square of order 10 contained in an orthogonal triple must have **trivial autoparatopism group**.

- Representatives **4, 11, 32** have explicit *nontrivial autotopisms* (a fortiori autoparatopisms). Each certificate consists of permutations of all 10 rows, columns and symbols; the equation `C[row_perm[r]][col_perm[c]] == sym_perm[C[r][c]]` is checked at all 100 cells.
- Hence **three of the fourteen orbits**, representing **18 of the 216 labeled completions**, are definitively impossible as a C square in a complete triple. This theorem application requires no belief in a numerical solver's UNSAT status.
- An independent quasigroup constraint propagation program checks autotopisms of all fourteen representatives. A second independent six-coordinate-parastrophe audit checks all six permutations of the row/column/symbol roles. It confirms that the other eleven representatives have trivial autoparatopism, so this particular theorem cannot immediately exclude them.
- `verify_E063.py` independently validates the orbit cover and the three explicit symmetries and deliberately mutates one certificate; the mutation is rejected. Final exact verification status `E063_FINITE_PATTERN_CERTIFICATES_VERIFIED`.

**Scope:** This excludes only three orbits under a fixed source pattern. It does not eliminate any complete E033 first-two-row `(f,g)` class and is **not** 3/14 progress toward the unrestricted global proof.

## 4. Actual complete-solver attempts (all appropriately labeled)

- The five-coordinate OA Z3 solver keeps A and B entirely free, with the 70-entry C pattern fixed. 17,146 binary candidate tuples, 1,000 exact-cover constraints, 171,460 incidences; 25-second direct solve returned **UNKNOWN / timeout**.
- With each of the fourteen complete C orbit representatives fixed, the exact solver has 5,050 candidate tuples and 1,000 exact-cover constraints. All fourteen bounded runs returned **UNKNOWN**, none SAT or UNSAT (first five at 5 s, remaining nine at 2 s; see JSON records).
- An independently written one-mate DLX on complete C needs only 730 candidate `(row,col,A_symbol)` choices and 400 exact-cover constraints; first four cases were tested to 10 million nodes each and all remained **UNKNOWN_BUDGET**. The Z3 one-mate solver on three representatives with 6-second limits also returned UNKNOWN. HiGHS MILP on representative 0 with 788 transversal options reached its 6-second limit without a feasible integer solution or proof.
- All fourteen C representatives have 780–864 single-C transversals; the GF(2) exact-cover column-span necessary condition holds for all (rank 73), so this simple necessary condition excludes none. No claim of universal failure follows.

## 5. Decision and next proof obligation

The rigorous fixed-pattern orbit reduction is a useful reusable technique, but the unrestricted **CLOSED** result is still missing. For the remaining eleven C orbits, either produce one complete pair of orthogonal mates A,B (independently verify 100/100/100), or a complete checkable negative proof for each to exclude this **one** 70-clue pattern. For the unrestricted problem, must still cover all 3-MOLS(10) patterns via sound global normalization/symmetry, or find a full triple directly.

**Priority:** no more pure DLX CPU sweeps without conflict-learning; explore an LRAT/DRAT-capable SAT representation of the complete five-coordinate OA plus global symmetry coverage. The MOLS10 hourly automation remains off. Do not promise a solution date.