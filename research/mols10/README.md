# Math Agent — 3-MOLS(10) continuing research

**Problem:** Do three mutually orthogonal Latin squares of order 10 exist?
**Status:** OPEN at the last primary-source review (2026-11-02).
**Study log:** https://docs.google.com/document/d/1NDPWEMM3Cf5HrhdOcV6pVE9tCI-kxKbavxcfIBFva3k/edit

## Reproducibility
```bash
cd research/mols10
python3 -m unittest -v test_verify.py
python3 verify.py near_triple.json --diagnostic
python3 verify.py candidate.json
```
The `near_triple.json` baseline comes from Egan–Wanless (2016). Its pairwise overlay counts are **100,100,91**, so it does **not** resolve the conjecture. Candidates pass only when every row/column is a permutation of 0..9 AND every pair overlay has 100 distinct ordered pairs.

## Every research iteration
1. Read `STATE.json`, `RESEARCH_LOG.md`, `HYPOTHESES.md`, the Google Drive research charter, and the latest CI.
2. Check reputable current academic literature for actual full resolution, not merely restricted cases or preprints claiming success.
3. Choose one clear falsifiable subproblem based on marginal information gain. Execute a bounded experiment if compute/tools allow; avoid replacing research with a plan.
4. Record experiment ID, reproducible code/inputs, assumptions, run details, failures, proof limits, commit and next action.
5. Independently replay any witness or UNSAT certificate. Use Lean 4 if a formal mathematical claim is ready, auditing exact statement equivalence.
6. Update state and both persistence locations where supported. Never expose secrets in this public repository.

## Research priority
H1: Third-Latin-square extension of a fixed orthogonal pair (A,B), enforcing orthogonality to **both** A and B; test encoding correctness on smaller orders.
H2: Latin trades on near-triple baseline, preserving all three constraints rather than optimizing one overlay alone.
H3: Prove correctness and completeness of symmetry normalizations before exhaustive search.
H4: Novel structural lemmas with explicit restricted hypotheses and independently replayable certificates.

**A negative fixed-pair result cannot establish nonexistence of all 3-MOLS(10).** An alleged external solution also requires independent validation and original-author credit.

Primary sources: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ;
https://doi.org/10.1090/mcom/3010 ;
https://theoremdb.org/statements/P2534/


## Current frontier and artifacts (updated after E007)

The fully open 3-MOLS(10) problem has **not** been settled. The research agent has advanced beyond the old pair-search baseline:

- `E003_E005_REPORT.md` and `E003_E005_RESULTS.json`: third historically published orthogonal pair (Parker), zero common transversals certified; exact-cover extension code; 200-seed Egan-A screening; two-symbol trades.
- `E006_E007_REPORT.md` and `E006_E007_RESULTS.json`: exact k-symbol repartitions, plus Parker-A bounded candidate search with explicit UNKNOWN statuses.
- `parker_pair.json` and `parker_frontier.py`: independently reproduced historical pair and compact 21-frontier obstruction.
- `exact_cover.py`, `sample_mates.py`, `two_symbol_trades.py`, `k_symbol_trades.py`: reproducible solvers and restricted-structure experiments.
- `STATE.json`: authoritative machine-readable next action. Read this and the current research log **before** allocating compute. Do not rerun Egan A/B <=5-symbol trade experiments.

### Full regression

```bash
cd research/mols10
python3 -m unittest discover -p 'test_*.py' -v
python3 parker_frontier.py
python3 sample_mates.py --samples 200 --seed-start 0 --output sampling_report.json
```

The complete k-symbol scan has strict scope: **fixed A, fixed B, chosen symbol support**, no per-support solution cap reached in reported cases. A positive candidate is never accepted without the independent exact Latin-and-three-overlay verifier. A budget-exhausted search is **UNKNOWN**, not UNSAT.

**Next E008:** Find genuinely different first Latin squares and coverage-directed candidate generation, favoring pairs with >=10 joint common transversals and full 100-cell support before expensive partition search.


## IMPORTANT — E008-E011 exact results and E012 handoff (2026-11-02)

**3-MOLS(10) remains OPEN.** Two published Egan near-triple fixed-pair directions have now been completely optimized in the conditional sense:
- **E008:** Fix A,C. ANY Latin B' orthogonal to A yields at most **91** distinct B',C symbol pairs. A nine-cell deletion set proves the bound exactly; published B attains it.
- **E010:** Fix A,B. ANY Latin C' orthogonal to A yields at most **91** B,C' pairs. A denominator-2 exact signed dual proves it; published C attains it.
- **E009:** Fix historical Parker A,B. Any Latin C' orthogonal to A yields at most **77** distinct B,C' pairs. Signed integer-matrix proof, *only an upper bound* (attainability unknown).
- **E011:** 48 alternate first Latin squares constructed via row-column 2-symbol Latin trades. Transversal counts differ from Egan A, so they are not paratopic to A. None remains orthogonal to the published B/C. Small-budget mate search UNKNOWN; no no-mate proof.

**Complete mathematical reasoning and strict proof scopes:** `E008_E011_OPTIMALITY_PROOFS.md`.

Certificate files: `E008_DUAL_CERTIFICATE.json`, `E009_PARKER_DUAL_CERTIFICATE.json`, `E009_PARKER_WEIGHTED77.json`, `E010_EGAN_AB_WEIGHTED91.json`. Standard-library exact replay: `dual_certificates.py`, `signed_dual.py`; regression: `test_dual_certificates.py`, `test_signed_dual.py`, `test_first_square_trades.py`.

```bash
cd research/mols10
python -m unittest discover -p 'test_*.py' -v
python dual_certificates.py E008_DUAL_CERTIFICATE.json --independent
python signed_dual.py E009_PARKER_WEIGHTED77.json
python signed_dual.py E010_EGAN_AB_WEIGHTED91.json
```

**Next E012:** Stop trying to repair the published near-triple by changing only one square. Search genuinely different first-square structures and orthogonal mates, screen for >=10 common transversals and full 100-cell coverage, then certify exact packing or retain UNKNOWN. Compare against recent SAT/CP literature before novelty claims.

The discovery optimizer used local SciPy/HiGHS but all *proof replay* above uses exact integer arithmetic without numerical optimization packages.
