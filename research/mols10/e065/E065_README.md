# E065: Direct 3-MOLS(10) CLOSED attempt, exact complete OA

**Only success:** independent full `100/100/100` witness, or independently checked unrestricted nonexistence proof. **Status: OPEN**, 0/1,700 globally excluded; no ETA. Hourly automation remains off.

This directory contains two different complete five-coordinate OA encodings: CNF using 33,000 vars/101,740 clauses and native PB using 41,338 placements/1,000 exact-one constraints. Both use the pre-existing E064 **1,700 paratopy branch list**. Small-order positive controls and all n=6 classes are checked; n=10 is UNKNOWN.

## Single command (offline Z3)

```bash
bash E065_replay.sh
```

Requires `g++`, Python 3, system `libz3.so.4`. The replay generates the CNFs, compiles both incremental solvers, checks n4/n5 SAT and n6 3/3 UNSAT using both, independently compiles and runs E064 C++ DLX over all three n6 branches, and spends 2 seconds each on three n10 branches. No remote calls.

For sampled n10 branches:

```bash
./E065_incremental_z3 E065_n10.cnf 10 5 E064_12_representatives.jsonl 16 0 probe_cnf.jsonl
./E065_pb_oa 10 5 E064_12_representatives.jsonl 16 0 probe_pb.jsonl
```

For a standalone CNF with external LRAT proof pipeline (requires CaDiCaL/lrat-check):

```bash
bash E065_cadical_proof.sh 5 0 30 E065_n5_reps.jsonl
bash E065_cadical_proof.sh 10 0 60 E064_12_representatives.jsonl
```

**Do not call order-10 UNKNOWN a nonexistence proof.** The `cadical_proof.sh` external solver/independent LRAT checker path has not yet been executed locally because tools are unavailable. Consult `E065_REPORT.md` for exact results and limitations. A copy of `E064_12_representatives.jsonl` is included in the standalone archive; in the repository the canonical file is at `../e064/E064_12_representatives.jsonl`.