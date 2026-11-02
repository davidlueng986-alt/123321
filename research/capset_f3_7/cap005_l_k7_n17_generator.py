#!/usr/bin/env python3
"""CAP-005L: deterministic exact N=17 seven-fiber conflict certificates.
Input CAP-005K orbit representatives must be independently checked first.
Only a restricted reconstruction obstruction, not a global cap bound.
"""
import argparse
import itertools
import json
from pathlib import Path
from cap005_k6_symmetry_quotient import read_cap, generate_group, image, fiber

HERE = Path(__file__).resolve().parent
third = lambda a,b: tuple((-x-y) % 3 for x,y in zip(a,b))
encode = lambda p: ''.join(map(str,p))

def generate(k7_path, cap_path):
    B = read_cap(cap_path)
    maps = generate_group(B)
    prior = json.loads(k7_path.read_text())
    assert prior['survivor_orbits'] == 1665 and prior['original_survivors'] == 25124
    reps = [row for row in prior['representatives'] if row['N'] == 17]
    assert len(reps) == 37 and sum(row['orbit_size'] for row in reps) == 576
    outsiders = set(itertools.product(range(3), repeat=7)) - B
    secants = {p: set() for p in outsiders}
    for a,b in itertools.combinations(sorted(B),2):
        z = third(a,b)
        assert z in outsiders
        if fiber(a) != fiber(b):
            secants[z].add((min(fiber(a),fiber(b)),max(fiber(a),fiber(b))))
    certificates = []
    for row in reps:
        T = tuple(row['fibers'])
        release = set(T)
        E = sorted(p for p in outsiders if fiber(p) in release
                   and all(a in release or b in release for a,b in secants[p]))
        assert len(E) == 17
        fixed = {p for p in B if fiber(p) not in release}
        witness = None
        for x,y in itertools.combinations(E,2):
            z = third(x,y)
            if z in fixed:
                witness = {'kind':'pair_fixed','points':[encode(x),encode(y)],
                           'third':encode(z)}
                break
            if z in E and z not in (x,y):
                witness = {'kind':'triple_outsiders',
                           'points':[encode(x),encode(y),encode(z)]}
                break
        assert witness is not None, ('no conflict',T)
        assert len({image(T,g) for g in maps}) == row['orbit_size']
        certificates.append({'fibers':list(T),'orbit_size':row['orbit_size'],
                             'N':17,'witness':witness})
    assert sum(c['orbit_size'] for c in certificates) == 576
    return {'scope':'fixed 236-point cap; first-three-coordinate exactly seven released fibers',
            'method':'N=17 forces all 17 eligible outsiders; explicit fixed-point pair or outsider triple contradiction',
            'k7_prior_survivor_orbits':1665,'excluded_orbits':37,
            'excluded_neighborhoods':576,'remaining_orbits':1628,
            'remaining_neighborhoods':24548,'seed':None,'gpu':False,
            'certificates':certificates}

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('prior',type=Path)
    ap.add_argument('--cap',type=Path,default=HERE/'candidates'/'calderbank_fishburn_236.txt')
    ap.add_argument('--out',type=Path,required=True)
    a = ap.parse_args()
    data = generate(a.prior,a.cap)
    a.out.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in data.items() if k!='certificates'},sort_keys=True))
