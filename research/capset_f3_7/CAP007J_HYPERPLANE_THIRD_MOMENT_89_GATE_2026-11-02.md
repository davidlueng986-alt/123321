# CAP-007J — A globally valid 89-point hyperplane-section gate (2026-11-02 10:54 UTC)

**Status:** rigorous elementary proof with exact-integer executable audit; independent direct 236-point regression performed in JavaScript; base theorem Python CI **GREEN** at run 41432934273; integer histogram fully CI GREEN at run 41433674492. **Not** a construction, not an improvement of the numerical bound on r3(7), and **not** a literature-priority claim.

## Statement and scope

**Theorem (conditional structural necessity).** If A is a 237-point cap in F3^7, some affine hyperplane H (dimension 6) satisfies |A ∩ H| >= 89. Consequently, the same holds for every cap of size >=237 (choose any 237-subset).

This applies to **all** hypothetical 237-caps, not merely edits of the known 236-cap, an invariant orbit family, or the anchored-112 family of CAP-007H. It does **not** show that a 237-cap exists or that r3(7) <=236.

## Proof by the exact second and third hyperplane moments

Index the 1093 nonzero linear forms modulo nonzero scalar by v. For each v let (a_v,b_v,c_v) be the sizes of the three parallel affine 6D slices, so a+b+c=237. The number of normal directions that send two distinct fixed points into the same slice is (3^6-1)/2=364. For three **noncollinear** fixed points it is (3^5-1)/2=121. A cap has no collinear triple, so ordered-tuple double counting gives, exactly:

S2 = sum_v(a_v^2+b_v^2+c_v^2)
   = 1093*237 + 364*237*236
   = 20,618,289.

S3 = sum_v(a_v^3+b_v^3+c_v^3)
   = 1093*237 + 3*364*237*236 + 121*237*236*235
   = 1,651,763,205.

Set x_v=a_v-79, y_v=b_v-79, z_v=c_v-79; x+y+z=0. Let V_v=x^2+y^2+z^2 and W_v=x^3+y^3+z^3. Exact substitution yields

sum_v V_v = 154,050,
sum_v W_v = -1,421,526,
sum_v (W_v + 9 V_v) = **-35,076**.

Suppose every affine hyperplane intersects A in <=88 points. Then every x,y,z <=9. If two deviations are nonnegative, write (x,y,z)=(p,q,-p-q), with 0<=p,q<=9. Now

W=-3pq(p+q), V=2(p^2+pq+q^2).

Since 3pq <= p^2+pq+q^2 (equivalent to (p-q)^2>=0) and p+q<=18, we have W>=-9V. If two deviations are nonpositive instead, W=3xyz>=0, so again W+9V>=0. This includes zero cases. Thus W_v+9V_v>=0 for **every** direction, contradicting the exact negative total -35,076. QED.

Independent exhaustive integer confirmation enumerated all **75** unordered triples 0<=a<=b<=c<=88 with a+b+c=237; the minimum of W+9V is 0.

### Sharpness of this particular relaxation

The second/third-moment equations **even with integer multiplicities** cannot force a 90-point slice: the following purely formal histogram has 1093 directions, every slice <=89, and exactly reproduces both moments:

- 238 directions of profile (59,89,89)
- 267 directions of profile (76,78,83)
- 65 directions of profile (76,79,82)
- 523 directions of profile (77,80,80)

Exact checks: counts sum to 1093, centered variance sum 154050, centered cubic sum -1421526. This is **NOT** a cap construction or a realizable hyperplane system; it proves only that these two aggregate moment equations plus integer histogram counts do not exclude max89. A rational three-profile convex model also exists, but the integer histogram is stronger. Any improvement to >=90 needs additional geometric consistency constraints.

## Reproducibility / independent checks

Source: cap007j_hyperplane_moment_gate.py (stdlib, no randomness or optimizer); tests: test_cap007j_hyperplane_moment_gate.py. From repository root:

    python research/capset_f3_7/cap007j_hyperplane_moment_gate.py
    python research/capset_f3_7/cap007j_hyperplane_moment_gate.py --witness research/capset_f3_7/candidates/calderbank_fishburn_236.txt
    python -m unittest discover -s research/capset_f3_7 -p 'test_cap007j_hyperplane_moment_gate.py' -v

Local scratch Python: 3 tests PASS, the repository-fixture test skipped because that fixture was not present in the isolated scratch runtime; CI should execute all four with the repository fixture. Independently, a separate JavaScript arithmetic checker fetched the exact 236-point witness from GitHub (blob bb75562499071945a07273e439a892c55a8d6b9f), confirmed 236 distinct points and zero collinear triples across all 27,730 unordered pairs, and explicitly accumulated all 1093 directions: S2=20,445,388; S3=1,631,114,708; maximum slice 112. Both moments exactly matched the independent combinatorial formulas. This 236 check is a regression, not a new construction.

No GPU, paid compute, SAT solver, or random seed. The mathematical proof is self-contained and independently auditable without executing software. The first CI after adding the 236 regression test failed on the fixture header 'n: 7' (run 41432756301); parsing was corrected in commit 205e3ded1eaacbd83e094f95cf979a81b3bf2afd. Full branch CI then passed at https://github.com/davidlueng986-alt/123321/actions/runs/41432934273. The newly added integer histogram is separately exact-checked in JavaScript; follow-up CI https://github.com/davidlueng986-alt/123321/actions/runs/41433674492 completed SUCCESS for the integer histogram and all tests.

## Research implications and meta-audit

CAP-007H handles the globally meaningful but incomplete case of a 112-point hyperplane section. CAP-007J proves that any hypothetical >=237 cap has **some** hyperplane section of size 89..112, so a global proof by slice cases can, without loss, restrict to this range. The 89..111 families remain extremely large; this theorem is a useful rigorous bridge but not close to a global upper bound on its own. Avoid using it to justify an unbounded 23-case SAT sweep.

Next valuable experiment: derive a cap-specific fourth-moment or cross-slice inequality (the third-moment identity uses only the no-collinear-triples condition) and test whether it can certify >=90 or restrict the slice histogram; alternatively find classification-driven cuts for large 6D slices. Validate small dimensions and provide exact rational certificates. Any new claimed bound needs a separate global-coverage proof.

Literature status rechecked 2026-11-02: https://cairn-commons.com/problems/cap-sets-dim-7 lists 236 <= r3(7) <= 291 (2026-10-03); https://arxiv.org/abs/2206.09804 claims 288 in a preprint, not independently reviewed here; https://doi.org/10.1002/jcd.70024 (Grace–Voloch, May 2026) studies algebraic constructions but does not settle r3(7). Search did not establish that the present moment lemma is new in the literature. No 237 witness, no stronger certified numerical global upper bound, exact r3(7) OPEN.
