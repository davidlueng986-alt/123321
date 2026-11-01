#!/usr/bin/env python3
"""Independent E017 audit: n! permutation enumeration + exact-cover B DFS.
UNSAT excludes only the supplied first Latin square A, not all 3-MOLS(10).
Requires only Python stdlib and the repository's two published input JSONs.
"""
import argparse, hashlib, itertools, json, random, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def latin(A):
 n=len(A);s=set(range(n))
 return len(A)==n and all(len(row)==n and set(row)==s for row in A) and all({A[r][c] for r in range(n)}==s for c in range(n))

def digest(A):return hashlib.sha256(json.dumps(A,separators=(',',':')).encode()).hexdigest()

def transversals(A):
 n=len(A)
 assert latin(A)
 return [p for p in itertools.permutations(range(n)) if len({A[r][p[r]] for r in range(n)})==n]

def two_symbol_trades(A):
 """Independent cycle-based enumeration; deterministic p,q and smallest row ordering."""
 n=len(A);out=[]
 for p in range(n):
  for q in range(p+1,n):
   cp=[row.index(p) for row in A];cq=[row.index(q) for row in A]
   inverse={cq[r]:r for r in range(n)};unseen=set(range(n));cycles=[]
   while unseen:
    r=min(unseen);cycle=[]
    while r in unseen:
     unseen.remove(r);cycle.append(r);r=inverse[cp[r]]
    cycles.append(cycle)
   for cycle in cycles[:-1]:
    B=[row.copy() for row in A];cells=[]
    for r in cycle:
     x,y=cp[r],cq[r];B[r][x],B[r][y]=B[r][y],B[r][x]
     cells.extend([(r,x),(r,y)])
    assert latin(B)
    out.append({'square':B,'symbols':[p,q],'size':len(cells),'cells':cells})
 return out

def audit(A,seed=17,max_nodes=500000,max_seconds=30):
 start=time.monotonic();n=len(A);T=transversals(A);m=len(T)
 masks=[sum(1<<(n*r+p[r]) for r in range(n)) for p in T]
 at=[0]*(n*n)
 for k,p in enumerate(T):
  for r,c in enumerate(p):at[n*r+c]|=1<<k
 compatible=[];disjoint=[]
 for mask in masks:
  cm=dm=0
  for k,v in enumerate(masks):
   hits=(mask&v).bit_count()
   if hits==1:cm|=1<<k
   elif hits==0:dm|=1<<k
  compatible.append(cm);disjoint.append(dm)
 setup=time.monotonic()-start
 rng=random.Random(seed);order=list(range(m));rng.shuffle(order);rank=[0]*m
 for pos,k in enumerate(order):rank[k]=pos
 nodes=pruned=dead=0;chosen=[];allcells=(1<<(n*n))-1
 class Budget(Exception):pass
 def dfs(used,eligible,possible):
  nonlocal nodes,pruned,dead
  if nodes>=max_nodes or time.monotonic()-start>max_seconds:raise Budget
  nodes+=1
  if any(not (possible&refs) for refs in at):pruned+=1;return None
  if used==allcells:return chosen.copy()
  remaining=allcells^used;best=None
  while remaining:
   bit=remaining&-remaining;remaining^=bit
   opts=at[bit.bit_length()-1]&eligible
   if not opts:dead+=1;return None
   if best is None or opts.bit_count()<best.bit_count():best=opts
   if best.bit_count()==1:break
  options=[]
  while best:
   bit=best&-best;best^=bit;options.append(bit.bit_length()-1)
  options.sort(key=lambda k:rank[k])
  for k in options:
   chosen.append(k)
   result=dfs(used|masks[k],eligible&disjoint[k],possible&compatible[k])
   if result is not None:return result
   chosen.pop()
  return None
 try:
  selected=dfs(0,(1<<m)-1,(1<<m)-1)
  status='SAT_SUPPORT_ONLY' if selected is not None else 'UNSAT_FIXED_A_EXHAUSTIVE'
 except Budget:selected=None;status='UNKNOWN_BUDGET'
 return {'status':status,'sha256':digest(A),'transversals':m,'nodes':nodes,
         'pruned_support':pruned,'dead_end':dead,'setup_seconds':round(setup,4),
         'total_seconds':round(time.monotonic()-start,4),
         'seed':seed,'node_budget':max_nodes,'seconds_budget':max_seconds,
         'selected_ids':selected}

def cases():
 E=json.loads((ROOT/'near_triple.json').read_text())['squares'][0]
 P=json.loads((ROOT/'parker_pair.json').read_text())['squares'][0]
 assert latin(E) and latin(P)
 et=two_symbol_trades(E);pt=two_symbol_trades(P)
 assert len(et)==48 and len(pt)==66
 # 4 new disjoint Egan two-trades; not among original + 48 single trades.
 known={digest(E)}|{digest(t['square']) for t in et}
 pairs=[];seen=set(known)
 for i in range(len(et)):
  for j in range(i+1,len(et)):
   if set(et[i]['cells'])&set(et[j]['cells']):continue
   B=[row.copy() for row in E]
   for t in (et[i],et[j]):
    x,y=t['symbols']
    for r,c in t['cells']:B[r][c]=y if B[r][c]==x else x
   assert latin(B)
   h=digest(B)
   if h not in seen:seen.add(h);pairs.append((i,j,B))
 return E,P,et,pt,pairs

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',default='E017_REPLAY_RESULTS.json');ap.add_argument('--seconds',type=float,default=30);ap.add_argument('--nodes',type=int,default=500000);args=ap.parse_args()
 E,P,et,pt,pairs=cases();inputs={'Egan_A':E,'Parker_A':P,'Egan_trade12':et[12]['square']}
 for k in [0,1,2,3]:inputs[f'Egan_disjoint_two_trade_{k}_{pairs[k][0]}_{pairs[k][1]}']=pairs[k][2]
 for k in [0,1,2,3,10,15,20,30,40,50,60,65]:inputs[f'Parker_trade_{k}']=pt[k]['square']
 result={'schema':'MOLS10-E017-v1','first_squares':{},'counts':{'Egan_one_trades':len(et),'Parker_one_trades':len(pt),'Egan_two_trade_distinct_labeled':len(pairs)},'scope':'Fixed-A only; no unrestricted proof'}
 for name,A in inputs.items():
  r=audit(A,max_nodes=args.nodes,max_seconds=args.seconds)
  result['first_squares'][name]=r
  print(name,r['status'],r['transversals'],r['nodes'],r['pruned_support'],flush=True)
 Path(args.output).write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
