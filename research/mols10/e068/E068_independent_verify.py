#!/usr/bin/env python3
"""Independent mathematical certificate check for a partial-pair no-transversal-through-cell cut.

This implementation does NOT reuse the C++ MRV search: uses fixed increasing row
permutation enumeration and bit masks. A full triple must partition 100 cells
into ten transversals of A,B. Hence failure to place ANY transversal through
one cell, even with unknown values treated as unrestricted, proves NO full
triple can contain the listed partial A/B coordinate assignments.
"""
from __future__ import annotations
import json, pathlib, itertools, hashlib, time
ROOT=pathlib.Path(__file__).resolve().parent

def witness(n:int,known:dict[tuple[int,int,int],int],anchor:tuple[int,int]) -> tuple[int,...]|None:
    ar,ac=anchor
    if not (0<=ar<n and 0<=ac<n): raise ValueError('anchor')
    arr=[-1]*n;arr[ar]=ac
    def next_row(r,cm,am,bm):
        if r==n:return tuple(arr)
        if r==ar:return next_row(r+1,cm,am,bm)
        for c in range(n):
            if cm>>c&1:continue
            ka=known.get((0,r,c));kb=known.get((1,r,c))
            if ka is not None and am>>ka&1:continue
            if kb is not None and bm>>kb&1:continue
            arr[r]=c
            ans=next_row(r+1,cm|(1<<c),am|((1<<ka) if ka is not None else 0),bm|((1<<kb) if kb is not None else 0))
            if ans is not None:return ans
        arr[r]=-1
        return None
    ka=known.get((0,ar,ac));kb=known.get((1,ar,ac))
    return next_row(0,1<<ac,(1<<ka) if ka is not None else 0,(1<<kb) if kb is not None else 0)

def valid_witness(n,known,anchor,perm):
    if perm is None or len(perm)!=n or sorted(perm)!=list(range(n)) or perm[anchor[0]]!=anchor[1]:return False
    aa=[known[(0,r,c)] for r,c in enumerate(perm) if (0,r,c) in known]
    bb=[known[(1,r,c)] for r,c in enumerate(perm) if (1,r,c) in known]
    return len(set(aa))==len(aa) and len(set(bb))==len(bb)

def main():
    all12=json.loads((ROOT/'E068_all_12_anchors.json').read_text())['results']
    assert len(all12)==12
    src=json.loads((ROOT/'E061_near_triple.json').read_text())['squares']
    A,B=src[:2];n=10
    assert all(sorted(mat[r])==list(range(n)) for mat in (A,B) for r in range(n))
    assert all(sorted(mat[r][c] for r in range(n))==list(range(n)) for mat in (A,B) for c in range(n))
    assert len({(A[r][c],B[r][c]) for r in range(n) for c in range(n)})==100
    full={(s,r,c):(A if s==0 else B)[r][c] for s in range(2) for r in range(n) for c in range(n)}
    best=min(all12,key=lambda q:q['literal_count'])
    assert best['literal_count']==len(best['known_symbols'])
    results=[];st=time.perf_counter()
    for q in all12:
        known={(s,r,c):v for s,r,c,v in q['known_symbols']}
        assert len(known)==q['literal_count']
        assert all(full[k]==v for k,v in known.items())
        assert witness(10,known,tuple(q['anchor'])) is None, 'false pruning certificate at '+str(q['anchor'])
        for i,(sym,rr,cc,v) in enumerate(q['known_symbols']):
            reduction=dict(known);assert reduction.pop((sym,rr,cc))==v
            perm=witness(10,reduction,tuple(q['anchor']))
            assert valid_witness(10,reduction,tuple(q['anchor']),perm), ('failed deletion minimality',q['anchor'],i)
        results.append({'anchor':q['anchor'],'core_symbols':len(known),
                        'NO_TRANSVERSAL_THROUGH_ANCHOR':'VERIFIED',
                        'every_one_literal_deletion_has_transversal':'VERIFIED'})
    known={(s,r,c):v for s,r,c,v in best['known_symbols']};anchor=tuple(best['anchor'])
    leaveone=[]
    for i,lit in enumerate(best['known_symbols']):
        s,r,c,v=lit;key=(s,r,c)
        without=dict(known);assert without.pop(key)==v
        perm=witness(10,without,anchor)
        assert valid_witness(10,without,anchor,perm), ('not deletion minimal',i,lit)
        leaveone.append({'omitted_literal_id':i,'row_to_column':list(perm)})
    # Positive control GF5 3-MOLS: A=r+c; B=r+2c; C=r+3c, modulo 5.
    n5=5
    squares=[[[ (r+k*c)%n5 for c in range(n5)] for r in range(n5)] for k in (1,2,3)]
    assert all(sorted(m[r])==list(range(5)) for m in squares for r in range(5))
    assert all(sorted(m[r][c] for r in range(5))==list(range(5)) for m in squares for c in range(5))
    assert all(len({(squares[a][r][c],squares[b][r][c]) for r in range(5) for c in range(5)})==25 for a,b in ((0,1),(0,2),(1,2)))
    pos={(s,r,c):squares[s][r][c] for s in range(2) for r in range(5) for c in range(5)}
    for r in range(5):
        for c in range(5):
            q=witness(5,pos,(r,c))
            assert valid_witness(5,pos,(r,c),q),('false positive',r,c)
    result={
      'experiment':'E068', 'n':10,
      'cert_type':'sound partial-pair transversal-through-anchor OVERAPPROX failure',
      'global_problem_status':'OPEN',
      'all_12_unsupported_anchors_verified':results,
      'best_anchor':list(anchor),'best_partial_core_size':len(known),
      'known_square_coordinates_possible':200,
      'unknown_square_coordinates':200-len(known),
      'all_best_core_single_literal_deletions_are_satisfiable':True,
      'independent_positive_GF5_anchor_checks':25,
      'negative_core_is_embedded_in_known_egan_pair':True,
      'global_first_column_classes_eliminated':0,
      'logic':'Any third Latin square orthogonal to A and B partitions the 100 cells into 10 disjoint common transversals. At least one must cover the anchor cell. If even wildcard-permitted partial pair has no transversal through anchor, NO completion to 3-MOLS contains all core assignments.',
      'elapsed_seconds':round(time.perf_counter()-st,5)
    }
    (ROOT/'E068_independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'E068_leave_one_out_witnesses.json').write_text(json.dumps({'anchor':list(anchor),'core_literals':best['known_symbols'],'witnesses':leaveone},indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='all_12_unsupported_anchors_verified'},indent=2))
if __name__=='__main__':main()
