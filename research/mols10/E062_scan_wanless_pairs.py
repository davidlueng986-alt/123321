#!/usr/bin/env python3
"""Exact common-transversal and disjoint-packing scan of Ian M. Wanless's
published order-10 MOLS pair catalogue. Source:
https://users.monash.edu.au/~iwanless/data/MOLS/MOLS10.txt

Input contains 5562 10x10 Latin squares (2781 consecutive orthogonal pairs),
per the author's published format. All conclusions restricted to THESE pairs.
No output implies unrestricted 3-MOLS(10) nonexistence.
"""
import argparse, collections, hashlib, json, sys, time, urllib.request
from pathlib import Path

def parse_latin_data(data):
    lines=data.decode('ascii').splitlines(); header=lines[0].split()
    n,k,m=map(int,header[:3]); assert n==k==10 and m%2==0, (n,k,m)
    allowed=set(chr(97+i) for i in range(n))
    rows=[]
    for l in lines[1:]:
        s=l.strip()
        if len(s)==n and set(s)==allowed:
            rows.append(tuple(ord(c)-97 for c in s))
        if len(rows)==n*m:break
    assert len(rows)==n*m,(len(rows),n*m)
    squares=[rows[i:i+n] for i in range(0,len(rows),n)]
    for M in squares:
        for row in M:assert len(set(row))==n
        for c in range(n):assert len(set(M[r][c] for r in range(n)))==n
    return [(squares[i],squares[i+1]) for i in range(0,m,2)]

def check_pair(A,B):
    n=len(A)
    assert len(B)==n
    assert len({(A[r][c],B[r][c]) for r in range(n) for c in range(n)})==n*n

def enumerate_common(A,B):
    n=len(A); col=[0]*n; trans=[];nodes=0
    def rec(r,cm,am,bm):
        nonlocal nodes
        nodes+=1
        if r==n:
            trans.append(tuple(col));return
        for c in range(n):
            bc=1<<c;aa=1<<A[r][c];bb=1<<B[r][c]
            if (cm&bc) or (am&aa) or (bm&bb):continue
            col[r]=c;rec(r+1,cm|bc,am|aa,bm|bb)
    rec(0,0,0,0)
    return trans,nodes

def packing_best(trans,n,limit=200000):
    # Each cell is a bit in an n*n-bit Python integer. Recursive search is exact
    # if the node bound is not reached; never call incomplete searches UNSAT.
    T=len(trans)
    if T==0:return {'status':'EXACT','size':0,'indices':[],'nodes':0}
    cells=[sum(1<<(r*n+c) for r,c in enumerate(tr)) for tr in trans]
    adj=[sum((1<<j) for j in range(T) if i!=j and (cells[i]&cells[j])==0) for i in range(T)]
    # Greedy-compatible branch order (high degree first) improves witness search.
    order=sorted(range(T),key=lambda i:adj[i].bit_count(),reverse=True)
    adjorder=[sum(1<<j for j in range(T) if i!=j and (cells[order[i]]&cells[order[j]])==0) for i in range(T)]
    counts=0;cut=False
    def dfs(mask,k,sel):
        nonlocal counts,cut
        counts+=1
        if counts>limit:
            cut=True;return None
        if k==0:return sel
        if mask.bit_count()<k:return None
        while mask:
            bit=mask & -mask; idx=bit.bit_length()-1;mask-=bit
            ret=dfs(mask&adjorder[idx],k-1,sel+[order[idx]])
            if ret is not None:return ret
            if cut:return None
            if mask.bit_count()<k:break
        return None
    for k in range(min(n-1,T),0,-1):
        got=dfs((1<<T)-1,k,[])
        if got is not None:
            return {'status':'EXACT' if not cut else 'UNKNOWN_PREVIOUS_K', 'size':k,'indices':got,'nodes':counts}
        if cut:
            return {'status':'UNKNOWN_BUDGET','lower_bound':0,'upper_bound':k,'nodes':counts}
    return {'status':'EXACT','size':0,'indices':[],'nodes':counts}

def construct_third(A,B,trans,idx):
    n=len(A);C=[[-1]*n for _ in range(n)]
    for color,i in enumerate(idx):
        for r,c in enumerate(trans[i]):
            assert C[r][c]==-1
            C[r][c]=color
    for r in range(n):
        for c in range(n):
            if C[r][c]==-1:C[r][c]=n-1
    for M in (A,B,C):
        assert all(set(row)==set(range(n)) for row in M)
        assert all({M[r][c] for r in range(n)}==set(range(n)) for c in range(n))
    for X,Y in ((A,B),(A,C),(B,C)):
        assert len({(X[r][c],Y[r][c]) for r in range(n) for c in range(n)})==n*n
    return C

