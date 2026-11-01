"""Exhaust two-symbol connected-component flips preserving A/B orthogonality.

Restricted exact neighborhood: fix A, choose B symbols p,q; connect the 20
positions whenever they share a row, column or A-symbol. Each connected
component can be flipped between p,q and still obey every pair constraint.
This does NOT enumerate all Latin trades or all orthogonal mates.
"""
from collections import defaultdict
from verify import analyze

def two_symbol_components(a,b,p,q):
    n=len(a)
    if p>=q or not(0<=p<q<n):raise ValueError("requires 0<=p<q<n")
    if not analyze([a,b],n)[0]["orthogonal"]:
        raise ValueError("input must be orthogonal Latin pair")
    cells=[(i,j) for i in range(n) for j in range(n) if b[i][j] in (p,q)]
    adjacency={c:set() for c in cells}
    for key in (lambda i,j:i,lambda i,j:j,lambda i,j:a[i][j]):
        groups=defaultdict(list)
        for i,j in cells:groups[key(i,j)].append((i,j))
        if len(groups)!=n or any(len(v)!=2 for v in groups.values()):
            raise AssertionError("invalid two-symbol pairing")
        for u,v in groups.values():
            adjacency[u].add(v);adjacency[v].add(u)
    components=[];visited=set()
    for start in cells:
        if start in visited:continue
        cur=[start];visited.add(start);comp=[]
        while cur:
            node=cur.pop();comp.append(node)
            for nxt in adjacency[node]:
                if nxt not in visited:visited.add(nxt);cur.append(nxt)
        components.append(sorted(comp))
    return components

def flip_component(a,b,p,q,component):
    out=[r.copy() for r in b]
    for i,j in component:out[i][j]=q if b[i][j]==p else p
    if not analyze([a,out],len(a))[0]["orthogonal"]:
        raise AssertionError("component flip broke pair")
    return out

def trade_neighborhood(a,b):
    n=len(a);trades=[]
    for p in range(n):
        for q in range(p+1,n):
            cs=two_symbol_components(a,b,p,q)
            if len(cs)>1:
                trades.append({"symbols":[p,q],
                               "component_sizes":[len(c) for c in cs],
                               "neighbor":flip_component(a,b,p,q,cs[-1])})
    return trades
