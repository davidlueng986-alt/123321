#!/usr/bin/env python3
"""Construct third MOLS from (n-2) disjoint common transversals of A,B
iff the 2n-cell residual coincidence graph (row,col,A-symbol,B-symbol)
is bipartite. This is a theorem valid for any n and is a direct closure gate.
"""
import json,itertools,collections
from pathlib import Path
from E061_transversal_route import common_transversals, verify_pair,verify_triple,close_pair
N=Path(__file__).resolve().parent

def residual_graph(A,B,packed):
 verify_pair(A,B);n=len(A)
 occupied=set()
 for T in packed:
  assert len(T)==n and set(T)==set(range(n))
  assert len({A[r][T[r]] for r in range(n)})==n
  assert len({B[r][T[r]] for r in range(n)})==n
  for r,c in enumerate(T):
   assert (r,c) not in occupied
   occupied.add((r,c))
 assert len(packed)==n-2
 left=[(r,c) for r in range(n) for c in range(n) if (r,c) not in occupied]
 assert len(left)==2*n
 graph=[set() for _ in left];resources=collections.defaultdict(list)
 for i,(r,c) in enumerate(left):
  for k in ((0,r),(1,c),(2,A[r][c]),(3,B[r][c])):resources[k].append(i)
 assert len(resources)==4*n and all(len(v)==2 for v in resources.values())
 for u,v in resources.values():
  assert u!=v
  graph[u].add(v);graph[v].add(u)
 color=[None]*(2*n);components=0
 for start in range(2*n):
  if color[start] is not None:continue
  components+=1;color[start]=0;stack=[start]
  while stack:
   u=stack.pop()
   for v in graph[u]:
    if color[v] is None:color[v]=1-color[u];stack.append(v)
    elif color[v]==color[u]:return {'bipartite':False,'conflict_edge':[left[u],left[v]],'vertices':2*n,'components_started':components}
 tr=[None]*n
 for i,(r,c) in enumerate(left):
  if color[i]==0:
   assert tr[r] is None
   tr[r]=c
 assert all(x is not None for x in tr)
 triple,C=close_pair(A,B,packed+[tr]);assert triple==[n*n]*3
 return {'bipartite':True,'components':components,'vertices':2*n,'new_common_transversal':tr,'overlays':triple}

def run():
 controls=[]
 for x in map(json.loads,open(N/'E061_dlx_runs.jsonl')):
  if x['n'] not in (4,5):continue
  A,B,C=x['witness'];n=len(A)
  from_z=[[next(c for c in range(n) if C[r][c]==s) for r in range(n)] for s in range(n-2)]
  z=residual_graph(A,B,from_z)
  assert z['bipartite']
  controls.append({'n':n,'status':'CONSTRUCTIVE_CLOSURE_PASS',**z})
  all_tr,_=common_transversals(A,B)
  if n<=5:
   checked=0;nonbip=0
   for inds in itertools.combinations(range(len(all_tr)),n-2):
    sets=[{(r,c) for r,c in enumerate(all_tr[i])} for i in inds]
    if len(set().union(*sets))!=n*(n-2):continue
    check=residual_graph(A,B,[all_tr[i] for i in inds]);checked+=1
    if not check['bipartite']:nonbip+=1
   controls[-1].update(total_disjoint_n_minus_2_packs=checked,non_bipartite=nonbip)
 res={'status':'THEOREM_AND_POSITIVE_CONTROLS_VERIFIED','lemma':'for any orthogonal A,B, a set of n-2 disjoint common transversals extends to a full third square iff residual 2n-cell graph is bipartite','controls':controls,'order10_requirement':'Find ANY orthogonal pair with 8 disjoint common transversals AND bipartite residual graph; exact triple then follows','current_mols10_status':'OPEN'}
 (N/'E061_two_transversal_completion.json').write_text(json.dumps(res,indent=2)+'\n')
 print(json.dumps(res,indent=2))
if __name__=='__main__':run()