# E059 — Goal-backward falsification and exact endgame reformulation

**Date:** 2026-11-03 UTC. **Global status: OPEN.**

**Only success condition:** a valid 100/100/100 order-10 triple, or a complete unrestricted verified nonexistence argument. This iteration does **not** meet it. The MOLS10 hourly automation remains disabled, as requested.

## Literature and crucial correction to search frontier

- Egan & Wanless, *Enumeration of MOLS of small order*, Math. Comp. 85 (2016), 799–824, source data `neartripleMOLS10.txt`, https://users.monash.edu.au/~iwanless/data/MOLS/ . Their A,B are orthogonal; this iteration independently enumerates 14 common transversals and proves maximum disjoint packing 7, for **this fixed pair**.
- Jäger, Markström, Öhman & Shcherbak, *Enumeration of Sets of Mutually Orthogonal Latin Rectangles*, Electronic Journal of Combinatorics 31(1) P1.53 (2024), https://doi.org/10.37236/9049 , PDF https://www.combinatorics.org/ojs/index.php/eljc/article/download/v31i1p53/pdf/ , **Figure 3 (printed page 22)**. The paper already exhibited 3 mutually orthogonal 9×10 Latin rectangles. Our previous references to 7 rows as a meaningful leading constructive frontier were misleading: 9 rows are published, not new.
- Bright, Keita & Stevens, EJC 33(1) P1.30 (2026), https://doi.org/10.37236/13960 , restrict their SAT result to subsquare hypotheses. No independently verified unrestricted solution was found in targeted 2026-11-03 checks.

## Falsified proof obligation N-A — exact fractional counterexample

Old N-A conjecture: for every legal 4-row partial 3-MOLR(10), its full column-aware residual LP `Mx=1, x>=0` is infeasible. **FALSE**.

New constructive input: the cyclic partial 4-row triple `S_s(r,c)=(c+d[s,r]) mod 10` with offset rows

```
A: 0 1 4 8
B: 0 6 1 9
C: 0 7 9 2
```

All three row/column Latin conditions hold and all partial pair overlays have 40 distinct ordered pairs. Cyclic-shift symmetry quotients the full 360-row 6-resource LP to **36 difference-orbit equations**, with 42 allowed quotient placements. The independently checked primal chooses precisely 12 quotient triples, each weight 1/2. Lift each triple over 10 columns for **120 full placements**, each weight 1/2; independent no-SciPy JS and Python verifiers check all **360 rational equalities exactly**, with mutation rejection.

```
(u,v,w):
(2,5,1) (2,8,5) (3,2,6) (3,7,4)
(5,4,6) (5,7,3) (6,4,8) (6,8,3)
(7,3,5) (7,5,4) (9,2,1) (9,3,8)
```

The support has a 3-cycle of forced complementary choices and cannot be rounded by selecting just those 120 placements. The **full** 420-variable/360-equation integer relaxation of this *particular cyclic prefix* was solver-reported infeasible (HiGHS, complete), but no independent integer UNSAT proof was produced and the claim is not used as the main result.

A **bounded nonuniform cyclic-family screen** tested 4,402 valid k4 offset triples from 5,000 seeded generation attempts: 79 zero support, 4,056 numerical LP infeasible, 267 numerical LP feasible. Of those 267, full integer solver reported 241 infeasible and 26 UNKNOWN (0.12 sec/case), **zero confirmed SAT**; none of the unknown cases may be counted as UNSAT. These statistical samples do not imply a universal integer obstruction.

## Stronger falsification — exact **integer** counterexample through 2-MOLS(10)

For any `OA(n²,4,n,2)` (equivalent to a pair of MOLS(n)), a family of `k` disjoint common transversals induces three legal `k×n` MOLR with column-symbol and pair-symbol demands still **integrally completable**, by using all remaining OA points. This is a simple general constructive equivalence; novelty not claimed.

On published Egan–Wanless A,B (two genuine MOLS(10)), independently enumerated **14 common transversals** with **6,837 DFS nodes** and exactly **one** 7-disjoint-transversal pack; maximum pack size 7. Four of those transversals yield a legal **4×10 triple** with 40/40/40 overlays. The other 60 OA points give an **integer** placement exact cover of all **360/360** missing six-resource equations. The seven-transversal pack gives a legal **7×10 triple**, 70/70/70 overlays, and the other 30 OA points give an integer exact cover of all **180/180** missing equations. Independent Node.js verifier checked both and rejected deliberate corruption.

