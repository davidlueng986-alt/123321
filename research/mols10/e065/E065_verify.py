#!/usr/bin/env python3
"""Independent SAT checker against complete 3-MOLS(n) constraints.
Accepts E065 Z3 JSON, or SAT-solver competition 'v <literals> 0' output.
An UNSAT message is NEVER an independently checked proof; use LRAT checker.
"""
import argparse,json,re
from pathlib import Path
from E065_cnf import x

def verify(S,n):
    if len(S)!=3 or any(len(M)!=n for M in S):raise ValueError('not 3 complete squares')
    expected=list(range(n))
    for M in S:
        for row in M:
            if sorted(row)!=expected:raise ValueError('non Latin row')
        for c in range(n):
            if sorted(M[r][c] for r in range(n))!=expected:raise ValueError('non Latin col')
    overlays=[]
    for a,b in ((0,1),(0,2),(1,2)):
        z={(S[a][r][c],S[b][r][c]) for r in range(n) for c in range(n)}
        if len(z)!=n*n:raise ValueError(f'overlay {a}/{b}: {len(z)}/{n*n}')
        overlays.append(len(z))
    return {'status':'SAT_WITNESS_INDEPENDENTLY_VERIFIED','order':n,'overlays':overlays}

def from_solver_output(text,n):
    if 's SATISFIABLE' not in text:raise ValueError('not confirmed SAT')
    lits=[]
    for line in text.splitlines():
        if line.lstrip().startswith('v '):
            lits.extend(int(w) for w in line.split()[1:] if int(w)!=0)
    chosen=set(lit for lit in lits if lit>0)
    if not chosen:raise ValueError('missing SAT model literals')
    W=[[[None]*n for r in range(n)] for s in range(3)]
    for s in range(3):
        for r in range(n):
            for c in range(n):
                vals=[v for v in range(n) if x(s,r,c,v,n) in chosen]
                if len(vals)!=1:raise ValueError('missing/duplicate onehot model')
                W[s][r][c]=vals[0]
    return W

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,required=True);ap.add_argument('--json')
    ap.add_argument('--sat-output');ap.add_argument('--output');a=ap.parse_args()
    if bool(a.json)==bool(a.sat_output):raise ValueError('specify exactly one source')
    if a.json:
        z=json.loads(Path(a.json).read_text());W=z['witness']
        if z['status']!='SAT':raise ValueError('not SAT')
    else:W=from_solver_output(Path(a.sat_output).read_text(),a.n)
    checked=verify(W,a.n)
    result={'check':checked,'squares':W}
    if a.output:Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(checked))