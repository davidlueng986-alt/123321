# E031 — Direct OA(100,5,10,2) search and exact triple-residual dual obstructions

Timestamp: **2026-11-02 ~10:14–10:20 UTC**. Status: **OPEN**, no 100/100/100 order-ten witness, no unrestricted nonexistence proof.

## Grounding and literature

Read latest `research/mols10/STATE.json`, E030 report/direct solver, and the Google Drive MOLS10 living research journal through E030. Fresh November 2 searches found no independently checkable unrestricted solution; search absence is not proof. Primary literature:

- Bright–Keita–Stevens (2026), *Myrvold's Results on Orthogonal Triples of 10×10 Latin Squares: A SAT Investigation*, https://arxiv.org/abs/2503.10504 and https://doi.org/10.37236/13960 . Eight residual pair families ≠ eight fixed Q witnesses.
- Barnoff–Bright (2026), *Improving SAT Solvers on Orthogonal Latin Square Problems*, https://arxiv.org/abs/2605.02132 . Pair-level SAT improvements, not general triple proof.
- Gill–Wanless (2023), *Pairs of MOLS of order ten satisfying non-trivial relations*, https://arxiv.org/abs/2204.10996 . F2-rank obstruction already audited in E030.
- Amadou Keita, *Computational Construction and Classification of Some Mutually Orthogonal Latin Squares*, 2026 thesis, https://cs.uwaterloo.ca/~cbright/group/amadou_thesis.pdf (particularly Ch. 3 and concluding remarks). The thesis explicitly says the general question remains unresolved and emphasizes certificate-producing SAT. This source is a methodological influence, not a newly verified solution.

## New theorem-level facts used for sound search reductions

**Direct row normalization.** In any triple, each square's symbols can be independently relabelled to make row 0 `[0,...,n−1]`; common row permutation then makes square A's first column `[0,...,n−1]`. Swapping B and C makes `B[1][0]<C[1][0]`, since a valid triple gives distinct symbols in B,C at cell (1,0) after row-0 normalization. These are sound *existence-preserving* transformations.

**Residual-triangle lemma (exact).** At any row-prefix, let `E_AB,E_AC,E_BC` be uncovered ordered symbol pairs. Each future cell with symbols `(a,b,c)` must satisfy `(a,b)∈E_AB`, `(a,c)∈E_AC`, `(b,c)∈E_BC`. Hence every residual pair edge must belong to at least one *allowed triple*. More strongly, the residual edges must admit a nonnegative fractional exact cover by allowed triples, `Mx=1, x>=0`; this is NECESSARY even though it ignores row/column Latin conditions. If a rational dual vector `w` satisfies `sum_e w_e>0` and `sum_{edges of t} w_e<=0` for every allowed triple t, no completion exists, because summing against `Mx=1` yields `0 < w^T 1 = (M^T w)^T x <= 0`.

**Derangement-factorization viewpoint.** After normalizing all first rows, each nonzero row's AB, AC and BC symbol maps is a derangement; for a valid complete triple the `n−1` maps in each pair form an edge-disjoint decomposition of `K_{n,n}\I`. They are coupled by per-row composition, so pairwise one-factorization constraints alone do NOT enforce a third-square completion. In particular, uncoloured residual pair graphs after k complete rows are `(n−k)`-regular; each individually has a perfect-matching factorization by bipartite graph theory. Therefore adding only separate residual-pair matching constraints is expected to be a weak or vacuous filter; the *three-way compatibility* is the actual bottleneck.

## Experiment A — actual bounded direct 5-net solver

`E031_rowwise_5net.py`: exact incremental three-square row assignment, MRV column choices, row/column Latin uniqueness, all three pair overlays tracked without duplicates, proven symmetries, bounded node/wall budgets, optional Hall/matching and residual-triangle pruning. No fixed Q. Outcomes must distinguish SAT, complete normalized UNSAT, and UNKNOWN_BUDGET.

Independent `E031_independent_replay.py` confirms valid order-4 and order-5 triples, with overlays **16/16/16** and **25/25/25**, respectively. Order 2 and 3 exhaustively UNSAT under justified normalization (both root node 1). Order 6 UNKNOWN at 250,000 nodes; order 10 UNKNOWN at 250,000 nodes. No order-10 solution.

Representative n=10 seed0 at 250,000 nodes: no triangle pruning: 3.93 s, deepest completed row index 5; with triangle pruning: 3.44 s, deepest *surviving* row index 4, `triangle_checks=4330`, `triangle_prunes=4187` (pruning at depths 5 and 6). Depth differences and node counts are *not* comparable as solution success metrics; actual throughput and remaining frontier matter. On order 6, triangle pruning at 250,000 nodes had 22,450 sound prunes of 25,858 checked prefixes, but the general order-6 search remained UNKNOWN. Hall pruning on order-6 seed0 at 250,000 nodes slowed from ~1.89 s to ~3.27 s even though it pruned branches; this is negative evidence against naive Python Hall checks. Because the long multi-seed benchmark hit an outer execution timeout, only completed cases from its log are counted.

## Experiment B — exact direct CNF encoding

`E031_direct_cnf.py` constructs CNF for all three squares jointly, not a fixed pair. `x(s,r,c,v)` is one-hot by cell/row/column. Auxiliary `y(p,r,c,a,b)` implies both symbol assignments at that cell, and each ordered pair `(a,b)` is covered by at least one `y` over all cells. Since there are exactly n² cells and exactly n² possible ordered pairs, coverage implies *exactly once*. No reverse y implication or pairwise y exclusion is required. All stated symmetry clauses are existence-preserving.

