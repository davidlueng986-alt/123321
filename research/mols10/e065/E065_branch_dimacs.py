#!/usr/bin/env python3
"""Add mathematically sound fixed-first-column units to E065's full-OA DIMACS.
One branch is one E064 paratopy-class representative. The generator changes
no other clauses. Use this to obtain an independently checkable CNF+LRAT proof
from a proof-producing standalone CDCL solver (e.g., CaDiCaL).
"""
import argparse,hashlib,json
from pathlib import Path
from E065_cnf import x

def branch(base,n,reps,index,dest):
    source=Path(base).read_text()
    lines=source.splitlines()
    ix=next(i for i,line in enumerate(lines) if line.startswith('p cnf'))
    _,_,nvars,orig=lines[ix].split()
    original=[i for i,line in enumerate(lines) if line and line[0] not in 'cp']
    if len(original)!=int(orig):raise ValueError('original clause count mismatch')
    R=[json.loads(t) for t in Path(reps).read_text().splitlines() if t.strip()]
    if index<0 or index>=len(R):raise ValueError('invalid representative index')
    b=R[index]['B_col0'];c=R[index]['C_col0']
    if not (len(b)==n and len(c)==n and b[0]==c[0]==0):raise ValueError('invalid B/C col0')
    if not (sorted(b)==list(range(n)) and sorted(c)==list(range(n))):raise ValueError('not permutations')
    if any(r in (b[r],c[r]) or b[r]==c[r] for r in range(1,n)):raise ValueError('duplicate firstcol pairs')
    units=[x(s,r,0,arr[r],n) for s,arr in ((1,b),(2,c)) for r in range(1,n)]
    lines[ix]='p cnf '+nvars+' '+str(int(orig)+len(units))
    Path(dest).write_text('\n'.join(lines)+'\n'+'\n'.join(str(v)+' 0' for v in units)+'\n')
    return {'n':n,'branch':index,'units':len(units),'nvars':int(nvars),
            'clauses':int(orig)+len(units),'sha256':hashlib.sha256(Path(dest).read_bytes()).hexdigest(),
            'B_col0':b,'C_col0':c}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True);ap.add_argument('--n',type=int,required=True)
    ap.add_argument('--reps',required=True);ap.add_argument('--branch',type=int,required=True);ap.add_argument('--output',required=True)
    a=ap.parse_args();print(json.dumps(branch(a.base,a.n,a.reps,a.branch,a.output)))