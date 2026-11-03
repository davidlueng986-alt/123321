#!/usr/bin/env python3
"""Exact 2-MOLS + (n-1) disjoint common transversals => 3-MOLS.
This is an EQUIVALENCE: any full triple's C-symbol classes yield the packing.
The omitted final transversal is the complement of the first n-1.
No claim of a 3-MOLS(10) witness unless n=10 and validation passes.
"""
import json,collections,itertools
from pathlib import Path
N=Path(__file__).resolve().parent

def verify_pair(A,B):
 n=len(A);symbols=set(range(n))
 for Q in [A,B]:
  assert len(Q)==n and all(len(row)==n and set(row)==symbols for row in Q)
  assert all({Q[r][c] for r in range(n)}==symbols for c in range(n))
 assert len({(A[r][c],B[r][c]) for r in range(n) for c in range(n)})==n*n

def verify_triple(S):
 assert len(S)==3
 for i,j in ((0,1),(0,2),(1,2)):verify_pair(S[i],S[j])
 return [len({(S[i][r][c],S[j][r][c]) for r in range(len(S[0])) for c in range(len(S[0]))}) for i,j in ((0,1),(0,2),(1,2))]

def common_transversals(A,B):
 n=len(A);vec=[0]*n;out=[];nodes=0
 def rec(r,cm,am,bm):
  nonlocal nodes
  nodes+=1
  if r==n:out.append(tuple(vec));return
  for c in range(n):
   a,b=A[r][c],B[r][c]
   if cm>>c&1 or am>>a&1 or bm>>b&1:continue
   vec[r]=c;rec(r+1,cm|1<<c,am|1<<a,bm|1<<b)
 rec(0,0,0,0)
 return out,nodes

def maxpack(trs,n):
 masks=[sum(1<<(r*n+c) for r,c in enumerate(T)) for T in trs]
 best=[]
 def dfs(i,picked,used):
  nonlocal best
  if len(picked)>len(best):best=picked[:]
  if len(picked)+(len(trs)-i)<=len(best):return
  if i==len(trs):return
  if not used & masks[i]:dfs(i+1,picked+[i],used|masks[i])
  dfs(i+1,picked,used)
 dfs(0,[],0)
 return best

def close_pair(A,B,transversals):
 verify_pair(A,B);n=len(A);assert len(transversals)==n-1
 symbols=set(range(n));C=[[-1]*n for _ in range(n)];seen=set()
 for label,T in enumerate(transversals):
  assert len(T)==n and set(T)==symbols
  assert len({A[r][T[r]] for r in range(n)})==n
  assert len({B[r][T[r]] for r in range(n)})==n
  for r,c in enumerate(T):
   assert (r,c) not in seen;seen.add((r,c));C[r][c]=label
 left=[(r,c) for r in range(n) for c in range(n) if C[r][c]<0]
 assert len(left)==n
 for r,c in left:C[r][c]=n-1
 return verify_triple([A,B,C]),C

def run():
 out=[]
 # n4,n5 positive controls from independent complete OA-DLX witness.
 for s in map(json.loads,open(N/'E061_dlx_runs.jsonl')):
  if s['n'] not in (4,5):continue
  A,B,C=s['witness'];overlays=verify_triple([A,B,C]);n=len(A)
  trs=[[next(c for c in range(n) if C[r][c]==label) for r in range(n)] for label in range(n-1)]
  cls,recovered=close_pair(A,B,trs)
  assert cls==overlays==[n*n]*3
  out.append({'n':n,'positive':True,'supplied':n-1,'verified_complement':True,'overlays':cls})
 # n10 Egan-Wanless published pair; known 14 transversals, at most 7 disjoint
 D=json.load(open(N/'E061_near_triple.json'))['squares'];A,B=D[0],D[1]
 verify_pair(A,B)
 trs,nodes=common_transversals(A,B);best=maxpack(trs,10)
 assert len(trs)==14 and len(best)==7,(len(trs),len(best))
 out.append({'n':10,'pair':'Egan-Wanless near triple A/B (2016)','common_transversals':len(trs),'max_disjoint':len(best),'n_minus_1_needed':9,'closure':False,'enumeration_nodes':nodes})
 result={'criterion':'n-1 disjoint common transversals in an orthogonal Latin pair iff a complete triple exists; tenth is forced complement','controls':out,'global_order10_status':'OPEN'}
 (N/'E061_transversal_route.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
 return result
if __name__=='__main__':run()