#!/usr/bin/env python3
"""E027 exhaustive fixed-Q orthogonal mates, using exact-cover bitsets.
Input from E024_appendix_six_replay.py (BKS EJC 2026 Appendix).
No conclusion about other Q, Myrvold families, or unrestricted 3-MOLS(10).
"""
from E024_appendix_six_replay import RAW,parse,derive,latin
import json,hashlib,time

def trans(q):
 out=[]
 def visit(r,cm,sm,path):
  if r==10:out.append(tuple(path));return
  for c in range(10):
   if cm>>c&1 or sm>>q[r][c]&1:continue
   visit(r+1,cm|1<<c,sm|1<<q[r][c],path+(c,))
 visit(0,0,0,())
 return out

def common(a,q):
 out=[]
 def visit(r,cm,am,qm,path):
  if r==10:out.append(path);return
  for c in range(10):
   if cm>>c&1 or am>>a[r][c]&1 or qm>>q[r][c]&1:continue
   visit(r+1,cm|1<<c,am|1<<a[r][c],qm|1<<q[r][c],path+(c,))
 visit(0,0,0,0,())
 return out

def solve(label):
 p,q=map(parse,RAW[label]);z=derive(p,q)
 assert latin(p) and latin(q) and latin(z)
 assert len({(z[r][c],q[r][c]) for r in range(10) for c in range(10)})==100
 ts=trans(q);n=len(ts)
 masks=[sum(1<<(10*r+c) for r,c in enumerate(t)) for t in ts]
 bycell=[0]*100
 for j,t in enumerate(ts):
  for r,c in enumerate(t):bycell[10*r+c]|=1<<j
 conflicts=[]
 for t in ts:
  b=0
  for r,c in enumerate(t):b|=bycell[10*r+c]
  conflicts.append(b)
 original={tuple(next(c for c in range(10) if z[r][c]==s) for r in range(10)) for s in range(10)}
 nodes=0;solutions=[];start=time.monotonic()
 def visit(uncovered,eligible,chosen):
  nonlocal nodes
  nodes+=1
  if not uncovered:
   selected=[ts[j] for j in chosen]
   a=[[-1]*10 for _ in range(10)]
   for t in selected:
    for r,c in enumerate(t):a[r][c]=t[0]
   assert latin(a) and len({(a[r][c],q[r][c]) for r in range(10) for c in range(10)})==100
   w=common(a,q)
   solutions.append({'mate':a,'is_original':set(selected)==original,'common_transversals':len(w),'common_cell_support':len({10*r+c for t in w for r,c in enumerate(t)})})
   return
  options=0;few=n+1;u=uncovered
  while u:
   b=u&-u;u-=b;cell=b.bit_length()-1
   cand=bycell[cell]&eligible;k=cand.bit_count()
   if k<few:few=k;options=cand
   if k<=1:break
  while options:
   b=options&-options;options-=b;j=b.bit_length()-1
   visit(uncovered^masks[j],eligible&~conflicts[j],chosen+(j,))
 visit((1<<100)-1,(1<<n)-1,())
 assert sum(x['is_original'] for x in solutions)==1
 return {'label':label,'input_q_sha256':hashlib.sha256(json.dumps(q,separators=(',',':')).encode()).hexdigest(),'q_transversals':n,'dfs_nodes':nodes,'complete':True,'partitions':len(solutions),'new_mates':len(solutions)-1,'solutions':solutions,'elapsed_s':round(time.monotonic()-start,4)}

if __name__=='__main__':
 results={k:solve(k) for k in RAW}
 print(json.dumps(results,indent=2))
