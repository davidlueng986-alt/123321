#!/usr/bin/env python3
"""CAP-040 ROOT-COMPLETE affine-frame + ninth/tenth orbit cover for r3(7).

Every >=237 cap is affine equivalent to one of 13 nine-point-selected
branches. Each ninth branch's tenth-point candidates are classified by the
stabilizer of the ninth point in S8. Generating CNF is NOT an UNSAT proof.
Pure standard-library GF(3) computation; no GPU/paid compute.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import combinations
from math import factorial, prod
import argparse, json

def pack(p):
    a=0
    for x in p:a=3*a+x
    return a

def vec(i,n):
    v=[0]*n
    for j in range(n-1,-1,-1):v[j]=i%3;i//=3
    return tuple(v)

def frame(n):
    return [(0,)*n]+[tuple(int(j==i) for j in range(n)) for i in range(n)]

def third(a,b):
    return tuple((-x-y)%3 for x,y in zip(a,b))

def forbidden(B):
    return {pack(third(x,y)) for x,y in combinations(B,2)}

def barycentric(p):
    return ((1-sum(p))%3,)+tuple(p)

def type_key(p):
    lam=barycentric(p)
    return tuple(lam.count(k) for k in (0,1,2))

def multinomial(counts):
    return factorial(sum(counts))//prod(factorial(z) for z in counts)

def root_orbits(n):
    B=frame(n)
    selected={pack(x) for x in B}
    banned=forbidden(B)
    assert len(selected)==n+1 and len(banned)==n*(n+1)//2
    assert not (selected&banned)
    classes=defaultdict(list)
    for i in range(3**n):
        classes[type_key(vec(i,n))].append(i)
    assert sum(map(len,classes.values()))==3**n
    excluded={k for k,vs in classes.items() if set(vs)&(selected|banned)}
    assert excluded=={(n,1,0),(n-1,0,2)}
    assert set(classes[(n,1,0)])==selected
    assert set(classes[(n-1,0,2)])==banned
    result=[]
    for key,vs in sorted(classes.items()):
        assert len(vs)==multinomial(key)
        if key in excluded:continue
        ninth=vec(vs[0],n)
        selected9=B+[ninth]
        bans9=forbidden(selected9)
        assert len({pack(p) for p in selected9})==n+2
        assert not(bans9&{pack(p) for p in selected9})
        reps=defaultdict(list)
        lam9=barycentric(ninth)
        free=set(range(3**n))-{pack(p) for p in selected9}-bans9
        for code in sorted(free):
            mu=barycentric(vec(code,n))
            matrix=tuple(sum(lam9[i]==a and mu[i]==b for i in range(n+1))
                         for a in range(3) for b in range(3))
            reps[matrix].append(code)
        for contingency,points in reps.items():
            expected=1
            for a in range(3):
                expected*=multinomial(contingency[3*a:3*a+3])
            assert expected==len(points)
        result.append({'type':key,'ninth':''.join(map(str,ninth)),
                       'ninth_orbit_size':len(vs),'fixed_ones':n+2,
                       'forced_zeros':len(bans9),'free_points_after_ninth':len(free),
                       'tenth_orbits':len(reps),
                       'largest_tenth_orbit':max(map(len,reps.values()),default=0),
                       'tenth_representatives':[
                           {'code':pt[0],'size':len(pt),'contingency':list(matrix)}
                           for matrix,pt in sorted(reps.items())]})
    assert sum(x['ninth_orbit_size'] for x in result)==3**n-(n+1)-(n+1)*n//2
    return result

def audit_n7():
    branches=root_orbits(7)
    assert len(branches)==13
    assert [b['ninth_orbit_size'] for b in branches]==[1,56,28,56,280,8,420,168,56,560,280,70,168]
    assert [b['forced_zeros'] for b in branches]==[36]*12+[35]
    assert [b['tenth_orbits'] for b in branches]==[11,62,48,73,138,29,167,114,62,187,138,67,115]
    return {'root_statement': 'r3(7)<=236 iff all 13 canonical target-237 SAT branches are UNSAT (given known 236 witness and sound proof logs)',
            'n':7,'target':237,'affine_frame_size':8,
            'full_affine_span_reason':'237>r3(6)=112',
            'excluded_basis_points':8,'excluded_frame_secants':28,
            'ninth_compatible_points':2151,'ninth_orbit_classes':13,
            'tenth_orbit_classes_total':sum(x['tenth_orbits'] for x in branches),
            'branches':branches,'sat_status':'UNKNOWN','global_bound_improved':False,
            'independent_proof_review_required':True}

def write_cnf(branch,out):
    # Exact global SAT model; no restriction to the known 236-point witness.
    from cap007_global_exact_model import clauses,stats
    base=stats(7,237,basis=True)
    B=frame(7)+[tuple(int(x) for x in branch['ninth'])]
    one={pack(x)+1 for x in B}
    zero={pack(third(x,y))+1 for x,y in combinations(B,2)}
    B8=frame(7)
    oldzero={pack(third(x,y))+1 for x,y in combinations(B8,2)}
    extra=[(pack(B[-1])+1,)]+[(-i,) for i in sorted(zero-oldzero)]
    assert len(one)==9 and len(zero)==branch['forced_zeros'] and len(extra) in (8,9)
    ncls=base['clauses']+len(extra)
    with open(out,'w',encoding='ascii') as f:
        f.write('c CAP040 globally complete canonical ninth type '+str(branch['type'])+'\n')
        f.write(f"p cnf {base['variables']} {ncls}\n")
        count=0
        for cl in clauses(7,237,basis=True):
            f.write(' '.join(map(str,cl))+' 0\n');count+=1
        for cl in extra:
            f.write(' '.join(map(str,cl))+' 0\n');count+=1
    assert count==ncls
    return {'variables':base['variables'],'clauses':ncls,
            'new_unit_clauses':len(extra)}

def main():
    a=argparse.ArgumentParser()
    a.add_argument('--out-json')
    a.add_argument('--branch',type=int)
    a.add_argument('--cnf')
    o=a.parse_args()
    data=audit_n7()
    if o.cnf:
        if o.branch is None or not(0<=o.branch<13):a.error('--cnf requires --branch 0..12')
        data['generated_cnf']=write_cnf(data['branches'][o.branch],o.cnf)
    if o.out_json:
        with open(o.out_json,'w') as f:json.dump(data,f,indent=2)
    else:
        print(json.dumps({k:v for k,v in data.items() if k!='branches'},sort_keys=True))
        for i,b in enumerate(data['branches']):
            print(f"{i:2}: type={b['type']} ninth={b['ninth']} orbit={b['ninth_orbit_size']} "
                  f"forced_zero={b['forced_zeros']} tenth-orbits={b['tenth_orbits']}")
if __name__=='__main__':main()
