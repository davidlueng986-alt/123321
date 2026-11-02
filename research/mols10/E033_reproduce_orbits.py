#!/usr/bin/env python3
"""E033 exact centralizer-orbit counts: independent Burnside and orbit BFS.
Stdlib only. python E033_reproduce_orbits.py [--full].
Not a proof of global MOLS(10) existence/nonexistence.
"""
import argparse,json,math
from collections import defaultdict

def partitions(n,low=2):
    if n==0:yield ()
    for k in range(low,n+1):
        for r in partitions(n-k,k):yield (k,)+r

def canonical(t):
    a=[];s=0
    for k in sorted(t,reverse=True):
        a.extend(s+(i+1)%k for i in range(k));s+=k
    return tuple(a)

def cycles(p):
    seen=set();ans=[]
    for i in range(len(p)):
        if i not in seen:
            c=[];j=i
            while j not in seen:
                seen.add(j);c.append(j);j=p[j]
            assert j==i;ans.append(c)
    return ans

def generators(f):
    n=len(f);C=cycles(f);out=[]
    for cyc in C:
        p=list(range(n))
        for i,x in enumerate(cyc):p[x]=cyc[(i+1)%len(cyc)]
        out.append(tuple(p))
    groups=defaultdict(list)
    for cyc in C:groups[len(cyc)].append(cyc)
    for arr in groups.values():
        for a,b in zip(arr,arr[1:]):
            p=list(range(n))
            for x,y in zip(a,b):p[x]=y;p[y]=x
            out.append(tuple(p))
    return out

def centralizer(f):
    n=len(f);start=tuple(range(n));seen={start};todo=[start]
    for p in todo:
        for q in generators(f):
            h=tuple(p[q[i]] for i in range(n))
            if h not in seen:seen.add(h);todo.append(h)
    assert all(all(p[f[i]]==f[p[i]] for i in range(n)) for p in seen)
    return seen

def permanent(W):
    dp={0:1};m=len(W)
    for row in W:
        nxt={}
        for mask,v in dp.items():
            for j,w in enumerate(row):
                if w and not mask>>j&1:
                    z=mask|(1<<j);nxt[z]=nxt.get(z,0)+v*w
        dp=nxt
    return dp.get((1<<m)-1,0)

def fixed_g(f,p):
    groups=defaultdict(list)
    for cyc in cycles(p):groups[len(cyc)].append(cyc)
    ans=1
    for L,arr in groups.items():
        W=[]
        for src in arr:
            W.append([sum(all(dest[(i+shift)%L] not in (src[i],f[src[i]])
                              for i in range(L)) for shift in range(L)) for dest in arr])
        ans*=permanent(W)
    return ans

def enumerate_g(f):
    n=len(f);g=[0]*n
    def rec(i,mask):
        if i==n:yield tuple(g);return
        for v in range(n):
            if v!=i and v!=f[i] and not mask>>v&1:
                g[i]=v;yield from rec(i+1,mask|(1<<v))
    yield from rec(0,0)

def orbit_count(f):
    n=len(f);gens=generators(f);seen=set();num=0;count=0
    for g in enumerate_g(f):
        count+=1
        if g in seen:continue
        num+=1;todo=[g];seen.add(g)
        for h in todo:
            for p in gens:
                inv=[0]*n
                for i,x in enumerate(p):inv[x]=i
                z=tuple(inv[h[p[i]]] for i in range(n))
                if z not in seen:seen.add(z);todo.append(z)
    assert len(seen)==count
    return count,num

def run(full=False):
    out=[]
    for t in partitions(10):
        f=canonical(t);G=centralizer(f);s=sum(fixed_g(f,p) for p in G)
        assert s%len(G)==0
        count=fixed_g(f,tuple(range(10)));orbits=s//len(G)
        if full:assert orbit_count(f)==(count,orbits)
        z={'type':list(t),'centralizer':len(G),'allowed_g':count,
           'orbits':orbits,'burnside_sum':s,'full_orbit_crosscheck':full}
        out.append(z);print(json.dumps(z),flush=True)
    assert sum(z['orbits'] for z in out)==162959
    assert sum(z['allowed_g'] for z in out)==5278724
    raw=sum(math.factorial(10)//(9*z['centralizer'])*z['allowed_g'] for z in out)
    assert raw==65239993856
    print(json.dumps({'types':12,'sum_orbits':162959,'raw_labeled_f_g':raw,'status':'PASS'}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--full',action='store_true')
    run(p.parse_args().full)
