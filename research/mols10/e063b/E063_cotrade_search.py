#!/usr/bin/env python3
"""Closure-directed 2-MOLS(10) paired symbol cycle trade search.
Find all nontrivial one-cycle or same-symbol-pair multi-cycle trades of Egan's A and B,
including simultaneous trades on both; keep only exactly orthogonal pairs, seek 8-pack.
Bounded *trade-neighborhood* only; no unrestricted inference.
"""
import json,collections,itertools,hashlib,time,pathlib,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('e062',D/'E063_transversal_core.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
N=10

def twosym_component_trades(S):
 assert m.validate(S,S) is False # overlay of a square against itself nonorthogonal
 n=len(S); moves=[];seen=set();symbols=range(n)
 for x in symbols:
  for y in range(x+1,n):
   pos={(r,c) for r in range(n) for c in range(n) if S[r][c] in (x,y)}
   # Graph on selected cells: connected when sharing a row or column.
   todo=set(pos);comps=[]
   while todo:
    start=next(iter(todo));q=[start];todo.remove(start);comp=[start]
    while q:
     r,c=q.pop();near=[p for p in todo if p[0]==r or p[1]==c]
     for p in near:todo.remove(p);q.append(p);comp.append(p)
    comps.append(comp)
   assert sum(len(c) for c in comps)==2*n
   # All nonempty proper unions of components, or one full component if there is only 1,
   # but a full-cycle exchange is global symbol renaming and excluded.
   if len(comps)<=1:continue
   for subset in range(1,(1<<len(comps))-1):
    cells=[(r,c) for i,comp in enumerate(comps) if subset>>i&1 for r,c in comp]
    cand=[row[:] for row in S]
    for r,c in cells:cand[r][c]=y if cand[r][c]==x else x
    key=tuple(v for row in cand for v in row)
    if key not in seen:
     seen.add(key);moves.append((cand,{'symbols':[x,y],'components':len(comps),'subset':subset,'cells_changed':len(cells)}))
 return moves

def ov(A,B):
 seen=set()
 for r in range(N):
  for c in range(N):
   z=(A[r][c],B[r][c]);
   if z in seen:return False
   seen.add(z)
 return len(seen)==100

def visit_pair(A,B,desc,best,stats):
 if not ov(A,B):return best
 stats['orthogonal_pairs_found']+=1
 assert m.validate(A,B)
 t,n=m.exact_transversals(A,B);r=m.max_disjoint(A,B,t,node_cap=200000)
 maxk=r['best_found_pack'];stats['max_pack_found']=max(stats['max_pack_found'],maxk)
 if len(t)>stats['max_transversal_count']:
  stats['max_transversal_count']=len(t);stats['top_transversal_source']=desc
 if maxk>=8:
  stats['eight_pack_pairs']+=1
 if r['closure_found']:
  stats['verified_full_solution']=m.build_full(A,B,t,r)
  stats['closed_source']=desc
 stats['valid_pair_records'].append({'source':desc,'transversals':len(t),'max_pack':maxk,'nodes':r['search_nodes'],'closure':r['closure_found']})
 return max(best,maxk)

def main():
 S=json.load(open(D/'E061_near_triple.json'))['squares'];A,B=S[0],S[1]
 assert m.validate(A,B)
 a=twosym_component_trades(A);b=twosym_component_trades(B)
 t0=time.monotonic();stats={'status':'IN_PROGRESS','A_variants':len(a),'B_variants':len(b),
 'paired_candidates':(1+len(a))*(1+len(b))-1,'orthogonal_pairs_found':0,'eight_pack_pairs':0,
 'max_pack_found':0,'max_transversal_count':0,'valid_pair_records':[],
 'verified_full_solution':None,'independent_control':'Egan A/B 14 transversals max 7'}
 best=7
 # Include every combination of zero/one trade from each square, excluding original-original.
 for ia,(AA,ra) in enumerate([(A,{'base':True})]+a):
  for ib,(BB,rb) in enumerate([(B,{'base':True})]+b):
   if ia==ib==0:continue
   best=visit_pair(AA,BB,{'A':ra,'B':rb},best,stats)
   if stats['verified_full_solution'] is not None:break
  if stats['verified_full_solution'] is not None:break
 stats['status']='CLOSED_VERIFIED' if stats['verified_full_solution'] is not None else 'LOCAL_NEIGHBORHOOD_EXHAUSTED_OPEN'
 stats['seconds']=round(time.monotonic()-t0,4)
 stats['orthogonal_pair_sources']=len(stats['valid_pair_records'])
 out=D/'E063_COTRADE_RESULTS.json';out.write_text(json.dumps(stats,indent=2)+'\n')
 print('RESULT',json.dumps({k:v for k,v in stats.items() if k not in ('valid_pair_records','verified_full_solution')},indent=2))
 print('valid pairs',stats['valid_pair_records'][:4],flush=True)

if __name__=='__main__':main()