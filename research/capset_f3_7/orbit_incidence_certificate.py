#!/usr/bin/env python3
"""Exact orbit-wise incidence lemma for the 236-point Calderbank–Fishburn cap.

For a chosen outsider set B contained in a single symmetry orbit O:
each outsider has s(O) old-old secants; any deleted original point hits
at most t(O) secants with third point anywhere in O.
Thus s(O)|B| <= t(O)|R|. Whenever s(O)>t(O), |R|>|B|,
so any nonempty B from that orbit alone strictly DECREASES cap size.

No linear-programming/heuristic assumptions: integers only.
"""
from collections import Counter
from symmetry_isolation_certificate import A, G, act, ORBITS, sec

records=[]
for representative, orbit_size, s in sorted(ORBITS,key=lambda o:(o[2],o[1])):
    orbit={act(representative,g) for g in G}
    assert len(orbit)==orbit_size
    incident=Counter()
    for p in orbit:
        assert len(sec[p])==s
        for i,j in sec[p]:
            incident[i]+=1;incident[j]+=1
    t=max(incident.values())
    assert sum(incident.values())==2*s*orbit_size
    records.append((representative,orbit_size,s,t))
eligible=[r for r in records if r[2]>r[3]]
assert sorted(r[1] for r in eligible)==[1,2,24,32,32,60]
assert sum(r[1] for r in eligible)==151
assert sorted((r[1],r[2],r[3]) for r in eligible)==[
  (1,38,1),(2,56,1),(24,10,3),(32,11,4),(32,30,10),(60,25,15)
]
print("VERIFIED ALL 14 ORBIT INCIDENCE COUNTS")
for rep,n,s,t in records:
    print("ORBIT", "".join(map(str,rep)), "size",n,"secants",s,"maximum_old_endpoint_incidence",t, "no_gain_from_orbit_alone",s>t)
print("EXACT OBSTRUCTION: any extension using outsider points solely from ONE of 6 listed orbits (151 points total) strictly reduces the original cap cardinality.")
print("Do NOT infer that using mixtures of these orbits is obstructed.")
