#!/usr/bin/env python3
"""Exhaustive min-removal audit for each pair of external points of the 236-cap.

Requires numpy and numba for a bounded CPU-only exhaustive calculation.
The union of the secant matchings for p and q is a graph of maximum
degree two and with no odd cycles. A minimum vertex cover in each path
or even-cycle component has size floor(number_of_vertices/2).
If r=-p-q belongs to the cap, r must also be removed (forced vertex).
"""
import collections
import itertools
import json
import numpy as np
from numba import njit
from generate_calderbank_fishburn import construction

@njit
def root(parent, i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i

@njit
def all_pair_covers(rows, lengths, outsider_digits, cap_lookup):
    count=rows.shape[0]
    freq=np.zeros(237,dtype=np.int64)
    best=237
    best_example=(-1,-1)
    for a in range(count):
        for b in range(a+1,count):
            parent=np.arange(236,dtype=np.int16)
            sizes=np.ones(236,dtype=np.int16)
            active=np.zeros(236,dtype=np.bool_)
            z=0
            for j in range(7):
                z=z*3+((-int(outsider_digits[a,j])-int(outsider_digits[b,j]))%3)
            forced=int(cap_lookup[z])
            for group in range(2):
                candidate=a if group==0 else b
                for k in range(lengths[candidate]):
                    u=int(rows[candidate,k,0]);v=int(rows[candidate,k,1])
                    if u==forced or v==forced:
                        continue
                    active[u]=True;active[v]=True
                    ru=root(parent,u);rv=root(parent,v)
                    if ru != rv:
                        if sizes[ru] < sizes[rv]:
                            ru,rv=rv,ru
                        parent[rv]=ru
                        sizes[ru]+=sizes[rv]
            deletions=1 if forced>=0 else 0
            for v in range(236):
                if active[v] and parent[v]==v:
                    deletions+=sizes[v]//2
            freq[deletions]+=1
            if deletions < best:
                best=deletions
                best_example=(a,b)
    return freq,best,best_example

def audit():
    A=construction()
    index={v:i for i,v in enumerate(A)}
    inside=set(A)
    outside=sorted(set(itertools.product(range(3),repeat=7))-inside)
    outside_idx={p:i for i,p in enumerate(outside)}
    lines=[[] for _ in outside]
    for i,p in enumerate(A):
        for j in range(i+1,len(A)):
            q=A[j]
            z=tuple((-x-y)%3 for x,y in zip(p,q))
            lines[outside_idx[z]].append((i,j))
    max_degree=max(map(len,lines))
    rows=np.full((len(outside),max_degree,2),-1,dtype=np.int16)
    lengths=np.zeros(len(outside),dtype=np.int16)
    for i,edges in enumerate(lines):
        lengths[i]=len(edges)
        for j,(u,v) in enumerate(edges):
            rows[i,j]=[u,v]
    digit_values=np.asarray(outside,dtype=np.int8)
    lookup=np.full(3**7,-1,dtype=np.int16)
    for p,i in index.items():
        key=0
        for d in p:
            key=3*key+d
        lookup[key]=i
    histogram,min_needed,(a,b)=all_pair_covers(rows,lengths,digit_values,lookup)
    n=len(outside)*(len(outside)-1)//2
    assert int(histogram.sum())==n==1_902_225
    assert min_needed==16
    assert histogram[16]==888
    return {
       "external_pairs_checked":n,
       "minimum_original_removals_for_any_two_outside_points":int(min_needed),
       "number_of_pairs_attaining_minimum":int(histogram[16]),
       "example_first":list(outside[a]),
       "example_second":list(outside[b]),
       "histogram":{str(i):int(c) for i,c in enumerate(histogram) if c>0},
       "implication":"Every edited cap containing at least two points outside the original 236-cap must delete at least 16 original points. Hence an improvement beyond 236 near this exact starting cap needs >=16 deletions and >=17 insertions. This is NOT a global upper bound for r3(7)."
    }

if __name__=="__main__":
    print(json.dumps(audit(),sort_keys=True,indent=2))