Thus both the universal k4 **fractional LP infeasibility** and the stronger universal k4/k7 **integer six-resource infeasibility** paths to global nonexistence are **provably invalid**. Neither relaxed witness is a full 3-MOLS(10): the remaining OA points have not been partitioned into legal new rows. This **row-factorization** is the missing global constraint. The same fixed published pair has no 8 disjoint common transversals (all 14 enumerated).

All 7 six-transversal subsets were checked for *all* possible 7th-row extensions (2/2/2/4/4/4/8 exact complete row solutions respectively, 26 total); all 28 resulting fixed seven-row prefixes admit no eighth row. This excludes only this finite anchored neighborhood, not arbitrary 7-row triples.

## Constructive 9-row frontier and last-two-row exact solver

We manually transcribed the three 9×10 arrays in Jäger et al. 2024 Figure 3 and independently verified every row, column, and the **90/90/90** partial overlays. Completing the unique missing symbol in every column forces three valid full Latin squares, whose overlay counts are **93/93/93**, with 7 duplicated and 7 missing ordered pairs for each of the three pairs. This published example is **not** a full triple.

For any fixed `(n−2)×n` Latin rectangle, missing symbols form a 2-regular bipartite graph (columns↔symbols); the last two Latin rows correspond exactly to its perfect matchings, enumerable by alternating choices on graph cycles. A true triple requires all three choices to have 100/100/100 overlays. A positive GF(4) order-4 control finds 2 complete witnesses from 64 last-two-row combinations.

For each of the **9 possible eight-row restrictions** obtained by omitting one row of Jäger et al.'s Figure 3 example, independently enumerated all choices of the last two Latin rows in each square. Per-square choice counts `[2,4,8,2,4,4,4,16,8]`. Exhaustively checked **5,392** candidate full triples across all nine fixed prefixes, with **zero 100/100/100**; maximum aggregate distinct-pair overlay count **279**, attained by 93/93/93. Python and separately written JavaScript verifiers agree. A bounded exhaustive one-square intercalate-swap scan detected 504 geometrically admissible 2×2 switches across the same nine eight-row subsets, **none preserved all three partial orthogonality conditions**. This does not exclude any other eight-row prefix.

### New endgame proof obligation

Given 9-row partial 3-MOLR, each pair of squares has a unique *missing-pair permutation* `pi_AB`, `pi_AC`, `pi_BC`. A complete 10th row requires the **composition identity** `pi_AC=pi_BC ◦ pi_AB`, *and* compatibility with each square's uniquely forced column completion. For the Figure 3 example the composition discrepancy is an odd permutation with only 4 fixed points and all three forced rows have only 3/10 required missing pair matches. This is a cheap **necessary** obstruction for any nine-row partial, not a new universal theorem.

## Main-goal decision / strongest next move

- **N-A fractional and N-A integer are closed as WRONG conjectures.** Do not spend further iterations trying to prove these universally, or generate more fixed-prefix duals as a proxy for global progress.
- **Existence route:** prioritize 9×10 MOLR last-row compatibility (or direct OA(100,5,10,2) construction), not 6→7 row count. Import published 9×10 MOLR data and use exact two-row endgame with invariant-aware global search, avoiding highly correlated local examples.
- **Nonexistence route:** must constrain the **five coordinates including ROW simultaneously**. Six-resource column/pair residual relaxations are insufficient even integrally. A certified, symmetry-complete direct 5-net solver remains a defensible but very large undertaking.
- **No defensible ETA.** Global orbit closures 0/162,959; neither resolution is in hand.

## Reproduce

- `python E059_cyclic_quotient.py 4 800` — fractional counterexample (seeded discovery); `python E059_verify_primal.py` — exact integer-doubled resource equality replay.
- `node E059_verify_independent.js` — independently validates all 3 relaxed witnesses and rejects deliberately corrupted one.
- `python E059_Egan_integral.py` — enumerate 14 common transversals, maximum pack 7, 4-row integer witness.
- `python E059_integral_k7_witness.py` — 7-row integer witness; `python E059_pack6_row8_hunt.py` — complete finite anchored 6→7→8 pilot.
- `python E059_2024_9x10.py`, `python E059_9row_permutation.py`, `python E059_8row_endgame.py`, `node E059_verify_endgame.js`, `python E059_endgame_control.py` — published 9×10 replay, endgame completeness and GF4 positive control.
- Result JSONs and SHA-256 manifest included in archive; no external secrets.

**Research status:** `OPEN`. MOLS10 hourly task remains disabled by user request; this was an on-demand experiment, not a future commitment.
