# CAP-021 — Exact projective-moment slice-forcing ladder (286→110, 287→111)
**2026-11-02 ~15:53–16:?? UTC | exact CPU only | two independent arithmetic implementations | novelty unverified | no new global r3(7) upper bound**

## 0. Continuity and strategic decision
Read the live CAPSET-F3-7 Google Drive Ledger and dedicated folder, GitHub `STATE.json`, `LOG.md`, `BACKLOG.md`, recent commits and green CAP-020 CI (run 41467691611). The latest candidate upper bound 287 remains **provisional pending mathematical referee**. Rather than rerun the 28-class CAP-019 finite certificate or optimize a fixed 236-cap, investigate the previously underexploited **balanced/no-112-slice regime** through an independent exact moment-dual certificate.

Sources checked 2026-11-02: Potechin (2008) unique 112-cap, Thackeray arXiv:2206.09804v1 (2022) Theorem 3.9 (every 110-cap extends to 112) and Proposition 4.1, Grace–Voloch (published 2026-05-21, exact r3(n) only n≤6). Searches for specific 286→110 and 287→111 slice forcing statements did not establish novelty; **no novelty priority claim**.

## 1. Self-contained global moments
For any cap A⊂F₃⁷ of M points and each of 1093 projective normal directions u, write the three affine slice sizes (a_u,b_u,c_u) in decreasing order, with S₂=a²+b²+c², S₃=a³+b³+c³.

Counting ordered point pairs and triples by the dimension of the orthogonal space yields:
```
Σ_u 1    = 1093
Σ_u S₂   = 364 M² + 729 M
Σ_u S₃   = 121 M(M−1)(M−2) + 1092 M(M−1) + 1093 M.
```
The three-distinct-points term uses the cap property: no three distinct cap points are affinely collinear, so the two difference vectors are independent and exactly (3⁵−1)/2=121 projective normals annihilate both. No 6D classification is used in these identities.

## 2. Exact dual certificates
Let `F_M(a,b,c)=α S₃−β S₂+γ`. For each row below, the stdlib Python verifier enumerates **every sorted integer triple** with 0≤c≤b≤a≤the hypothesized max slice and a+b+c=M. For the conditional rows, it also removes triples with a,b≥110, because their c≥66 contradicts the previously established CAP-017B two-near-maximal-slices upper c≤64 (requires the published Thackeray 110 completion and the CAP-017B Fourier/common-tangent proof).

| M | Hypothetical maximum 6D slice | Remaining profiles | (α,β,γ) | Minimum F on all remaining profiles | Exact Σ_u F |
|---:|---:|---:|---|---:|---:|
| 286 | ≤109 | 161 | (40,10893,193029098) | 0 | **−2,468,100** |
| 287 | ≤110 | 175 | (82,22401,399662803) | 0 | **−4,531,050** |
| 288 | ≤111 | 189 | (589,161442,2900219904) | 0 | **−29,038,176** |

Since a sum of 1093 nonnegative integers cannot be negative, the exact conclusions are:

1. **Unconditional elementary theorem:** Every 286-point cap in F₃⁷ has at least one affine 6D hyperplane section containing **≥110 points**. The same is true of every cap of size ≥286 by choosing any 286-point subset. This needs no Potechin/Thackeray classification or CAP-017B.
2. **Conditional structural theorem:** Every hypothetical 287-point cap has a section of **≥111 points**, assuming the CAP-017B common-tangent lemma and Thackeray's 110-cap completion theorem. The single dangerous profile (110,110,67) is specifically excluded by c≤64. The dual functional on that excluded triple equals **−52,920**, demonstrating why silently dropping the tangent dependency would be invalid.
3. **Conditional consistency check:** Every hypothetical 288-point cap has a 112-point section, under the same premises. CAP-019 already provisionally excludes 288 entirely; this is a structural cross-check, **not** a new stronger global bound.

This is a short **finite arithmetic proof**, not a proof of r3(7)=236 or a construction of 287 points.

