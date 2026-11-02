# CAP-005C — exact rational LP-dual obstruction for all five-fiber edits

Date: 2026-11-01/02 UTC. Status: LOCAL CPU exact-rational PASS; CI pending.
Scope: only the 27 fibers of F3^7 indexed by its first three coordinates, with at most five editable fibers of dimension four. **Not** a global upper bound on r3(7).

**Theorem (restricted).** No cap obtained by changing points of the published 236-point Calderbank–Fishburn/Bierbrauer–Edel cap in at most five of these fibers can contain 237 points.

**Proof.** The previous CAP-005A certified all edits involving <=4 fibers. For exactly five released fibers, enumerate all C(27,5)=80,730 choices. A candidate outsider x is admissible only when every original secant through x has an endpoint in a released fiber. Exactly 80,418 choices admit fewer than 10 outsiders; since any outsider requires >=10 original deletions, these choices cannot improve 236.

The remaining **312** five-fiber choices admit >=10 outsiders (at most 22). Freeze the original points in the other 22 fibers. Variables correspond to all original points in the five released fibers plus admissible outsiders. Enumerate all triples x+y+z=0 among the variable and frozen points; with f frozen members in a triple, impose sum(variable members)<=2-f. Also 0<=x_i<=1. A valid replacement cap must satisfy this LP relaxation. The known original 236 cap is feasible.

For each of the 312 LPs, SciPy HiGHS proposes a dual solution. **The floating-point answer is not trusted as proof.** Convert all dual coefficients to exact rational fractions (denominator <=1000) and check with integer/rational arithmetic:
- all row multipliers y_i and variable-upper-bound multipliers z_j are nonnegative;
- for every candidate variable j, (A^T y)_j+z_j >=1;
- the exact dual objective b^T y + sum(z_j) is at most the number of original points in the five released fibers.

These exact inequalities prove the maximum selected variable count cannot exceed the original selected count. The 312 duals all passed this exact checker in a local CPU run (~20 seconds); the remaining 80,418 cases are excluded by the elementary 10-deletion gate. Therefore **the restricted optimum for all <=5 fiber edits is 236**. This does not exclude nonlocal 237 constructions.

**Reproduction and artifacts.** `python -m pip install scipy==1.16.3` then `python research/capset_f3_7/cap005_k5_rational_duals.py --out /tmp/cap005_k5_rational_duals.json`. The output JSON contains all 312 nonzero rational dual coefficients and their associated five-fiber indices. The source reconstructs the full constraint matrices deterministically from the immutable 236 fixture; it invokes `verify_capset.py` for independent exact arithmetic of the baseline and rechecks every dual in exact fractions. CI publishes a 30-day JSON artifact. No GPU, randomness or paid compute.

**Meta-audit.** This supersedes the earlier k=5 necessary-condition-only inconclusive gate; the LP relaxation itself is already strong enough for every five-fiber choice, with exact rational dual witnesses. Further local edits of <=5 such fibers are mathematically incapable of improving 236. Next prioritize >=6 fibers, non-coordinate/nonlocal templates, or rigorous global upper-bound research. Literature novelty of this restricted result is unverified. Global r3(7) remains OPEN; Thackeray arXiv:2206.09804 is a separate unreviewed 288-bound preprint.
