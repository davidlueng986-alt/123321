# CAP-033 — Exact overlap of the only (7,6,6) and (7,7,4) lines in CAP027 formal 285 occupancy
2026-11-03 UTC. CPU-only, deterministic. Continuation of CAP027, CAP032B and CAP032C, not a cap construction.

Let P be lexicographic F3^4, E={t:t0=t1=0}, S={P[7i mod81]:0<=i<11}, f=3+1_E+3*1_S. Enumerate each affine quotient line once as {a,b,-a-b}.

**Exact result:** The 1080 quotient lines include precisely ONE (7,6,6) line and ONE (7,7,4) line:
- (7,6,6): (0000:7), (1001:6), (2002:6).
- (7,7,4): (0000:7), (0012:4), (0021:7).
Thus they share the *same* 7-point fiber at 0000. By CAP032C, any actual point-level realization of this fixed occupancy must assign that shared fiber the non-9-extendable AGL(3,3) seven-cap orbit (size 50544). This is a genuine **joint cross-line domain reduction**, not a contradiction. CAP032B also restricts the other 7-fiber on the (7,7,4) line through exact point compatibility, but its orbit type has not been deduced here.

**Verification:** Run `python research/capset_f3_7/cap033_occupancy_line_overlap.py`. It independently enumerates all 81 quotient points and 1080 lines, checks the histogram and two exact triples. No random seed or solver. This only tests the count-only CAP027 model; it does not instantiate any of the 285 points. No SAT/UNSAT proof, new >=237 witness, global upper bound, or novelty claim.

**Meta-audit:** Most quotient lines are low-density, so a full SAT pilot needs global shared variables and orbit-domain pruning; local high-density counts alone cannot settle the problem. Next P0: force fiber 0000 into nonextendable seven-cap orbit in fixed-occupancy SAT, and test whether 7+7+4 geometry is simultaneously compatible. Any UNSAT would exclude only this particular occupancy model, not all 285-caps. Independently referee CAP019/Thackeray classification and continue balanced/no-112 and >=237 branches. r3(7) OPEN.
