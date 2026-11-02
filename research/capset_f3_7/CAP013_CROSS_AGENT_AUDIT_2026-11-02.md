# CAP-013 — Cross-agent integration audit (2026-11-02)

**Scope:** Read-only audit of Drive-only CAP-008B/C, CAP-009A/B, CAP-010B/C, CAP-011A/B/C and CAP-012 additions against the authoritative GitHub branch at commit 37b6caff. No claim of a global r3(7) improvement; the exact problem remains OPEN.

## Provenance and conflict boundary
- Dedicated Drive ledger: https://docs.google.com/document/d/1eaL6YYNB80X9DwmPCVZ0mnuwSVIjSSPvpJ19uoZPQTM/edit
- Other-agent campaign report: https://docs.google.com/document/d/1_TWv6RzjYtBHJCawC6aT-q4ulBBdKuFaR7_nUaWp7lY/edit
- Original uploaded source: https://drive.google.com/file/d/1wvk5OGLjZltQnN67Yr_J7NZwd_y7QFmO/view (SHA256 bad468e7f6123e101f0c739ce1d3c911b5236b4806c528183921e2ad6acb2c23).
- Original uploaded JSON: https://drive.google.com/file/d/1JUi8ikknz945pFpkyZX9YUfTyGECgk9O/view (SHA256 97cb17340cb3cd874f5112fdc1acc0ca522dbf2567a2e992804822064af925d5).
- GitHub CAP-010A workflow 41440753830 now SUCCESS. New Drive CAP-010B..012 source is not in this dedicated GitHub branch yet; do NOT silently promote Drive claims as verified GitHub evidence.
- This audit does not modify, replace, or rename the other agent's original Drive files.

## P0: CAP-011A incorrect sign **confirmed by source and independent exact arithmetic**
In `capset_swarm_solver_v4.0.py` function `prove_wave2_universal_quadric_and_codim2_hierarchy`, the code sets `Q = (centered.T @ centered) % 3` and incorrectly tests `a1 == d.T@Q@d`. When the mod-3 centroid vanishes, a1=a2 (mod 3), and `a1+a2 == sum_x (d.x)^2`. Hence **a1 == -sum_x (d.x)^2 (mod 3)**, not plus. Correct `Q=(-centered.T @ centered)%3`, or change the asserted result to `(-q_vals)%3`.

Independent check using the actual uploaded coordinates: direct O(M^2) cap checker passed for all 112/236/496/512 witnesses; all projective directions enumerated in 6/7/8 dimensions.
- 6D112: original check TRUE, but only because Q=0;
- 7D236: original check FALSE in 729/1093 directions; corrected sign TRUE in 1093/1093;
- 8D496: original check FALSE in 2160/3280; corrected TRUE in 3280/3280;
- 8D512: original check FALSE in 2160/3280; corrected TRUE in 3280/3280.

Critically the uploaded v4.0 JSON itself contains `majority_residue_equals_dT_Q_d: false` for all three affected datasets. Thus the Drive CAP-012 designation 'all verified' is incorrect AS WRITTEN. The underlying theorem with a negative sign survives; must rerun source and all assertions before promoting.

## P0: CAP-010B's exact certificate is NOT fully exact as delivered
`prove_exact_rational_spectral_and_completion_audit` builds integer B_scaled and G_int, but determines `rank(185130000*I-G_int)` via `np.linalg.svd(diff_mat.astype(np.float64))` with a numerical threshold and determines maximum eigenvalue on 1^perp using float `np.linalg.eigvalsh`. This does not constitute an exact rational rank proof or an exact positive-semidefinite certificate. The reported 425/576 is NUMERICALLY SUPPORTED, not independently certified with exact arithmetic. Replacing the final arithmetic ceiling with integer fractions does NOT fix the floating-point spectral premise.

Required: exact rational rank or modular-rank certificate, plus independent exact PSD/characteristic-polynomial or algebraic Gram decomposition establishing the spectral norm bound; verify `G_int*1` consistency. Only then promote d>=ceil(64512m/(576m+47600)), m<=32, to a rigorous conditional theorem. Treat CAP-009B's m<=35 floating result as exploratory, not certified.

## Verified in this audit
- CAP-008B mod-3 centroid direction dichotomy for M=237: Type-1 count must be 0 or 729, so CAP-007J's proposed 267-Type-1 abstract moment countermodel cannot be an actual point-set incidence profile. This does NOT prove no 237-cap exists.
- CAP-009A stated pointwise convolution formula is algebraically consistent with the Fourier self-dual identity, conditional on the established canonical 112-cap Fourier spectrum. Do not infer global 237 exclusion from its k<=30 zero-hole restricted cases.
- CAP-011B 5D affine-subspace moments for ANY cap of size237 independently recomputed via Gaussian-binomial counts: 23,572,731; 639,439,983; 17,775,438,687. The third moment uses the cap property (all distinct triples are noncollinear). A 6D section of size 89 forces a 5D subsection of size >=33 by second moment. Proof: sum over 364 directions of triples' squares equals 121s^2+243s. If all three sections <=32 at s=89, each square sum <=2673, so 980068 > 364*2673=972972, contradiction. Similarly s=91,92,93 imply >=34,34,34.
- CAP-011C bijection: for fixed z the cross-slice pairs x+y=-z form a matching in the disjoint union of the two slices, so deleting d1+d2 vertices can destroy at most d1+d2 blocker pairs, forcing d1+d2>=r(z) to free z. Elementary, general and sound.
- Classical 6D 112-cap, 7D236 and 8D496/512 witness cap properties independently verified in the associated local audit; no >=237 7D witness.

## Not yet promoted
- CAP-008C finite B6 46080 enumeration: math plausible but requires independent repository script and replay; B6 is a tiny subgroup of GL6.
- CAP-010C 3812 alignment histogram: stated in Drive but uploaded v4 function `prove_exact_rational_spectral_and_completion_audit` does not contain that enumeration. Need dedicated replayable checker and CI before accepting exact counts.
- CAP-012 M1-M3 'independent review' cannot be treated as an external independent audit of itself. Missing code/certificates and unasserted false booleans invalidate a blanket green flag.
- Novelty is not established for the centroid/quadric formulas or the spectral conditional bounds. Check older affine-geometry literature before priority claims.

## Reproducibility and next steps
- New independent, stdlib-only regression: `python -m unittest research/capset_f3_7/test_cap013_cross_agent_audit.py -v` (small abstract sign counterexample, all three 237-moments, 89/91/92/93 five-dimensional gates).
- Independent full-coordinate audit performed CPU-only (numpy, no GPU), no random seed; original Drive source/data SHA256 above. Code used: local `/mnt/data/capset_cross_agent_independent_audit_2026_11_02.py` (not yet stored in repository; avoid treating this local path as CI artifact).
- P0: correct CAP-011A sign and assert `all(values)` before reporting success; P0: replace float SVD/eigenvalue with exact PSD/rank certificate; P1: replay full 3812 histogram; P0: continue independent no-112-hyperplane global branch and proof-logged conditional SAT. All restricted results stay restricted.
- No GPU or paid compute. No solution to r3(7), no stronger global upper bound, no 237 witness.
