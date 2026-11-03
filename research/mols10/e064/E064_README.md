# E064: 1700 complete paratopy frontier — 3-MOLS(10) remains OPEN

**Sole goal: 3-MOLS(10) CLOSED.** Read `E064_REPORT.md` for the mathematically complete coverage argument, limitations, and scientific credit to the preexisting Latin rectangle class counts.

Run `bash E064_REPLAY.sh` to reproduce 16,085 ordered orbits by **two independent algorithms**, quotient 2,877 (isotopy) → 1,700 (paratopy), and exhaustive positive/negative DLX order-4/5/6 controls.

For a one-off limited, strictly scoped order-10 attempt, run:

```bash
python E064_BRANCH_RUNNER.py --start 0 --count 5 --seconds 1 --max-nodes 1000000 --output E064_branch_log.jsonl
```

`UNKNOWN_BUDGET` is not UNSAT. SAT outputs are independently replayed and their full matrices saved. Every 1,700 canonical class must be covered to prove global nonexistence. No scheduled hourly work is enabled.
