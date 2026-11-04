#!/usr/bin/env python3
"""Direct 5-coordinate OA( n^2,5,n,2 ) CNF encoding.

This model has ALL three Latin squares free. Clauses are exact under witness
semantics. Built-in normalization fixes A/B/C first rows to identity and
A first column to identity. No B-vs-C first-column comparison is imposed;
branch symmetry reduction is supplied by E064 externally.

SAT -> independently validate complete triples.  UNSAT -> only the full model
or a separately assumed specific E064 branch; NEVER confuse UNKNOWN and UNSAT.
"""
import argparse, hashlib, json
from pathlib import Path

PAIRS=((0,1),(0,2),(1,2))

def x(s,r,c,v,n): return 1+(((s*n+r)*n+c)*n+v)
def y(p,r,c,a,b,n): return 3*n**3+1+(((((p*n+r)*n+c)*n+a)*n+b))

def build(n, file):
    nvars=3*n**3+3*n**4
    clause_count=0
    unit_count=0
    with open(file, 'w') as out:
        out.write('c E065 FULL FIVE-COORDINATE exact OA CNF; first-row/first-column normalization ONLY\n')
        out.write('p cnf '+str(nvars)+' '+' ' * 12+'\n')
        def add(cl):
            nonlocal clause_count,unit_count
            clause_count+=1
            if len(cl)==1:unit_count+=1
            out.write(' '.join(map(str,cl))+' 0\n')
        def one(vs):
            add(vs)
            for i in range(len(vs)):
                for j in range(i+1,len(vs)):
                    add([-vs[i],-vs[j]])
        for s in range(3):
            for r in range(n):
                for c in range(n):one([x(s,r,c,v,n) for v in range(n)])
            for r in range(n):
                for v in range(n):one([x(s,r,c,v,n) for c in range(n)])
            for c in range(n):
                for v in range(n):one([x(s,r,c,v,n) for r in range(n)])
        for p,(s,t) in enumerate(PAIRS):
            for a in range(n):
                for b in range(n):
                    add([y(p,r,c,a,b,n) for r in range(n) for c in range(n)])
                    for r in range(n):
                        for c in range(n):
                            z=y(p,r,c,a,b,n)
                            add([-z,x(s,r,c,a,n)])
                            add([-z,x(t,r,c,b,n)])
        for s in range(3):
            for c in range(n):add([x(s,0,c,c,n)])
        for r in range(n):add([x(0,r,0,r,n)])
    # Rewrite fixed-width header without changing payload / line count.
    data=Path(file).read_text()
    data=data.replace('p cnf '+str(nvars)+' '+' '*12+'\n',f'p cnf {nvars} {clause_count}\n',1)
    Path(file).write_text(data)
    return {'n':n,'nvars':nvars,'clauses':clause_count,'units':unit_count,
            'sha256':hashlib.sha256(Path(file).read_bytes()).hexdigest(),
            'encoding':'E065-full-OA-normalized-no-B<C'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('n',type=int);ap.add_argument('--output',required=True)
    a=ap.parse_args(); print(json.dumps(build(a.n,a.output)))