# E069 — Independent mathematical and implementation audit (2026-11-07)

**Source:** Google Drive `E069_R2_R4_CLOSED_ATTACK.zip` (2026-11-06) and `E069_REPORT.md`. Audited local original files without changing them. **3-MOLS(10): OPEN.** This is NOT a claim that any global order-10 branch is UNSAT.

## Verdict

**R2.2: a genuine but very specific sound 64-literal no-good, not a minimal defining set and currently *zero* pruning in the 1,700 E064 canonical branches.**

**R2.1: Egan-specific rigidity claim independently reproduced; useful conditional fact but NOT a global restriction or a general constructive algorithm.**

**R4: partly meaningful algebraic / structural sanity checks; code does NOT establish the full named 'universal theorems' claimed by the report, and it generates no general contradiction.**

**R2.3: new CP-SAT implementation gives relevant small-n controls and n10 UNKNOWN, but three purported n6 paratopy-class tests are actually three repeats of the unbranched model.**

## Primary findings

1. **Independent unique completion of the 64-clue core is CONFIRMED.** An independent Python bitset Algorithm X (no E069 C++ DLX internals) enumerated 5,131 allowed 4-coordinate `(row,column,A,B)` placements satisfying 64 clues. All 600 2-net / pair-orthogonality resource classes were required exactly once, with no extra normalization. It exhausted the exact-cover search in **13,100 nodes**, finding exactly one full A/B pair, equal to the original orthogonal Egan–Wanless A/B. Thus the negative clause is **sound**: if a triple contained all 64 clues, the pair would be the unextendable Egan pair.

2. **The advertised deletion minimality of 64 clues is FALSE.** E069's greedy minimizer calls `is_uniquely_forcing(mask, 20000)` and retains a clue whenever solving exceeds 20,000 nodes; this does NOT mean the smaller clue set is non-unique. We independently reran 64 leave-one-out exact covers using a separate C++ exact cover implementation with 500,000 nodes per test. For **37 of 64** deletions, a unique solution was **exhaustively** proven (0 cap). For another 27, the new run hit the cap and made no mathematical claim. In particular, deleting **original literal index 2** gives exactly the same unique Egan pair: **41,814 exhaustive C++ nodes**, and an independent Python bitset search confirms **46,382 nodes, exactly one full pair**. Hence **a 63-literal core is already certified**, and the 64 set is certainly *not deletion-minimal*. The globally minimal size is NOT known.

3. **Exported single clause is completely inert on current E064's 1,700 root branches.** Under E065's standard gauge, E069's 64-clue pattern contains the B-first-column requirements `(r,B[r,0]) = (1,2), (5,9), (7,5)`. Exhaustively checking all 1,700 canonical `B_col0` permutations found **zero** simultaneously matching them. Therefore the single *fixed-orientation* 64-literal clause is already satisfied at branch root in **1,700/1,700 classes**. It excludes no branch and no node in current canonical branch searches. Symmetry-orbit transforms or an adaptive defining-set clause generator could in principle be useful, but **E069 did not implement or benchmark either**. Five of the 64 literals are fixed true by the E065 normalization even before selecting a branch.

4. **R2.1 Egan-rigidity is CORRECT as a restricted enumeration.** Recompiled E069's C++ DLX (with its E068 source data correctly mounted) and independently reproduced `(k=7: 1 unique / 1 pack, 31 nodes; k=6: 7/7, 287; k=5: 24/24, 1224; k=4: 51/51, 4426)`, no capped search for k>=4. E069 also tests k=3 but all 65 such searches hit the 100,000-node cap; they are **UNKNOWN**, not excluded. The rigidity claim says nothing about orthogonal pairs *not* matching these special Egan partial patterns.

5. **R2.3 n=6 three-branch control is mislabelled.** E069 reads `E065_n6_branches_pb.jsonl` as though each result record contains `B_col0`/`C_col0` (or `f`/`g`), and passes absent values as `None`. The actual E065 records contain `n,branch,status,seconds,assumptions,placements` only; none contain these permutations. Thus E069 called `solve_full_oa_cpsat(6, f_col=None, g_col=None)` **three times**, not three distinct canonical branches. Its separate unbranched n6 UNSAT control could be valid (n=6 nonexistence is known); the claimed 3/3 branch benchmark is not valid as labelled.

6. **R4 evidence is overstated.** The GF(2) formal parity system and its 512-to-32 projection are legitimate calculations for the *chosen abstract linear equations*, but they do not prove every geometric 4-net / every actual 2-MOLS pair has an extension to 5-net; nor do they establish no possible stronger parity obstruction. The published Francetić–Herke–Wanless result is formulated as an **upper bound on actual OA parity information dimension**, not equality for all realizable OAs. The 5-star weight identity and symbolic Gram spectra are reasonable necessary-condition / feasibility exercises, but produce **no contradiction**. Crucially `audit_r4_bose_mesner_and_snf()` simply **hardcodes** `srg_krein_feasible: True`, does not compute Krein parameters, and does **not compute Smith normal form**, despite reporting these as completed audit results. The code samples 1000 codewords from a particular Egan **4-net**, but that is not a standalone proof of the purported universal 5-net Hull identity.

7. **The supplied ZIP cannot replay standalone as claimed.** `E069_REPLAY.sh` uses four externally expected folder paths (`E068_COMPLETE_ARCHIVE`, `E067_MOLS10_GLOBAL_CONSTRAINTS_AUDIT`, `E065_MOLS10_DIRECT_SAT_CLOSED_ATTEMPT`, `E064_MOLS10_CLOSED_ATTEMPT`) and outputs into `e069/`, none of which appear as such in the archive. `node E069_independent_verify.js` fails when run after simple unzip (missing `e069/E069_64_defining_core.json`); the JS also only verifies the 64 clues *match Egan values*, not that they force a unique pair. Code paths must be corrected before claiming self-contained reproducibility.

## CLOSED-oriented decision

- **Keep:** the rigorous unique-pair core concept and transversal-pack rigidity conditional as candidate **R1 sound cuts**; the independent Python/CP-SAT approach with corrected benchmark controls.
- **Reject or correct:** the 'deletion-minimal 64' claim, the 'all three n6 canonical classes tested' claim, the false standalone replay claim, and unproved R4 'theorem' / computed-Krein/SNF claims.
- **Do not prioritize:** more Egan-specific minimizing for its own sake, without evidence that symmetry lifting / dynamic nogood generation improves global E064 branch search.
- **High-value next test:** generate sound **symmetry-orbit-aware** defining-set cuts or dynamically extract uniquely-forcing cores from *generic* partial orthogonal pairs, then measure genuine solver conflicts/search reduction and LRAT-safe proof lifting across all 1,700 canonical classes. Preserve direct SAT witness and global UNSAT routes.

**Global result after E069 review:** 0/1700 verified order-10 UNSAT branches, 0 full 100/100/100 witnesses. **OPEN**.

### Independently certified immediate correction

`E069_63_CERTIFIED_CORE.json` and `E069_63_nogood_e065_dimacs.txt` remove original E069 core literal **index 2** and preserve *exactly one* Egan–Wanless orthogonal pair completion (independent exhaustive C++ and Python searches above). The derived 63-literal clause is a mathematically sound stronger local no-good, but, like E069's original fixed-gauge 64-literal clause, it has **no direct effect on all 1,700 E064 canonical root branches without symmetry lifting**. The 63-literal core is **not claimed minimal**.
