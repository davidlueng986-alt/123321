#!/usr/bin/env python3
"""Independent exact 3-color CSP enumeration for E026 (no MILP backend).
A 3-symbol trade preserving orthogonality with Q is exactly a proper
3-coloring of each 3-edge row, column, and Q-symbol fiber. Normalize row0.
"""
import itertools, json
from E024_appendix_six_replay import RAW, parse, derive, latin

def count_normalized(z,q,S):
 n=len(z);cells=[(r,c) for r in range(n) for c in range(n) if z[r][c] in S]
 assert len(cells)==3*n
 groups=[]
 for d in range(3):
  for v in range(n):
   g=[i for i,(r,c) in enumerate(cells) if (r,c,q[r][c])[d]==v]
   assert len(g)==3
   groups.append(g)
 original=[S.index(z[r][c]) for r,c in cells]
 dom=[7]*len(cells)
 for i,(r,c) in enumerate(cells):
  if r==0:dom[i]=1<<original[i]
 def propagate(a):
  again=True
  while again:
   again=False
   for g in groups:
    used=0
    for i in g:
     x=a[i]
     if x&(x-1)==0:
      if used&x:return False
      used|=x
    for i in g:
     if a[i]&(a[i]-1):
      new=a[i]&~used
      if not new:return False
      if new!=a[i]:a[i]=new;again=True
    for bit in (1,2,4):
     possible=[i for i in g if a[i]&bit]
     if not possible:return False
     if len(possible)==1 and a[possible[0]]!=bit:
      a[possible[0]]=bit;again=True
  return True
 solutions=[0];new=[0];nodes=[0]
 def dfs(a):
  nodes[0]+=1
  if not propagate(a):return
  pending=[i for i,x in enumerate(a) if x&(x-1)]
  if not pending:
   solutions[0]+=1
   if any(a[i]!=(1<<original[i]) for i in range(len(a))):new[0]+=1
   return
  i=min(pending,key=lambda i:a[i].bit_count())
  for bit in (1,2,4):
   if a[i]&bit:
    b=a.copy();b[i]=bit;dfs(b)
 dfs(dom)
 return solutions[0],new[0],nodes[0]

def main():
 out={}
 for label,(pstr,qstr) in RAW.items():
  p,q=map(parse,(pstr,qstr));z=derive(p,q)
  assert latin(p) and latin(q) and latin(z)
  counts={'triples':0,'nodes':0,'normalized_solutions':0,'nontrivial':0,'exceptions':[]}
  for triple in itertools.combinations(range(10),3):
   sol,nontrivial,nodes=count_normalized(z,q,list(triple))
   counts['triples']+=1;counts['nodes']+=nodes
   counts['normalized_solutions']+=sol;counts['nontrivial']+=nontrivial
   if sol!=1 or nontrivial:counts['exceptions'].append([triple,sol,nontrivial])
  out[label]=counts;print(label,counts,flush=True)
 with open('E026_DFS_RESULTS.json','w') as f:json.dump(out,f,indent=2)
if __name__=='__main__':main()
