#!/usr/bin/env python3
"""CAP046: NONLOCAL 237-point constructive MILP using affine-unions of known 236.

Directly search for a cap of size >=237 in B ∪ g(B) for affine GL7 maps g.
All returned witnesses are checked by independent F3 arithmetic. A solver
time limit gives UNKNOWN; even MILP infeasibility is only a restricted
pool claim and has no globally exhaustive coverage.
CPU-only SciPy HiGHS, no paid compute.
"""
import argparse,random,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csr_matrix,vstack

POWS=np.array([729,243,81,27,9,3,1],dtype=np.int16)
ALL=np.array([[(i//int(k))%3 for k in POWS] for i in range(2187)],dtype=np.int16)
THIRD=((-(ALL[:,None,:]+ALL[None,:,:]))%3@POWS).astype(np.int16)
BUCKETS=(24,48,72,96,112,128,144,160,172,192)

def load_236():
    p=Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt'
    rows=[x.strip() for x in p.read_text().splitlines()
          if len(x.strip())==7 and set(x.strip())<=set('012')]
    ids=[int(s,3) for s in rows]
    assert len(ids)==236 and cap_valid(ids)
    return ids,np.array([ALL[i] for i in ids])

def cap_valid(A):
    s=set(A)
    return len(s)==len(A) and all(int(THIRD[x,y]) not in s
           for k,x in enumerate(A) for y in A[k+1:])

def elementary(rng):
    a,b=rng.sample(range(7),2)
    mode=rng.randrange(4)
    E=np.eye(7,dtype=np.int16)
    if mode==0:E[a,b]=rng.choice([1,2])
    if mode==1:E[[a,b]]=E[[b,a]]
    if mode==2:E[a,a]=2
    if mode==3:E[a,b]=rng.choice([1,2]);E[b,b]=2
    return E

def choose_pools(base,coords,seed=202611031,trials=1400):
    rng=random.Random(seed)
    buckets={}
    base_set=set(base)
    for _ in range(trials):
        T=np.eye(7,dtype=np.int16)
        for j in range(rng.randrange(1,8)):
            T=(elementary(rng)@T)%3
        shift=np.zeros(7,dtype=np.int16)
        if rng.random()<.25:shift[rng.randrange(7)]=rng.choice([1,2])
        transformed=set(map(int,((coords@T.T+shift)%3@POWS)))
        overlap=len(base_set&transformed)
        group=min(BUCKETS,key=lambda v:abs(v-overlap))
        if group not in buckets or abs(group-overlap)<abs(group-buckets[group][0]):
            buckets[group]=(overlap,T.tolist(),shift.tolist(),transformed)
    return buckets

def matrix_pool(U):
    U=sorted(U);index={v:i for i,v in enumerate(U)}
    rows=[];cols=[];num=0
    for i,x in enumerate(U):
        for j in range(i+1,len(U)):
            z=int(THIRD[x,U[j]])
            k=index.get(z,-1)
            if k>j:
                rows.extend((num,)*3);cols.extend((i,j,k));num+=1
    sparse=csr_matrix((np.ones(len(rows)),(rows,cols)),
                       shape=(num,len(U)))
    return U,sparse,num

def attempt(pool,seconds=12,mode='feasibility'):
    U,M,num=matrix_pool(pool);n=len(U)
    c=np.zeros(n) if mode=='feasibility' else -np.ones(n)
    if mode=='feasibility':
        A=vstack((M,csr_matrix(np.ones((1,n)))),format='csr')
        low=np.concatenate((np.full(num,-np.inf),[237.]))
        up=np.concatenate((np.full(num,2.),[np.inf]))
    else:
        A=M;low=np.full(num,-np.inf);up=np.full(num,2.)
    start=time.perf_counter()
    sol=milp(c=c,integrality=np.ones(n),bounds=Bounds(np.zeros(n),np.ones(n)),
             constraints=LinearConstraint(A,low,up),
             options={'time_limit':seconds,'presolve':True,'mip_rel_gap':0.})
    out={'pool_size':n,'3AP_constraints':num,'status':int(sol.status),
         'message':sol.message,'wall_seconds':round(time.perf_counter()-start,2),
         'independent_global_status':'UNKNOWN'}
    if sol.x is not None:
        found=[U[i] for i,val in enumerate(sol.x) if val>.5]
        out['candidate_size']=len(found)
        out['candidate_mod3_valid']=cap_valid(found)
        if out['candidate_mod3_valid'] and len(found)>=237:
            out['witness_7digits']=[''.join(map(str,ALL[k])) for k in found]
            out['disproves_r3_7_equals_236']=True
    return out

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--seed',type=int,default=202611031)
    parser.add_argument('--buckets',nargs='+',type=int,default=[112,96])
    parser.add_argument('--seconds',type=float,default=12)
    parser.add_argument('--mode',choices=['feasibility','maximize'],default='feasibility')
    args=parser.parse_args()
    base,coords=load_236()
    groups=choose_pools(base,coords,args.seed)
    print(json.dumps({'seed':args.seed,'baseline_verified':True,
                      'available_pools':{k:len(set(base)|v[3]) for k,v in groups.items()}}),flush=True)
    for k in args.buckets:
        if k not in groups:continue
        overlap,T,shift,G=groups[k]
        out=attempt(set(base)|G,args.seconds,args.mode)
        out.update({'selected_bucket':k,'overlap':overlap,
                    'affine_matrix':T,'translation':shift})
        print(json.dumps(out,sort_keys=True),flush=True)
        if out.get('disproves_r3_7_equals_236'):break

if __name__=='__main__':main()
