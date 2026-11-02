#!/usr/bin/env python3
"""Independent randomized valid k4 MOLR prefixes; LP is only a necessary condition.
Deterministic seed, bounded row DFS; every reported sample independently checked.
"""
import random, time, json, hashlib, argparse
from scipy.optimize import linprog
from E035_column_residual import model
import numpy as np
N=10

def valid(S):
 k=len(S[0]); assert len(S)==3
 for a in S:
  assert len(a)==k
  for row in a:assert sorted(row)==list(range(N))
  for c in range(N):assert len({a[r][c] for r in range(k)})==k
 for i,j in [(0,1),(0,2),(1,2)]:
  assert len({(S[i][r][c],S[j][r][c]) for r in range(k) for c in range(N)})==N*k

def add_row(S,rng,max_nodes=30000):
 k=len(S[0]);used_cols=[[{S[s][r][c] for r in range(k)} for c in range(N)] for s in range(3)]
 used_pairs=[{(S[i][r][c],S[j][r][c]) for r in range(k) for c in range(N)} for i,j in [(0,1),(0,2),(1,2)]]
 opts=[]
 for c in range(N):
  v=[]
  for a in range(N):
   if a in used_cols[0][c]:continue
   for b in range(N):
    if b in used_cols[1][c] or (a,b) in used_pairs[0]:continue
    for d in range(N):
     if d in used_cols[2][c] or (a,d) in used_pairs[1] or (b,d) in used_pairs[2]:continue
     v.append((a,b,d))
  rng.shuffle(v);opts.append(v)
 filled=[None]*N;seen=[set(),set(),set()];pnew=[set(),set(),set()];nodes=[0]
 def dfs(left):
  nodes[0]+=1
  if nodes[0]>max_nodes:return False
  if not left:return True
  best=None;best_opts=None
  for c in left:
   o=[t for t in opts[c] if all(t[s] not in seen[s] for s in range(3)) and (t[0],t[1]) not in pnew[0] and (t[0],t[2]) not in pnew[1] and (t[1],t[2]) not in pnew[2]]
   if not o:return False
   if best_opts is None or len(o)<len(best_opts):best=c;best_opts=o
  for t in best_opts:
   filled[best]=t
   pairs=((t[0],t[1]),(t[0],t[2]),(t[1],t[2]))
   for s in range(3):seen[s].add(t[s]);pnew[s].add(pairs[s])
   if dfs([c for c in left if c!=best]):return True
   for s in range(3):seen[s].remove(t[s]);pnew[s].remove(pairs[s])
  filled[best]=None;return False
 if not dfs(list(range(N))):return None,nodes[0]
 R=[[filled[c][s] for c in range(N)] for s in range(3)]
 out=[S[s]+[R[s]] for s in range(3)]
 valid(out)
 return out,nodes[0]

def random_second(rng):
 perms=[]
 for s in range(3):
  for _ in range(50000):
   p=list(range(N));rng.shuffle(p)
   if all(p[c]!=c and all(p[c]!=q[c] for q in perms) for c in range(N)):
    perms.append(p);break
  else:raise RuntimeError('failed second row')
 S=[ [list(range(N)),p] for p in perms];valid(S);return S

def run(seed=20261102,attempts=30,seconds=100):
 rng=random.Random(seed);t0=time.monotonic();out=[];fails=[];distinct=set();summary={}
 for i in range(attempts):
  if time.monotonic()-t0>seconds:break
  S=random_second(rng);n=[];ok=True
  for k in (2,3):
   S,z=add_row(S,rng,12000);n.append(z)
   if S is None:ok=False;break
  if not ok:
   fails.append({'attempt':i,'nodes':n,'reason':'bounded DFS failure (not UNSAT)'})
   continue
  h=hashlib.sha256(json.dumps(S,separators=(',',':')).encode()).hexdigest()
  if h in distinct:continue
  distinct.add(h)
  A,T,E=model(S);zero=int(sum(np.diff(A.indptr)==0));row={'attempt':i,'sha256':h,'nodes':n,'variables':len(T),'zero_support':zero,'prefix':S}
  if zero:row['lp']='EXACT_ZERO_SUPPORT'
  else:
   z=linprog(np.zeros(len(T)),A_eq=A,b_eq=np.ones(A.shape[0]),bounds=(0,1),method='highs',options={'time_limit':4})
   row['lp']={0:'NUMERIC_FEASIBLE',1:'UNKNOWN_TIME',2:'NUMERIC_INFEASIBLE',3:'UNBOUNDED',4:'ERROR'}[z.status]
   if z.x is not None:row['residual_max_abs_error']=float(max(abs(A@z.x-1)))
  summary[row['lp']]=summary.get(row['lp'],0)+1
  out.append(row)
  print('case',i,'nodes',n,'candidates',len(T),'zero',zero,'LP',row['lp'],flush=True)
 result={'seed':seed,'attempts_completed':i+1,'successes':len(out),'failures':fails,'summary':summary,'seconds':round(time.monotonic()-t0,3),'cases':out,'limits':{'per_row_dfs_nodes':12000,'lp_seconds':4,'overall_seconds':seconds}}
 with open('E044_RESULTS.json','w') as f:json.dump(result,f,indent=2)
 print('SUMMARY',json.dumps({k:v for k,v in result.items() if k!='cases' and k!='failures'}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--attempts',type=int,default=30);p.add_argument('--seconds',type=int,default=100);p.add_argument('--seed',type=int,default=20261102);a=p.parse_args();run(a.seed,a.attempts,a.seconds)
