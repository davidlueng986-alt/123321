# E052 certificate audit — 2026-11-03 UTC

Status OPEN. Objective: independent integrity and compression audit of E051, not repeat LP search.

Local replay: python /mnt/data/E051_verify.py => PASS 15 fixed-prefix certificates, 6210 placements. Additional seven deliberate RHS+1 mutations were rejected by independent coefficient-sum check. All seven integer duals have 360/360 nonzero coefficients, gcd 1; naive gcd compression cannot reduce them. Eight zero-support cases passed original independent replay.

Input E051_CERTIFICATES.json SHA256 b27b2d81946aa1c1e5c3bd2a7a350e0060c7049d8751d0bb670f8bd105223b52; verifier SHA256 ba8f3eaeee3806e4ca5c65440ca4415cb549cba3956e14d9c7dcbd3db5b825f2. Generator SHA256 5ae6ce07b67cab6473d831c6c5f9d3e9809983e0813e7233056859ae916a74d8.

Limitations: mutation check tests only RHS integrity, not arbitrary corruptions. Full JSON and code remain local, not published in this commit. No remote CI replay, no global symmetry orbit excluded. No complete solution.

Literature: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30 ; https://arxiv.org/abs/2605.02132 . Journal: https://docs.google.com/document/d/1NDPWEMM3Cf5HrhdOcV6pVE9tCI-kxKbavxcfIBFva3k/edit .

Next: upload full E051 code/JSON, remote replay, then LP screen remaining E049 source prefixes and prioritize symmetry-complete SAT.
