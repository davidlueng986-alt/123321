# CAP-032C — Shared-fiber affine orbit-type obstruction for the (7,6,6) AG(4,3) profile

**2026-11-03 UTC.** Exact finite computation of two AGL(3,3) orbit representatives; independently replayed via Python stdlib and previous C++ enumeration. GitHub CI pending until final code commit is completed. No novel global F3^7 numerical upper bound, 237-point witness, or priority claim.

## Universal conditional theorem

Let C be ANY cap in F3^4 with three parallel F3^3 slices of sizes (7,6,6). Then the 7-point slice is AFFINELY EQUIVALENT to the F3^3 7-cap encoded as bitmask 5659, whose AGL3 orbit has exactly 50544 elements; it cannot lie in the other size-75816 7-cap orbit (representative mask 17947). The first type is exactly the orbit of seven-point caps which CANNOT be extended by two further points to a 9-cap within F3^3. The other type is extendable to a 9-cap in exactly one way (relative to a fixed cap).

## Complete exact audit

CAP032B already independently proved exhaustive classification of all 126360 7-caps as two AGL3 orbits of sizes 50544 and 75816. This follow-up enumerates all 107406 6-caps B and considers H=F3^3\(-(A+B)) for each of the TWO canonical 7-cap representatives A. Enumerates every 6-subset of H and checks the exact no-3AP condition.

- First 7-cap orbit (50544 elements, canonical bitmask 5659): 27 B choices give a feasible 6-point third slice, with exactly 27 (B,C) completions.
- Second 7-cap orbit (75816 elements, canonical bitmask 17947): zero B choices, zero completions.
- Direct exhaustive possible 9-cap completions: first representative 0; second representative 1.
- Exact full 19-point 4D cap example with slices represented in little-endian ternary integer codes:
  * size-7: [0,1,3,4,9,10,12]
  * size-6: [0,1,5,8,11,20]
  * size-6: [5,11,12,13,17,23]
  Verified all 171 unordered point pairs directly, no 3AP.

This proves a universally valid **fiber-type** cut, not merely a count inequality. For ANY quotient F3^7 -> F3^4, if some quotient affine line has 3D fiber cardinalities (7,6,6), the 7-fiber's induced seven-cap must be nonextendable to a 9-cap. This can be used when multiple quotient lines SHARE that fiber. It does not by itself imply incompatibility of CAP027's formal285 occupancy assignment, which remains a count-only feasible negative control.

Reproduce:

```bash
python research/capset_f3_7/cap032c_766_orbit_obstruction.py
python -m unittest discover -s research/capset_f3_7 -p 'test_cap032c_766_orbit_obstruction.py' -v
```

Mathematical/strategy note: CAP032B's third-slice maxima and CAP032C's internal orbit-type cut are classical-scale finite combinatorics, and their precise literature priority is unverified. Continue as rigorous testable SAT presolve, NOT as a solution of exact r3(7). The stronger next target is a globally consistent assignment of 3D caps to ALL 81 fibers with the 1080 quotient-line constraints simultaneously, or a proof-logged obstruction for a specified formal occupation pattern. Anchored-112/111 and balanced/no-112 branches remain open. Provisional CAP019 <=287 depends on Thackeray classification that has not been independently reconstructed.
