#!/usr/bin/env python3
"""Exact theorem: for an orthogonal pair A,B, a two-symbol swap within A
preserves Latin(A) and A orthogonal to B iff swapped cells form unions of connected
components in the graph induced by equal row, equal column, equal B-symbol
on the 20 A-entries having either swapped symbol.
Analogous for B; useful to navigate orthogonal-pair space safely.
"""
import itertools,collections,importlib.util,pathlib,json
D=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('e062',D/'E063_transversal_core.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def get_components(A,B,x,y):
 n=len(A);S=[(r,c) for r in range(n) for c in range(n) if A[r][c] in (x,y)]
 assert len(S)==2*n
 by=[collections.defaultdict(list) for k in range(3)]
 for i,(r,c) in enumerate(S):
  by[0][r].append(i);by[1][c].append(i);by[2][B[r][c]].append(i)
 for fam in by:
  assert len(fam)==n and all(len(v)==2 for v in fam.values())
 adj=[[] for _ in S]
 for fam in by:
  for u,v in fam.values():adj[u].append(v);adj[v].append(u)
 todo=set(range(len(S)));comps=[]
 while todo:
  st=todo.pop();q=[st];comp=[S[st]]
  while q:
   i=q.pop()
   for j in adj[i]:
    if j in todo:todo.remove(j);q.append(j);comp.append(S[j])
  comps.append(comp)
 return comps

def check_pair(label,A,B):
 assert m.validate(A,B)
 stat={'label':label,'A_symbolpair_components':{},'B_symbolpair_components':{},'orthogonal_trades':0,'best_found_pack':0,'best_total_transversals':0,'example':None,'exact_invariant':'Component union iff two-symbol A/B trade preserves Latin+orthogonality'}
 for side,(X,Y) in [('A',(A,B)),('B',(B,A))]:
  for x,y in itertools.combinations(range(10),2):
   comps=get_components(X,Y,x,y)
   key=f'{x},{y}';stat[side+'_symbolpair_components'][key]=len(comps)
   if len(comps)>1:
    for subset in range(1,(1<<len(comps))-1):
     Z=[row[:] for row in X]
     for i,comp in enumerate(comps):
      if subset>>i&1:
       for r,c in comp:Z[r][c]=y if Z[r][c]==x else x
     assert m.validate(Z,Y)
     t,_=m.exact_transversals(Z,Y)
     p=m.max_disjoint(Z,Y,t)
     stat['orthogonal_trades']+=1
     if p['best_found_pack']>stat['best_found_pack']:
      stat['best_found_pack']=p['best_found_pack'];stat['example']={'side':side,'pair':key,'subset':subset,'A':Z if side=='A' else Y,'B':Y if side=='A' else Z}
     stat['best_total_transversals']=max(stat['best_total_transversals'],len(t))
 sA=collections.Counter(stat['A_symbolpair_components'].values())
 sB=collections.Counter(stat['B_symbolpair_components'].values())
 print(label,'A_graph_comps',dict(sA),'B_graph_comps',dict(sB),'nontrivial_valid_trades',stat['orthogonal_trades'],'best_pack',stat['best_found_pack'],flush=True)
 return stat

def main():
 Q=json.load(open(D/'E063_SCHEINERMAN_PAIR.json'));A=Q['A'];B=Q['B']
 E=json.load(open(D/'E061_near_triple.json'))['squares']
 all={}
 for name,aa,bb in [('Egan_AB',E[0],E[1]),('Egan_AC',E[0],E[2]),('Scheinerman_AB',A,B)]:
  all[name]=check_pair(name,aa,bb)
 (D/'E063_COMPONENT_TRADE_GRAPH.json').write_text(json.dumps(all,indent=2)+'\n')

if __name__=='__main__':main()