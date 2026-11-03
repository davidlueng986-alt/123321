# MOLS10 E061 — CLOSED is the only success criterion

**Mathematical status: OPEN.** Success means an independently checked three-10×10-square 100/100/100 witness or a complete unrestricted independently replayable impossibility proof. No local search nodes or partial rows count as a percentage solved. The MOLS10 hourly automation is deliberately **paused**.

## New exact constructive target

Find any orthogonal order-10 Latin pair with **nine mutually disjoint common transversals**, which forces the tenth and proves 3-MOLS(10) exists. Or find **eight** disjoint common transversals and show that the 20 uncovered cells' shared row/column/A-symbol/B-symbol conflict graph is **bipartite**, which also proves existence. See `E061_REPORT.md`, `E061_transversal_route.py`, `E061_two_transversal_completion.py`.

## Reproduce

`bash E061_replay.sh` runs C++ exact solver controls, independently validates n4/n5 positive witnesses, checks the n6 finite UNSAT computation, replays bounded Latin cycle trades, and replays the exact transversal lemmas. `E061_full_oa_dlx.cpp 10 15 200000000` gives an unrestricted *bounded* order-10 probe; its `UNKNOWN_BUDGET` result cannot be treated as proof. `E061_12types.jsonl` contains bounded cases for all 12 normalized A-second-row cycle types, **none closed**.

E061 is an on-demand iteration and creates **no new background automation**.