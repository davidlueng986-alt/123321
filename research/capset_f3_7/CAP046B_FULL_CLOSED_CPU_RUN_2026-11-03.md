# CAP-046 — Actual CLOSED attempt for r₃(7) (2026-11-03 UTC)

## Outcome (no claim of solution)

**OPEN**. No independently verified 237-point cap and no independently checkable global UNSAT proof. The existing 236-point witness remains the verified lower bound; the publicly published upper bound is 291, with Thackeray's 2022 preprint claiming 288 and the team's provisional 287 argument still subject to external classification referee. None of those equals 236.

The CAPSET every-hour research automation (task 6ae77c6ed4f4819191afec5f9b63437a) was **disabled successfully** via the Automations API, and the user's unrelated automations were not changed.

Unlike CAP001–045's mostly verification and subproblem exploration, the following were actual search runs aimed at directly finding a cap >=237 or proving a root-complete branch UNSAT. Only solver results in this document are reported; timeout means UNKNOWN, not infeasible.

## Verified inputs

The exact 236-point fixture was retrieved from the authoritative GitHub branch. The reconstituted UTF-8 file `witness236.txt` has Git blob SHA1 `bb75562499071945a07273e439a892c55a8d6b9f`, matching the repository's canonical `research/capset_f3_7/candidates/calderbank_fishburn_236.txt`. Independently checked: 236 distinct F3^7 points; all 27730 unordered point pairs; zero 3AP triples. Affine hyperplane at first coordinate 0 has 112 points; first-coordinate1 also 112; first-coordinate2 12.

Separate Z3 native C API control: in F3², target k=4 returned SAT and k=5 returned UNSAT. Thus the C API's finite-field lines and `at-least-k` primitives have independent known-value controls. No Z3 UNSAT was found in dimension7, and proof logging was not enabled.

## Closed attack 1: root-equivalent target237 H00 using native Z3

Actual command:

`/usr/bin/timeout 95s ./root_z3 55000 1 1`

Encoded all 2187 Boolean points, all 796797 distinct affine 3AP clauses, `at-least-237`, the rigorous CAP007J `at-least-89` dense hyperplane normalization, and nine selected affine-frame+ninth points with 36 forced nonselected secant points. Model construction completed in 3.3s. After the full 95s external hard wallclock limit, the process exited with code 124 before Z3 had produced SAT/UNSAT. **UNKNOWN**. Native Z3 solver used the locally available `/usr/lib/x86_64-linux-gnu/libz3.so.4`; no GPU or paid compute.

## Closed attack 2: ALL caps with a 112-point 6D hyperplane, conditional root branch

Actual command:

`/usr/bin/timeout 65s ./anchored112_z3 40000 1 0`

Assuming a hypothetical >=237 cap contains a 112-point 6D affine hyperplane, the published affine uniqueness of all dimension-6 maximal 112-caps permits normalizing that entire 112-point hyperplane to the canonical GitHub fixture's first-coordinate0 slice. Fixed 112 selected points, 617 other points in that 6D hyperplane unselected; remaining 1458 7D points free. A necessary and sufficient reduced target becomes >=125 selected free points.

Independent exact local 3AP accounting: of 796797 original lines, 538245 clauses are tautologically satisfied by the zero slice assignments; 81648 become binary exclusions and 176904 remain ternary. Built solver in 0.3s; after 65s external wall limit exit code 124, **UNKNOWN**. This is a complete *conditional* branch, not a proof that r3(7)<=236.

## Closed attack 3: independent CPU HiGHS MILP on whole root H00 leaf

Actual command:

`/usr/bin/timeout 65s python global_h00_milp.py`

Rebuilt the full CAP041 root H00 via separate NumPy/SciPy code, with 2142 free points, nine fixed 1s, 36 fixed 0s. Independent 3AP constraint counts: dropped 38718; binary 9513; ternary 748566. Added full-root cardinality lower bounds >=228 free selected and >=81 free in the 6D dense H, for 758081 rows and 2267559 matrix nonzeros. Build took 14.04s CPU. External 65s timeout exited with 124 before a primal feasible 237-point witness or provable infeasibility status was produced. **UNKNOWN**. This is the same root-complete H00 leaf as attack1 but an independent integer-programming technology.

## Closed attack 4: disproof-oriented search for 112+112+13 constructions

Full candidate algorithm: fix the 112-point first slice S and 112-point second slice T from the verified 236-cap. For every tested invertible GL(6,3) matrix M (generated as products of row shears, swaps, and sign changes), transform T->MT. Compute all 12544 two-slice cross sums and allowed third-slice positions H_M=F3^6\\(-S-MT). If H_M contains >=13 points, run bounded recursive cap search on those positions; any genuine 13-cap would construct a >=237-point cap, independently checked in F3^7 before saving.

