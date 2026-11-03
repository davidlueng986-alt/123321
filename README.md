# Math Agent — MOLS10 research

## Research mission — OPEN → CLOSED

**唯一成功條件：主問題由 OPEN 變成 CLOSED。** 局部證書、工具、掃描與界線只作解題手段，不是成功百分比。

- [完整成功規約與 proof／disproof 圖](docs/MISSION.md)
- [全部已識別的24項局部問題、範圍與決策](docs/LOCAL_PROBLEM_CATALOG.md)
- [完整暴力窮舉、天文成本與安全包圍方法](docs/EXHAUSTIVE_METHODS.md)
- [本批可重播實作與精確證書](research/closure_batch/README.md)

目前研究branch：`math-agent-mols10`。主問題仍 **OPEN**；維持現有on-demand模式。

## Inherited Lean verifier workspace

This is a ready-to-run **Lean 4 + Mathlib** formal verification workspace for a mathematics agent swarm.

**Branch note:** The verifier below originated on `math-agent-lean-verifier`; its clone command refers to that verifier branch.

## What it does

- Pins **Lean 4 v4.35.0** and **Mathlib v4.35.0** to avoid version mismatch.
- Installs Lean and Lake on GitHub-hosted Ubuntu runners.
- Downloads Mathlib and its compiled cache.
- Builds the `MathAgent` module. A green build means Lean accepted the example proofs.
- Rejects common proof holes and local axiom/unsafe declarations. This policy is a source-text guard, not a complete proof audit of every imported dependency.

## Add a theorem

Create `MathAgent/MyConjecture.lean`:

```lean
module

import Mathlib

namespace MathAgent

theorem sample_identity (a b : ℤ) :
    (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  ring

end MathAgent
```

Then add `public import MathAgent.MyConjecture` to `MathAgent.lean`. Push the branch and watch **Actions → Lean 4 / Mathlib proof verification**.

## Run locally

```bash
git clone --branch math-agent-lean-verifier https://github.com/davidlueng986-alt/123321.git math-agent-lean-verifier
cd math-agent-lean-verifier
lake update
lake exe cache get
lake build --wfail
```

`elan` (the Lean toolchain manager) is required. CI installs it automatically.

## Agent integration

`hypothesis → candidate .lean file → GitHub commit → Actions CI → compiler diagnostics → revised proof → repeat`

Use the GitHub Actions run and job logs to diagnose proof errors. **Do not report a theorem as verified until a relevant build succeeds.**

## Security

No secrets or model API keys are needed for proof checking. The workflow grants only `contents: read` and has a 45-minute job timeout. Avoid running arbitrary generated shell commands as part of proof submission. Source-level keyword checks are an additional precaution; Lean's kernel, not the keyword scanner, determines whether an elaborated proof term type checks.
