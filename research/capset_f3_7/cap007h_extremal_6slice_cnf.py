#!/usr/bin/env python3
"""CAP-007H: conditional n7 cap CNF with ONE known 112-cap 6D slice fixed.
If all 112-caps in F3^6 are affinely equivalent (Potechin 2008), this
models all n7 caps that contain *some* maximal 112-point hyperplane.
It does NOT model arbitrary n7 caps lacking that hyperplane.
SAT and UNSAT status remain UNKNOWN.
"""
from itertools import product,combinations
import argparse,json
from cap007_global_exact_model import digits,pack,third
from cap006b_partition_pilot import baseline

def fixed_slice():
    X={p[1:] for p in baseline() if p[0]==0}
    assert len(X)==112
    assert all(third(a,b) not in X for a,b in combinations(sorted(X),2))
    return X

def lines6():
    V=[digits(i,6) for i in range(729)]
    for a in range(729):
        for b in range(a+1,729):
            c=pack(third(V[a],V[b]))
            if b<c:yield a,b,c

def aux_id(i,j,N,k):
    t=i-1
    return N+(t*(t+1)//2 if t<=k else k*(k+1)//2+(t-k)*k)+j

def stats(target=237):
    k=target-112;N=1458
    assert 1<=k<=N
    aux=sum(min(i,k) for i in range(1,N+1))
    nlines=2*729*728//6
    edges=112*729
    return {'total_target':target,'fixed_6d_cap':112,
            'variable_points_in_two_other_slices':N,
            'target_in_two_other_slices':k,
            'within_6d_line_clauses':nlines,
            'cross_fixed_slice_pair_clauses':edges,
            'auxiliary_counter_variables':aux,
            'total_variables':N+aux,
            'total_clauses':nlines+edges+2*aux-N+1,
            'scope':'all caps with this 112-point 6D section, not global',
            'SAT_UNSAT':'UNKNOWN'}

def clauses(target=237):
    X=fixed_slice();N=1458;k=target-112
    for a,b,c in lines6():
        yield (-a-1,-b-1,-c-1)
        yield (-a-730,-b-730,-c-730)
    for c in sorted(X):
        for a in product(range(3),repeat=6):
            b=third(c,a)
            yield (-pack(a)-1,-pack(b)-730)
    for i in range(1,N+1):
        for j in range(1,min(i,k)+1):
            s=aux_id(i,j,N,k)
            p=aux_id(i-1,j,N,k) if j<=min(i-1,k) else None
            q=aux_id(i-1,j-1,N,k) if j>1 else 0
            yield (-s,p,i) if p is not None else (-s,i)
            if j>1:
                yield (-s,p,q) if p is not None else (-s,q)
    yield (aux_id(N,k,N,k),)

def check_witness(A,target=236):
    """Independent direct evaluation of every CNF clause on a known cap."""
    k=target-112;N=1458
    if {p[1:] for p in A if p[0]==0}!=fixed_slice():return False
    S={pack(p[1:])+1 if p[0]==1 else pack(p[1:])+730
       for p in A if p[0]!=0}
    truth={i:(i in S) for i in range(1,N+1)}
    count=0
    for i in range(1,N+1):
        count+=int(truth[i])
        for j in range(1,min(i,k)+1):
            truth[aux_id(i,j,N,k)]=count>=j
    return all(any(truth[abs(l)]==(l>0) for l in cl) for cl in clauses(target))

def write(target,out):
    r=stats(target);num=0
    with open(out,'w',encoding='utf-8') as f:
        f.write('c Conditional n7 anchored 112-slice model; no SAT/UNSAT conclusion\n')
        f.write('p cnf {} {}\n'.format(r['total_variables'],r['total_clauses']))
        for c in clauses(target):
            f.write(' '.join(map(str,c))+' 0\n');num+=1
    assert num==r['total_clauses']
    return r

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--target',type=int,default=237)
    p.add_argument('--out');a=p.parse_args()
    print(json.dumps(write(a.target,a.out) if a.out else stats(a.target),sort_keys=True))
