# CAP-042 — Independent complete ten-leaf incidence census (2026-11-03 UTC)

Continues CAP-041 after reading the current branch and Drive ledger. CAP-041 code CI #41622010906 is **SUCCESS** (head a27982e3e0279123178cbbd202405b6d88ea50c1). The ten globally covering dense-H branches remain SAT/UNSAT UNKNOWN.

**Substantive bounded step:** independently compute the exact literal-substitution 3AP clause counts for **all ten** CAP-040H ninth-point orbit representatives. This checker does not import CAP-040/041 or enumerate all 796797 triples ten times. It constructs the 9 selected points and their forced secant-zero set; the union of lines incident to the forced zeros is deduplicated via canonical sorted triples. Separately, it deduplicates lines through exactly one selected point and two free points. The residual is the ternary count by subtraction from the independently known total 796797. The complete H-orbit representatives are independently obtained from barycentric S7 types, 701 eligible ninth points in ten types. No SAT solver, proof log, random seed, GPU or paid compute.

| Branches | Forced zeros | Dropped | Binary | Ternary | CNF variables | CNF clauses |
|---|---:|---:|---:|---:|---:|---:|
| H00–H04, H06 | 36 | 38718 | 9513 | 748566 | 517533 | 1786028 |
| H05 | 36 | 38733 | 9513 | 748551 | 517533 | 1786013 |
| H07–H08 | 36 | 38724 | 9516 | 748557 | 517533 | 1786022 |
| H09 | 35 | 37662 | 9526 | 749609 | 517843 | 1787700 |

All ten local CPU checks PASS. Note the nontrivial finding: H05, H07, H08 have different tautology/line-incidence totals even though all have 36 forced zeros. A generic H00-derived clause count cannot be reused for every leaf. H09 has one fewer forced zero. This closes the CAP-041 aborted eight-of-ten census gap, **but does not establish satisfiability or unsatisfiability**.

Reproduce: `python research/capset_f3_7/cap042_ten_leaf_incidence.py`. No random seed. The source includes exact assertions for each branch; GitHub CI should be checked independently after commit.

**Meta-audit:** Every leaf still requires a checked SAT witness or UNSAT certificate. Ten giant root-equivalent instances are a proof roadmap, not an efficient solver by themselves. Avoid interpreting incidence differences as difficulty estimates. Next: CPU-bounded proof-logged H00 SAT pilot and independent certificate validation; explore stronger universal pruning if solver stalls. CAP-019 upper-bound classification still requires external referee. No >=237 cap, new global upper bound, or exact determination of r3(7). Novelty not established.