## 3. Exact negative controls: why the present moment method stalls
Two explicit **formal integer direction histograms** match all three global moment sums but are **not actual cap sets** and do not satisfy all 5D incidence constraints.

For M=285, with every slice ≤109:
```
(109,109,67):152; (101,96,88):3; (98,94,93):2;
(96,95,94):826; (95,95,95):110.
```
Their counts sum to 1093, second moment 29,773,665, third moment 2,860,326,405. Thus global moments alone cannot force a ≥110 slice at M=285; the unconditional 286 threshold is **sharp for this exact moment-only relaxation** (not necessarily sharp for true caps).

For M=287, with every slice ≤111 and all profiles respecting CAP-017B:
```
(111,109,67):140; (111,96,80):2; (110,109,68):6;
(101,94,92):1; (98,95,94):47; (97,97,93):1;
(96,96,95):896.
```
Their second moment is 30,191,539 and third moment 2,920,545,005. Hence **even with CAP-017B and the global first three moments**, one cannot force a 112 slice at M=287. This is a falsification of a tempting stronger proof strategy, not a geometric witness. The formal models do not encode barycenter quadratic-residue spectra, individual hyperplane intersection consistency, or cap geometry.

## 4. Independent verification, failed hypotheses, literature cross-check
- `test_cap021_slice_forcing.py`: five deterministic stdlib unit tests, **5/5 PASS in 0.003 seconds locally**; enumerates 161/175/189 triples and independently checks both formal histograms.
- Separate JavaScript implementation, with independently written loops and exact integer arithmetic, reproduced all profile counts, functional coefficients, negative totals and formal histograms. All values are below JS safe-integer threshold. Machine-readable certificate `CAP021_slice_forcing_certificate.json`.
- Independent direct F₃⁷ checker reread the existing 236-point witness from `external_agent_v5/capset_swarm_v5_corrected_evidence.json` blob `025a93713119d111db50b54b1d1238b97864c013`; verified 236 distinct points, all 27,730 unordered pairs, **zero collinear triples**, and complete coverage of all 2,187 ambient points. This is a known construction, not new ≥237.
- Exploratory SciPy HiGHS LP (discovery only) initially found 286/287/288 moment infeasibility under restricted max slices; a SciPy MILP produced exact integer formal models at M285 and M287. **Final certificate and tests do not depend on SciPy, optimization status or numerical tolerances.**
- Negative controls: allowing (110,110,67) makes the M287 functional negative locally, so CAP-017B cannot be omitted; M285 moment histogram and M287 max111 histogram falsify attempts to extend the same moment-only dual to stronger slice thresholds.
- **Literature meta-audit:** Thackeray Proposition 4.1(a) already gives **c≤34** for 112+112 slices, stronger than CAP-020's c≤56; Proposition 4.1(b) gives **c≤55** for two slices totaling ≥222, stronger than CAP-020's d≤2 bounds. Future research must incorporate these **published-in-preprint stronger conditional cuts**, and not claim CAP-020 numerically improves the known bounds for d=0,1,2. CAP-020's antipodal lemma may remain mathematically useful for d=3,4 and independent structure. Neither preprint proof nor priority independently reproduced here.

## 5. Commands and scope
```bash
python research/capset_f3_7/test_cap021_slice_forcing.py
python -m unittest discover -s research/capset_f3_7 -p 'test_cap021_slice_forcing.py' -v
```
No random seed, GPU, paid compute, or new candidate ≥237. GitHub CI status must be checked on the exact commit. Source and evidence are on the dedicated `research/capset-f3-7` branch only; no unrelated branches touched.

**Meta-audit and next step:** The M287 search can now focus on **at least one 111-point slice** (assuming CAP-017B and 110 completion). Since the formal 287 histogram remains feasible, pursue *five-dimensional codimension-two incidence constraints*, barycenter Gaussian-quadric residue counts and proof-logged SAT/ILP; a mere global S₂/S₃ functional cannot finish the proof. Separately commission hostile review of CAP-017B and 110 completion before presenting candidate 287 upper bound as established. Exact r₃(7) remains OPEN.
