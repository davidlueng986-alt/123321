# CAP-052: Single-root secant-centre disproof attempts (2026-11-06)

**Status: NOT DONE (ATTEMPTED).** No independently verified 237-cap or complete UNSAT proof. No new global numeric bound or academic novelty claim. Hourly automation remains disabled.

## Theorem A — one universally complete dense-H centred normal form

By the CAP007J exact hyperplane-moment theorem, every hypothetical cap of size at least 237 in F3^7 has an affine six-flat H containing at least 89 cap points. This slice spans dimension 6 because r3(5)=45. The C(s,2) internal secants have missing third point q in H outside the cap. For s>=89, C(s,2)>6(729-s), so one q centres at least seven antipodal cap pairs. Their seven projective pair directions form a projective cap. Since PG(2,3) has 13 projective lines and seven no-three-collinear directions would determine 21 distinct lines, their span has rank >=4. Choose four independent paired directions; extend by two selected H points to full six-dimensional H span, and one selected point outside H to span 7D (r3(6)=112). Translate q to0 and apply an invertible linear change of coordinates.

Without losing ANY >=237 cap, fix origin q=0 UNSELECTED; select +/-e1,...,+/-e4,e5,e6,e7 (11 points); require at least 89 selected points in H={x7=0} and at least seven selected opposite pairs among the 364 H projective directions. This is ONE globally equivalent full-root SAT problem replacing the earlier ten CAP040H ninth-point orbit branches.

Exact direct F3 reduction: 11 mandatory ones, 52 forced zeros, 2124 free points; 10 mandatory H ones, 42 forced H zeros, 677 free H points. Of 796797 affine 3AP clauses, 55554 are tautologically removed, 11475 become binary exclusions, and 729768 remain ternary. Require >=226 free points, >=79 free H points, and >=3 additional selected opposite H pairs beyond four fixed. For a free/free pair, indicator y implies both selected; for a selected/free pair, the free variable itself is the indicator.

Actual native Z3 15000ms root solve: BUILD=1.632s, CHECK=UNKNOWN reason timeout, total16.712s. Independent HiGHS MILP encoding: 741904 rows, 2216702 nonzeros, 3.09s construction; external 65s hard timeout without SAT/UNSAT. A first implementation bug wrongly required every extra pair to have two free endpoints; corrected, re-ran, and obtained the explicit Z3 UNKNOWN result.

## Theorem B — one universally complete global 15-secant-centre form

C(237,2)=27966 secants are centred at 2187-237=1950 outside points, so some q has >=15 antipodal cap pairs. Projective pair directions form a cap. Those 15 directions must span rank>=5: PG(2,3) caps have <=4 points (5 points generate 20 secant/outside incidences but eight outsiders can support at most16), and PG(3,3) has 40 planes, each point on13; if 15 projective cap directions were confined to a PG(3,3), 15*13>40*4. Select five independent pairs and two further cap vectors to span F3^7, normalize q=0 and +/-e1,...,+/-e5,e6,e7 selected (12 points), plus >=15 antipodal pairs total. This is a SECOND globally complete ONE-branch formulation; no dense-H anchor is assumed at this centre.

Exact reduction: 12 selected, 62 excluded, 2113 free points, 65975 dropped /12412 binary /718410 ternary 3AP clauses, 1047 potential additional pair indicators, >=10 required. Actual native Z3 15000ms check: model build1.553s, UNKNOWN timeout after16.632s.

## Soundness controls and research verdict

Independent direct GF3 arithmetic checked all forced exclusions. An independent GitHub-witness JS normalizer transformed the actual known 236-cap to the dense-centre normal form, finding H size112, outside q=0 with56 selected antipodal pairs; rank4/6/7 frame conditions, 11 mandatory selected points, 236 distinct points, 27730 pair checks, zero 3AP violations all passed. The same known236 witness had full-centre rank5 and56 pairs. All 13 PG(2,3) points and lines and every 5-set were separately checked using exact integer arithmetic.

These are theorem-to-root implication and encoding reductions, NOT closure. Z3 and HiGHS did not determine SAT/UNSAT; no 237-point cap appeared. The exact goal remains OPEN, and the project remains manual-only, CPU-only. A mathematical theorem proving the one global instance UNSAT with independently checked certificate, or a verified construction with a matching upper bound, is still required. The external literature novelty of these elementary normalization lemmas is not established. Full runnable code, raw logs and proof notes in the present-turn archive; **the archive has not been uploaded to Google Drive in this runtime**, while the readable Drive ledger is updated separately.

Root status: NOT DONE (ATTEMPTED).