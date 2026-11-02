# E034C — Independent exact integer Farkas proof for all 39 Egan–Wanless four-row anchors

**UTC 2026-11-02 ~11:54–12:03. Global 3-MOLS(10) status: OPEN.** This supplements E034_REPORT.md, which reported 39 C++ exhaustive fixed-four-row exclusions but lacked an independently replayable certificate for every case. E034C supplies **39 explicit integer dual proof objects** and an independently implemented exact verifier. This is a *conditional near-triple rigidity theorem*, NOT a solution to unrestricted 3-MOLS(10).

## Precisely proved statement

Let S be the exact Egan–Wanless three-square near-triple in `near_triple.json`, with pair overlays 100/100/91. No full 3-MOLS(10) triple can agree with S on four complete common rows in the given symbols and columns (a common permutation of rows is harmless). Hence any such aligned repair must change **at least seven entire rows**. This does not exclude a triple with unrelated symbols/columns or arbitrary first square.

Of 210 choices of four source rows, 171 already repeat a symbol pair and cannot be part of any orthogonal triple; 39 are locally valid. For each valid I, form the exact 600-row 0/1 incidence matrix A_I of **every** allowed assignment (future row r, column c, symbols a,b,d). Candidate assignments respect the three squares' existing column symbols and all previously used AB,AC,BC symbol pairs. The 600 exact-once constraints comprise 60 cell positions, 180 future row/square/symbol, 180 column/square/missing-symbol, and 180 remaining ordered-pair constraints. Every genuine completion produces x>=0 with A_I x=1.

For each of the 39 valid I, the committed `E034_FOUR_ROW_EXACT_DUALS.json` stores an integer y_I of length 600 such that **sum(y_I)>0** and **A_I^T y_I <= 0** entrywise. If A_I x=1 for x>=0, then 0<sum(y_I)=y_I^T A_I x<=0, contradiction. Thus no completion of any valid four-row anchor exists. This argument does not rely on the optimizer after the integer proof objects are produced.

## Independent verification evidence

`node E034_verify_exact_duals.js` reconstructs the Latin squares, verifies 100/100/91, independently enumerates all 210 four-row subsets and the 39 valid ones, independently builds every possible future cell/triple candidate, and checks every dual inequality using only integer arithmetic and Node.js standard library. It does not import SciPy, the MILP model generator, or any solver.

**Exact replay: PASS 39/39, 94,572 candidate columns, minimum positive dual sum 8,475, maximum candidate-column dual sum -7.** The certificate file is 111,715 bytes; SHA-256 `7cda98c7aeaa94002bb6405c1ad1514896d0c48e4efafdeddeeb71af17ffe800`.

Independent solver controls: `E034_controls.py` reconstructs affine triples at orders 4 and 5, obtains SAT for both one- and two-row anchored completion (4/4), and replays every Latin row/column and all three n² overlays. For the 39 n=10 instances, `E034_direct_completion.py` reports solver-complete UNSAT in ~5.2s combined at 0.8s per instance; **the independently verified integer certificates are the decisive evidence**, not the solver statuses.

A useful methodological contrast: all 39 valid four-row anchors pass the **column-free residual triangle LP and integral exact-cover** test, so those weaker filters miss the contradiction. Adding actual cell/row/column placement constraints produces a fractional infeasibility certificate already at four rows.

## Reproduce

From `research/mols10`, with Python NumPy/SciPy and Node.js:

```bash
node E034_verify_exact_duals.js
python E034_controls.py
OPENBLAS_NUM_THREADS=1 python E034_direct_completion.py --seconds 0.8 --max 39
OPENBLAS_NUM_THREADS=1 python E034_direct_certify.py
node E034_verify_exact_duals.js
```

Files: `E034_FOUR_ROW_EXACT_DUALS.json`, `E034_verify_exact_duals.js`, `E034_direct_completion.py`, `E034_direct_certify.py`, `E034_controls.py`, `E034_DIRECT_COMPLETION_RESULTS.json`, plus existing `near_triple.json`. Identical proof objects and source were also uploaded to Google Drive Math Agent folder. The Python scripts were patched in GitHub to use repository-relative input/output paths.

## Failures and uncertainty

- A naive rationalization of interior-point LP solutions yielded only 1/39 exact certificates; a bounded integer dual MILP pilot timed out. Integer scaling of the numerical duals, followed by **exact** full inequality checking, yielded 39/39 certificates.
- Three primal LP calls initially returned HiGHS numerical status 4 (not UNSAT); changing algorithm/presolve reported infeasible. The exact integer duals independently resolve all three, so numerical status 4 was not used as evidence.
- A five-row near-triple pilot enumerated 300 sixth-row options and checked 31 residual MILPs, all UNSAT; this is **not** a complete six-row claim.
- All 39 four-row residual *symbol-triangle-only* MILPs were SAT, confirming that the stronger column/row/cell conditions are essential.
- No unrestricted proof and no 100/100/100 witness. Nothing justifies disabling the hourly research task.

## Next falsifiable global task

The four-row near-triple-preserving construction avenue is now exactly excluded, so **do not spend more compute on it**. Move to the E033 globally covering 12 A-second-row cycle types / 162,959 A/B second-row centralizer orbit representatives, incorporating these **full cell/row/column/pair** dual constraints into incremental SAT/CP-SAT. Prioritize a small proof-producing sample with independent LRAT/DRAT replay, then establish and certify complete symmetry-orbit coverage. If a full triple is found, independently verify every Latin row/column and overlays [100,100,100] before any claim.

Literature checked 2026-11-02: Bright–Keita–Stevens EJC 2026 https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; Barnoff–Bright https://arxiv.org/abs/2605.02132 ; Gill–Wanless https://arxiv.org/abs/2204.10996 . No independently checkable 2026-11-02 unrestricted resolution found; search absence is not proof.
