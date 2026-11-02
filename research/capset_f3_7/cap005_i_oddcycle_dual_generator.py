#!/usr/bin/env python3
"""CAP-005I: CPU-only LP dual proposal with valid 3-clique/5-cycle cuts.
Floating-point solver output is NEVER proof; use the independent checker."""
import argparse,itertools,json
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from verify_capset import read_points,verify
HERE=Path(__file__).resolve().parent
REPS=[(0,1,2,4,5,18),(0,1,3,4,5,18),(0,1,3,5,8,18),
      (1,2,3,4,8,18),(1,2,4,5,7,18),(1,3,5,7,8,18),(1,4,5,7,8,18)]
fiber=lambda p:9*p[0]+3*p[1]+p[2]
third=lambda a,b:tuple((-x-y)%3 for x,y in zip(a,b))

def generate():
    B=set(read_points(HERE/'candidates'/'calderbank_fishburn_236.txt'))
    assert verify(sorted(B))==236
    sec={x:[] for x in itertools.product(range(3),repeat=7) if x not in B}
    for a,b in itertools.combinations(sorted(B),2):
        x=third(a,b)
        if x in sec:sec[x].append((fiber(a),fiber(b)))
    certs=[]
    for group in REPS:
        T=set(group);fixed={p for p in B if fiber(p) not in T}
        E={x for x,pairs in sec.items() if fiber(x) in T and all(a in T or b in T for a,b in pairs)}
        V=sorted((B-fixed)|E);ix={p:i for i,p in enumerate(V)}
        rows=[];cols=[];constraints=[];adj=[set() for _ in V]
        def add(ids,rhs,typ):
            row=len(constraints);constraints.append((tuple(ids),rhs,typ))
            for i in ids:rows.append(row);cols.append(i)
        for i,a in enumerate(V):
            for j in range(i+1,len(V)):
                b=V[j];z=third(a,b);k=ix.get(z)
                if k is not None:
                    if j<k:add((i,j,k),2,'line')
                elif z in fixed:
                    add((i,j),1,'pair');adj[i].add(j);adj[j].add(i)
        for a in range(len(V)):
            for b in sorted(x for x in adj[a] if x>a):
                for c in sorted(x for x in adj[b] if x>b and x in adj[a]):
                    add((a,b,c),1,'triangle')
        cycles={}
        for a in range(len(V)):
            for b in sorted(x for x in adj[a] if x>a):
                for c in sorted(x for x in adj[b] if x>a and x!=b):
                    for d in sorted(x for x in adj[c] if x>a and x not in (b,c)):
                        for e in sorted(x for x in (adj[d]&adj[a]) if x>a and x not in (b,c,d)):
                            ids=(a,b,c,d,e)
                            if len(set(ids))==5:cycles.setdefault(tuple(sorted(ids)),ids)
        for ids in cycles.values():add(ids,2,'cycle5')
        A=coo_matrix((np.ones(len(rows)),(rows,cols)),shape=(len(constraints),len(V))).tocsr()
        sol=linprog(-np.ones(len(V)),A_ub=A,b_ub=[r for _,r,_ in constraints],bounds=(0,1),method='highs')
        assert sol.status==0,(group,sol.message)
        rational=lambda x:Fraction(float(x)).limit_denominator(1000)
        scale=Fraction(1001,1000)
        y=[rational(-x)*scale for x in sol.ineqlin.marginals]
        z=[rational(-x)*scale for x in sol.upper.marginals]
        assert all(v>=0 for v in y+z)
        objective=sum(y[i]*rhs for i,(_,rhs,_) in enumerate(constraints))+sum(z)
        baseline=len(B-fixed);cover=z[:]
        for i,(ids,_,_) in enumerate(constraints):
            if y[i]:
                for j in ids:cover[j]+=y[i]
        assert min(cover)>=1,(group,'coverage',min(cover))
        assert objective<baseline+1,(group,objective,baseline)
        frac=lambda v:[v.numerator,v.denominator]
        certs.append({'fibers':list(group),'baseline':baseline,'objective':frac(objective),
          'rows':[[typ,[''.join(map(str,V[j])) for j in ids],frac(y[i])]
                  for i,(ids,_,typ) in enumerate(constraints) if y[i]],
          'upper':[[''.join(map(str,V[i])),frac(z[i])] for i in range(len(V)) if z[i]]})
        print('candidate dual',group,'rows',len(certs[-1]['rows']),
              'objective_approx',round(float(objective),6),'baseline',baseline,flush=True)
    return {'scope':'classical 236 cap, exactly six of 27 first-three-coordinate 4D fibers',
      'method':'exact rational duals: pair, line, conflict triangle and five-cycle cuts',
      'certificates':certs,'certified_unresolved_orbits':7,'certified_unresolved_cases':88,
      'restricted_optimum':236,'gpu_used':False,'seed':None}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();d=generate()
    a.out.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