def check_bipartite_remaining(A,B,trans,idx):
    n=len(A);occ={(r,c) for i in idx for r,c in enumerate(trans[i])}
    left=[(r,c) for r in range(n) for c in range(n) if (r,c) not in occ]
    assert len(left)==2*n
    demands=collections.defaultdict(list)
    for i,(r,c) in enumerate(left):
        for key in ((0,r),(1,c),(2,A[r][c]),(3,B[r][c])):
            demands[key].append(i)
    assert len(demands)==4*n and all(len(q)==2 for q in demands.values())
    G=[set() for _ in left]
    for i,j in demands.values():G[i].add(j);G[j].add(i)
    color=[-1]*len(left)
    for start in range(len(left)):
        if color[start]>=0:continue
        color[start]=0;stack=[start]
        while stack:
            u=stack.pop()
            for v in G[u]:
                if color[v]<0:color[v]=1-color[u];stack.append(v)
                elif color[v]==color[u]:return False,None
    tr=[None]*n
    for i,(r,c) in enumerate(left):
        if color[i]==0:tr[r]=c
    assert all(x is not None for x in tr)
    return True,tr

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',help='Pre-downloaded Wanless file (avoid all network)',default=None)
    parser.add_argument('--url',default='https://users.monash.edu.au/~iwanless/data/MOLS/MOLS10.txt')
    parser.add_argument('--output',default='E062_WANLESS_PAIR_SCAN.json')
    parser.add_argument('--maxpack-nodes',type=int,default=200000)
    parser.add_argument('--max-pairs',type=int,default=0)
    opt=parser.parse_args();t0=time.monotonic()
    data=Path(opt.input).read_bytes() if opt.input else urllib.request.urlopen(opt.url,timeout=45).read()
    parsed=parse_latin_data(data);count=len(parsed)
    if opt.max_pairs:parsed=parsed[:opt.max_pairs]
    distributions=collections.Counter();ntrans=collections.Counter();cases=[];found=None;unknown=[];summary_max=-1
    for index,(A,B) in enumerate(parsed):
        check_pair(A,B)
        tr,nodes=enumerate_common(A,B)
        pack=packing_best(tr,10,opt.maxpack_nodes)
        ntrans[len(tr)]+=1
        if pack['status']=='UNKNOWN_BUDGET':unknown.append(index)
        if pack['status'] in ('EXACT','UNKNOWN_PREVIOUS_K'):
            distributions[pack['size']]+=1
            if pack['size']>summary_max:
                summary_max=pack['size']
                cases.append({'index':index,'max_disjoint_lower_bound':pack['size'],'common_transversals':len(tr),'best_pack':pack['indices']})
            if pack['size']>=9:
                C=construct_third(A,B,tr,pack['indices'][:9])
                found={'index':index,'A':A,'B':B,'C':C,'closure':'FULL_100_100_100_VERIFIED'}
                break
            if pack['size']==8:
                bp,other=check_bipartite_remaining(A,B,tr,pack['indices'][:8])
                if bp:
                    C=construct_third(A,B,tr,pack['indices'][:8]+[tr.index(tuple(other))])
                    found={'index':index,'A':A,'B':B,'C':C,'closure':'FULL_100_100_100_VERIFIED'}
                    break
        if (index+1)%250==0:
            print('PROGRESS',index+1,'/',len(parsed),'transversal_max',max(ntrans),'packing_max_lower_bound',summary_max,'unknown',len(unknown),flush=True)
    report={'source_url':opt.url if not opt.input else None,'source_file':str(opt.input) if opt.input else None,'sha256':hashlib.sha256(data).hexdigest(),'source_squares':count*2,'source_pairs':count,'pairs_processed':index+1,'max_common_transversals':max(ntrans) if ntrans else None,'common_transversal_count_distribution':dict(sorted(ntrans.items())), 'disjoint_packing_distribution_exact_or_lowerbound':dict(sorted(distributions.items())), 'packing_unknown_cases':unknown, 'record_packing_improvements':cases,'complete_witness':found,'global_claim':'OPEN; results apply only to published pairs; a full witness requires 3 complete 10x10 arrays','seconds':round(time.monotonic()-t0,3)}
    Path(opt.output).write_text(json.dumps(report,indent=2)+'\n')
    print('SUMMARY',json.dumps({k:v for k,v in report.items() if k not in ('complete_witness','record_packing_improvements')},indent=2),flush=True)
    if found:print('CLOSED_WITNESS',json.dumps(found),flush=True)
if __name__=='__main__':main()