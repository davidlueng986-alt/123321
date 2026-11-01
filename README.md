# Math Agent — Lean 4 proof verifier

This is a ready-to-run **Lean 4 + Mathlib** formal verification workspace for a mathematics agent swarm.

**Hosting note:** This workspace is currently on the isolated public branch `math-agent-lean-verifier` of the public GitHub repository `davidlueng986-alt/123321`, not on its default branch. Existing `main` is unchanged. The files can be moved to a dedicated public repository later.

## What it does

- Pins **Lean 4 v4.35.0** and **Mathlib v4.35.0** to avoid version mismatch.
- Installs Lean and Lake on GitHub-hosted Ubuntu runners.
- Downloads Mathlib and its compiled cache.
- Builds the `MathAgent` module. A green build means Lean accepted the example proofs.
- Rejects common proof holes and local axiom/unsafe declarations. This policy is a source-text guard, not a complete proof audit of every imported dependency.

## Add a theorem

Create `MathAgent/MyConjecture.lean`:

```lean
import Mathlib

namespace MathAgent

theorem sample_identity (a b : ℤ) :
    (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  ring

end MathAgent
```

Then add `import MathAgent.MyConjecture` to `MathAgent.lean`. Push the branch and watch **Actions → Lean 4 / Mathlib proof verification**.

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
