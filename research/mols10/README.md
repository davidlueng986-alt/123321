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
