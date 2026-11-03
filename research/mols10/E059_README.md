# E059 reproducible mathematical checks (no credentials)

Research status: **OPEN**, no full 3-MOLS(10) witness or universal nonexistence proof.

Source: E059_REPORT.md. All files are preserved in this directory with relative paths.

## Core checks (no extra Python packages)

```bash
node E059_verify_independent.js
node E059_verify_endgame.js
python3 E059_endgame_control.py
```

- The first JS verifier checks **exact** 360/360 half-integral k4, 360/360 integral k4 and 180/180 integral k7 resource equalities; negative mutation rejected.
- The second JS verifier enumerates exactly 5,392 last-two-row completions of nine fixed 8-row prefixes from Jäger et al 2024 Figure3; zero produce a full triple.
- Python positive control constructs 3 MOLS of order4 over GF4 and finds 2 complete solutions among 64 endgame completions.

## Recompute from source (SciPy for cyclic discovery only)

```bash
python3 E059_Egan_integral.py
python3 E059_integral_k7_witness.py
python3 E059_2024_9x10.py
python3 E059_8row_endgame.py
python3 E059_cyclic_quotient.py 4 800
python3 E059_verify_primal.py
```

The 2024 9x10 data are attributed to *Enumeration of Sets of Mutually Orthogonal Latin Rectangles*, EJC 31(1) P1.53 Figure3, https://doi.org/10.37236/9049. The 2 MOLS order10 pair is attributed to Egan and Wanless (2016), https://doi.org/10.1090/mcom/3010.

`E059_cyclic_quotient.py` calls SciPy HiGHS for discovery. The exact math claims **do not depend on HiGHS output**: full independently checked witness JSONs are shipped. The larger cyclic-family sample has 26 UNKNOWN integer cases and is not an exhaustive proof.

All claims concern identified *fixed* partial configurations, except the explicit universal-counterexample consequence (showing two proposed universal nonexistence lemmas are false). There is no claim of a solution to 3-MOLS(10).