Order 10 DIMACS statistics: **33,000 variables, 101,795 clauses, 240,150 literals**, exact SHA256 `4debf4e1be09d05205fae30c5385cf0dd413ffc9b8c9c019efb203ba6b4a6062`. Model assignment from independently verified n4 and n5 triples satisfies every clause. Tampered n4/n5 arrays fail; the order-10 Latin-valid duplicated-square negative control violates 271 clauses. **No CDCL solver or proof checker was installed**, so no order-10 SAT/UNSAT claim from this CNF; merely constructing a CNF is not executing it.

## Experiment C — rigorous stronger obstruction and proof objects

`E031_triangle_completion.py` forms the 3-partite allowed-triple hypergraph on uncovered AB, AC, BC ordered pair edges, checks triangle support, and when appropriate solves exact-cover MILP *without row/column constraints*. Several n10 6-row prefixes found by the raw DFS have 40 missing edges per pair and 53–61 allowed triples, but 2–8 missing edges per pair lack any triangle support: each fixed prefix is immediately impossible to extend. This is a *conditional* exclusion only.

For n10 seed0 using `--triangle`, the first **12 distinct surviving five-row prefixes** each had 50 missing edges per pair and **108–113 allowed triples**, and all three sets of edges had complete triangle support. However, **all 12 residual exact-cover LPs were infeasible**, and SciPy/HiGHS returned solver-complete infeasibility for corresponding MILPs (not external proof certificates). Crucially, `E031_dual_certificates.py` separately solved the Farkas dual and recovered 12 exact rational weights with positive sums **3–14** (denominators 1 or 2). `E031_verify_duals.js`, an *independent Node.js exact-integer verifier requiring no solver*, re-derived all uncovered edges/triples from the stored partial rows, validated row/column uniqueness and pair distinctness, checked all triangle inequalities and positive dual sums, and **passed all 12 certificates**. No numerical tolerance enters final dual checking. `E031_DUAL_CERTIFICATES_min.json` preserves the 12 witnesses and exact input row-prefix matrices. These prove exactly those 12 prefixes cannot be completed, not that order ten is impossible.

Use `python E031_rowwise_5net.py --orders 3 4 5 6 10 --budget 100000 --triangle`; `python E031_direct_cnf.py 10 --output E031_n10.cnf`; `python E031_independent_replay.py`; `python E031_dual_certificates.py` after generating `E031_TRIANGLE_SEARCH.jsonl`; `node E031_verify_duals.js E031_DUAL_CERTIFICATES_min.json`. Python requires SciPy only for the MILP/LP scripts; Node standalone verifier does not.

## Negative findings and failures (preserved)

- Direct order-10 DFS remains UNKNOWN: reaching 5 or 6 normalized rows is not remotely a solution.
- Hall checks often cost more than they saved in measured samples.
- A long multi-seed benchmark exceeded an outer execution timeout; uncompleted instances are not interpreted.
- The first triangle exact-cover MILP run included a fully completed small-order prefix with zero variables, causing a SciPy input ValueError. Fixed by explicitly treating no remaining pairs as `COMPLETE_NO_REMAINING_PAIRS`; reran all cases.
- All 12 LP-dual obstructions are local; they do not classify the unrestricted search space.
- CNF semantic validation does not replace running an independent SAT engine with externally checked DRAT/LRAT/FRAT proofs.

## Priority hypotheses and concrete next iteration

H31-A (highest): **Integrate exact rational dual cuts as conflict learning** into direct search. A prefix's valid dual certificate excludes it; generalize to a minimal pair-edge obstruction and re-use as a nogood across branches. Retain an independent rational checker for every learned cut.

H31-B: **LP feasibility gate after each surviving row prefix** (`k>=4`), balancing solver-call cost against catastrophic search expansion; compare matched budgets and baseline node/time counts. Test n4/5 positive and n6 negative first.

H31-C: **Core minimization** of 12 sparse dual witnesses; identify smallest support, lift under row/symbol isomorphisms, attempt a reusable structural lemma.

H31-D: **Incremental CDCL on full 5-net CNF** with safe normalization and verified clauses, log solver version/seed/certificate, run n4 SAT, n3 UNSAT and limited n10 UNKNOWN/SAT. The CNF now exists but solver is not installed here.

H31-E: **Joint derangement factorization** search: each row encodes a compatible triangle of AB/AC/BC 1-factors; design branch rules around triple compatibility rather than individual pair matchings.

H31-F: **Strong column-aware residual hypergraph**: allowed triple `(a,b,c)` must have a viable *column assignment* given remaining column symbol domains; derive further sound exact cover inequalities.

H31-G: **Proof-of-completeness of symmetry** and optional paratopy canonicalization with a verified graph-isomorphism backend; do not infer symmetry from matching cycle-spectrum signatures alone.

H31-H: **Residual combinatorial trade-offs**, test LP dual rank / sparse inequality features against random biased partial states and controls; avoid overfitting n10 seed0.

H31-I: **Independent proof checking of full SAT UNSAT** with DRAT/LRAT; exact rational local dual witnesses can be used now, but no unrestricted certificate exists.

H31-J: **Better branch metrics**, compare fraction of prefixes passing exact LP cover (not just max depth or raw nodes) per CPU second.

H31-K: **Avoid fixed published Q bias**, use full OA constraints or random normalized row states. Count classes only with *proved* canonical equivalences.

**Next exact action:** benchmark `triangle+dual` lazy checks vs triangle-only and no-pruning on same deterministic seeds, with standalone rational replay of every discovered conflict; then couple any verified speedup to a proof-aware full 5-net SAT search. Research automation remains enabled.
