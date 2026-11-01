#!/usr/bin/env python3
"""E020: exact unary obstruction for a FIXED first Latin square A.
For each A-transversal U, test if an orthogonal mate C of A exists
whose every symbol class meets U exactly once. If not, U cannot be a
B-symbol class in any triple (A,B,C). Exhaustive per-root exact cover.
This does NOT decide unrestricted 3-MOLS(10).
"""
import argparse
import hashlib
import json
import time

PARKER_A = [
 [0,4,1,7,2,9,8,3,6,5],
 [8,1,5,2,7,3,9,4,0,6],
 [9,8,2,6,3,7,4,5,1,0],
 [5,9,8,3,0,4,7,6,2,1],
 [7,6,9,8,4,1,5,0,3,2],
 [6,7,0,9,8,5,2,1,4,3],
 [3,0,7,1,9,8,6,2,5,4],
 [1,2,3,4,5,6,0,7,8,9],
 [2,3,4,5,6,0,1,8,9,7],
 [4,5,6,0,1,2,3,9,7,8]
]

def transversals(a):
 n=len(a); out=[]
 assert all(set(row)==set(range(n)) for row in a)
 assert all({a[r][c] for r in range(n)}==set(range(n)) for c in range(n))
 def dfs(r,cols,syms,mask):
  if r==n:
   out.append(mask);return
  for c in range(n):
   if not(cols>>c&1 or syms>>a[r][c]&1):
    dfs(r+1,cols|1<<c,syms|1<<a[r][c],mask|1<<(n*r+c))
 dfs(0,0,0,0)
 return out

def prepare(a):
 n=len(a); T=transversals(a); cells=[0]*(n*n)
 for k,v in enumerate(T):
  for c in range(n*n):
   if v>>c&1:cells[c]|=1<<k
 disjoint=[];compatible=[]
 for v in T:
  disjoint.append(sum(1<<j for j,w in enumerate(T) if not(v&w)))
  compatible.append(sum(1<<j for j,w in enumerate(T) if (v&w).bit_count()==1))
 return T,cells,disjoint,compatible

def exact_cover(T,cells,disjoint,allowed,seconds=0.25,max_nodes=100000):
 allcells=(1<<len(cells))-1;start=time.monotonic();nodes=0;solution=[]
 class Budget(Exception):pass
 def dfs(used,eligible):
  nonlocal nodes
  if nodes>=max_nodes or time.monotonic()-start>seconds:raise Budget
  nodes+=1
  if used==allcells:return True
  remaining=allcells^used;best=None
  while remaining:
   bit=remaining&-remaining;remaining-=bit
   opts=cells[bit.bit_length()-1]&eligible
   if not opts:return False
   if best is None or opts.bit_count()<best.bit_count():best=opts
   if best.bit_count()==1:break
  while best:
   bit=best&-best;best-=bit;k=bit.bit_length()-1
   solution.append(k)
   if dfs(used|T[k],eligible&disjoint[k]):return True
   solution.pop()
  return False
 try:status='SAT' if dfs(0,allowed) else 'UNSAT_EXHAUSTIVE'
 except Budget:status='UNKNOWN_BUDGET';solution=[]
 return dict(status=status,nodes=nodes,seconds=round(time.monotonic()-start,4),
             selected_ids=solution if status=='SAT' else [])

def audit(a,limit=None,seconds=0.25,max_nodes=100000):
 start=time.monotonic();T,cells,disjoint,compatible=prepare(a)
 cases=[]
 for i in range(len(T) if limit is None else min(len(T),limit)):
  result=exact_cover(T,cells,disjoint,compatible[i],seconds,max_nodes)
  if result['status']=='SAT':
   ids=result['selected_ids']
   assert len(ids)==len(a)
   assert all(sum((T[k]>>c)&1 for k in ids)==1 for c in range(len(a)**2))
   assert all((T[k]&T[i]).bit_count()==1 for k in ids)
  cases.append(dict(root=i,allowed=compatible[i].bit_count(),**result))
 survivors=[x['root'] for x in cases if x['status']=='SAT']
 covered=[sum((T[i]>>c)&1 for i in survivors) for c in range(len(a)**2)]
 return dict(schema='MOLS10-E020-unary-v1',
  scope='Fixed first A only; necessary condition; no unrestricted proof',
  input_sha256=hashlib.sha256(json.dumps(a,separators=(',',':')).encode()).hexdigest(),
  transversals=len(T),roots_tested=len(cases),
  status_counts={s:sum(x['status']==s for x in cases)
    for s in ['SAT','UNSAT_EXHAUSTIVE','UNKNOWN_BUDGET']},
  surviving_roots=survivors,uncovered_cells=[c for c,v in enumerate(covered) if v==0],
  total_nodes=sum(x['nodes'] for x in cases),
  total_seconds=round(time.monotonic()-start,3),cases=cases)

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--limit',type=int,default=None)
 p.add_argument('--seconds',type=float,default=0.25)
 p.add_argument('--nodes',type=int,default=100000)
 p.add_argument('--output',default='E020_RESULTS.json')
 args=p.parse_args()
 r=audit(PARKER_A,args.limit,args.seconds,args.nodes)
 with open(args.output,'w') as f:json.dump(r,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in r.items() if k!='cases'},indent=2))
