#!/usr/bin/env python3
"""CAP-005M: deterministic seven-fiber outsider pair matching certificates."""
import argparse,itertools,json
from pathlib import Path
from cap005_k6_symmetry_quotient import read_cap,generate_group,image,fiber
HERE=Path(__file__).resolve().parent
def third(a,b): return tuple((-x-y)%3 for x,y in zip(a,b))
def enc(p): return ''.join(map(str,p))
def maximum_matching(n,edges):
    """Exact cardinality matching in a general undirected graph (Edmonds blossom).
    Output is a witness only; independent checker re-verifies each chosen edge.
    """
    adj=[[] for _ in range(n)]
    for i,j,_ in edges:
        adj[i].append(j);adj[j].append(i)
    for neighbors in adj:neighbors.sort()
    mate=[-1]*n
    def augment(root):
        base=list(range(n));parent=[-1]*n;used=[False]*n
        used[root]=True;queue=[root]
        def lca(a,b):
            seen=[False]*n
            while True:
                a=base[a];seen[a]=True
                if mate[a]==-1:break
                a=parent[mate[a]]
            while True:
                b=base[b]
                if seen[b]:return b
                b=parent[mate[b]]
        def mark(v,b,child,blossom):
            while base[v]!=b:
                blossom[base[v]]=True
                blossom[base[mate[v]]]=True
                parent[v]=child
                child=mate[v]
                v=parent[mate[v]]
        for v in queue:
            for u in adj[v]:
                if base[v]==base[u] or mate[v]==u:continue
                if u==root or (mate[u]!=-1 and parent[mate[u]]!=-1):
                    b=lca(v,u);blossom=[False]*n
                    mark(v,b,u,blossom);mark(u,b,v,blossom)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i]=b
                            if not used[i]:
                                used[i]=True;queue.append(i)
                elif parent[u]==-1:
                    parent[u]=v
                    if mate[u]==-1:
                        cur=u
                        while cur!=-1:
                            pv=parent[cur]
                            nxt=mate[pv] if pv!=-1 else -1
                            mate[cur]=pv
                            if pv!=-1:mate[pv]=cur
                            cur=nxt
                        return True
                    used[mate[u]]=True
                    queue.append(mate[u])
        return False
    for i in range(n):
        if mate[i]==-1:augment(i)
    return [(i,mate[i]) for i in range(n) if mate[i]>i]

def generate(prior_path,cap_path):
    B=read_cap(cap_path); G=generate_group(B)
    prior=json.loads(prior_path.read_text())
    assert prior['survivor_orbits']==1665 and prior['original_survivors']==25124
    outsiders=sorted(set(itertools.product(range(3),repeat=7))-B)
    req={p:set() for p in outsiders}
    for a,b in itertools.combinations(sorted(B),2):
        z=third(a,b)
        if fiber(a)!=fiber(b):req[z].add(tuple(sorted((fiber(a),fiber(b)))))
    certs=[];hist={}
    for row in prior['representatives']:
        N=row['N']
        if N<18 or N>32:continue
        T=tuple(row['fibers']);R=set(T)
        E=[p for p in outsiders if fiber(p) in R and
           all(a in R or b in R for a,b in req[p])]
        assert len(E)==N,(T,N,len(E))
        fixed={p for p in B if fiber(p) not in R}
        edges=[(i,j,third(E[i],E[j])) for i,j in itertools.combinations(range(N),2)
               if third(E[i],E[j]) in fixed]
        matching=maximum_matching(N,edges)
        if len(matching)<N-16:continue
        orbit={image(T,g) for g in G}
        assert len(orbit)==row['orbit_size']
        certs.append({'fibers':list(T),'N':N,'orbit_size':len(orbit),
                      'matching':[[enc(E[i]),enc(E[j]),enc(third(E[i],E[j]))] for i,j in matching[:N-16]]})
        hist[str(N)]=hist.get(str(N),0)+1
    n=sum(r['orbit_size'] for r in certs)
    assert len(certs)>=500 and n>=7440,(len(certs),n)
    return {'scope':'fixed 236 cap; exactly seven first-three-coordinate 4D fibers',
            'previous_excluded':863482,'new_excluded':n,'total_excluded':863482+n,
            'remaining_neighborhoods':888030-863482-n,'new_orbits':len(certs),
            'remaining_orbits':1628-len(certs),'N_range':[18,32],
            'N_orbit_histogram':hist,'seed':None,'gpu':False,'certificates':certs}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('prior',type=Path)
    p.add_argument('--cap',type=Path,default=HERE/'candidates'/'calderbank_fishburn_236.txt')
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    data=generate(a.prior,a.cap)
    a.out.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in data.items() if k!='certificates'},sort_keys=True))
