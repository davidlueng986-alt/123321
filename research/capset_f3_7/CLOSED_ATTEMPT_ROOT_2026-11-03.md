# CLOSED ATTEMPT — CAPSET-F3-7, 2026-11-03 (UTC)

## Mission and automation change

**Only objective:** determine exact `r_3(7)`, making the open problem closed. At the user's explicit request, the hourly automation `Cap Set Hourly Research`, task ID `6ae77c6ed4f4819191afec5f9b63437a`, was **successfully paused** using `Automations.update(is_enabled=false)`, confirmed `success=true`, `is_enabled=false`. No new recurring automation was created. Do not restart it without explicit permission. Research is pursued only upon direct request (or separate explicit authorization).

The independently verified classical 236-point cap remains the lower-bound construction. A new >=237 verified cap would disprove equality r3(7)=236 but would NOT by itself establish exact r3(7). A full proof of no 237 cap, together with the 236 witness, would close the problem at 236.

## Two REAL CPU closed attempts, not merely verifier maintenance

### A. Solve one complete root-problem SAT branch

The dedicated CAP040H root proof DAG establishes a logically exhaustive ten-way split of all hypothetical >=237 caps. The H00 branch fixes nine selected points 0,e1,...,e7,(1,2,2,2,2,2,0), excludes all 36 third points of pairs, and distinguishes a 6D hyperplane H with >=89 selected points (from the established CAP007J third-moment lemma). A C++17 solver was compiled using the installed **Z3 4.13.3** `libz3.so.4` library (the CLI Kissat/CaDiCaL/MiniSat were not installed, and internet DNS was unavailable).

Instead of stopping at DIMACS generation, **the actual native Z3 solver was invoked** on the root-equivalent H00 problem. Exact direct-line arithmetic generates all 796797 affine lines, reduced to 9513 binary and 748566 ternary nontrivial constraints, with 38718 satisfied by fixed zeros. Z3's native pseudo-Boolean constraints require >=228 selected among 2142 free points, >=81 selected among the 693 free points of H, plus universal at-most-112 on all 21 coordinate hyperplanes and (stronger version) at-most-45 on all 189 coordinate 5D flats.

- n=3 target10 calibration: Z3 returned UNSAT in ~0.38s (no UNSAT certificate). 
- n=4 target21 calibration: Linux 15s walltime cap terminated without SAT/UNSAT.
- n=7 root H00 with 6D constraints: external CPU timeout; UNKNOWN.
- n=7 root H00 with 6D+5D constraints: internal Z3 timeout=12000ms; **solver explicitly returned UNKNOWN reason=timeout**, total 13.87s including 1.8s model-build. It did NOT return SAT, UNSAT or a proof certificate.

**This is not a global proof:** H00 is one of ten exhaustive branches, and none of these root SAT branches has a checked UNSAT proof. The current Z3 C++ wrapper does not produce a DRAT/LRAT/FRAT proof. Nothing can be promoted from timeouts.

### B. Construct a >236 cap as 112 + 112 + >=13

Independent Python mod3 arithmetic re-constructed the classical two 112-point 6D slices from its explicit (6,3,2) design and checked the full 236-point union: all 236 points distinct, 27730 unordered pairs, zero forbidden 3APs, and precisely 12 unblocked third-slice positions (the twelve signed unit vectors).

Compiled and ran C++17 over **170001** relative GL(6,3) alignments of the second 112-point slice, seed=20261103. This combined uniformly random invertible matrices, short products of elementary matrices, and longer random elementary words. Every alignment's 112×112=12544 cross-slice pairs were computed exactly; an actual 237 witness would be emitted only after checking a 13-point cap subset of unblocked third positions.

Observed histogram: holes 0:160529, 1:8214, 4:264, 12:994; maximum holes **12**, no 13-hole candidate and no 237-point cap. Runtime ~23.59s CPU. This is a *finite sample*, not exhaustive GL(6,3).

Second independent seed=20261104 added Fourier high-support overlap measurement for **45001** alignments (C++17), with histogram holes 0:42429, 1:2257, 4:68, 12:247; maximum again12. All sampled cases with holes 4 or 12 had exactly **16 common special projective Fourier directions**, whereas all sampled one-hole alignments had 0 shared. This overlap–holes relationship is **a new testable hypothesis**, NOT an established universal theorem and NOT evidence that every 112+112 construction is capped at236. Across the full 215002 sampled alignments (including identity twice), no >=237 witness appeared.

Compilation failure preserved: an early C++17 `apply` helper name collided with `std::apply`; renamed to `matapply` and reran. The results above are the corrected source. No GPU, paid compute, or background job.

## Artifact chain and exact commands

All original C++ sources, trial logs, readme and SHA metadata were successfully uploaded as a ZIP inside the *dedicated* CAPSET Google Drive folder:

`https://drive.google.com/file/d/1_c7bf_JyXIgO_RFPEvg4CVW-KYzijUyd/view?usp=drivesdk`

