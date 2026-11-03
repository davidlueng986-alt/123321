#!/usr/bin/env python3
"""CAP-040H: ROOT-COMPLETE 237-target SAT with dense 6D hyperplane anchoring.

CAP007J proved via exact 2nd/3rd moments that every 237-cap has some
6D hyperplane containing >=89 points. Since r3(5)=45, that intersection
affinely spans its 6-flat. Pick seven points there as an affine basis,
and one cap point outside. Normalize to 0,e1,..,e6 in x7=0, e7 outside.
Thus global target237 existence is EQUIVALENT to SAT of this CNF.
SAT/UNSAT remains UNKNOWN. No solver or external novelty claim.
"""
from __future__ import annotations
from collections import defaultdict
import argparse,json
from cap040_root_orbits import frame,forbidden,pack,vec,barycentric,multinomial

def moment_89_check():
    M=237;D=1093;t=M//3
    S2=364*M*M+729*M
    S3=121*M*(M-1)*(M-2)+1092*M*(M-1)+D*M
    V=S2-2*t*D*M+3*t*t*D
    W=S3-3*t*S2+3*t*t*D*M-3*t*t*t*D
    assert (S2,S3,V,W,W+9*V)==(20618289,1651763205,154050,-1421526,-35076)
    triples=0
    for a in range(89):
        for b in range(a,89):
            c=237-a-b
            if not b<=c<=88:continue
            x,y,z=a-79,b-79,c-79
            assert x+y+z==0
            assert x*x*x+y*y*y+z*z*z+9*(x*x+y*y+z*z)>=0
            triples+=1
    assert triples==75
    return {'affine_hyperplane_at_least':89,'projective_directions':1093,
            'contradiction_global_moment_sum':W+9*V,'local_cases_checked':triples}

def h_anchor_orbits():
    B=frame(7)
    invalid={pack(v) for v in B}|forbidden(B)
    cases=defaultdict(list)
    for i in range(3**7):
        lam=barycentric(vec(i,7))
        tag=(lam[7],)+tuple(lam[:7].count(x) for x in (0,1,2))
        cases[tag].append(i)
    assert len(cases)==36
    omitted=[(tag,ids) for tag,ids in cases.items() if set(ids)&invalid]
    assert len(omitted)==4 and sum(len(ids) for _,ids in omitted)==36
    assert all(set(ids)<=invalid for _,ids in omitted)
    valid=[{'tag':tag,'rep':ids[0],'size':len(ids)}
           for tag,ids in sorted(cases.items()) if not set(ids)&invalid]
    assert len(valid)==32 and sum(x['size'] for x in valid)==2151
    for t in valid:
        assert t['size']==multinomial(t['tag'][1:])
    return valid

def card_aux_id(i,j,offset,k):
    assert 1<=j<=min(i,k)
    z=i-1
    before=z*(z+1)//2 if z<=k else k*(k+1)//2+(z-k)*k
    return offset+before+j

def at_least_clauses(variables,k,offset):
    n=len(variables)
    assert 1<=k<=n
    for i in range(1,n+1):
        for j in range(1,min(i,k)+1):
            s=card_aux_id(i,j,offset,k)
            prev=card_aux_id(i-1,j,offset,k) if j<=min(i-1,k) else None
            low=card_aux_id(i-1,j-1,offset,k) if j>1 else 0
            if prev is not None:yield(-s,prev,variables[i-1])
            else:yield(-s,variables[i-1])
            if j>1:
                if prev is not None:yield(-s,prev,low)
                else:yield(-s,low)
    yield(card_aux_id(n,k,offset,k),)

def stats():
    from cap007_global_exact_model import stats as base_stats
    original=base_stats(7,237,basis=True)
    n=729;k=89
    aux=sum(min(i,k) for i in range(1,n+1))
    clauses=sum(2*min(i,k)-1 for i in range(1,n+1))+1
    assert (aux,clauses)==(60965,121202)
    return {'primary_variables':2187,'total_variables':original['variables']+aux,
            'total_clauses':original['clauses']+clauses,
            'anchor_6flat_size':729,'minimum_in_anchor':89,
            'counter_aux_variables':aux,'additional_clauses':clauses,
            'base_variables':original['variables']}

def anchored_ninth_branches():
    # The >=89-point H already contains seven chosen basis vertices.
    # Thus every >=237 cap supplies a ninth point INSIDE H, allowing
    # the H-preserving S7 stabilizer instead of the unrestricted S8.
    cases=[q for q in h_anchor_orbits() if q['tag'][0]==0]
    assert len(cases)==10 and sum(q['size'] for q in cases)==701
    return cases

def extra_ninth_units(case):
    from cap040_root_orbits import third
    p=vec(case['rep'],7)
    assert p[-1]==0
    base=frame(7)
    both=base+[p]
    old={pack(third(x,y))+1 for x,y in __import__('itertools').combinations(base,2)}
    new={pack(third(x,y))+1 for x,y in __import__('itertools').combinations(both,2)}
    assert not (new & {pack(x)+1 for x in both})
    assert len(new) in (35,36)
    return [(pack(p)+1,)]+[(-i,) for i in sorted(new-old)]

def write_cnf(path,branch=None):
    from cap007_global_exact_model import clauses as base_clauses
    d=stats().copy()
    extra=[] if branch is None else extra_ninth_units(anchored_ninth_branches()[branch])
    d['total_clauses']+=len(extra)
    d['ninth_extra_unit_clauses']=len(extra)
    H=[i+1 for i in range(2187) if i%3==0]
    assert len(H)==729
    with open(path,'w',encoding='ascii') as f:
        f.write('c CAP040H globally complete target237, moment-anchored hyperplane>=89'+(' branch='+str(branch) if branch is not None else '')+'\n')
        f.write(f"p cnf {d['total_variables']} {d['total_clauses']}\n")
        count=0
        for cl in base_clauses(7,237,basis=True):
            f.write(' '.join(map(str,cl))+' 0\n');count+=1
        for cl in at_least_clauses(H,89,d['base_variables']):
            f.write(' '.join(map(str,cl))+' 0\n');count+=1
        for cl in extra:
            f.write(' '.join(map(str,cl))+' 0\n');count+=1
        assert count==d['total_clauses']
    return d

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cnf');p.add_argument('--branch',type=int)
    args=p.parse_args()
    if args.branch is not None and not 0<=args.branch<10:p.error('--branch must be 0..9')
    o={'moment_proof':moment_89_check(),'normalized_9th_orbits':len(h_anchor_orbits()),
       'dense_hyperplane_ninth_orbits':len(anchored_ninth_branches()),
       'dense_hyperplane_ninth_candidate_points':701,
       'coverage':2151,'cnf_stats':stats(),'sat_status':'UNKNOWN',
       'global_bound_improved':False}
    if args.cnf:o['generated']=write_cnf(args.cnf,args.branch)
    print(json.dumps(o,sort_keys=True))
