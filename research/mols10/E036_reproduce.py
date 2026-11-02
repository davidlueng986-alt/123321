#!/usr/bin/env python3
"""E036 reproducible constructive certificate for f=(01)(23)(45)(67)(89).
Enumerates all C(f)-orbits of legal g and constructs six-row partial 3-MOLS.
Full order-10 3-MOLS existence/nonexistence remains OPEN.
"""
import json,random,hashlib
N=10; f=tuple(i^1 for i in range(N)); I=list(range(N))
def generators():
    out=[]
    for k in range(5):
        p=I[:];p[2*k],p[2*k+1]=p[2*k+1],p[2*k];out.append(p)
    for k in range(4):
        p=I[:];a,b=2*k,2*k+2
        p[a],p[b]=p[b],p[a];p[a+1],p[b+1]=p[b+1],p[a+1];out.append(p)
    return out
G=generators()
def legal_g():
    a=[0]*N
    def rec(i,mask):
        if i==N:yield tuple(a);return
        for x in range(N):
            if x!=i and x!=f[i] and not(mask>>x&1):
                a[i]=x;yield from rec(i+1,mask|1<<x)
    yield from rec(0,0)
def conj(g,p):
    inv=[0]*N
    for i,v in enumerate(p):inv[v]=i
    return tuple(inv[g[p[i]]] for i in range(N))
def representatives():
    seen=set();out=[];total=0
    for g in legal_g():
        total+=1
        if g in seen:continue
        out.append(g);q=[g];seen.add(g)
        for x in q:
            for p in G:
                z=conj(x,p)
                if z not in seen:seen.add(z);q.append(z)
    assert total==len(seen)==440192 and len(out)==156
    return out
def h_matching(g):
    adj=[[x for x in I if x not in (c,f[c],g[c])] for c in I]
    m=[-1]*N
    def aug(c,seen):
        for v in adj[c]:
            if v in seen:continue
            seen.add(v)
            if m[v]<0 or aug(m[v],seen):m[v]=c;return True
        return False
    for c in I:assert aug(c,set())
    h=[-1]*N
    for v,c in enumerate(m):h[c]=v
    return h
def verify(R):
    k=len(R[0]);assert len(R)==3
    for A in R:
        assert len(A)==k
        for row in A:assert sorted(row)==I
        for c in I:assert len({A[r][c] for r in range(k)})==k
    for i,j in ((0,1),(0,2),(1,2)):
        assert len({(R[i][r][c],R[j][r][c]) for r in range(k) for c in I})==k*N
    return True
def extend(R,seed,limit=100000):
    k=len(R[0]);rng=random.Random(seed)
    used={(i,j):{(R[i][r][c],R[j][r][c]) for r in range(k) for c in I} for i,j in ((0,1),(0,2),(1,2))}
    dom=[]
    for c in I:
        avail=[[v for v in I if v not in {R[s][r][c] for r in range(k)}] for s in range(3)]
        opts=[(a,b,d) for a in avail[0] for b in avail[1] for d in avail[2]
              if (a,b) not in used[0,1] and (a,d) not in used[0,2] and (b,d) not in used[1,2]]
        rng.shuffle(opts);dom.append(opts)
    order=sorted(I,key=lambda c:(len(dom[c]),c));ans=[[-1]*N for _ in range(3)];nodes=0
    def dfs(t,ma,mb,mc):
        nonlocal nodes
        nodes+=1
        if nodes>limit:raise RuntimeError('UNKNOWN_BUDGET')
        if t==N:return True
        c=order[t]
        for a,b,d in dom[c]:
            if (ma>>a&1) or (mb>>b&1) or (mc>>d&1):continue
            ans[0][c]=a;ans[1][c]=b;ans[2][c]=d
            if dfs(t+1,ma|1<<a,mb|1<<b,mc|1<<d):return True
        return False
    assert dfs(0,0,0,0),'UNSAT_FOR_THIS_FIXED_PREFIX'
    for s in range(3):R[s].append(ans[s])
    verify(R)
    return nodes

def main():
    witnesses=[];node_max=0
    for idx,g in enumerate(representatives()):
        h=h_matching(g)
        R=[[I[:],list(f)],[I[:],list(g)],[I[:],h]]
        node_max=max(node_max,extend(R,20261102+idx))
        for depth in (4,5,6):node_max=max(node_max,extend(R,9183+idx*10+depth,30000))
        witnesses.append(R)
    canonical=json.dumps(witnesses,separators=(',',':'))
    sha=hashlib.sha256(canonical.encode()).hexdigest()
    result={'f_cycle_type':[2]*5,'g_orbits':156,'g_labeled':440192,'six_row_witnesses':len(witnesses),
            'overlay_each':[60,60,60],'max_nodes_one_row':node_max,'canonical_witness_sha256':sha,
            'global_status':'OPEN'}
    print(json.dumps(result,indent=2))
    assert sha=='5b198704a6cd24cae9ba57b7f938ce121aba182df1fc78738d39ab92a2aff66f'
    with open('E036_WITNESSES.json','w') as out:out.write(canonical+'\n')
if __name__=='__main__':main()
