#!/usr/bin/env python3
"""CAP-005G: exact-rational LP dual certificates for six-fiber edits.
SciPy proposes duals; no solver status is accepted as proof. CPU only.
"""
import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from verify_capset import read_points, verify
from cap005_k6_clique_cover_certificate import eligible_outsiders, dsatur_cover, fiber, third

HERE = Path(__file__).resolve().parent

def problem(B, group, candidates):
    released = set(group)
    fixed = set(B) - {p for p in B if fiber(p) in released}
    variables = sorted([p for p in B if fiber(p) in released] + candidates)
    assert len(variables) == len(set(variables))
    ix = {p:i for i,p in enumerate(variables)}
    constraints = []
    for i,a in enumerate(variables):
        for j in range(i+1,len(variables)):
            b=variables[j]
            z=third(a,b)
            k=ix.get(z)
            if k is not None:
                if j < k:
                    constraints.append(((i,j,k),2))
            elif z in fixed:
                constraints.append(((i,j),1))
    rows=[];cols=[]
    for row,(ids,rhs) in enumerate(constraints):
        for i in ids: rows.append(row);cols.append(i)
    A=coo_matrix(([1]*len(rows),(rows,cols)),shape=(len(constraints),len(variables))).tocsr()
    return variables,constraints,A

def rational(x):
    f=Fraction(float(x)).limit_denominator(1000000)
    assert abs(float(f)-float(x))<1e-7
    return [f.numerator,f.denominator]

def generate():
    B=read_points(HERE/'candidates'/'calderbank_fishburn_236.txt')
    assert verify(B)==236
    by=eligible_outsiders(B)
    certs=[];unresolved=[];eligible_ge17=0;greedy_covered=0
    for group in itertools.combinations(range(27),6):
        mask=sum(1<<j for j in group)
        candidates=[x for f in group for x,req in by[f] if all(mask&e for e in req)]
        if len(candidates)<17:continue
        eligible_ge17+=1
        if len(dsatur_cover(candidates,set(group),set(B)))<=16:
            greedy_covered+=1
            continue
        variables,constraints,A=problem(B,group,candidates)
        rhs=[b for _,b in constraints]
        sol=linprog([-1.0]*len(variables),A_ub=A,b_ub=rhs,bounds=(0,1),method='highs')
        if sol.status!=0:raise RuntimeError(f'LP solver failed {group}: {sol.message}')
        baseline=sum(fiber(p) in group for p in B)
        if -sol.fun>baseline+1e-7:
            unresolved.append(list(group))
            continue
        y=[Fraction(*rational(-a)) for a in sol.ineqlin.marginals]
        z=[Fraction(*rational(-a)) for a in sol.upper.marginals]
        assert all(a>=0 for a in y+z)
        assert sum(y[i]*rhs[i] for i in range(len(y)))+sum(z)<=baseline
        cover=z[:]
        for i,(ids,_) in enumerate(constraints):
            if y[i]:
                for j in ids:cover[j]+=y[i]
        assert min(cover)>=1
        certs.append({'fibers':list(group),
            'rows':[[[''.join(map(str,variables[j])) for j in ids],list(rational(y[i]))]
                    for i,(ids,_) in enumerate(constraints) if y[i]],
            'upper':[[''.join(map(str,variables[i])),list(rational(a))]
                     for i,a in enumerate(z) if a]})
    assert (eligible_ge17,greedy_covered,len(certs),len(unresolved))==(1616,680,848,88)
    return {'scope':'classical 236 cap; six first-three-coordinate fibers only',
            'method':'independently checkable exact rational dual to all 0/1 line inequalities',
            'previous_excluded':295074,'additional_certificates':len(certs),
            'total_excluded':295074+len(certs),'unresolved':len(unresolved),
            'unresolved_groups':unresolved,'seed':None,'gpu':False,'certificates':certs}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    d=generate();args.out.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in d.items() if k not in ('certificates','unresolved_groups')},sort_keys=True))
