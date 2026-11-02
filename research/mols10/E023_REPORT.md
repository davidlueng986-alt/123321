# MOLS10 E023 — Source-audited Myrvold residual-eight 4x4 compatibility lemma

**UTC:** 2026-11-02 02:46–02:49. **GLOBAL STATUS: OPEN.** This is a small, exact restricted-family experiment, NOT a 3-MOLS(10) solution.

## Source and literature check
- Bright–Keita–Stevens, *Electronic Journal of Combinatorics* 33(1) P1.30 (published 2026-02-13), https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 : explicitly states unrestricted 3-MOLS(10) open; SAT constructs orthogonal pairs for eight Myrvold residual types, not triples.
- Barnoff–Bright arXiv:2605.02132v2 (revised 2026-07-04), https://arxiv.org/abs/2605.02132 : improves orthogonal-pair SAT, not global triple.
- Authors' source repository https://github.com/curtisbright/Myrvold-MOLS (README, encode.py, verify.py read). Its eight residual cases: SX, UX, VX, WX, XX, UU, UW, WW.
- Fresh November 2 search did not reveal a verified unrestricted proof or 100/100/100 witness; absence of search hits is not proof.

## Exact mathematical subproblem
In source `verify.py`, each candidate row of a transversal-representation square has k=1,2,3,4 white entries in its last four columns. White symbols are 0..3. Given a chosen 4x4 Latin subsquare Omega, source compatibility forbids two white (column,symbol) pairs that occur in the same row of Omega.

Enumerate all column subsets of size k and all injective symbol assignments (4 choose k)*(4)_k; independently check via the unique Omega-row witness of each chosen (column,symbol) pair. Both checks agree on every input.

| k | Total injective partial assignments | Compatible Omega1=Z4 | Compatible Omega2=V4 |
|---|---:|---:|---:|
| 1 | 16 | 16 | 16 |
| 2 | 72 | 48 | 48 |
| 3 | 96 | 32 | 32 |
| 4 | 24 | **0** | **8** |

**Exact lemma:** a row containing four white entries in the last four columns is incompatible with cyclic Z4 subsquare Omega1. Proof: writing column c, white symbol v(c), the Omega1 row witness is r(c)=v(c)-c mod 4. A full compatible assignment would make both v and r permutations of Z4. But sum r(c) = sum v(c) - sum c = 0 mod 4, whereas the sum of a permutation of Z4 is 0+1+2+3 = 2 mod 4. Contradiction.

For Omega2=V4, eight full compatible permutations exist. A concrete positive witness is v=(0,2,3,1), with distinct Omega2 row witnesses (0,3,1,2).

**Additional finite rigidity:** under V4, each compatible two-white partial row has **exactly one** full four-white virtual completion (48/48); each compatible three-white partial has exactly one (32/32); each compatible one-white partial has exactly two (16/16). These are *virtual* completions of the subsquare compatibility condition, not actual extensions of a row of the order-10 Latin square.

**Consequence for source residual types:** source `encode.py` defines type V with one row having four white entries. Among the eight residual cases, **VX requires Omega2=V4**; its Omega1=Z4 branch is impossible by the lemma, independently of a SAT solver. The other seven types are locally compatible with either Omega, which does NOT establish global feasibility. For any type with an R/T/V row, Omega1 is similarly impossible.

## Reproduction and independent checks
- Executed local stdlib-only `python E023_subsquare_audit.py` (the committed file prints JSON); all internal assertions passed.
- Independent ECMAScript enumeration using a separate algorithm reconstructed the same 16/48/32/0 and 16/48/32/8 counts and 48/48 unique two-white completions, then wrote E023_RESULTS.json.
- Inputs are the two exact 4x4 Cayley tables from the authors' `encode.py` and `verify.py`, with XOR table for V4 and modular addition for Z4.
- GitHub code: [E023_subsquare_audit.py](E023_subsquare_audit.py); data: [E023_RESULTS.json](E023_RESULTS.json). Run `cd research/mols10 && python E023_subsquare_audit.py`. No GPU or SAT solve was required.
- The local filesystem `git clone` of the public source failed due to DNS resolution (cannot resolve github.com). Author source was nevertheless read directly through connected GitHub fetch actions; do not mistake clone failure for absence of source.
- No actual Myrvold SAT model/decoded order-10 pair was obtained. The source repository contains an encoder/decoder/solver workflow rather than checked-in explicit pair arrays. **Therefore no order-10 pair-extension SAT/UNSAT is claimed.**

## Assessment and next action
This is a correct, narrow and potentially useful SAT preprocessing/symmetry specialization, **not claimed to be a novel theorem** (the parity obstruction for cyclic groups is classical). It eliminates the Z4 subsquare branch for VX and gives an eight-state lookup for V4 compatible two-white partial rows; whether this materially accelerates the authors' full SAT solver is unmeasured.

**E024:** obtain an actual SAT-produced Myrvold residual-eight orthogonal pair (source verified), normalize its transversal-representation conversion, then enumerate all common transversals and attempt exact-cover third-square extension with independent replay. If SAT model retrieval is impractical, test the VX Z4 restriction as an independently checkable UNSAT preprocessing unit in a certificate-producing solver; do not conflate this with unrestricted triple nonexistence.

**No global 100/100/100 witness; no unrestricted nonexistence certificate. Keep automation enabled.**
