# Manual root-directed CLOSED attempt — 2026-11-03

Exact r3(7) remains OPEN. The user's CAPSET hourly automation stays DISABLED and should not resume without an explicit instruction. This is an actual CPU attempt, not a solved proof.

Reproducible source files and deterministic seeds are in this folder. Complete raw logs + 236-point fixture (portable ZIP, SHA256 e5d3d6c6f676b145e33c1e3133f9312a462ab8e4493db3c56aed4f9b3bd8eea4): https://drive.google.com/file/d/1HmRyzpxzEGvokDo6wanAjssloeVwgHwN/view?usp=drivesdk

The Fourier identity is **previously derived in CAP025**, not a claimed novelty. Five completed constructive runs: 18,000,000 attempts, 17,797,340 sum of **within-run** unique matrices (not globally deduplicated), 177,872 full hole evaluations, max12 holes, 0 eligible 13-cap candidates. Assertions-enabled annealing 6,000,000 exchanges best 10 forbidden lines in a 237-point set, no 237 witness. A formal 287-point direction histogram satisfies first three aggregate moment constraints but is not a cap. No new global bound.

Failure log: the 25m single-run search was interrupted at wall timeout without completion; excluded from totals. Initial Python input-newline issue and first M287 modulo-3 residue categorization mistake were corrected and rejected. Repackaged scripts now support CAPSET_WITNESS environment variable and the included witness236.txt. No GPU/paid compute.
