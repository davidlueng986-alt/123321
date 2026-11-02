#!/usr/bin/env python3
"""CAP-005K: exact quotient of CAP-005J's 25,124 seven-fiber survivors.
Uses the independently verified 16-element affine stabilizer. This is a
restricted necessary-only search reduction, not a global r3(7) bound.
"""
import argparse
import json
from collections import Counter
from pathlib import Path
from cap005_j_k7_gate_incidence import census, rank, unrank
from cap005_k6_symmetry_quotient import read_cap, generate_group, image, orbit_partition

HERE = Path(__file__).resolve().parent

def mask(T):
    return sum(1 << i for i in T)

def run(cap_path):
    B = read_cap(cap_path)  # independent exact arithmetic cap verification
    maps = generate_group(B)  # verifies each affine generator pointwise on B
    baseline, counts = census(cap_path, return_counts=True)
    assert baseline['not_excluded'] == 25124
    survivors = {tuple(unrank(i)) for i, n in enumerate(counts) if n >= 17}
    assert len(survivors) == 25124
    partition = orbit_partition(survivors, maps)
    assert len(partition) == 1665
    orbit_hist = Counter()
    N_hist = Counter()
    # Compute actual released baseline occupancy from B, not from aggregate histogram.
    by_fiber = Counter(9*p[0]+3*p[1]+p[2] for p in B)
    reps = []
    for T, size in partition:
        orbit = {image(T, g) for g in maps}
        assert len(orbit) == size
        N = counts[rank(mask(T))]
        assert N >= 17 and all(counts[rank(mask(u))] == N for u in orbit)
        orbit_hist[size] += 1
        N_hist[N] += 1
        reps.append({'fibers': list(T), 'N': int(N), 'orbit_size': size,
                     'baseline_occupancy': sum(by_fiber[i] for i in T)})
    assert dict(orbit_hist) == {4:3, 8:185, 16:1477}
    assert sum(s * v for s, v in orbit_hist.items()) == 25124
    assert sum(v for v in N_hist.values()) == 1665
    assert N_hist[198] == 1 and N_hist[17] == 37
    assert max(N_hist) == 198
    assert baseline['excluded_by_16_outsider_gate'] + sum(s*v for s,v in orbit_hist.items()) == 888030
    return {'scope':'fixed 236 cap, first-three-coordinate seven-fiber edits only',
            'status':'EXACT_SYMMETRY_QUOTIENT_NECESSARY_ONLY_NO_GLOBAL_BOUND',
            'group_order':len(maps), 'original_survivors':len(survivors),
            'survivor_orbits':len(reps),
            'orbit_size_histogram':{str(k):v for k,v in sorted(orbit_hist.items())},
            'N_orbit_histogram':{str(k):v for k,v in sorted(N_hist.items())},
            'max_individually_admissible_outsiders':198,
            'max_N_orbits':1, 'seed':None, 'gpu':False, 'representatives':reps}

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--cap', type=Path, default=HERE/'candidates'/'calderbank_fishburn_236.txt')
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    result = run(a.cap)
    a.out.write_text(json.dumps(result, sort_keys=True, separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('representatives','N_orbit_histogram')},sort_keys=True))
