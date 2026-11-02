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
- The authors' GitHub source contains a solver workflow, not checked-in pair arrays. However, the **published Appendix itself** contains eight explicit TRPs; the SX instance was transcribed and independently replayed in the follow-up below.

## Assessment and next action
This is a correct, narrow and potentially useful SAT preprocessing/symmetry specialization, **not claimed to be a novel theorem** (the parity obstruction for cyclic groups is classical). It eliminates the Z4 subsquare branch for VX and gives an eight-state lookup for V4 compatible two-white partial rows; whether this materially accelerates the authors' full SAT solver is unmeasured.

**E024:** extend the Appendix SX replay to the other seven published TRPs; obtain an actual SAT-produced Myrvold residual-eight orthogonal pair (source verified), normalize its transversal-representation conversion, then enumerate all common transversals and attempt exact-cover third-square extension with independent replay. If SAT model retrieval is impractical, test the VX Z4 restriction as an independently checkable UNSAT preprocessing unit in a certificate-producing solver; do not conflate this with unrestricted triple nonexistence.

**No global 100/100/100 witness; no unrestricted nonexistence certificate. Keep automation enabled.**

## E023 follow-up — published Appendix SX pair, exact order-10 fixed-pair exclusion (2026-11-02 ~02:50 UTC)

**Critical primary-source discovery:** The EJC PDF Appendix **page 31 (PDF zero-based page 30)** directly prints eight TRP witnesses, beginning with a full 10x10 type **SX** pair P,Q. This supersedes the earlier statement that no source-verified pair arrays were accessible. Source: https://www.combinatorics.org/ojs/index.php/eljc/article/download/v33i1p30/pdf/ (Appendix, page 31). The same paper **explicitly states** the VX/Z4 impossibility (p.24), so our earlier parity derivation is a replication/alternate proof of a **known observation**, not a new restricted result.

**Reproducible computation:** Transcribed the first 20 10-symbol rows of Appendix into [E023_SX_pair_replay.py](E023_SX_pair_replay.py). Independently verified P and Q each Latin (10 rows/columns). Following paper Proposition 9, define Z[r,c] as the unique t with P[t,c]=Q[r,c], equivalently Z=P^{-1}Q in column-wise composition. Verified Z Latin, Q Latin, Q[r,c]=P[Z[r,c],c] for all 100 cells, and **Z and Q overlay has exactly 100 distinct ordered pairs**. Therefore (Z,Q) is an actual orthogonal Latin pair of order 10, directly constructed from a source-published TRP.

**Exact third-square obstruction:** Enumerated common transversals of Z and Q by independent row-by-row bitmask DFS: **0**. A second independent Python `itertools.permutations(range(10))` exhaustive replay of **all 3,628,800** row-column permutations also found **0** common transversals in **3.733 s** local CPU. Thus this **specific published SX-derived orthogonal pair cannot extend to a third orthogonal square**. This is fixed-pair only, not exclusion of the SX pattern family, the 4x4-subsquare family, or unrestricted 3-MOLS(10). Source-published TRP P,Q must not be confused with the derived orthogonal pair Z,Q.

**Code/data/test:** [E023_SX_pair_replay.py](E023_SX_pair_replay.py) (commit 506fafd501424f0e20b6347ae68469b29b7dead0); [E023_SX_RESULTS.json](E023_SX_RESULTS.json) (commit 276d4852dc3b1d7f0a16bbf12b8a838368ff0c89); [test_E023_SX_pair_replay.py](test_E023_SX_pair_replay.py) (commit 8776fc5aee83e69e9ea147e53513c84689ada25d). JS reimplementation independently reconstructed Z, checked Latin/overlay 100, and counted 0 common transversals. Python full-permutation test was run locally; GitHub CI for newly committed test is not yet confirmed.

**Next highest-value action:** replay the other seven Appendix TRPs with the same independent conversion and common-transversal check. If a pair has >=10 common transversals and full cell coverage, run exact-cover third-square search. Do not extrapolate zero common transversals in SX to all SX pairs or all eight types.

## E023 second Appendix witness — UU (2026-11-02 ~02:51 UTC)

Transcribed the **next** two 10x10 TRP arrays of type **UU** from the same primary-source Appendix page 31 (lines immediately following SX). [E023_UU_pair_replay.py](E023_UU_pair_replay.py) commit 51fff620274d172d0712a9d2eb195a708811a6c5 and [E023_UU_RESULTS.json](E023_UU_RESULTS.json) commit a957132ea0abd144defa98763d40f54597474e08 contain complete inputs and derived Z=P^{-1}Q. Independently checked P,Q,Z Latin, 100/100 overlay of Z,Q, and Q[r,c]=P[Z[r,c],c]. Both row-by-row exact DFS and a separate exhaustive 10! permutation replay found **zero** common transversals; the full permutation replay took 3.796s local CPU. Thus this **specific UU-derived orthogonal pair** also cannot extend to a third square. Two individual published examples (SX, UU) excluded; **no claim** about every SX/UU pair, all eight types, or global 3-MOLS(10).

**Corrected next step:** replay the **six remaining** Appendix witnesses UW, WW, VX, UX, WX, XX; each must be independently checked. Source paper already notes VX/Z4 impossibility; no novelty claimed. No SAT/DRAT/FRAT global certificate.
