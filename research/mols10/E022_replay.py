#!/usr/bin/env python3
"""E022 fixed-Egan-A unary/pair-root C exact-cover replay (stdlib).
UNSAT is reported only on exhaustive completion; cap exhaustion is UNKNOWN.
This is NOT a solution of unrestricted 3-MOLS(10).
"""
import itertools, json, argparse, hashlib, time
A=[[0,8,9,7,5,6,4,2,3,1],[9,1,4,6,2,7,3,8,0,5],
[7,4,2,5,1,3,8,6,9,0],[8,6,5,3,9,2,1,0,4,7],
[6,2,1,8,4,0,9,5,7,3],[4,9,3,2,7,5,0,1,6,8],
[5,3,7,1,0,8,6,9,2,4],[3,5,0,9,8,4,2,7,1,6],
[1,7,6,0,3,9,5,4,8,2],[2,0,8,4,6,1,7,3,5,9]]
FULL=(1<<100)-1

def prepare():
 assert all(sorted(row)==list(range(10)) for row in A)
 assert all(sorted(A[r][c] for r in range(10))==list(range(10)) for c in range(10))
 T=[sum(1<<(10*r+p[r]) for r in range(10))
    for p in itertools.permutations(range(10))
    if len({A[r][p[r]] for r in range(10)})==10]
 cell=[0]*100
 for i,t in enumerate(T):
  m=t
  while m:
   b=m&-m;m-=b;cell[b.bit_length()-1]|=1<<i
 disjoint=[]
 for t in T:
  blocked=0;m=t
  while m:
   b=m&-m;m-=b;blocked|=cell[b.bit_length()-1]
  disjoint.append(((1<<len(T))-1)^blocked)
 return T,cell,disjoint

def cover(T,cell,disjoint,roots,cap):
 eligible=0
 for i,t in enumerate(T):
  if all((t&T[r]).bit_count()==1 for r in roots):eligible|=1<<i
 nodes=0;failed=set();path=[]
 class Limit(Exception):pass
 def dfs(remaining,avail):
  nonlocal nodes
  if not remaining:return True
  if remaining in failed:return False
  nodes+=1
  if nodes>cap:raise Limit
  best=None;m=remaining
  while m:
   b=m&-m;m-=b;options=cell[b.bit_length()-1]&avail
   if not options:failed.add(remaining);return False
   if best is None or options.bit_count()<best.bit_count():best=options
   if best.bit_count()==1:break
  while best:
   b=best&-best;best-=b;i=b.bit_length()-1
   path.append(i)
   if dfs(remaining^T[i],avail&disjoint[i]):return True
   path.pop()
  failed.add(remaining);return False
 try:status='SAT' if dfs(FULL,eligible) else 'UNSAT_EXHAUSTIVE'
 except Limit:status='UNKNOWN_BUDGET';path=[]
 if status=='SAT':
  assert len(path)==10 and sum(T[i] for i in path)==FULL
  assert all(all((T[i]&T[r]).bit_count()==1 for r in roots) for i in path)
 return status,nodes,path

def main():
 p=argparse.ArgumentParser();p.add_argument('--cap',type=int,default=20000)
 p.add_argument('--out',default='E022_REPLAY.json');args=p.parse_args()
 start=time.monotonic();T,cell,disjoint=prepare()
 unary=[];unknown_unary=[]
 for i in range(len(T)):
  status,_,_=cover(T,cell,disjoint,(i,),args.cap)
  if status=='SAT':unary.append(i)
  if status=='UNKNOWN_BUDGET':unknown_unary.append(i)
 pairs=[(i,j) for k,i in enumerate(unary) for j in unary[k+1:] if not(T[i]&T[j])]
 counts={};sat={};unsat=[];unknown=[];nodes=0;maxnodes=0
 for i,j in pairs:
  status,n,path=cover(T,cell,disjoint,(i,j),args.cap)
  counts[status]=counts.get(status,0)+1;nodes+=n;maxnodes=max(maxnodes,n)
  if status=='SAT':sat[f'{i},{j}']=path
  elif status=='UNSAT_EXHAUSTIVE':unsat.append([i,j])
  else:unknown.append([i,j])
 surviving=sorted({i for key in sat for i in map(int,key.split(','))})
 covered=0
 for i in surviving:covered|=T[i]
 out=dict(schema='MOLS10-E022-stdlib-v1',
   input_sha256=hashlib.sha256(json.dumps(A,separators=(',',':')).encode()).hexdigest(),
   transversal_count=len(T),unary_survivors=unary,unary_unknown=unknown_unary,
   pair_count=len(pairs),pair_status=counts,sat_witnesses=sat,
   unsat_pairs=unsat,unknown_pairs=unknown,pair_nodes=nodes,max_nodes=maxnodes,
   surviving_pair_roots=surviving,
   uncovered_cells=[i for i in range(100) if not(covered>>i&1)],
   cap=args.cap,seconds=round(time.monotonic()-start,3),
   scope='fixed Egan A only; not unrestricted 3-MOLS(10)')
 with open(args.out,'w') as f:json.dump(out,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ('unary_survivors','sat_witnesses','unsat_pairs','unknown_pairs')},indent=2))
if __name__=='__main__':main()
