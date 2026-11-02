#!/usr/bin/env python3
"""E027 independent replay: separate transversal recursion and mutable Algorithm X cover/uncover."""
from E024_appendix_six_replay import RAW,parse,latin
import json

def solve(label):
 _,q=map(parse,RAW[label]);assert latin(q)
 ts=[]
 def tr(r,cols,syms,path):
  if r==10:ts.append(path);return
  for c in range(10):
   if c not in cols and q[r][c] not in syms:tr(r+1,cols|{c},syms|{q[r][c]},path+(c,))
 tr(0,set(),set(),())
 rows=[tuple(10*r+c for r,c in enumerate(t)) for t in ts]
 cols={cell:set() for cell in range(100)}
 for i,rr in enumerate(rows):
  for cell in rr:cols[cell].add(i)
 def select(i):
  removed=[]
  for c in rows[i]:
   for j in list(cols[c]):
    for k in rows[j]:
     if k!=c and k in cols:cols[k].discard(j)
   removed.append((c,cols.pop(c)))
  return removed
 def undo(removed):
  for c,rr in reversed(removed):
   cols[c]=rr
   for j in rr:
    for k in rows[j]:
     if k!=c and k in cols:cols[k].add(j)
 solutions=[];nodes=0
 def visit(chosen):
  nonlocal nodes
  nodes+=1
  if not cols:
   a=[[-1]*10 for _ in range(10)]
   for j in chosen:
    for r,c in enumerate(ts[j]):a[r][c]=ts[j][0]
   assert latin(a) and len({(a[r][c],q[r][c]) for r in range(10) for c in range(10)})==100
   solutions.append(a);return
  c=min(cols,key=lambda k:len(cols[k]))
  for i in list(cols[c]):
   removed=select(i);visit(chosen+(i,));undo(removed)
 visit(())
 return {'label':label,'q_transversals':len(ts),'nodes':nodes,'partitions':len(solutions),'mates':solutions,'complete':True}

if __name__=='__main__':print(json.dumps({k:solve(k) for k in RAW},indent=2))
