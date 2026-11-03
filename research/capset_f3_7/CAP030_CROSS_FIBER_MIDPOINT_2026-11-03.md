# CAP-030 — Cross-fiber midpoint exclusion (2026-11-03 UTC)

Continuation from CAP-029 CI-success head cc8ea8546c6aeba53f1a28c773e5900e08b24a09. No GPU, random seed, SAT solver or paid compute.

## Exact necessary point-level constraint
For an affine quotient line with three fibers A_0,A_1,A_2 ⊂ F_3^3, define M(A_i,A_j)={-a-b : a∈A_i,b∈A_j}. Since (a,i)+(b,j)+(c,k)=0 for three distinct quotient points i,j,k on the same affine line, cap-freeness implies A_k∩M(A_i,A_j)=∅. Thus |A_k|≤27−|M(A_i,A_j)|. This is a point-level constraint, stronger than cardinality-only |A_0|+|A_1|+|A_2|≤20 for fixed fiber assignments. For a given fiber X participating in multiple quotient lines, all midpoint exclusions must be imposed simultaneously on the SAME X; independently lifting each line cannot certify a global cap.

## Exact regression on repaired CAP-028 witnesses
The three cyclic cross-fiber midpoint-image cardinalities are [23,19,19] for the 18-point (7,7,4) cap, and [20,19,20] for the repaired 19-point (7,6,6) cap. The former has exactly 4 allowed sites in its third fiber given the first two fibers and saturates the exclusion bound |A_2|≤4. This is a property of that explicit witness, not a universal extremal theorem for all (7,7,*) configurations.

## Reproducibility
Run: python -m unittest research/capset_f3_7/test_cap030_midpoint_compatibility.py (from repository root). Exact modulo-3 arithmetic; tests include both repaired witnesses and an intentionally invalid midpoint insertion. The existing CAP028 JSON is read directly; no candidate set of size ≥237 is produced. CI status must be checked after commit.

## Research decision
Prior count-only negative controls remain intact; next useful experiment is a shared-fiber SAT/PB pilot with one 3D fiber variable reused across intersecting quotient lines, plus independently checked satisfiability witnesses or proof-logged UNSAT. CAP-019 ≤287 remains provisional until independent Thackeray completion classification audit. No new global bound; exact r_3(7) OPEN. Novelty of the elementary midpoint observation is not claimed.
