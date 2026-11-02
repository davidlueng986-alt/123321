#!/usr/bin/env python3
"""CAP-005M independent checker: no generator imports, exact F3 arithmetic."""
import argparse,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def parse(s):
    assert isinstance(s,str) and len(s)==7 and set(s)<={'0','1','2'}
    return tuple(map(int,s))
def third(a,b):return tuple((-x-y)%3 for x,y in zip(a,b))
def fid(p):return 9*p[0]+3*p[1]+p[2]
def maps():
    def gens(i):
        a,b,c=i//9,(i//3)%3,i%3
        return (((1-a)%3)*9+b*3+c,a*9+((-b)%3)*3+c,
                a*9+b*3+((-c)%3),a*9+c*3+b)
    identity=tuple(range(27));G={identity};pending=[identity]
    while pending:
        g=pending.pop()
        for k in range(4):
            h=tuple(gens(g[i])[k] for i in range(27))
            if h not in G:G.add(h);pending.append(h)
    assert len(G)==16
    return G
def verify(cert_path,prior_path,cap_path):
    lines=cap_path.read_text().splitlines()
    assert lines[0].strip()=='n: 7'
    pts=[parse(s.strip()) for s in lines[1:] if s.strip()]
    B=set(pts);assert len(pts)==len(B)==236
    req={p:set() for p in itertools.product(range(3),repeat=7) if p not in B}
    assert len(req)==1951
    for a,b in itertools.combinations(sorted(B),2):
        z=third(a,b);assert z not in B
        if fid(a)!=fid(b):req[z].add(tuple(sorted((fid(a),fid(b)))))
    prior=json.loads(prior_path.read_text())
    assert prior['group_order']==16 and prior['survivor_orbits']==1665
    assert prior['original_survivors']==25124
    reps={tuple(r['fibers']):r for r in prior['representatives']}
    assert len(reps)==1665
    data=json.loads(cert_path.read_text())
    assert data['new_orbits']>=500 and data['new_excluded']>=7440
    assert data['total_excluded']==863482+data['new_excluded']
    assert data['remaining_neighborhoods']==888030-data['total_excluded']
    assert data['remaining_orbits']==1628-data['new_orbits']
    assert data['previous_excluded']==863482 and data['N_range']==[18,32]
    assert len(data['certificates'])==data['new_orbits']
    G=maps();covered=set();checked=set();hist={}
    for row in data['certificates']:
        T=tuple(row['fibers'])
        assert len(T)==7 and T==tuple(sorted(set(T))) and T in reps and T not in checked
        checked.add(T);R=set(T);N=reps[T]['N']
        assert row['N']==N and 18<=N<=32
        assert row['orbit_size']==reps[T]['orbit_size']
        E={p for p,pairs in req.items() if fid(p) in R and
           all(a in R or b in R for a,b in pairs)}
        assert len(E)==N,(T,len(E),N)
        fixed={p for p in B if fid(p) not in R}
        assert len(row['matching'])==N-16
        used=set()
        for triple in row['matching']:
            assert isinstance(triple,list) and len(triple)==3
            a,b,z=map(parse,triple)
            assert a!=b and a in E and b in E and a not in used and b not in used
            used.update((a,b))
            assert third(a,b)==z and z in fixed
        orbit={tuple(sorted(g[i] for i in T)) for g in G}
        assert len(orbit)==row['orbit_size'] and not orbit.intersection(covered)
        covered.update(orbit);hist[str(N)]=hist.get(str(N),0)+1
    assert len(covered)==data['new_excluded'] and len(checked)==data['new_orbits']
    assert hist==data['N_orbit_histogram']
    assert 862906+576+len(covered)+data['remaining_neighborhoods']==888030
    return {'status':'PASS_INDEPENDENT_EXACT_F3_MATCHING','certificates':len(checked),
            'newly_excluded':len(covered),'total_excluded':data['total_excluded'],
            'unresolved':data['remaining_neighborhoods'],
            'global_bound_improved':False}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('certificate',type=Path)
    p.add_argument('prior',type=Path)
    p.add_argument('--cap',type=Path,default=HERE/'candidates'/'calderbank_fishburn_236.txt')
    a=p.parse_args();print(json.dumps(verify(a.certificate,a.prior,a.cap),sort_keys=True))
