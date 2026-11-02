#!/usr/bin/env python3
"""CAP-005H numerical proposal of two exact-rational duals; NOT the verifier."""
import argparse,itertools,json
from pathlib import Path
from fractions import Fraction
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from verify_capset import read_points,verify
HERE=Path(__file__).resolve().parent
fiber=lambda p:9*p[0]+3*p[1]+p[2]
third=lambda a,b:tuple((-x-y)%3 for x,y in zip(a,b))
REPS=[(1,2,3,4,8,18),(1,2,4,5,7,18)]

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
        constraints=[];rows=[];cols=[]
        for i,a in enumerate(V):
            for j in range(i+1,len(V)):
                b=V[j];z=third(a,b);k=ix.get(z)
                if k is not None:
                    if j<k:ids=(i,j,k);rhs=2
                    else:continue
                elif z in fixed:ids=(i,j);rhs=1
                else:continue
                row=len(constraints);constraints.append((ids,rhs))
                for v in ids:rows.append(row);cols.append(v)
        A=coo_matrix(([1]*len(rows),(rows,cols)),shape=(len(constraints),len(V))).tocsr()
        sol=linprog([-1.0]*len(V),A_ub=A,b_ub=[r for _,r in constraints],bounds=(0,1),method='highs')
        assert sol.status==0
        rational=lambda x:Fraction(float(x)).limit_denominator(1000000)
        y=[rational(-x) for x in sol.ineqlin.marginals]
        z=[rational(-x) for x in sol.upper.marginals]
        assert all(v>=0 for v in y+z)
        objective=sum(y[i]*rhs for i,(_,rhs) in enumerate(constraints))+sum(z)
        baseline=len(B-fixed)
        cover=z[:]
        for i,(ids,_) in enumerate(constraints):
            for j in ids:cover[j]+=y[i]
        assert min(cover)>=1 and objective<baseline+1
        frac=lambda v:[v.numerator,v.denominator]
        certs.append({'fibers':list(group),'baseline_occupancy':baseline,
            'dual_objective':frac(objective),
            'rows':[[[''.join(map(str,V[j])) for j in ids],frac(y[i])]
                    for i,(ids,_) in enumerate(constraints) if y[i]],
            'upper':[[''.join(map(str,V[i])),frac(z[i])] for i in range(len(V)) if z[i]]})
    return {'method':'integer rounding of exact rational duals and affine symmetry',
            'certificates':certs,'additional_eliminated':32,'remaining_unresolved':56}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();d=generate()
    a.out.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
    print([(c['fibers'],c['dual_objective']) for c in d['certificates']])
