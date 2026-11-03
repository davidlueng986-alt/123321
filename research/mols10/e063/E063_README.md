# E063 local seven-class pattern: mathematically certified partial closure only

**Sole success criterion for global 3-MOLS(10): complete 100/100/100 witness or unrestricted independently checked nonexistence proof. Current status OPEN.**

Quick reproducibility (Python 3.11; independent verifier uses only Python standard library):

```bash
python3 verify_E063.py
python3 paratopy_audit.py
python3 complete_C.py
# The discovery implementation requires networkx:
python3 classify_C.py
python3 export_group.py
python3 explicit_autotopisms.py
# Optional exact bounded solver on the first representative (requires system libz3.so.4):
python3 z3_full_C7.py 3 0
# Optional C++ one-mate search; UNKNOWN_BUDGET is NOT UNSAT:
g++ -std=c++17 -O3 mate_dlx.cpp -o mate_dlx
./mate_dlx 0 0.5 100000 C7_all_complete.txt
```

`verify_E063.py` reenumerates all 216 C completions, checks all 18 certified symmetry actions on every completion, verifies the 14 orbits, checks the three nontrivial autotopism certificates, and tests certificate tampering. A published theorem (McKay, Meynert and Myrvold 2007) then excludes those three representative classes from a full triple. Eleven orbits remain open. Z3 on the other representatives returned UNKNOWN on bounded runs. This is one fixed source pattern, not a global proof.