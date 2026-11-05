# CAPSET-F3-7 — Manual closed/disproof attempt (2026-11-06)

**Final mathematical status: OPEN / NOT DONE.** No >=237 cap, no complete no-237 proof, no new global bound. User's CAPSET hourly automation remains disabled. This file records *failed attempts only*; no local verification is claimed as a mathematical result.

## Root goal and complete-cover boundary

With the already known 236-cap, proving `r3(7)=236` requires ruling out **every** 237-point cap. The n=7 experiments here use an affine frame 0,e1,...,e7, ninth selected point 1222220, and a hyperplane H containing >=89 points (CAP007J). This is just **one H-anchored symmetry branch** out of ten root-complete cases; even its UNSAT would not close the root without the other branches. None of the branches was proven UNSAT.

## Actual disproof attempts

1. Direct exact MILP on known n=5 UNSAT control, target46 (actual max45): all 9,801 3AP lines and 363 affine 4D flats with <=20 cap points. HiGHS 22-second internal time cap: `UNKNOWN`, no incumbent or dual bound.
2. Direct native Z3 for same n=5 target46 and 363 sharp affine 4D flat bounds: **32.0084 s UNKNOWN** after 605,378 conflicts and 824,811 decisions.
3. Strengthened native Z3 n=5 with *all* 10,890 affine 3D flats constrained to <=9 points in addition: **45.0033 s UNKNOWN**, 1,303,655 conflicts. All exact incidence counts checked (1,210 dual 2D normal subspaces x nine cosets).
4. Direct native Z3 n=7 target237, fixed frame+ninth H00, all **796,797** 3AP lines, all **3,279** affine 6D hyperplanes with <=112 cap points and >=89 points in distinguished H: **35.0481 s UNKNOWN**, 15,581 conflicts. No SAT assignment / proof.
5. Completely different signed-projective encoding: translate one selected cap point to 0; for each of 1,093 PG(6,3) directions select none, +v or -v, forbidding **795,704** signed projective 3AP patterns; add all **1,093** through-origin 6D hyperplane <=112 bounds, frame+ninth anchor and >=88 nonzero H points. Native Z3 n=7 target237 **30.0823 s UNKNOWN**; n=5 target46 **30.0106 s UNKNOWN**. n=2 size4 SAT and size5 UNSAT controls checked.
6. Fractional failure diagnosis on n=5: the direct 3AP plus all affine-4D cap<=20 LP relaxation has max **57.166666...** including six fixed frame points, while true integer cap optimum is 45. Adding **every** affine-3D cap<=9 cut leaves LP optimum unchanged (**57.166666...**). Therefore generic slice-size quota tightening does not close the integrality gap. This explains the large number of Z3 conflicts without proof even for n=5.

Note: a first CPU run of the n=5 strengthened model hit the tool wrapper timeout while the subprocess was still running; it subsequently terminated with the Z3 45s UNKNOWN result. Similarly one n=7 wrapper timed out but the underlying Z3 process subsequently wrote its 35s UNKNOWN result. Neither was misreported as UNSAT.

## Root-oriented failure reflection / what must change

- **Structural gap** rather than slight timeout: generic cap/max-subspace cardinality cuts do not encode classifications of large 6D caps. On n=5, even all 3D-flat caps <=9 cannot prove an impossible 46-point cap in 45s; n=7 is drastically harder.
- The existing global moment theorem only forces a 6D section of >=89 for a hypothetical 237 cap, **23 below** 6D optimum112; existing classifications of 110–112 cap sections therefore do not cover all cases. Any use of 112-slice classification alone is **conditional**, not a complete disproof.
- A logically sound alternative root plan is to prove every 236-cap is complete (every outside point has at least one secant) *without assuming affine uniqueness*; this is equivalent to no237 and needs genuinely new universal geometry. The known 236 witness alone has min outside secant degree10, but says nothing about other 236 caps and is **not** progress toward that universal statement.
- A radically improved method would require a **universally valid** high-dimensional stability/structure lemma for every >=237 cap, with a complete orbit cover that makes the remaining exact subproblems provable. No such lemma was found here. Do not rerun these generic solver encodings with only longer timeouts unless a quantitatively stronger universal cut is derived.

## Verification of artifacts and honesty boundary

The bundle includes C++17 native-Z3 C-API sources, Python HiGHS/LP sources, raw stdout/stderr (including precise UNKNOWN statuses), compile commands, and the direct n=2 controls. Exact-size outputs in this report are not new mathematical records. No paid services/GPU. No background or hourly research restarted.

To reproduce on a Linux system with `libz3.so.4`:

```bash
g++ -O2 -std=c++17 capset_root_z3_codim1.cpp -o capset_root_z3_codim1 -L/lib/x86_64-linux-gnu -l:libz3.so.4
./capset_root_z3_codim1 5 32
./capset_root_z3_codim1 7 35

g++ -O2 -std=c++17 capset_root_z3_codim2.cpp -o capset_root_z3_codim2 -L/lib/x86_64-linux-gnu -l:libz3.so.4
./capset_root_z3_codim2 5 45

g++ -O2 -std=c++17 capset_projective_signed_z3.cpp -o capset_projective_signed_z3 -L/lib/x86_64-linux-gnu -l:libz3.so.4
./capset_projective_signed_z3 2 5 5
./capset_projective_signed_z3 5 30 46
./capset_projective_signed_z3 7 30 237

OPENBLAS_NUM_THREADS=1 python capset_root_milp_6d_cuts.py --n 5 --seconds 22
OPENBLAS_NUM_THREADS=1 python capset_lp5_codim2.py
```

All actual 7D proof branches **remain UNKNOWN**. No claim of "nearly solved" is warranted.
