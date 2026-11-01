# CAPSET-F3-7 | Hourly Mathematical Research

Problem: Determine r_3(7), the maximum size of a cap set in (Z/3Z)^7.

Status at bootstrap (2026-11-02): OPEN. Reported best construction 236; widely reported bound <=291; a 2022 preprint claims <=288. Verify these independently as literature evolves.

Milestones: (1) construct an exact, independently audited 237-point cap; (2) establish a rigorously proved matching upper and lower bound for exact r_3(7). Do **not** stop research at milestone (1).

Canonical state: STATE.json, LOG.md, BACKLOG.md.
Human-readable mirror: Google Drive Math Agent / 03_RESEARCH_LOG / CAPSET_F3_7_HOURLY.
Dedicated branch: research/capset-f3-7. Do not modify other branches; another mathematics project runs concurrently.

Per-cycle operating protocol:
1. Read STATE.json, LOG.md, backlog and Drive log; reconcile parallel activity before writing.
2. Check current published record/status (especially independent reports of a solution).
3. Pick one falsifiable and bounded experiment or mathematical lemma; record why.
4. Run exact local tests, compare to current baseline, and inspect counterexamples.
5. Save every verified result, failed hypothesis, resources, seed, executable command, and next priority to GitHub. Mirror a concise finding and decision in Drive.
6. Use precise labels: UNVERIFIED / VERIFIED COMPUTATION / FORMALIZED / INDEPENDENTLY REVIEWED / REFUTED.
7. Only claim new mathematics with exact evidence, novelty check, and independent reproduction. Never confuse a high benchmark score with theorem proving.
8. Stop the recurring automation only if the exact maximum is resolved by a mathematically sound proof plus matching construction and independent review, or the user stops it. If a breakthrough <= some bound is merely partial, continue.

References:
https://cairn-commons.com/problems/cap-sets-dim-7
https://zerothesis.com/challenges/cap-sets
https://arxiv.org/abs/2206.09804
https://doi.org/10.1002/jcd.70024

Verifier input: dimension 7 ternary digits per line, optionally header n: 7; check points distinct and no three distinct x,y,z with x+y+z=0 mod 3. This exact verifier is mandatory for all construction claims. Later formalize in Lean 4 for certified proof artifacts.
