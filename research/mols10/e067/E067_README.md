# E067 — Global mathematical constraints for closing 3-MOLS(10)

**Status OPEN.** This iteration answers whether more CPU is the main blocker: the public literature and our full-class tests instead point to weak domain-specific propagation as a major bottleneck. This package does **not** contain a 100/100/100 witness or a global UNSAT certificate.

Run `bash E067_REPLAY.sh` (requires Python and NumPy). It verifies spectral adjacency against a second implementation, checks all 1700 representative classes against two mathematically necessary constraints, and independently enumerates the common transversals of two published order-10 orthogonal pairs. The full 1700-class root screens eliminate **zero** classes. The completed E066 proof-campaign ledger records **1700 UNKNOWN**; it does **not** prove UNSAT.

Read `E067_REPORT.md` for theorem proofs, the discovered initial spectral modeling bug and correction, negative results, source citations, and implementation priorities.

**Caution for future proof-producing SAT solvers:** If you add mathematically justified but non-DRAT-derivable GF(2) relation clauses to a CNF, checking an LRAT proof for that *augmented CNF* does not alone certify the original problem. The added clauses require separate, auditable mathematical derivations (or a formal proof of redundancy). Never report the unaugmented problem UNSAT merely from a proof for a strengthening whose safety has not been checked.