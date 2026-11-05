# E066 — Single-formula global CLOSED attempt

**Only goal:** decide unrestricted 3-MOLS(10). **Status: OPEN.** This supplements, without replacing, the existing 17-by-100 CaDiCaL/LRAT GitHub campaign.

From E065's complete normalized 5-coordinate OA CNF, add 1700 fresh selectors; require at least one selector true and each selector implies the 18 first-column units of that E064 canonical class. Thus the single formula is SAT exactly when one of the 1700 full branches is SAT. E064's independently verified paratopy coverage turns this into an unrestricted SAT question. The order10 global CNF has **34700 variables and 132341 clauses**. A SAT model must be independently verified to give 100/100/100; an UNSAT result needs a genuinely independently checked LRAT certificate and the audited coverage lemma.

Local controls: order4 SAT 16/16/16, order5 SAT 25/25/25, order6 UNSAT in 0.44 seconds using native Z3. Order10 Z3 global attempt at 2 seconds returned UNKNOWN. The local full 1700-class Z3 scan attempted all representatives under a nominal 50ms branch budget and returned 1700 UNKNOWN, zero branch closures. Exact source and all four shard logs, CNFs, checksum manifest and independent controls are archived at https://drive.google.com/file/d/1wh05Zye-0-nGSkwRSPT1usboVB4TDgHl/view .

The companion workflow uses pinned CaDiCaL and LRAT, calibrates n5 SAT and n6 LRAT UNSAT, then attempts the complete order10 1700-class global formula. Workflow outcome is **unverified** until remote runs and artifacts are inspected. No order10 witness or formal UNSAT currently exists. Hourly automation remains disabled.
