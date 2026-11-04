#!/usr/bin/env python3
"""Numerical screening only; INFEASIBLE requires an exact independent rational dual.
All five OA coordinates included; first row and first column fixed.
"""
import json,itertools,random,time,sys
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from pathlib import Path
reps=[json.loads(line) for line in open(str(Path(__file__).resolve().parent/'E064_quotient_representatives.jsonl'))]
selected=[0,3,158,692,1417,2185,2265,2597,2697,2876]
random.Random(64).shuffle(selected)

def build(f,g):
    used=np.zeros(1000,dtype=bool)
    ab=set();ac=set();bc=set()
    def keys(r,c,a,b,d):
        return [10*r+c,100+10*r+a,200+10*c+a,300+10*r+b,400+10*c+b,500+10*r+d,600+10*c+d,700+10*a+b,800+10*a+d,900+10*b+d]
    for r in range(10):
        for c in range(10):
            if r and c:continue
            a,b,d=(c,c,c) if r==0 else (r,f[r],g[r])
            for k in keys(r,c,a,b,d):assert not used[k];used[k]=True
            ab.add((a,b));ac.add((a,d));bc.add((b,d))
    idx={k:i for i,k in enumerate(np.where(~used)[0])}
    I=[];J=[];vals=[];count=0
    for r in range(1,10):
        for c in range(1,10):
            for a in range(10):
                if a in (r,c):continue
                for b in range(10):
                    if b in (c,f[r]) or (a,b) in ab:continue
                    for d in range(10):
                        if d in (c,g[r]) or (a,d) in ac or (b,d) in bc:continue
                        ks=keys(r,c,a,b,d)
                        if any(used[k] for k in ks):raise ValueError('covered resource reused')
                        I.extend(idx[k] for k in ks);J.extend([count]*10);count+=1
    A=coo_matrix((np.ones(len(I),dtype=np.float64),(I,J)),shape=(len(idx),count)).tocsr()
    return A

out=[]
for i in selected:
    q=reps[i];a=build(q['B_col0'],q['C_col0'])
    start=time.monotonic();z=linprog(np.zeros(a.shape[1]),A_eq=a,b_eq=np.ones(a.shape[0]),bounds=(0,None),method='highs',options={'time_limit':3})
    out.append({'id':i,'type':q['type'],'rows':a.shape[0],'columns':a.shape[1],'status':int(z.status),'message':z.message,'seconds':round(time.monotonic()-start,3),'max_err':float(np.max(np.abs(a@z.x-1))) if z.status==0 else None})
    print(out[-1],flush=True)
Path(str(Path(__file__).resolve().parent/'E064_root_lp_probe.json')).write_text(json.dumps(out,indent=2)+'\n')