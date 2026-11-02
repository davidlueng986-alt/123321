# E036 — Constructive six-row coverage for the 2^5 first-row cycle type
2026-11-02 12:46–12:52 UTC. GLOBAL 3-MOLS(10) STATUS: OPEN.

## Primary-source status
Checked Bright–Keita–Stevens (Electronic Journal of Combinatorics 33(1) P1.30, 2026-02-13), https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 and arXiv:2503.10504v2; Barnoff–Bright (arXiv:2605.02132v2, revised 2026-07-04), https://arxiv.org/abs/2605.02132. Targeted fresh 2026-11-02 searches found no independently checkable unrestricted resolution. Absence of search hits is not proof.

## Objective
E033 proved 12 derangement cycle types for the normalized second row f of A. For f=(01)(23)(45)(67)(89), C(f) acts on 440192 legal second rows g of B, producing 156 orbits. E035 had biased local prefix failures. Test the falsifiable opposite hypothesis: does EVERY g-orbit for this f admit some six-row partial 3-MOLS, with C row1 and all subsequent rows free?

## Exact finite constructive result
YES for all 156 representatives. Deterministic exact row-permutation DFS produced three 6x10 arrays for each g; every row is a permutation, each column has six distinct symbols, and each of the three overlays has 60 distinct ordered pairs. Independent Node.js replay verified all 156 witnesses and all 440192 legal g via disjoint centralizer orbit union. By conjugacy the statement covers all normalized f of cycle type 2+2+2+2+2, but only this one of E033's 12 cycle types. Therefore mere existence of a six-row partial triple cannot exclude any such (f,g) orbit. This is a restricted constructive theorem, NOT a complete 3-MOLS(10) witness, and novelty relative to published work is unknown.

Deterministic generated six-row witness JSON SHA256: 5b198704a6cd24cae9ba57b7f938ce121aba182df1fc78738d39ab92a2aff66f . Maximum single-row DFS nodes 12846. The witness JSON is generated locally by committed code, not claimed as an uploaded GitHub data file.

## Bounded failure evidence and two seven-row witnesses
For each of 156 fixed five-row prefixes, tried up to 20 seeded sixth-row choices and exact seventh-row DFS. 3093 sixth-row choices SAT; 3091 exact seventh-row UNSAT for THOSE FIXED six-row prefixes; 2 seven-row prefixes SAT, independently replayed with overlays 70/70/70 (indices 39 and 47). Both seven-row prefixes are nonextendable to eight rows when held fixed: independent column-aware residual support check finds 9 allowed candidate variables with 133 unsupported mandatory constraints for index39, and 4 candidates with 156 unsupported constraints for index47. These local UNSAT results do NOT exclude any entire g-orbit.

Secondary local 10-restart-per-g search: all 156 reached six rows, zero reached seven. A 50-restart exploratory batch was interrupted before final output and is NOT counted as a completed experiment. All completed 3093 seventh-row checks were SAT or exact fixed-prefix UNSAT, no UNKNOWN. None of this proves global nonexistence.

## Reproduction (stdlib only, no GPU)
Run in research/mols10:
1. python E036_reproduce.py (enumerates orbits, constructs and validates 156 six-row witnesses, emits E036_WITNESSES.json, checks exact SHA256).
2. node E036_verify.js (independent 440192-g orbit union and witness checks; deliberate corrupted witness must be rejected).
3. python E036_lookahead_reproduce.py (bounded 3093 fixed-prefix checks; emits two E036_K7_WITNESSES.json).
4. node E036_verify_k7.js (independent 70/70/70 and exact column-aware zero-support check).

Exact code and data-summary commits:
- generator https://github.com/davidlueng986-alt/123321/commit/d5c4c4ec0c8ee3c390ced97e480702574dabc9b4
- independent verifier https://github.com/davidlueng986-alt/123321/commit/94cd88b4628aa129697c309c5105f6aef74f8769
- bounded lookahead https://github.com/davidlueng986-alt/123321/commit/dba75521371ce23d8d3f0029972252464b545934
- independent k7 checker https://github.com/davidlueng986-alt/123321/commit/db1679b0f6c69df7344b7dc21af77efa393500dc
- summary https://github.com/davidlueng986-alt/123321/commit/13e6029152211e9453295a925ecf4bee79192afb

## Next action and uncertainty
Do NOT use greedy fixed-prefix UNSAT to prune an entire globally canonical g-orbit. Integrate sound column-aware Hall/LP/exact-cover lookahead BEFORE committing rows 6/7, measure actual certified orbit exclusions, and keep separate proof-producing SAT/CP-SAT full 100/100/100 witness search across all 12 f types / 162959 (f,g) orbits. No unrestricted certificate. Automation remains enabled.
