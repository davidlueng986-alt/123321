# Batch 2 — Complete fixed-prefix obstruction, certified nogood, and binary-relaxation countermodels

2026-11-03. **Root status: MOLS10 OPEN; exact r3(7) OPEN.** No root success is claimed.
This batch closes specific local questions and implements safe interfaces to complete enumeration.

## 1. Stronger than rejecting a single residual cover

Input: the seven-row prefix in `row_cover_fixture.json` (E059 historical Egan–Wanless source).
Its canonical JSON SHA256 is
`e199bf4266f744369b4401c6726ecebdd4a91b8b87a79b0f2f4b86518cd4739e`.

The previous batch proved one particular 30-placement integral cover could not be split into
three missing rows. That alone did not rule out another cover of the same prefix.

This batch independently reconstructs **all** legal residual placements: exactly 30, for 180
missing column-symbol/pair-symbol demands. Every demand has exactly one legal supporting placement.
Thus those 30 placements are forced in every completion; there is no alternative integral cover.
Twelve forced placements induce the 12-vertex, 22-edge non-3-colorable row-conflict core.
The supplied complete 33-node coloring proof is independently replayed.

**Conclusion: this entire exact seven-row prefix has no full completion.**
This is not a statement about all seven-row prefixes or a complete E033 orbit.
Global orbit closures remain zero. No literature-novelty claim is made for the source or method.

### General proof bridge

Any full extension must cover each missing resource exactly once. A singleton support forces
its placement, independently of the order of search. In a completion with q=n-k missing rows,
the forced placements must admit a q-coloring: same column or same square-symbol placements
cannot be put in the same row. A checked non-q-colorable forced subgraph contradicts extension.
The verifier uses all n^4 tuples, independently of the producer's missing-symbol product,
and checks every forcing demand and every coloring branch. It imports no producer code.
No solver timeout, sample, or floating-point result enters this proof.

### Tests

Nine Python tests cover complete support reconstruction, independent proof replay, corrupt
forcing demand, missing coloring branch, wrong prefix hash, positive affine order-5 prefixes
of four depths, three legal relabelings, a small zero-support case, and serialization pinning.
The first development run exposed tuple/list serialization mismatches; corrected before
accepting the committed artifact. Corrupted certificates remain rejected.

## 2. A guarded cut for the unrestricted normalized full-OA solver

`normalized_oa_cut.json` is a **60-negative-literal** clause in the existing 41,338-option
normalized full-OA numbering. Independent symbol relabelings make the three first rows identity;
physical row r maps to the label given by its normalized A first-column symbol. Known row labels
are 0,1,2,3,7,8,9; missing labels need not be consecutive. This is a legal common row reordering.
Any full normalized solution containing all these non-first-row assignments would invert the
relabeling to a completion of the excluded prefix, a contradiction. The ten row0 assignments
are already forced by the base model and are omitted from the clause.

This is a nogood under its **entire exact partial-assignment guard**, not a universal ban on
the twelve placements, not a ban on all seven-row prefixes, and not an arbitrary imported
CNF clause. Independent JS recomputes the full option numbering and every guard literal.
Dropping an assumption, changing a sign, or altering row labels is rejected.

`certified_search.js` first runs the independent Python premise checker, then verifies the
normalization/numbering bridge, and only then supplies the clause to `solveOA`.
The optional `learnedClauses` interface requires soundness justification by the caller;
its schema validation alone cannot prove arbitrary clauses valid.

A deliberately tiny 16-node-budget integration run returned UNKNOWN both with and without
the clause (17 visited nodes including the budget stop), with **zero learned prunes**.
Therefore no speedup or global-branch exclusion is claimed. The clause can skip this guarded
subtree when encountered; applicability frequency and cost need matched larger measurements.

## 3. Cap Set: all ten binary-only root relaxations are SAT

The full root CNFs remain unchanged and UNKNOWN. We test a specific prospective shortcut:
keep the selected frame/ninth point, all secant-forced zeros, all binary constraints induced
by one selected point, and both cardinalities total>=237 and dense-H>=89, but omit free-point
ternary clauses. Could an exact graph/MIS bound on this information alone prove no 237-cap?

**No.** For each of the ten dense-H ninth-point types, a deterministic greedy independent set
gives a binary-relaxation witness. Full greedy totals including the nine fixed points are:
`716,737,707,739,746,696,747,685,692,713`.
For each branch, the file also gives exactly 237 selected points with exactly 89 in H,
plus an explicit violated free-point ternary 3AP. These sets are deliberately **not caps**.

The standalone Python generator imports no CAP040/041 code. The independent JS checker uses
numeric base-3 arithmetic, reconstructs the 701 eligible ninth points/ten tags, verifies all
unit/binary conditions directly via triples containing a fixed selected point, both cardinalities,
and the explicit omitted ternary. Three mutations are rejected. It does not trust a supplied
binary-clause list. This is a SAT countermodel of each named relaxation, not a full-model SAT result.

Consequently no sound upper bound using only that binary relaxation can establish <=236.
This does **not** make binary propagation useless inside the full solver. It rules out relying
on it alone; useful future closure work must couple ternary constraints or other sound information.
No claim of novelty is made for the countermodel construction.

## Reproduce, standard Python and Node only

```bash
node research/closure_batch/run_batch.js
python3 -m unittest discover -s research/closure_batch -p test_forced_prefix.py -v
python3 research/closure_batch/verify_forced_prefix.py
node research/closure_batch/test_normalized_cut.js
node research/closure_batch/certified_search.js
node research/closure_batch/verify_cap_binary.js
```

Generators are deterministic and separate from their verifiers:

```bash
python3 research/closure_batch/forced_prefix.py
python3 research/closure_batch/cap_binary_countermodels.py
```

The existing closure-batch workflow runs all checks. Results are local until the exact new
commit's CI is observed; do not infer CI GREEN from an earlier commit. No automation was enabled.

## Next useful decisions

- Measure the forced-row filter on genuinely different prefixes with matched search cost;
  do not accumulate more rephrasings of this same source.
- A whole E033 orbit still requires all remaining C/row continuations and complete evidence.
- The Cap Set full ternary SAT leaves and the independent upper-bound referee remain open.
- Keep complete finite enumeration as the fallback; only apply cuts with an explicit proof bridge.
