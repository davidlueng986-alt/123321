#!/usr/bin/env python3
"""Global cap-set CNF, without assuming a particular 236-point baseline.
Proof-producing SAT solver is NOT included; generating CNF is NOT an UNSAT proof.
Optional affine-basis normalization is sound for n=7, target>r3(6)=112.
"""
from itertools import combinations
import argparse,json

def digits(i,n):
    a=[0]*n
    for j in range(n-1,-1,-1):
        a[j]=i%3;i//=3
    return tuple(a)

def pack(p):
    q=0
    for x in p:q=3*q+x
    return q

def third(p,q):return tuple((-a-b)%3 for a,b in zip(p,q))

def lines(n):
    N=3**n
    v=[digits(i,n) for i in range(N)]
    for a in range(N):
        for b in range(a+1,N):
            c=pack(third(v[a],v[b]))
            if b<c:yield (a+1,b+1,c+1)

def basis_ids(n):
    return [1]+[pack(tuple(int(i==j) for i in range(n)))+1 for j in range(n)]

def forbidden_basis_ids(n):
    B=[digits(i-1,n) for i in basis_ids(n)]
    return sorted({pack(third(p,q))+1 for p,q in combinations(B,2)})

def aux_id(i,j,N,k):
    assert 1<=j<=min(i,k)
    t=i-1
    before=t*(t+1)//2 if t<=k else k*(k+1)//2+(t-k)*k
    return N+before+j

def clauses(n,k,basis=False):
    N=3**n
    for a,b,c in lines(n):yield (-a,-b,-c)
    if basis:
        for a in basis_ids(n):yield (a,)
        for a in forbidden_basis_ids(n):yield (-a,)
    # s[i,j] implies at least j selected variables among x[1:i].
    # A true s[i,j] requires s[i-1,j] or BOTH x[i] and s[i-1,j-1].
    for i in range(1,N+1):
        for j in range(1,min(i,k)+1):
            s=aux_id(i,j,N,k)
            prev=aux_id(i-1,j,N,k) if j<=min(i-1,k) else None
            prev_low=aux_id(i-1,j-1,N,k) if j>1 else 0
            yield (-s,prev,i) if prev is not None else (-s,i)
            if j>1:
                yield (-s,prev,prev_low) if prev is not None else (-s,prev_low)
    yield (aux_id(N,k,N,k),)

def stats(n,k,basis=False):
    N=3**n
    aux=sum(min(i,k) for i in range(1,N+1))
    counter=sum(2*min(i,k)-1 for i in range(1,N+1))+1
    return {'dimension':n,'target':k,'points':N,'line_clauses':N*(N-1)//6,
            'basis':basis,'fixed_ones':(n+1 if basis else 0),
            'fixed_zeros':(n*(n+1)//2 if basis else 0),
            'variables':N+aux,'aux_variables':aux,
            'clauses':N*(N-1)//6+counter+(n+1+n*(n+1)//2 if basis else 0),
            'scope':'global exact encoding, SAT status unknown'}

def write_cnf(n,k,out,basis=False):
    s=stats(n,k,basis)
    with open(out,'w',encoding='utf-8') as f:
        f.write('c cap-set exact global CNF, SAT status unknown\n')
        f.write('p cnf {} {}\n'.format(s['variables'],s['clauses']))
        num=0
        for c in clauses(n,k,basis):
            f.write(' '.join(map(str,c))+' 0\n')
            num+=1
    assert num==s['clauses']
    return s

def verify_candidate_assignment(n,k,A,basis=False):
    N=3**n
    X={pack(p)+1 for p in A}
    if basis and (not set(basis_ids(n))<=X or set(forbidden_basis_ids(n))&X):
        return False
    truth={i:i in X for i in range(1,N+1)}
    cnt=0
    for i in range(1,N+1):
        cnt+=bool(truth[i])
        for j in range(1,min(i,k)+1):
            truth[aux_id(i,j,N,k)]=cnt>=j
    return all(any(truth[abs(l)]==(l>0) for l in cl) for cl in clauses(n,k,basis))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--n',type=int,default=7)
    p.add_argument('--target',type=int,default=237)
    p.add_argument('--basis',action='store_true')
    p.add_argument('--out')
    a=p.parse_args()
    assert 1<=a.target<=3**a.n
    if a.basis and a.n==7:assert a.target>112
    print(json.dumps(write_cnf(a.n,a.target,a.out,a.basis) if a.out else stats(a.n,a.target,a.basis),sort_keys=True))
