# E066 — ALL 1,700 paratopy branches: proof-carrying CLOSED attempt

**SOLE GOAL: 3-MOLS(10) CLOSED** via independently verified 100/100/100 matrices, or a complete unrestricted negative proof whose entire 1,700-branch partition is covered by independently replayable LRAT certificates.

**Before any actual UNSAT certification, status is OPEN.** Neither a timeout nor a solver's unverified `UNSAT` statement closes a branch. The old E065 shell checker had a bug: it expected `VERIFIED` but the independent `lrat-check` prints `c VERIFIED`; this version explicitly handles the real checker output and rejects malformed/truncated proofs.

## Campaign scope

- Complete normalizations from E064; no additional unproved branch restrictions.
- **1,700 unique first-column paratopy representatives**, indexed `0..1699`. This is a *coverage* inventory, not a solved count.
- **17 deterministic shards × 100 representatives**. Every branch uses an **individually recorded complete branch CNF** with 33,000 Boolean variables, 101,758 clauses (= E065's 101,740 + 18 branch units), and a source SHA-256.
- CaDiCaL v3 pinned at `c60730422e758ef1cebe7aeddf2dda31c996bf04` with text LRAT, `--no-factor --no-binary`; independently compiled `lrat-check` pinned at `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
- Calibration **must** pass order5 branch0 certified `UNSAT`, branch1 independently checked `SAT`, and a deliberately bogus LRAT proof must be rejected. The full sweep depends on this calibration.
- All 1700 branches are attempted with a bounded per-branch solver budget (workflow currently **8 seconds**). Each remains `UNKNOWN_BUDGET` unless a witness or an independently checked UNSAT certificate is produced.
- Aggregate ledger has exactly 1,700 records in canonical order. Missing shard / unexpected exit / rejected proof never count as UNSAT. Verified proofs are gzip-archived with SHA-256 alongside the exact branch formula identity.
- Workflow automatically uploads the ledger, proofs, and logs as GitHub Actions artifacts; a best-effort GitHub commit of the aggregate summary is attempted. If GitHub Actions are disabled or cannot fetch/build dependencies, the sweep has **not run**. No claim of finished execution is made until all 17 shard artifacts have been inspected.
- This workflow is triggered by pushing the E066 script/workflow to `math-agent-mols10`. It is not the hourly ChatGPT automation (which remains disabled).

## Offline checks

```bash
cd research/mols10/e066
python E066_inventory.py                   # 1700 exact branch CNF fingerprints and audit 3 full CNFs
python E066_campaign.py aggregate --input <downloaded-shard-artifacts> --output <result-dir>
```

## Deployment and interpretation

GitHub Actions `.github/workflows/mols10-e066-all-1700.yml` first builds and calibrates proof-producing tools, then fans out across all 17 shards. Results are not merged into a mathematical proof until **every one of 1700** branches is backed by a valid LRAT or a complete SAT solution is independently checked. An all-UNKNOWN initial pass is a valid execution result but **zero mathematical closure progress**. Later passes should prioritize unresolved branches with different encodings and stronger propagation, not claim a solution percentage.
