#!/usr/bin/env python3
"""Enumerate and validate 1700 distinct complete first-column branches.
The digests are of the EXACT branch DIMACS, not just the B/C permutations.
This does NOT claim any branch solved.
"""
import hashlib,json,sys
from pathlib import Path
THIS=Path(__file__).resolve().parent
sys.path.insert(0,str(THIS))
from E066_campaign import E065,REPS,COUNT,reps,digest
sys.path.insert(0,str(E065))
from E065_cnf import build as make_cnf,x
from E065_branch_dimacs import branch as make_branch

def main():
    R=reps();dest=THIS/'E066_1700_BRANCH_INVENTORY.jsonl';base=THIS/'E066_n10_base.cnf'
    info=make_cnf(10,base)
    # Generic branch file writer preserves header plus exact 18 positive B/C first column units.
    template=base.read_bytes()
    assert template.endswith(b'\n')
    old=f'p cnf {info["nvars"]} {info["clauses"]}\n'.encode()
    new=f'p cnf {info["nvars"]} {info["clauses"]+18}\n'.encode()
    assert template.count(old)==1
    header=template.replace(old,new,1)
    types={}; out=[]
    for i,t in enumerate(R):
        bb=t['B_col0'];cc=t['C_col0']
        units=[x(s,r,0,arr[r],10) for s,arr in ((1,bb),(2,cc)) for r in range(1,10)]
        assert len(units)==18 and len(set(units))==18
        suffix=('\n'.join(str(v)+' 0' for v in units)+'\n').encode()
        h=hashlib.sha256();h.update(header);h.update(suffix)
        typ='.'.join(str(z) for z in t['type'])
        types[typ]=types.get(typ,0)+1
        out.append({'branch':i,'ordered_orbit_id':t['ordered_orbit_id'],
                    'B_col0':bb,'C_col0':cc,'type':t['type'],
                    'branch_cnf_sha256':h.hexdigest(),'clauses':info['clauses']+18,
                    'nvars':info['nvars'],'status':'NOT_SOLVED'})
    with dest.open('w') as f:
        for a in out:f.write(json.dumps(a,separators=(',',':'))+'\n')
    # Independently reconstruct 3 file digests through actual E065 branch writer.
    for i in (0,849,1699):
        f=THIS/f'_E066_audit_{i}.cnf'
        m=make_branch(base,10,REPS,i,f)
        assert m['sha256']==out[i]['branch_cnf_sha256'],i
        assert digest(f)==m['sha256']
        f.unlink()
    summary={'status':'INVENTORY_ONLY_NO_ORDER10_UNSAT_PROVED','branches':len(out),
             'inventory_sha256':digest(dest),'base_sha256':digest(base),
             'types':types,'nvars':info['nvars'],'branch_clauses':info['clauses']+18,
             'normalization':'E064 complete first-column paratopy coverage',
             'positive_controls':'E065 n4/5 SAT and n6 3/3 UNSAT, not reproduced by this inventory',
             'actual_order10_proofs':0}
    (THIS/'E066_INVENTORY_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    base.unlink()
if __name__=='__main__':main()