**First deterministic pilot:** seed 20261103; 100000 transformations (not deduplicated); hole-count histogram 0:98501, 1:1330, 4:31, 12:138, >=13:0. CPU 1.99s.

**Substantive broader run:** seed 2026110302; **1,600,000** generated transformations, **1,544,404 distinct 6x6 matrices** after deduplication (55596 duplicates), elapsed 33.45 CPU seconds; hole counts **0:1,542,390; 1:1,447; 4:403; 12:164; >=13:0**. Thus there was no possibility of a 112+112+13 construction among these sampled matrices. This is NOT exhaustive GL(6,3) or a global 112+112 theorem. Distinct matrices need not correspond to inequivalent transformed 112-caps. The unusual restriction to hole counts {0,1,4,12} is an empirical clue worth turning into a mathematical theorem, not a bound. No >=237 witness was produced.

## Closed attack 5: large-neighborhood exact MILP relative to verified 236-cap

A separate implementation fixed subsets of the known 236-cap and gave the solver freedom to simultaneously reselect released points and any individually admissible outsiders. For each such finite neighborhood, exact 3AP pair/triple constraints were formed; any candidate returned was checked independently over all 7D triples.

Two selected *conditional neighborhood* integer models completed with HiGHS `status=0 (optimal)` and best size=236:

- Keep 121, free 317; release coordinate-prefix fibers [2,3,4,6,9,10,13,15,17,20,21,22,23,24]; 6193 constraints (3789 binary,2404 ternary); 0.52s; best 236.
- Keep 111, free 283; release fibers [0,3,4,6,8,9,11,13,16,18,24,26]; 3804 constraints (2131 binary,1673 ternary); 0.16s; best 236.

A larger keep126/free350 attempt reached a valid incumbent size144 with HiGHS 8s timeout, no conclusion; and initial keep76/free995 test timed out with a much weaker feasible incumbent. Both remain UNKNOWN, not refutations. These local results are *not* global progress and are explicitly deprioritized.

## Proof status, stopping policy and next actual closure lever

No verified >=237 construction; no verified universal upper<=236. Exact problem remains OPEN. A solution requires one independently checked 237/238/etc witness plus matching global upper bound at its size, OR an independently checked UNSAT certificate of the globally equivalent target237 model plus the 236 witness. Our Z3/HiGHS timeouts are not such certificates. Only the CAPSET hourly automation was paused; no new scheduling is being established or claimed.

The most promising concrete follow-on paths are: (a) a proof-logging SAT solver and independent LRAT/DRAT checker with enough CPU to tackle CAP040's ten *globally complete* branches, not a fixed285 fake cap; (b) a rigorous full GL6 symmetry/double-coset classification to prove or refute 112+112+13, potentially reducing one conditional branch; (c) new constructions not confined to the old236 neighborhood. Do not mistake more proof infrastructure, verification runs, or random matrices for mathematical closure.

Reproduction commands, code, raw logs and the verified 236 fixture are packaged in this bundle. No paid compute or GPU used. Literature priority for new results: unverified; none claimed.

## Relevant sources

- Canonical project branch: https://github.com/davidlueng986-alt/123321/tree/research/capset-f3-7
- Root-equivalent proof tree: https://github.com/davidlueng986-alt/123321/blob/research/capset-f3-7/research/capset_f3_7/CAP040_ROOT_FIRST_PROOF_DAG_2026-11-03.md
- Prior fixed anchor model: https://github.com/davidlueng986-alt/123321/blob/research/capset-f3-7/research/capset_f3_7/CAP041_ROOT_BRANCH_PRESOLVE_2026-11-03.md
- https://arxiv.org/abs/2206.09804 (Thackeray's 288 preprint)
- https://cairn-commons.com/problems/cap-sets-dim-7 (public current open status, 236..291)
## Durable artifact references (uploaded and verified)

Complete runnable CPU source, logs, exact seed and 236 fixture (ZIP SHA256 `5f0057fb0112d24cb491ea88db591837e2960687ec3dec4c1e714fe5c2541506`): https://drive.google.com/file/d/1o8mpVfMfVqqCoAANf9LjEV0I4k8gR-bn/view?usp=drivesdk

Readable Drive-side report: https://drive.google.com/file/d/1eY9bhdsFbmT-2Fcc1a3n284wfFc1ilni/view?usp=drivesdk

Hourly CAPSET automation remains disabled; all SAT branches remain UNKNOWN. See the adjacent concurrent CLOSED_ATTEMPT_ROOT work for a separate Z3 run with globally sound 5D/6D cardinality cuts and 15,000 nonlocal destroy–repair iterations; that independent effort likewise found no matching proof or >236 witness. Do not conflate the two sets of seeds, timings, or model configurations.
