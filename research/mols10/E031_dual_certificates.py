#!/usr/bin/env python3
"""Exact verified Farkas certificates for residual-triangle LP infeasibility.
Given remaining pairs E in AB/AC/BC and allowed triples T, a rational weight w
with sum_{e in E} w_e > 0 and sum_{e in each T} w_e <= 0 disproves
any fractional exact cover A x=1, x>=0. Verified with exact fractions.
"""
import json,sys
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
P=((0,1),(0,2),(1,2))

def certificate(S,n=10):
    k=len(S[0]);E=[]
    for a,b in P:
        occ={(S[a][r][c],S[b][r][c]) for r in range(k) for c in range(n)}
        E.append([(v,w) for v in range(n) for w in range(n) if (v,w) not in occ])
    sets=list(map(set,E))
    T=[(a,b,c) for a,b in E[0] for c in range(n) if (a,c) in sets[1] and (b,c) in sets[2]]
    idx={};j=0
    for p in range(3):
        for edge in E[p]:idx[p,edge]=j;j+=1
    I=[];J=[]
    for u,(a,b,c) in enumerate(T):
        for p,edge in enumerate(((a,b),(a,c),(b,c))):I.append(u);J.append(idx[p,edge])
    AT=coo_matrix((np.ones(len(I)),(I,J)),shape=(len(T),j)).tocsr()
    z=linprog(-np.ones(j),A_ub=AT,b_ub=np.zeros(len(T)),bounds=[(-1,1)]*j,method='highs')
    if z.status!=0:return {'status':'UNKNOWN_DUAL','solver_status':z.status}
    # Recover simplest small-denominator rational certificate and exact-replay it.
    for d in (1,2,3,4,5,6,8,10,12,16,24,48,120,1000):
        w=[Fraction(float(v)).limit_denominator(d) for v in z.x]
        if sum(w)>0 and all(w[idx[0,(a,b)]]+w[idx[1,(a,c)]]+w[idx[2,(b,c)]]<=0 for a,b,c in T):
            break
    else:return {'status':'UNKNOWN_RATIONAL_RECOVERY','LP_objective':float(-z.fun)}
    used=[{'pair_axis':P[p], 'edge':list(edge),'numerator':w[idx[p,edge]].numerator,
           'denominator':w[idx[p,edge]].denominator} for p in range(3) for edge in E[p] if w[idx[p,edge]]]
    bound=sum(w)
    assert bound>0
    assert all(w[idx[0,(a,b)]]+w[idx[1,(a,c)]]+w[idx[2,(b,c)]]<=0 for a,b,c in T)
    return {'status':'EXACT_RATIONAL_DUAL','n':n,'fixed_rows':k,'pair_edges':j,
      'candidate_triples':len(T),'nonzero_weights':len(used),'dual_sum':[bound.numerator,bound.denominator],
      'certificate':used,'source_squares':S}

def independently_replay(D):
    if D['status']!='EXACT_RATIONAL_DUAL':return None
    S=D['source_squares'];n=D['n'];k=len(S[0]);weights={}
    for ent in D['certificate']:
        p=P.index(tuple(ent['pair_axis']));weights[p,tuple(ent['edge'])]=Fraction(ent['numerator'],ent['denominator'])
    E=[]
    for a,b in P:
        u={(S[a][r][c],S[b][r][c]) for r in range(k) for c in range(n)}
        E.append({(x,y) for x in range(n) for y in range(n)}-u)
    assert all(edge in E[p] for (p,edge) in weights)
    total=sum(weights.values())
    assert total>0 and [total.numerator,total.denominator]==D['dual_sum']
    tested=0
    for a,b in E[0]:
        for c in range(n):
            if (a,c) in E[1] and (b,c) in E[2]:
                tested+=1
                assert weights.get((0,(a,b)),0)+weights.get((1,(a,c)),0)+weights.get((2,(b,c)),0)<=0
    assert tested==D['candidate_triples']
    return {'exactly_verified':True,'triangles_checked':tested,'strictly_positive_dual_sum':str(total)}

if __name__=='__main__':
    x=[json.loads(z) for z in open(Path(__file__).resolve().parent / 'E031_TRIANGLE_SEARCH.jsonl')][1]
    out=[]
    for i,S in enumerate(x['triangle_survivor_samples']):
        z=certificate(S);z['sample_index']=i;z['independent_replay']=independently_replay(z)
        out.append(z);print(i,z['status'],z.get('dual_sum'),z.get('nonzero_weights'),flush=True)
    open(Path(__file__).resolve().parent / 'E031_DUAL_CERTIFICATES.json','w').write(json.dumps(out,indent=2))
