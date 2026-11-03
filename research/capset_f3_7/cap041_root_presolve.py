#!/usr/bin/env python3
"""CAP041: sound root-COMPLETE 237-cap dense-H branch CNF presolve.

Fix 9 selected frame points (including one in >=89 H) and their secant-
forced zeros, eliminating all fixed point variables. Globally require
>=228 free points (237 minus 9) and >=81 free H points (89 minus 8).
Every 3AP containing a fixed zero is satisfied; one selected yields
binary negative clause, no selected yields ternary clause; two selected
force the third zero already. This literal substitution is equisatisfiable
with the corresponding CAP040H ten-way branch. SAT/UNSAT UNKNOWN.
"""
import argparse, json, os, shutil, tempfile
from itertools import combinations
from cap040_root_orbits import frame,vec,pack,third
from cap040_hyperplane_anchor import anchored_ninth_branches,at_least_clauses
from cap007_global_exact_model import lines

def counter_stats(n,k):
    aux=sum(min(i,k) for i in range(1,n+1))
    return aux,2*aux-n+1

def configure(branch):
    cases=anchored_ninth_branches()
    if not 0<=branch<len(cases):raise ValueError('branch must be 0..9')
    p=vec(cases[branch]['rep'],7)
    B=frame(7)+[p]
    selected={pack(x)+1 for x in B}
    zero={pack(third(a,b))+1 for a,b in combinations(B,2)}
    assert len(selected)==9 and len(zero) in (35,36) and not(selected&zero)
    free=[i for i in range(1,2188) if i not in selected and i not in zero]
    label={p:i+1 for i,p in enumerate(free)}
    high=[label[i] for i in free if (i-1)%3==0]
    assert len(free) in (2142,2143) and len(high) in (693,694)
    assert len(selected & {i for i in range(1,2188) if (i-1)%3==0})==8
    return cases[branch],selected,zero,free,label,high

def filtered_lines(selected,zero,label):
    for line in lines(7):
        if any(i in zero for i in line):
            yield None
            continue
        live=tuple(-label[i] for i in line if i not in selected)
        assert len(live) in (2,3)
        yield live

def audit(branch=0,out=None):
    case,selected,zero,free,label,H=configure(branch)
    count={'dropped':0,'binary':0,'ternary':0}
    fd=None;tmp=None
    if out:
        fd,tmp=tempfile.mkstemp(prefix='cap041_',suffix='.part',dir=os.path.dirname(os.path.abspath(out)))
        f=os.fdopen(fd,'w',encoding='ascii')
    else:f=None
    try:
        for cl in filtered_lines(selected,zero,label):
            if cl is None:count['dropped']+=1;continue
            count['binary' if len(cl)==2 else 'ternary']+=1
            if f:f.write(' '.join(map(str,cl))+' 0\n')
        assert sum(count.values())==796797
        atotal,ctotal=counter_stats(len(free),228)
        ah,ch=counter_stats(len(H),81)
        total_vars=len(free)+atotal+ah
        total_cls=count['binary']+count['ternary']+ctotal+ch
        summary={'branch':branch,'ninth':''.join(map(str,vec(case['rep'],7))),
                 'selected':9,'forced_zero':len(zero),'free':len(free),
                 'free_H':len(H),'line_counts':count,
                 'allpoint_counter_aux':atotal,'H_counter_aux':ah,
                 'variables':total_vars,'clauses':total_cls,
                 'target_total_selected':237,'target_free_selected':228,
                 'target_H_selected':89,'target_free_H_selected':81,
                 'sat_status':'UNKNOWN','global_bound_improved':False}
        if f:f.close();f=None
        if out:
            with open(out,'w',encoding='ascii') as o,open(tmp,'r',encoding='ascii') as linesfile:
                o.write('c CAP041 root-complete dense-H branch '+str(branch)+'; SAT UNKNOWN\n')
                o.write(f'p cnf {total_vars} {total_cls}\n')
                shutil.copyfileobj(linesfile,o)
                m=count['binary']+count['ternary']
                for cl in at_least_clauses(list(range(1,len(free)+1)),228,len(free)):
                    o.write(' '.join(map(str,cl))+' 0\n');m+=1
                for cl in at_least_clauses(H,81,len(free)+atotal):
                    o.write(' '.join(map(str,cl))+' 0\n');m+=1
                assert m==total_cls
            with open(out+'.mapping.json','w') as j:
                json.dump({'branch':branch,
                           'selected_point_codes_sorted':sorted(x-1 for x in selected),
                           'free_id_to_point_code':[p-1 for p in free],
                           'sat_status':'UNKNOWN'},j,separators=(',',':'))
        return summary
    finally:
        if f:f.close()
        if tmp and os.path.exists(tmp):os.remove(tmp)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--branch',type=int,default=0);p.add_argument('--out')
    a=p.parse_args();print(json.dumps(audit(a.branch,a.out),sort_keys=True))
