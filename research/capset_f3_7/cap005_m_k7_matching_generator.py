#!/usr/bin/env python3
"""CAP-005M: deterministic seven-fiber outsider pair matching certificates."""
import argparse,itertools,json
from pathlib import Path
from cap005_k6_symmetry_quotient import read_cap,generate_group,image,fiber
HERE=Path(__file__).resolve().parent
def third(a,b): return tuple((-x-y)%3 for x,y in zip(a,b))
def enc(p): return ''.join(map(str,p))
def generate(prior_path,cap_path):
    B=read_cap(cap_path); G=generate_group(B)
    prior=json.loads(prior_path.read_text())
    assert prior['survivor_orbits']==1665 and prior['original_survivors']==25124
    outsiders=sorted(set(itertools.product(range(3),repeat=7))-B)
    req={p:set() for p in outsiders}
    for a,b in itertools.combinations(sorted(B),2):
        z=third(a,b)
        if fiber(a)!=fiber(b):req[z].add(tuple(sorted((fiber(a),fiber(b)))))
    certs=[];hist={}
    for row in prior['representatives']:
        N=row['N']
        if N<18 or N>32:continue
        T=tuple(row['fibers']);R=set(T)
        E=[p for p in outsiders if fiber(p) in R and
           all(a in R or b in R for a,b in req[p])]
        assert len(E)==N,(T,N,len(E))
        fixed={p for p in B if fiber(p) not in R}
        edges=[(i,j,third(E[i],E[j])) for i,j in itertools.combinations(range(N),2)
               if third(E[i],E[j]) in fixed]
        deg=[0]*N
        for i,j,_ in edges:deg[i]+=1;deg[j]+=1
        best=[]
        for mode in range(5):
            if mode==0:ordered=sorted(edges,key=lambda e:-(deg[e[0]]+deg[e[1]]))
            elif mode==1:ordered=sorted(edges,key=lambda e:deg[e[0]]+deg[e[1]])
            elif mode==2:ordered=sorted(edges,key=lambda e:-deg[e[0]])
            elif mode==3:ordered=sorted(edges,key=lambda e:deg[e[0]])
            else:ordered=sorted(edges,key=lambda e:e[0]+e[1])
            used=set();matching=[]
            for i,j,z in ordered:
                if i not in used and j not in used:
                    matching.append((i,j,z));used.update((i,j))
            if len(matching)>len(best):best=matching
        if len(best)<N-16:continue
        orbit={image(T,g) for g in G}
        assert len(orbit)==row['orbit_size']
        certs.append({'fibers':list(T),'N':N,'orbit_size':len(orbit),
                      'matching':[[enc(E[i]),enc(E[j]),enc(z)] for i,j,z in best[:N-16]]})
        hist[str(N)]=hist.get(str(N),0)+1
    n=sum(r['orbit_size'] for r in certs)
    assert len(certs)==500 and n==7440,(len(certs),n)
    return {'scope':'fixed 236 cap; exactly seven first-three-coordinate 4D fibers',
            'previous_excluded':863482,'new_excluded':n,'total_excluded':863482+n,
            'remaining_neighborhoods':888030-863482-n,'new_orbits':len(certs),
            'remaining_orbits':1628-len(certs),'N_range':[18,32],
            'N_orbit_histogram':hist,'seed':None,'gpu':False,'certificates':certs}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('prior',type=Path)
    p.add_argument('--cap',type=Path,default=HERE/'candidates'/'calderbank_fishburn_236.txt')
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    data=generate(a.prior,a.cap)
    a.out.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in data.items() if k!='certificates'},sort_keys=True))
