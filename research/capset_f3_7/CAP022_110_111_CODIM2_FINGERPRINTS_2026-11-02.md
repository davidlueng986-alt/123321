# CAP-022 — Exhaustive 5D hyperplane fingerprints of near-maximal 6D caps
**2026-11-02 UTC | CAPSET-F3-7 | CPU-only | exact finite census | mathematical novelty unverified**

## Decision and context
Continues CAP-021 (green GitHub CI 41477382285). The conditional CAP-021 gate says a hypothetical 287-cap must contain a >=111-point 6D affine section; aggregate global S2/S3 and Gaussian rank spectra admit explicit false models. We therefore derive *local 5D incidence fingerprints* for that 111 section and for 110 sections, rather than repeating global moments. The current candidate <=287 upper bound is still provisional, and the exact r3(7) is OPEN.

## Exact finite theorem for canonical H112
Reconstruct the canonical centrally symmetric 112-cap H in F3^6 using the 10 blocks of the 2-(6,3,2) design and the 32 full-support even-parity vectors. Independently check all 6216 pairs for absence of nontrivial 3-term progressions. Enumerate all 364 projective normals u, and the three 5D affine hyperplane section sizes in the direction u, sorted.

Canonical H112: (40,36,36) x308; (45,45,22) x56.
Every one-point deletion H\{p} (112 choices) has the SAME spectrum:
- (39,36,36) x110; (40,36,35) x198; (45,44,22) x45; (45,45,21) x11.
Every two-point deletion H\{p,q} (6216 choices) has one of EXACTLY TWO spectra:
- If q=-p (56 antipodal pairs): (38,36,36) x110; (40,35,35) x198; (44,44,22) x45; (45,45,20) x11.
- If q!=-p (6160 other pairs): (38,36,36) x38; (39,36,35) x144; (40,35,35) x63; (40,36,34) x63; (44,44,22) x18; (45,43,22) x18; (45,44,21) x18; (45,45,20) x2.
Each spectrum sums to 364 projective directions. These are exact exhaustive results for canonical H, not random samples or approximate LP output.

**Distinguishing invariant.** Counting individual 5D affine sections containing the maximum 45 cap points (count both 45s in a (45,45,t) direction), the totals are 112 for H112, 67 for any H111, 22 for antipodal H110 and 40 for nonantipodal H110. Thus the two H110 deletion types are distinguishable solely from their 5D hyperplane spectra.

## Generalization and dependencies
Potechin, *Maximal Caps in AG(6,3)* (DCC 2008), proves all 112-caps affinely equivalent to canonical H. Thackeray, *The cap set problem: Up to dimension 7*, arXiv:2206.09804v1 (2022), Theorem 3.9 proves every 110-cap extends to a 112-cap by adding two points. Therefore the two 110 spectra cover all 110-caps **conditional on accepting that external preprint theorem**. To infer that every 111-cap has the single 111 fingerprint, additionally use CAP-010A's exact secant stability / unique completion argument: deleting one point from a 111-cap yields a 110-cap; the 111-cap's removed point must be one of the two completion points. This argument still requires hostile independent referee. No claim that the 110-caps form exactly two affine-isomorphism classes; only that they have exactly two possible spectra.

## Relevance to 287 and solver design
For a hypothetical 287-cap with an anchored 111-point section (conditional CAP-021), its 111 section has exactly 11 projective 5D directions with profile (45,45,21), 45 with (45,44,22), 110 with (39,36,36), and 198 with (40,36,35). Across the three parallel 6D layers, each such direction defines a 3x3 grid of 5D cells; all nine cell counts <=45 and every one of the 12 affine lines of cells has total <=112 (a 6D cap). These are **necessary** codimension-two incidence constraints to incorporate into a proof-logged SAT/ILP model. The fingerprint alone does not rule out 287 and is not a new global upper bound.

## Verification, falsification, and priority audit
Commands: `python -m unittest discover -s research/capset_f3_7 -p 'test_cap022_110_111_codim2_fingerprints.py' -v` and `python research/capset_f3_7/test_cap022_110_111_codim2_fingerprints.py`. Local Python 4/4 passed (standalone unittest ~1.96s; full print ~3.34s), stdlib only. An independently written JavaScript implementation recomputed aggregate one-deletion counts across all 112 choices and aggregate two-deletion counts over all 6216 pairs, split into 56 antipodal and 6160 other; exact match. No seed, GPU, paid compute, solver or numerical tolerance. GitHub CI must be checked for the final commit.
Literature checked 2026-11-02: Potechin 2008 DOI 10.1007/s10623-007-9132-z; Thackeray 2022 arXiv:2206.09804 (Theorem 3.9 and Proposition 4.1); Grace–Voloch 2026 DOI 10.1002/jcd.70024; targeted exact-spectrum searches. No novelty priority established; Thackeray already gives stronger near-maximal geometric structure. Do not advertise a novel bound.

## Meta-audit and next bounded step
This produces a useful, exhaustive and cheap geometry-aware fingerprint to replace the CAP-021 aggregate-only relaxation. It does not yet encode cross-direction consistency or prove any new exclusion. Next: implement an anchored-111 3x3 codimension-two grid checker and cross-slice clauses, then try small proof-logged SAT subcases. Separately referee CAP-017B and Thackeray 110 completion, as they remain critical dependencies of the provisional <=287 theorem. Keep no-112/balanced branch alive for the exact 236..287 gap; r3(7) OPEN.
