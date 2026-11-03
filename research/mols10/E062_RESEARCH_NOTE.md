# E062 — Goal-directed scan of public orthogonal-pair data

**Only target:** an independently validated order-10 100/100/100 triple or a complete, unrestricted nonexistence proof. Until then status OPEN.

## Main hypothesis

Ian M. Wanless publishes order-10 MOLS data as 5,562 order-10 Latin squares in 2,781 consecutive orthogonal pairs (first-line format `10 10 5562`, interpreted using the author's `LSformat.html`). Instead of constructing pairs blindly, systematically enumerate every common transversal of each known pair, then test for `9` pairwise disjoint common transversals, which would immediately close the existence problem. If only `8` are disjoint, test the residual 20-cell graph for bipartiteness to close the pair. Both closure gates are mathematically exact, including an independent 100/100/100 verifier.

Source: https://users.monash.edu.au/~iwanless/data/MOLS/MOLS10.txt and https://users.monash.edu.au/~iwanless/data/LSformat.html . Source is attributed to Egan and Wanless, *Enumeration of MOLS of small order*, Math. Comp. 85 (2016).

## Actual local tests

- Egan–Wanless 2016 neartriple A/B independent exact enumeration: 14 common transversals, maximum 7 pairwise disjoint, 6,837 enumeration nodes, exact packing solver status EXACT. Test fixture: `E062_LOCAL_TEST_PAIRS.txt`.
- Independent public order-10 orthogonal pair, `scheinerman/LatinSquares.jl/ortho10.txt`: verified 100/100 Latin and orthogonality; exactly zero common transversals (6,666 search nodes). Source: https://github.com/scheinerman/LatinSquares.jl/blob/master/ortho10.txt . It refutes the idea that a generic orthogonal pair is promising as a seed.
- Full 2,781-pair Wanless scan is designed to run remotely on GitHub Actions because external file hosting is not accessible from this local compute container. Do not describe the full scan as completed or say a result is proven until the generated JSON and independent 100/100/100 checker have been read back. `UNKNOWN_BUDGET` cases remain unproven, never UNEXTENDIBLE.

## Reproducibility

`bash E062_CI_REPLAY.sh` uses Python 3.11+ standard library, requires internet only for the public `MOLS10.txt` download. The source MOLS file itself is *not redistributed*; the script records SHA-256, counts and derived metadata. All pairwise packings are independently enumerated by row/column/A/B-symbol bitmasks and maximum packing is proven through finite bitset clique search unless explicitly marked UNKNOWN.

Even a complete finite scan of 2,781 published pairs with no solution is *not* a global nonexistence proof. It can only falsify the specific route "a publicly tabulated pair has a compatible near-complete transversal packing".