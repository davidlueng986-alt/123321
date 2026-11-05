#!/usr/bin/env python3
"""A SINGLE complete 1700-class 3-MOLS(10) CNF, not a relaxation."""
import argparse, json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
MOLS=HERE.parent
sys.path.insert(0,str(MOLS/'e065'))
from E065_cnf import build,x
from E065_verify import from_solver_output,verify
from E065_small_order_symmetry import group_orbits
from E066_campaign import cmd,read_lrat_verified,lrat_structure_ok,digest

def representatives(n):
    if n==10:
        p=MOLS/'e064'/'E064_12_representatives.jsonl'
        entries=[json.loads(t) for t in p.read_text().splitlines() if t.strip()]
        assert len(entries)==1700
        assert len({(tuple(v['B_col0']),tuple(v['C_col0'])) for v in entries})==1700
        return [(v['B_col0'],v['C_col0']) for v in entries],digest(p)
    raw,_,_=group_orbits(n-1)
    return [([0]+[v+1 for v in f],[0]+[v+1 for v in g]) for f,g in raw],None

def global_cnf(n,folder):
    folder.mkdir(parents=True,exist_ok=True)
    base=folder/'base.cnf'; inp=build(n,base)
    reps,rep_sha=representatives(n)
    data=base.read_text().splitlines()
    pos=next(i for i,s in enumerate(data) if s.startswith('p cnf '))
    _,_,oldvar,oldclauses=data[pos].split()
    oldvar=int(oldvar);oldclauses=int(oldclauses)
    assert oldvar==3*n**3+3*n**4
    extra=1+len(reps)*2*(n-1)
    data[pos]=f'p cnf {oldvar+len(reps)} {oldclauses+extra}'
    out=folder/'all_1700_classes.cnf'
    with out.open('w') as f:
        f.write('\n'.join(data)+'\n')
        f.write(' '.join(str(oldvar+i+1) for i in range(len(reps)))+' 0\n')
        for i,(B,C) in enumerate(reps):
            assert len(B)==len(C)==n and B[0]==C[0]==0
            assert sorted(B)==sorted(C)==list(range(n))
            assert all(B[r]!=r and C[r]!=r and B[r]!=C[r] for r in range(1,n))
            selector=oldvar+i+1
            for r in range(1,n):
                f.write(f'-{selector} {x(1,r,0,B[r],n)} 0\n')
                f.write(f'-{selector} {x(2,r,0,C[r],n)} 0\n')
    return out,{'n':n,'classes':len(reps),'vars':oldvar+len(reps),
                'clauses':oldclauses+extra,'base_sha256':inp['sha256'],
                'global_sha256':digest(out),'representatives_sha256':rep_sha}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--n',type=int,default=10)
    p.add_argument('--output',required=True)
    p.add_argument('--cadical',required=True)
    p.add_argument('--lrat-check',required=True)
    p.add_argument('--seconds',type=int,default=120)
    p.add_argument('--proof-seconds',type=int,default=180)
    a=p.parse_args()
    d=Path(a.output).resolve()
    cnf,meta=global_cnf(a.n,d)
    log=d/'global_solver.log';proof=d/'global_solver.lrat'
    rc,elapsed=cmd([a.cadical,'--lrat','--no-factor','--no-binary','-t',str(a.seconds),str(cnf),str(proof)],a.seconds,log,slack=15)
    out={'model':'complete all canonical firstcolumn classes','formula':meta,
         'solver_exit':rc,'seconds':elapsed,'status':'UNKNOWN_BUDGET'}
    if rc==10:
        W=from_solver_output(log.read_text(errors='replace'),a.n)
        v=verify(W,a.n);assert v['overlays']==[a.n*a.n]*3
        path=d/'full_witness.json'
        path.write_text(json.dumps({'squares':W,'check':v},indent=2)+'\n')
        out.update(status='SAT_FULL_WITNESS_INDEPENDENTLY_VERIFIED',witness_sha256=digest(path))
    elif rc==20:
        if not proof.exists() or not proof.stat().st_size:
            out['status']='UNSAT_UNVERIFIED_MISSING_PROOF'
        else:
            try:
                lrat_structure_ok(proof,meta['clauses'])
                checkerlog=d/'lrat_check.log'
                checkrc,checksecs=cmd([a.lrat_check,str(cnf),str(proof)],max(180,a.proof_seconds),checkerlog,slack=20)
                if checkrc==0 and read_lrat_verified(checkerlog):
                    out.update(status='UNSAT_LRAT_VERIFIED',proof_sha256=digest(proof),checker_seconds=checksecs)
                else:out.update(status='UNSAT_UNVERIFIED_CHECKER_REJECTED',checker_exit=checkrc)
            except (ValueError,UnicodeError) as e:out.update(status='UNSAT_UNVERIFIED_STRUCTURE',error=str(e))
    elif rc not in (0,124):
        out.update(status='ERROR_SOLVER',solver_tail=log.read_text(errors='replace')[-800:])
    (d/'E066_GLOBAL_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    if out['status']=='UNKNOWN_BUDGET' and proof.exists():proof.unlink()
    if out['status'].startswith('ERROR'):raise SystemExit(3)
if __name__=='__main__':main()