Local bundle archive `CAPSET_CLOSE_2026_11_03.zip`, SHA256 `92e1d8a7cd15c4edbc4893e38de4ca5652ad82bfe688f5d56c2981e53efbd63c`; individual code SHA:
- native-Z3 C++ `13361cabe0a38f6be31c9bd59049a0f96f1b00f5f6e7e8900377ab52fef05e04`;
- Fourier GL6 C++ `7cabef1addc04dcce4c05fd4ead68fdb427b37432fb48a90da58ed824f602905`;
- GL6 no-Fourier C++ `dec4a4214c38b8b1230937cb73c155c24d9461729acc047c5e0ba0079a42fa1b`.

Commands (from extracted archive folder; C++17, Linux):

```bash
g++ -O2 -std=c++17 cap_close_z3.cpp -L/lib/x86_64-linux-gnu -Wl,-rpath,/lib/x86_64-linux-gnu -l:libz3.so.4 -o cap_close_z3
./cap_close_z3 7 237 12000 1   # complete H00 root SAT leaf; returns UNKNOWN at timeout
g++ -O3 -std=c++17 cap_close_gl6.cpp -o cap_close_gl6
./cap_close_gl6 170000 20261103
g++ -O3 -std=c++17 cap_close_gl6_fourier.cpp -o cap_close_gl6_fourier
./cap_close_gl6_fourier 45000 20261104
```

No leakage of secrets/tokens. No MOLS10 or unrelated branch files touched.

## Goal-first meta-decision

The only durable outcome so far is **OPEN**. Do not claim new global upper/lower bound, solver proof, or literature priority. The current *root* hard barrier is finding either a SAT model for any of ten global >=237 branches, or an independently checked UNSAT proof for all ten. Simple Z3 + known slice bounds did not terminate. The construction branch 112+112+13 also failed to find a witness despite 170k+ GL6 attempts; do not endlessly rerun unstructured random transformations. The Fourier overlap sample suggests studying special m*=16 alignments *only if* it directly yields a 13-cap witness or rigorous universal case-exclusion with a bridge to the root.

Next serious closed attempt, only when requested: a scalable proof-producing SAT/CP-SAT implementation for ALL globally complete leaves and a separate nonlocal constructive algorithm not assumed near 236 or near two full 112 slices, with exact independent witness/certificate checks. Avoid routine regression-only scheduled research. Do not presume r3(7)=236.

## Literature status

- As of 2026-10-03, public status remained OPEN with 236 <= r3(7) <=291: https://cairn-commons.com/problems/cap-sets-dim-7
- Thackeray 2022 preprint arXiv:2206.09804 claims <=288, not independently reviewed in this campaign; CAP019 provisional <=287 is also not independently refereed.
- FunSearch high-dimensional program search, Nature 2024, is a construction-search precedent, but no exact r3(7) closure was found.

## Further actual unrestricted 7D construction attempt: 15,000 nonlocal destroy–repair runs

To avoid overfitting the rigid 112+112 split, a separate C++17 builder explicitly maintained arbitrary cap sets in the FULL 2187-point F3^7 geometry. Starting from the independently validated classical 236 cap, each trial removed 70–195 random existing points and greedily reinserted any unblocked point using randomized candidate-pair interaction scores. The algorithm did **not** require preserving any 112-slice/fiber occupancy, special automorphism or fixed relative GL6 alignment; each step maintained no3AP by exact incremental third-point counts.

Seed=20261105, **15000 full long-range destroy–repair trials**, ~15.61 CPU seconds. Best cap size remained **236**, no >=237 witness. 7122 trial reconstructions returned to size236; other results typically below236. This is a randomized constructive attempt, not a complete search or upper bound; the fact that many trials reassemble the original witness is evidence of a strong local basin for this heuristic, not evidence of universal optimality.

Additional runnable source and raw complete log uploaded to the same dedicated Drive folder:
- C++17: https://drive.google.com/file/d/1wx1SuOhRq-V2MfmKHhNh_afzXiyIvy3i/view?usp=drivesdk
- 15000-trial raw log: https://drive.google.com/file/d/1wyhzxvopruCFzXcS1dN6XXyEI9SyeBhG/view?usp=drivesdk

Compile `g++ -O3 -std=c++17 cap_close_destroy_repair.cpp -o cap_close_destroy_repair`; run `./cap_close_destroy_repair 15000 20261105`.

### Concurrency reconciliation with CAP-046

While this run was active, another in-flight CAP-046 agent committed independent, root-relevant full 237-cap MILP and affine-union constructor attempts. See `CAP046_CLOSED_ATTEMPT_2026-11-03.md`; preserve them. Its SciPy HiGHS global 796797-line feasibility model timed out without SAT/UNSAT, and some restricted 236+affine-image union MILPs reported local infeasibility/feasibility diagnostics, none proving a global bound. It also produced an exact formal integer countermodel showing aggregate moment+quadratic-spectrum conditions alone do not force a 90-point hyperplane. These are complementary to the native-Z3 and long-range GL6/direct cap attempts here. **No 237 witness or matching bound was found in any of these contemporaneous attempts.** User-requested hourly automation remains disabled; no task restart.
