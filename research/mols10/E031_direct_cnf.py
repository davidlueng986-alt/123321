#!/usr/bin/env python3
"""E031 exact CNF encoding of 3-MOLS(n)=OA(n^2,5,n,2), no fixed Latin square.
Variables x(s,r,c,v), y(p,r,c,a,b) for p in ((0,1),(0,2),(1,2)).
One-hot x cell/row/column; y => both x values; for each pair p,a,b,
OR_{r,c} y[p,r,c,a,b]. Necessity/sufficiency: n^2 cells and n^2
ordered pairs force a bijection; reverse implication y<=>x&x is unnecessary.
Symmetry (all sound): independently relabel symbols to make all first rows
identity; permute rows to make first column of A identity; swap B,C
so B[1][0]<C[1][0] (their values cannot agree outside first row).
"""
import argparse,json,hashlib
from pathlib import Path
PAIRS=((0,1),(0,2),(1,2))

def make(n, symmetry=True):
    nx=3*n**3
    def x(s,r,c,v):return 1+(((s*n+r)*n+c)*n+v)
    def y(p,r,c,a,b):return nx+1+(((((p*n+r)*n+c)*n+a)*n+b))
    clauses=[]
    def exactly_one(xs):
        clauses.append(xs)
        for i in range(len(xs)):
            for j in range(i+1,len(xs)):
                clauses.append([-xs[i],-xs[j]])
    for s in range(3):
        for r in range(n):
            for c in range(n): exactly_one([x(s,r,c,v) for v in range(n)])
        for r in range(n):
            for v in range(n): exactly_one([x(s,r,c,v) for c in range(n)])
        for c in range(n):
            for v in range(n): exactly_one([x(s,r,c,v) for r in range(n)])
    for p,(s,t) in enumerate(PAIRS):
        for a in range(n):
            for b in range(n):
                clauses.append([y(p,r,c,a,b) for r in range(n) for c in range(n)])
                for r in range(n):
                    for c in range(n):
                        z=y(p,r,c,a,b)
                        clauses.append([-z,x(s,r,c,a)])
                        clauses.append([-z,x(t,r,c,b)])
    if symmetry:
        for s in range(3):
            for c in range(n): clauses.append([x(s,0,c,c)])
        for r in range(n):clauses.append([x(0,r,0,r)])
        for b in range(n):
            for c in range(b+1):
                clauses.append([-x(1,1,0,b),-x(2,1,0,c)])
    return {'n':n,'vars':nx+3*n**4,'clauses':clauses,'x':x,'y':y,'symmetry':symmetry}

def from_squares(M,S):
    """Evaluate CNF under a Latin triple; canonical y are true iff actual pair at cell."""
    n=M['n'];assignment=set()
    for s in range(3):
        for r in range(n):
            for c in range(n):assignment.add(M['x'](s,r,c,S[s][r][c]))
    for p,(s,t) in enumerate(PAIRS):
        for r in range(n):
            for c in range(n):assignment.add(M['y'](p,r,c,S[s][r][c],S[t][r][c]))
    return [i for i,cl in enumerate(M['clauses']) if not any((z>0 and z in assignment) or (z<0 and -z not in assignment) for z in cl)]

def normalize(S):
    n=len(S[0]);Z=[]
    for A in S:
        ren={A[0][c]:c for c in range(n)}
        Z.append([[ren[A[r][c]] for c in range(n)] for r in range(n)])
    positions={Z[0][r][0]:r for r in range(n)}
    Z=[ [A[positions[r]][:] for r in range(n)] for A in Z ]
    if Z[1][1][0]>Z[2][1][0]:Z[1],Z[2]=Z[2],Z[1]
    return Z

def dimacs(M,path):
    with open(path,'w') as out:
        out.write('c E031 exact 3-MOLS direct OA encoding. Symmetries explained in source.\n')
        out.write(f'p cnf {M["vars"]} {len(M["clauses"])}\n')
        for c in M['clauses']:out.write(' '.join(map(str,c))+' 0\n')
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('n',type=int);p.add_argument('--output',type=str)
    a=p.parse_args();M=make(a.n)
    res={'n':a.n,'vars':M['vars'],'clauses':len(M['clauses']),
      'literals':sum(map(len,M['clauses'])),'symmetry':M['symmetry']}
    if a.output:res['sha256']=dimacs(M,a.output)
    print(json.dumps(res))
