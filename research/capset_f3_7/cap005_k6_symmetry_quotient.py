#!/usr/bin/env python3
"""CAP-005H exact affine symmetry quotient for six-fiber reconstructions.
No optimizer; verifies 236 cap and four explicit affine automorphisms."""
import argparse,json
from pathlib import Path
from collections import Counter
from itertools import combinations
HERE=Path(__file__).resolve().parent

def read_cap(path):
    lines=path.read_text().splitlines()
    assert lines[0].strip()=='n: 7'
    B={tuple(map(int,s)) for s in lines[1:] if s.strip()}
    assert len(B)==236 and all(len(p)==7 and set(p)<={0,1,2} for p in B)
    for a,b in combinations(sorted(B),2):
        assert tuple((-x-y)%3 for x,y in zip(a,b)) not in B
    return B

def fiber(p):return 9*p[0]+3*p[1]+p[2]

def transform_point(p,k):
    a,b,c,d,e,f,g=p
    if k==0:return ((1-a)%3,b,c,f,g,e,d)
    if k==1:return (a,(-b)%3,c,(-d)%3,e,f,g)
    if k==2:return (a,b,(-c)%3,(-d)%3,e,f,g)
    if k==3:return (a,c,b,d,e,g,f)
    raise ValueError(k)

def generate_group(B):
    generators=[]
    for k in range(4):
        assert {transform_point(p,k) for p in B}==B,('invalid automorphism',k)
        mapping=tuple(fiber(transform_point((i//9,i//3%3,i%3,0,0,0,0),k)) for i in range(27))
        assert len(set(mapping))==27
        generators.append(mapping)
    identity=tuple(range(27));group={identity};todo=[identity]
    while todo:
        g=todo.pop()
        for h in generators:
            new=tuple(h[g[i]] for i in range(27))
            if new not in group:group.add(new);todo.append(new)
    assert len(group)==16
    return group

def image(T,g):return tuple(sorted(g[i] for i in T))

def orbit_partition(subsets,maps):
    universe=set(subsets);seen=set();out=[]
    for T in sorted(universe):
        if T in seen:continue
        orbit={image(T,g) for g in maps}
        assert orbit<=universe
        seen.update(orbit);out.append((T,len(orbit)))
    assert seen==universe
    return out

def check(cert_path,cap_path):
    B=read_cap(cap_path);maps=generate_group(B)
    data=json.loads(cert_path.read_text())
    assert data['additional_certificates']==848 and data['unresolved']==88
    U=[tuple(T) for T in data['unresolved_groups']]
    assert len(U)==len(set(U))==88
    assert all(len(T)==6 and tuple(sorted(set(T)))==T and 0<=T[0]<T[-1]<27 for T in U)
    orbits=orbit_partition(U,maps)
    assert len(orbits)==7 and Counter(n for _,n in orbits)=={8:3,16:4}
    full=orbit_partition(combinations(range(27),6),maps)
    histogram=dict(sorted(Counter(n for _,n in full).items()))
    assert len(full)==19464 and histogram=={1:2,2:18,4:139,8:1683,16:17622}
    assert sum(k*v for k,v in histogram.items())==296010
    return {'cap_points':236,'symmetry_order':16,'full_six_fiber_orbits':19464,
            'full_histogram':histogram,'unresolved':88,'unresolved_orbits':7,
            'representatives':[{'fibers':list(T),'orbit_size':n} for T,n in orbits],
            'global_bound_improved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('certificate',type=Path)
    p.add_argument('--cap',type=Path,default=HERE/'candidates'/'calderbank_fishburn_236.txt')
    p.add_argument('--out',type=Path)
    a=p.parse_args();result=check(a.certificate,a.cap)
    if a.out:a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
