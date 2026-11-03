#!/usr/bin/env python3
from pathlib import Path
"""Goal-backward: refute even the stronger universal k4 INTEGRAL
column-aware residual obstruction using four disjoint common transversals
of Egan-Wanless order-10 MOLS A,B. Independently check 360 exact equations.
Does NOT construct three full MOLS(10): the remaining 60 placements are
NOT partitioned into six compatible future rows.
"""
import json,itertools,collections,hashlib
A=[[0,8,9,7,5,6,4,2,3,1],[9,1,4,6,2,7,3,8,0,5],[7,4,2,5,1,3,8,6,9,0],[8,6,5,3,9,2,1,0,4,7],[6,2,1,8,4,0,9,5,7,3],[4,9,3,2,7,5,0,1,6,8],[5,3,7,1,0,8,6,9,2,4],[3,5,0,9,8,4,2,7,1,6],[1,7,6,0,3,9,5,4,8,2],[2,0,8,4,6,1,7,3,5,9]]
B=[[0,7,8,9,1,2,3,4,5,6],[9,0,6,1,8,3,2,5,4,7],[7,2,0,4,3,9,1,8,6,5],[8,5,3,0,2,1,7,6,9,4],[6,9,5,3,0,7,4,2,1,8],[4,1,7,6,5,0,8,9,3,2],[5,4,2,8,9,6,0,3,7,1],[3,6,1,7,4,8,5,0,2,9],[1,8,4,2,6,5,9,7,0,3],[2,3,9,5,7,4,6,1,8,0]]
n=10
for M in (A,B):
 assert all(sorted(x)==list(range(n)) for x in M)
 assert all(sorted(M[r][c] for r in range(n))==list(range(n)) for c in range(n))
assert len({(A[r][c],B[r][c]) for r in range(n) for c in range(n)})==100
# Each solution represents one cell per row, column, A symbol and B symbol.
trs=[];cols=[-1]*n;nodes=0
def rec(r,cm,am,bm):
 global nodes
 nodes+=1
 if r==n:
  trs.append(tuple(cols));return
 for c in range(n):
  if cm>>c&1:continue
  a,b=A[r][c],B[r][c]
  if am>>a&1 or bm>>b&1:continue
  cols[r]=c
  rec(r+1,cm|1<<c,am|1<<a,bm|1<<b)
rec(0,0,0,0)
print('common transversals',len(trs),'dfs',nodes,flush=True)
masks=[sum(1<<(r*n+c) for r,c in enumerate(T)) for T in trs]
def packing(t,left,chosen):
 if len(chosen)>=left:return chosen[:]
 for i in range(t,len(trs)):
  if all(masks[i]&masks[j]==0 for j in chosen):
   a=packing(i+1,left,chosen+[i])
   if a is not None:return a
 return None
pick=packing(0,4,[])
assert pick is not None,'could not find four disjoint common transversals'
# Construct partial 3-Latin-rectangle over NEW row=t and col=old column.
S=[ [[-1]*n for _ in range(4)] for __ in range(3)]
chosen_cells=set()
for t,ix in enumerate(pick):
 for r,c in enumerate(trs[ix]):
  assert (r,c) not in chosen_cells
  chosen_cells.add((r,c))
  S[0][t][c]=r;S[1][t][c]=A[r][c];S[2][t][c]=B[r][c]
assert len(chosen_cells)==40
for U in S:
 assert all(sorted(row)==list(range(n)) for row in U)
 assert all(len({U[r][c] for r in range(4)})==4 for c in range(n))
for i,j in ((0,1),(0,2),(1,2)):
 assert len({(S[i][r][c],S[j][r][c]) for r in range(4) for c in range(n)})==40
# Remaining 60 *integer* placements from Egan OA(100,4,10,2).
remaining=[(c,r,A[r][c],B[r][c]) for r in range(n) for c in range(n) if (r,c) not in chosen_cells]
assert len(remaining)==60
P=((0,1),(0,2),(1,2));used=[];needed=set()
for t,(i,j) in enumerate(P):
 used.append({(S[i][r][c],S[j][r][c]) for r in range(4) for c in range(n)})
 for a in range(n):
  for b in range(n):
   if (a,b) not in used[-1]:needed.add(('P',t,a,b))
for s in range(3):
 for c in range(n):
  for v in range(n):
   if v not in {S[s][r][c] for r in range(4)}:needed.add(('C',s,c,v))
assert len(needed)==360
actual=collections.Counter()
for c,a,b,d in remaining:
 for e in [('P',0,a,b),('P',1,a,d),('P',2,b,d),('C',0,c,a),('C',1,c,b),('C',2,c,d)]:
  assert e in needed
  actual[e]+=1
assert set(actual)==needed and all(x==1 for x in actual.values())
# Prove this fixed PAIR can't yield 10 disjoint transversals via complete 14 enumeration.
maxpack=0
for k in range(len(trs),0,-1):
 if packing(0,k,[]) is not None:
  maxpack=k;break
assert maxpack<10
out={'status':'EXACT_INTEGRAL_K4_RESIDUAL_COUNTEREXAMPLE','source':'Egan-Wanless near-triple A,B (2016)',
     'A':A,'B':B,'common_transversals':len(trs),'maximum_disjoint_common_transversals':maxpack,
     'search_nodes':nodes,'four_disjoint_transversal_indices':pick,'four_transversals':[trs[x] for x in pick],
     'prefix':S,'remaining_integer_placements':remaining,'verified_exact_constraints':360,
     'scope':'Refutes universal four-row INTEGER column-aware residual infeasibility, NOT full 3-MOLS(10)'}
print(json.dumps({k:v for k,v in out.items() if k not in ('A','B','four_transversals','prefix','remaining_integer_placements')},indent=2),flush=True)
with open(str(Path(__file__).with_name('E059_INTEGRAL_PRIMAL_WITNESS.json')),'w') as f:json.dump(out,f,indent=2)
