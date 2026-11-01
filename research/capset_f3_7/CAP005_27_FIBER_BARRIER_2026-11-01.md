# CAP-005A — exact <=4 coordinate F3^4 fiber edit obstruction

Date: 2026-11-01 UTC. Status: LOCAL EXACT CPU PASS; CI confirmation pending. **Restricted theorem only**, not a global bound on r3(7).

**Theorem.** Let C be the known 236-point Calderbank–Fishburn/Bierbrauer–Edel cap. Partition F3^7 into 27 fibers indexed by the first three coordinates, each isomorphic to F3^4. If a cap A agrees with C outside at most four fibers, then |A| <=236.

**Exact proof.** For outsider x, enumerate all original pairs {a,b} with a+b+x=0 mod 3. If x is selected, each such pair requires deleting a or b. When only fibers in R may change, a necessary condition is fiber(x) in R and each original secant {a,b} has at least one endpoint in R. Enumerate all R with 1<=|R|<=4. The complete histogram (admissible outsiders : number of R) is:

- k=1: {0:27}
- k=2: {0:335,1:16}
- k=3: {0:2501,1:408,2:8,4:8}
- k=4: {0:12510,1:4320,2:408,4:160,5:96,6:56}

Thus <=4 released fibers permit at most 6 outsiders. There are 1951 outsiders in total; exact mod-3 secant counts per outsider range from 10 to 56. The secants through any fixed x are disjoint pairs because each a uniquely determines b=-x-a. Therefore adding any outsider forces >=10 original deletions. A cap with an outsider has size <=236-10+6=232; without outsiders it has size <=236. This proves the restricted theorem.

**Reproduce:** `python research/capset_f3_7/cap005_27_fiber_barrier.py`; `python -m unittest discover -s research/capset_f3_7 -p 'test_cap005_27_fiber_barrier.py' -v`. Deterministic CPU scratch replay 2.6 s; 20,853 released-fiber sets; direct independent `verify_capset.py` arithmetic baseline checker. No GPU, random seed, optimizer or paid compute.

**Meta-audit.** Translation-only 27-block twists preserve total point count and cannot produce 237, even if cap-valid. Must instead alter occupancies or use nonlocal templates affecting >=5 fibers. This theorem does not exclude non-invariant large-neighborhood constructions and its literature novelty is not established. Literature check 2026-11-01: public status 236<=r3(7)<=291; Thackeray arXiv:2206.09804 claims <=288 in preprint, not independently reviewed here; Grace/Voloch 2026 algebraic capsets do not settle n=7.
