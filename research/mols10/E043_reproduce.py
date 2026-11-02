#!/usr/bin/env python3
"""E043: reproducible bounded exact fixed-prefix Farkas certificates.
Run E036_reproduce.py first in this directory to create E036_WITNESSES.json.
Then python E043_reproduce.py START END, with 0<=START<END<=2184.
This proves ONLY specified fixed-prefix nonextension, not global 3-MOLS(10).
Requires NumPy and SciPy; independently replay certificates with a separate
integer-only verifier. No numerical solver status alone is accepted as proof.
"""
import sys,json,itertools,collections,time
import numpy as np
from scipy.optimize import linprog
from E035_column_residual import model

def main(start,end):
    assert 0<=start<end<=2184
    witnesses=json.load(open('E036_WITNESSES.json'))
    assert len(witnesses)==156
    subsets=[s for s in itertools.combinations(range(6),4) if s!=(0,1,2,3)]
    assert len(subsets)==14
    counts=collections.Counter()
    certs=[]
    began=time.monotonic()
    for index in range(start,end):
        orbit,sub=index//14,subsets[index%14]
        S=[[sq[r] for r in sub] for sq in witnesses[orbit]]
        A,T,E=model(S)
        assert A.shape[0]==360
        deg=np.diff(A.indptr)
        if (deg==0).any():
            demand=list(E[int(np.flatnonzero(deg==0)[0])])
            certs.append(dict(orbit=orbit,rows=sub,kind='ZERO',demand=demand))
            counts['ZERO']+=1
            continue
        lp=linprog(np.zeros(len(T)),A_eq=A,b_eq=np.ones(360),
                   bounds=(0,None),method='highs',options={'time_limit':1})
        if lp.status!=2:
            counts['NOT_PROVED_BY_LP']+=1
            certs.append(dict(orbit=orbit,rows=sub,kind='UNKNOWN',lp_status=int(lp.status)))
            continue
        dual=linprog(-np.ones(360),A_ub=A.T,b_ub=np.zeros(len(T)),
                     bounds=[(-1,1)]*360,method='highs',
                     options={'time_limit':1})
        if dual.status!=0 or -dual.fun<1e-5:
            counts['DUAL_UNKNOWN']+=1
            certs.append(dict(orbit=orbit,rows=sub,kind='UNKNOWN',reason='dual'))
            continue
        success=False
        for scale in (10,30,100,300,1000,3000,10000,30000,100000):
            w=np.floor(dual.x*scale+1e-9).astype(np.int64)-1
            if int(w.sum())>0 and int((A.T@w).max())<=0:
                # All exact checks use int64 and are repeated after rounding.
                certs.append(dict(orbit=orbit,rows=sub,kind='DUAL',
                    weights=w.tolist(),rhs=int(w.sum()),maxscore=int((A.T@w).max()),
                    scale=scale))
                counts['DUAL']+=1
                success=True
                break
        if not success:
            counts['ROUNDING_UNKNOWN']+=1
            certs.append(dict(orbit=orbit,rows=sub,kind='UNKNOWN',reason='rounding'))
    obj={'experiment':'E043','start':start,'end':end,'counts':dict(counts),
         'certificates':certs,'elapsed_s':round(time.monotonic()-began,3),
         'status':'OPEN','scope':'fixed four-row prefixes only'}
    name=f'E043_REPRODUCED_{start}_{end}.json'
    with open(name,'w') as f:json.dump(obj,f,separators=(',',':'))
    print(name,obj['counts'],'elapsed_s',obj['elapsed_s'])
    assert counts['NOT_PROVED_BY_LP']==counts['DUAL_UNKNOWN']==counts['ROUNDING_UNKNOWN']==0

if __name__=='__main__':
    assert len(sys.argv)==3,'Usage: python E043_reproduce.py START END'
    main(int(sys.argv[1]),int(sys.argv[2]))
